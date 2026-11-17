# Digital Devil Story: Megami Tensei (Famicom, English translation patch) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
**ROM text** = read from the patched ROM's English script (`work/scout/megami-tensei/text_dump.txt`, decoder below),
not yet seen in play.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Digital Devil Story: Megami Tensei / デジタル・デビル物語 女神転生 (Dejitaru Debiru Sutōrī: Megami Tensei); title screen "DIGITAL DEVIL STORY / MEGAMI TENSEI" (verified) |
| Platform / model used | Famicom, NTSC (`game.json`); mapper 76 (Namco 3446), 256 KiB PRG + 128 KiB CHR, no battery |
| Release (region, year) | Japan, 11 September 1987 (Wikipedia); never released outside Japan; English fan translation applied (owner-supplied BPS, see `game.json` "source") |
| Developer / publisher | Atlus / Namco (title screen "NAMCOT (c) 1987 NAMCO LTD.", verified; Wikipedia) |
| Genre | first-person dungeon RPG with demon negotiation and fusion |
| Players / save system | 1 player; **passwords** (title: START / PASSWORD; 40 characters); no battery RAM (header, intake) |

## Boot sequence
- Intake probe: `work/intake/megami-tensei/sheet.png`: black, a dragon on grey (~f180), title from ~f300; with no
  input the attract intro starts ~f1000 (a boy at a computer, 6502-style assembler scrolling, then the story text
  "It all began at Juusei High, when Akemi Nakajima..."). The intro is a `cutscene` shot: `pow,w1000...`.
- `TITLE` = `w400,settle` (verified; cursor on START). Checkpoint `title`.
- `NEWGAME` = `start,w60,settle,STATS_NAKAJIMA,STATS_YUMIKO,w200,settle` (verified): START goes straight to the
  stat allocation (no naming: the heroes are fixed as **Nakajima** and **Yumiko**, so the owner's "ryz" rule does
  not apply). Each hero has 5 in every stat and 15 points to spend; the macros give
  Nakajima STR 9 WIS 7 ATT 9 AGI 8 LUK 7 and Yumiko STR 8 WIS 10 ATT 7 AGI 8 LUK 7, each confirmed with Yes.
  A short cutscene follows (the two at the foot of a stepped pyramid under the moon) and play starts on 8F.
  Checkpoint `start`.

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Up/Down, Start | cursor START / PASSWORD; Start confirms | verified |
| Stat allocation | Up/Down | stat cursor (wraps) | verified |
| | A / B | +1 / -1 point | verified |
| | (all 15 spent) | "Is this okay?" Yes/No, A confirms | verified |
| Dungeon | Up | step forward (a step animates; blocked by walls silently) | verified |
| | Left / Right | turn 90 degrees | verified |
| | Down | turn 180 degrees | verified |
| | A | put the cursor into the command window (Comp / Stats / Magic); A again opens the entry | verified |
| | B | toggles the info panel (floor + facing "8F E", automap box, CLASS levels) in place of the command window; with the panel open A does nothing | verified |
| | Start / Select | nothing seen | verified (no effect seen) |
| Command window | Comp | Call / Bind / Order (demon summoning; wraps, three entries) | verified (menu only) |
| | Stats | "View whose stats?" -> portrait, stats, Next Level, items, MAG, Jewel, Makka; Yumiko's page lists spells | verified |
| | Magic | "Cast which?" (Yumiko: Mappa 2 MP at level 1) | verified |
| Battle | menu | Fight / Run / Order / Auto, then per hero: Nakajima Fight / Comp / Guard, Yumiko Fight / Magic / Guard; "Is this okay?" Yes | verified |
| Stairs | Up into them | "Use the stairs?" Use / Don't (cursor on Don't: `up,a`) | verified |
| Text | A | next page; text types slowly (~150 frames a page) | verified |
| Password screen | Right / A | next character in the alphabet / write it and advance the entry cursor | verified; Down, B, Select, Start: no visible effect in one test |

Input timing: the default press (hold 8, wait 40) works everywhere tested (stats, menus, steps, turns). Text
pages: one `a` plus `w150` per page (typewriter rule). A battle round with messages takes up to ~900 frames.

## Game structure
- Story (ROM text, intro verified): Akemi Nakajima of Juusei High wrote a Devil Summoning Program; demons
  escaped; he and Yumiko (Yumiko Shirasagi, Wikipedia) go after them. The prisoner ("I was bound by the hands of
  Lucifer") asks to be freed.
- The dungeon is a tower/labyrinth called **Daedalus**; the game starts on **8F**, which is the town of
  **Micom** ("Welcome to the eighth floor of Daedalus. We call this place the town of Micom.", ROM text). Stairs
  down from the guard's corridor lead to 7F (verified). Other places in the text: the town of **Bien** (a town
  that moves and can be summoned), the **Heretic** (where demons are fused), "a strange shop".
- Bosses named in the ROM: Tyrant Minotaur, Tyrant Medusa, Tyrant Loki, Tyrant Hecate, Tyrant Set, Dark Lord
  Lucifer (ROM text; order of the list, likely the order of the game).
- Systems (Wikipedia + verified menus): two humans plus up to seven demons stocked (four summoned at once);
  demons join through negotiation (magnetite, money, items) and do not level up but are fused; moon phase
  ("FULL MOON" box, verified) affects demon behaviour; Mappa shows the automap in the info panel (verified).
- **Passwords:** given by **the sage in Micom Town** ("I am known as the sage here in Micom Town... Let me tell you
  the password.", ROM text): so passwords are asked for on 8F, not from a menu (the menus have no save entry,
  verified). Wrong entry: "That password is wrong." (ROM text). A FAQ quoted in search results says demons that
  are dead when the password is taken are gone after restarting (source, unchecked).

## Shot plan
- [ ] `title_screen` - title - title screen (@title)
- [ ] `boot_dragon` - boot - the dragon on grey before the title (~f180)
- [ ] `intro_code` - cutscene - attract intro: the boy at the computer, assembler code (~f1400 without input)
- [ ] `intro_story` - cutscene - "It all began at Juusei High..." text page (~f1900)
- [ ] `stats_nakajima` - menu - stat allocation with points left (@title,start,...)
- [ ] `stats_confirm` - menu - "Is this okay?" Yes/No
- [ ] `pyramid` - cutscene - the pyramid under the moon after the stats
- [ ] `start_corridor` - gameplay - first control on 8F (@start)
- [ ] `hud_panel` - hud - info panel open (floor/facing, CLASS, HP/MP) (@start,b)
- [ ] `guard` - dialogue - the guard's warning (@guard)
- [ ] `stairs` - gameplay - "Use the stairs?" prompt (@guard,up,w60,settle,up,settle,up,settle,up)
- [ ] `f7_corridor` - gameplay - 7F corridor (@f7_arrival)
- [ ] `mappa` - map - automap after Mappa (@f7_mappa)
- [ ] `status_nakajima`, `status_yumiko` - inventory - Stats pages (MAG, Jewel, Makka, spells)
- [ ] `comp_menu` - system - Comp: Call / Bind / Order
- [ ] `battle_menu` - battle - Gnome x4, Fight / Run / Order / Auto (@battle_gnome)
- [ ] `battle_attack` - battle - "Nakajima attacks!" / damage message
- [ ] `battle_magic` - battle - Yumiko casting in battle
- [ ] `negotiation` - system - a demon talking / joining (needs play: when a demon speaks first)
- [ ] `summon` - system - a demon called with Comp > Call, party list with demons
- [ ] `fusion` - system - the Heretic's fusion screen (needs two demons)
- [ ] `micom_town`, `sage_password` - dialogue / save - the sage giving a password
- [ ] `shop` - shop - a shop in Micom or Bien
- [ ] `heal` - system - healing ("health was restored")
- [ ] `password_screen` - save - password entry (@password_entry) and a filled one
- [ ] `levelup` - battle - victory / EXP / level up
- [ ] `boss_minotaur` - boss - Tyrant Minotaur (first boss, likely)
- [ ] `later_floor` - gameplay - a deeper floor with a different wall set
- [ ] `gameover` - gameover - GAME OVER skull and taunt (@gameover)
- [ ] `ending` - ending - only via a late password (none known)
How to reach: everything up to `battle_menu`, `mappa`, `gameover` and the password screen is a checkpoint
here. Negotiation, summon, fusion, the sage, shops, level-up and bosses need play on 8F/7F with frozen HP
(`freeze:04B5=1700,freeze:04C3=1500`) and, for bosses, a password or pokes once the password format is known.

## Strategy and walkthrough notes
- **Auto loses the first fight**: Gnome x4 on 7F wiped the level-1 party under Auto (that is the `gameover`
  route). Freeze both heroes' HP for every fight (above); battles are still slow (Gnomes take ~4 damage a hit and
  come in fours), about 900 frames a round: prefer Run (`down,a`) unless the fight is the shot.
- The guard on 8F (three steps E, then S) only warns; walking on past him leads to the stairs down to 7F.
- The first random encounter route is in `battle_gnome` (RNG follows frame timing: change the walk or add `wN`
  to get another group).
- Talk to everyone on 8F (Micom): the sage gives passwords, someone mentions the Heretic (fusion) and Bien.

## Naming
None: the heroes are Nakajima and Yumiko, fixed (verified: the game goes from START straight to stat
allocation). Demons keep their names.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Survive any fight | `freeze:04B5=1700,freeze:04C3=1500` (Nakajima 23 HP, Yumiko 21 HP, 16-bit) | RAM (here) | verified for 8 battle rounds (HP stayed full) |
| Floor display | `poke:055D=05` changes the panel to "5F" | RAM (here) | verified for the display only; whether the map follows (poke during the stairs transition) is untested |
| Passwords | from the sage in Micom Town (8F) | ROM text | not yet obtained |
| Action Replay codes | almarsguides.com has an Action Replay page for this game ("enemies can be killed in one hit" etc.) | search result | host not allowed here: owner to fetch |
| Debug menu / level select | none found (TCRF 403) | - | - |

No password list was found: GameFAQs, StrategyWiki, TCRF and gamehacking.org answered 403, the archive.org
manual scan's file host was refused by the proxy, the FAQ PDF on video-games-museum.com is on a host that is
not allowed. Making a "late" password: poke levels/stats/items, then ask the sage (README "Hangs and dead ends").

### Saves (rom/saves/megami-tensei/, never committed)
None: password game, no battery. Record passwords here once the sage gives one.

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| 0490 | 1 | facing: 1 N, 2 E, 3 S, 4 W (0491/0492 = step vector) | RAM diff over four turns, matches the panel; verified |
| 055D | 1 | floor number shown in the panel (8 at start, 7 after the stairs; 00FD changes with it) | RAM diff over the stairs; poke shown in the panel |
| 04B4 | 1 | Nakajima level | RAM (value 1) |
| 04B5 / 04B7 | 2+2 | Nakajima HP / max HP (little-endian) | RAM (23/23); freeze verified in battle; a poke does not redraw the status window until it is redrawn |
| 04B9-04BD | 5 | Nakajima STR WIS ATT AGI LUK | RAM (9 7 9 8 7 = the allocation) |
| 04C2 | 1 | Yumiko level | RAM |
| 04C3 / 04C5 | 2+2 | Yumiko HP / max HP | RAM (21/21); freeze verified |
| 04C7 / 04C8 | 1+1 | Yumiko MP / max MP | RAM (13/13; 11 after Mappa) |
| 04C9-04CD | 5 | Yumiko STR WIS ATT AGI LUK | RAM (8 10 7 8 7) |
| ? | | position x/y | not found: 00CE/00CF and 0102/0103 follow steps for a while but are overwritten (temporaries); 055C counts steps |
| ? | | Makka, MAG, Jewel, EXP | not found (all 0 at start; win a battle, then `find`) |
`play.py find` returned 0 candidates right after `find reset` in this game (twice); dumping RAM with `peek` and
diffing worked (`work/scout/megami-tensei/ramdiff.py save NAME` / `diff A B C`).

## Emulation notes
- NTSC, defaults fine. Mapper 76 runs in Mesen without trouble.
- The left 8-pixel column shows garbage tiles in the dungeon view (the console's output, do not crop).
- Text types slowly; `settle` may stop mid-page because the typewriter pauses: use fixed `w150` after each `a`.
- The status window (HP/MP) is not redrawn after a RAM poke until the game redraws it (menu, battle).
- Script decoder (patched ROM): space BC, a-z = 24-3D, A-Z = 9A-B3, line break FD FE, '.' 61.

## Checkpoints
All in `checkpoints.txt`; built from an empty cache and compared with a cache hit: identical frames
(2026-11-17). `guard` -> `f7_arrival` (stairs) -> `battle_gnome` (first random battle) / `f7_mappa` (automap);
`password_entry` from `title`; `gameover` from `battle_gnome` (Auto).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Digital_Devil_Story:_Megami_Tensei | release, developer, systems (demons, fusion, moon, passwords) | 2026-11-17 |
| archive.org manual scans (metadata only) | https://archive.org/details/digital-devil-story-megami-tensei-fc-hiresscans | exists (Japanese manual PDF/OCR); download host refused by the proxy | 2026-11-17 |
| Patched ROM text | `rom/megami-tensei.nes`, decoded | place names, sage/password, bosses | 2026-11-17 |
| GameFAQs, StrategyWiki, TCRF, gamehacking.org | (game pages) | 403, unavailable | 2026-11-17 |
| video-games-museum.com FAQ PDF, almarsguides.com Action Replay codes | https://www.video-games-museum.com/en/faqs/Nes/4287-Digital-Devil-Monogatari-Megami-Tensei.pdf, https://almarsguides.com/retro/walkthroughs/nes/games/digitaldevilstorymegamitensei/actionreplay/ | hosts not allowed: for the owner | - |

## Open questions
- Where exactly the sage is on 8F, and the password format (could a password be built from RAM?).
- Position RAM (x/y) and money/MAG/EXP addresses.
- Does a floor poke during the stairs transition load the other floor's map (warp)?
- How negotiation starts (no Talk command in the battle menu: probably the demon speaks first).
- Password screen: which button deletes a character / confirms (Down, B, Select, Start showed nothing).
