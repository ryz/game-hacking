# Beyond Zork: The Coconut of Quendor (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Interpreter:** Infocom's own `BZORK.EXE` (start-menu entry 2), not the bundle's `.bat` (= Frotz 2.32).
  It runs correctly: colour prompt in 80x25 text mode, then the whole game in a **640x200 16-colour graphics
  mode** (8-pixel text rows; `play.py text` / `preview.py --text` do not work: look at sheets).
- **Aspect (owner's rule 2026-11-21):** `game.json` "aspect": "rowdouble": every tool writes the 640x200 frames as
  640x400 (each row twice). Colours: COLOR cycles palettes 1-6, and N at "Do you want color?" gives monochrome,
  grey on black (`options_monochrome`).
- **Look (owner's decision 2026-11-21): palette 6, black on light grey, in every Bzork.exe shot.** `BOOT` sets it
  with two pokes, so every route and checkpoint inherits it: `GREYPC` (`poke:9A37=00,poke:9A38=07`, at the colour
  question before `y`: Bzork.exe's own default text/background colours, EGA numbers, normally 07 on 01 = grey on
  blue; this makes even the opening prompt grey) and `GREY` (after the opening prompt: the game globals FORE
  `0D06C`=2, INCOLOR `0D0EA`=2, BGND `0D14C`=9, GCOLOR `0D1D4`=2, words big-endian = exactly what COLOR palette 6
  writes; PALLETTE `0D122` stays 1). A display palette is a presentation setting, not a game value (owner), so
  `start` uses it too. Proven harmless: every old shot recoloured blue->grey, grey->black equals its retake
  pixel for pixel (routes, random moors, fights unchanged). `BOOTBLUE` = the original boot (white on blue,
  `options_color_default`). With `GREYPC` palette 1 (all colours "default") is grey too; palette 2 is the
  explicit white on blue. Palette table in the story: IBM entry `0xD416` (6 pointers to BGND/FORE/INCOLOR/GCOLOR
  byte records: p1 1,1,1,1; p2 6,9,9,9; p3 6,9,9,4; p4 2,9,8,3; p5 2,9,9,9; p6 9,2,2,2); the story is loaded and
  STARTUP has run within one frame after `y`, so the table cannot be poked before STARTUP.
- **Start:** `@start` (Hilltop, preset character Frank Booth, Level 0 Male Peasant). Chain, all honest and
  reproducing from power-on (`cachecheck.py`: 11/11): `boot` (BEGIN/RESTORE/QUIT prompt) -> `title` (title card
  after the prologue) -> `setup` (Character Setup menu) -> `start` -> `cove` / `shillelagh` (driftwood taken and
  wielded at the Wharf) -> `vapor` (moors, an eldritch vapor attacks) -> `vapor_won` (Level 1) -> `saved1`
  (SAVE completed, disk file written); side branches `lighthouse`, `kitchen`.
- **Typing:** `GO:text` = `type:text\n,w200` (one command, answer drawn). Commas: `type:sailor,comma,type: hello\n`.
  `$` (CASH) types fine. Function keys F1-F10 are the game's command macros (F7 = ATTACK MONSTER). Waits: 200
  frames per command is enough everywhere seen; `w300` after BEGIN/the prologue pages.
- **Macros:** `BOOT` (grey, see Look), `BOOTBLUE`, `GREYPC`, `GREY`, `TITLE`, `SETUP`, `NEWGAME` (Bzork.exe); `FROTZ`, `FZSETUP`, `FZNEWGAME` (Frotz comparison);
  `GO:cmd`; `ATTRS:en:st:dx:iq:cm:lk` (sets current and maximum of the six attributes; verified on STATUS).
- **Saving:** `type:save\n,w200,enter,w300` -> "[SAVE completed.]" (default file `DATA\BEYONDZO.SAV`).
  RESTORE: at the opening prompt `type:restore\n,w200,enter,w300`, or in play the same. `play.py export`
  captures the file (`BEYOZORK/DATA/BEYONDZO.SAV` in the ZIP); `sav:02_first_fight,BOOT,type:restore\n,w200,enter,w300`
  verified. Not allowed during combat (manual).
- **Traps:** the moors south of the village are laid out at random: room names and the place of the first
  monster depend on everything typed before (the route is deterministic, so keep routes exact; a changed
  earlier command moves the vapor). Bandits in the Rusty Lantern refuse a fight ("Suicide"). The cook cannot be
  attacked. `play.py` reports "NOT settled" on every frame (blinking cursor): normal.
- **Sets (2026-11-21, retaken in palette 6):** `main` 100 shots (13 of them Frotz) and `start` 34, verified from an empty cache, published;
  `games/dos/beyond-zork/shots.txt` holds the main lines. Checkpoints `s_*` = the start chain, `m_*` = main:
  `m_ratant` (Level 0 losing to the rat-ant), `m_cellar`/`m_darkness` (strong character in the Wine Cellar /
  the dark beyond it), `m_odors` (moors, strong), `m_mizniaport`, `m_boutique` (shop), `m_ryz` (created
  character Ryz on the Hilltop).
- **Money:** `MONEY:n` macro (zorkmids at `0D20C`, 2 bytes **big-endian**: object data is not byte-swapped,
  unlike the attribute block). `ATTRS:47:31:28:22:14:29` is the strong character used in `main`.
- **Way to the seaport:** from `@vapor_won` `sw` (Odors, gray potion), `sw` (Gasses, rumpled scroll), `sw`
  (Bluffs), `w` = Mizniaport. Boutique: `open door`, `n`. Gurth City: Mizniaport `nw` (Intersection), `n`.
- **Traps (new):** going `u` from the Wine Cellar locks you in ("an unseen hand slams the cellar door"); moving
  on in the Darkness can kill (grue). A Level 0 peasant dies to the rat-ant (`m_ratant` + five F7). Scroll
  words are random per route. `tools/gamestable.py` rewrites README.md/docs/status.md: leave that to the
  coordinator.
- **Open:** Level 2 (37 experience still Level 1), the cellar after the lock (light? the cook wants the old
  bottle of wine for the giant onion), lighthouse upper floors (1st Level has no stairs up in daylight),
  Fields of Frotzen past the lightning, the Skyway ride, Gurth City beyond the South Market, potion and scroll
  effects (USE SCROLL: "How do you intend to do it?").

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
- **`BOOT`** = `w120,down,enter,w600,GREYPC,y,w300,GREY` (until 2026-11-21 without the two palette pokes, now `BOOTBLUE`; verified as one route): `BZORK.EXE` loads
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
  drawn over the screen. Comparison: 13 shots `extra_frotz_*` in `main` (2026-11-21; routes from `FROTZ`,
  `FZSETUP`, `FZNEWGAME`; verified: F2/F3 function keys, DEFINE, SETTINGS, COLOR = 4 palettes, Alt-H = Frotz's
  hot key help (Alt-D/H/N/P/R/S/U/X), the moors differ from Bzork.exe: `FZNEWGAME,GO:e,GO:e,GO:z,GO:take
  driftwood,GO:wield shillelagh,GO:w,GO:s,GO:s,GO:s,GO:e` = Gasses with the vapor). What Frotz draws differently:
  `design/interface.md`, "Frotz 2.32 compared". The palette pokes are for Bzork.exe only (Frotz keeps its look). `FROTZ.EXE` alone prints its usage and quits.

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
| Play | MODE, ZOOM, COLOR (6 palettes; 4 under Frotz), MONITOR, VERSION, `$` (cash) | display / info | verified |
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
Done 2026-11-21: `main` 87 (battle 9, boot 1, cutscene 1, dialogue 7, extra 4, gameover 2, gameplay 20 (env_ 10),
inventory 7, map 1, menu 11, options 9, save 3, shop 5, system 6, title 1)
and `start` 34 (power-on to the first SAVE, all honest, checkpoints `s_*`). Scout lines all kept (captions
fixed where the frame said otherwise). Still wanted: Level 2, a magic item with a visible effect, the
lighthouse floors, the Skyway ride, Gurth City, the cellar puzzle solved (wine for the onion).

## Strategy and walkthrough notes
- Moors from `@vapor_won` (layout of this route): Noises; `w` Deep Mist (guttersnipe); `sw` Odors (gray potion,
  guttersnipe); from Odors `se` Eyes, `se`,`e` Mud Flats (wounded pterodactyl, whistle, stave), `sw` Gasses
  (rumpled scroll, word Macuga), `sw` Bluffs, `w` Mizniaport. Mizniaport: `ne` Private Way, `n` Stablehouse
  (unicorn, saddle, horseshoe); `w` Skyway Entrance (gondola; `enter gondola`: "Wait yer turn"); `nw`
  Intersection, `n` South Market of Gurth City (hawker, fish cake); `s`/`sw`/`se` "You'd fall in the bay".
- Kitchen: `open door` (cellar door) makes the cook ask for the old bottle of wine downstairs in exchange for
  the giant onion; `d` Wine Cellar (rat-ant, crinkly scroll); `n` Darkness; `u` locks you in.
- First weapon: Wharf, `z` once, `take driftwood`, `wield shillelagh` (checkpoint `shillelagh`).
- First fight: from `@shillelagh` `w,s,s,s,e` meets an eldritch vapor at Noises; three or four attacks win
  (Level 1, Endurance 23). Other routes give other moor layouts.
- Lighthouse: Ledge riddle answer LIGHTNING.
- Do not attack the bandits (refused); the dagger in the kitchen is free.

## Naming
The preset character is named by the game (Frank Booth for the default preset). `name me ryz` is refused
("The word "ryz" isn't in the vocabulary"); NAME is for weapons and creatures, with vocabulary words only
(manual). ~~Create your own character asks no name before play~~: it does (verified 2026-11-21): after the
attributes, YES, then "Shall your character be male or female?", then "By what Name shall your character be
known?" (any text: `ryz` becomes "Ryz"), YES, "Are you sure Ryz is the character you want?" YES, "Do you want
to save this character before you proceed?" NO, any key -> Hilltop (checkpoint `m_ryz`). The sets use the
preset Frank Booth because the whole chain (moors layout) was built on it; Ryz appears in the creation shots.

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
| 14558 | 2 LE | experience: 0 at the start, 9 after the vapor (Level 1), 16 after a guttersnipe; poked to 37 still Level 1 | diff, preview --peek |
| 0D20C | 2 BE | zorkmids (`MONEY:n`); found by selling a scroll (1 -> 6) | find |
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
- ~~Death screen~~: found 2026-11-21 (rat-ant at Level 0: RESTORE/RESTART/QUIT; grue: also UNDO).
- ~~Shops~~: the Boutique in Mizniaport (cloak 30 zorkmids; sells a scroll for 5).
- Where the level is stored and what Level 2 needs (14558 is experience).
- ~~Create your own: name prompt~~: yes (see Naming).
- Mouse on the map (manual): not tried; DOSBox Pure mouse tokens exist.
