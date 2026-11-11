---
name: proof
description: Attach proof to finished work so the user can check it at a glance on a phone instead of opening apps. Use when handing back any finished task, or when a subagent reports done.
---

# Proof

"Done" arrives with **proof**: evidence the user can glance at in about 20 seconds, on a phone, that shows the real thing working. A claim, a diff or "tests should pass" is not proof.

## 1. Capture

Pick the recipe that matches the work, and capture after your last change. If you changed it again afterwards, capture again.

| Work | Proof |
|---|---|
| Web page or app UI | Screenshots of the changed screen at phone width (~390 px) and desktop width, in the state the change affects. Use a short screen recording when the change is motion or a multi-step flow. |
| HTML report or chart | Render it inline (`html_preview`, then `html_render` in T3 Code), plus the saved file's path. |
| iOS app | A simulator screenshot (`xcrun simctl io booted screenshot <file>`), or one from the device when the change is device-only. |
| Video or audio | A contact sheet (one frame every few seconds, tiled), duration, and integrated loudness against the target, e.g. `ffmpeg -i <in> -af ebur128=peak=true -f null -`. |
| Images or a candidate set | One contact sheet or gallery of every image, each labelled with its ID. |
| Backend, API or service | The passing test summary line, plus one live request against the running service with its status and the key part of the response. |
| Background job, timer or install | The scheduler's own state (`launchctl print`, `systemctl --user status`) plus the job's latest log line or output from a real run. |
| Script or automation | A real run, or a dry run when the real one would send, delete or spend, with the tail of its output. |
| Config or infrastructure | The check that proves the effect (the port answers, the file is served, the setting reads back), not the config diff alone. |
| Docs or prose | The rendered document, or its path and the paragraph that changed. |

Rules for every recipe:

- **Real**: capture the real system. If it has to be a sandbox or mock data, label the proof that way.
- **Specific**: the shot shows the thing that changed, not a generic home screen.
- **Saved**: write proof files to a `proof/` folder in your scratch space, never into the repo unless asked. Machine rules about where files go still apply.

Completion criterion: every distinct change in the hand-back has at least one proof item, and each item names what it proves.

## 2. Attach

- In the final reply, put the proof right after the summary: embed images with markdown image syntax and their absolute paths, give recordings and pages as absolute paths, and put command output in a short code block, trimmed to the lines that matter.
- One line per item: what it shows, then the proof itself.
- A subagent includes its proof paths and output in its final message, so the parent can check them and pass them on.
- When something can't be proven (it needs the user's login, a device you can't reach, or a future event), say exactly what's unproven and why, in the list of what's left.
- When the work is in a PR, put the same proof under `## Proof` in its description. Upload images only to repos that are private.
