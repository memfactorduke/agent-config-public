## Claude Code

The native `Agent` tool runs only Claude models, and only on this machine. Use it just for subagents that must stay here, with `effort: "high"`. Spawn everything else, including every Sol subagent, through T3's `delegate_task`.

## Commands that pause Full Access

Claude Code's delete-safety check stops a Bash command for my approval, even in Full Access, whenever it can't prove where an `rm` lands. These shapes pass it:

- Create and change files with Write and Edit. For a one-off script, Write it to a file and run that file. A heredoc whose body holds backticks or `${…}` can stop the run even with no `rm` in it; commit messages with backticks go through `git commit -F <file>`.
- Guard every variable in a delete: `rm -rf "${DIR:?}"/*.png`.
- Delete by absolute path: `rm /abs/dir/*.png` or `find /abs/dir -name '*.png' -delete`, never `cd dir && rm *.png`.
- Keep your scratch work in subfolders such as `<drive>/scratch/<job>/`, so your cleanup never removes a folder sitting directly under `/Volumes/<drive>/`. When I ask you to delete one, do it; I'll answer the prompt.
- Run `rm` as its own command, outside `sh -c '…'` and `bash -c '…'`.
- When the check refuses a command, use the rewrite it suggests.
