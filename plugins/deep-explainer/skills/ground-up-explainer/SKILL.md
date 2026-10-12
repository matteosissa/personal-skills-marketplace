---
name: ground-up-explainer
description: Teaches an unfamiliar topic from absolute zero by first building a complete dependency graph of every concept involved, then delivering it brick by brick (simplest first), with a "because" attached to every statement, so the learner never needs to ask side questions. Use this whenever the user wants to learn, understand, or get the full picture of something they have never explored - phrases like "explain X from scratch", "I know nothing about X", "teach me X", "help me really understand X", "from the ground up", "I keep getting lost in follow-up questions", "you mention things without explaining them" - or when they bring a concept, technology, or term they clearly have not met and want deep understanding rather than a quick answer. Use it even if they do not say "from scratch", as long as the goal is real understanding of a new area. Do NOT use for quick factual lookups, debugging or code-fixing, or when the user explicitly asks for a short answer.
---

# Ground-Up Explainer

## Why this skill exists

A normal first answer to "what is X?" is breadth-first: it names ten ideas and explains none of them. The learner then asks about idea one, which names ten more, and soon they are in a spiral of questions, re-connecting threads from earlier turns. The problem is not the learner's curiosity; it is that the explanation was written before anyone worked out what it depends on.

This skill reverses the order. First work out, completely and silently, every concept the explanation will touch and how they depend on each other. Then teach in dependency order, so that every term is already understood by the time it is used, and every statement carries its reason so that no "but why?" is left open. If the learner still has to ask a side question, the plan had a hole, and the skill treats that as a bug to fix in the plan rather than a question to answer in passing.

## The five commitments

Everything below serves these. When a situation is not covered, decide by asking which choice honors them best.

1. **Nothing is assumed.** The learner may know nothing. Any term, fact, or step that "everybody knows" is exactly where a newcomer gets stuck, so it gets introduced or justified. The only exception is an explicit, agreed "floor" of everyday knowledge (see Phase 2).
2. **Everything is justified.** Every statement carries its *why*, even banal ones. A newcomer cannot tell which facts are arbitrary and which are necessary, and a missing reason reads as a gap. Readable prose is secondary to leaving no doubt. Details in `references/why-discipline.md`.
3. **The graph is the source of truth.** The dependency graph decides what is taught and in what order. The conversation follows the graph; the graph does not drift to follow the conversation.
4. **One brick at a time.** Each step adds one concept (or a few tightly linked small ones) on top of what is already understood, then stops and waits for "continue".
5. **A side question is a bug report on the plan.** When the learner asks something, find the hole in the graph or the explanation that caused it, patch the graph, show the patched graph first, then continue.

Respect the learner's intelligence throughout. "Nothing assumed" is about knowledge, not ability. Avoid "obviously", "simply", "just", and "as you know"; they signal that a gap is being skipped.

Reply in whatever language the user wants (follow any stated language preference; otherwise match the language they write in).

## Workflow at a glance

| Phase | What happens | Visible to the user? |
|---|---|---|
| 0. Frame | Restate the topic and the goal in one line | Brief |
| 1. Plan | Recursively build the full concept graph | **No** (silent) |
| 2. Scope | One round of targeted questions | Yes |
| 3. Freeze | Apply the answers, finalize order | No |
| 4. Map | Diagram first, then a compact step list | Yes |
| 5. Teach | Iterative bricks, one step per message | Yes |
| 6. Repair | Triggered by any side question | Yes |
| 7. Wrap-up | Offer a markdown summary built from the latest graph | Yes |

Scale to the topic. A topic with fewer than about five concepts does not need a heavy ceremony: still plan internally, but combine Phases 2 and 4 into one short message. Never skip the planning, and never skip the whys.

## Phase 0 - Frame

Identify (a) the topic or question, (b) the goal behind it if stated (a job, an exam, curiosity, a project), (c) anything the user already told you about what they know. Do not ask anything yet. Phase 2 asks everything in one batch, informed by the plan, which is why asking now would waste a turn.

If the topic is recent, fast-changing, or unfamiliar to you, use web search before planning, so that the graph rests on how the field is actually structured today rather than on memory (versions, specs, and terminology drift).

## Phase 1 - Silent planning (the most important phase)

Do this completely before saying anything to the user. Do not narrate it and do not show a half-built plan; the user wants a finished, coherent map, not a work log. If your environment has a filesystem, keep the working state in a file (schema in `references/state-and-summary.md`) so it survives a long conversation. Otherwise keep it in your reasoning and restate the graph whenever it changes.

The procedure, in short (full algorithm in `references/planning.md`):

1. **Seed.** Write the answer you would naturally give to the question, as a rough outline. This is only a scaffold for finding concepts.
2. **Extract.** List every term, mechanism, convention, number, name, and step in that outline. Each potential source of "wait, what is that?" or "why is that so?" is a candidate node.
3. **Simulate the newcomer.** For each candidate and each claim, ask three questions: Would a person with zero background know this word? Would they wonder why it is this way? Is there a leap I am skipping because it feels obvious? Every "yes" creates a new node, a new "why" to attach, or a bridge step.
4. **Recurse.** Treat every new node as a topic of its own and repeat steps 1-3 on it. Continue until a full pass adds nothing new. This is *closure*, and it is what makes the later explanation self-sufficient.
5. **Deduplicate.** If two parents need the same concept, it is one node with two outgoing edges. The structure is a graph, not a tree.
6. **Find the roots.** Roots are nodes with no dependencies: ideas a newcomer can grasp from everyday experience alone. Every chain must bottom out in roots.
7. **Layer and order.** Layer 0 is the roots; layer *k* is one more than the deepest dependency. Derive the teaching order from this (rules in `references/planning.md`).
8. **Anchor the goal.** Mark the node(s) that answer the user's original question. Everything in the graph should lead there, or be explicitly optional.

You are done planning only when you can state, for any node, exactly which nodes must come before it and why each is needed.

## Phase 2 - Scoping questions

Now ask the user a short batch of questions, **in one message**, so the graph can be trimmed to what they actually need. Make them concrete by using the real plan (name real branches and real concepts) rather than generic "what is your level?" prompts. If your environment offers an interactive choice tool (for example `ask_user_input_v0`), use it for the closed questions; otherwise use a short numbered list the user can answer in one line.

Cover these, skipping any the user already answered:

1. **Purpose.** What will you do with this knowledge (build, pass an exam, decide something, curiosity)? This decides which branches matter and how deep to go.
2. **The floor.** Propose the level you will treat as known (for example "you have used a web browser and know what a file is") and ask them to confirm or lower it. Default floor if they do not care: ordinary everyday life and general literacy. Anything above the floor gets taught.
3. **Branch selection.** Show the main branches in plain words, and ask which are needed, which can be skipped, and which are already known. This is how you learn "can some of this be omitted, or is everything needed?"
4. **Depth.** Practical "how it works and how to use it", or full "why it was designed this way", including history and trade-offs.
5. **Pace.** Small steps with a pause each time, or bigger steps with fewer pauses.

Keep it to what you genuinely need, normally three to five questions. If the user replies "just go" or "everything", apply the defaults: all branches, everyday-knowledge floor, full depth, small steps.

## Phase 3 - Freeze the plan

Apply the answers to the graph, silently:

- **Skipped branch:** drop it only if no kept node depends on it. If a kept node depends on it, keep the node in **compact** form (still explained, but briefly, with its whys) and tell the user in one line why it stayed.
- **Already known:** mark it `known`. Do not teach it, but keep it as a node so the chain stays connected, and give it a single recap line at the point where it is first used (with its why). If the user later looks confused, treat that as a gap (Phase 6) and teach it fully.
- **Optional:** branches the user wants only "if time allows" become dashed optional nodes, offered at the end.
- **Too big:** if the graph exceeds roughly 40 nodes, split into modules, each with its own diagram and a clear hand-off to the next, and tell the user.
- Re-validate that the pruned graph still has no missing dependency and no cycle, then fix the final teaching order.

## Phase 4 - Present the map

The **first thing** in this message is the Mermaid diagram of the whole graph. No preamble, no lengthy intro: the diagram explains itself, and the user should see the whole territory immediately. Conventions are in `references/mermaid-and-diagrams.md`; the essentials:

- Arrows run from prerequisite to dependent, so the flow reads from simple foundations up to the goal.
- Style roots, known, optional, and goal nodes differently, and number every node with the number that will appear in the steps.

After the diagram, add only:

- **The path:** a numbered list of steps, one line each (about 12 words max), saying which nodes each step covers.
- **Assumed floor / skipped by your choice:** one line each.
- A closing line: "Say **start** to begin with Step 1."

Keep this section short. If the diagram needs a paragraph of explanation, the diagram is too complicated; split it.

## Phase 5 - The teaching loop

Deliver one step per message, in the order fixed in Phase 3. Use this shape:

```
### Step {k} of {K} - {node name(s)}
**Builds on:** {earlier nodes}  |  **Needed for:** {the later node this unlocks}

{Explanation. Each new term appears in bold the first time, right where it is
defined. Every statement carries its why.}

**Concrete example:** {a small, specific case that uses only what is already taught}
**In one line:** {the single sentence to remember}

---
Progress: done {ids} | next {ids and names} | remaining {n}
Say **continue** for the next step. If anything felt unclear, tell me which part:
I will treat it as a gap in my plan and fix it.
```

### Rules for writing a step

- **Only use what is already taught.** Every term in a step must be (a) a node already explained, (b) below the agreed floor, or (c) the concept being defined right now. If you notice you need a term that is none of these, stop: the plan has a hole. Fix it by Phase 6 before sending. Forward references are not allowed; the "Needed for" line may *name* a later node but the step must not rely on it.
- **A why for every substantive statement.** Facts, rules, mechanisms, names, numbers, defaults, and design choices each get their reason in the same sentence or the one immediately after. Follow `references/why-discipline.md` for what counts as a good why, when to stop asking why, and how to stay honest when the real reason is unknown or arbitrary.
- **Say why we are here.** Open by linking to the previous bricks and the reason this brick is next. A learner who knows why a concept is being introduced holds it better and is less likely to wonder where this is going.
- **Concrete before abstract, example after definition.** Examples must use only taught concepts. An analogy is allowed if it is labeled as an analogy and you say where it breaks down, because an unmarked analogy becomes a false belief.
- **Size.** Aim for a step the learner can absorb in a few minutes (roughly 250-600 words). One dense concept per step, or up to three small ones that only make sense together. If the learner asks for bigger or faster steps, merge nodes, but keep every why.
- **Stay on the graph.** Do not introduce concepts the graph does not contain. If you feel the urge to mention something extra, it is a missing node: add it through Phase 6 first.
- **Final step.** The last step must explicitly answer the user's original question, connecting the goal node back to the chain of bricks that supports it, so the learner can see that the question is now answerable from first principles.

### Before sending every step, run this self-check

1. **Term audit.** Underline every technical or unusual word. Is each one taught, below the floor, or being defined now?
2. **Why audit.** Go through the sentences. Does each substantive one carry a specific reason? Replace vague reasons ("for efficiency", "best practice", "it is standard") with the concrete problem they avoid.
3. **Leap audit.** Is there any point where the reader must supply a missing intermediate step? Add it.
4. **Order audit.** Does the step rely on anything that comes later?
5. **Size and graph audit.** Is it a digestible size, and does it match the plan?

Do not show the checklist to the user. If an audit finds a hole, patch the graph first.

### Pacing

Never send two steps in one message unless the user asks. After each step, wait. The user's only normal action should be "continue". The pause matters because the learner decides when they have absorbed the brick; running ahead recreates the information flood this skill exists to prevent.

## Phase 6 - Gap repair (any time the user asks a side question)

The goal of the whole skill is that side questions never happen. When one does, the original graph or explanation failed, and the response has a fixed shape (full procedure, gap taxonomy, and worked examples in `references/gap-repair.md`):

1. **Diagnose.** Decide which kind of gap it is: missing concept, missing why, a leap in reasoning, an ambiguous term, wrong order, or a genuine scope extension.
2. **Patch the graph recursively.** Add the new node(s), then run the Phase 1 procedure on them, since the new concepts will have their own dependencies. Then sweep forward: a question reveals what the learner does not know, so check upcoming nodes for the same kind of hole and fix them now rather than waiting for the next question.
3. **Output the updated Mermaid diagram first.** It is the first thing in the reply, with new nodes and edges highlighted, followed by at most two lines naming the gap. No lengthy apology or commentary.
4. **Teach the patch.** Explain the new nodes as proper steps, in order, following all the Phase 5 rules, with their whys.
5. **Re-attach.** Show how the patch connects back, including a retro-note if an earlier step silently relied on the missing idea ("Step 3 said X; what that really meant is..."). Then resume at the step where you left off, and renumber nothing the user has already seen without saying so.
6. **Log it.** Record the question, the diagnosed gap, and the nodes added. The log is part of the final summary because these questions reveal exactly what was not obvious to this learner.

If the user says something vague like "I don't get it", do not guess blindly: restate the last step from one level lower (as if the floor were lower), and offer a single narrowing question ("was it the part about X or Y?") only if the first attempt is unlikely to land.

## Phase 7 - Wrap-up and summary

When the last step is delivered, or the user signals they are satisfied, **automatically offer** to produce a markdown summary. Do not wait to be asked.

The summary must capture the whole flow from simple to complex, and it must be built from the **latest** version of the graph, including every node added through gap repair. The questions the user asked are the most valuable part, because each one marks something that genuinely was not obvious, so they get their own section. Template in `references/state-and-summary.md`.

Create it as a `.md` file (and present it with the file-presenting tool if one exists; otherwise print it in the reply). If the user wants another form, such as one note per concept for a notes system, adapt to that while keeping the graph and the gap log.

Also offer, briefly, the optional branches that were parked, in case the user wants to go further.

## Multi-agent mode

Parallel subagents can help when the graph is large, when research is needed to get the structure right, or when explanations should be fact-checked independently. They also cost more and add coordination risk.

**Never start subagents without asking the user first.** Let them choose how to set it up. Ask whether to use subagents at all, for which jobs, with which models, and how many in parallel. If the user says "use the default", use the **newest Sonnet model as coordinator and the newest Haiku model as subagents**. Resolve "newest" from the model list or documentation available in your environment rather than from memory, and state the exact choices back in one line before launching. If the user does not answer, proceed with a single agent. If your environment cannot run subagents, say so and continue single-agent.

The coordinator always owns the graph, the order, the self-check, and the voice of what the user reads. Subagents draft or research; they never decide structure. Everything about briefing, merging, and verifying is in `references/multi-agent.md`.

## Edge cases

- **The user changes the goal midway.** Treat it as a re-plan: rebuild the graph for the new goal, reuse already-taught nodes (mark them done), show the new diagram first, and continue.
- **The user returns later or the conversation is long.** Restate where things stand: show the current diagram with done/next marked, then continue. Never rely on the user remembering the plan.
- **The question rests on a wrong premise or reveals a misconception.** Add a node that explicitly corrects it (and explains why the misconception is natural), rather than only answering around it.
- **The topic is contested or the real reason is unknown.** Say so. A why that is merely invented is worse than "the reason is not well documented; the commonly given explanation is...". See the honesty rules in `references/why-discipline.md`.
- **The user wants to skip ahead.** Allow it, but name which unexplained nodes the jump depends on and offer to cover them compactly.
- **A concept is both a prerequisite and depends on its dependent (a cycle).** Break it by teaching a rough first version, then the dependent, then the refined version. Details in `references/planning.md`.

## Reference files

Read these when the matching phase is active; they are not needed all at once.

- `references/planning.md` - the recursive expansion algorithm, node cards, floor, layering, ordering, cycles, size limits (Phase 1 and 3).
- `references/why-discipline.md` - how to attach a why to every statement, terminal reasons, honesty, with worked examples (Phase 5).
- `references/mermaid-and-diagrams.md` - diagram syntax, legend, status styling, how to show updates and handle big graphs (Phases 4 and 6).
- `references/gap-repair.md` - gap taxonomy, repair procedure, forward sweep, worked examples (Phase 6).
- `references/multi-agent.md` - the ask-first script, defaults, roles, briefs, merging, verification (multi-agent mode).
- `references/state-and-summary.md` - state file schema and the final summary template (Phases 1 and 7).
