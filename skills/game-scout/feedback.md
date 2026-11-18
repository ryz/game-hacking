---
skill: game-scout
---

# Feedback - game-scout

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-18 - Dungeon Magic (NES)
- Task: scout Dungeon Magic: playbook, macros, title/start/field/castle checkpoints, RAM and map-data location,
  inn save export, shot plan.
- Worked: disassembling the joypad handler found the pause-then-icon command scheme in 3 calls after ~8 blind
  tries; RAM dump before/after a step found position and the map at $0600, matched against the ROM to locate the
  stored maps; wall-consistency scan + PNG renderer for an atlas; parallel poke-warps next to doors found the inn
  and shops in one call; the step-and-tile helper.
- Friction: no shared 6502 disassembler or RAM dump/diff; web sources mostly blocked (search snippets and ROM text
  instead); ~10 calls on the pause scheme before going to the code; scout cannot run `shoot.py --verify`.
- Proposed rule change: skill step 3: joypad read before guessing controls; shared `tools/dis6502.py` and `play.py
  dump/diff`; emulator guide: dump the RAM floor block and search the ROM for stored maps.
- Corrected: coordinator verified 12/12 from an empty cache; `tools/dis6502.py` made shared (second occurrence)
  with a test, game copy removed and playbook updated; joypad and map-block hints in `docs/emulator/README.md`.
- Status: promoted 2026-11-18 (disassembler, hints); open (`play.py dump/diff`, scout running shoot.py)

### 2026-11-18 - Megami Tensei II (Famicom, English IPS)
- Task: scout Megami Tensei II: playbook, macros, title/start and later checkpoints, RAM, save handling, shot plan.
- Worked: step-and-tile helper (`work/scout/megami-tensei-2/steps.py`); `emu.py` sheets to time typing text;
  ROM script decoding by relative search (two encodings): save prompts, places, an original story-point list;
  RAM block dumps for HP/MP/stats; `find "new == 20"` after a victory found money; empty-cache vs cache-hit check.
- Friction: `settle` stopped on a typewriter pause, a checkpoint was a page behind (~8 calls); `peek` length is
  decimal; TCRF and the manual host outside the network; `01_start` export impossible before Devil Buster ends.
- Proposed rule change: typewriter note on checking before checkpoint; hex `peek` length or document it; shared
  `play.py steps`; skill step 4: export at the first save point when none exists at start.
- Corrected: coordinator verified 15/15 routed shots from an empty cache. Typewriter/checkpoint and peek notes in
  `docs/emulator/README.md`; step-and-tile helper (second occurrence, see Shin Megami Tensei) and ROM-script
  decoding (second occurrence, see Megami Tensei) promoted into skill.md step 3; export exception in step 4.
  Shared `play.py steps` not built. Network hosts are the owner's environment decision.
- Status: promoted 2026-11-18 (helper, ROM script, export exception); open (`play.py steps`)

### 2026-11-17 - Megami Tensei (Famicom, English BPS patch)
- Task: scout Digital Devil Story: Megami Tensei (Famicom, English patch): playbook, macros, title/start and
  later checkpoints, RAM, password handling, shot plan.
- Worked: one-shot `emu.py` runs with a contact sheet per token to learn menus; decoding the patched ROM's script
  by relative search ("password") replaced the blocked web sources (sage in Micom gives passwords, floor/town/boss
  names); dump-and-diff RAM over four turns found the facing byte; empty-cache rebuild vs cache hit for every
  checkpoint.
- Friction: `play.py find` gave 0 candidates right after `find reset` although `055C` counts steps; `play.py
  checkpoint` writes straight into checkpoints.txt (a scratch checkpoint removed by hand); GameFAQs,
  StrategyWiki, TCRF, gamehacking.org 403, archive.org download host refused; the status window does not redraw
  after a poke, so HP pokes looked as if they failed.
- Proposed rule change: skill.md step 2: when web sources are blocked and the game is a translation, decode the
  ROM script (relative search for a known word) and tag those facts "ROM text"; tools: check `play.py find` on
  NES; `play.py checkpoint --scratch`; proxy: allow archive.org download hosts.
- Corrected: coordinator re-took the 9 routed shots and verified 9/9 from an empty cache. Proxy hosts are the
  owner's environment decision (not changed).
- Status: open (ROM-script decoding: first occurrence; `--scratch` not done). `find` on NES fixed 2026-11-17
  (reset took no snapshot).

### 2026-11-17 - Shin Megami Tensei (Super Famicom, English patches; first SNES game)
- Task: scout Shin Megami Tensei (Super Famicom, English patch), the first SNES game: playbook, macros,
  title/start checkpoints, RAM map, save, shot plan.
- Worked: a small step-and-tile helper (several token groups, one tiled image) cut the look-at-every-frame cost;
  fixed `a,w150` per text page made the naming route replayable; `find "new == 10000"` right after the allowance
  found the money address in one call; rebuilding every checkpoint with an empty cache and comparing with a
  cache hit.
- Friction: about 30 minutes on the opening (presses during typing text counted unreliably, two macro attempts
  typed wrong names); macros could not be repeated with `*N`; 8-frame Up/Down skips rows in this game; SNES
  emulation about half the NES speed and the opening is 20,000 frames; TCRF, GameFAQs and StrategyWiki 403 and
  the only code list is on a host that is not allowed (no walkthrough, debug or save source); the write list
  excludes `work/shots/`, so planned routes could not go through `shoot.py`.
- Proposed rule change: emulator guide: typewriter text needs one press per page with a fixed wait; support
  `MACRO*N` or document that it is not supported; skill.md step 3: test Up/Down with a 4-frame hold if a default
  press skips a row; let the scout run `shoot.py` into `work/scout/<slug>/`.
- Corrected: `MACRO*N` added to `tools/emu.py` (test); typewriter-text and short-hold notes added to
  `docs/emulator/README.md`. No late-game checkpoint: flags and position not found (left to the capture run).
- Status: promoted 2026-11-17 (empty-cache check and `games/<slug>/tools/` in the write list: second
  occurrence, see the Dragon Quest entry); open (scout running `shoot.py`)

### 2026-11-17 - Dragon Quest (Famicom, English patch; first NES game)
- Task: scout Dragon Quest (Famicom, English patch), the first NES game: playbook, macros, title/start/late
  checkpoints, password handling, RAM map, shot plan.
- Worked: making a late-game "save" by poking the state and asking the king for a password; an inverse IPS as a
  `rom:jp` variant to compare the kana and translated password grids; position poke plus one step as a warp;
  rebuilding every checkpoint with an empty cache and comparing against cache hits, which exposed a frame bug.
- Friction: cache hit versus build differed by one frame on NES (`lrcore.Core.image()` ran a frame when none was
  drawn); `status` PC is useless for this game (always the frame-wait loop); TCRF and StrategyWiki 403; the
  skill's write list has no `tools/` folder although pokemon-blue has one; reading a password off a screenshot
  is error-prone (icons are symbols).
- Proposed rule change: fix `lrcore.Core.image()` so a screenshot never advances emulation, with a test; in
  skill.md step 3 add "rebuild the checkpoints once with an empty cache and compare with a cache hit"; allow
  `games/<slug>/tools/` in the guardrails; for password games "make passwords by poking the state and asking
  the game for one".
- Corrected: backend fixed the same day (screenshots never emulate; savestates carry the frame; test
  `test_nes_state_keeps_frame_and_timing`); all nine checkpoints rebuilt and checked by the coordinator.
  Password-by-poke and the PC note went into `gamedb/docs/emulator.md`.
- Status: open (skill.md changes: empty-cache check, `tools/` in the write list; first occurrence)

### 2026-11-15 - Pokémon Blue (first game through the pipeline)
- Task: scout Pokémon Blue: playbook, macros, title/start/late checkpoints, RAM recipes (late game, warp),
  saves for the owner.
- Worked: pret/pokered disassembly via curl to raw.githubusercontent.com + base stats read from the ROM ->
  generator script for realistic party pokes, right first time; warping by rewriting a door's warp entry;
  in-game save + `play.py export --state`, checked with `sav:` + CONTINUE.
- Friction: `undo` one level only (an over-long mash typed into the naming keyboard); settle accepts all-white
  fade frames; RAM watches could not show BCD money; `--model sgb` hangs on SGB transfer garbage; snap routes
  using a macro break silently when the macro changes later; WebFetch fails, TCRF/GameFAQs 403.
- Proposed rule change: docs/emulator.md: never mash into a name prompt; settle should refuse/warn on blank
  frames; a bcd type for RAM watches.
- Corrected: coordinator replayed @late without cache, the party screen, both exported saves via
  `sav:NAME,TITLE,CONTINUE` (trainer card ryz / 48215 / 27:47 / 8 badges; bedroom for 01): all as reported.
  Added `"fmt": "bcd"` watches (money watch for pokemon-blue) and the mash and blank-frame rules to
  docs/emulator.md. Settle itself left unchanged (recorded routes depend on it). SGB hang and macro-change
  breakage go to docs/status.md Next.
- Status: promoted 2026-11-15 (mash rule, blank-frame note, bcd watch); sgb and macro versioning open
