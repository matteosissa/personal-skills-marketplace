# Gap repair: what to do when the user asks a side question

A side question means the plan or the explanation had a hole. The skill's goal is zero side questions, so every one is information about where the design failed. Do not just answer it in passing; repair the design, then continue.

## Contents

- Principles
- Step 1: classify the gap
- Step 2: repair by type
- Step 3: forward sweep
- Step 4: the reply, in order
- Step 5: re-attach and log
- Worked examples
- Special cases

## Principles

1. **Every question is a bug report, not an interruption.** Thank nobody and apologize for nothing at length; fix it.
2. **Diagram first.** The updated graph is the first thing in the reply, so the learner immediately sees how the plan changed and that nothing was lost.
3. **Repair is recursive.** The new concept may have its own prerequisites. Run the planning loop on it.
4. **Fix the future, not just the present.** A question reveals what the learner does not know. Look for the same kind of hole ahead.
5. **Never leave the graph and the conversation out of sync.** After the repair, the graph is the plan again.

## Step 1: classify the gap

| Type | Signal | Example |
|---|---|---|
| **Missing concept** | The question asks "what is X?" about a term used in a step | "What is a socket?" |
| **Missing why** | "Why is it X?" about a claim stated without a reason or with a weak one | "Why 80 and not some other number?" |
| **Leap** | "How do we get from A to C?" or "Where does B come from?" | "How does the server know which program to hand it to?" |
| **Ambiguity** | A term was used in two senses, or a reference was vague | "Do you mean the request or the connection?" |
| **Wrong order** | The step used something that comes later, or the learner needs a concept earlier | "You said X before explaining Y" |
| **Misconception** | The question shows a wrong mental model | "So the server remembers me between requests?" |
| **Scope extension** | A new topic outside the original goal ("what about WebSockets?") | An adjacent subject |

A single question can be several types at once. Treat each.

## Step 2: repair by type

- **Missing concept.** Add a node. Run the planning loop on it. Insert it as early as its first use requires, which is usually *before* the step that triggered the question.
- **Missing why.** Add the reason to the original claim. If the reason needs a concept, add that node. Check whether other claims in the plan share the same weak pattern (for example all defaults) and fix them too.
- **Leap.** Insert a bridge node or expand the step with the missing intermediate reasoning (see "Bridge nodes" in `planning.md`).
- **Ambiguity.** Fix the naming in the graph and the remaining steps: one word, one meaning. If two meanings were really needed, create two nodes with distinct names and say how they differ.
- **Wrong order.** Re-sort the graph; correct the dependency that was missing; re-validate the order.
- **Misconception.** Add a node that states the correct model, shows why the misconception is natural, and shows what goes wrong if you hold it. Do not simply answer the question and move on.
- **Scope extension.** Add the new branch as `optional` (dashed) unless the user says they want it now. Say in one line that this goes beyond the original goal, and ask whether to cover it now or after the main path. This is the one case where asking is fine, since the answer changes the plan.

Always check afterwards: does the new node need anything not yet in the graph? Recurse until closure.

## Step 3: forward sweep

The question tells you about the learner's actual floor and habits. Use it:

1. **Lower the floor if needed.** If a basic thing was missing, assume other basics may be too. Update the stated floor.
2. **Scan the remaining nodes** for the same pattern (same kind of term, same kind of unexplained default, same type of leap) and fix them now.
3. **Scan already-taught steps** for statements that silently relied on the missing idea; prepare retro-notes.

The aim is that the *next* question does not happen.

## Step 4: the reply, in order

1. **The updated Mermaid diagram.** First thing in the message. New nodes use the `gap` style, new edges are thick. (Conventions in `mermaid-and-diagrams.md`.)
2. **At most two lines.** Name the gap and what you changed, for example: "Gap: I used 'socket' without defining it. Added node 9 (Socket) below Port, and a bridge node 10 (Why programs need their own address) before it." No lengthy apology and no self-analysis.
3. **The patch, taught properly.** Explain the new node(s) as real steps, in order, following the Phase 5 template (builds on / needed for, whys, example, in one line). For a small patch, one compact step is enough; for a larger one, several, with a "continue" pause between them.
4. **Re-attach.** Say where this connects to what was just taught and return to the interrupted step: "Back to Step 6." If an earlier step used the idea implicitly, add a retro-note ("In Step 3, 'X' really meant ...").
5. **Progress line** as usual.

If the patch was tiny (a missing why on one sentence), the "patch" can be the corrected sentence itself plus the updated diagram, without a full step.

## Step 5: re-attach and log

Add a gap-log entry:

```
Q: <the learner's question, short>
Type: <gap type(s)>
Cause: <what was missing in the plan or the explanation>
Added: <node ids and names>, <edges changed>
Also swept: <other nodes fixed pre-emptively>
```

The log feeds the final summary (see `state-and-summary.md`). Do not renumber already-taught steps without telling the learner; if the order changed, say so in one line.

## Worked examples

### Example A: missing concept

Context: Step 5 said "the server hands the request to the right program using the port."
User: "What exactly is a port? Is it physical?"

Diagnosis: missing concept ("port"), plus a possible misconception (physical). The graph had Port inside the "IP address" step.

Repair: split the node: new node "Port" with its own step, prerequisite "several programs share one machine" (a bridge node, "why one address is not enough"). Forward sweep: check "socket" and "connection", which are also close to this idea; fix the same kind of gap there.

Reply: diagram with the new nodes in orange, two lines naming the gap, then the new steps, then "Back to Step 5".

### Example B: missing why

Context: The step said "web servers use port 80 by default."
User: "Why 80 and not something else?"

Diagnosis: missing why on a convention. Forward sweep: other defaults appear later (443, 8080). Pre-empt them by adding the "why defaults exist" idea once, as a node that those steps depend on.

Reply: diagram (one new node "Why defaults exist", thick edge to "Port"), two lines, then the corrected claim with the full reason, including the honest statement that the number itself is arbitrary.

### Example C: scope extension

User: "And how is this different from WebSockets?"

Diagnosis: scope extension. Reply: diagram with a dashed optional branch "WebSockets" attached to the dependent concepts it would build on, one line "This goes beyond the original question; I added it as an optional branch. Cover it now, or after the main path?", then wait.

## Special cases

- **Vague confusion ("I don't get it").** Re-explain the last step from a lower floor, with more examples and whys. Offer one narrowing question only if the first attempt is unlikely to work. Then treat whatever was confusing as a gap and log it.
- **Two questions at once.** Repair both together in one updated diagram; list both nodes.
- **A question that is already answered later in the plan.** Do not just say "later". If the learner needs it now, move it earlier and say so. If it genuinely cannot be understood yet because prerequisites are missing, show those prerequisites in the diagram, give a one-line honest placeholder ("this depends on 6 and 7; here is the shape of the answer"), and keep the order.
- **The question exposes an error in an earlier step.** Say so plainly, correct it, update the graph and any dependent steps. Honesty beats a clean record.
- **The same kind of gap keeps recurring.** The planning pass is systematically too shallow for this learner. Lower the floor, re-run the newcomer simulation on all remaining nodes, and tell the user briefly that you are doing a deeper sweep.
- **The user is simply curious about something unrelated to the goal.** Treat as a scope extension.
