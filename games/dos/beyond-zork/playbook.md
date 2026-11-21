# Beyond Zork: The Coconut of Quendor (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Interpreter:** Infocom's own `BZORK.EXE` (start-menu entry 2), not the bundle's `.bat` (= Frotz 2.32).
  It runs correctly: colour prompt in 80x25 text mode, then the whole game in a **640x200 16-colour graphics
  mode** (8-pixel text rows; `play.py text` / `preview.py --text` do not work: look at sheets).
- **Start:** `@start` (Hilltop, preset character Frank Booth, Level 0 Male Peasant). Chain, all honest and
  reproducing from power-on (`cachecheck.py`: 11/11): `boot` (BEGIN/RESTORE/QUIT prompt) -> `title` (title card
  after the prologue) -> `setup` (Character Setup menu) -> `start` -> `cove` / `shillelagh` (driftwood taken and
  wielded at the Wharf) -> `vapor` (moors, an eldritch vapor attacks) -> `vapor_won` (Level 1) -> `saved1`
  (SAVE completed, disk file written); side branches `lighthouse`, `kitchen`.
- **Typing:** `GO:text` = `type:text\n,w200` (one command, answer drawn). Commas: `type:sailor,comma,type: hello\n`.
  `$` (CASH) types fine. Function keys F1-F10 are the game's command macros (F7 = ATTACK MONSTER). Waits: 200
  frames per command is enough everywhere seen; `w300` after BEGIN/the prologue pages.
- **Macros:** `BOOT`, `TITLE`, `SETUP`, `NEWGAME` (Bzork.exe); `FROTZ`, `FZSETUP`, `FZNEWGAME` (Frotz comparison);
  `GO:cmd`; `ATTRS:en:st:dx:iq:cm:lk` (sets current and maximum of the six attributes; verified on STATUS).
- **Saving:** `type:save\n,w200,enter,w300` -> "[SAVE completed.]" (default file `DATA\BEYONDZO.SAV`).
  RESTORE: at the opening prompt `type:restore\n,w200,enter,w300`, or in play the same. `play.py export`
  captures the file (`BEYOZORK/DATA/BEYONDZO.SAV` in the ZIP); `sav:02_first_fight,BOOT,type:restore\n,w200,enter,w300`
  verified. Not allowed during combat (manual).
- **Traps:** the moors south of the village are laid out at random: room names and the place of the first
  monster depend on everything typed before (the route is deterministic, so keep routes exact; a changed
  earlier command moves the vapor). Bandits in the Rusty Lantern refuse a fight ("Suicide"). The cook cannot be
  attacked. `play.py` reports "NOT settled" on every frame (blinking cursor): normal.
- **Shot plan:** `shots.txt` holds 33 previewed lines (opening area, menus, options, first fight, save, Frotz
  comparison) ready for `shoot.py dos/beyond-zork main --only ...`. The `start` set can use the honest chain
  as it is (list below).
- **Open:** death screen, a shop, a magic item (wand/scroll/potion) used, the lighthouse upper floors, other
  regions beyond the moors (no walkthrough host is reachable: see Sources), Endurance bar shot with NOTIFY.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Beyond Zork: The Coconut of Quendor (verified: title card and VERSION) |
| Platform / model used | IBM PC / MS-DOS, `svga-7800` (`game.json`); interpreter `BZORK.EXE` |
| Release (region, year) | US, 1987; story Release 57 / Serial Number 871221, "IBM/MS-DOS Color Version J" (VERSION, verified); interpreter file date 1996-06-22 (a later Activision re-release bundle); Frotz 2.32 (1997) and `Bzork.bat` added by whoever packed the folder |
| Developer / publisher | Infocom (Activision subsidiary); author Brian Moriarty (source: Wikipedia) |
| Genre | Parser interactive fiction with role-playing rules (attributes, levels, combat), auto-map |
| Players / save system | 1 player; SAVE to a named file (default `DATA\BEYONDZO.SAV`), RESTORE, UNDO (one move; not in combat) |
| Dump | `rom/beyond-zork.zip` (`beyond_zork/` folder: `Bzork.exe`, `Beyondzo.mg1`, `Data/Beyondzo.dat` = Z-machine v5 story, `Frotz.exe`, `Bzork.bat`) |

## Boot sequence
- Intake probe (`work/intake/dos/beyond-zork/sheet.png`): DOSBox Pure's start menu only. Its entries, in order:
  `BEYOZORK\BZORK.BAT`, `BZORK.EXE`, `FROTZ.EXE`, Go to Command Line (verified).
- **`BOOT`** = `w120,down,enter,w600,y,w300` (verified as one route): `BZORK.EXE` loads
  `data\beyondzo.dat` by itself (default path in the program), asks "Do you want color?" (80x25 text mode,
  640x400 frame), `y` -> 640x200 colour graphics, "Copyright (C)1987 Infocom ... Do you want to begin a new game,
  restore a saved game, or quit? [Type BEGIN, RESTORE or QUIT.] >". `n` gives a monochrome (grey on black)
  screen (verified, not used).
- **`TITLE`** = `BOOT,type:begin\n,w300,space,w200,space,w300`: two prologue pages (Y'Gael, the Guildmaster's
  council; first page ends with [MORE]) then the title card "B E Y O N D  Z O R K / The Coconut of Quendor / An
  Interactive Fantasy" (verified). There is no title picture in Bzork.exe.
- **`SETUP`** = `TITLE,space,w300`: Character Setup menu (verified).
- **`NEWGAME`** = `SETUP,enter,w300,space,w300`: "Begin using a preset character" -> "Press any key to begin
  the story" -> Hilltop, first `>` prompt (verified).
- **Why Bzork.exe:** it is Infocom's own PC interpreter and runs the game completely (graphics mode, map,
  menus, function keys, save/restore all verified). The bundle's `Bzork.bat` runs `frotz data\Beyondzo.dat`:
  Frotz 2.32 shows a title picture from `Beyondzo.mg1` (the Beyond Zork logo over rock pillars), then the same
  game in a 640x400 VGA mode, black background, red frames, a proportional font, and DOSBox's mouse pointer
  drawn over the screen. Comparison: plan lines `extra_frotz_title`, `extra_frotz_cove` (routes `FROTZ`,
  `FZNEWGAME,GO:e`). `FROTZ.EXE` alone prints its usage and quits.

## Controls
| Context | Key | Action | Status |
|---|---|---|---|
| Opening prompt | `type:begin\n` / `type:restore\n` | new game / load | verified |
| Prologue, title card | space | next page ([MORE]) | verified |
| Character Setup | up/down, enter | choose; presets list Lucky, Tank, Muscles, Nimble, Genius, Saint | verified |
| Random character | space / enter | roll a new set / accept | verified (frame) |
| Create your own | up/down attribute, left/right adjust, enter | spread 60% potential; then "Are you sure ... [Please type YES or NO.]" | verified (frames) |
| Play | typed command + enter | parser (`GO:...`) | verified |
| Play | F1 LOOK AROUND, F2 INVENTORY, F3 STATUS, F4 EXAMINE _, F5 TAKE _, F6 DROP _, F7 ATTACK MONSTER, F8 AGAIN, F9 UNDO, F10 OOPS _ | defaults; `_` = waits for the object | verified (all ten) |
| Play | DEFINE | function-key editor (Restore Defaults, Exit) | verified |
| Play | SETTINGS | Display Mode, Descriptions, Transcripting, Status Notify, Map View, Display Priority, Combat Monitor | verified |
| Play | MODE, ZOOM, COLOR (6 palettes), MONITOR, VERSION, `$` (cash) | display / info | verified |
| Play | keypad (kp6) | nothing (manual: keypad not supported on IBM PC) | verified |
| Play | up arrow | no command history | verified |
| Play | mouse on the map | source (manual); not tried | source |

Input timing: default press (hold 8, wait 40) works; `type:` strings are taken completely; 200 frames after
Enter is enough for any answer seen.

## Game structure
Prologue -> Character Setup -> Hilltop above a village by the Great Sea. Opening area (verified):
- Hilltop: E Cove, NW Edge of Storms (gray fields, billboard "WELCOME TO THE FIELDS OF FROTZEN"; going W is
  blocked by lightning).
- Cove (street): W Hilltop, E Wharf (old sailor painting a galleon; wait and TAKE DRIFTWOOD = shillelagh),
  S Outside Pub, NE Ledge.
- Outside Pub: OPEN DOOR, W The Rusty Lantern (bandits at the fireplace, bearskin rug), W again: Kitchen (a
  thrown rusty dagger sticks in the wall: TAKE DAGGER; skinny old cook, giant onion, closed door "Keepeth Out").
- Ledge: inscription riddle; SAY LIGHTNING blasts an opening; ENTER OPENING -> Lighthouse plateau, UP ->
  Lighthouse, 1st Level.
- S of Outside Pub: Moor's Edge, then the moors (random rooms: Mud Flats, Eyes, Deep Mist, Odors, Noises ...;
  monsters such as the eldritch vapor; a potion lying in the mud in some layouts).
Beyond that: not explored (source for the plot only: recover the Coconut from the Ur-Grues).

## Shot plan
33 lines in `shots.txt`, all previewed 2026-11-21 (`work/preview/dos/beyond-zork/plan.png`), category counts:
boot 1, menu 5, cutscene 1, title 1, gameplay 7 (`env_` 4), system 2, inventory 2, dialogue 2, battle 3, map 1,
options 3, save 2, extra 3. Still to add by the capture agent: gameover (death), shop, magic item used, the
lighthouse floors, more regions and monsters, NOTIFY messages, a NAME (weapon) use, UNDO.

`start` set (played honestly, power-on to the first save), routes from the chain: boot prompt (`@boot`),
prologue page (`@boot,type:begin\n,w300`), title card (`@title`), Character Setup (`@setup`), the story starts
(`@setup,enter,w300`), Hilltop (`@start`), STATUS F3 (`@start,f3,w200`), Cove (`@cove`), Wharf, driftwood,
`@shillelagh`, Outside Pub, Moor's Edge, the moors, `@vapor`, the fight (`@vapor,type:attack vapor\n,w200`,
then `f7,w200` twice), `@vapor_won`, STATUS, SAVE prompt, `@saved1`. Name its checkpoints `s_...` (copies of
these routes).

## Strategy and walkthrough notes
- First weapon: Wharf, `z` once, `take driftwood`, `wield shillelagh` (checkpoint `shillelagh`).
- First fight: from `@shillelagh` `w,s,s,s,e` meets an eldritch vapor at Noises; three or four attacks win
  (Level 1, Endurance 23). Other routes give other moor layouts.
- Lighthouse: Ledge riddle answer LIGHTNING.
- Do not attack the bandits (refused); the dagger in the kitchen is free.

## Naming
The preset character is named by the game (Frank Booth for the default preset). `name me ryz` is refused
("The word "ryz" isn't in the vocabulary"); NAME is for weapons and creatures, with vocabulary words only
(manual). No naming of the character found; Create your own character asks no name before play (not checked
to the end).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Attributes | `ATTRS:en:st:dx:iq:cm:lk` (current and maximum) | RAM, this run | verified (STATUS shows them) |
| UNDO | F9 / `GO:undo` (one move, not in combat) | manual | verified "[UNDO failed.]" at the start (nothing to undo) |
| Debug commands | none found | - | - |

### Saves (rom/saves/beyond-zork/, never committed)
None downloaded (no reachable host offers them). Own saves in `saves/` (README there): `01_start` (Hilltop),
`02_first_fight` (Noises after the vapor; RESTORE from the opening prompt verified).

## RAM map (for `game.json` "ram" watches and pokes)
The Z-machine's memory starts at physical `0CDB0` (story header found there: version 5, serial 871221).
Bzork.exe keeps words **little-endian** (byte-swapped story).
| Address | Size | Meaning | How found |
|---|---|---|---|
| 0CDB0 | - | Z-machine address 0 (header); globals at Z 02B6 = `0D066` | story header search |
| 1454A | 2 LE | Endurance (current), then 1454C ST, 1454E DX, 14550 IQ, 14552 CM, 14554 LK, 14556 AC | search for 23,8,8,8,1,25; pokes shown on STATUS |
| 14558 | 2 LE | 9 after the first fight (experience? not confirmed) | diff |
| 1455A | 2 LE | maximum Endurance, then 1455C... the other maxima in the same order | poke |

## Emulation notes
- Model `svga-7800` (intake default) works; no reason to change.
- Every frame reports "NOT settled": the block cursor blinks. Routes end with fixed waits.
- Randomness: the start is deterministic from power-on: the default preset is always Frank Booth; the random
  character roll gave the same set with and without 77 extra frames before it, so the interpreter's random
  seed does not follow frame timing at that point; the moors layout follows the commands typed (same route,
  same layout).
- `play.py text` fails (graphics mode).

## Checkpoints
See `checkpoints.txt`; all 11 reproduce (`python3 tools/cachecheck.py dos/beyond-zork`, 2026-11-21), `saved1`
also with the same save file on disk.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Beyond_Zork | releases (R57 = 1987-12-21), author, platforms | 2026-11-21 |
| Manual, archive.org full text | https://archive.org/stream/vgmuseum_infocom_beyondzork-manual/beyondzork-manual_djvu.txt | special commands, function keys, combat, SAVE/UNDO limits, keypad not on IBM | 2026-11-21 |
| Manual PDF | https://archive.org/download/vgmuseum_infocom_beyondzork-manual/beyondzork-manual.pdf | unavailable: redirect to an archive.org storage host refused by the proxy (403) | 2026-11-21 |
| GameFAQs | https://gamefaqs.gamespot.com/pc/564510-beyond-zork-the-coconut-of-quendor/faqs | unavailable (403) | 2026-11-21 |
| Walkthroughs (cyberly.org, the-spoiler.com, walkthroughking.com, ifarchive solutions) | search results only | not fetched: hosts not on the approved list (ask the coordinator) | 2026-11-21 |

## Open questions
- Death screen and its options (RESTART/RESTORE/QUIT?): no safe death found in the opening area.
- Shops (the manual mentions CASH; you start with 1 zorkmid): where is the first one?
- What 14558 counts (experience?); where the level is stored.
- Create your own character: does it end with a name prompt?
- Mouse on the map (manual): not tried; DOSBox Pure mouse tokens exist.
