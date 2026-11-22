---
skill: game-capture
---

# Open lessons - game-capture

Read this before working: lessons from single runs that are not in `skill.md` yet. A lesson that a second run
confirms, or that the owner states as a rule, is promoted into `skill.md` (or the document it names) and
removed here. Every run's full feedback, newest first: `feedback-log.md` (history, not required reading).
Tool wishes are not listed here: `docs/backlog.md`.

- **Party games: do not poke the facing byte.** Move by position pokes plus the game's own turns; a poked
  facing left the champions' formation unrotated and no blow landed (Dungeon Master, 2026-11-20, ~15 calls).
- **Clean warps and forced battles:** find the game's main state byte and write its "enter map" / "start
  battle" values instead of poking position alone (Phantasy Star, 2026-11-19).
- **Fixed encounters may be set up only on floor entry:** warp onto stairs, an elevator or a chute, not next
  to the room (Wizardry I NES, 2026-11-18).
- **Special squares:** one route per open side, taken from the decoded walls (Wizardry I DOS, 2026-11-19).
- **Item powers can hide behind Equip as well as Use:** read the item records before calling a quest item
  inert (Wizardry III DOS, 2026-11-19).
- **Scrolling command logs:** write the caption from the frame, not from the keys sent (Ultima II, 2026-11-19).
- **Check the must-have list** (title, menu, first control, HUD, game over: `docs/capture-guide.md`) before
  the first full verify, not after (Ultima II, 2026-11-19).
- **First-person RPGs: survey first.** A per-game script that steps onto every event square and reads the
  encounter from memory gives the monster groups and messages of all areas in one run (Might and Magic 1 DOS
  round 2, 2026-11-18; a shared version is in `docs/backlog.md`).
- **Shots added during a run:** `shoot.py SLUG SET --verify --only id,id` checks just those (Shin Megami
  Tensei run 2, 2026-11-17).
- **Scripts that play routes** use `emu.start(game, route)` and `emu.play(emu, game, rest)`; a hand-made token
  list needs `emu.expand(game, emu.split(...))` for macros (Dungeon Master, 2026-11-20). Prefer
  `tools/preview.py` to a script of your own.
- **Townspeople to talk to:** find the NPC object table (position, line pointer) and the collision grid early and
  plan a Talk route per person; trying waits against wandering people fails (Sword of Vermilion, 2026-11-20).
- **Menu-driven warps (Aries-style lists):** check the destination by its RAM index, not by the keys sent
  (Sword of Vermilion, 2026-11-20: three checkpoints reached the wrong towns).
- **Restyles that must not change routes** (palette, font, display option): copy the published PNGs before the
  retake and compare each retake with its old picture through a colour map (Beyond Zork palette 6, 2026-11-21).
- **Walks without random fights:** search a fight-free wait per step (check a fight indicator after each step)
  instead of previewing whole routes (Bard's Tale III Apple II, 2026-11-21: `tools/safewalk.py`).
- **A first-person view that stays black after entering** may be darkness, not a load hang: click once or
  light a torch/spell before waiting longer (Dragonflight, 2026-11-22).
