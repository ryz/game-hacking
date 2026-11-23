# Phantasie - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/phantasie.zip` (disk 1 = PHANT1A boot disk, disk 2 = PHANT1B dungeon disk), model `c64` (PAL).
  Power-on to start menu 4900 frames (`MENU`), Pelnor after "1" another ~3800. The game is a BASIC program
  (PC in A000-BFFF): its state is in BASIC variables (decode the variable table at 2D/2F, see RAM map).
- **Checkpoints that matter:** `@pelnor_party`, `@pelnor_gold` (1536 gold carried), `@outdoors_pelnor`
  (wilderness on Pelnor's square), `@enc_bantir` (first random encounter, party options), `@bantir_set`
  (options set), `@s_won` / `@s_pelnor_back` / `@s_saved` (start set: after the fight, back in town, saved),
  `@w_inn` (independent inn), `@w_dungeon_door` (dungeon prompt), `@d1_entry` (inside dungeon 1),
  `@d1_ants` / `@d1_ants_r2` / `@d1_won` (dungeon fight: ants and bees), `@pineville_old`.
- **Warp:** `POS:XX:YY` pokes the wilderness position (X, Y as 5-byte C64 floats, e.g. 14 = `8460000000`;
  table in RAM map), then step with `STEP:dir` to trigger the square. Dungeon door = `POS:8410000000:8420000000`
  then `STEP:n` twice (square 9,8).
- **Keys are dropped unless the game is idle:** in routes put `settle` between every cursor key in menus
  (`down,settle,down,settle`); `down*3` and `up*5,return` lose presses. Macros `IO0`..`IO5` (individual
  option 0-5 for the highlighted member, then next member), `IOSP:n` (spell n), `IOR:r` (thief: thrust at rank r),
  `FIGHT` (party options -> individual options, cursor on the first member), `OPTS`/`OPTS2` (whole party).
- **Wilderness:** `STEP:e` etc. (`e:20,w100`); the first press after a message only clears it, so counts are
  not exact: check the position watch (`x`, `y`). Dungeon: `DSTEP:s` (`w150`), same caveat.
- **Combat:** party options (beg mercy, threaten, greetings, fight, flee) -> FIGHT -> per member option ->
  "go on fighting" (cursor lands there after the last member) -> return. A round takes ~1100-2400 frames;
  options are kept, so the next round is `return,w100,settle,return`.
- **Cheats used for `main`:** `RICH1` (XP 476-511 and bank gold 690-867 per member, 2-byte big-endian in the
  party records) + `set:9ED2=1247:2` (carried gold) before Guild training/spells.
- **Loads:** "Leaving" ~3600 frames (`LEAVE`); town entry from the map ~3600 then shares; dungeon entry:
  `return,w1300` (disk request) `disk:2,w50,return,w3000`; game save ~2100 (`SAVE`).
- **Open:** game over, other towns/sections, dungeon floors beyond the first rooms, scroll reading, spell names.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Phantasie (title picture; menus say "Start in Pelnor") |
| Platform / model used | Commodore 64, PAL `c64` (see `game.json`); the dump says PAL(+NTSC?) |
| Release (region, year) | North America, 1985; Commodore 64 Version 1.4 (boot screen) |
| Developer / publisher | Winston Douglas Wood (design), C64 conversion W. P. Kubalski / LDW Software; published by Strategic Simulations, Inc. |
| Genre | party role-playing game (six characters), top-down wilderness and dungeons, menu combat |
| Players / save system | 1 player; game save in towns onto the boot disk; character backup disk via the dungeon disk (source) |

Dump: GameBase64 release, two D64 images (volume names "BOOT DISK", "DUNGEON DISK"), not cracked; the boot disk
already holds five characters of a previous owner (grunt, robert (dead), hit, scott, borack, all in town 2).

## Boot sequence
Verified (`work/preview/c64/phantasie/routes.png`):
- 0-~500 frames: blue screen (autostart load); ~540: SSI "proudly presents" screen (C64 Version 1.4, Drive
  Technology fast-load credit); ~840: black; ~2880: title picture; ~4770: start menu "1 - Start in Pelnor,
  2 - Continue saved game". No key needed. `TITLE` = `w3000`, `MENU` = `w4900`.
- `1`: black ~2200 frames, grey frame, "Welcome to Pelnor" (~3200), town screen (~3800). Route `@menu,1,w3200,settle,w600,settle`.
- `2`: loads the last saved party into its town (~3900 frames).

## Controls
| Context | Key | Action | Status |
|---|---|---|---|
| All menus | cursor keys (`up` `down` `left` `right`), joystick port 2 | move the highlight; lists wrap | verified (keys); joystick verified for moving outdoors |
| All menus | `return` (also space / fire per manual) | select | return verified; space did not close the character sheet |
| Start menu | `1` / `2` | new game / continue | verified |
| Town | `c` `u` `g` `p` | cast, use items, game save, printout | u, g, p, c verified (prompts shown) |
| Number prompts (bank) | digits, `return` | type the amount | verified (`type:256`) |
| Name entry | letters, `return` | name (shown in capitals) | verified |
| Yes/No | `right` = no, `return` | answer | verified |
| Wilderness | `3`/`n`, `w`, `e`, `s`; cursor keys; joystick | move one square | verified (`e`, `w`, `3`, `s`, right, left, joyright) |
| Wilderness | `return` | command menu: Inspect, Use potion, Health, Cast spell, Move | verified |
| Dungeon | `return` menu (cast, inspect, use, health, look, move); Move then `n` `s` `e` `w` | explore; Look on the first square showed nothing new | verified |
| Combat | cursor `up`/`down` + `return` with `settle` between keys | party options, member list, option list; spell/rank: type the digit then `return` | verified |

Input timing: the default press (hold 8, wait 40) works in menus inside `play.py`; in one route add `settle` or
`w60` after a screen change (the macros do). Outdoors a move takes ~100 frames.

## Game structure
(source: manual + C64 supplement, verified where marked)
- Isle of Gelnor, 11 towns (Pelnor = town 1 in the NW, Pineville = town 2 verified), 16 map sections, dungeons
  on disk 2 (Cemetary file names on disk B). Goal: defeat the Black Knights and the sorcerer Nikademus; 20
  scrolls hold the story.
- Town: Guild (create, add/drop, train levels, learn spells, inspect, rename, purge; max 21 characters on C64),
  Armory (stock depends on what adventurers sold), Bank (per-character accounts, party gold pooled, max 65000),
  Inn (free rest in towns, "distribute" items), Mystic (party score: "novice adventurers" at score 2), gate.
- Wilderness: move square by square; messages describe terrain ("You are on a path, to the east lies a small
  town"); independent inns cost 250 GP; swimming can hurt.
- Encounters: party options Beg mercy, Threaten, Greetings, Fight, Flee; per-member Thrust, Attack, Slash,
  Lunge, Spell, Parry (kept from round to round) (source).
- Experience is only turned into levels by training at a Guild (source).

## Shot plan
Sets published 2026-11-21: `start` (39 shots, power-on to the first save after the first fight, honest) and
`main` (77 shots). Plan lines: `work/plan/phantasie/` (not committed); the set lists are `shots/*/shots.txt`.
- [x] battles (wilderness bantirs, dungeon ants and bees), party options incl. beg/threaten/flee, individual
  options, spell and rank selectors, rewards
- [x] dungeon entry, disk swap, exit prompt, dungeon menu, four room types
- [x] inn (town, independent), guild spells/training/inspect/drop/rename, armory buy, bank deposit
- [ ] game over, scroll reading (use items), other towns and wilderness sections, deeper dungeon, greetings result

## Strategy and walkthrough notes
- Recommended party (manual): 2 spellcasters, 1 healer, 1 thief type, 2 fighters - the party above follows it.
- Gold: each new character has 256 in the bank; withdraw with `WD:256` six times from the bank's withdraw list
  (the cursor advances by itself after each withdrawal).
- Game save puts carried gold back into the bank: withdraw again after loading.
- Pokes that are safe: attributes in the party records (shown at once on Health/Inspect). Use realistic values.

## Naming
ryz, condi, ebo, cubi, deddo, mnz (owner's rule). Name entry: `type:NAME,settle,return` (macro `KEEP:NAME`);
shown in capitals. Case does not matter.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Old saved party in Pineville | `@pineville_old` (`MENU,2,w3900`) | the dump's boot disk | verified (levels unknown) |
| Party gold | `set:9ED2=N:2` | RAM search | verified |
| Attributes / HP / magic | party records, see RAM map | RAM search + poke | verified |
| Debug menus, codes | none found (no TCRF / GameFAQs page for Phantasie C64) | - | - |

### Saves (rom/saves/phantasie/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| `rom/saves/c64/phantasie/01_start.sav` | our party saved in Pelnor (own export, ZIP of the written disks) | - | see `saves/README.md` | loads via Continue: verified |
No downloadable saves found.

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| 9ED2 | 2 LE | party gold carried (0-65000); a winning fight's gold did not add up exactly in this watch (1536 -> 1579 for 6 x 17) | search 0 -> 1536 after withdrawals; watch `gold` |
| 9A25 + n*0xAA | 6 | party member n (0-5): strength, intelligence, dexterity, constitution, charisma, luck | stats search; poke 9A25=10 showed STR 16 in Inspect |
| 9A2E / 9A2F + n*0xAA | 1+1 | magic: shown as [9A2F]/[9A2E] on Health | poke 9A2E=3 -> "5/3" |
| 9A30 / 9A31 + n*0xAA | 1+1 | hit points: shown as [9A31]/[9A30] on Health (which is current: open) | poke 9A30=9 -> "11/9"; slot 2 (9ADA) checked |
| 9AA7 + n*0xAA | 12 | party member name (PETSCII capitals, space-padded), 0x82 after the stats | name search |
| 8A0D + k*0xAA | - | guild roster copy (same layout; grunt = roster #1) | name search |
| 9A32 + n*0xAA | 2 BE | gold in bank of member n | 256 -> 273 after the first town entry; RICH1 shown on Inspect |
| 9A58 + n*0xAA | 2 BE | experience points of member n | 0 -> 71 (0x47); RICH1 483 shown on Inspect |
| 7488 / 7506 | 5 | wilderness X / Y (BASIC float variables X and Y; also CX/CY at 7537/753E, OX/OY at 7545/754C) | variable-table decode; Pelnor 14,15, inn 7,13, dungeon door 9,8 |
| 2D/2E, 2F/30 | 2 | BASIC VARTAB / ARYTAB: the whole game state is BASIC variables (dungeon program has its own layout: X at 744B, CY at 74FA) | scratch script decoding the table |

## Emulation notes
- Loads use the drive in real time (the "Drive Technology" credit is a fast loader for the boot; later loads sit in
  KERNAL serial code, PC ED5A/EEB2). Everything works on this backend: boot, town, wilderness, game save to
  disk 1, export, reload.
- Screens are mostly text-mode with a custom font: `play.py text` reads menus and stats (capitals in the font
  show as lowercase in the text dump; town and wilderness pictures appear as character garbage).
- Water animates outdoors: wilderness frames never settle (fine; preview takes them as they are).
- In the town screen the red "ENTER" marker can lag behind the highlighted building after a save (cosmetic).

## Checkpoints
Scout: `title`, `menu`, `pelnor_new`, `guild_created`, `party`, `pelnor_party`, `pelnor_gold`, `outdoors_pelnor`,
`saved_start`, `pineville_old`. Capture 2026-11-21: `enc_bantir`, `bantir_set`, `s_won`, `s_pelnor_back`,
`s_saved` (start set chain, all honest play), `w_inn`, `w_dungeon_door`, `d1_entry`, `d1_ants`, `d1_ants_r2`,
`d1_won` (main: POS warp to the door, then plain walking; the ants were met after ~100 dungeon steps of a fixed
pattern, route in `checkpoints.txt`).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| C64 manual + supplement (archive.org text) | https://archive.org/details/Phantasie_I_1986_SSI | controls, C64 differences, towns, save, backup, races/classes | 2026-11-21 |
| Rulebook scan (archive.org, mocagh copy) | https://archive.org/details/vgmuseum_ssi_phantasie-manual | same text, cross-check | 2026-11-21 |
| Wikipedia | https://en.wikipedia.org/wiki/Phantasie | release facts, premise | 2026-11-21 |
| mocagh.org refcard, datadrivengamer blog | - | not reachable from the container (host not allowed) | 2026-11-21 |
| GameFAQs / TCRF | - | no Phantasie (C64) pages found | 2026-11-21 |

## Open questions
- ~~Where do encounters happen?~~ Random: the first came after 28 steps east of Pelnor (e,e,e,w,w pattern), the dungeon's after ~100 steps.
- ~~Dungeon entry~~: "A dungeon. Enter?" -> "Insert dungeon disk and press a key" -> `disk:2,w50,return` works (verified). Leaving a dungeon (disk 1 back) not tried.
- Which HP/magic byte is current and which is max.
- Outdoor position: candidates 7506/753E changed with a south step; not confirmed.
- Levels and equipment of the old Pineville party (useful for late-game shots).
