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
Capture run 2026-11-18: 36 shots in `main` (`shots.txt`, published to `shots/main/`). Ticked = captured (other id in
brackets). Must-haves from the capture guide:
- [x] `title_screen` - title; `intro_skyline`, `intro_face`, `intro_blast` - cutscene (attract intro)
- [x] `caution` - cutscene - Devil Buster's opening text
- [x] `naming_hero`, `naming_ryz`, `stats_alloc` - menu
- [x] `start_room` - gameplay - first control in the Devil Buster maze
- [x] `hud_cmd` (+ `cmd_overworld`) - hud - field command screen
- [x] `stats_ryz` - inventory - status page
- [x] `battle_menu`, `battle_action`, `battle_chat`, `battle_victory` - battle
- [x] `pazuzu` (+ `pazuzu_born`, `pazuzu_war`, `pazuzu_rift`, `pazuzu_messiahs`, `pazuzu_program`, `pazuzu_armory`, `statue_reaction`) - cutscene - round 2
- [x] `shelter` (+ `shelter_soldier`, `shelter_gate_guard`) - gameplay - the shelter (real world, first town)
- [x] `save_slots` (+ `computer_menu`, `computer_room`) - save - the computer's SAVE DATA / "Choose a slot" screen
- [x] `tokyo_overworld` - map/gameplay - ruined Tokyo overhead
- [x] `dungeon_3d` - gameplay - first-person view in a dungeon (if dungeons switch to full 3D)
- [ ] `automap` - map - the auto-mapping program
- [x] `comp_stock`, `comp_summoned`, `battle_demons`, `battle_demon_cmd`, `battle_demon_hit` (round 2, demons poked into the COMP); [ ] a demon joining by CHAT (never seen)
- [x] `fusion_menu`, `fusion_whom`, `fusion_pair`, `fusion_result`, `fusion_ritual` - system (round 2, Devil Buster's fusion master)
- [x] `shop`, `shop_armor`, `shop_bought` (round 2), `heal`, `save_totem`, `save_recorded`, `teleport_list`, `registry`, `village`
- [x] `levelup` - battle (+ `battle_magic`, `battle_dia`, `battle_item`, `battle_overworld`, `battle_chat_golem`); [x] `boss_taurus` (+ `taurus_appears`, `taurus_victory`, `got_sorb`, `god_statue`); [ ] `boss_nebro` - boss (B1 per Pazuzu, not B8); `tokyo_tower_witch` - dialogue
- [x] `gameover` - gameover
Extra: `error_screen` (leftover debug screen). Not captured: `pazuzu`, `automap`, `fusion`, `shop`, `boss_nebro`,
`tokyo_tower_witch`, a joined/summoned demon (see Strategy, capture run).
How to reach (scout): everything up to `battle_victory` is a checkpoint here. The rest needs Devil Buster finished
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

### Capture run 2026-11-18: what worked
- **The real world without finishing Devil Buster:** lose every hero inside Devil Buster (any battle; HP freezes do
  not hold inside one token, a ST GOLEM x3 fight with `down*2,a,w10*25` killed the party). GAME OVER ("THE WORLD WILL
  PERISH!") is followed by the computer room (EBO: "...QUIT THE GAME AND SPOKE."), then the computer menu BOOT GAME /
  LEAVE / SAVE DATA (checkpoints `computer_room`, `computer_menu`). SAVE DATA > DATA1 saves (export `01_computer_room`);
  LEAVE puts RYZ + EBO into the shelter B4 (checkpoint `shelter_b4`). Macca and MAG drop to 0. Whether the Pazuzu scene
  (COMP summoning, auto-mapping, CONDI's magic) still comes later on this path is not known.
- **No random encounters:** `freeze:037A=FF` (TCRF cheat list via web search; verified in Devil Buster, the overworld
  and caves). TCRF also lists `04C5=FF` (alternative), `040C=01` (overworld wall walk), `DB04=FF` / `C091=FF` (wall walk),
  and a controller-2 B debug toggle (no controller 2 here).
- **Warps on overhead maps:** a position poke alone does not move collision. Poke `0431/0432` **8 frames into a stairs
  transition** (step onto stairs, `w8`, poke, `w120`): the new map is drawn and walkable (frames 4-30 work). The area
  byte `0436` decides which map and events apply at a position: the grey temple at 5B,7F is the healer's temple with
  `0436=05`, and with `0436=04` its door (5B,7E) leads out to the Tokyo overworld at 11,2B (checkpoints `db_last`,
  `overworld`).
- **Event scan in first-person mazes:** poke `042F/0430` (and the copies `0433/0434`) to the square before the target
  facing S, then `up:16,w24,w200`: the event of the target square fires. A 16x16 contact sheet of all squares finds
  NPCs and stairs in one run (script idea from Megami Tensei I; shelter B4 events: soldier 04,05; DANGER-gate guards
  05,07 0A,07 05,0F 0A,0F; stairs 00,02 0F,07 0F,0F). The floor below the B4 stairs (00,02) showed the same event
  squares, so events seem to be per area, not per floor (`0436=01` in the shelter).
- **Overhead explorer:** a breadth-first search over savestates (press each direction, keep new squares, log jumps as
  stairs) mapped Devil Buster floor 8 and the overworld near 11,2B (the cave holes at 0E,2F and 1C,2B are cave
  entrances). Moves are only reliable with `settle` between direction changes (`right:16,w24` per step).
- Negotiation: answers change with the frame of the CHAT press (`wN` before it); 60 variations against a Willowisp
  gave only "calls a Willowisp" / "THEY WILL NOT TALK!". ST GOLEMs asked YES/NO questions in untranslated text.
- Dead ends: decoding how Devil Buster ends (floor-8 exit stairs inside a wall; the area-2 event table is empty) took
  ~60 tool calls without an answer; the warp-table rom variant (`bytes` patch of the floor-1 stairs target) reproduced
  the poke result exactly and was removed again.

### Capture run 2 (2026-11-18, round 2): what worked
- **Devil Buster is finished by its own event squares, not by stairs.** The overhead event table (ROM file 0x7DAB-0x7F40,
  3-byte entries `x y id`, one list for all overhead maps) holds Devil Buster's events: 5E,08 fusion master (id 8F),
  59,0C healer (8E), 53,0E Micon's elder (15: "QUIT THIS GAME"), 53,11 treasure (16), 58,11 weapon/armour shop (04),
  52,2C the fallen **god statue** (25), 76,23 **Taurus** (24: "HEY BRATS! DIE!" then the boss battle), 5D,2C hint "OFFER
  THE S.ORB TO THE FALLEN GOD STATUE" (20), 72,14 "TAURUS HOLDS THE S.ORB" (1E), jammed elevators (23, eight squares),
  NPC hints (17-1F, 21), 6B,5C / 72,52 a trap back to the start 51,08 (7D), floor-8 squares 6A,67 (97), 76,6A (98,
  Cerberus, untranslated), 6A,6A (37, a door). Story: kill Taurus (`poke:0548=01` before the round) -> "GOT S.ORB" ->
  offer it at the god statue -> Pazuzu's speech -> computer room (Demon Summoning Program, auto-mapping program, EBO
  gets magic) -> shelter B4 (checkpoints `boss_taurus`, `taurus_won`, `taurus_done`, `statue_offer`, `pazuzu_tale`,
  `real_world`). The floor-8 stairs in the wall are not needed.
- **Event warps:** macro `DBEV:x:y` from `@db_f1_back` (Devil Buster) and `TOWNEV:x:y` from `@overworld_demons` (towns)
  poke 0431/0432 to the square **below** the event 8 frames into a transition, then step up. Inside Devil Buster a plain
  `poke:0431=..,poke:0432=..` + step also fires an event once the map is loaded (used for the god statue).
- **Demons by poke:** the COMP stock is party slots 2-11 of the battle-slot arrays (stride 0x14): flag `0516+i` = 80
  (bit 7 = owned, bits 5-6 clear = in the COMP), HP `053E+i`, max HP `057A+i`, demon id `05B6+i` (code bank 19 $A103).
  Macro `DEMONS3` = PIXIE (8D) 17/19, GOBLIN (8B) 21/24, KOBOL (96) 25/25. CALL lists them with the Macca cost
  (PIXIE 47, GOBLIN 175, KOBOL 79); summoning costs Macca (untranslated "not enough Macca" line when short), then
  every step costs MAG. Ids near these: ST GOLEM 53, STONK AD, MEZU 9B, MEPHI 99, JINN 9C, CHORON 97.
- **Fusion** works inside Devil Buster at the fusion master (5E,08) with poked demons: FUSE TWO -> chart -> PIXIE + KOBOL
  = CARBUNK (BRT, LV 4, ZIO). Menu input there needs held presses (`down:12,w60,a:12`).
- **Encounters on demand:** 037A is a step countdown (FF frozen = none); `poke:037A=01` (macro `ENCOUNTER`) and one step
  starts a battle.
- **Towns:** the settlement north of 11,2B (inside 5B,7E, area 05) has a shop (armour, Jamaican-patois clerk), a save
  **totem** (house 59,7F: LEAVE / SAVE / Teleport; SAVE -> DATA1/DATA2 -> "RECORDED."), houses. A scan of the town
  event table found: registry man "REGISTER / LISTEN" (55,C3 id 4B), "NEED HELP?" (51,C7 4C), slots (55,C7 4D), Mr. Nandi
  gambling (59,C7 4E), Dream Drugstore (59,BF 4F), bar (55,BF 28), gun shop "FOR WHOM?" (59,6F 08), weapon shop (2B,BF 5A),
  totems (46, 47, 49, 4A). Sheets: `work/capture/mt2/scan1/`, Devil Buster `work/capture/mt2/dbs_dn/`.
- **Dead ends:** the story-point list at bank 11 $CF3F has no caller; $CF07 maps a value to an index by thresholds
  (not a scenario jump). Flags 0480-049F are battle data, not story flags. No auto-map button found (Select, Start, B
  in the shelter do nothing). CHAT with golems ends with them leaving; no join seen.
- **Who is who:** after Pazuzu the second messiah is called EBO and the real-world party is RYZ + EBO (the hero named
  second, CONDI, is the Devil Buster partner on screen). The name prompts' order may not match the roles assumed in
  round 1; check before naming captions.

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

### Saves
Exported: `games/megami-tensei-2/saves/01_computer_room.sav` (slot DATA1, RYZ/CONDI LV 2 at the home computer after
the Devil Buster game over; see `saves/README.md`). None downloaded (rom/saves/megami-tensei-2/ is empty). No in-game save before the shelter: the battery RAM at `start` holds no slot, so no `01_start`
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
| 037A | 1 | encounter control: `FF` held = no random battles | TCRF cheat (web search); verified |
| 042F / 0430 | 1+1 | position in a first-person maze (x, y; S = y+1); copies at 0433/0434; on the overworld the world position | RAM diff; poke + step fires the target square's event (verified) |
| 037A | 1 | step countdown to the next random battle (FF held = none; 01 + one step = a battle) | round 2 |
| 0516+i, 053E+i, 057A+i, 05B6+i | 1 each | COMP stock / party slots 2-11: flag (80 = owned, in COMP), HP, max HP, demon id (PIXIE 8D, GOBLIN 8B, KOBOL 96, ST GOLEM 53, STONK AD) | round 2 (COMP CALL code bank 19 $A103) |
| 7E0B-ish table | - | overhead event squares: ROM file 0x7DAB-0x7F40, 3-byte `x y event` (Devil Buster from 0x7DAB, towns after) | round 2 |
| 0436 | 1 | area: 03 Devil Buster floor 1, 02 other Devil Buster floors, 04 overworld, 05 building interiors, 01 shelter | peek after warps; set from the warp's target byte through a table at $D82F |
| 0438 | 1 | area number of the last warp (byte 4 of a warp entry) | code at $DD08 |
| 04AA / 04AB | 1+1 | event/script id set by a warp or an event square | code at $DAE4/$DD1E |
| 0440 / 0441 | 1+1 | overhead camera top-left (player - 8, - 7) | peek |
| 040C | 1 | map mode nibble shown on the ERROR screen; TCRF: `01` = overworld wall walk | code at $EC14 |

ROM (file offsets without the 16-byte header): warp tables are 7-byte entries `x y tx|80 ty area ev1 ev2` in PRG bank
3 (e.g. Devil Buster from 0x744D: 57,0C -> 6F,0C ...; real-world doors from ~0x7407); the event-square table per area
is at bank 3 $ABAE (4-byte entries `x y id-lo id-hi`); warp search code at $DC97, ERROR printer at $EB5A.

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
Capture run 2026-11-18 added: `db_f1_back` (floor 1 again, LV 2, 120 Macca) -> `db_last` (warp poke to 5B,7F) ->
`overworld` (11,2B) -> `dungeon_1f` (cave) / `battle_golem` -> `golem_r2` -> `computer_room` (game over) ->
`computer_menu` -> `saved_data1` (DATA1 saved) ; `computer_menu` -> `shelter_b4` (LEAVE) -> `shelter_stairs1`.
All routes are deterministic; every shot built on them passed `--verify`.
Round 2 added: `demons_party` -> `village` -> `village_out` -> `totem` ; `overworld_demons` -> `battle_demons` ;
`db_f1_back` -> `boss_taurus` -> `taurus_won` -> `taurus_done` -> `statue_offer` -> `pazuzu_tale` -> `real_world`.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Digital_Devil_Story:_Megami_Tensei_II | release, developer, story outline, systems (negotiation, fusion, moon phases, alignment) | 2026-11-18 |
| Patched ROM text | `rom/megami-tensei-2.nes`, decoded | save prompts, Pazuzu, Nebro, places, story-point list | 2026-11-18 |
| TCRF, manual PDF (yojimbo.eludevisibility.org), almarsguides walkthrough | https://www.tcrf.net/Digital_Devil_Story:_Megami_Tensei_II , https://yojimbo.eludevisibility.org/Stardust_Crusaders_Files/complete/NES/mt2files/Digital%20Devil%20Story%20Megami%20Tensei%202%20Manual.pdf , https://almarsguides.com/retro/walkthroughs/nes/Games/DigitalDevilStoryMegamiTenseiII/ | hosts not resolvable from this session (outside the allowed network); for the owner / an allowed session | 2026-11-18 |

## Open questions
- (round 2) The auto-mapping program: how to open it (not Select/Start/B in the shelter). Nebro (B1), the Tokyo Tower
  witch and the moon-phase effects were not reached. How to make a demon join by CHAT. Town names (labels untranslated).
- (round 2) A save after the Pazuzu scene: the shelter route has no save point checked yet (home computer?).
- (capture run) How Devil Buster is meant to end and how the Pazuzu scene is triggered; whether it still happens after
  quitting Devil Buster by a game over. Next idea: from `shelter_b4`, play the shelter (gates, other floors) and watch
  for Pazuzu at the computer (BOOT GAME); or find the script that prints "BORN FROM FIRE AND STORM" (bank 12, file
  0x183E8) and the event id that starts it, then poke `04AA/04AB`.
- (capture run) Where demons join (no join in ~80 CHAT tries) and where the first shop is.
- How Devil Buster ends (which floor, a boss?) and where the first save point is (the home computer?).
- Does the title get a CONTINUE entry once a slot is saved? Load route for `sav:` saves.
- The 50-entry story-point list: a debug menu? Which code reads the pointer table (PRG bank 11, $CF00 area)?
- Name entry: which button deletes (B? BWK); what FWD/BWK do (move the write cursor?).
- HP high bytes and the demon/COMP records; EXP address (RYZ had 4 EXP after the first win).
- The blue orb tile in the first room of Devil Buster.
