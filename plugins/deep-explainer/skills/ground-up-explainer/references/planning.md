# Planning: building the concept graph

This is the engine of the skill. If the graph is complete and correctly ordered, the explanation almost writes itself and the learner never has to ask anything. If the graph has holes, no amount of good writing in Phase 5 will rescue it.

## Contents

- Node card
- The expansion loop (with the newcomer simulation)
- Where to stop: the floor
- Keeping the graph small and clean
- Layering and teaching order
- Cycles
- Bridge nodes
- Validating before you speak
- Worked mini-example

## Node card

For every node, hold these fields (in the state file or in your reasoning):

| Field | Meaning |
|---|---|
| `id` | Short stable number or key. The learner sees this number in the diagram and the steps, so never reuse or silently renumber it. |
| `name` | Plain-language label, short enough for a diagram box. |
| `plain definition` | One sentence a newcomer could follow using only the node's prerequisites. If you cannot write it, a prerequisite is missing. |
| `needs` | Ids of prerequisites. |
| `why it exists` | The problem this concept solves. This becomes the opening of its step ("we need this because..."). |
| `claims` | The individual statements the step will make (facts, rules, defaults, numbers, names). Each will need a why. |
| `terms introduced` | Words that first appear here. Each must be defined here. |
| `example idea` | A concrete case using only taught concepts. |
| `status` | `full`, `compact`, `known`, `optional`, or `done`. |
| `layer` | Computed, see below. |

If you cannot fill `plain definition`, `needs`, and `why it exists` for a node, you do not understand it well enough to teach it yet. Research it (web search if available) before continuing.

## The expansion loop

```
queue <- [the user's question]
graph <- {}
while queue is not empty:
    item <- pop(queue)
    draft <- write the rough explanation of item, as you would naturally
    candidates <- every term, mechanism, convention, number, name, step in draft
    for each candidate and each claim in draft:
        ask the three newcomer questions (below)
        for each "yes":
            create or reuse a node, add edge (new node -> item), push new node to queue
            or record a why to attach, or insert a bridge node
until a complete pass over every node creates nothing new   # closure
```

### The three newcomer questions

Ask them about every word and every claim in your draft. Be a pessimist: assume the reader has never seen the field.

1. **Word test.** Would a person with no background in this field know this word, name, or symbol? If it is jargon, an acronym, a proper noun from the field, or an everyday word used with a special meaning, it needs a node. Acronyms are a frequent trap: knowing what the letters stand for is not understanding.
2. **Why test.** Would they wonder why this is the case? Defaults, conventions, specific numbers, names, rules, and design choices all trigger it. This creates a *why to attach* and, often, a new node when the reason itself needs a concept.
3. **Leap test.** Am I going from A to C without mentioning B because B feels obvious? If the connection is not trivially forced, B is a bridge (see below).

The recursion matters. An explanation of one concept may need ten others; each of those needs its own draft and its own three tests. Do not stop after one level just because the result already looks big. Stop only at closure and at the floor.

### Sources of hidden dependencies (check these deliberately)

- Acronyms and abbreviations.
- Words with a special technical meaning that clash with everyday meaning (for example "session", "process", "stateless").
- Implicit units, scales, and orders of magnitude.
- Tools or artifacts the explanation assumes you have seen (a terminal, a diagram, a form).
- Historical context that makes a design look strange without it.
- The *purpose* of the whole thing: why anyone built this in the first place.
- Notation and symbols.
- "Standard" or "default" anything: always ask who decided and why that matters.

## Where to stop: the floor

Recursion must end somewhere or you would explain physics to explain a web page. The stopping rule is the **floor**: the explicit level of knowledge the learner is stated to have.

- Default floor: everyday life and general literacy. Any concept that cannot be explained from everyday experience alone is above the floor and needs a node.
- For technical topics, the floor is usually something concrete the learner confirms in Phase 2, such as "you have used a browser", "you can read basic code", or "you know what a variable is".
- The floor is explicit, shown in the Phase 4 message, and revisable. If a side question reveals that the real floor is lower than assumed, lower it (Phase 6 forward sweep).
- Things below the floor can still appear in the explanation, and they still get a why. They just do not get their own node.

A concept sitting exactly at the floor boundary is a judgment call: when in doubt, add a one-line root node. The cost of a tiny extra node is far lower than the cost of a hole.

## Keeping the graph small and clean

- **Deduplicate and merge.** One concept, one node, however many parents. Merge synonyms. Do not create "HTTP basics" and "introduction to HTTP".
- **Split fat nodes.** If a node's explanation would need more than about 600 words, or contains two separable ideas, split it. Smaller bricks are easier to absorb and to fix.
- **Drop decorative nodes.** A node that no other node needs and that does not help answer the question is a tangent. Either drop it or mark it `optional`.
- **Size limit.** Beyond roughly 40 nodes in one diagram, group into modules (see `mermaid-and-diagrams.md`). Offer to cover the topic as module 1, module 2, and so on, with each module ending at a natural milestone.

## Layering and teaching order

1. **Layer.** Layer 0 = nodes with no prerequisites (roots). Layer *k* = 1 + max(layer of its prerequisites).
2. **Order.** Any topological order is valid, but a good one also:
   - **Teaches a concept shortly before it is used.** A foundation introduced twenty steps before its first use is forgotten by then. Prefer to advance along one chain toward the goal, pulling in the roots that chain needs, then start the next chain.
   - **Keeps tightly related nodes adjacent** so the learner holds fewer things in mind at once.
   - **Reaches a first useful milestone early.** Where possible, arrange that by the middle the learner can already explain a meaningful small part of the goal.
   - **Never puts a node before one of its prerequisites.** Check this mechanically.
3. **Group into steps.** Each step is one node, or up to three small nodes that are only meaningful together. Number the steps (the learner sees "Step k of K").

## Cycles

If A seems to need B and B seems to need A, the concepts are usually understood in a spiral, not defined circularly. Break the cycle with a **rough pass**:

1. Introduce A-rough: a deliberately simplified version, labeled as such ("for now, treat A as just..."), with the reason it is simplified.
2. Teach B using A-rough.
3. Return to A as a refinement node ("A, now with the full picture"), which depends on B.

Show both nodes in the diagram (A-rough and A-full) so the learner is not surprised. Never hide a circle by silently using a term before it is defined.

## Bridge nodes

Sometimes the missing piece is not a concept but a step of reasoning. Typical bridges:

- A *motivating problem*: show the pain that exists without the concept before introducing it, so its why is felt.
- A *worked case* that makes an abstract rule concrete.
- A *contrast*: how it works without the concept, to reveal what the concept adds.
- A *definition by purpose*: what this thing is for.

If the leap test says yes and no concept fits, add a bridge node.

## Validating before you speak

Check mechanically, not by feel:

- [ ] Every edge points from a prerequisite to a dependent, and there are no cycles (except resolved rough/full pairs).
- [ ] Every non-root node has all its prerequisites present.
- [ ] Every chain ends in roots that sit at or below the floor.
- [ ] Every node has a plain definition, a why-it-exists, and its claims listed.
- [ ] The goal node is reachable from every non-optional node (nothing is stranded).
- [ ] The teaching order respects every edge.
- [ ] Step count and sizes are reasonable.

## Worked mini-example (abbreviated)

Question: "How does a web browser load a page?" Rough draft mentions: URL, DNS, IP address, port, TCP, HTTP request, status codes, HTML, rendering.

Newcomer simulation on "IP address": word test yes (jargon) -> node. Its definition needs "network" -> node. "Network" needs "computer" and "communication", which are at the everyday floor. "Port": word test yes, why test on "port 80 by default" yes -> a convention node ("why defaults exist") feeds it. "TCP": needs "protocol" -> node; "protocol" needs the idea of "agreement between parties", which is everyday. "HTTP request" needs "message", "method", "path", "header" (each a node or part of the message node, with whys). And so on until a pass adds nothing.

The resulting graph is shown in `mermaid-and-diagrams.md`.
