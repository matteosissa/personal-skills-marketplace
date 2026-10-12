# Templates, properties, and conventions

Use these when advising on structure or when the user explicitly asks you to draft notes or fix findings. Do not create notes otherwise.

## Contents
1. Property reference
2. Concept note
3. Flow note
4. Scratch note
5. Source note
6. Map note
7. Excalidraw conventions
8. Recommended Obsidian settings
9. Naming rules and examples

## 1. Property reference

| Property | Values | Used by | Notes |
|---|---|---|---|
| `type` | concept, flow, scratch, source, map, project, log | all | Source of truth; must match the folder |
| `status` | seed, growing, evergreen | concept, flow | seed = rough; growing = sections filled; evergreen = complete and sourced |
| `domain` | `"[[Map name]]"` (quoted wiki-link) | concept, flow | Must point to an existing Map in `30 Maps` |
| `created` | `YYYY-MM-DD` | all except scratch | Drives age-based rules |
| `reviewed` | `YYYY-MM-DD` | map, diagram (optional elsewhere) | Last retrieval review: redrawn/recalled from memory |
| `source` | `"[[Source note]]"` | concept, flow (optional) | Provenance |
| `aliases` | list | any | Must not equal another note's name |

Always quote wiki-links in frontmatter so YAML stays valid.

## 2. Concept note (`10 Concepts/<Noun phrase>.md`)

```markdown
---
type: concept
status: seed
domain: "[[<Map>]]"
created: YYYY-MM-DD
---
## Definition
<One or two sentences, in your own words. What it IS.>

## Invariants
<Rules that are always true about it - like business rules in a domain class.>

## Prerequisites
<[[Concept]] links only. Write "None." if there are none.>

## Often confused with
<Optional. Sideways references go here or under "See also".>

## Sources
<Optional. [[Source note]] links.>
```
Rules: no links to Flows, Maps, or Diagrams; no narrative; target under ~350 words.

## 3. Flow note (`20 Flows/<Question?>.md`)

```markdown
---
type: flow
status: seed
domain: "[[<Map>]]"
created: YYYY-MM-DD
---
## Question I'm trying to answer
<One concrete question.>

## Walkthrough
<The reasoning in order, long if needed. Explain inline first. Embed foundational
concepts with transclusion: ![[Consumer group#Definition]]. Link only the first
meaningful mention of a prerequisite concept.>

## Key insights
<Conclusions that answer the question.>

## Open questions
<What is still unclear.>
```
Rules: link to Concepts and Sources, never to Maps or Diagrams; extract a Concept only on the second reference or if it is foundational.

## 4. Scratch note (`00 Inbox/<anything>.md`)

```markdown
---
type: scratch
created: YYYY-MM-DD
---
<Raw, linear, messy. Wrong turns and questions welcome. No structure, no split, no linking duty.>
```
Process within about 14 days: extract the few foundational Concepts, rewrite the rest as a Flow, discard the remainder, then archive or delete the scratch note.

## 5. Source note (`50 Sources/<Title>.md`)

```markdown
---
type: source
created: YYYY-MM-DD
---
Author / URL / date: ...
Why it matters: ...
Notes created from it: [[...]]
```

## 6. Map note (`30 Maps/<Topic>.md`)

```markdown
---
type: map
created: YYYY-MM-DD
reviewed: YYYY-MM-DD
---
# <Topic>
Parent: [[<Parent Map>]]   (omit for domain Maps linked from Home)

## Foundations
- [[Concept]] - why it is here, in one phrase
## Flows
- [[How does X work?]] - what it explains
## Diagram
![[<Diagram name>.excalidraw]]
## Sub-maps
- [[<Sub-Map>]]
```
Create a Map when about 7-10 notes cluster. Split above ~40 links. A Map may embed a Base (`![[x.base]]`) for dynamic lists, but keep hand-written context lines for the key links.

## 7. Excalidraw conventions

- File lives in `40 Diagrams/`, named for the question or topic it answers; embedded in the Map of its domain.
- **One diagram, one question.** Put the question as a header text element.
- **Edges carry verbs** (triggers, requires, breaks if, causes, replaces). Unlabeled arrows lose the reasoning.
- **Nodes link to notes** with `[[Concept]]` / `[[Flow]]` in the text element, so depth is one click away.
- Keep to about 25 nodes; for bigger topics make a top-level diagram whose nodes link to sub-diagrams.
- Consistent visual language: left-to-right for causality; one colour per node type (concept / decision / pitfall).
- Build them yourself: constructing beats studying. Do not paste long paragraphs into nodes; if a node needs a paragraph it needs a note.
- Retrieval loop: periodically redraw the topic from a blank canvas from memory, compare with the saved diagram, fix gaps, then set `reviewed:` to today.

## 8. Recommended Obsidian settings

- Default location for new notes: `00 Inbox`.
- Default location for new attachments: `_Attachments`.
- Excalidraw plugin default folder: `40 Diagrams`; template folder: `_Templates`.
- Always update internal links on rename: on. Use wiki-links, shortest path when possible.
- Optional: Templater folder templates so new files in `10 Concepts` / `20 Flows` start with the skeleton.
- Core Bases per type (concepts by status, flows by domain, inbox by age) replace manual index maintenance.
- Back up with Git or sync; everything is plain files.

## 9. Naming rules and examples

| Kind | Rule | Good | Bad |
|---|---|---|---|
| Concept | Noun phrase, stable, no date, no question | `Consumer group`, `Idempotency` | `What is idempotency?`, `Notes 2026-03-12` |
| Flow | Question | `How does a consumer rebalance work?` | `Kafka stuff` |
| Map | Topic name | `Distributed Systems` | `Misc` |
| Diagram | Names the question/topic | `Consumer rebalance.excalidraw.md` | `Drawing 3` |
| All | Unique vault-wide; none of `# ^ [ ] \|` | | |
