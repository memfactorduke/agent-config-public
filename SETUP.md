# Set up agent-config on this machine

You are an agent setting up agent-config for your user on the machine you're running on. Work through the steps in order. Each step ends on its **done when** line; meet it before moving on. Discover facts from the machine before asking the user; ask only for what no command can tell you, and batch those questions into one message.

Every step checks before it acts, so re-running this on a machine that's already set up just brings it up to date.

`$AC` below means `~/.agent-config`.

## 1. Prerequisites

Check for `git` and `python3` (3.9 or newer). Install what's missing: Homebrew on macOS, the system package manager on Linux.

**Done when** `git --version` and `python3 --version` both succeed, and Python is 3.9+.

## 2. Clone and name the machine

- If `$AC/repo` is a git checkout, run `git -C $AC/repo pull --ff-only`. Otherwise run `git clone https://github.com/memfactorduke/agent-config-public.git $AC/repo`.
- If `$AC/machine` exists, keep its name. Otherwise pick a short lowercase name for this computer (e.g. `laptop`, `studio`, `vps`) from its hostname or its Tailscale name, and write it to `$AC/machine`. Each of the user's machines needs a different name.

**Done when** `$AC/repo/bin/agent-config` exists and `$AC/machine` holds a single name.

## 3. Collect the user's facts

Fill in every row. Use the command first, and ask the user only when the command can't answer.

| Fact | Where to find it |
| --- | --- |
| Git identity | `gh api user --jq '"\(.login) <\(.id)+\(.login)@users.noreply.github.com>"'` when `gh` is signed in; otherwise `git config --global user.name` / `user.email`. If the two disagree, ask which to use. |
| Tailnet | `tailscale status --json` (on macOS the CLI may be `/Applications/Tailscale.app/Contents/MacOS/Tailscale`): `MagicDNSSuffix` is the tailnet; `Self.DNSName` gives this machine's host. No Tailscale means the tailnet is "none". |
| Remote box | An always-on Linux machine (VPS or server) that takes subagents. In T3 Code, call `t3_environment_links`: the linked Linux environment is the candidate, and its `environmentId` is the ID you need. Then call `t3_project_list` with that `environmentId`: the project for a scratch or misc folder gives the scratch `projectId`, and the parent folder of its repo projects is the projects folder. If several machines qualify, ask which one. With no T3 Code and no remote box, the remote box is "none". |
| Mac for Mac-only work | Among the linked environments, the Mac the remote box should hand logged-in-browser, simulator and Xcode work to. "None" if there isn't one. |

**Done when** every row has a value or an explicit "none".

## 4. Write the personal layer

`$AC/local/personal.md` describes the user, and must be identical on all of their machines.

1. If it already exists, keep it and update only rows from step 3 that have changed.
2. Otherwise, check whether another of the user's machines already has one. For each online Tailscale peer (`tailscale status`), run `ssh -o BatchMode=yes -o ConnectTimeout=5 <peer> cat .agent-config/local/personal.md`. If one answers, copy that file verbatim.
3. Otherwise, start from `$AC/repo/examples/local/personal.md`, fill in step 3's facts, and delete the HTML comments. For a remote box of "none", write `- Remote box: none.` in place of the remote-box line.

**Done when** the file contains no example values or placeholders (`yourname`, `XXXX`, `my-vps`, `<from …>`) and no HTML comments.

## 5. Move the user's existing instructions over

The first sync replaces these files: `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.grok/AGENTS.md`, `~/.config/opencode/AGENTS.md` and `~/.pi/agent/AGENTS.md`. It backs them up first, but anything the user wrote there stops applying. Skip any file whose first line starts with `> Built daily from` (agent-config already built it) and any file that doesn't exist. Read the rest in full, along with `$AC/repo/core.md` and `$AC/repo/providers/`. For each instruction in them:

- **Already covered** by core or a provider file: drop it.
- **About the user**, true on every machine (preferences, identity, accounts): add it to `personal.md`.
- **About this machine only** (paths, drives, local tools, services): add it to `$AC/local/machines/<machine>.md`. Start that file from `$AC/repo/examples/local/machines/laptop.md` with this machine's real host and notes, or `## This machine: <Name>` alone if there's nothing else to say.
- **Contradicts** core or a provider file: keep the user's version in `personal.md` under `## Overrides`, phrased as an override ("Ignore the shared rule on X: do Y."), and list it in your final report.

**Done when** every instruction in the old files is dropped as covered, moved, or kept as an override, and you can name its fate.

## 6. Preview

Run `python3 $AC/repo/bin/agent-config render <machine> /tmp/agent-config-preview` and read the Claude file it prints.

**Done when** its first line lists `personal` and the machine name among its layers, and the "Me and my machines" section and this machine's section both read correctly.

## 7. Sync

Run `python3 $AC/repo/bin/agent-config sync`. It installs plugins with the `claude` and `codex` CLIs when they're present, adds MCP servers, and copies the skills into `~/.claude/skills` and `~/.agents/skills`. Skills it doesn't manage are left alone. Leave out `--cleanup`, which removes them.

**Done when** the sync exits 0, its output has no `ERROR:` or `FAILED` lines (or you've fixed each one and re-run), and `head -1 ~/.claude/CLAUDE.md` names this machine.

## 8. Run it daily

- **macOS**: if `launchctl list | grep local.agent-config` prints nothing, copy `$AC/repo/service/agent-config.plist` to `~/Library/LaunchAgents/local.agent-config.plist` and `launchctl load` it.
- **Linux**: if `systemctl --user is-enabled agent-config.timer` doesn't print `enabled`, copy `$AC/repo/service/agent-config.service` and `agent-config.timer` into `~/.config/systemd/user/`, then run `systemctl --user daemon-reload && systemctl --user enable --now agent-config.timer` and `loginctl enable-linger "$USER"`.

**Done when** the job shows in `launchctl list`, or the timer shows in `systemctl --user list-timers`.

## 9. Report

Tell the user:

- the machine name, and the facts you used for each row of step 3;
- what moved from their old instruction files, and where each override went;
- where the old files were backed up (`$AC/backups/<timestamp>/`);
- anything left for them, and why it needs them (e.g. Tailscale or T3 Code isn't installed, a CLI needs signing in, a plugin failed).

Finish with: to set up another machine, give its agent the same prompt; it will copy `personal.md` from this machine over Tailscale if SSH is on.
