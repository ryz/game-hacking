# Phantasie - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/phantasie.zip` (disk 1 = PHANT1A boot disk, disk 2 = PHANT1B dungeon disk), model `c64` (PAL).
  Power-on to start menu takes 4900 frames (`MENU`), Pelnor after "1" another ~3800. Begin from a checkpoint:
  `@pelnor_party` (party of six in town), `@pelnor_gold` (same, 1536 gold carried), `@outdoors_pelnor`
  (wilderness, standing on Pelnor's square, move compass active), `@saved_start` (after the first save).
- **Party:** ryz human fighter, condi dwarf fighter, ebo human priest, cubi elf wizard, deddo halfling thief, mnz
  human monk (guild #6-11). Made by macros `GUILDNEW`, `ROLL:race:class:1`, `REROLL`, `KEEP:name`, `MORE`
  (route of `guild_created`). Attribute rolls do NOT depend on timing: only the number of rolls so far changes
  them, so a different roll = one more `REROLL,ROLL:...`.
- **Menus:** cursor keys move the highlight, `return` selects (space did not leave the character sheet).
  Town: buildings in a 3x2 grid (top: Guild, Armory, Bank; bottom: Inn, gate = exit, Mystic), cursor wraps;
  letters `c` cast, `u` use items, `g` game save, `p` printout. Number prompts: type the digits (`type:256`).
- **Wilderness:** direction keys `3`/`n` north, `w`, `e`, `s` (also cursor keys / joystick). Use `STEP:e` etc.
  (`e:20,w100`): with shorter waits a press during the step animation is lost, and the first press after a
  message only clears the message. `return` opens the command menu (Inspect, Use potion, Health, Cast spell,
  Move). Stepping on a town square asks "A town. Enter? yes/no": answer `right,return` (no) or `return` (yes).
- **Loads are slow (real 1541, KERNAL loader):** "Leaving Pelnor" waits for `return`, then ~3600 frames to the
  map (macro `LEAVE`); game save ~2100 frames (`SAVE`, from the town screen). Do not `settle` through a load:
  the screens are black or static for long stretches; use the waits in the macros.
- **Shortcut:** `@pineville_old` = "Continue saved game" on the untouched dump: the previous owner's saved party
  (grunt fighter, hit thief, scott priest, borack wizard) in Pineville, town 2. Levels not checked yet.
- **Saves:** game save divides all carried gold back into the bank (shares 0-3 per member) and writes to the boot
  disk (disk 1). "Continue saved game" loads the last saved party straight into its town (no guild number asked,
  unlike the Apple manual). Export `01_start` (rom/saves, not committed) tested through Continue: verified.
- **Open:** no random encounter met in ~80 steps around Pelnor (combat screens not seen); dungeon entry and the
  disk swap (`disk:2`) not tried; outdoor position bytes not found; HP byte order (current/max) unclear.

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
| Dungeon | `l` | look at a larger area | source (manual) |

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
31 lines in `shots.txt`, all previewed (`work/preview/c64/phantasie/plan.png`): boot 1, title 1, menu 8,
gameplay 5 (2 env), system 2, inventory 2, shop 3, save 2, dialogue 2, hud 1, extra 1. Still to add by playing:
- [ ] `battle_encounter` "An encounter" + party/monster pictures; `battle_party_options`; `battle_member_options`;
      `battle_spell`; `battle_result` (XP/gold) - walk the wilderness farther from Pelnor until an encounter.
- [ ] `dungeon_enter` prompt, `dungeon_disk` (swap request, `disk:2`), `env_dungeon_*` corridors, `dungeon_look`.
- [ ] `inn_rest`, `guild_spells` (wizard cubi), `guild_train_level` after a fight, `armory_buy`, `scroll_read`.
- [ ] other towns, an independent inn, `gameover` (party dead), `map` of a second section.

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
| 9ED2 | 2 LE | party gold carried (0-65000) | search 0 -> 1536 after withdrawals; watch `gold` |
| 9A25 + n*0xAA | 6 | party member n (0-5): strength, intelligence, dexterity, constitution, charisma, luck | stats search; poke 9A25=10 showed STR 16 in Inspect |
| 9A2E / 9A2F + n*0xAA | 1+1 | magic: shown as [9A2F]/[9A2E] on Health | poke 9A2E=3 -> "5/3" |
| 9A30 / 9A31 + n*0xAA | 1+1 | hit points: shown as [9A31]/[9A30] on Health (which is current: open) | poke 9A30=9 -> "11/9"; slot 2 (9ADA) checked |
| 9AA7 + n*0xAA | 12 | party member name (PETSCII capitals, space-padded), 0x82 after the stats | name search |
| 8A0D + k*0xAA | - | guild roster copy (same layout; grunt = roster #1) | name search |

## Emulation notes
- Loads use the drive in real time (the "Drive Technology" credit is a fast loader for the boot; later loads sit in
  KERNAL serial code, PC ED5A/EEB2). Everything works on this backend: boot, town, wilderness, game save to
  disk 1, export, reload.
- Screens are mostly text-mode with a custom font: `play.py text` reads menus and stats (capitals in the font
  show as lowercase in the text dump; town and wilderness pictures appear as character garbage).
- Water animates outdoors: wilderness frames never settle (fine; preview takes them as they are).
- In the town screen the red "ENTER" marker can lag behind the highlighted building after a save (cosmetic).

## Checkpoints
`title`, `menu`, `pelnor_new` (town, no party), `guild_created` (six characters made), `party` (formed, guild
menu), `pelnor_party`, `pelnor_gold`, `outdoors_pelnor` (via a look into the Armory), `saved_start` (after the
first save), `pineville_old`. `tools/cachecheck.py phantasie`: 10/10 reproduce (2026-11-21).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| C64 manual + supplement (archive.org text) | https://archive.org/details/Phantasie_I_1986_SSI | controls, C64 differences, towns, save, backup, races/classes | 2026-11-21 |
| Rulebook scan (archive.org, mocagh copy) | https://archive.org/details/vgmuseum_ssi_phantasie-manual | same text, cross-check | 2026-11-21 |
| Wikipedia | https://en.wikipedia.org/wiki/Phantasie | release facts, premise | 2026-11-21 |
| mocagh.org refcard, datadrivengamer blog | - | not reachable from the container (host not allowed) | 2026-11-21 |
| GameFAQs / TCRF | - | no Phantasie (C64) pages found | 2026-11-21 |

## Open questions
- Where do encounters happen? None in ~80 steps around Pelnor on paths and grass.
- Dungeon entry: does the game ask for disk 2 by a prompt, and does `disk:2` + `return` work? Dungeon saves go to
  which disk?
- Which HP/magic byte is current and which is max.
- Outdoor position: candidates 7506/753E changed with a south step; not confirmed.
- Levels and equipment of the old Pineville party (useful for late-game shots).
