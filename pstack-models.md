# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Task `model`). Alias entries in a panel list still count toward its fan-out.
# Managed by agent-config: Sol for every role, Opus added to the multi-model panels, always high effort.
# budget: medium (high)
feature, refactoring: gpt-6.1-sol high
bug-fix: gpt-6.1-sol high
perf-issue: gpt-6.1-sol high
hillclimb: gpt-6.1-sol high
judgment and prose: gpt-6.1-sol high
hardest tasks: gpt-6.1-sol high
how explorer: gpt-6.1-sol high
how explainer: gpt-6.1-sol high
why investigators: gpt-6.1-sol high
why synthesizer: gpt-6.1-sol high
reflect tooling: gpt-6.1-sol high
reflect judgment, divergent, synthesizer: gpt-6.1-sol high
arena runners: gpt-6.1-sol high, opus high
arena cross-judge pool: opus high, gpt-6.1-sol high
swarm workers: gpt-6.1-sol high
architect runners: gpt-6.1-sol high, opus high
interrogate reviewers: gpt-6.1-sol high, opus high
