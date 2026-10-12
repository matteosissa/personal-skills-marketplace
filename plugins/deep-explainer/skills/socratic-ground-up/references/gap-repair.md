# Gap repair in the Socratic skill

A question from the learner that the plan did not anticipate means the graph or the quest design had a hole. The skill's aim is that such questions are rare; each one is a bug report. Repair the design, show the updated map first, then keep guiding.

## Contents

- Principles
- Step 1: classify the gap
- Step 2: repair by type
- Step 3: forward sweep
- Step 4: the reply, in order
- Step 5: re-attach and log
- Worked examples
- Special cases

See also `staying-on-track.md`: it decides whether a reply is a gap question, a clarification, or a tangent in the first place.

## Principles

1. **Every gap question is a bug report, not an interruption.** Fix it; do not apologise at length.
2. **Map first.** The updated map is the first thing in the reply, with new nodes in the `gap` colour and new edges drawn thick.
3. **Repair recursively.** The new concept may have its own prerequisites; run the planning loop on it until closure.
4. **Fix the future.** A question reveals what the learner does not know. Look for the same kind of hole ahead and repair it now.
5. **Telling is allowed.** If the gap is vocabulary or an arbitrary fact, tell it briefly with its why. Do not turn a vocabulary question into a guessing game.
6. **The graph and the conversation stay in sync.** After the repair the graph is the plan again.

## Step 1: classify the gap

| Type | Signal | Example |
|---|---|---|
| **Missing concept** | "What is X?" about a term used in a scene or question | "What's a socket?" |
| **Missing why** | "Why is it X?" about something stated without a reason or with a weak one | "Why 80 and not another number?" |
| **Leap** | "How do we get from A to C?" | "How does the server know which program to give it to?" |
| **Ambiguity** | A term used in two senses, or a vague scene | "Do you mean the request or the connection?" |
| **Wrong order** | Used something not yet established, or the learner needs a concept earlier | "You mentioned X before explaining Y" |
| **Misconception** | The question shows a wrong mental model | "So the server remembers me between visits?" |
| **Unanswerable question** | The learner could not answer because the question needed something they never had (the agent's fault) | They answered "no idea" because a term was never introduced |
| **Scope extension** | A new topic beyond the original goal | "What about WebSockets?" |

One question can be several types. Treat each.

## Step 2: repair by type

- **Missing concept.** Add a node. Decide `guided` or `told`:
  - Vocabulary or arbitrary convention: `told` (brief statement with its why, then a tiny confirming question).
  - Derivable idea: `guided` (a short quest following `socratic-method.md`).
  Run the planning loop on it; insert it before the node that exposed the gap.
- **Missing why.** Add the reason to the original claim (or ask a Socratic question that leads to it if it is derivable). If the reason needs a concept, add that node. Check the plan for the same pattern (for example other defaults) and fix it too.
- **Leap.** Insert a bridge node: a motivating problem, a worked case, or a contrast. Add beats to the quest card.
- **Ambiguity.** Fix the naming in the graph and the remaining quests: one word, one meaning. Two meanings mean two nodes.
- **Wrong order.** Re-sort the graph, fix the dependency, re-validate the order.
- **Misconception.** Add a node that states the correct model, shows why the wrong one is tempting, and shows what goes wrong if you hold it. Use a counter-scenario question rather than a lecture.
- **Unanswerable question.** Own it in one line ("I asked something I hadn't set you up for"), add the missing premise to the scene or the missing node to the graph, and re-ask the question in answerable form.
- **Scope extension.** Add as `optional` (dashed). Say in one line that this is beyond the original goal, and ask whether to cover it now or after the main path. This is the one case where asking is appropriate, because the answer changes the plan.

Afterwards check: does the new node need anything not yet in the graph? Recurse until closure.

## Step 3: forward sweep

1. **Lower the floor if needed.** If a basic thing was missing, other basics may be too; update the stated floor.
2. **Scan the remaining nodes** (their scenes, premises, and questions) for the same pattern and fix them now.
3. **Scan completed nodes** for statements that silently relied on the missing idea; prepare a retro-note.
4. **Re-check answerability** of the upcoming questions given what the learner has shown.

The aim: the next question of this kind never has to be asked.

## Step 4: the reply, in order

1. **The updated map**, first thing in the message (`gap` colour for new nodes, `==>` for new edges; every other node keeps its current progress colour).
2. **At most two lines** naming the gap and what changed.
3. **The patch**:
   - `told` node: the statement with its why, plus one tiny confirming question.
   - `guided` node: a short quest following the usual pattern (scene, ladder, insight, name, check), one question at a time.
4. **Re-attach.** Say how it connects to the interrupted node, add a retro-note if an earlier step silently relied on the missing idea, and **restate the interrupted question**.
5. Thread line and status as usual.

When the patch is tiny (one missing why), the patch can be one corrected sentence plus the map, then the interrupted question.

## Step 5: re-attach and log

Append to the gap log:

```
Q: <the learner's question, short>
Type: <gap type(s)>
Cause: <what was missing in the plan, the scene, or the question>
Added: <node ids and names>, <edges changed>
Also swept: <other nodes fixed pre-emptively>
```

The log feeds the final summary. Do not renumber nodes the learner has already seen. If the order changed, say so in one line.

## Worked examples

### A: missing concept (derivable)

Pending: node 5 (Port), Q3. The learner asks: "what's a program, though? like an app?"

Diagnosis: missing concept, very basic, so the floor may be lower than assumed. Mode `told`: it is vocabulary and a plain definition. Forward sweep: check upcoming scenes for similar basics (process, file, connection).

Reply: map with a new orange node "Program"; one line: "Gap: I used 'program' without checking it was clear. Added node 9."; then a two-sentence definition with its why, one tiny confirming question ("So a browser is a program. Is a music player a program too?"), then the interrupted Q3 restated.

### B: missing why

Context: "web servers wait at number 80". The learner: "but why 80?"

Diagnosis: missing why on a convention. Handling: the *need* for a default is derivable (and normally already in the quest); the *digits* are arbitrary, so tell that honestly. Sweep: other defaults appear later (443); pre-empt by checking they carry the same explanation.

### C: scope extension

The learner: "how is this different from WebSockets?"

Reply: map with a dashed `optional` node "WebSockets" attached to what it would build on; one line: "That goes beyond our question, so I've added it as an optional branch. Cover it now or after the main path?"

## Special cases

- **Vague confusion ("I don't get it").** Re-ask the last question one level smaller, with options, and treat whatever was confusing as a gap afterwards.
- **Two questions at once.** Repair both in one updated map; list both nodes.
- **A question answered later in the plan.** If the learner needs it now, move it earlier and say so. If it cannot yet be understood, show the missing prerequisites in the map, give one honest line ("this depends on 6 and 7; the shape of the answer is..."), and keep the order.
- **The question exposes an error in something the agent said.** Say so plainly, correct it, update the dependent parts.
- **Recurring gaps of the same kind.** The planning pass was too shallow for this learner. Lower the floor, re-run the newcomer simulation on all remaining nodes, and tell the learner briefly.
- **Curiosity unrelated to the goal.** That is a tangent, not a gap: park it (see `staying-on-track.md`).
