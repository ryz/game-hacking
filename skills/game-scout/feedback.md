---
skill: game-scout
---

# Open lessons - game-scout

Read this before working: lessons from single runs that are not in `skill.md` yet. A lesson that a second run
confirms, or that the owner states as a rule, is promoted into `skill.md` (or the document it names) and
removed here. Every run's full feedback, newest first: `feedback-log.md` (history, not required reading).
Tool wishes are not listed here: `docs/backlog.md`.

- **First-person games with position bytes:** map a level with a depth-first walker (poke, step, read the
  position back) before exploring by hand (Dungeon Master, 2026-11-20).
- **Chains that depend on a random world state** (wind, moons, a moving whirlpool): poke it to a fixed value
  in the macro and look at each checkpoint's frame (`tools/cachecheck.py` sheet) before building on it
  (Ultima III, 2026-11-19).
- **After `export`, load the save** with `sav:NAME` through the game's own Continue before reporting it
  (Phantasy Star, 2026-11-19: the first export held no cartridge RAM).
- **Record tables:** count the names shown against the items poked; nameless entries are skipped in lists
  (Wizardry III DOS, 2026-11-19).
- **Compressed text:** point an existing message square at each message number and read the screen before
  decoding the format (Wizardry III DOS, 2026-11-19).
- **Placed monsters or objects:** use a slot the game's lookups reach (index 0 can be skipped) and check with
  one attack (Ultima II, 2026-11-19).
- **Name keyboards:** check whether shift/case persists from one name to the next (Wizardry I NES, 2026-11-18).
- **Facts in a dispatch are "to be checked":** verify the stated start (year, place, working files) on screen
  before naming checkpoints after it (Ultima II, 2026-11-19).
- **Doors that ignore walking into them:** test "step onto the tile, release, press again" in one preview batch
  before trying Open/Seek or other doors (Sword of Vermilion, 2026-11-20, ~40 calls). An exit that does nothing
  before a story event: retry it after the event before searching elsewhere (same game, the south gate).
- **Dungeon games: load every level through the game's own level-change code** (a script around it) before
  writing warps; it doubles as the dump check (Bard's Tale III Apple II, 2026-11-21).
