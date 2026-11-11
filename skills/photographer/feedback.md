---
skill: photographer
---

# Feedback - photographer

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-11 - jp_tour: reference catalogue of the original Japanese ROM
- Task: pixel-exact catalogue of the JP original (121 power-on shots + 33 state shots), published and committed (5633ea1).
- Worked: gbemu-cli `turbo` (6x faster, byte-identical PNGs); exploring with emu.py --save chains; 2x contact sheets.
- Corrected: none (commit checked: only docs/shots/jp_tour/, 1.1 MB).
- Friction: tools do not enable turbo; shoot.py has no state-based mode; --publish copies every PNG in the work
  folder; index tokens column cut at 120 chars; curated maze_menu/stairs_prompt show the wrong screens.
- Proposed rule change: (1) emu.open_emu enables turbo; (2) maze controls in skill.md (A/up forward, B camp,
  SELECT dungeon menu; battle messages wait for A); (3) shoot.py --state lists; (4) replace curated
  maze_menu/stairs_prompt with maze_dmenu/stairs_up_prompt.
- Status: open (tool changes pending; maze controls already promoted in the playtester skill)

_No runs yet._
