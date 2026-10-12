#!/usr/bin/env python3
"""
audit_vault.py - deterministic rule checker for the layered Obsidian knowledge base.

Usage:
  python audit_vault.py <vault_root> [--scope PATH ...] [--format md|json]
                        [--min-severity INFO|WARN|ERROR] [--config rules.json]

Exit codes: 0 = no ERROR findings, 1 = at least one ERROR finding, 2 = script/usage failure.

Stdlib only. The graph (links, titles, reachability) is always computed over the WHOLE
vault; --scope only filters which files findings are reported for.
Folder names and thresholds can be overridden with --config (JSON with the same keys as DEFAULTS).
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict, deque
from datetime import date, datetime

DEFAULTS = {
    "folders": {
        "inbox": "00 Inbox",
        "concepts": "10 Concepts",
        "flows": "20 Flows",
        "maps": "30 Maps",
        "diagrams": "40 Diagrams",
        "sources": "50 Sources",
        "projects": "60 Projects",
        "journal": "70 Journal",
        "archive": "90 Archive",
        "templates": "_Templates",
        "attachments": "_Attachments",
    },
    "home": "Home.canvas",
    "root_file_allowlist": ["README.md", "AGENTS.md", "CLAUDE.md", ".gitignore"],
    "thresholds": {
        "concept_words_warn": 350,
        "concept_words_error": 700,
        "flow_words_info": 2500,
        "map_links_warn": 40,
        "map_links_min": 3,
        "max_depth_from_home": 4,
        "home_nodes_warn": 12,
        "diagram_nodes_warn": 30,
        "diagram_unlinked_words": 25,
        "inbox_days_warn": 14,
        "inbox_days_error": 60,
        "seed_days_info": 90,
        "review_days_info": 90,
        "premature_extraction_days": 30,
        "min_section_words_evergreen": 5,
    },
}

TYPE_BY_FOLDER = {
    "inbox": {"scratch", None},
    "concepts": {"concept"},
    "flows": {"flow"},
    "maps": {"map"},
    "sources": {"source"},
    "projects": {"project"},
    "journal": {"log"},
}
VALID_TYPES = {"concept", "flow", "scratch", "source", "map", "project", "log"}
VALID_STATUS = {"seed", "growing", "evergreen"}
REQUIRED_PROPS = {
    "concept": ["type", "status", "domain", "created"],
    "flow": ["type", "status", "domain", "created"],
    "map": ["type", "created"],
    "source": ["type", "created"],
    "project": ["type", "created"],
    "log": ["type"],
}
REQUIRED_SECTIONS = {
    "concept": {
        "Definition": r"definition",
        "Invariants": r"invariant|rules",
        "Prerequisites": r"prerequisite",
    },
    "flow": {
        "Question": r"question",
        "Walkthrough": r"walkthrough",
        "Key insights": r"insight|why it works",
        "Open questions": r"open question",
    },
}
SIDEWAYS_SECTION = re.compile(r"see also|related|often confused|confused with", re.I)

# Link policy: which target kinds each source type may NOT link to from its body.
FORBIDDEN_TARGETS = {
    "concept": {"flow", "map", "diagram", "canvas", "project", "journal"},
    "flow": {"map", "diagram", "canvas", "project", "journal"},
}

RULES = {
    "STR-01": "Unknown item at vault root",
    "STR-02": "Loose note at vault root",
    "STR-03": "Required folder or Home canvas missing",
    "STR-04": "Subfolder inside a flat folder (Concepts/Flows/Maps/Diagrams)",
    "STR-05": "`type` property does not match the folder",
    "STR-06": "Markdown note inside Diagrams that is not an Excalidraw file",
    "STR-07": "Attachment stored outside _Attachments/Diagrams",
    "STR-08": "Filename contains characters that break wiki-links",
    "FM-01": "Required frontmatter property missing",
    "FM-02": "Frontmatter value outside allowed set",
    "FM-03": "`domain` is not a link to an existing Map",
    "FM-04": "`created` is not an ISO date",
    "DEP-01": "Body link points outward (violates the dependency rule)",
    "DEP-02": "Prerequisite cycle among Concepts",
    "DEP-04": "Flow does not link or embed any Concept",
    "DEP-05": "Link to Inbox (unprocessed) or Archive from a structured note",
    "ATM-01": "Concept note too long to be atomic",
    "ATM-02": "Required section missing",
    "ATM-03": "Evergreen note has an empty required section",
    "ATM-04": "Concept title is a question or contains a date",
    "ATM-05": "Flow title/length smell",
    "ATM-06": "Possible premature extraction (concept referenced < 2 times)",
    "NAV-01": "Broken link",
    "NAV-02": "Duplicate note name (ambiguous links)",
    "NAV-03": "Note not reachable from Home through Maps",
    "NAV-04": "Note too deep from Home",
    "NAV-05": "Map size smell (too many / too few links)",
    "NAV-07": "Home canvas too crowded",
    "NAV-08": "Alias collides with another note name",
    "DGM-01": "Diagram not linked or embedded from any Map",
    "DGM-02": "Diagram contains no [[links]] to notes",
    "DGM-03": "Diagram too large (split into a sub-diagram)",
    "DGM-04": "Knowledge trapped in diagram (long unlinked text)",
    "LIF-01": "Inbox item overdue for processing",
    "LIF-02": "Seed note has not matured",
    "RET-01": "Map/diagram has no recent review (retrieval loop)",
}

SEV_ORDER = {"INFO": 0, "WARN": 1, "ERROR": 2}

WIKILINK = re.compile(
    r"(!?)\[\[([^\]\|#\^]+?)(?:#[^\]\|]*)?(?:\^[^\]\|]*)?(?:\|[^\]]*)?\]\]"
)
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
BLOCK_ID_END = re.compile(r"\s\^[A-Za-z0-9]{6,}\s*$")
INVALID_NAME_CHARS = re.compile(r"[#\^\[\]\|]")
DATE_IN_TITLE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
WORD = re.compile(r"[A-Za-zÀ-ÿ0-9_'’-]+")


def deep_merge(base, over):
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            deep_merge(base[k], v)
        else:
            base[k] = v
    return base


# ----------------------------------------------------------------------------- parsing

def parse_frontmatter(text):
    """Minimal YAML subset: scalars, inline lists, block lists. Returns (dict, body)."""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not m:
        return {}, text
    block, body = m.group(1), text[m.end():]
    fm, key = {}, None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if re.match(r"^\s+-\s+", raw) and key is not None:
            item = re.sub(r"^\s+-\s+", "", raw).strip().strip("\"'")
            if not isinstance(fm.get(key), list):
                fm[key] = []
            fm[key].append(item)
            continue
        km = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", raw)
        if not km:
            continue
        key, val = km.group(1), km.group(2).strip()
        if val == "":
            fm[key] = ""
        elif val.startswith("[") and not val.startswith("[["):
            inner = val.strip("[]")
            fm[key] = [v.strip().strip("\"'") for v in inner.split(",") if v.strip()]
        else:
            fm[key] = val.strip("\"'")
    return fm, body


def scan_body(body):
    """Return (links, headings, sections) with code blocks / inline code removed.
    links: [{target, embed, section}], sections: {heading_lower: text}"""
    links, sections = [], defaultdict(list)
    headings, in_code, current = [], False, "(preamble)"
    for line in body.splitlines():
        if line.strip().startswith("```") or line.strip().startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        hm = HEADING.match(line)
        if hm:
            current = hm.group(2).strip()
            headings.append((len(hm.group(1)), current))
            continue
        sections[current.lower()].append(line)
        for m in WIKILINK.finditer(line):
            links.append({"target": m.group(2).strip(), "embed": bool(m.group(1)), "section": current})
    return links, headings, {k: "\n".join(v) for k, v in sections.items()}


def count_words(text):
    return len(WORD.findall(text))


def parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(str(val)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


class Note:
    def __init__(self, rel, abspath, folder_key, kind):
        self.rel, self.abspath, self.folder_key, self.kind = rel, abspath, folder_key, kind
        self.name = os.path.basename(rel)
        self.title = self.name
        self.fm, self.body = {}, ""
        self.links, self.headings, self.sections = [], [], {}
        self.words = 0
        self.mtime = date.fromtimestamp(os.path.getmtime(abspath))
        self.canvas_nodes = []
        self.text_elements = []  # for excalidraw: list of strings

    @property
    def ntype(self):
        t = self.fm.get("type")
        return t if isinstance(t, str) and t else None

    @property
    def created(self):
        return parse_date(self.fm.get("created")) or self.mtime

    @property
    def effective_kind(self):
        """Layer kind used by the link policy."""
        if self.kind == "excalidraw":
            return "diagram"
        if self.kind == "canvas":
            return "canvas"
        return {
            "concepts": "concept", "flows": "flow", "maps": "map", "inbox": "inbox",
            "sources": "source", "projects": "project", "journal": "journal",
            "archive": "archive", "diagrams": "diagram",
        }.get(self.folder_key, "other")


# ----------------------------------------------------------------------------- vault load

def load_vault(root, cfg):
    folders = cfg["folders"]
    key_by_folder = {v: k for k, v in folders.items()}
    notes, attachments, root_items = [], {}, sorted(os.listdir(root))
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for fn in filenames:
            if fn.startswith("."):
                continue
            absp = os.path.join(dirpath, fn)
            rel = os.path.relpath(absp, root).replace(os.sep, "/")
            first = rel.split("/")[0] if "/" in rel else None
            folder_key = key_by_folder.get(first, "root" if first is None else "unknown")
            low = fn.lower()
            if low.endswith(".excalidraw.md"):
                kind = "excalidraw"
            elif low.endswith(".md"):
                kind = "md"
            elif low.endswith(".canvas"):
                kind = "canvas"
            elif low.endswith(".base"):
                kind = "base"
            elif low.endswith(".excalidraw"):
                kind = "excalidraw_raw"
            else:
                attachments[low] = rel
                kind = "attachment"
                n = Note(rel, absp, folder_key, kind)
                notes.append(n)
                continue
            n = Note(rel, absp, folder_key, kind)
            try:
                with open(absp, encoding="utf-8") as fh:
                    raw = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            if kind in ("md", "excalidraw"):
                n.fm, n.body = parse_frontmatter(raw)
                n.title = fn[:-len(".excalidraw.md")] if kind == "excalidraw" else fn[:-3]
                if folder_key != "templates":
                    n.links, n.headings, n.sections = scan_body(n.body)
                n.words = count_words("\n".join(n.sections.values()))
                if kind == "excalidraw":
                    n.text_elements = parse_excalidraw_text(n.body)
            elif kind == "canvas":
                n.title = fn
                try:
                    data = json.loads(raw)
                    n.canvas_nodes = data.get("nodes", [])
                except json.JSONDecodeError:
                    n.canvas_nodes = []
                for node in n.canvas_nodes:
                    if node.get("type") == "file" and node.get("file"):
                        n.links.append({"target": node["file"], "embed": False, "section": "canvas"})
                    elif node.get("type") == "text":
                        for m in WIKILINK.finditer(node.get("text", "")):
                            n.links.append({"target": m.group(2).strip(), "embed": False, "section": "canvas"})
            else:
                n.title = fn
            notes.append(n)
    return notes, root_items


def parse_excalidraw_text(body):
    m = re.search(r"##\s*Text Elements\s*\n(.*?)(?:\n%%|\n##\s|\Z)", body, re.S)
    if not m:
        return []
    elems, buf = [], []
    for line in m.group(1).splitlines():
        buf.append(line)
        if BLOCK_ID_END.search(line):
            elems.append("\n".join(buf))
            buf = []
    return [BLOCK_ID_END.sub("", e).strip() for e in elems if e.strip()]


def build_index(notes):
    idx = defaultdict(list)
    for n in notes:
        if n.folder_key == "templates":
            continue
        if n.kind == "md":
            idx[n.title.lower()].append(n)
        elif n.kind == "excalidraw":
            idx[n.title.lower()].append(n)
            idx[(n.title + ".excalidraw").lower()].append(n)
        elif n.kind in ("canvas", "base", "attachment", "excalidraw_raw"):
            idx[n.name.lower()].append(n)
    return idx


def resolve(target, idx):
    t = target.strip().replace("\\", "/")
    t = t.split("/")[-1]
    key = t.lower()
    if key.endswith(".md"):
        key = key[:-3]
    return idx.get(key, [])


def resolve_canvas_path(target, by_rel):
    return by_rel.get(target)


# ----------------------------------------------------------------------------- audit

class Auditor:
    def __init__(self, root, cfg):
        self.root, self.cfg = root, cfg
        self.th = cfg["thresholds"]
        self.findings = []
        self.rules_run = set()
        self.today = date.today()
        self.notes, self.root_items = load_vault(root, cfg)
        self.by_rel = {n.rel: n for n in self.notes}
        self.idx = build_index(self.notes)
        self.stats = {}

    def add(self, rule, sev, file, msg, fix=""):
        self.findings.append({"rule": rule, "severity": sev, "file": file, "message": msg, "fix": fix})

    def structured(self):
        for n in self.notes:
            if n.kind in ("md", "excalidraw") and n.folder_key not in ("templates", "archive", "unknown", "root"):
                yield n

    # -- resolved links ---------------------------------------------------------------
    def resolved_links(self, n):
        out = []
        for ln in n.links:
            if n.kind == "canvas":
                t = self.by_rel.get(ln["target"])
                targets = [t] if t else resolve(ln["target"], self.idx)
            else:
                targets = resolve(ln["target"], self.idx)
            out.append((ln, targets[0] if targets else None))
        return out

    def all_targets(self, n):
        """Like resolved_links but yields every candidate for ambiguous names (duplicates are
        reported separately by NAV-02; this avoids cascading false 'unreachable' errors)."""
        out = []
        for ln in n.links:
            if n.kind == "canvas":
                t = self.by_rel.get(ln["target"])
                cands = [t] if t else resolve(ln["target"], self.idx)
            else:
                cands = resolve(ln["target"], self.idx)
            for c in cands:
                out.append((ln, c))
        return out

    # -- checks -----------------------------------------------------------------------
    def check_structure(self):
        f = self.cfg["folders"]
        for r in ("STR-01", "STR-02", "STR-03", "STR-04", "STR-05", "STR-06", "STR-07", "STR-08"):
            self.rules_run.add(r)
        allowed_root = set(f.values()) | {self.cfg["home"]} | set(self.cfg["root_file_allowlist"])
        for item in self.root_items:
            if item.startswith("."):
                continue
            if item not in allowed_root:
                path = os.path.join(self.root, item)
                if os.path.isfile(path) and item.lower().endswith(".md"):
                    self.add("STR-02", "ERROR", item, "Note sits at the vault root.",
                             "Move it to 00 Inbox (if unprocessed) or the folder matching its type.")
                else:
                    self.add("STR-01", "WARN", item, "Item is not part of the defined root layout.",
                             "Move it into the right folder or add it to the config allowlist.")
        core = ["inbox", "concepts", "flows", "maps", "diagrams"]
        for key, name in f.items():
            if not os.path.isdir(os.path.join(self.root, name)):
                sev = "ERROR" if key in core else "WARN"
                self.add("STR-03", sev, name + "/", "Required folder is missing.", f"Create '{name}/'.")
        if not os.path.exists(os.path.join(self.root, self.cfg["home"])):
            self.add("STR-03", "ERROR", self.cfg["home"], "Home canvas is missing.",
                     "Create Home.canvas at the vault root: one node per domain Map.")

        for n in self.notes:
            if n.folder_key in ("templates",):
                continue
            parts = n.rel.split("/")
            if n.kind == "attachment":
                if n.folder_key not in ("attachments", "diagrams", "archive"):
                    self.add("STR-07", "WARN", n.rel, "Attachment stored outside _Attachments.",
                             "Move it to _Attachments/ (Obsidian: set 'Default location for new attachments').")
                continue
            if n.kind in ("md", "excalidraw") and INVALID_NAME_CHARS.search(n.title):
                self.add("STR-08", "ERROR", n.rel, "Filename contains one of # ^ [ ] | which break wiki-links.",
                         "Rename the file.")
            if n.folder_key in ("concepts", "flows", "maps", "diagrams") and len(parts) > 2:
                sev = "WARN" if n.folder_key == "diagrams" else "ERROR"
                self.add("STR-04", sev, n.rel, f"{self.cfg['folders'][n.folder_key]} must stay flat but this file is in a subfolder.",
                         "Move it to the folder root; express topic via a Map and the `domain` property.")
            if n.kind == "md" and n.folder_key == "diagrams":
                self.add("STR-06", "ERROR", n.rel, "Plain Markdown note inside Diagrams.",
                         "Diagrams holds only Excalidraw files. Move the note to the folder for its type.")
            if n.kind == "md" and n.folder_key in TYPE_BY_FOLDER:
                allowed = TYPE_BY_FOLDER[n.folder_key]
                t = n.ntype
                if t not in allowed and not (n.folder_key == "inbox" and t is None):
                    self.add("STR-05", "ERROR", n.rel,
                             f"type is '{t}' but the folder expects {sorted(x for x in allowed if x)}.",
                             "Either move the note or correct `type` (the property is the source of truth).")

    def check_frontmatter(self):
        for r in ("FM-01", "FM-02", "FM-03", "FM-04"):
            self.rules_run.add(r)
        maps = {n.title.lower() for n in self.notes if n.folder_key == "maps" and n.kind == "md"}
        for n in self.structured():
            if n.kind != "md" or n.folder_key in ("inbox", "diagrams"):
                continue
            t = n.ntype
            if t is None:
                self.add("FM-01", "ERROR", n.rel, "`type` property is missing.", "Add `type:` matching the folder.")
                continue
            if t not in VALID_TYPES:
                self.add("FM-02", "ERROR", n.rel, f"type '{t}' is not one of {sorted(VALID_TYPES)}.")
                continue
            for p in REQUIRED_PROPS.get(t, []):
                if not n.fm.get(p):
                    self.add("FM-01", "ERROR", n.rel, f"Required property `{p}` is missing or empty.",
                             f"Add `{p}:` (see references/templates.md).")
            st = n.fm.get("status")
            if st and st not in VALID_STATUS:
                self.add("FM-02", "ERROR", n.rel, f"status '{st}' is not one of {sorted(VALID_STATUS)}.")
            if n.fm.get("created") and not re.match(r"^\d{4}-\d{2}-\d{2}", str(n.fm["created"])):
                self.add("FM-04", "WARN", n.rel, "`created` should be an ISO date (YYYY-MM-DD).")
            if t in ("concept", "flow") and n.fm.get("domain"):
                m = WIKILINK.search(str(n.fm["domain"]))
                ok = bool(m) and m.group(2).strip().lower() in maps
                if not ok:
                    self.add("FM-03", "ERROR", n.rel,
                             f"`domain` ('{n.fm['domain']}') is not a [[link]] to an existing Map.",
                             "Set domain to a quoted wiki-link to a note in 30 Maps, e.g. domain: \"[[Distributed Systems]]\".")

    def check_links(self):
        for r in ("NAV-01", "NAV-02", "DEP-01", "DEP-05", "NAV-08"):
            self.rules_run.add(r)
        # duplicates
        seen = defaultdict(list)
        for n in self.notes:
            if n.kind in ("md", "excalidraw") and n.folder_key not in ("templates",):
                seen[n.title.lower()].append(n)
        for title, group in seen.items():
            if len(group) > 1:
                paths = ", ".join(g.rel for g in group)
                for g in group:
                    self.add("NAV-02", "ERROR", g.rel, f"Name '{g.title}' is used by several notes: {paths}.",
                             "Titles must be unique vault-wide; rename or merge.")
        # aliases
        for n in self.structured():
            al = n.fm.get("aliases")
            for a in (al if isinstance(al, list) else [al] if al else []):
                others = [o for o in seen.get(str(a).lower(), []) if o is not n]
                if others:
                    self.add("NAV-08", "WARN", n.rel, f"Alias '{a}' equals the name of {others[0].rel}.")
        # per-link checks
        for n in self.notes:
            if n.kind not in ("md", "excalidraw", "canvas") or n.folder_key == "templates":
                continue
            for ln, tgt in self.resolved_links(n):
                if tgt is None:
                    self.add("NAV-01", "ERROR", n.rel, f"Broken link [[{ln['target']}]] (section: {ln['section']}).",
                             "Fix the target name or create the missing note.")
                    continue
                src_kind = n.effective_kind
                tk = tgt.effective_kind
                if n.kind == "md" and src_kind in ("concept", "flow", "map") and tk == "inbox":
                    self.add("DEP-05", "ERROR", n.rel, f"Links to unprocessed Inbox note [[{tgt.title}]].",
                             "Process the Inbox note first or remove the link.")
                if n.kind == "md" and src_kind in ("concept", "flow", "map") and tk == "archive":
                    self.add("DEP-05", "WARN", n.rel, f"Links to archived note [[{tgt.title}]].")
                if n.kind == "md" and src_kind in FORBIDDEN_TARGETS and tk in FORBIDDEN_TARGETS[src_kind]:
                    self.add("DEP-01", "ERROR", n.rel,
                             f"{src_kind.capitalize()} links outward to {tk} [[{tgt.title}]] "
                             f"(section: {ln['section']}).",
                             "Remove the link; let the outer layer (Flow/Map/Diagram) reference this note instead.")

    def check_cycles(self):
        self.rules_run.add("DEP-02")
        concepts = {n.rel: n for n in self.structured() if n.folder_key == "concepts" and n.kind == "md"}
        graph = {rel: [] for rel in concepts}
        for rel, n in concepts.items():
            for ln, tgt in self.resolved_links(n):
                if tgt and tgt.rel in concepts and tgt.rel != rel and not SIDEWAYS_SECTION.search(ln["section"]):
                    graph[rel].append(tgt.rel)
        # iterative Tarjan SCC
        index, low, onstack, stack, sccs, counter = {}, {}, set(), [], [], [0]
        for start in graph:
            if start in index:
                continue
            work = [(start, iter(graph[start]))]
            index[start] = low[start] = counter[0]
            counter[0] += 1
            stack.append(start)
            onstack.add(start)
            while work:
                v, it = work[-1]
                adv = False
                for w in it:
                    if w not in index:
                        index[w] = low[w] = counter[0]
                        counter[0] += 1
                        stack.append(w)
                        onstack.add(w)
                        work.append((w, iter(graph[w])))
                        adv = True
                        break
                    elif w in onstack:
                        low[v] = min(low[v], index[w])
                if adv:
                    continue
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = stack.pop()
                        onstack.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    if len(comp) > 1:
                        sccs.append(comp)
        for comp in sccs:
            names = ", ".join(sorted(concepts[c].title for c in comp))
            for c in comp:
                self.add("DEP-02", "ERROR", c, f"Prerequisite cycle among concepts: {names}.",
                         "Keep prerequisites one-directional; move the sideways reference into a 'See also' section.")

    def check_atomicity(self):
        for r in ("ATM-01", "ATM-02", "ATM-03", "ATM-04", "ATM-05", "ATM-06", "DEP-04"):
            self.rules_run.add(r)
        inbound = defaultdict(list)
        for n in self.notes:
            if n.kind not in ("md", "excalidraw", "canvas") or n.folder_key == "templates":
                continue
            for ln, tgt in self.all_targets(n):
                if tgt is not n:
                    inbound[tgt.rel].append(n)
        self.inbound = inbound
        th = self.th
        for n in self.structured():
            if n.kind != "md" or n.folder_key not in ("concepts", "flows"):
                continue
            t = n.ntype
            status = n.fm.get("status", "seed")
            req = REQUIRED_SECTIONS.get(t, {})
            heads = {h[1].lower(): h[1] for h in n.headings}
            missing = []
            for label, pat in req.items():
                found = next((h for h in heads if re.search(pat, h, re.I)), None)
                if found is None:
                    missing.append(label)
                elif status == "evergreen":
                    txt = n.sections.get(found, "")
                    explicit_none = re.search(r"prerequisite", found, re.I) and re.match(r"^\s*(none|n/a)\b", txt, re.I)
                    if count_words(txt) < th["min_section_words_evergreen"] and not explicit_none:
                        self.add("ATM-03", "ERROR", n.rel, f"Evergreen note has an empty/near-empty '{found}' section.",
                                 "Fill it in (write 'None - <reason>' for no prerequisites) or demote status to growing.")
            if missing:
                sev = "INFO" if status == "seed" else "ERROR"
                self.add("ATM-02", sev, n.rel, f"Missing section(s): {', '.join(missing)}.",
                         "Add them (see references/templates.md)." if sev == "ERROR"
                         else "Acceptable for a seed; add before promoting to growing.")
            if t == "concept":
                if n.words > th["concept_words_error"]:
                    self.add("ATM-01", "ERROR", n.rel, f"Concept has {n.words} words; it likely holds several ideas.",
                             "Split into several concepts and move the narrative into a Flow.")
                elif n.words > th["concept_words_warn"]:
                    self.add("ATM-01", "WARN", n.rel, f"Concept has {n.words} words; check it is one idea.")
                if n.title.endswith("?") or DATE_IN_TITLE.search(n.title):
                    self.add("ATM-04", "WARN", n.rel, "Concept titles must be stable noun phrases (no question, no date).",
                             "Rename (Obsidian updates links).")
                non_map = [s for s in inbound.get(n.rel, []) if s.effective_kind not in ("map", "diagram", "canvas")]
                age = (self.today - n.created).days
                if len(non_map) < 2 and age > th["premature_extraction_days"]:
                    self.add("ATM-06", "INFO", n.rel,
                             f"Referenced by only {len(non_map)} Flow/Concept note(s) after {age} days. "
                             "Extraction rule: extract on the second reference.",
                             "Keep if it is a foundational prerequisite; otherwise inline it into the Flow that uses it.")
            if t == "flow":
                if not n.title.endswith("?"):
                    self.add("ATM-05", "INFO", n.rel, "Flow titles are conventionally phrased as a question.")
                if n.words > th["flow_words_info"]:
                    self.add("ATM-05", "INFO", n.rel, f"Flow has {n.words} words; consider splitting into two flows "
                             "or extracting repeated concepts.")
                has_concept = False
                for ln, tgt in self.resolved_links(n):
                    if tgt is not None and tgt.effective_kind == "concept":
                        has_concept = True
                        break
                if not has_concept:
                    sev = "INFO" if status == "seed" else "WARN"
                    self.add("DEP-04", sev, n.rel, "Flow neither links nor embeds any Concept note.",
                             "Extract recurring ideas into Concepts, or confirm this should stay a scratch note.")

    def check_navigation(self):
        for r in ("NAV-03", "NAV-04", "NAV-05", "NAV-07", "DGM-01"):
            self.rules_run.add(r)
        home = self.by_rel.get(self.cfg["home"])
        th = self.th
        depth, order = {}, deque()
        base_maps = set()
        if home:
            if len(home.canvas_nodes) > th["home_nodes_warn"]:
                self.add("NAV-07", "WARN", home.rel, f"Home has {len(home.canvas_nodes)} nodes (> {th['home_nodes_warn']}).",
                         "Group domains; Home should hold roughly one node per domain Map.")
            for ln, tgt in self.all_targets(home):
                if tgt.rel not in depth:
                    depth[tgt.rel] = 1
                    order.append(tgt)
        while order:
            cur = order.popleft()
            if cur.effective_kind != "map":
                continue
            for ln, tgt in self.all_targets(cur):
                if tgt.name.lower().endswith(".base"):
                    base_maps.add(cur.rel)
                if tgt.rel not in depth:
                    depth[tgt.rel] = depth[cur.rel] + 1
                    order.append(tgt)
        self.depth = depth
        maps_with_base = {self.by_rel[r].title.lower() for r in base_maps}
        for n in self.structured():
            if n.folder_key not in ("concepts", "flows", "maps", "diagrams"):
                continue
            if n.rel in depth:
                if depth[n.rel] > th["max_depth_from_home"]:
                    self.add("NAV-04", "WARN", n.rel, f"{depth[n.rel]} hops from Home (max {th['max_depth_from_home']}).",
                             "Link it from a shallower Map or flatten the Map hierarchy.")
                continue
            dom = WIKILINK.search(str(n.fm.get("domain", "")))
            if dom and dom.group(2).strip().lower() in maps_with_base and n.folder_key in ("concepts", "flows"):
                self.add("NAV-03", "INFO", n.rel,
                         "Reachability relies on a Base embed in its domain Map (dynamic membership not verifiable by script).",
                         "Open the Map and confirm the Base filter includes this note.")
                continue
            what = "Map" if n.folder_key == "maps" else "Diagram" if n.folder_key == "diagrams" else "note"
            if n.folder_key == "diagrams":
                continue  # handled by DGM-01
            self.add("NAV-03", "ERROR", n.rel, f"{what} is not reachable from Home through Maps.",
                     "Link it from the relevant Map" if what == "note" else "Link this Map from a parent Map or from Home.")
        # map size
        for n in self.structured():
            if n.folder_key != "maps" or n.kind != "md":
                continue
            outl = {t.rel for _, t in self.resolved_links(n) if t is not None}
            if len(outl) > th["map_links_warn"]:
                self.add("NAV-05", "WARN", n.rel, f"Map has {len(outl)} links; split it into sub-Maps.")
            elif len(outl) < th["map_links_min"]:
                self.add("NAV-05", "INFO", n.rel, f"Map has only {len(outl)} links; maps are created when 7-10 notes cluster.")
        # diagrams linked from a Map
        for n in self.structured():
            if n.kind != "excalidraw":
                continue
            if not any(s.effective_kind == "map" for s in self.inbound.get(n.rel, [])):
                self.add("DGM-01", "WARN", n.rel, "Diagram is not linked or embedded from any Map.",
                         "Embed it in the Map of its domain.")

    def check_diagrams(self):
        for r in ("DGM-02", "DGM-03", "DGM-04"):
            self.rules_run.add(r)
        th = self.th
        for n in self.structured():
            if n.kind != "excalidraw":
                continue
            elems = n.text_elements
            linked = [e for e in elems if WIKILINK.search(e)]
            if not linked:
                self.add("DGM-02", "WARN", n.rel, "No [[links]] to notes found in the diagram's text elements.",
                         "Link key nodes to Concept/Flow notes so the diagram works as navigation.")
            if len(elems) > th["diagram_nodes_warn"]:
                self.add("DGM-03", "WARN", n.rel, f"{len(elems)} text elements (> {th['diagram_nodes_warn']}); "
                         "edge labels count too, so treat as a heuristic.",
                         "Split into a top-level diagram whose nodes link to sub-diagrams.")
            for e in elems:
                if not WIKILINK.search(e) and count_words(e) > th["diagram_unlinked_words"]:
                    snippet = e.replace("\n", " ")[:70]
                    self.add("DGM-04", "WARN", n.rel, f"Long unlinked text ({count_words(e)} words): '{snippet}...'",
                             "Move the knowledge into a Concept/Flow note and link the node to it.")

    def check_lifecycle(self):
        for r in ("LIF-01", "LIF-02", "RET-01"):
            self.rules_run.add(r)
        th = self.th
        for n in self.notes:
            if n.kind != "md":
                continue
            if n.folder_key == "inbox":
                age = (self.today - n.created).days
                if age > th["inbox_days_error"]:
                    self.add("LIF-01", "ERROR", n.rel, f"In Inbox for {age} days.", "Process, archive, or delete.")
                elif age > th["inbox_days_warn"]:
                    self.add("LIF-01", "WARN", n.rel, f"In Inbox for {age} days.", "Do the weekly processing pass.")
            if n.folder_key in ("concepts", "flows") and n.fm.get("status") == "seed":
                age = (self.today - n.created).days
                if age > th["seed_days_info"]:
                    self.add("LIF-02", "INFO", n.rel, f"Still a seed after {age} days.", "Promote, merge, or discard.")
        for n in self.structured():
            if n.folder_key in ("maps", "diagrams"):
                rev = parse_date(n.fm.get("reviewed"))
                ref = rev or n.created
                age = (self.today - ref).days
                if age > th["review_days_info"]:
                    what = "reviewed" if rev else "created (never reviewed)"
                    self.add("RET-01", "INFO", n.rel,
                             f"Last {what} {age} days ago. Redraw it from memory on a blank canvas, then set `reviewed:`.")

    # -- orchestrate ------------------------------------------------------------------
    def run(self):
        self.check_structure()
        self.check_frontmatter()
        self.check_links()
        self.check_cycles()
        self.check_atomicity()
        self.check_navigation()
        self.check_diagrams()
        self.check_lifecycle()
        by_kind = defaultdict(int)
        for n in self.notes:
            if n.kind in ("md", "excalidraw"):
                by_kind[n.folder_key] += 1
        self.stats = {
            "notes_by_folder": dict(sorted(by_kind.items())),
            "max_depth_from_home": max(self.depth.values()) if getattr(self, "depth", None) else 0,
            "reachable_from_home": len(getattr(self, "depth", {})),
            "home_nodes": len(self.by_rel[self.cfg["home"]].canvas_nodes) if self.cfg["home"] in self.by_rel else 0,
        }


# ----------------------------------------------------------------------------- output

def in_scope(file, scopes):
    if not scopes or not file:
        return True
    return any(file == s or file.startswith(s.rstrip("/") + "/") for s in scopes)


def render_md(aud, findings, scopes):
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in ("ERROR", "WARN", "INFO")}
    verdict = "FAIL" if counts["ERROR"] else "PASS WITH WARNINGS" if counts["WARN"] else "PASS"
    out = [f"# Knowledge base audit - {verdict}", ""]
    out.append(f"Vault: `{aud.root}`  |  Date: {aud.today}  |  Scope: {', '.join(scopes) if scopes else 'whole vault'}")
    out.append(f"Errors: **{counts['ERROR']}**  Warnings: **{counts['WARN']}**  Info: **{counts['INFO']}**")
    out.append("")
    out.append("## Vault stats")
    for k, v in aud.stats.items():
        out.append(f"- {k}: {v}")
    out.append("")
    out.append("## Checks executed")
    by_rule = defaultdict(list)
    for f in findings:
        by_rule[f["rule"]].append(f)
    for rid in sorted(aud.rules_run):
        fs = by_rule.get(rid, [])
        mark = "FAIL" if any(f["severity"] == "ERROR" for f in fs) else "WARN" if any(f["severity"] == "WARN" for f in fs) \
            else "info" if fs else "ok"
        out.append(f"- [{mark}] {rid} - {RULES.get(rid, '')} ({len(fs)})")
    out.append("")
    for sev in ("ERROR", "WARN", "INFO"):
        group = [f for f in findings if f["severity"] == sev]
        if not group:
            continue
        out.append(f"## {sev} ({len(group)})")
        group.sort(key=lambda f: (f["rule"], f["file"] or ""))
        for f in group:
            loc = f["file"] or "(vault)"
            line = f"- **{f['rule']}** `{loc}` - {f['message']}"
            if f["fix"]:
                line += f"  \n  Fix: {f['fix']}"
            out.append(line)
        out.append("")
    out.append("> Script findings are mechanical. Semantic rules (is it ONE idea? are edges labeled? is the "
               "diagram one question?) still need the manual review in references/rules.md.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vault")
    ap.add_argument("--scope", nargs="*", default=[], help="vault-relative files/folders to report on")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--min-severity", choices=list(SEV_ORDER), default="INFO")
    ap.add_argument("--config", help="JSON file overriding DEFAULTS")
    args = ap.parse_args()

    root = os.path.abspath(args.vault)
    if not os.path.isdir(root):
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    cfg = json.loads(json.dumps(DEFAULTS))
    if args.config:
        with open(args.config, encoding="utf-8") as fh:
            deep_merge(cfg, json.load(fh))
    aud = Auditor(root, cfg)
    aud.run()
    scopes = [s.replace("\\", "/").strip("/") for s in args.scope]
    findings = [f for f in aud.findings
                if in_scope(f["file"], scopes) and SEV_ORDER[f["severity"]] >= SEV_ORDER[args.min_severity]]
    if args.format == "json":
        print(json.dumps({"stats": aud.stats, "rules_run": sorted(aud.rules_run), "findings": findings}, indent=2))
    else:
        print(render_md(aud, findings, scopes))
    return 1 if any(f["severity"] == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001
        print(f"audit_vault.py failed: {exc!r}", file=sys.stderr)
        sys.exit(2)
