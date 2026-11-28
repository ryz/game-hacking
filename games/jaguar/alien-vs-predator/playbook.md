# Alien vs Predator - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `python3 tools/play.py start alien-vs-predator --route @start` (Marine), `@start_alien`,
  `@start_predator`. Model `ntsc` (HLE boot, no Jaguar logo; `ntsc-bios` only for a `boot` shot of the logo).
  Needs `rom/alien-vs-predator.j64` (`python3 tools/vault.py pull alien-vs-predator`).
- **Chain:** `title` (f600) -> `menu` -> `select` (Alien in front) -> `start` / `start_alien` / `start_predator`.
  The macros `MARINE`, `ALIEN`, `PREDATOR` do the same from power-on. Confirm = A (any fire button) everywhere.
- **Warp anywhere:** `WARP:NN` (= `poke:2F5AC=00NN,w300`): 01-05 sublevels 1-5, 06-0D air ducts
  1B 2B 3B 3C 4B 4C 5B 5C, 0E Alien ship, 0F Predator ship. Works for every character, no debug mode needed;
  the arrival shows "ENTERING SUBLEVEL N" for about 3 s (add `w180` for a clean view).
- **Gear by poke (Marine):** weapons `poke:2F30A=1E` (bits 1-4 shotgun, pulse rifle, flamethrower, smart gun),
  ammo words 2F214/2F224/2F234/2F244 (max at +2: 44/264/88/88), security `poke:30AD0=07` (0-10, HUD shows
  "07"), select the weapon with keypad `1`-`4`. Energy `30A6A` (word; Marine 1000 max, Predator 3000).
- **Debug mode (verified, ROM code):** macro `DEBUG` in play (pause, option, 6, 1+3, then
  B A 9 A 9 A * Option 6 # * * Option 2 Option); then resume with `pause` and any move. Keys afterwards:
  Option+B / Option+A sublevel up/down, Option+6 / Option+9 security +1/-1, Option+1-4 toggle weapons,
  Option+8 motion tracker, Option+5 CHEAT ON/OFF (no death, ammo refills; damage still drains energy).
  `GODMODE` = `poke:30A7A=FFFF` sets the same flag without the code.
- **Saves:** Pause, Option, `down` (GAME 1), B = save (`pause,w30,option,w30,down,w20,b,w120`);
  `saves/01_start.sav` = Marine at the start in GAME 1; `sav:01_start,MENU,down,w30,a,w120` shows the list.
- **Traps that cost calls:**
  - `settle` stops on the black frames after a menu press: use fixed waits (macros do).
  - The Marine's "LOADING SIMULATION... PRESS FIRE" takes about 1000 frames (Alien/Predator about 500): a press
    before that is lost.
  - The Alien start is under attack from something unseen: energy falls from about 1025 to 825 in the first
    10 s (purple flash). Hold `freeze:30A6A=0401` for Alien shots.
  - Gameplay screens never settle (animated HUD, enemies): end shot routes with `!` or a fixed wait.
  - Option+key debug combinations are exact: no other button may be held.
- **Position and walking (2026-11-28):** player x/y are words at `2F1CE` / `2F1D2` (cell 0-63, fraction in the
  next word), angle `2F1D6` (0000 east, 4000 north = y-1, 8000 west, C000 south). A position poke is a clean
  teleport: `poke:2F1CE=0017B000,poke:2F1D2=00068000,poke:2F1D6=0000` stands in front of a terminal.
  The level grid is in RAM at `4FC00` (64x64 cells of 8 bytes, walls W N E S): draw it with
  `games/jaguar/alien-vs-predator/tools/avpmap.py ROUTE [--box x0,y0,x1,y1] [--raw]`; walk honestly with
  `tools/avpwalk.py ROUTE X,Y ... [--face 0000] [--hurt-ok]` (path search, prints the pad tokens; it stops when
  energy falls so you can fight). Score / honor points: long at `30A76`.
- **Wall ids on sublevel 3** (byte values in the grid): 05 terminal, 06 vent, 0F/0E/02/01/10/11/0A signs
  (BRIG, CANTEEN, ELEVATOR, SUB LEVEL 3, BARRACKS, PETTY OFFICERS AREA, AIRLOCK), 40 hatch of a lift cell, 50 and
  58 doors, 28 airlock doors, 30 cell bars, 08 wall locker with shotgun rounds.
- **Terminals:** A at close range; menu types for ~400 frames; B selects, A next page, C exits (after C the menu
  retypes: wait 400 before the next key). Lift: A opens, step in (`up:40`), `a+down:30` rides down, `w600`,
  `right:128,w20,a` opens the doors on the new level.
- **High score entry:** game over with a score above 400,000 (`poke:30A76=0006AC02`, 437250); each letter starts
  at A, `up` steps backwards (A, symbols, Z, Y, X ...): RYZ = `up*15,right,up*7,right,up*6,a`. The table is then
  only reachable through title and menu with long waits (`a,w400,a,w400,down,w30,down,w30,a,w150`).
- **Reset:** `star+hash:30` (held; an 8-frame press does nothing).
- **Predator weapons:** `poke:30A76=000BEC26` (781,350 honor) gives all four; SHOULDER CANNON ATTAINED appears
  ~36 frames after the next key. Keys: 1 combistick, 2 shoulder cannon, 3 smart disc (4 not identified).
- **State:** captured 2026-11-28: `main` 75 shots, `start` 28 shots, both verified; lenses clean. Open: boot
  logo shot (needs `ntsc-bios`), cocooning, other enemy kinds, Queen, med-lab, self-destruct, ending.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Alien vs Predator |
| Platform / model used | Atari Jaguar cartridge (4 MiB, EEPROM save), `ntsc` |
| Release (region, year) | World cartridge (filed `na`): NA 21 Oct 1994, UK 20 Oct 1994, JP 8 Dec 1994 (Wikipedia) |
| Developer / publisher | Rebellion Developments / Atari Corporation |
| Genre | first-person action (corridor shooter / melee), three playable species |
| Players / save system | 1 player; EEPROM, 3 save slots (GAME 1-3), save anywhere from the pause menu |

Dump: SHA-1 fd8c89250ebc1e403838b2e589d1f69e3fe2fe02, CRC32 dc187f82. The cartridge code is compressed
(inflate): ROM strings are unreadable, read text from a DRAM dump instead (`work/scout/alien-vs-predator/dram.py`).

## Boot sequence
- Intake probe: `work/intake/jaguar/alien-vs-predator/sheet.png`. Black to f300, logo build f300-480, logo with
  copyright f480-760, main menu from f780; idle on the menu about 800 frames -> attract intro (USCM "final
  transmission" text, then ship cutscenes), which returns to the menu.
- `TITLE` = `w600` (logo + copyright). `MENU` = `w780`; from `@title`, `a,w120` also reaches the menu (verified).
- `SELECT` = `MENU,a,w240`: carousel, Alien in front; `right` -> Predator, `left` -> Colonial Marine (verified).
- Fire on a character -> briefing text ("LOADING SIMULATION...", then "PRESS FIRE") -> fire -> first control.
  `MARINE` = `SELECT,left,w60,a,w1000,a,w300`, `ALIEN` = `SELECT,a,w600,a,w600`,
  `PREDATOR` = `SELECT,right,w60,a,w600,a,w600`; `NEWGAME` = `MARINE` (verified 2026-11-27).

## Controls
Manual (archive.org scan) + verified here. Jaguar pad: A, B, C, Option, Pause, keypad 0-9 * #.
| Context | Button | Action | Status |
|---|---|---|---|
| Menus | up/down, A (any fire) | move, confirm | verified (A, B and C all confirm the character) |
| Character select | left/right | rotate the carousel | verified |
| All | d-pad up/down | forward/back | verified (Marine) |
| All | d-pad left/right | turn | verified |
| Marine | A | open/close doors, use terminals, enter airlocks/ducts | verified (cell bars open) |
| Marine | B | fire the selected weapon | verified with a poked weapon (`b:60`) |
| Marine | C + left/right | sidestep | source (C alone does nothing: verified) |
| Marine | keypad 1-4 | shotgun, pulse rifle, flamethrower, smart gun | verified (weapon appears in hand) |
| Alien | A / B / C | claw (also doors) / bite (jaw) / tail | source; presses verified to do no harm |
| Alien | Option + left/right | sidestep | source |
| Alien | claw, tail, claw on a Marine | stun, then walk over him: "COCOON COMPLETE" | source |
| Predator | B | attack with the selected weapon | source |
| Predator | A | open/close door | source |
| Predator | Option | invisibility on/off (with vision filter; mask icon in the HUD) | verified |
| Predator | keypad 6 | cycle the vision filter (5 filters) | verified (one step) |
| Predator | keypad 5 | use the health reserve | source (StrategyWiki snippet) |
| Predator | keypad 1-4 | weapons: combistick, shoulder cannon, smart disc, wrist blade | source (HUD labels) |
| Predator | C + left/right | sidestep | source |
| All | Pause | pause ("PAUSED") | verified |
| Paused | Option | menu: HUD brightness slider, GAME 1-3 save slots, B = save | verified |
| Lift hatch | up + A / down + A | ride up / down a level | source |
| Terminal | A next, B previous, C exit | read pages | source |
| Facehugger on you | rapid left-right | shake it off | source |
| All | # + * | reset the game | source |

Input timing: the default press (hold 8, wait 40) works everywhere tried. The debug code works with holds of 1,
2 and 8 frames.

## Game structure
- A simulation of the USCM training base Golgotha: sublevels 1-5 joined by lifts and air ducts, plus the docked
  Alien ship and Predator ship (source; all seen through `WARP`).
- **Marine** (Pvt. Lance J. Lewis): starts in the brig on sublevel 3 with nothing. Collect weapons, motion tracker
  (on a dead Marine on sublevel 5), security cards 1-10 from dead staff; card 10 starts the self-destruct at the
  command centre on sublevel 2; escape in the pod on sublevel 5 (source). Terminals: logs, level schematic,
  First Aid in med-labs with card 4+ (source; strings "LEVEL SCHEMATIC", "FIRST AID" in RAM).
- **Alien**: starts in the Alien ship; goal: rescue the Queen held in the Predator ship. Cannot heal; cocoons up to
  three Marines as extra lives; air ducts only, no lifts (source).
- **Predator**: starts in the Predator ship with the wrist blade; goal: the Alien Queen's skull in the Alien ship.
  Honor points (the score) unlock combistick 150,000, smart disc 350,000, shoulder cannon 750,000; kills while
  invisible cost points; health reserve refilled by food/medkits; lifts, no ducts (source).
- Death: "SIMULATION TERMINATED" (USCM badge), then the high score table (verified).
- Level ids (RAM `2F5AA`, verified by warping): 1-5 sublevels, 6-13 ducts 1B 2B 3B 3C 4B 4C 5B 5C, 14 Alien ship,
  15 Predator ship.

## Shot plan
`shots.txt` holds 30 lines with routes, all previewed (`work/preview/jaguar/alien-vs-predator/plan.png`):
title 1, menu 7 (main, 3 selects, high scores, pause, ...), cutscene 6 (3 briefings, 3 attract scenes), credits 1,
gameplay 11 (3 starts, cell, 5 environments, 2 weapons), system 3 (cloak, filter, tracker), save 2, gameover 1.
Captured 2026-11-28 (main 75, start 28; `shots.txt` holds the main set). Ticked below; open items stay open:
- [ ] `boot_jaguar_logo` boot - `ntsc-bios` works (JAGUAR + ATARI logo at w400, the game boots after), but shoot.py takes one model per set: not shot
- [x] terminal menu, General Log page, level schematic (map) - walk to a terminal (sublevel 3 near the brig?)
- [x] (weapon and rounds; no card) security card / weapon / ammo pickup message (inventory) - corpses near the brig
- [x] Marine firing each weapon at an Alien (`WARP:04` has an Alien close), acid blood, flamethrower
- [ ] facehugger on the screen, egg (Alien ship / sublevel 5)
- [ ] Alien claw / tail / bite, "COCOON THE ENEMY" and "COCOON COMPLETE", cocoon count in the HUD
- [x] (honor poke) Predator weapons: poke the score past 750,000 once its address is known (or debug Option+1-4), smart disc
  thrown, shoulder cannon blast; dishonour message
- [x] (lift only) lift hatch and ride, airlock, self-destruct terminal and escape pod (end)
- [ ] Alien Queen (Predator ship for the Alien, Alien ship for the Predator) - boss
- [x] Marine in the Alien and the Predator ship (`WARP:0e` / `WARP:0f`): distinct environments

## Strategy and walkthrough notes
- Use `WARP` and pokes instead of walking; the base layout is not mapped here yet.
- Hold energy for fights: `freeze:30A6A=03A2` (Marine, 930 of 1000) or `GODMODE` (prevents death only).
- Sublevel 4 arrival (`WARP:04`) puts an Alien straight in front of the Marine: good for weapon and combat shots.
- Item positions and enemies are randomised per simulation and after a restore (source): routes stay
  reproducible here because the emulator is deterministic, but a different wait moves things.

## Naming
High score entry: three letters, entered as RYZ (route in Read first; shots `highscore_entry`, `highscore_ryz`).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Warp to a level | `WARP:NN` (poke 2F5AC) | ROM code + test | verified, all 15 ids |
| Debug mode | `DEBUG` macro (pause, option, 6, 1+3, B A 9 A 9 A * Option 6 # * * Option 2 Option) | Atarimania (via search snippet), ROM code at C9xx-CE88 (DRAM) | verified: sets 2EE78/2EE79 |
| Debug level select | Option+B up, Option+A down | arcade-history (snippet), ROM code 10470 | verified |
| Debug security | Option+6 +1, Option+9 -1 (0-10) | ROM code 104D2 | verified |
| Debug weapons | Option+1/2/3/4 toggle shotgun/pulse rifle/flamethrower/smart gun | ROM code 10566 | verified (Marine) |
| Debug motion tracker | Option+8 | test | verified |
| CHEAT ON/OFF | Option+5 after DEBUG, or `GODMODE` | ROM code 10524, C5CA, E670 | flag verified; effect read from code |
| HUD brightness | Pause, Option, left/right on HUD | manual | menu seen |

### Saves (rom/saves/alien-vs-predator/, never committed)
None downloaded (GameFAQs refuses automated access). Own export: `games/jaguar/alien-vs-predator/saves/01_start.sav`
(Marine, GAME 1, start; restore verified through RESTORE GAME 1).

## RAM map (for `game.json` "ram" watches and pokes)
DRAM addresses for this ROM; the game copies its code to DRAM, so these are fixed.
| Address | Size | Meaning | How found |
|---|---|---|---|
| 02F5AA | word | current level id (1-15, list above) | code at C384 + warps |
| 02F5AC | word | pending level: write N to warp | code 104CA/EEBC; poke verified |
| 030A6A | word | energy (Marine 1000 max at 030A6C; Alien about 1125; Predator 3000) | death check C582; poke shows in the HUD bar |
| 030AD0 | byte | security clearance 0-10 (HUD "SECURITY 07") | debug code; poke verified |
| 02F30A | byte | weapons owned, bits 1-4 (Marine); Predator starts with 30, Alien 0E | debug code; poke verified |
| 02F214 / 2F224 / 2F234 / 2F244 | word | Marine ammo shotgun / pulse rifle / flamethrower / smart gun (max at +2: 2C, 108, 58, 58) | pointer 2F274; poke + fire verified (pulse rifle -2 per burst) |
| 030A7A | word | CHEAT flag (FFFF: no death, ammo refills) | code |
| 02EE78 / 02EE79 | byte | debug keys enabled (FF) | code CE44 |
| 02EE60 | long | pad, active low (Atari layout: A bit 29, B 25, C 13, Pause 28, Option 9, up 20 ...) | test |
| 039834 | long | pointer of the on-screen message record | code |
| 02F1CE | long | player x (high word = cell 0-63, low word = fraction) | walk + diff, poke verified |
| 02F1D2 | long | player y (same format; north = smaller y) | walk + diff, poke verified |
| 02F1D6 | word | facing angle: 0000 east, 4000 north, 8000 west, C000 south; right turns decrease it | turn + diff |
| 030A76 | long | score (Marine 10,000 per Alien) / honor points (Predator) | kill + search; poke verified (HUD) |
| 04FC00 | 64x64x8 | level grid: per cell bytes 0-3 = wall id on the W, N, E, S side (0 = open), 4-5 floor/ceiling texture | code F040 (flood fill from the player) |
| 03EAE0 | 64x64 words | visited / reachable cells (FFFF) | code F01E |

## Emulation notes
- Virtual Jaguar runs the game fully: all three starts, every level id, cutscenes, menus, save and restore, no
  freezes or render faults seen in about 60 previewed routes (2026-11-27). Speed: a route of ~2500 frames plays
  in about 5 s.
- The HUD is drawn translucent over the 3D view (by design). Damage flashes the screen purple (Alien).
- `cachecheck.py`: 6/6 checkpoints reproduce.

## Checkpoints
`title`, `menu`, `select` (Alien in front), `start` (Marine), `start_alien`, `start_predator`. The three starts
branch from `select`. Start set: `s_fight1` (honest walk from the brig to the east-room door, first Alien
coming in) and `s_terminal` (two Aliens killed, facing the brig-office terminal at 43,13).

## Start set (honest route, 2026-11-28)
Cell bars (`a`), walk out over the body (shotgun), path search to the brig office (`avpwalk.py`), first Alien:
`down:10,right:10` then six `b,w30`; second Alien at the south door: `down:10` and four `b,w30`; walk on with
`--hurt-ok` (acid where it died), terminal at 43,13: schematic, General Log (4 pages here), Pause, Option,
`down`, `b` saves GAME 1; `star+hash:30` resets; the Restore list shows GAME 1. Save `saves/02_brig_terminal.sav`.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Manual (scan, OCR text via archive.org stream) | https://archive.org/details/avp-jag | controls, items, saving, scenarios, honor points | 2026-11-27 |
| Wikipedia | https://en.wikipedia.org/wiki/Alien_vs_Predator_(Atari_Jaguar_game) | release, developer, structure | 2026-11-27 |
| Atarimania (search snippet only, host not reachable) | https://www.atarimania.com/game-atari-jaguar-alien-vs-predator_30098.html | debug code | 2026-11-27 |
| arcade-history (search snippet only) | https://www.arcade-history.com/game/76401/ | level select keys | 2026-11-27 |
| StrategyWiki controls (403; search snippet only) | https://strategywiki.org/wiki/Alien_vs_Predator_(Atari_Jaguar)/Controls | Predator keypad 5/6 | 2026-11-27 |
| TCRF (tcrf.net 403, new.tcrf.net not allowed), GameFAQs (403), gamehacking.org (403) | - | unavailable | 2026-11-27 |

## Open questions
- ~~Score / honor points address~~: `30A76` (2026-11-28).
- ~~Player position and facing~~: `2F1CE` / `2F1D2` / `2F1D6` (2026-11-28).
- ~~First terminal, lift, items on sublevel 3~~: terminals at cells 23,6 (east face) and 43,13 (brig office),
  lifts at 34,21 (enter from the west) and 9,21; shotgun on the body outside the cell; rounds in the locker
  at 32,6 (2026-11-28).
- Is the attack from behind at the Alien start a Predator? (purple flashes, energy -200 in 10 s.)
- ~~High score name entry~~: seen and done (RYZ).
- The save record format in the EEPROM (slot 1 holds energy 03E8 at byte 16).
