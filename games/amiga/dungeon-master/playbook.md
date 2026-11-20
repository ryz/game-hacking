# Dungeon Master - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

Scouted 2026-11-20 (game-scout): mouse positioning worked out and put into macros, controls verified, the Hall of
Champions mapped (23 mirrors), a party of four recruited and taken down to level 2 with a torch, an in-game save
to a disk the game formatted itself, RESUME from that save, RAM map. Helper scripts of the scout:
`work/scout/dungeon-master/` (not committed; `try.py` runs route variants and tiles them, `explore.py` walks a
level depth-first by the position bytes, `path.py` turns the walked graph into keypad routes).

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Dungeon Master, version 3.60 ("V3.6" on the save dialogs; multi-language English/French/German) |
| Platform / model used | Amiga, `A500` (Kickstart 1.3, 512K chip + 512K slow RAM): **verified** from power-on to level 2, saving and resuming |
| Release (region, year) | Europe (Psygnosis release, title text "COPYRIGHT 1992"); the game is from 1987 (Atari ST), first Amiga release 1988 (Wikipedia) |
| Developer / publisher | FTL Games / Psygnosis (this version) |
| Genre | real-time first-person dungeon crawler, party of up to four |
| Players / save system | 1 player; saves to a separate disk the game formats itself (volume `DungeonSave`, file `DMGAME.DAT`, 48652 bytes): **verified** |
| Dump | `Dungeon Master v3.60 (FTL + Psygnosis).adf` from the owner's ZIP (SHA-1 in `game.json`); a cracked release (crack intro by The Driver/Dytec, SCSI, Mr.Rox & AmoK/Ministry): no copy protection left, **verified** |

## Boot sequence
- Intake probe: `work/intake/amiga/dungeon-master/sheet.png` (frame every 60 frames, no input).
- **verified** 2026-11-20 (checkpoints `entrance`, `dungeon`, rebuilt cold and identical):
  - Kickstart 1.3 boot, then the disk's Startup-sequence types the crack note (`dungeonrel.txt`) in a hires
    AmigaDOS window and waits for the left mouse button: `w700,mouse1:10`. A click before about frame 600 is
    lost (the window is not up yet).
  - `BJELoad_R` loads the game: the Dungeon Master logo stays for about 4000 frames (80 s of game time) at the
    real floppy speed; clicks do nothing while it loads. Then the entrance doors with ENTER / RESUME / QUIT,
    the pointer already on ENTER: macro `TITLE` = `w700,mouse1:10,w4000`, checkpoint `entrance`.
  - `mouse1:10` on ENTER opens the doors, then about 4500 frames of loading (the doors stay open on the corridor)
    until the dungeon view with the movement arrows: checkpoint `dungeon` (no champions yet).
  - The same with a blank disk available for saving: checkpoint `sd_dungeon` (`sav:blank` prefix; the frame is
    pixel-identical to `dungeon`, the extra disk is not in a drive). All later checkpoints build on it.
  - A cold build of `sd_dungeon` takes about 15 s of host time; `level2` about 30 s.
  - On an `A1200` model the same loads take a fraction of the time (seen once with `emu.py --model A1200`); the
    A500 is kept as the machine the game was made for.
- The entrance is the game's title screen (there is no other title): ENTER at screenshot (285,71), RESUME
  (285,101), QUIT (285,133) **verified** (RESUME; ENTER is the default pointer spot).

## Pointer: how to put the mouse on a screen spot (verified 2026-11-20)
Dungeon Master is played with the mouse. `mouse:DX:DY` is relative, so every click starts from a known corner:
- One `mouse:` token moves the pointer **at most 120 counts** (larger values are cut to 120, not spread over
  frames: `mouse:-1000:-1000` moved only 60 px). 2 counts = 1 pixel, linear, no acceleration.
- `HOME` = `mouse:-120:-120*6,w4` pushes the pointer into the top-left corner: its tip is then at screenshot pixel
  **(21,19)** (the DM screen's 320x200 sits at about (20,18) in the 360x287 picture).
- `AT:A:B:C:D` = HOME, A moves of 120 counts right, B moves of 120 down, then C, D counts: tip at
  x = 21 + 60*A + C/2, y = 19 + 60*B + D/2. `CLICK:A:B:C:D` = AT + `mouse1` (left button, hold 8, wait 40).
- `python3 games/amiga/dungeon-master/tools/at.py SX SY [c]` prints the AT/CLICK token for a screenshot pixel.
- `HIDE` = `mouse:120:120*6,w4` pushes the pointer to the bottom-right, where it is not drawn: use it before
  every shot (the hand pointer otherwise sits in the view). Verified: no pointer pixel left on screen.
- Exception: while dragging a champion icon in the formation box, a move through HOME cancels the drag; use a
  relative move from the picked-up icon (macro `FORMATION`).
- Named spots (screenshot pixels, all verified by their effect):

| Spot | Pixel | Macro / token |
|---|---|---|
| Wall ornament in front (mirror, sconce, button) | (131,100) | `MIRROR`, `WALL` (`CLICK:1:1:100:42`) |
| Champion panel RESURRECT / REINCARNATE / CANCEL | (151,132) / (210,132) / (181,169) (all three verified) | `RESURRECT`, `REINCARNATE`, `PANELCANCEL` |
| Name entry OK | (226,169) | `NAMEOK` |
| Champion 1 left (ready) hand slot in the top bar | (32,35) | `CLICK:0:0:22:32` |
| Champion 1 action button (right panel) | (263,121) | `CLICK:4:1:4:84` (then the action list) |
| Spell caster tab of champion 2 (Tiggy) | (306,63) | `CLICK:4:0:90:88` |
| Rune row: 1st..6th symbol | x 261, 276, 290, 304, 318, 332; y 74 | e.g. 1st `CLICK:4:0:0:110`, 4th `CLICK:4:0:86:110` |
| Cast (the incantation line) | (290,86) | `CLICK:4:1:58:14` |
| Formation icons (top right) | front L (309,25), front R (328,25), back L (309,40), back R (328,40) | `FORMATION` swaps front R and back L |
| Inventory save (disk) / sleep (ZZZ) / close (X) icons | (198,58) / (216,58) / (234,58) | in `SAVEMENU` |
| Save dialog: SAVE / QUIT / FORMAT FLOPPY / CANCEL | (78,126) / (185,126) / (78,163) / (185,163) | `SAVEBTN`, -, `FORMAT`, `SAVEDONE` |
| Entrance RESUME | (285,101) | in `RESUME` |
| Load dialogs OK | (180,162) | in `RESUME` |

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Crack intro | `mouse1` (left button) | continue to the game | verified |
| Entrance | `mouse1` on ENTER (pointer starts there) / RESUME | new game / load a save | verified |
| Dungeon | `kp8` (`FWD`) | step forward | verified (position bytes) |
| Dungeon | `kp5` (`BACK`) | step back | verified |
| Dungeon | `kp4` (`SL`) / `kp6` (`SR`) | step left / right without turning | verified (position bytes) |
| Dungeon | `kp7` (`TL`) / `kp9` (`TR`) | turn left / right | verified (facing byte) |
| Dungeon | on-screen arrows (mouse) | the same six moves | forward verified (`CLICK` at (297,154)) |
| Dungeon | `f1`-`f4` | open / close the inventory of champion 1-4 | verified (`f1`, `f2`) |
| Dungeon | `esc` | freeze the game ("GAME FROZEN") | verified |
| Dungeon | click a mirror | show the champion: RESURRECT / REINCARNATE / CANCEL | verified |
| Name entry | `type:ryz` (keyboard works), `enter` = next line (title), OK button | name a reincarnated champion | verified |
| Dungeon | click a champion's bars or name | inventory (bars) / make leader (name) | bars verified; leader source (manual) |
| Dungeon | click a wall ornament / floor item with the hand | take, press, put | verified (torch from a sconce) |
| Dungeon | action button + action name | attack / use the item in the action hand | menu verified (THROW, BASH for a club); hitting not tried |
| Dungeon | spell panel: caster tab, runes, cast line, recant arrow | cast spells | verified (Tiggy, LO FUL cast: mana spent) |
| Inventory | click eye / mouth with empty hand (held) | statistics / food and water | source (manual); food/water panel shows by default (verified) |
| Inventory | disk icon / ZZZ / X | save menu / sleep / close | save and close verified |

Input timing: the default press (hold 8, wait 40) works for keys and clicks. `kp8,w30` per step is enough with
an unloaded party (every step of the routes landed, checked by the position bytes). After a stairs move wait
`w60`. Loads (doors at ENTER, save, format, resume) need long waits, see the macros.

**Stairs:** turning while standing on a staircase square takes the stairs again (arriving on level 2 and pressing
`TR` put the party back on level 1). Step off forward (`FWD`) before turning. **verified**

## Game structure
- Entrance (title) -> ENTER -> the **Hall of Champions** (level 1, which the game numbers 0): corridors with 24
  mirrors (manual: "no more than four" champions are chosen). 23 found and named here (map below); Gando not
  found. The hall's iron gate west of (6,9) is closed until at least one champion has joined, then open
  (**verified**: closed in the empty-party walk, open with the party).
- Behind the gate: a corridor south (an apple on the floor at (4,9), a torch in a sconce on the west wall at
  (4,14), a wall ring and an alcove at (4,16)) and the stairs down west of (4,15).
- **Level 2** (the dungeon proper) starts at (3,1) on the stairs, level index 1. It is pitch dark without light:
  carry a torch. Behind the arrival square a wooden door with a button (west) and a corridor (east).
- The dungeon has 14 levels (source: search summaries of walkthroughs); the Firestaff and the Power Gem are the
  quest items, Lord Chaos the final opponent; leaving with the Firestaff without defeating Chaos is a second
  ending (Wikipedia). Creature names on the disk (ROM text): Giant Scorpion, Swamp Slime, Giggler, Wizard Eye,
  Pain Rat, Ruster, Screamer, Rockpile, Ghost, Stone Golem, Mummy, Black Flame, Skeleton, Couatl, Vexirk, Magenta
  Worm, Trolin, Giant Wasp, Animated Armour, Materializer, Water Element, Oitu, Demon, Lord Chaos, Red Dragon,
  Lord Order, Grey Lord.

### Hall of Champions map (verified 2026-11-20)
Coordinates are the game's (X east, Y south). Start (1,3) facing south with the entrance doors behind (north).
Stand on the square, face the direction, click the mirror (`MIRROR`). Values are health / stamina / mana as the
panel shows them.

| Square, facing | Champion | H / S / M | Carries (seen) |
|---|---|---|---|
| (7,9) N | Halk the Barbarian | 90 / 75 / 0 | club, helmet, hide |
| (11,15) S | Stamm Bladecaster | 75 / 80 / 0 | axe |
| (6,13) W | Daroou | 100 / 65 / 6 | nothing |
| (16,14) S | Hissssa Lizar of Makan | 80 / 61 / 5 | nothing |
| (8,15) N | Leif the Valiant | 75 / 70 / 7 | clothes, boots |
| (15,4) E | Hawk the Fearless | 70 / 85 / 10 | arrows/stick |
| (14,12) E | Sonja She Devil | 65 / 70 / 2 | sword |
| (12,9) N | Linflas | 65 / 50 / 12 | green clothes |
| (7,16) S | Azizi Johari | 61 / 77 / 7 | daggers, throwing items |
| (10,5) S | Zed Duke of Banville | 60 / 60 / 10 | torch, chain armour |
| (9,7) W | Elija Lion of Yaitopya | 60 / 58 / 22 | magical box |
| (16,17) N | Gothmog | 60 / 55 / 18 | wand |
| (17,9) S | Nabi the Prophet | 55 / 65 / 15 | staff |
| (13,14) E | Mophus the Healer | 55 / 55 / 19 | food |
| (9,9) S | Syra Child of Nature | 53 / 72 / 15 | apple |
| (16,8) N | Alex Ander | 50 / 57 / 13 | staff |
| (10,4) N | Iaido Ruyito Chiburi | 48 / 65 / 11 | samurai sword |
| (13,12) N | Leyla Shadowseek | 48 / 60 / 3 | rope |
| (14,3) N | Chani Sayyadina Sihaya | 47 / 67 / 20 | moonstone (necklace) |
| (7,13) S | Wu Tse Son of Heaven | 45 / 47 / 20 | throwing stars |
| (12,13) W | Wuuf the Bika | 40 / 50 / 30 | flask |
| (14,6) S | Boris Wizard of Baldor | 35 / 65 / 28 | (item in backpack) |
| (9,13) E | Tiggy Tamal | 25 / 45 / 36 | staff/wand |

Other hall features: the "HALL OF CHAMPIONS" inscription on the wall south of (8,4); empty sconces at
(6,1) E, (6,4) W, (6,12) W; grates and wall rings; small items on the floor (blue at (6,1)/(4,3), green at
(16,6)/(14,9)/(11,14)). Explored: 116 squares of the hall plus 17 behind the gate.

## Shot plan
See `shots.txt` (plan lines with routes where the scout verified them; ids and categories per
`docs/capture-guide.md`). Summary by category (about 60 planned):
- boot 2 (crack note, logo while loading), title 1 (entrance doors), cutscene 1 (doors opening, a clip).
- Hall of Champions: gameplay/env 4 (start corridor, inscription, mirror wall, gate), system 6 (champion
  panel, reincarnate name entry, resurrect message, formation, leader change, gate open), content: several mirrors
  of different champions (inventory-style panels, one per family: barbarian, lizard, ninja, wizard).
- hud 1 (party bars, hands, spell panel, actions, arrows on level 2, pointer hidden).
- inventory 4 (inventory with food/water, statistics via the eye, an object examined, a chest/scroll), system:
  eating and drinking, sleeping (ZZZ), spell runes being recited, a cast spell (light, fireball later), a potion
  made (Wuuf with a flask: VI), throwing, action menus of several weapons, a level-up message, a lever/button
  opening a door, a pit, a teleporter, a pressure plate.
- battle 4+ (first monsters on level 2 and below: Mummy, Screamer, Rockpile, Giant Scorpion...), boss 1-2 (Lord
  Chaos needs the full game; a Red Dragon, Animated Armour or Demon), gameover 1 (party dead).
- save 5 (save menu, formatting, saving, RESUME prompt, "GAME LOADED, READY TO PLAY").
- env: plain corridors on levels 1, 2 and as deep as reached (`env_<level>_<what>`).
- `start` set: power-on to the first save, played as above (no pokes): crack note, logo, entrance, doors, hall,
  mirrors, the four champions, gate, torch, stairs, level 2, save. All of it is in the checkpoints already.
How to reach deeper levels: play down by the stairs from `saved`/`resumed`; there is no level warp yet (see
Shortcuts). Fights: RYZ and Stamm in front with club and axe; heal and cheat with the champion records.

## Strategy and walkthrough notes
- Party (chosen 2026-11-20 for capture variety): **ryz** = Halk the Barbarian reincarnated (front left, club;
  the strongest body in the hall), **Stamm** resurrected (front right, axe), **Tiggy** resurrected (back, the
  hall's largest mana: wizard spells), **Wuuf** resurrected (back, carries a flask: priest potions). Resurrected
  champions keep their skills (manual), so the two casters can cast from the start; one reincarnation gives the
  main character's name. Forum opinions found by search agree on Halk as a fighter and Wuuf as a flexible caster
  (dungeon-master.com threads, not opened: host blocked).
- Light: the hall is lit, level 2 is pitch dark. Take the torch from the sconce at (4,14) facing west (behind the
  gate) and put it into a hand (route in `level2`). A torch burns down (inferred from the ROM text "(BURNT OUT)");
  for long sessions cast the magic torch (manual: a power symbol, LO the weakest, then the element FUL; that FUL
  is the 4th symbol of the element row is the scout's recollection; the cast is verified only as "mana spent")
  or carry more torches.
- Real time: monsters act while the agent thinks. Use `esc` (GAME FROZEN) before long pauses in a fight; check it
  does not stay in the shot.
- Formation: fighters in the front row, casters behind (manual: swung weapons only reach from the front).
- Food and water drop over time; the Hall has an apple at (4,9) and Mophus carries food. Champions die of hunger
  (manual).
- Stairs: step off forward before turning (turning on stairs takes them).
- Cheats that are safe: the champion records (health, stamina, mana) are plain big-endian words and redraw on
  the inventory screen; keep values realistic.

## Naming
Main character: **ryz** (owner's rule). Champions are fixed characters: only a reincarnated one gets a new name
(up to 7 letters plus an optional title of up to 19, manual). The name entry accepts the keyboard: `type:ryz`
shows RYZ; `enter` moves to the title line; OK at (226,169) (`NAMEOK`). Route: `MIRROR,REINCARNATE,type:ryz,w30,
NAMEOK`. If more are reincarnated: condi, ebo, cubi (dispatch 2026-11-20). The title stays empty.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Same-level warp | `poke:C167D0=00XX,poke:C167D2=00YY,poke:C167CE=000F,w2,TL,TR` (X, Y, facing F; the turns redraw the view) | RAM (found here) | verified on level 1 (to Halk's mirror at (7,9) N) |
| Level warp | poking the level word C167D4 alone does not switch the map (view and moves stay on the old map) | RAM | failed; open |
| Health / stamina / mana | champion records (RAM map) | RAM | verified (health and mana pokes shown on the inventory) |
| Freeze | `esc` | game | verified |
| Ready-made Amiga save | Aminet `game/hint/DungeonMSave`: a DMGAME.DAT with four Artisan-level champions on level 1 near the stairs (search summary) | https://aminet.net/package/game/hint/DungeonMSave | not fetched (host blocked); it would have to be written into a DungeonSave disk image as `DMGAME.DAT` |
| Savegame editors | DMute (works with Amiga v3.6 per a forum thread title), an editor for PC/Amiga saves; edited saves fail the game's checksum unless the editor fixes it ("SAVED GAME DAMAGED") | dungeon-master.com forum (search results only) | not tried |
| Debug menu, level select | none found (tcrf.net Dungeon_Master_(Amiga) refused automated access) | - | open |

### Saves (rom/saves/dungeon-master/ and rom/saves/amiga/dungeon-master/, never committed)
| Name | Contents | How made | SHA-1 | Status |
|---|---|---|---|---|
| `blank` (rom/saves/dungeon-master/blank.sav) | ZIP with `savedisk.adf`: 901120 zero bytes (an unformatted disk); becomes disk 2 | made here (python, see below) | 6da3c85156b80b24d804ddba108b235e06c0eb32 | verified: the game formats it |
| `01_level2` (rom/saves/amiga/dungeon-master/01_level2.sav) | the formatted save disk with DMGAME.DAT: party of four on level 2 with a torch | `play.py export` after `SAVENEW` | 7b19b9b73f8f... (saves/README.md) | verified: RESUME loads it (`resumed`) |
Rebuild `blank.sav`: `python3 -c "import zipfile;z=zipfile.ZipFile('rom/saves/dungeon-master/blank.sav','w',zipfile.ZIP_DEFLATED);i=zipfile.ZipInfo('savedisk.adf',(1990,1,1,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,bytes(901120));z.close()"`.

### Saving and loading (verified 2026-11-20)
- The game saves to its own save disk in DF0: (one drive is enough: no `-df1` needed; the game asks for disk
  swaps). The blank disk must exist from power-on (`sav:` prefix), so the checkpoints from `sd_dungeon` on carry it.
- `SAVENEW` (first save): `SAVEMENU` (`f1` opens RYZ's inventory, click the disk icon: "PUT THE GAME SAVE DISK IN
  DF0:" with SAVE / QUIT / FORMAT FLOPPY / CANCEL), `FORMAT` (`disk:2`, FORMAT FLOPPY, "PUT A BLANK DISK IN DF0:",
  FORMAT FLOPPY again, "FORMATTING DISK . . ." with a bar, w6000), `SAVEBTN` ("SAVING GAME . . .", then the
  menu again: no "saved" message), `SAVEDONE` (`disk:1`, CANCEL, `f1` closes the inventory).
- `SAVEGAME` for later saves on the already formatted disk (no format): **verified** from `saved` (`FWD,SAVEGAME`):
  the disk then holds `DMGAME.DAT` and the previous save as `DMGAME.BAK`, play continues.
- `RESUME` at the entrance: click RESUME: "PUT THE GAME SAVE DISK IN DF0:" (LOAD SAVED GAME / CANCEL);
  inserting disk 2 loads by itself; "PUT THE DUNGEON MASTER DISK IN DF0:" OK; "LOADING GAME . . ."; "GAME
  LOADED, READY TO PLAY." OK; the party stands where it saved. Route: `sav:01_level2,pow,TITLE,settle,RESUME`.
- After `SAVEBTN` the save disk holds `DMGAME.DAT` (48652 bytes) on volume `DungeonSave` (read from the image).

## RAM map (for `game.json` "ram" watches and pokes)
All big-endian (68000). Same addresses in the `party`, `level2` and `resumed` runs (checked); Amiga memory can
move between boots of other routes, so re-check with `work/scout/dungeon-master/findbytes.py ROUTE RYZ`.

| Address | Size | Meaning | How found |
|---|---|---|---|
| C167CE | 2 | facing: 0 north, 1 east, 2 south, 3 west (low byte C167CF) | turning, peek |
| C167D0 | 2 | party X on the current level | stepping pattern |
| C167D2 | 2 | party Y | stepping pattern (`ramwalk.py`) |
| C167D4 | 2 | level index (0 = Hall level, 1 = level 2) | stairs, peek |
| C19748, C1974A | 2+2 | copies of Y (and X?) | stepping pattern |
| C18538 | 0x140 each | champion records, champion 1 at C18538, 2 at C18678, 3 at C187B8, 4 at C188F8 | names in RAM |
| record +0x00 | 8 | first name (ASCII, 0-padded) | names |
| record +0x08 | 20 | title | names |
| record +0x34 / +0x36 | 2 / 2 | health current / maximum | poke 77 -> "77/ 90" |
| record +0x38 / +0x3A | 2 / 2 | stamina x10 current / maximum (749 = "74") | values |
| record +0x3C / +0x3E | 2 / 2 | mana current / maximum | poke 33 -> "33/ 36" |
| C63A02 (candidate) | | level 1 square map, column x=1? (bytes 0x90 door, then 0x2x corridors) | pattern search, unconfirmed |

## Emulation notes
- A500 (Kickstart 1.3, 512K + 512K): runs the game from power-on through saving and resuming; nothing broken.
- Mouse: one `mouse:` token moves at most 120 counts (60 lores px); `docs/emulator/amiga.md` says large moves
  arrive over a few frames, but they are cut. Not the game: on the AmigaDOS screen of the crack note
  (`w700`, then `mouse:N:30,w12`) +50 and +100 counts moved Intuition's pointer 50 and 100 hires pixels, +200 and
  +400 both stopped at +120. So the limit is in the emulator or front end (PUAE's per-frame mouse delta), not a
  property of Dungeon Master. Workaround: chains of moves of at most 120 counts (macros `HOME`, `AT`).
- Disk swaps: `disk:2` / `disk:1` with `w100` work at every prompt; the game sees an inserted disk by itself.
- Screens settle normally in the dungeon (no idle animation); `settle` after `do` is fine.
- The emulated clock and RNG are deterministic: all routes replayed identically (cold rebuild check below).

## Checkpoints
| Name | What |
|---|---|
| `entrance` | the entrance doors (title), pointer on ENTER |
| `dungeon` | in the hall, no champions (route without the blank disk) |
| `sd_dungeon` | the same with the blank disk as disk 2 (`sav:blank`): the base of all later checkpoints |
| `party` | ryz, Tiggy, Wuuf, Stamm recruited; Stamm moved to the front; standing at Stamm's mirror (11,15) S |
| `level2` | level 2 at (3,0) facing east, ryz holding the torch, pointer hidden |
| `saved` | `level2` after `SAVENEW`: the save disk holds the game, disk 1 back in DF0:, pointer hidden |
| `resumed` | power-on with `sav:01_level2`, RESUME: the same party and place, loaded from the save |

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Dungeon Master manual (archive.org text of the scanned manual) | https://archive.org/stream/DungeonMasterManual/DungeonMasterManual_djvu.txt | champions, resurrect/reincarnate, naming, leader, screen areas, movement buttons, action hand, spells, inventory, eye/mouth, sleep, saving needs a blank disk the game formats | 2026-11-20 |
| Wikipedia: Dungeon Master (video game) | https://en.wikipedia.org/wiki/Dungeon_Master_(video_game) | release facts, story (Theron, Grey Lord, Lord Chaos, Firestaff), endings | 2026-11-20 |
| Web search summaries (dungeon-master.com forum, Aminet, walkthrough sites) | https://www.dungeon-master.com/forum/viewtopic.php?p=25551, https://aminet.net/package/game/hint/DungeonMSave, https://www.dungeon-master.com/forum/viewtopic.php?p=21531 | party opinions, the Aminet save, DMute with v3.6, 14 levels | 2026-11-20 (hosts themselves blocked) |
| The game disk (ROM text) | `strings` on the ADF | dialog texts (save, format, resume), creature, item, action and skill-level names | 2026-11-20 |
| Unavailable | dmweb.free.fr, dungeon-master.com, tcrf.net (403), gamefaqs.gamespot.com (403), strategywiki.org (403), mocagh.org, aminet.net, discmaster.textfiles.com, gamerwalkthroughs.com, web.archive.org | the DM Encyclopaedia, manual PDFs, cheats, maps | 2026-11-20 |

## Open questions
- A level warp: the game's own level-change routine or the stairs coordinates of each level (decode the level
  maps; candidate map bytes at C63A02). Until then deeper levels are played down by the stairs.
- Gando (the 24th champion) was not found in the explored hall.
- The eye (statistics) shows only while the button is held: can a shot catch it (`mouse1:N` releases before the
  frame is taken)? Try `AT..,mouse1:200,!` or a held-button token.
- LO FUL: cast and mana spent, but its light effect was not measured (the view was already lit by the torch).
- How long a torch lasts; the dungeon's light falloff on deeper levels.
