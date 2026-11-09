---
name: hillclimb
description: Build something, have a council of reviewer agents score it out of 10, fix, and repeat until every reviewer clears the bar. Use when the user says "hillclimb" or "hill climb", or asks to keep iterating until reviewers rate the work N/10.
---

# Hillclimb

A builder makes the work. A council of independent reviewers scores it out of 10. You fix what blocks the bar and run another round, until every reviewer clears it. You own the loop's integrity: a fixed bar, honest scores, and a tight scope.

The work can be anything a reviewer can inspect: an app UI, a feature, a document, an image set, a script. It comes in two shapes:

- **One artifact** improved in place (a UI, a PR).
- **A candidate set** (icons, thumbnails, titles): several variants per round. Each candidate gets a permanent ID (`r<round>-<k>`) and a file that is never overwritten.

pstack's hillclimb playbook is a different loop: it climbs a measured metric. Use this skill when the score comes from reviewers.

## 1. Set up

Read the request for five things:

- the **work**;
- the **criteria** (e.g. "visual appeal, ease of use, intuitive design");
- the **reference bar** (e.g. "against YouTube Studio", "beats most thumbnails in this niche");
- any **hard requirements** (e.g. the exact text "EVERYONE HATES YOU!");
- the **finish** (open a PR, show me, install the icon).

Infer what's missing, and state your inferences in the same message as the setup questions, so one reply can correct both.

**Find the models.** In T3 Code, call `orchestrator_capabilities`; `delegate_task` can start any model it lists. Elsewhere, use the models your own subagent tool can start. List the latest flagship from each reachable provider. If only one provider is reachable, list its two or three strongest current models instead, and note in the kickoff message that this harness can't run a cross-provider council.

**Ask the setup questions** and wait for the answers before building. Skip any question the request already answers. Put your recommendation first:

1. **Threshold** out of 10: 9 (recommended), 8, 10.
2. **Max rounds**: no cap (recommended; a stall still stops the run and asks you), 5, 10.
3. **Reviewers**: the models you listed, more than one allowed. Pre-mark the latest Claude Opus and the latest GPT Sol. If either is unreachable, pre-mark the strongest reachable model from another provider in its place.

Each chosen model gets one reviewer.

Use your harness's question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex) as far as its limits allow. Ask whatever it can't hold as a numbered list in chat, with your recommendations marked, then end your turn and start when the user replies. Use the recommendations without asking only if the user says not to ask.

**Map the council.** Give each reviewer a slot ID, a short name for its model (`opus`, `sol`). Map each slot to the tool that will start it, its model, and a machine where it can read the workspace and see the work. If a reviewer runs on another machine, copy or sync the workspace there before every round. If a slot can't run, tell the user and get a revised council before you start.

**Define the pass.** The overall score must reach the threshold. So must every criterion the user named as a target; by default, that's all of them. Every hard requirement must hold, and the reviewer must report no blockers (for a candidate set, none tagged with that candidate's ID).

Done when the threshold, the round cap, the mapped council, the criteria, the bar, the hard requirements, the pass and the finish are all fixed. Post them in the kickoff message.

## 2. Write the brief

Make a workspace, `hillclimb-<slug>/`, in a scratch folder outside the repo that survives a reboot. Write `BRIEF.md`, the one file every reviewer reads every round. It covers:

- **Role**: an independent, strict senior reviewer in the domain. Judge against the reference bar; be concrete rather than polite.
- **How to see the work**: URLs of running servers, file paths, commands, screenshot helpers, and the conditions to judge under (widths and themes; feed size, e.g. "shrink to 360 px and score that view"). Start servers before round 1, on sandbox data if the real data could be harmed.
- **Criteria**: each scored 1–10, plus one overall score. Explain what the threshold means in the bar's terms. State the pass: REACHED means the overall score and every target criterion are at or above the threshold, every hard requirement holds, and there are no blockers.
- **Hard requirements**: missing any one makes the verdict NOT YET, whatever the scores.
- **Grading rule**: sort every finding into exactly one list.
  - **Blocks a <threshold>**: what a top practitioner would not ship (contradictions, confusing flow, broken layout, inconsistency, jargon, visible defects). Rank it, and give each item the location, the problem, a concrete fix and an evidence path.
  - **Polish nits**: what they would still ship.
  - If the blocking list is empty, the overall score and every target criterion are at or above the threshold. Any score below the threshold needs at least one blocker that explains it. Hold the bar, and report only blockers you'd defend.
- **Known non-defects**: things the environment causes that are not flaws (empty sandbox data, missing media). Add to this list when reviewers flag such things.
- **Output**: the scores, then `VERDICT: REACHED (<overall>)` or `VERDICT: NOT YET (<overall>)`, then the two lists, all in under about 800 words. For a candidate set, give each candidate's ID, scores and verdict in about 120 words each, tag every blocker with its candidate ID, then name a top pick and the one change most likely to raise it.
- **Safety**: read-only. Write only into your own new, empty folder. Never take an action that sends, publishes, approves or uploads. Never use `rm`, and never put globs or variables in a destructive command.

Keep the bar, criteria, pass and grading rule fixed for the whole run. Later edits to the brief may only make it clearer, for example by adding known non-defects.

## 3. Build

Build the best version you can before the first review, because a weak first draft wastes a round. Do the build yourself, or delegate it when it needs a tool or model you lack, such as image generation. Before round 1, confirm that the builder's machine has that tool.

For a candidate set, make several variants per round. Save the exact prompt or input behind each one, and have the builder leave scoring and ranking to the reviewers. Each round, vary one element of the input, guided by the reviewers' advice, so you can tell what moved the score. After a stall, pivot instead (step 5). Put the current leader into every new set, so it's judged side by side with the new variants. The leader is the candidate with the highest lowest score, comparing the overall and target-criterion scores in each slot's latest review of that candidate. Break ties by the higher mean of those scores, then by the newer candidate.

Before each review, run whatever checks the work has (tests, type check, build, smoke run, hard-requirement check), and send only work that passes. Snapshot each revision into `round-<n>/`: the commit SHA or candidate files, screenshots or other rendered output where they apply, and a few lines on what changed.

## 4. Review

Start a fresh reviewer for every slot each round, all in parallel. Give each one `BRIEF.md`, its slot ID, its own folder, and its previous review if it has one. In T3 Code, start every reviewer with its own `delegate_task`, whatever its provider.

From round 2 on, also give them `round-<n>/ROUND.md`:

- every slot's previous scores (scores only, no findings);
- what changed since, by theme;
- the blockers you declined, and why;
- "Judge it as it is now, fresh and strict, with no credit for effort."

Save each reply to `round-<n>/reviews/<slot>.md`. Wait for every reviewer to finish, however long it takes: a review of complex work can run for hours. Wait on each one's completion notice.

A reviewer that errors out or returns no verdict has given no review. It never counts as a pass. Start one replacement in the same slot. If the replacement also fails, stop: keep the completed reviews and the current work, and ask the user how to proceed.

Check every review against the pass. If its verdict contradicts its own scores or its blocking list, follow the scores and the list, and note the conflict. If a score is below the threshold but no blocker explains it, count the review as NOT YET, and ask that slot's next reviewer to name the blocker. Log each review in `LEDGER.md`, one row per slot per candidate scored: round, slot, candidate ID, scores, verdict, blocker count, the top blocker, and how long the review took.

## 5. Decide

- **Pass**: in the same round, every slot passes the same revision (for a candidate set, the same candidate ID; if several pass, the leader wins). A pass belongs to the revision it reviewed: if the work changes, every slot reviews again. After a pass, change only what the finish needs, and report the remaining nits rather than fixing them. Finish steps such as exporting files, installing an icon or opening the PR leave the work unchanged and need no new review. Go to step 6.
- **Fix themes, not instances**: when the same kind of complaint comes back in a new place, fix the whole class once (one vocabulary, one layout token, one source of truth) and name the theme in `ROUND.md`.
- **Hold the scope**: fix the blockers you agree with. Decline any that would grow the work beyond the request, and record why in `ROUND.md`. When reviewers disagree, decide, and tell both next round. Do the cheap nits; nits never block.
- **Keep the best** (one artifact): if every slot scores a revision below the previous one, revert to the better revision before fixing.
- **Stall**: if for two rounds no slot's overall score rises above its best so far (for a candidate set, the leader's lowest score), or one blocker survives two fixes, pivot: fix the theme, rethink the design, or try something more radical. If the next round is still flat, stop and ask the user, with the ledger.
- **Cap**: every review round counts toward the cap, re-checks included. At the cap, stop. Report the best revision, its scores and its open blockers, then ask how to proceed.

Otherwise, go back to step 3.

## 6. Finish

Do the finish the user asked for. Report:

- a score table, one row per slot and one column per round, writing `no score` where a reviewer gave none;
- one line per round on what changed;
- the final revision or winning candidate, with paths to the snapshots;
- the decisions you made: blockers you declined, re-checks, stall pivots;
- the nits still open.

If the work ends in a PR, put the score table under `## Hillclimb review` in the description. For runs longer than about three rounds, also write `CHANGELOG.md` in the workspace, with one section per revision linking its snapshots, so the user can see how the work evolved.
