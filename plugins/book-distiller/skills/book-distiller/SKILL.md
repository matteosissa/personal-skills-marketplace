---
name: book-distiller
description: Use when the user wants a whole book or very long document (PDF, EPUB, DOCX, text) turned into a study summary that keeps the book's chapter order and every distinct idea, condenses it with tables and diagrams, adds ground-up enrichment (missing prerequisites, skipped reasoning steps, real examples), and can be read in at most about 3 hours. Triggers - summarize this book, distill this book, study summary of a book, I don't have time to read this book.
---

# Book Distiller

## What this skill produces, and why it works this way

The person has a long book (often 300-600 pages) and not the time to read it. They want one document that:

1. **Follows the book's structure.** Same parts, chapters and sections, in the same order. No restructuring into "themes", because the book's sequence is how its author builds the argument, and because the reader may later want to jump into the original at the right place.
2. **Loses no idea, but drops the bulk.** Books repeat themselves, pad with anecdotes, and restate each point three times. The summary keeps every *distinct* idea (claim, argument step, definition, method, piece of evidence, caveat) and throws away the repetition and padding. "Lossless at the level of ideas, lossy at the level of words."
3. **Is condensed visually where content is structured.** Parallel content (comparisons, lists of attributes, steps, timelines, pros/cons, cause-and-effect chains) becomes tables and diagrams, because a table carries the same information as three paragraphs in a fraction of the reading time.
4. **Is enriched from the ground up.** Where the book takes a concept for granted, or jumps over a reasoning step, or condenses something too much, the summary adds what is missing. Where an important abstract idea would not stick, it adds a real-world example. All additions are visibly marked so the reader always knows what is the book and what is not.
5. **Fits a reading budget.** At most about 3 hours (180 minutes) of focused study, less for short books. The budget is measured, not guessed.

Goals 2, 4 and 5 pull against each other: keeping everything and adding things both make the summary longer, while the budget makes it shorter. The whole pipeline below is designed to resolve that tension explicitly: inventory every idea first, measure, allocate the budget by idea density rather than by page count, compress *representation* (tables, merging duplicates) before ever dropping content, and tell the user if the budget truly cannot hold the book.

This is primarily for non-fiction (essays, textbooks, technical books, history, how-to). For fiction, see "Genre adaptations".

## The ground-up principles (applied to a book)

These come from the ground-up-explainer method, adapted to a written summary instead of a live lesson. They govern every sentence the summary contains.

1. **Nothing assumed above the floor.** The "floor" is what the reader already knows (agreed at intake). Any term, fact or step above the floor that the book uses without explaining is a gap, and gets a short **Foundation** placed just before it is first needed. Below the floor, nothing is explained, because explaining known things wastes the budget and patronizes the reader.
2. **Every statement carries its "because".** A claim without its reason reads as arbitrary and does not stick. If the book gives the reason, keep it (condensed). If the book gives none and the claim matters, add the reason as a marked addition. If the real reason is unknown or contested, say so honestly; never invent one.
3. **Dependency order, inside the book's order.** You may not reorder the book, so dependencies are handled by insertion: a Foundation before first use, a **Bridge** where the book leaps, and a one-line forward pointer when the book uses a term it only defines in a later chapter ("defined properly in Ch. 7; for now: ...").
4. **One idea per paragraph.** Each paragraph adds one brick on top of what came before. A term is **bolded** where it is defined, and only there.
5. **Concrete before abstract, example after definition.** Analogies are allowed only if labeled as analogies and you say where they break, because an unmarked analogy becomes a false belief.
6. **Respect the reader's intelligence.** Never write "obviously", "simply", "just", "as you know": they signal a skipped gap.
7. **Misconceptions get named.** If a book's point contradicts a common intuition, say which intuition and why it fails, because otherwise the reader silently keeps the old belief.

## Fidelity rules (non-negotiable)

- **Plain text = the book.** Everything outside an "added" callout must be a faithful paraphrase of what the book says, including the book's own examples and its own reasoning.
- **Additions live only in callouts** (legend below). Never slip your own claims, opinions or corrections into the book's voice.
- **No fabricated facts.** Real examples must be real: named events, organizations, experiments, dates. Numbers you are not sure of are verified by web search if available; otherwise give the example without the precise figure. A made-up "illustrative" scenario must be labeled as such.
- **No silent corrections.** If the book is clearly outdated or wrong on a checkable fact, keep the book's claim and add an **Update** callout with the verified current fact and its source. Do not editorialize on the book's opinions unless the user asked for critique.
- **Paraphrase, do not copy.** Quote the author only for a short phrase whose exact wording matters (a coined term, a key definition), a few per chapter at most. The summary is a personal study aid, not a reproduction.

## Callout legend

Use Obsidian-style callouts. They render as styled boxes in Obsidian and as plain blockquotes elsewhere, so they degrade gracefully.

| Callout | Syntax | Use for |
|---|---|---|
| 🧱 Foundation (added) | `> [!info] 🧱 Foundation: <concept>` | A prerequisite the book assumes, explained compactly with its why |
| 🌉 Bridge (added) | `> [!tip] 🌉 Bridge` | A reasoning step the book skips or compresses too much |
| 🌍 Real example (added) | `> [!example] 🌍 Real example: <name>` | A real case that makes an important abstract idea stick |
| 🔄 Update (added) | `> [!warning] 🔄 Update` | A verified fact that has changed since publication, with source |
| 🎯 Chapter in one view (book) | `> [!abstract] 🎯 Chapter N in one view` | End-of-chapter recap table or diagram |

The book's own examples are not callouts: they stay in the text, condensed to the one or two sentences that carry the point.

## Pipeline overview

| Stage | What happens | Output (in the work folder) |
|---|---|---|
| 0. Intake | Ask the few questions that change the result | `state.md` |
| 1. Extract | Book file → chapter text files + word counts | `chapters/`, `manifest.json` |
| 2. Survey | Read TOC, intro, conclusion, chapter openings → book map, genre, thesis | `survey.md` |
| 3. Inventory | Read every chapter fully → ledger of every idea unit | `ledger/NN.md` |
| 4. Plan | Concept graph, gaps, budget allocation per chapter | `concepts.md`, `budget.md` |
| 5. Write | Chapter by chapter, in order, within budget | `draft/NN.md`, `established.md` |
| 6. Audit | Coverage, fidelity, term order, budget per chapter | `audit/NN.md` |
| 7. Assemble | Front matter, chapters, glossary → final file, measured | `<slug>-summary.md` |
| 8. Deliver | Send the file with a short report | |

Work from files, never from memory: a 500-page book does not fit in context, and a long run may be compacted or resumed in a later session. Update `state.md` after every chapter (which stage, which chapters done, open issues) so the work can always resume from it.

Tell the user at the start that a full book is a long job, roughly how long, and send the first finished chapter as soon as it passes audit so they can redirect style early (too dense, too many callouts, wrong floor) before the whole book is written that way.

## Stage 0 - Intake

Ask in one message (use a multiple-choice question tool if available), skipping anything already known:

1. **Reader floor.** What does the reader already know about this field? Propose a concrete floor from the book's subject (e.g. "educated adult, no economics background" vs. "knows basic statistics"). This decides how many Foundations are added.
2. **Purpose.** Understanding the ideas, exam preparation, applying it at work, deciding whether to read the full book. Exam prep shifts weight to definitions and formulas; work use shifts it to methods and examples.
3. **Time budget.** Default: `min(180 min, 30% of the book's normal reading time)`. Confirm or override.
4. **Language** of the summary (default: the language the user writes to you in, or their stated preference).
5. **Output.** Default: one Markdown file (works in Obsidian with Mermaid and callouts). Options: one file per chapter, or a document artifact if the environment offers one.

If the user says "just go", use the defaults and an "educated adult, no specialist background in this field" floor, and state those assumptions at the top of the summary.

Ask for the book file if it was not provided. Work only on a copy; never modify the original.

## Stage 1 - Extract

Create the work folder `<book-slug>-work/` and write the script below to it (outside the folder holding the book file), then run it. It needs `pymupdf` for PDFs (`pip install pymupdf`) and `pandoc` for everything else.

```python
# extract_book.py  -  usage: python3 extract_book.py BOOK_FILE WORK_DIR [--level N]
import json, re, subprocess, sys
from pathlib import Path

def words(t): return len(re.findall(r"\w+", t))
def slug(t): return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:50] or "section"

def pdf_chapters(path, level):
    import pymupdf
    doc = pymupdf.open(path)
    pages = [p.get_text() for p in doc]
    if sum(words(p) for p in pages) < 50 * len(pages):
        print("WARNING: little text; PDF may be scanned. OCR it first (ocrmypdf).", file=sys.stderr)
    toc = [(t, p) for lv, t, p in doc.get_toc() if lv == level and p > 0]
    if not toc:  # fallback: pages starting with a chapter-like heading
        pat = re.compile(r"^\s*(chapter|capitolo|cap\.|part|parte)\s+\w+", re.I)
        toc = [(pages[i].strip().splitlines()[0][:80], i + 1)
               for i in range(len(pages)) if pages[i].strip() and pat.match(pages[i])]
    toc = toc or [("Whole book", 1)]
    out = []
    for i, (title, start) in enumerate(toc):
        end = toc[i + 1][1] - 1 if i + 1 < len(toc) else len(pages)
        out.append((title, "\n".join(pages[start - 1:end]), f"pp. {start}-{end}"))
    return out

def pandoc_chapters(path, level):
    md = subprocess.run(["pandoc", str(path), "-t", "gfm", "--wrap=none"],
                        capture_output=True, text=True, check=True).stdout
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    hits = list(re.finditer(rf"^#{{{level}}}\s+(.+)$", md, re.M))
    if not hits: return [("Whole book", md, "")]
    return [(m.group(1).strip(), md[m.start():(hits[i+1].start() if i+1 < len(hits) else len(md))],
             f"heading {i+1}") for i, m in enumerate(hits)]

src, work = Path(sys.argv[1]), Path(sys.argv[2])
level = int(sys.argv[sys.argv.index("--level") + 1]) if "--level" in sys.argv else 1
chs = pdf_chapters(src, level) if src.suffix.lower() == ".pdf" else pandoc_chapters(src, level)
(work / "chapters").mkdir(parents=True, exist_ok=True)
manifest = []
for n, (title, text, loc) in enumerate(chs, 1):
    f = work / "chapters" / f"{n:02d}-{slug(title)}.txt"
    f.write_text(text, encoding="utf-8")
    manifest.append({"n": n, "title": title, "loc": loc, "words": words(text),
                     "file": str(f.relative_to(work)), "kind": "body"})
(work / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
for m in manifest: print(f'{m["n"]:>3} {m["words"]:>7} w  {m["loc"]:<14} {m["title"]}')
print("TOTAL", sum(m["words"] for m in manifest), "words")
```

Then check the split by eye:

- If chapters came out wrong (one giant unit, or every subsection separate), rerun with another `--level`, since books nest parts → chapters → sections differently.
- In `manifest.json`, set `"kind"` to `front`, `back` or `skip` for front matter, acknowledgments, notes, bibliography and index. They are not summarized and not counted in the book's word count. Keep endnotes available: if a body passage depends on a note, read that note.
- If the PDF is scanned (the warning fires), OCR it first (`ocrmypdf` or `tesseract`), because summarizing garbage text produces confident nonsense.

## Stage 2 - Survey

Before reading in depth, read the table of contents, the introduction, the conclusion, and the first and last page of each chapter. Write `survey.md` with:

- **Book thesis** in 1-2 sentences, and the question the book answers.
- **Genre** (see Genre adaptations), because it decides which representations to favor.
- **Chapter one-liners:** for each chapter, the question it answers and how it feeds the thesis.
- **Book map:** a Mermaid diagram of how the parts and chapters build on each other.
- **First guess at the floor gap:** which fields the book draws on that the reader may not know.

Why this comes first: knowing where the book is going tells you, while reading chapter 2, which ideas are load-bearing for chapter 9, so importance is judged correctly in the inventory.

## Stage 3 - Inventory (the ledger)

Read each body chapter **in full**, in chunks of about 6-10k words, and record every idea unit in `ledger/NN.md`, one line each:

```
- L03-017 | p.84 / §3.2 | claim | core | Paraphrase of the idea in <=25 words | because: <book's reason or "none given"> | needs: term A, term B
- L03-018 | p.85 | example | supporting | Book's story of X shows the claim in practice
- L03-019 | p.86 | claim | supporting | Restates L03-017 | dup-of: L03-017
```

- **Types:** definition, claim, argument step, evidence/data, example/story, method/procedure, formula, caveat/limitation, comparison, prediction/recommendation.
- **Importance:** `core` (the thesis, or something later chapters depend on), `supporting` (a real, distinct point, reason or piece of evidence), `color` (padding, rhetorical flourish, a third anecdote for the same point). Be strict with `color`: a distinct piece of evidence is `supporting`, even if minor.
- **Duplicates:** mark restatements with `dup-of:` so they are counted once. Repetition is where most of the compression comes from.
- **Ground-up gap scan.** Simulate the reader at the agreed floor while reading, and log in the same file, under `## Gaps`:
  - `ASSUMED: <term/idea>`: used without explanation, above the floor.
  - `LEAP: L03-021 -> L03-022`: the conclusion does not follow without an unstated step.
  - `TOO CONDENSED: L03-030`: correct, but too compressed to be understood.
  - `NEEDS EXAMPLE: L03-017`: important and abstract; would not stick without a concrete case.
  - `FORWARD REF: <term> (defined Ch. 7)`.
  - `CHECK: <fact>`: a checkable fact that may be outdated.
- Record the book's own section headings in order, because the summary will mirror them.

Inventory is the step that guarantees "no idea lost": the summary is later checked against the ledger, not against your memory of the chapter.

## Stage 4 - Plan: concept graph and budget

### Concept graph (`concepts.md`)

Merge all ledgers and `ASSUMED`/`FORWARD REF` entries into one list of concepts, each with: where the book defines it (if anywhere), where it is first used, and its status:

- `book-defined`: the book explains it adequately; nothing to add.
- `floor`: below the reader floor; nothing to add.
- `foundation`: above the floor and never adequately explained; gets one Foundation callout, placed right before its first use, never repeated later.
- `forward`: used before the book defines it; gets a one-line pointer at first use.

Then expand recursively, as in the ground-up method: each Foundation may itself use terms above the floor, which need their own Foundation (or a simpler wording). Stop when a pass adds nothing. Keep Foundations compact (typically 40-120 words): they exist to unlock the book, not to replace it.

### Budget (`budget.md`)

1. `W` = words in body chapters. Original reading time `T_orig = W / 230` min.
2. Target `T` = the agreed budget (default `min(180, 0.30 * T_orig)`).
3. Reading-time model, used everywhere: prose at 180 words/min, table text at 120 words/min, 1.5 min per diagram. (Focused study is slower than normal reading, and tables are denser than prose.)
4. Split `T`: about **70% book content**, **20-25% enrichment** (Foundations, Bridges, examples, Updates), **5-10% scaffolding** (front matter, chapter openers and recaps, glossary). Enrichment must not crowd out the book.
5. Allocate the book-content share across chapters in proportion to **idea weight**, not page count: `core = 3`, `supporting = 1.5`, `color = 0.3`, `dup-of = 0`. Allocate enrichment in proportion to each chapter's gap list. A 40-page chapter that says one thing twice gets less than a dense 15-page one.

For scale: 180 minutes is roughly 25,000-30,000 words of prose, less when there are many tables and diagrams. A 500-page book has about 125,000-175,000 words, so book content is compressed to roughly 12-15% of its words. That is achievable without losing ideas because typical non-fiction is highly redundant, but it requires disciplined use of tables and merging.

**If the budget cannot hold the book** (core + supporting ideas do not fit even in table form): first compress representation further (more tables, merge closely related ideas into single sentences), then move budget from scaffolding, then trim enrichment to the most important gaps. If it still does not fit, do not silently drop ideas: stop and tell the user the estimated minimum time and the options (accept an overrun of N minutes, or move listed detail-level items into a compact "Reference details" appendix that is not part of the study read).

## Stage 5 - Write, chapter by chapter, in order

Write sequentially, because the reader meets chapters in order and each chapter may rely on what earlier chapters (and earlier Foundations) already explained. Keep `established.md`: every term explained so far, with the chapter where it was explained. Before writing a chapter, read its ledger, its gap list, its budget, and `established.md`, and reread the source text of passages whose nuance matters.

### Chapter template

```markdown
## Chapter N - <book's title>
*Book: pp. X-Y · Reading time: ~M min*

**Where this fits:** <1-2 sentences: what earlier chapters established, and what question this one answers.>
**Chapter in one sentence:** <the chapter's thesis.>

### N.1 <book's section heading>

<Condensed paraphrase in the book's order. One idea per paragraph, each with its because.> <!-- L0N-001 L0N-002 -->

> [!info] 🧱 Foundation: <concept>
> <What it is, why it exists or matters, in as few words as possible, using only established terms.>

<More of the book's content, now understandable.> <!-- L0N-003 -->

| <Comparison table where the book compares or lists parallel items> |
|---|

> [!tip] 🌉 Bridge
> <The step the book skips: "The book goes from A to C. The missing step is B, because ...">

> [!example] 🌍 Real example: <name>
> <A real, specific case, 2-5 sentences, ending with the link back to the idea.>

### N.2 <next section heading>
...

> [!abstract] 🎯 Chapter N in one view
> <Recap table (idea → why it matters → where it leads) or a small Mermaid diagram. Book content only.>
```

### Writing rules

- **Mirror the book's order** of sections and of ideas within sections. The only permitted adjustment is inserting a Foundation, Bridge or forward pointer; never move the book's content around.
- **Ledger markers.** After each paragraph, table or callout that covers ledger items, put an HTML comment with their IDs (`<!-- L03-017 L03-018 -->`). This is what makes the coverage check mechanical. Every `core` and `supporting` ID must appear at least once; `color` items may be dropped or folded into a phrase; `dup-of` items are covered by their original.
- **Choose the representation by the shape of the content:**

  | Content shape | Representation |
  |---|---|
  | An argument (premises → conclusion) | Prose with explicit "because/therefore", or a small Mermaid flowchart for a long chain |
  | Several items compared on the same attributes | Table |
  | A process or procedure | Numbered steps, or a flowchart if it branches |
  | Causes and effects, feedback loops | Mermaid flowchart |
  | Events over time | Timeline table (date → event → significance) |
  | A taxonomy or classification | Nested list or Mermaid mindmap/tree |
  | Claims with supporting evidence | Table: claim → evidence the book gives → strength as the book presents it |
  | A formula | The formula, every variable explained, then one worked example |
  | A story the book uses as an example | One or two sentences keeping only what makes the point |

  Do not turn everything into tables: an argument chopped into table cells loses its "because". Prose for reasoning, tables for parallel facts.
- **Flow.** Write so it reads as continuous explanation, not notes. Each paragraph opens by connecting to the previous one, and each section ends where the next one picks up. The reader should be able to read straight through for three hours without reconstructing the logic.
- **Real examples: only where they earn their place**, meaning an important idea that is abstract and would not stick from the book's own material. Typically one per few core ideas, not one per paragraph. Prefer the book's own example when it is good; add a real one when the book has none, or when the book's is vague or hypothetical. Choose well-documented cases (major historical events, well-known companies, landmark experiments, everyday products) and verify specific numbers.
- **Term discipline.** Every term above the floor must be defined in the book text you have already summarized, in a Foundation, or in `established.md` before it is used. Bold a term only where it is defined.
- **Stay within the chapter budget** (measure with the checker below). If you are far over, convert parallel prose to tables and merge restatements before cutting anything.

## Stage 6 - Audit every chapter before moving on

Write the checker to the work folder once:

````python
# check_summary.py  -  usage: python3 check_summary.py DRAFT.md [LEDGER_FILE_OR_DIR ...]
import re, sys
from pathlib import Path
PROSE_WPM, TABLE_WPM, DIAGRAM_MIN = 180, 120, 1.5

def reading_time(md):
    diagrams = len(re.findall(r"^```mermaid", md, re.M))
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    lines = md.splitlines()
    w = lambda ls: len(re.findall(r"\w+", "\n".join(ls)))
    tw = w([l for l in lines if l.lstrip().startswith("|")])
    pw = w([l for l in lines if not l.lstrip().startswith("|")])
    return pw, tw, diagrams, pw / PROSE_WPM + tw / TABLE_WPM + diagrams * DIAGRAM_MIN

def ledger_ids(paths):
    need = set()
    for p in paths:
        files = sorted(Path(p).glob("*.md")) if Path(p).is_dir() else [Path(p)]
        for f in files:
            for line in f.read_text(encoding="utf-8").splitlines():
                m = re.match(r"\s*[-|]?\s*(L\d+-\d+)\b.*\b(core|supporting)\b", line)
                if m and "dup-of:" not in line: need.add(m.group(1))
    return need

md = Path(sys.argv[1]).read_text(encoding="utf-8")
pw, tw, d, mins = reading_time(md)
print(f"prose {pw} w | table {tw} w | diagrams {d} | est. {mins:.0f} min ({mins/60:.1f} h)")
if len(sys.argv) > 2:
    need = ledger_ids(sys.argv[2:])
    have = set(re.findall(r"L\d+-\d+", " ".join(re.findall(r"<!--(.*?)-->", md, re.S))))
    missing = sorted(need - have)
    print(f"coverage {len(need) - len(missing)}/{len(need)} core+supporting ideas")
    if missing: print("MISSING:", ", ".join(missing)); sys.exit(1)
````

Run `python3 check_summary.py draft/NN.md ledger/NN.md`, then do the judgment checks the script cannot do. Record results in `audit/NN.md` and fix before writing the next chapter:

1. **Coverage:** the script reports no missing IDs. A marker must reflect real coverage: spot-check that the marked paragraph actually conveys each idea, not just mentions it.
2. **Fidelity:** compare the draft against the source for the chapter's core items. Is anything distorted, overstated, or stripped of a qualification the author made? Are all numbers identical to the book's? Is every addition inside a callout?
3. **Term order:** scan for any term above the floor used before it is defined (in this chapter, an earlier one, or a Foundation).
4. **Why audit:** does each substantive statement carry a specific reason? Replace vague ones ("for efficiency") with the concrete problem they address.
5. **Leap audit:** reading only the summary, is there any point where the reader must supply a missing step?
6. **Budget:** within roughly ±15% of the chapter's allocation; adjust the remaining chapters' allocations if not.

## Stage 7 - Assemble

Concatenate the chapters into `<book-slug>-summary.md` with this frame:

```markdown
# <Book title> - Study Summary
*<Author>, <year>. Original: ~P pages, ~H hours of reading. This summary: ~M min of focused study.*
*Reader assumed: <floor>. Purpose: <purpose>.*

## How to read this
<3-4 lines: plain text is the book, condensed and in its order; callouts are additions (legend table); suggested sessions, e.g. 3 x 60 min with break points named by chapter.>

## The book in one page
<Thesis, the question it answers, and the book map (Mermaid) from the survey,
plus a table: Chapter → the question it answers → reading time.>

<Chapters 1..N>

## Glossary
<Every bolded term: term → one-line definition → chapter where defined. Sorted alphabetically.>

## What was compressed
<Short honest note: what kinds of material were condensed or dropped (repeated anecdotes,
rhetorical restatements, author biography in Ch. X), so the reader knows what the original adds.>
```

Then:

- Strip the `<!-- L.. -->` markers from the final file (keep them in `draft/`).
- Run the checker on the final file, compare with the budget, and put the measured time in the header.
- Check Mermaid blocks for syntax errors (an unclosed bracket or an unquoted label with parentheses breaks the whole diagram): quote labels containing punctuation, e.g. `A["Price (nominal)"]`.
- Read the transitions between chapters once more for flow.

## Stage 8 - Deliver

Send the file. In the reply, give in a few lines: the measured reading time, coverage (ideas kept / ideas inventoried, after removing duplicates), how many Foundations, Bridges and real examples were added, any budget compromise the user agreed to, and any part of the book that could not be processed (e.g. unreadable pages). Offer, in one line, a version split into one note per chapter if that suits their notes system.

## Parallel mode (optional; ask first)

For a long book, the inventory (Stage 3) and the audit (Stage 6) parallelize well, because each chapter's ledger is independent. Writing (Stage 5) should stay with one coordinating agent, because voice, term order and `established.md` need a single owner. Drafts can be parallelized only after `concepts.md` is complete, by giving each drafter the exact list of terms established before its chapter, and the coordinator must rewrite them into one voice.

Never start subagents without asking the user: ask whether to use them, for which stages, which models, and how many at once. If the environment has no subagents, run single-agent. Each subagent gets a self-contained brief: the agreed floor, the ledger format above, the rules (paraphrase, every idea logged, duplicates marked, gaps logged, uncertain claims flagged rather than guessed), and the chapter file path. The coordinator reviews every returned ledger for importance grading and missing items before using it, since the guarantee of "no idea lost" rests on the ledger.

## Genre adaptations

| Genre | Emphasize | Typical representations |
|---|---|---|
| Argument / ideas (economics, psychology, essays) | The argument chain, evidence, the author's caveats | Argument flowcharts, claim → evidence tables |
| Textbook / technical | Every definition, formula and method; heavier Foundations | Formula blocks with variables explained, one worked example per method, comparison tables |
| Practical / how-to | Procedures, decision rules, pitfalls | Numbered steps, checklists, decision tables ("if X → do Y, because Z") |
| History / biography / narrative non-fiction | The causal story and its turning points | Timeline tables, cast-of-characters table, cause → effect diagrams |
| Essay or paper collection | Each piece as its own unit with its own thesis | One section per piece, a cross-piece table of positions at the end |
| Fiction (if asked) | Plot per chapter, characters, themes; enrichment limited to context (historical, cultural) the reader needs | Character table, plot timeline; no "real examples" |

## Worked example (style only)

Book passage, paraphrased, from a hypothetical economics book: *the author writes that after the shock, the central bank kept rates "low in real terms", which is why borrowing exploded, and moves straight to the next topic.*

Summary output:

```markdown
> [!info] 🧱 Foundation: nominal vs. real interest rate
> The **nominal rate** is the percentage written on the loan. The **real rate** is roughly the nominal rate minus inflation, because inflation shrinks what the money you repay can buy: borrowing at 5% when prices rise 8% a year means you repay less purchasing power than you borrowed.

The author argues that after the shock the central bank kept real rates low, and that this is why borrowing grew so fast. <!-- L04-012 -->

> [!tip] 🌉 Bridge
> The book skips why low real rates cause borrowing. The step: when the real rate is low or negative, debt gets lighter over time as inflation erodes it, so taking a loan today is cheap in real terms, and households and firms borrow more.

> [!example] 🌍 Real example: Turkey, 2022
> In October 2022 Turkey's annual inflation reached about 85% while the central bank cut its policy rate to 10.5%, a real rate of roughly -75%. Borrowing became so attractive (and housing so popular as an inflation hedge) that the authorities had to impose administrative limits to hold credit growth back, which is the mechanism above showing up in practice.
```

Note what the example shows: the book's claim stays in plain text with its reason; the missing prerequisite, the skipped step and the real case are each marked as additions; the real example uses verified figures. (When this example was drafted, a first version claimed credit "surged" in late 2022; checking showed regulators were actually restraining it, so the claim was rewritten. That check is the point of the fidelity rules.)

## Failure modes to avoid

- Summarizing from the survey or from general knowledge of the book instead of the full text. The ledger must come from reading every page.
- Restructuring the book "for clarity". The order is a requirement.
- Additions written in the book's voice, or invented examples and figures.
- A wall of tables that has lost the reasoning between them.
- Foundations that balloon into mini-lectures, eating the budget meant for the book.
- Re-explaining a concept in every chapter instead of once (check `established.md`).
- Padding a short book to fill 3 hours: 180 minutes is a ceiling, not a target.
- Silently dropping ideas to hit the budget, instead of compressing representation or asking.
