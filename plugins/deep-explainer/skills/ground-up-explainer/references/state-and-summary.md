# State tracking and the final summary

## Contents

- Why keep state
- State file schema
- Updating state
- The final summary: when and what
- Summary template
- Rules for building the summary

## Why keep state

A long learning session spans many messages, repairs, and renumbering risks. The only way to never lose the thread is to treat the graph and progress as data, not as something remembered from earlier turns. If your environment has a filesystem, keep a working state file (a scratch file is fine; the learner does not need to see it). If not, keep the same structure in your reasoning and re-state the graph whenever it changes.

## State file schema

Use a single markdown file, for example `concept-state.md`, structured as:

```markdown
# Topic: <topic>
Goal question: <the user's original question, verbatim or tightened>
Learner purpose: <from scoping>
Floor: <the agreed assumed knowledge>
Depth / pace: <choices>

## Nodes
| id | name | plain definition | needs | status | layer | step |
|----|------|------------------|-------|--------|-------|------|
| 1  | ...  | ...              | -     | done   | 0     | 1    |
| 2  | ...  | ...              | 1     | next   | 1     | 2    |

(status: pending | next | done | known | compact | optional)

## Claims and whys (per node, condensed)
- n2: <claim> - because <why>
  ...

## Order
Step 1: n1, n2 | Step 2: n3 | ...

## Mermaid (current)
```mermaid
...latest diagram...
```

## Gap log
- Q: "<question>" | Type: <type> | Cause: <what was missing> | Added: <nodes/edges> | Swept: <others fixed>

## Parked / optional branches
- <branch>: <reason it is parked>

## Multi-agent setup (if any)
- Coordinator: <model>; Subagents: <model>; N parallel; jobs: <...>
```

The *Mermaid (current)* block and the *Gap log* are the two things the final summary is built from, so keep both current at all times.

## Updating state

- After every step delivered: set the step's nodes to `done`, mark the next ones `next`.
- After every repair: update the node table, the order, the Mermaid block, and append a gap-log entry. Do this before writing the reply, so the reply is generated from the updated state.
- After the Phase 3 freeze: record the floor, the pruned branches, the `known` and `compact` marks.
- When the user changes the goal: archive the old graph under a heading, start a fresh one, carry over `done` nodes.

## The final summary: when and what

Offer it automatically when the last step is complete or the user indicates they are satisfied. A single short offer is enough: "Want me to put everything we covered into a markdown summary, built from the final graph, including the questions you asked?"

If the user accepts, create a `.md` file and present it (with the file-presenting tool if available; otherwise print it in the reply).

## Summary template

```markdown
# <Topic> - from the ground up

## The question we started from
<The original question and the learner's purpose, in two or three lines.>

## The map
<The latest Mermaid diagram, with nodes added through questions marked in the
"gap" style, plus a one-line legend.>

## The path, from simplest to most complex
| Step | Concept | What it is (plain words) | Why it matters here |
|------|---------|--------------------------|---------------------|
| 1 | ... | ... | ... |

(Ordered exactly as taught: foundations with no dependencies first, then each
layer built on the previous ones, ending at the answer to the original question.)

## The concepts, compressed
For each node in teaching order:
### <id> - <Concept>
- **Builds on:** <ids and names>
- **Is:** <definition in one or two sentences>
- **Because:** <the key whys, condensed, two to four bullets>
- **Unlocks:** <what depends on it>

## Questions that revealed gaps
These are the points that were not obvious to the learner, and so they deserve
special attention when reviewing.

| # | Your question | What was missing | Where it now sits in the map |
|---|---------------|------------------|------------------------------|
| 1 | "..." | <concept / why / leap> | node <id>, between <a> and <b> |

## How it all fits together
<One short narrative, in prose, going from the roots to the goal: how each layer
rests on the one below, and how the original question is answered by the whole
chain. This is the paragraph that makes the map a story.>

## Glossary
| Term | Plain definition | Introduced in |
|------|------------------|---------------|

## Optional branches not covered
<Parked or optional topics and what they would add.>
```

## Rules for building the summary

1. **Use the latest graph.** The Mermaid block and the node table must reflect every repair. A summary built from the original plan is wrong.
2. **Preserve the flow.** Order by teaching sequence, from nodes with no dependencies up to the goal. Do not reorder alphabetically or by theme.
3. **Keep the whys.** The reasons are what turn a glossary into understanding. Condense them, but do not drop them.
4. **Make the learner's questions prominent.** Each question marks a real gap; give them their own section and mark the corresponding nodes in the diagram.
5. **Be self-contained.** A reader who was not in the conversation, or the learner in six months, should be able to follow it from top to bottom without having seen the chat.
6. **Match the learner's language and format preferences.** If they ask for a different format (for example one note per concept for a notes system), produce that instead, keeping the graph links and the gap log.
7. **No new content.** Summarize what was taught. If you notice a mistake while summarizing, correct it and tell the learner.
