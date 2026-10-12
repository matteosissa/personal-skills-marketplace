# Staying on track

In guided questioning, the learner reasons out loud, which is exactly when conversations drift: a clever tangent, a jump ahead, a wrong mental model, a half-answer to a different question, fatigue. The agent's job is to keep the thread without suppressing the learner's thinking. This file is the playbook.

## Contents

- Why conversations derail
- The three anchors
- Classify every reply
- Policies by reply type
- The parking lot
- Re-anchoring recap
- Jump-ahead handling
- Reasoning in a wrong direction
- Commands the learner can use
- The agent's own discipline
- Long conversations and returning later
- Examples

## Why conversations derail

- Curiosity: a real question the learner wants answered *now*.
- Confusion: an unexplained term or missing step.
- Jumping ahead: the learner already half-sees a later idea.
- A wrong mental model that makes the current question look different.
- Tiredness or boredom.
- The agent's own vagueness: a question that could be read two ways.

Most derailments are signals about the plan or about the learner, not misbehavior. Treat them as information, but keep the thread.

## The three anchors

These three habits do most of the work:

1. **Thread line.** Start every question message with a one-line italic anchor: node, and rough position in the quest: `*Node 5 · Port - question 3 of ~6*`. It tells the learner where they are at a glance and tells you where you are. Use "~" because the length can change.
2. **One question per message.** One pending question means one thing to answer, and a clear way to tell whether the learner answered it.
3. **Restate the pending question after any detour.** Whenever you handle anything other than the pending question, finish by repeating that question (verbatim or in tightened form). A detour never ends without returning to it.

## Classify every reply

Before responding, silently decide which of these the learner's reply is. Many replies are a mix; handle the most important part first.

| Type | What it looks like |
|---|---|
| **A. Answer, correct** | Answers the pending question correctly |
| **B. Answer, partial** | Right idea, incomplete or imprecise |
| **C. Answer, wrong** | A sensible but wrong answer, usually due to a misconception or a missing premise |
| **D. Stuck** | "I don't know", "idk", silence, "hmm", "?" |
| **E. Clarifying question** | Asks what a word or a step in the *current* scene means |
| **F. Gap question** | Asks about a concept or reason the plan did not cover |
| **G. Tangent** | Asks or reasons about something else, not required for the current node |
| **H. Jump-ahead** | Answers more than asked, or proposes the answer to a later node |
| **I. Meta** | About the process: pace, hint, skip, show map, "where are we" |
| **J. Frustration or fatigue** | Short, irritated, or disengaging |

## Policies by reply type

- **A (correct).** Confirm with the reason, then the next question. If correct without reasoning, add a why-probe first.
- **B (partial).** Keep what is right, name the missing piece, ask a smaller question about it.
- **C (wrong).** Do not correct directly. Use a **counter-scenario**: a small concrete case where their idea leads to something that clearly does not work, and ask what happens. See "Reasoning in a wrong direction". If the wrong answer came from an untaught term, it was an answerability failure: fix the plan (gap) and own it in one line.
- **D (stuck).** Climb the hint ladder (`socratic-method.md`). "Tell me" goes straight to level 4. Never make them feel slow.
- **E (clarifying).** Answer immediately and plainly, with its why (vocabulary is told, never withheld). Then check whether this is a gap: if a word in the scene was not understood, other words may not be either, so scan the upcoming scene and fix it. Then restate the pending question.
- **F (gap).** Run the repair in `gap-repair.md`: diagnose, patch the graph recursively, **show the updated map first**, then teach the patch (as a quest if derivable, told if not), then return to the interrupted question.
- **G (tangent).** Acknowledge it in one line, park it (parking lot), and return to the pending question. Do not answer it now unless it turns out to be a gap (if answering is *required* to understand the current node, it is F, not G).
- **H (jump-ahead).** See "Jump-ahead handling".
- **I (meta).** Execute the command (see "Commands"), then restate the pending question.
- **J (frustration or fatigue).** Lower the effort: shrink the next question, offer options, or offer to tell the next part and then check with one small question. Offer a pause. Never push through or lecture. Do not take the tone personally.

If a reply is a mix (for example a correct answer *plus* a tangent), handle in this order: respond to the answer, park the tangent in one line, ask the next question.

## The parking lot

A list of side topics the learner raised that are not needed for the current node. Purpose: respect their curiosity without losing the thread.

- Add an item in one line: "Good question about how encryption fits in. I've parked it; we'll see if it comes up on the map, or we can go there when we finish the main path."
- Keep it in the state file with the node where it came up.
- **Check at every node boundary.** If a parked item has become answerable (its prerequisites are now mastered) or is now needed by the next node, bring it up at that moment.
- **Show on request** and **offer at the end**: the parked items become optional branches on the map or a short follow-up path.
- Never silently drop a parked item, and never answer parked items mid-quest unless they became a gap.

## Re-anchoring recap

Use a recap whenever the learner seems lost, after two consecutive off-thread replies, after a long detour, or when they come back after a pause. Keep it to three lines:

```
So far: <what we have worked out in this node, in the learner's own words if possible>
We're working out: <the target of this node, in plain words>
Back to the question: <the pending question>
```

Do not re-explain the whole node; the recap restores the thread, nothing more.

## Jump-ahead handling

The learner leaps to a later idea ("so then there must be a number for each program, like 80?").

1. **Validate what is right**, with its reason (credit their reasoning, not just the conclusion).
2. **Bank it.** Mark the beats or nodes it covers as `pre-answered` in the state. When you get to that node, start from their formulation and spend only a check question or two, instead of asking every beat again.
3. **Check support.** Did they leap *correctly*? If their answer rests on a premise they have not actually established (a lucky guess), ask a short why-probe, because correct conclusions with no support are fragile.
4. **Return** to the pending question if the jump skipped something needed for the rest of the node. If the jump really covers the node, skip ahead on the ladder and say so ("You've just done our next two questions in one go.").

## Reasoning in a wrong direction

When the learner builds a coherent but wrong model, do not argue and do not lecture.

1. **Follow their idea one step**, honestly. "Suppose that's true. Then in this situation..."
2. **Build a counter-scenario** that is tiny and concrete, where the idea gives an absurd or impossible result.
3. **Ask what happens**, and let them notice the contradiction.
4. **Let them repair it.** They propose the fix, you confirm with the reason.
5. If the misconception is likely to recur, add a node that states the correct model and why the wrong one is tempting (see misconception in `gap-repair.md`).

Never say "that's wrong" bluntly. Say "that works if ___, let's see whether it holds here".

## Commands the learner can use

Tell the learner at the start (Phase 4) that they can say these at any time. Support all of them:

| Command | Effect |
|---|---|
| `map` / `where are we` | Show the current coloured map and a one-line status, then restate the pending question |
| `hint` | Next level on the hint ladder |
| `tell me` / `just explain` | Level 4 immediately: state it with its why, then one tiny confirming question |
| `skip` | Mark the node `skipped` (not mastered); say which later nodes depend on it and offer a compact explanation instead |
| `faster` / `bigger steps` | Merge beats: fewer, slightly larger questions, same whys |
| `slower` / `smaller` | Split beats further; add options |
| `park this` / `later` | Add the current thought to the parking lot |
| `recap` | The three-line re-anchoring recap |
| `options` | Present the current question as a tap-to-choose or A/B/C |
| `pause` | Save state; summarise where we are so it is easy to resume |

## The agent's own discipline

The agent can derail the conversation too. Hold to these:

- **Never ask a question that is not in the quest card's ladder**, unless it is a hint, a why-probe, or a counter-scenario that serves the current beat.
- **Never abandon a pending question** without writing, in your state, why (gap found, jump-ahead banked, etc.) and how you will return.
- **Do not chase the learner's tangent yourself**, even if it is interesting. Park it.
- **No answer sprawl.** Responses are short: feedback, optional consolidation, a map if due, then a question. If the message is growing, you are lecturing; cut.
- **Ambiguity is your fault.** If a learner's answer shows they read the question differently, rephrase it, do not mark them wrong.
- **Keep the numbering honest.** If order changes, say so once.
- **Update state before every reply**: current node, beat index, pending question, hint level, ledger of established facts, parking lot, statuses.

## Long conversations and returning later

- Keep a **ledger** per node: the short list of facts the learner has established in their own words. It feeds recaps and the final summary.
- If the learner has been away or the conversation has grown long, open with the recap and the map, then the pending question.
- If you detect that your state may have been lost (for example after a long gap), rebuild it from the map and ledger, and tell the learner briefly: "Here is where we are; tell me if anything looks off."
- Every N nodes (about 4-5), show the full map even if the learner has not asked, so the big picture stays alive. (A map is already shown on every node completion; this rule matters mainly in large graphs when maps are shown at module level.)

## Examples

### Tangent

> Pending: **Q3.** Could someone sending you a message from the other side of the world know which apps you installed?
> Learner: wait, is this how hackers get in?

Response shape:
> Good question; security does connect to this, but it needs a few more pieces first, so I've parked it and we'll come back to it.
> **Q3 again.** Could someone sending you a message from the other side of the world know which apps you installed?

### Jump-ahead

> Learner: so each program gets a number, and web servers use 80?

> Yes, that's exactly where this goes, because the number is what picks the program, and a web server needs a number that browsers can know in advance. I've banked it. One thing to nail down first:
> **Q4.** Why does that number have to be agreed *before* anyone connects?

### Wrong direction

> Learner: the computer will just look at all apps and decide.

> Let's test that. Suppose two apps both want a message that arrived with only the street address. The computer looks at all apps...
> **Q.** How does it choose between a browser and a music app, when the message says nothing about either?

### Frustration

> Learner: ok this is slow

> Fair enough, let's speed up. Here's the short version of this part: [two sentences with whys]. One quick check to make sure it clicked:
> **Q.** ...

### Lost

> Learner: wait what are we doing again?

> So far: a message needs two labels, one for the computer and one for the program.
> We're working out: how a computer tells which program gets a message.
> Back to the question: **Q3.** ...
