# Digital Devil Monogatari: Megami Tensei II (Famicom, English translation patch) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
**ROM text** = read from the patched ROM's English script (decoder in Emulation notes; dump
`work/scout/megami-tensei-2/text_dump.txt`, rebuilt by `work/scout/megami-tensei-2/textdump.py`), not yet seen in play.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Digital Devil Story: Megami Tensei II / デジタル・デビル物語 女神転生II (Dejitaru Debiru Monogatari: Megami Tensei II); the title screen keeps the Japanese logo (verified) |
| Platform / model used | Famicom, NTSC (`game.json`); mapper 19 (Namco 163), 256 KiB PRG + 256 KiB CHR, 8 KiB battery RAM |
| Release (region, year) | Japan, 6 April 1990 (Wikipedia); never released outside Japan; English fan translation applied (owner-supplied IPS, headered layout, see `game.json` "source") |
| Developer / publisher | Atlus / Namco (Wikipedia; title screen "namcot (c) 1987 1990 NAMCO LTD.", verified) |
| Genre | RPG: overhead maps plus first-person 3D view, turn-based battles, demon negotiation and fusion |
| Players / save system | 1 player; **battery save** with slots ("WANT TO SAVE? / CHOOSE A SLOT. / RECORDED.", ROM text); a computer menu "BOOT GAME / LEAVE / SAVE DATA" (ROM text). No save was reachable inside the opening Devil Buster game (see Saves) |

## Boot sequence
- Intake probe `work/intake/megami-tensei-2/sheet.png`: a blue logo slides in (~f120-240), Tokyo skyline with a
  falling missile (~f480-600), a demon's face over the skyline (~f660-720), nuclear blast with "199X- MANKIND...
  IS OVER....." (~f780-1020), static (~f1080-1260), title from ~f1320 (logo), START from ~f1560 (verified).
- `TITLE` = `w1600,settle` (verified). Checkpoint `title`. Start during the intro (`pow,w300,start`) jumps to the
  title (verified), but a second Start right after was ignored; the macro keeps the full intro (deterministic).
- `NEWGAME` (verified, checkpoint `start`): `start,w700,a,w700,a,w400` (two "Caution for Devil Busters" text pages;
  they type for ~550 frames each and **a press while a page types is lost**, so fixed waits), then three name
  entries `NAME_RYZ`, `NAME_CONDI`, `NAME_EBO` (w300 between), stat allocation `STATS_RYZ`, `STATS_CONDI`, `w600`.
  Play starts in the overhead maze of **Devil Buster**, the game-within-the-game.
- Name entry: hero ("Your character is the young hero. Name him."), girlfriend ("Name your girlfriend."), best
  friend ("Give a name for your best friend."): RYZ, CONDI, EBO (owner's naming rule; the grid has upper case only).
- Stats: each hero has 5 in VIT INT STR SPEED LUK and 15 points; A adds a point to the stat under the cursor, Down
  moves; with 0 left a CONFIRM Yes/No box appears (cursor on Yes). RYZ: VIT 9 INT 6 STR 10 SPEED 7 LUK 8 (HP 8);
  CONDI: VIT 7 INT 10 STR 6 SPEED 8 LUK 9 (HP 6, MP 11). Only RYZ and CONDI fight; EBO is the friend in the story.

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Start | START (only entry with an empty battery; whether a CONTINUE entry appears after saving is untested) | verified |
| Text pages | A | next page (lost while the page is still typing) | verified |
| Name entry | D-pad | cursor over the grid (kana blocks, `"°!-`, A-Z, FWD, BWK, OK) | verified |
| | A | write the character / OK confirms | verified |
| | B | (probably delete; untested) | - |
| Stat allocation | A / Down | +1 point / next stat; CONFIRM Yes with A | verified |
| Overhead map | D-pad | walk one 16-px tile per ~16 frames held (`right:16`); the camera follows | verified |
| | A | field command screen: moon phase, WEALTH (Makka, MAG), 3D view of the corridor, CMD COMP / MAGIC / ITEM / STATS, party HIT-PTS / MP / STATUS | verified |
| | B | close the command screen | verified |
| | Start / Select | nothing seen | verified (no effect seen) |
| CMD > STATS | A | "See info on who?" RYZ / CONDI -> status page (LV, HP, MP, EXP, NEXT, MAG, Makka, DEMONS, STATE, GEAR slots, stat bars); any button returns | verified |
| Stairs tile | walk onto it | next floor (moon phase changed full -> half on the way) | verified |
| Battle | menu | FIGHT / FLEE / CHAT / AUTO ("CHOICE?") | verified |
| | FIGHT | RYZ: RUSH / COMP / ITEM / GUARD; CONDI: RUSH / MAGIC / ITEM / GUARD; then "IS THIS CORRECT?" YES / NO | verified |
| | CHAT | "RYZ CONVERSES.." -> the demon answers (one test: "WILLOWISP CALLS A WILLOWISP.") | verified |
| | FLEE, AUTO, COMP, MAGIC, ITEM | not tried | - |

Input timing: the default press (hold 8, wait 40) works in name entry, stats, menus and battle menus. Exceptions:
presses during typing text are lost (use fixed waits), and the first battle press after a round needs the round to
finish (`w400` after the YES). A battle round with two RUSH and the enemy's action takes ~400 frames.
Round macro idea: `a,w60,a,w60,a,w60,a,w400` = FIGHT, RYZ RUSH, CONDI RUSH, YES.

## Game structure
- Opening (verified + ROM text): the heroes play **Devil Buster** on a computer; it is played as the real game
  (overhead maze, battles vs demons, stairs between floors). After it, **Pazuzu** (sealed in the machine "by Tokyo's
  ruler, Bael") calls the two messiahs, gives the hero a Demon Summoning Program ("this includes demons from Devil
  Buster") and an auto-mapping program, gives the girlfriend magic, and sends them to kill **Nebro** ("He is in
  B8"); they head for the **armory** (ROM text).
- The real world: post-apocalyptic Tokyo (20XX, 35 years after a nuclear war, people in shelters, Wikipedia).
  Places named in the ROM: the **shelter** ("SHELTER ACCESS GATE / RELEASE AIRLOCK", "ENTER SHELTER"), **Tokyo
  Tower** (a witch who heals and is called a threat), **Shinjuku**, **Ueno**, the **Daedalus Tower**, Shibuya.
- An internal list of 50 story points in the ROM (identical in the unpatched Japanese ROM: original romanised
  text, not the translation), in likely story order: Elder in Micon, Minotauros, Statue of Evil, Computer Room,
  Armory, Girlfriend, Ferry by Moura, Orutoros, Partner, Man in Sibuya, Reseption for Balam, Balam, Hatikou, Naga,
  Mr. Saigou, Nihiru Blade, Dr. Bakuta, Aporion, Mouth of Devil, Cybarne Laboratory, Reonalds Sabbath, Manmon,
  Pazusu, Kerberos, Nitohog, Ordeal Nisiarai, Buritora, Inspection, Zaratan Island, Friend Dead, Baeru, Ground
  Zero, Masakado, Underground Lake, Asumodeus, Belial, Despair Bridge, Moloch, Belphegor, Izanami, Sword Knight,
  Astarte, Mitora, Beruzebubu, Lusifers Shrine, Lusifer, Asherah, Satan, The Y.H.V.H (ROM text, file offset
  0x16FB3, pointer table just before it, PRG bank 11 at $C000). Looks like a debug scenario/warp list; how to
  open it is unknown (Open questions).
- Systems (Wikipedia + verified menus): demons joined by negotiation (CHAT) and summoned from the COMP; fusion at
  a special place; moon phases (8, shown as FULL MOON / HALF MOON / 3/8 MOON, verified); alignment through
  choices decides the ending; EXP, Makka (money), MAG (magnetite) from battles (verified: Willowisp gave 4 EXP,
  20 Makka, 8 MAG).

## Shot plan
Routed lines are in `shots.txt` (15 shots, frames checked by the scout). Must-haves from the capture guide:
- [ ] `title_screen` - title; `intro_skyline`, `intro_face`, `intro_blast` - cutscene (attract intro)
- [ ] `caution` - cutscene - Devil Buster's opening text
- [ ] `naming_hero`, `naming_ryz`, `stats_alloc` - menu
- [ ] `start_room` - gameplay - first control in the Devil Buster maze
- [ ] `hud_cmd` - hud - field command screen
- [ ] `stats_ryz` - inventory - status page
- [ ] `battle_menu`, `battle_action`, `battle_chat`, `battle_victory` - battle
- [ ] `pazuzu` - cutscene/dialogue - Pazuzu after Devil Buster (needs Devil Buster finished)
- [ ] `shelter` - gameplay - the shelter (real world, first town)
- [ ] `save_slots` - save - the computer's SAVE DATA / "Choose a slot" screen
- [ ] `tokyo_overworld` - map/gameplay - ruined Tokyo overhead
- [ ] `dungeon_3d` - gameplay - first-person view in a dungeon (if dungeons switch to full 3D)
- [ ] `automap` - map - the auto-mapping program
- [ ] `comp_summon`, `demon_joined` - system - a demon recruited by CHAT and summoned
- [ ] `fusion` - system - fusing two demons
- [ ] `shop`, `heal` - shop/system
- [ ] `levelup` - battle; `boss_nebro` - boss (B8); `tokyo_tower_witch` - dialogue
- [ ] `gameover` - gameover
How to reach: everything up to `battle_victory` is a checkpoint here. The rest needs Devil Buster finished
(play: floors via stairs, HP frozen, enemies' HP poked to 1), then the shelter (save there, export `01_start`).

## Strategy and walkthrough notes
- Devil Buster: the party is level 1 with 8/6 HP. Freeze HP for every fight: `freeze:053C=08,freeze:053D=06`
  (re-applied between tokens only: wait with `w10*N` in battles). Kill fast with `poke:0548=01` (first enemy's HP)
  before the round, or FLEE.
- Encounters are random and follow frame timing (route of `battle_willowisp`: walking left/right in the top
  corridor of the 2nd floor).
- The first floor's room has a stairs tile (the walk to it is part of the route of `battle_willowisp`, the
  `down:16,w30` that changes x/y to 6F/0C) and a blue orb tile in an enclosure (not tried).
- The goal of Devil Buster is not known yet (ROM: Pazuzu speaks after it); find the way down/the exit floor by floor
  and checkpoint every floor.

## Naming
Hero **RYZ**, girlfriend **CONDI**, best friend **EBO** (owner's rule; upper case is all the grid offers).
Grid: 5 rows x 20 columns: kana (cols 0-9), `" ° ! -` (cols 10-14 of row 0), `UVWXY` (row 0 cols 15-19), `ABCDE`
row 1 cols 10-14, `Z` row 1 col 15, `FGHIJ` row 2, `KLMNO` row 3, `PQRST` row 4 (cols 10-14); FWD / BWK / OK at
col 15 of rows 2/3/4. Cursor starts on ア (0,0) for every name. Macros `NAME_RYZ`, `NAME_CONDI`, `NAME_EBO`.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Survive fights | `freeze:053C=08,freeze:053D=06` (RYZ / CONDI HP, low bytes; values for level 1) | RAM (here) | poke verified (HP shown 5/8 after `poke:053C=05`); freeze untested in a long fight |
| Win a fight | `poke:0548=01` (first enemy's HP) then one RUSH round | RAM (here) | verified (checkpoint `won_willowisp`) |
| Money / MAG | `set:0404=2471:3` (Makka), `set:0407=1386:2` (MAG) | RAM (here) | verified on the command screen and the status page |
| Debug scenario list | 50 story points listed at ROM 0x16FB3 (see Game structure) | ROM text | how to open it unknown |
| Saves from the web, codes | none found: TCRF, the manual PDF host (yojimbo.eludevisibility.org) are not reachable from here | - | - |

### Saves (rom/saves/megami-tensei-2/, never committed)
None downloaded. No in-game save before the shelter: the battery RAM at `start` holds no slot, so no `01_start`
export was made (the first export belongs after Devil Buster, at the computer's SAVE DATA).

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| 0431 / 0432 | 1+1 | position x / y on the overhead map (tile units; x grows right, y grows down); 0440/0441 move with them (another frame of reference) | RAM diff while walking; watches `x`, `y` |
| 0437 | 1 | facing on the overhead map (0 up, 2 left/right, 3 down) | RAM diff (inferred) |
| 0404 | 3 | Makka (money), little-endian | `find "new == 20"` after a victory; poke shown |
| 0407 | 2 | MAG (magnetite) | RAM after the victory (8); poke shown |
| 0410 / 0418 / 0420 | 8 each | names RYZ / CONDI / EBO (A = 0x11 encoding) | peek |
| 0500 + 2s + p | 1 | stats, interleaved per hero p (0 RYZ, 1 CONDI): s = 0 VIT, 1 INT, 2 STR, 3 SPEED, 4 LUK | peek (09 07 06 0A 0A 06 07 08 08 09) |
| 050C / 050D | 1+1 | level RYZ / CONDI | peek (01 01) |
| 053C + n | 1 | HP (low byte) of battle slot n: 0 RYZ, 1 CONDI, 12 (0548) first enemy; max HP at 0578 + n (enemy 0584); high bytes probably 0554 + n / 0590 + n | poke verified on screen |
| 0564 + n | 1 | MP of slot n (0565 CONDI); max MP 05A0 + n | poke verified (MP 9) |

## Emulation notes
- NTSC, defaults fine. Mapper 19 (Namco 163) runs in Mesen without trouble; the patched text renders cleanly
  (no sign of a mis-applied patch in intro, caution pages, naming, menus or battle text).
- Typewriter text: a press while a page types is lost and `settle` stops on the typing pauses, so a `checkpoint`
  after `a,w60,settle` can be one page behind what you think: use fixed waits (`w700` per caution page).
- The overhead camera follows the hero with black outside the map edge; after a stairs tile the new floor draws
  in place (no fade).
- Script decoders: main script A-Z = 0x80-0x99, space 00, line break F0, page FE, end FF, `.` 9D, `'` 9F, `,` B7,
  with dictionary codes (0x40-0x7F, A0-BF) inside many lines (names like Lucifer are compressed); intro / naming /
  internal lists: A-Z = 0x11-0x2A, space 00, `.` 2C, digits 01-0A. Relative search: `relsearch.py WORD`.

## Checkpoints
All in `checkpoints.txt`; built from an empty cache and compared with a cache hit: identical frames
(2026-11-18) for `title`, `naming`, `start`, `battle_willowisp`, `won_willowisp`. `battle_willowisp` has a long
route (menu tests and walking on two floors) because the encounter depends on its exact frame timing: do not tidy it.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Digital_Devil_Story:_Megami_Tensei_II | release, developer, story outline, systems (negotiation, fusion, moon phases, alignment) | 2026-11-18 |
| Patched ROM text | `rom/megami-tensei-2.nes`, decoded | save prompts, Pazuzu, Nebro, places, story-point list | 2026-11-18 |
| TCRF, manual PDF (yojimbo.eludevisibility.org), almarsguides walkthrough | https://www.tcrf.net/Digital_Devil_Story:_Megami_Tensei_II , https://yojimbo.eludevisibility.org/Stardust_Crusaders_Files/complete/NES/mt2files/Digital%20Devil%20Story%20Megami%20Tensei%202%20Manual.pdf , https://almarsguides.com/retro/walkthroughs/nes/Games/DigitalDevilStoryMegamiTenseiII/ | hosts not resolvable from this session (outside the allowed network); for the owner / an allowed session | 2026-11-18 |

## Open questions
- How Devil Buster ends (which floor, a boss?) and where the first save point is (the home computer?).
- Does the title get a CONTINUE entry once a slot is saved? Load route for `sav:` saves.
- The 50-entry story-point list: a debug menu? Which code reads the pointer table (PRG bank 11, $CF00 area)?
- Name entry: which button deletes (B? BWK); what FWD/BWK do (move the write cursor?).
- HP high bytes and the demon/COMP records; EXP address (RYZ had 4 EXP after the first win).
- The blue orb tile in the first room of Devil Buster.
