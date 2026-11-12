---
skill: photographer
---

# Feedback - photographer

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-12 - ref_tour: the reference English patch (8 px) on Rev 1
- Task: 164 shots of the reference fan translation (all jp_tour routes + museum monster room + battle/chest
  from states), catalogue and contact sheets in work/shots/ref_tour/; not published.
- Worked: jp_tour list ran unchanged on Rev 1; turbo wrapper (30 s -> 2 s per shot); mash-A state chain for
  a whole battle/chest sequence; poke token for the museum flags.
- Friction: no turbo in the tools; explore.py stuck at the entrance stairs prompt (bank 32); battle messages
  auto-advance (settle wait skips them); no poke/state lines in shoot.py; no contact-sheet tool.
- Proposed rule change: battle messages = state + no settle wait (skill); turbo in emu.open_emu; @STATE lines,
  poke and `!` in shoot.py; explore.py answers No at stairs; replace maze_menu/stairs_prompt.
- Corrected: turbo verified (same frame hash, 23.8 s -> 3.6 s) and made the emu.open_emu default; poke token
  added to shoot.py; shots.txt: maze_dmenu/stairs_up_prompt replace the two wrong lines, 9 museum lines added.
  The "rects.json modified" note was the coordinator's own edit in progress.
- Status: promoted 2026-11-12 (turbo and maze_menu/stairs_prompt: second entry; battle-message capture rule
  added to skill.md); @STATE lines, `!`, stairs-No and contact sheets stay in the tool backlog

### 2026-11-11 - jp_tour: reference catalogue of the original Japanese ROM
- Task: pixel-exact catalogue of the JP original (121 power-on shots + 33 state shots), published and committed (5633ea1).
- Worked: gbemu-cli `turbo` (6x faster, byte-identical PNGs); exploring with emu.py --save chains; 2x contact sheets.
- Corrected: none (commit checked: only docs/shots/jp_tour/, 1.1 MB).
- Friction: tools do not enable turbo; shoot.py has no state-based mode; --publish copies every PNG in the work
  folder; index tokens column cut at 120 chars; curated maze_menu/stairs_prompt show the wrong screens.
- Proposed rule change: (1) emu.open_emu enables turbo; (2) maze controls in skill.md (A/up forward, B camp,
  SELECT dungeon menu; battle messages wait for A); (3) shoot.py --state lists; (4) replace curated
  maze_menu/stairs_prompt with maze_dmenu/stairs_up_prompt.
- Status: superseded 2026-11-12 by the ref_tour entry (turbo, (4) done). Was: logged 2026-11-11 (tool changes (1) (3) (4) moved to the tool backlog in docs/status.md Next; maze
  controls promoted in the playtester skill)

