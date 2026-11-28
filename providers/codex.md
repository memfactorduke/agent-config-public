## Codex

Use the `pstack:poteto-mode` skill for every task except computer use, which skips it.

Codex's built-in subagents run only on this machine. Use them just for subagents that must stay here, and start the rest through T3's `delegate_task`.

When a thread ends, save durable lessons to the project's notes, linked from its AGENTS.md. A thread with no new lesson needs no entry.

## Deleting files

Codex holds any `rm` with `-f`, `-rf`, `-fr` or `--force` for my approval, even in Full Access, and the thread stalls until I answer. That covers an `rm` anywhere in the command: inside a longer script, after `sudo` or `env`, or in a `trap` cleanup. Delete with `find` instead, which runs straight through:

- A file or a whole folder: `find <path> -delete`.
- A pattern: `find <dir> -maxdepth 1 -name '<glob>' -delete`.
- A path that may not exist: `[ ! -e <path> ] || find <path> -delete`.

A hook from agent-config rejects a forced `rm` before Codex can hold it. If you see its message, rerun the command with the `find` form.
