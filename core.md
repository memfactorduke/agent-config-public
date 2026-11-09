## Working with me

Finish the whole job before handing back. Do every step you can yourself: look things up, run the commands, drive the UI (browser, simulator, iPad, computer use). Ask me only for a decision that is genuinely mine, and ask me to act only when no tool of yours can. Resolve every unknown you can; when you hand back, list what's left and why it needs me.

When I say something exists and you can't find it, treat that as a lead and keep digging: other search terms, current docs, the actual UI. Before recommending or concluding, compare the credible alternatives and verify the facts that matter.

When I need to decide, explain the options in plain English and recommend one. Reports and comparisons I ask for come as a polished, clearly laid out, visually designed HTML page, rendered and checked before you hand it over.

## Models and subagents

- Subagents run the latest GPT Sol, except UI work, which runs the latest Claude Opus. Always high reasoning effort.
- Claude models always run at standard speed. Sol subagents use their parent's speed tier; under a Claude parent, `default`.
- Start every Sol prompt with `$pstack:poteto-mode` on its own line, then the brief.
- Set effort and speed explicitly on every spawn; the tools' defaults differ. T3 `delegate_task`: Sol → `reasoningEffort: "high"`, `serviceTier` = parent's; Claude → `effort: "high"`, `fastMode: false`.
- Fable only when I ask for it. Never `max` effort.
- Keep a running chat's model and effort; change them only when I ask.

## Where subagents run

My remote box, with its T3 IDs, is named under "Me and my machines". If none is named there, run subagents on this machine and skip this section.

Run subagents on the remote box by default: it's spare compute, it can run most things, and the machine you're on may be the one I'm using.

Keep one on this machine only when it needs this machine:
- computer use, a logged-in browser, a simulator or device, or a macOS-only tool such as Xcode;
- files too big to copy, such as video and editing media on local drives;
- local secrets, services or MCP servers that the remote box doesn't have.

Small files that live only here are not a reason to stay. Copy them over with `rsync -a`, or push unpushed work first, and point the child at the copy. Most review rounds, image sets, briefs and scratch folders are small.

Helpers a skill spawns for itself (pstack, for example) run where the skill puts them. A quick read-only lookup can stay here too.

How to send one:
- In `delegate_task`, set `target.environmentId` to the remote box's environment ID. Repo work runs in the remote box's copy of the same repository. If it has none, clone it there with `t3_project_clone` (`remoteUrl` = the HTTPS clone URL, `destinationPath` = the remote box's projects folder + `/<repo>`), then register it with `t3_project_create`, both with the remote box's `environmentId`. Outside a repo, also pass `target.projectId` = the remote box's scratch-folder project ID, and have the child work in its own subfolder there.
- Push your branch first: the child sees pushed commits only.
- Children on the remote box share one checkout per repo, and `isolation: "worktree"` isn't available there. Tell a child that edits to leave that checkout alone: `git fetch origin && git worktree add ~/worktrees/<repo>/<branch> -b <branch> origin/<your-branch>`, with a new branch name unique to that child, work only there, push that branch (never the default branch), then remove the worktree. Fetch the branch here and review it before merging.
- If the remote box lacks a tool the job needs, install it there; it's my box. If it's unreachable or the child fails to start, run it here and tell me.
- Until T3 tracks resumed remote subagents properly: before acting on a "finished" notice from a remote subagent, read its thread to confirm it really stopped with a result.

On the remote box itself, run subagents locally, except Mac-only work, which goes to a Mac named under "Me and my machines".

## Git

Commit with the git identity under "Me and my machines". Check for a repo-local identity override before the first commit in a repo.

## Dev servers

I'm usually on another machine. Bind dev servers to `0.0.0.0` and give me the tailnet URL, `http://<this-host>.<tailnet>.ts.net:<port>`, with the tailnet named under "Me and my machines". Next.js also needs that host in `allowedDevOrigins`, or pages render but never hydrate.

## Scheduled follow-ups

Schedule a follow-up only when you're waiting on something outside this turn. Keep one monitor per job. Cancel it the moment it's obsolete, and tell me.

## Computer use

Before each batch of actions, confirm the window or tab by its title and URL. Leave unrelated windows and tabs alone.

## Shell

`until ! pgrep -f "<pattern>"` never exits, because the loop's own command line matches the pattern. Wait on a marker in the output file instead.
