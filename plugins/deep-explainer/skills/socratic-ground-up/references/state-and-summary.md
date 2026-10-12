# State tracking and the final summary

## Contents

- Why keep state
- State file schema
- Updating state
- Final synthesis (optional)
- The final summary: when and what
- Summary template
- Rules for building the summary

## Why keep state

Guided dialogue is long and branching: many tiny questions, hints, detours, repairs. The only reliable way to never lose the thread is to treat the graph, the learner's progress, and the pending question as **data**, not as something remembered from earlier turns. If your environment has a filesystem, keep a working state file (a scratch file; the learner need not see it). Otherwise keep the same structure in your reasoning and re-state the essentials whenever they change.

## State file schema

```markdown
# Topic: <topic>
Goal question: <the learner's original question>
Purpose: <from scoping>
Floor: <the agreed assumed knowledge>
Style: <options vs open answers; step size; pace>

## Nodes
| id | name | mode | needs | status | layer | hint level reached | notes |
|----|------|------|-------|--------|-------|--------------------|-------|
| 1  | ...  | guided | -   | done   | 0     | 0                  |       |
| 5  | ...  | guided | 4   | current| 2     | 1                  | beat 3 |

(mode: guided | told. status: todo | ready | current | done | shaky | known | compact | optional | skipped | pre-answered)

## Quest state (current node)
- Node: <id, name>
- Beat: <index of ladder>
- Pending question (verbatim): <...>
- Hint level used on this question: <0-4>
- Ledger of established facts (learner's own words): 
  - <fact 1>
  - <fact 2>

## Quest cards
(One per node: target insight, scene, given facts with whys, ladder, likely wrong answers with probes, name, consolidation, transfer check. Later nodes may be filled in just in time.)

## Spaced recalls scheduled
- <shaky node> -> recall at start of <dependent node>

## Parking lot
- <item> (raised at node <id>) - status: parked | answered | became node <id>

## Gap log
- Q: "<question>" | Type: <type> | Cause: <what was missing> | Added: <nodes/edges> | Swept: <other nodes fixed>

## Mermaid (current)
```mermaid
...latest map with progress colours...
```

## Multi-agent setup (if any)
- Coordinator: <model>; Subagents: <model>; N parallel; jobs: <...>
```

The three things the final summary is built from are the **Mermaid (current)** block, the **ledger** (what the learner established in their own words), and the **gap log**, so keep them current.

## Updating state

- **Before every reply**, update: current node, beat index, pending question, hint level, ledger, parking lot, statuses. The reply is generated from the updated state, never the reverse.
- **On node completion:** set status (`done`, or `shaky` if help reached level 3-4 or the check needed repair), schedule a recall for shaky nodes, mark the next node `current` and recompute `ready`/`todo` for all others, redraw the map.
- **On repair:** add nodes, edges and a gap-log entry; recolour; set the interrupted question as the pending one to restate.
- **On jump-ahead:** mark covered beats or nodes `pre-answered`.
- **On skip:** mark `skipped`; record which later nodes depend on it and how they will be covered.
- **On goal change:** archive the old graph under its own heading, start fresh, carry over `done` nodes.

## Final synthesis (optional)

When all main nodes are done, before the summary, run one **final synthesis question** so the learner assembles the whole picture themselves: "Using the map, how would you explain in your own words how ___ works?" (the original question). Let them answer in a few sentences; then complete it with them, adding only what is missing and tying each point to its node. If the learner prefers to skip it, skip it. It is a retrieval exercise, and it also shows which nodes to flag in the review list.

Also resolve the **spaced recalls** still pending (shaky nodes) with one tiny question each, or move them to the review list.

## The final summary: when and what

Offer it automatically when the main path is complete (or the learner signals they are done). One short offer is enough: "Want a markdown summary of everything, built from the final map and including the questions you asked and the ideas in your own words?"

If accepted, create a `.md` file and present it (with the file-presenting tool if available, otherwise print it in the reply).

## Summary template

```markdown
# <Topic> - from the ground up (guided)

## The question we started from
<The original question and the learner's purpose, two or three lines.>

## The map (final)
<The latest Mermaid map with progress colours, nodes added through questions
marked in the "gap" colour, plus a one-line legend.>

## The path, from simplest to most complex
| Step | Concept | What it is (plain words) | Why it matters here |
|------|---------|--------------------------|---------------------|
| 1 | ... | ... | ... |

(Ordered exactly as worked through: foundations with no dependencies first, then
each layer on top of the previous ones, ending at the answer to the original question.)

## The concepts, compressed
For each node, in the order worked through:
### <id> - <Concept>
- **Builds on:** <ids and names>
- **The idea, in your words:** <the learner's own formulation from the ledger>
- **Stated precisely:** <the consolidation, one or two sentences>
- **Because:** <the key whys, two to four bullets>
- **Unlocks:** <what depends on it>

## Questions that revealed gaps
These marked real things that were not obvious, so they deserve extra attention
when you review.

| # | Your question | What was missing | Where it now sits in the map |
|---|---------------|------------------|------------------------------|
| 1 | "..." | <concept / why / leap / misconception> | node <id>, between <a> and <b> |

## Misconceptions we corrected
<Wrong models the learner tried, why they were tempting, and what replaced them.>

## How it all fits together
<One short narrative from the roots to the goal: how each layer rests on the one
below, and how the original question is answered by the whole chain.>

## Glossary
| Term | Plain definition | Introduced in node |
|------|------------------|--------------------|

## Worth reviewing
<Shaky nodes (needed heavy help) with a one-line reminder of each, and a quick
self-check question for each.>

## Parked topics and optional branches
<Side topics that came up and were parked, optional branches, and what each would add.>
```

## Rules for building the summary

1. **Use the latest graph and the ledger.** The map and node table must reflect every repair. A summary built from the original plan is wrong.
2. **Preserve the flow.** Order by the path worked through, from nodes with no dependencies up to the goal. No alphabetical or thematic reordering.
3. **Keep the whys** and the learner's own words. The reasons turn a glossary into understanding; their own formulations make it theirs.
4. **Make the learner's questions and misconceptions prominent.** Each marks something that was genuinely not obvious.
5. **Be self-contained.** A reader who was not in the conversation, or the learner in six months, should follow it from top to bottom.
6. **Match language and format preferences.** If the learner wants another format (for example one note per concept for a notes system), produce that, keeping the graph links, the ledger wording and the gap log.
7. **No new content.** Summarize what was worked through. If you find a mistake while summarizing, correct it and tell the learner.
