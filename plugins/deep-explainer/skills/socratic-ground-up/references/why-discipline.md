# Why-discipline: a reason for every statement

> **How this applies in the Socratic skill.** The learner reasons out most ideas themselves, so the *agent's* statements are fewer, but they still must carry their why. The why-discipline applies to every moment where the agent speaks as a source of truth: (1) the **facts given** in a scene (premises the learner could not deduce), (2) the **feedback** after each answer ("Yes - because..."), (3) the **consolidation** after a quest (naming the concept and stating it with its reasons), and (4) any **told** node. Questions themselves do not need a why, but each must have a *purpose* in the quest card.

The learner cannot tell which facts are arbitrary and which are necessary. A statement without a reason therefore looks like a hole, and a hole produces a side question. Attaching a reason to every substantive statement removes the doubt before it forms. The prose can be a little heavier as a result; that is an accepted price, because a slightly clumsy explanation with no open "but why?" beats an elegant one that leaves three.

## Contents

- What needs a why
- What a good why looks like
- Terminal reasons (where to stop asking why)
- The why ladder
- Honesty rules
- Style
- Worked examples
- Common failures

## What needs a why

Attach a reason to every sentence that states:

- a fact ("a server waits for requests"),
- a rule or constraint ("a request must name the thing it wants"),
- a mechanism ("the message is split into pieces"),
- a name or label ("this is called a header"),
- a number or default ("port 80", "ten minutes"),
- a design choice ("it is plain text"),
- an order ("first this, then that").

Sentences that do not need one: pure transitions ("now that we have X, let us look at Y"; the why of the transition belongs in the step opening), headings, and restatements of something whose why was just given. If you are unsure, add the why. Over-explaining costs a clause; under-explaining costs a question.

## What a good why looks like

A good why is **specific** and **names the problem avoided or the need served**. Test it with the *otherwise* check: complete the sentence "...because otherwise ___". If you can fill the blank with a concrete bad outcome, the why is real. If the blank would be "it would not be as good", it is vague.

Prefer reasons that connect to something the learner already understands (an earlier node, or everyday experience), because that makes the reason checkable by them.

## Terminal reasons (where to stop asking why)

Asking "why?" forever is useless. Stop when you reach one of these, and *say which kind it is* so the learner knows the chain has really ended:

1. **Necessity.** It follows from logic or a physical limit ("a signal cannot arrive before it is sent").
2. **Definition.** It is true because of what the word means; give the reason the word was chosen ("called a server because its job is to serve requests").
3. **Convention.** People agreed on it and the specific choice is arbitrary. Say so explicitly, and give the reason agreement itself matters ("the exact digits could have been different; what matters is that everyone uses the same one, because otherwise a client cannot know where to connect without asking first").
4. **History.** It happened that way because of the circumstances of the time. State the circumstance, and flag your confidence (see honesty rules).
5. **Trade-off.** One benefit was bought with one cost. Name both ("this is bulkier, in exchange for being readable by people").
6. **Taught-for-later.** It is stated now because a later node needs it. Say which one ("we need this because Step 6 builds on it").

If the reason you wrote contains a term the learner has not met, you have found a missing node: go to the planning loop, do not smuggle in the term.

## The why ladder

For each claim:

1. Write the claim.
2. Ask "why is this so?" and write the answer as a trailing clause.
3. Check the answer: does it use only taught terms? If not, add the node (planning) and come back.
4. Ask: could a newcomer reasonably doubt the *answer itself*? If yes, give its reason too (one more rung). Stop when you hit a terminal reason or when the next "why" would only restate the same thing.

Usually one or two rungs suffice. Three is unusual. The goal is to leave no *reasonable* doubt, not to build an infinite regress.

## Honesty rules

The why-requirement is strong pressure to invent reasons. Resist it, because an invented reason is a false belief the learner will carry.

- If the real reason is unknown, undocumented, or contested, say so: "the original reason is not well documented; the commonly given explanation is..., which makes sense because...".
- Mark history with calibrated language ("this was probably chosen because...", "the usual account is..."). Do not state a guess as a fact.
- For dates, versions, specifications, and numbers, verify with web search when available. Facts that change over time are especially error-prone.
- If a statement is only true for some versions, contexts, or conditions, say which, and why the condition matters.
- "Because that is the standard" is only acceptable if followed by why the standard exists and who benefits from everyone following it.

## Style

- Default form: **claim, because reason.** Vary the connective for readability: because, since, so that, which is needed because, which avoids ___ (otherwise ___).
- Keep the reason in the same sentence or the sentence immediately after. A why placed three paragraphs away is a why the learner cannot find.
- Do not hide the claim inside the reason. Say the claim cleanly first, then the reason.
- It is fine for the text to be repetitive in structure. Clarity of cause beats elegance.
- First use of a new term goes in **bold**, with its definition and the reason for the name or the concept.

## Worked examples

### Example 1: a default number

Weak:
> A web server listens on port 80 by default.

Better:
> A web server listens on port 80 by default, because a browser that is given only a website name still needs to know which "door" (port) to knock on, and if everyone agrees on one default number in advance, nobody has to ask or be told. The digits "80" themselves have no deep technical meaning: it is the number that was registered for web traffic when this was standardized, and it stuck because every browser and server afterwards followed the same registry, since a server on a different number would be unreachable to a browser using the default.

Why this works: it gives the need (a shared default), says outright that the specific number is arbitrary, and explains why arbitrary agreement still matters. Every term used (browser, port, registry) must already be taught or be below the floor.

### Example 2: a design choice with a trade-off and a condition

Weak:
> HTTP messages are plain text.

Better:
> Early HTTP messages are plain text, because the designers wanted people to be able to read and debug them just by looking, which keeps the system easy to understand and to build tools for, at the cost of being bulkier than a compact binary format. (This describes the older text-based versions; later versions changed the trade-off, because speed became more important than human readability as the web grew.)

Why this works: names the benefit, the cost, and the scope of the claim, so the learner is not misled when they meet a later version.

### Example 3: a rule

Weak:
> A request has a method such as GET or POST.

Better:
> A request carries a **method** (such as GET or POST) because the server must know *what you want done* and not only *which thing* you mean, since the same address could be read, replaced, or deleted, and without the method the server could not tell these apart. The method is a single word near the start of the request, because the server needs it first to decide how to handle everything that follows.

### Example 4: a name

> The part of the message that describes the message is called a **header**, because, like the heading on a letter, it comes before the main content and tells the receiver how to treat it.

### Example 5: a "because" that is only a restatement (reject it)

> A server is a computer that serves, because that is what it does.

Rewrite as a definition-type terminal reason:
> A **server** is a program (usually on a computer that stays switched on) whose job is to wait for requests and answer them. It is called a server because it *serves* others, and it stays running continuously because a client could ask at any moment and would otherwise find nobody there.

## Common failures

| Failure | Fix |
|---|---|
| "For efficiency / security / performance" | Efficiency of what, compared to what? Security against which specific problem? |
| "Best practice" / "it is standard" | Who benefits from it and what goes wrong without it? |
| "Because that is how it works" | That is the claim again. Give the mechanism or the terminal reason. |
| A why that uses an untaught word | Missing node. Add it in planning. |
| Invented history | State uncertainty or verify. |
| The why is correct but placed far from the claim | Move it next to the claim. |
| All whys are identical in shape and the learner stops reading them | Vary the form and make each one specific. |
| A claim that only holds sometimes, stated as always | State the condition and why it matters. |
