---
skill: playtester
---

# Feedback - playtester

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-12 - rev1d (5ab9d44): new bank-49 messages on screen
- Task: bring the census messages on screen (422B, 4314, 44CE, 451F, 4583, 43B9, 4432, 5594/55A4).
- Worked: JP party states via party.py --rom for a JP twin of every screen; explore copy with stop
  breakpoints that poke flags at the exact code point; gbdis on each message's caller to find its trigger.
- Friction: shared build/ had uncommitted edits (built own copy - correct); no SRAM poke / breakpoint-hook
  helper; stop=True halts inside run_frames; party.py prints relative paths; hidden-BG text can't be judged.
- Proposed rule change: RAM shortcuts (spell bits +$31, mage points +$3C, priest +$43; $CB99 bit 3 text map;
  Find allies roster +$58 and SRAM $AEE2 table; $C001 bits 2/3 surprise); check git status of build/.
  Tools: tools/poke.py (WRAM+SRAM), breakpoint hooks in explore.py.
- Corrected: Add-whom leftover row (46 spaces), teleport prompt values at the JP columns, find-allies list in
  the VWF (20:62C6), battle Equip slot names right-aligned + prompt tail cleared; 5594 one line. The garbled
  top box on old states = signature bump re-init (native state clean). Not fixed: 地下 map label (graphics).
- Status: promoted 2026-11-12 (RAM shortcut lines added to skill.md); poke/hook tools -> backlog

### 2026-11-12 - rev1c (85d10bc): chests, events, recruit, temple fee
- Task: chest screens/traps/loot, bank-45 events, NPC recruit with a free slot, temple resurrection payment.
- Worked: the ready chest/event states; a WRAM diff across chest states found the trap byte ($C635) so
  every trap message could be forced; maze_goto.py also works on the JP ROM for comparisons.
- Friction: Dead needs the SRAM roster too (cart_ram 0x001+$80n, mirror +$1000) and Rescue lists only
  deposited members; emu.py names shots by token index; jp_tour explore states are not where their names say.
- Proposed rule change: 'RAM for shortcuts' note (party copy + SRAM roster offsets, temple Deposit then
  Rescue); a census check that every message in a bank-49 run of $FF-terminated messages is in the script.
- Corrected: temple fee verified OK (5000 -> 4900). Fixed: down-stairs prompt 49:422B was missing from the
  script (untranslated on the main path); {FA} look-ahead counted 8 px per character (early wraps) - now
  3/4 cell per character (Stub_WrapCmp). Open: magic-circle party list in 8 px with '-' for '/', resurrection
  'ebo    went to the tavern.' gap, spell grid ' /'.
- Status: promoted 2026-11-12 (RAM shortcut note added to skill.md); bank-49 run census -> tool backlog

### 2026-11-12 - rev1b (6500974): chests, friendly encounter, events
- Task: reach chests, a friendly encounter, bank-45 events and floor 2 on the current build.
- Worked: explore.py with several seeds in parallel; 999 HP poke; an auto-fight loop with a $C1BF check found
  a crash on its own; RAM watch + trace_start found its cause in minutes.
- Friction: chests/events not reachable by random walking on floor 1; no native EN chest/event states; JP
  states are useless in the EN build; state + token replays are not always deterministic; key presses after
  a battle open Camp and derail loops.
- Proposed rule change: ask the coordinator for native EN checkpoints (or poke the position $CB80-$CB82)
  for chests/events; a build check that unidentified group names are <= 12 characters.
- Corrected: crash fixed (Gaseous form / Gaunt figure / Armored one; tests/test_limits.py), 'Aim for
  damage' -> 'Power hit' (fits the box), panel names that fit 80 px stay on line 1. #2 (Fight submenu
  garble) not reproduced on the new build in 6 timings; #3 unconfirmed (replay artifact suspected).
- Status: promoted 2026-11-12 (name-length check is now a test); native chest/event states -> coordinator todo

### 2026-11-12 - Rev 1 round trip (8052a1f)
- Task: standard round trip on the first Rev 1 build; regressions from the port.
- Worked: building the pre-port commit with the v1.0 dump in SESSION/old and replaying suspicious screens
  separated port regressions from old bugs; poke.py and a run.sh wrapper.
- Friction: explore.py looped on 'Ouch!' (closing key does not turn); seeds did not vary the walk; relative
  --state paths fail in emu.py; archived tools/ lack gbemu-cli; party.state cursor not at Edge of Town.
- Proposed rule change: symlink gbemu-cli and use absolute --state paths; build the previous commit with its
  base ROM for regression checks after a port; explore.py turns twice after 'Ouch!'.
- Corrected: #1/#2 battle panel and Fight submenu garble: GC read SCX mid-frame under the battle's raster
  split and freed the panel's slots - fixed (columns 0-20 always count when SCX != 0). #3 quit screen and #6
  'divided' already fixed. explore.py rewritten (stairs No, double turn after 'Ouch!', VWF bank not a hit);
  battle reached in 73 steps. Battle group names with a line break ('Robed/figure') now spaced. Open: #4
  tavern list after the sheet submenus, #5 level-up ' gained a level!' line, #7 range dashes.
- Status: promoted 2026-11-12 (regression via previous commit + base ROM; absolute --state paths) - skill.md

### 2026-11-11 - pt2: full session on 3f26beb (report only, owner compares with own playtest)
- Task: full first-session playtest of the owner's ROM, report only.
- Worked: building the target commit from git archive into the session dir; frame-by-frame capture to tell
  transient from persistent glitches; RAM pokes (Fighter record $C8D1, gold $C8D9, EXP $C8DD, HP $C8E4) to
  reach a level-up, same poke on JP for comparison.
- Corrected: none yet (owner comparing).
- Friction: build/ was rebuilt mid-session by the coordinator (states broke, ~15 min); explore walker stops on
  any bank change and cannot aim for the stairs; fast inputs are swallowed outside battle too; dead status in
  RAM unknown.
- Proposed rule change: build the dispatched commit into SESSION/src and always pass --rom; document the
  Fighter record addresses for level-up tests.
- Status: promoted 2026-11-11 (build-your-own-ROM rule + record addresses; coordinator caused the friction)

### 2026-11-11 - pt1: first session (town, shop, inn, temple, training, maze, 3 battles, stairs)
- Task: first full playtest from power-on.
- Worked: same route on the Japanese ROM separated bugs from original behaviour; RAM search turned "gold looks
  wrong" into a confirmed bug (buying added gold: RAM data copies were stubbed as text, fixed 8fe8999).
- Corrected: "Status lists spell names as untranslated" is right; battle message order issue not reproduced
  after the bank-49 fix (verbs now read from bank 49).
- Friction: skill said A opens the dungeon menu (it is SELECT); stairs route missing; explore.py stops at
  message boxes; battle inputs need ~30 frames; skill asked for report.md though the harness forbids it.
- Proposed rule change: correct maze controls, compare with JP before reporting, check RAM for wrong values.
- Status: promoted 2026-11-11 (factual control fix + both rules; explore.py change open)

