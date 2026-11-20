---
skill: triage
---

# Open lessons - triage

Read this before working: lessons from single runs that are not in `skill.md` yet. A lesson that a second run
confirms, or that the owner states as a rule, is promoted into `skill.md` (or the document it names) and
removed here. Every run's full feedback, newest first: `feedback-log.md` (history, not required reading).
Tool wishes are not listed here: `docs/backlog.md`.

- **Display corruption:** (a) watch writes to `$FF40-$FF4B` over one frame (raster splits show other maps on
  some lines); (b) VRAM watches do not see DMA: poll-diff VRAM or watch `$FF51-$FF55`; there are two DMA paths
  (`0:1443` queue, `0:1553` immediate) (maze strip, 2026-11-12).
