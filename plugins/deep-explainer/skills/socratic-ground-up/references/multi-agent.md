# Multi-agent mode

Parallel subagents can speed up planning and drafting for large topics. They also cost more, add coordination risk, and can lower quality if the work is not checked. The rule that governs everything here: **ask the user first, and let them set it up.**

## Contents

- When it is worth offering
- The ask-first step
- Defaults
- Roles and division of labor
- Briefing a subagent
- Merging and quality control
- Failure modes
- If subagents are not available

## When it is worth offering

Offer it (do not start it) when at least one of these holds:

- The graph is large (roughly 20+ nodes) or the topic has several independent branches.
- The structure needs research to be correct (new, specialized, or fast-moving field).
- The user wants high assurance on facts and whys and an independent check is valuable.

Do not offer it for small topics: the coordination overhead exceeds the gain.

## The ask-first step

Never spawn subagents before the user has answered. Ask in one compact message, using an interactive choice tool if the environment has one, otherwise a short numbered list. Cover:

1. **Whether to use subagents at all.**
2. **Which jobs** to parallelize: (a) *planning/expansion*, one subagent per branch to find hidden dependencies; (b) *quest-card drafting*, one subagent per node or cluster to write the question ladders; (c) *audit and verification*, independent checks of answerability, facts and whys; or any combination.
3. **Which models**: a coordinator model and a subagent model. Offer "default".
4. **How many in parallel**, and whether subagents may use web search.
5. (Optional) A reminder of the trade-off: more agents means faster and broader but more cost, and the coordinator still reviews everything.

Example:

> This topic has several independent branches, so I could split the research across subagents. How would you like to set it up?
> 1. Use subagents? (yes / no)
> 2. For what? (expand the plan / draft question ladders / audit and fact-check / all)
> 3. Models: choose your own, or say "default"
> 4. How many in parallel, and may they search the web?

The user's answer is binding. If they say "no" or do not answer, continue as a single agent. If they change their mind later, adapt.

## Defaults

If the user says "default" (or "use the default"):

- **Coordinator:** the newest Sonnet model available.
- **Subagents:** the newest Haiku model available.
- **Jobs:** planning expansion and quest-card drafting; the coordinator does the answerability audit and verification itself.
- **Parallelism:** one subagent per major branch, capped at a sensible number (about 4-6) unless told otherwise.
- **Web search:** allowed if the topic benefits from it.

Resolve "newest" from the model list or documentation that your environment exposes at run time, not from memory, because model names change. Before launching, state the exact choice back in one line ("Coordinator: <model>; subagents: <model>; 4 in parallel; web search on") so the user can correct it. If you cannot determine which models are available, say so and ask the user to name them.

## Roles and division of labor

**Coordinator (you):**
- Owns the dependency graph, the order, the learner's progress state, and **every word the learner reads**. The live dialogue is always yours, in one consistent voice, because Socratic guidance depends on reacting to the learner's last answer; a subagent cannot do that.
- Writes the briefs, merges results, audits quest cards, resolves new concepts that subagents discover, and runs the recursion to closure.

**Subagents (never talk to the learner):**
- *Branch expander:* given one branch of the topic, runs the newcomer simulation and returns candidate nodes, dependencies, and unresolved terms.
- *Quest-card drafter:* given one node and its allowed premises, drafts the quest card (scene, given facts with whys, ladder of baby-step questions with expected answers, likely wrong answers with counter-scenarios, name, consolidation, transfer check).
- *Answerability auditor:* independently checks each question of a quest card: can it be answered using only the floor, mastered nodes, and the facts in the scene? Is it one idea? Is every leap small? Flags any question that is a guess, a trick, or too big.
- *Verifier:* checks facts, history, numbers, and whys.

Why the split: structure and live dialogue need a global view and consistent judgment, which one agent should hold; drafting and checking cards are local and parallelizable. Quest cards can be prepared ahead, but the *dialogue* only ever uses them as maps; the coordinator adapts to the learner's actual answers.

## Briefing a subagent

A subagent knows nothing about this conversation. Give each a self-contained brief:

```
You are helping build a ground-up explanation of "<topic>" for a learner who knows nothing beyond: <floor>.

Your assignment: <expand branch X / draft the quest card for node N / audit quest card C / verify draft D>.

Rules:
- Nothing may be assumed. Every technical term you use must be in the ALLOWED VOCABULARY below, below the floor, or the concept you are defining.
- Every statement the *agent* makes as a source of truth needs a specific reason ("because ...", naming what would go wrong otherwise). If the true reason is unknown or arbitrary, say so; never invent one.
- Questions must be baby-sized (one idea, answerable in a word or a short sentence) and answerable using only the floor, the allowed vocabulary, and facts stated in the scene. Never write a question that needs an untaught term.
- If you need a term that is not allowed, do NOT use it silently. List it under NEW TERMS.
- Mark claims you are unsure about under UNCERTAIN, and give sources if you used search.

ALLOWED VOCABULARY (already taught): <list of nodes with one-line definitions>
THIS NODE: <id, name, plain definition, needs, why it exists, claims to cover>

Return:
1. DRAFT: <quest card / expansion / audit report>
2. NEW TERMS: <terms you needed but were not allowed>
3. UNCERTAIN: <claims and why>
4. SOURCES: <if any>
```

Keep briefs short and specific. Give only the context each subagent needs.

## Merging and quality control

1. **Collect NEW TERMS.** Every one is a potential missing node. Add it to the graph and decide whether another delegated round is needed (closure is still the goal).
2. **Audit every card yourself** with the pre-send checklist (answerability, size, on-thread, whys, map consistency). Smaller models tend to write questions that are too big, leading, or answerable only by guessing, and generic whys ("for efficiency"); fix them.
3. **Reconcile conflicts.** If two subagents define a term differently, pick one meaning and fix both (one word, one meaning).
4. **Check consistency** of numbering, vocabulary, and tone across drafts, and rewrite into one voice.
5. **Verify facts** that matter (dates, versions, numbers, "who decided and why"), either by a verifier subagent or by your own search.
6. **Re-validate the graph** after merging (acyclic, complete, ordered).

Cards can be prepared ahead, but the learner receives **one question at a time**, adapted to their answers. Never paste a card or ladder to the learner.

## Failure modes to avoid

- Launching agents without asking, or with models the user did not choose.
- Letting a subagent restructure the graph.
- Passing through cards unreviewed.
- Briefs that omit the allowed vocabulary, which causes silent use of untaught terms.
- Subagents inventing reasons because "a why is required". Briefs must say that "unknown" is acceptable.
- Too many agents for a small job; the overhead dominates.
- Letting a subagent address the learner, or pasting its text unedited. The learner should meet one consistent guide.

## If subagents are not available

If the environment cannot run subagents, say so plainly in one line and continue as a single agent. You can still approximate the benefit by doing the planning in separate passes per branch and a separate verification pass before presenting each step.
