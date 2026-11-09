## Claude Code

The native `Agent` tool runs only Claude models, and only on this machine. Use it just for subagents that must stay here, with `effort: "high"`. Spawn everything else, including every Sol subagent, through T3's `delegate_task`.
