---
skill: photographer
---

# Feedback - photographer

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-12 - three-way set compare3 (JP | EN | REF)
- Task: shoot.py three-way mode and the compare3 set (35 shots), published.
- Worked: route cache + turbo (3 ROMs x 35 shots in ~3 min); testing the patched tool via __file__ without touching
  tools/; old-vs-new byte comparison of the two-way mode; native contact sheets for the same-screen check.
- Friction: the dispatch asked for a tools/ edit and a docs/ publish, outside the photographer's write scope; the
  dispatch said 40 shots (35); no contact-sheet tool.
- Proposed rule change: tool changes staged as `work/shots/<set>/_tool/` (diff + full file) for the coordinator;
  a same-screen check with per-shot content differences in the set README when comparing patches.
- Corrected: coordinator reviewed the diff, applied it and published docs/shots/compare3/.
- Status: promoted 2026-11-12 (staged tool changes; same-screen check)

### 2026-11-12 - rev1_tour: the jp_tour routes on Rev 1 + EN
- Task: reshoot the 121 v1.0 reference routes on Rev 1 and the EN build, compare each with v1.0.
- Worked: list generated from index.json (full tokens); pixel diff old vs new found the 5 changed routes at once;
  a wait sweep found `w24` restoring the old bonus roll; boot/PARTY cache: full 2-ROM run ~9 min.
- Friction: `shoot.py --only` rewrites the index with only those ids (a fix needs a full rerun); `build/` was
  rebuilt by other sessions during the run (caught by the index SHA-1s); no step for comparing with an older set.
- Proposed rule change: --only merges into the index; replacing-a-set steps (diff vs old, RNG wN fix, single
  rom_sha1 check).
- Corrected: set committed as docs/shots/rev1_tour/; its 'classsir' observation reproduced (two owners of slot
  $40) and sent to triage. shoot.py --only now merges (coordinator).
- Status: promoted 2026-11-12 (Replacing a set section)

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

