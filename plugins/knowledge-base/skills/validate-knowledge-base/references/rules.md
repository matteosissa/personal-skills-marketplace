# Rule catalogue

Severity: **ERROR** = violates a principle (blocks PASS). **WARN** = smell, fix soon. **INFO** = advisory.
"Verified by": `script` = `scripts/audit_vault.py` checks it; `manual` = you must read the files.

Exempt from all rules: `_Templates/`, `90 Archive/` (but structured notes must not link into it), dotfolders.
Inbox notes are exempt from frontmatter and structure rules; only age and "nothing structured links to Inbox" apply.

## Contents
1. Structure (STR)
2. Frontmatter (FM)
3. Dependencies (DEP)
4. Atomicity (ATM)
5. Navigation (NAV)
6. Diagrams (DGM)
7. Lifecycle and retrieval (LIF, RET)
8. Manual semantic checklist (M-01..M-12)
9. Fallback shell commands
10. Thresholds

---

## 1. Structure

| ID | Sev | Rule | Why | Verified by |
|---|---|---|---|---|
| STR-01 | WARN | Vault root contains only the defined folders, `Home.canvas`, and allow-listed files (README.md, AGENTS.md, CLAUDE.md) | Unknown places defeat "I always know where things are" | script |
| STR-02 | ERROR | No loose `.md` notes at the root | Every note has a kind; unprocessed goes to Inbox | script |
| STR-03 | ERROR/WARN | Core folders (Inbox, Concepts, Flows, Maps, Diagrams) and `Home.canvas` exist (ERROR); other folders WARN | Skeleton must be intact | script |
| STR-04 | ERROR | `10 Concepts`, `20 Flows`, `30 Maps` have no subfolders (Diagrams: WARN) | Topic lives in Maps/`domain`; topic folders rot | script |
| STR-05 | ERROR | `type` agrees with the folder (concept->10, flow->20, map->30, source->50, project->60, log->70, scratch->00) | Property is the source of truth; drift means two sources of truth | script |
| STR-06 | ERROR | `40 Diagrams` contains only `*.excalidraw.md` / `*.excalidraw` files (plus exported images) | Diagrams are a distinct layer | script |
| STR-07 | WARN | Binary attachments live in `_Attachments` (or Diagrams exports) | Keeps note folders clean | script |
| STR-08 | ERROR | Filenames contain none of `# ^ [ ] \|` | These break wiki-links | script |

## 2. Frontmatter

Required properties by type: concept/flow: `type, status, domain, created`; map/source/project: `type, created`; log: `type`.

| ID | Sev | Rule | Why | Verified by |
|---|---|---|---|---|
| FM-01 | ERROR | Required properties present and non-empty | Bases/queries and this audit depend on them | script |
| FM-02 | ERROR | `type` in {concept, flow, scratch, source, map, project, log}; `status` in {seed, growing, evergreen} | Closed vocabularies keep queries reliable | script |
| FM-03 | ERROR | `domain` (concepts, flows) is a quoted wiki-link to an existing Map, e.g. `"[[Distributed Systems]]"` | Ties every note to a navigation hub | script |
| FM-04 | WARN | `created` is ISO `YYYY-MM-DD` | Age-based rules need a date | script |

Frontmatter links (`domain`, `source`) are metadata and are exempt from the dependency rule.

## 3. Dependencies (body links only; frontmatter exempt)

Allowed outbound body links by source type:

| From | May link to | Must not link to |
|---|---|---|
| Concept | Concept (prerequisites; sideways only under "See also"), Source, attachments | Flow, Map, Diagram, Canvas, Project, Journal, Inbox |
| Flow | Concept, Source, other Flow, attachments | Map, Diagram, Canvas, Project, Journal, Inbox |
| Map | anything structured | Inbox |
| Diagram | anything | - |
| Source / Project / Journal / Inbox | anything | - |

| ID | Sev | Rule | Why | Verified by |
|---|---|---|---|---|
| DEP-01 | ERROR | No body link from Concept/Flow to a forbidden layer (table above) | The dependency rule: inner layers must not know about outer layers, else rewriting a Flow or redrawing a diagram forces edits to Concepts | script |
| DEP-02 | ERROR | Prerequisite links among Concepts form no cycle (links under "See also / Related / Often confused" are excluded) | A cyclic prerequisite graph has no learning order; mutual relations belong in "See also" | script |
| DEP-04 | WARN (INFO for seeds) | A Flow links or embeds at least one Concept | A Flow with no Concept is usually a scratch note, or its foundations were never extracted | script |
| DEP-05 | ERROR/WARN | Concepts, Flows, Maps do not link to Inbox (ERROR) or Archive (WARN) | Structured notes must not depend on unprocessed or retired material | script |

## 4. Atomicity

| ID | Sev | Rule | Why | Verified by |
|---|---|---|---|---|
| ATM-01 | WARN > 350 words, ERROR > 700 | A Concept is one idea and short | Long concepts hide several ideas; narrative belongs in a Flow | script (+ M-01) |
| ATM-02 | ERROR (INFO for seed) | Concepts have Definition, Invariants, Prerequisites; Flows have Question, Walkthrough, Key insights, Open questions | Fixed anatomy makes notes scannable and reviewable | script |
| ATM-03 | ERROR | `status: evergreen` notes have every required section filled (Prerequisites may say "None") | Evergreen is a promise of completeness | script |
| ATM-04 | WARN | Concept titles are stable noun phrases: no `?`, no dates | Stable names keep links valid for years | script |
| ATM-05 | INFO | Flow titles are questions; flows over ~2500 words deserve a look | A question gives the Flow a single purpose | script |
| ATM-06 | INFO | A Concept older than 30 days referenced by fewer than 2 Flow/Concept notes may be a premature extraction | Extract on the second reference | script (judgement: M-02) |

## 5. Navigation

| ID | Sev | Rule | Why | Verified by |
|---|---|---|---|---|
| NAV-01 | ERROR | No broken links (ignores `_Templates`) | Broken links are lost knowledge | script |
| NAV-02 | ERROR | Note names are unique vault-wide (case-insensitive) | Wiki-links resolve by name; duplicates make them ambiguous | script |
| NAV-03 | ERROR | Every Concept, Flow and Map is reachable from `Home.canvas` by walking through Maps. If reachability only relies on a Base embed in the domain Map, it is INFO and must be verified manually | "Where is everything?" must always have an answer | script (+ manual for Bases) |
| NAV-04 | WARN | Depth from Home is at most 4 hops | Stable, shallow navigation matches how people re-find personal information | script |
| NAV-05 | WARN > 40 links / INFO < 3 | Maps are neither bloated nor premature | Split at ~40; create when 7-10 notes cluster | script |
| NAV-07 | WARN | Home has at most ~12 nodes | Home is an index of domains, not a dump | script |
| NAV-08 | WARN | No alias equals another note's name | Prevents ambiguous resolution | script |

## 6. Diagrams

| ID | Sev | Rule | Why | Verified by |
|---|---|---|---|---|
| DGM-01 | WARN | Every diagram is linked or embedded from a Map | Diagrams are the visual layer of a Map | script |
| DGM-02 | WARN | Diagram has `[[links]]` to notes in its text elements | Diagram as navigation, depth one click away | script |
| DGM-03 | WARN | At most ~30 text elements (edge labels count; heuristic) | Beyond that a canvas becomes a wall; split into sub-diagrams | script |
| DGM-04 | WARN | No unlinked text element over 25 words | Knowledge must not live only in a drawing | script |
| (manual) | - | One question per diagram; edges labeled with verbs; consistent conventions | See M-05, M-06 | manual |

Note: Excalidraw compresses the drawing JSON by default; the script reads only the "Text Elements" section, which is always plain text.

## 7. Lifecycle and retrieval

| ID | Sev | Rule | Why | Verified by |
|---|---|---|---|---|
| LIF-01 | WARN > 14 days, ERROR > 60 | Inbox is processed regularly | The Inbox is the only unstructured place; if it grows it becomes a graveyard | script |
| LIF-02 | INFO | Seeds older than 90 days: promote, merge, or discard | Prevents permanent half-notes | script |
| RET-01 | INFO | Maps and diagrams carry a `reviewed:` date within 90 days (created date used if absent) | Retrieval practice and spaced review beat rereading; redraw from memory, compare, fix, update `reviewed:` | script |

---

## 8. Manual semantic checklist

Apply to every file in scope (or a sample of at least 10 per layer for big vaults - say that you sampled). Quote the offending line as evidence. Treat these as ERROR if the principle is clearly broken, WARN if arguable.

- **M-01 One idea per concept.** Could you state the concept in one sentence? Does the body mix a definition with a story, comparison, or tutorial? Fix: split, and move narrative to a Flow.
- **M-02 Invariants are rules.** "Invariants" must be statements that are always true (like business rules), not descriptions, examples, or opinions. Prerequisites must be real dependencies - if you can understand the concept without it, it is a "See also".
- **M-03 Concepts do not tell stories.** No "first/then" reasoning, no "in my project" context, no mention of how it was learned.
- **M-04 Flows answer their question.** The Question section states a concrete question; the Walkthrough actually answers it using Concepts; Key insights are conclusions, not restatements. Inline explanation is fine - a Flow should not be split just for length.
- **M-05 Diagrams answer one question** (stated in the title/filename or an obvious header text) and edges carry labels (verbs such as triggers, requires, breaks if). Unlabeled arrows lose the reasoning.
- **M-06 Diagram conventions are consistent**: direction (e.g. left-to-right for causality), colour per node type, same layout for similar topics.
- **M-07 Maps give context.** Each link in a Map has a short phrase saying why it is there; Maps are hand-curated, not file dumps. Sub-Maps are linked from a parent Map.
- **M-08 No knowledge only in a diagram.** Every non-trivial claim drawn is also recoverable from a linked note.
- **M-09 Own words.** Pasted text, quotes, or slabs copied from sources are a smell. Provenance belongs in a Source note and a link.
- **M-10 Provenance.** Growing/evergreen Concepts and Flows should be traceable to a Source or the user's own work; flag unsupported evergreen claims as WARN.
- **M-11 Titles tell the type**: noun phrases for Concepts, questions for Flows, no scratch-like titles ("Notes", "Untitled", "Misc") outside Inbox.
- **M-12 The retrieval loop is real.** Is there evidence the user revisits maps/diagrams (`reviewed:` dates, recent edits)? If the vault only accumulates, say so: browsing and rereading are weak for retention; redrawing from memory is the intended habit.

## 9. Fallback shell commands (only if the script cannot run)

```bash
# STR-02 loose notes at root
find "$V" -maxdepth 1 -type f -name '*.md'
# STR-04 subfolders in flat folders
find "$V/10 Concepts" "$V/20 Flows" "$V/30 Maps" -mindepth 1 -type d
# STR-05 type vs folder (list type per folder)
grep -rH --include='*.md' -m1 '^type:' "$V/10 Concepts" | grep -v 'type: concept'
# FM-01 missing domain in concepts/flows
grep -rL --include='*.md' '^domain:' "$V/10 Concepts" "$V/20 Flows"
# DEP-01 outward links from Concepts (to flows/maps/diagrams): list all links then match names against 20 Flows/30 Maps/40 Diagrams
grep -rHo --include='*.md' '\[\[[^]|#^]*' "$V/10 Concepts"
# NAV-02 duplicate basenames
find "$V" -name '*.md' -not -path '*/.*' -printf '%f\n' | tr 'A-Z' 'a-z' | sort | uniq -d
# LIF-01 old inbox items
find "$V/00 Inbox" -type f -mtime +14
```

Manual checks cannot prove reachability or cycles cheaply; if you fall back, mark NAV-03, NAV-04 and DEP-02 as **not verified** unless you traced them by hand.

## 10. Thresholds (heuristics, overridable via `--config`)

`concept_words_warn=350`, `concept_words_error=700`, `flow_words_info=2500`, `map_links_warn=40`, `map_links_min=3`, `max_depth_from_home=4`, `home_nodes_warn=12`, `diagram_nodes_warn=30`, `diagram_unlinked_words=25`, `inbox_days_warn=14`, `inbox_days_error=60`, `seed_days_info=90`, `review_days_info=90`, `premature_extraction_days=30`.

These are practical heuristics chosen for maintainability, not research findings. The research-backed principles are: creating concept maps yourself beats studying someone else's (Nesbit & Adesope 2006; Schroeder et al. 2017); retrieval practice beats elaborative concept mapping for retention (Karpicke & Blunt 2011); practice testing and spaced practice beat rereading and highlighting (Dunlosky et al. 2013); and people re-find personal information better through a stable navigable hierarchy they built than through tags or search alone (Bergman & Whittaker 2016).
