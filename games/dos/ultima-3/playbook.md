# Ultima III: Exodus (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"ROM text" = read from EXODUS.BIN / BOOTUP.BIN or the map files; "code" = read from EXODUS.BIN with ndisasm.
EXODUS.BIN is loaded at CS = DS = 0198, offset 0x100 (a COM image): **physical address = 0x1980 + DS offset =
0x1A80 + file offset**; code offsets below are DS/IP offsets (`ndisasm -b16 -o 0x100 EXODUS.BIN`).

> **Tools moved (2026-11-20).** Where this playbook says `try.py`, `cachecheck.py` or `screen.py` (copies that
> lived in this game's `tools/`), use the shared tools: `python3 tools/preview.py dos/ultima-3 FILE` (`--frames K` is now
> a `?` mark inside the route or `--timeline N:STEP`; sheets in `work/preview/dos/ultima-3/`), `python3
> tools/cachecheck.py dos/ultima-3` (`--after TOKENS` for a save in the game, `--peek ADDR:LEN` for party tables) and
> `python3 tools/play.py text` / `preview.py --text` for text screens. Pictures are native size
> (`play.py shot --scale N` on demand).

## Read first
- Start: `python3 tools/play.py start ultima-3 --name ultima-3 --route @start` (new party on Sosaria) or `@hero` (late
  party by poke). Menus: letter + Enter. Sets: `main` (260, everything) and `start` (60, played honestly to the first save).
- Macros that matter: `NEWGAME`/`PARTY` (honest creation), `POS`, `ENTER`, `SHOP`, `HERO`, `MON`, `FOE`; routes in
  game.json. Checkpoints: `start`, `towne`, `castle`, `hero`, the endgame chain; the honest chain `s_*` (Start set).
- Traps: the play screen never settles (idle Pass every 5 s): use `do!` / `w`N, previews say "NOT settled", that is normal.
  Shops end with `q,w30,enter` (Q or Esc at "Your interest?"); Enter alone repeats the question.
  Walking in towns: BFS over the town file (tiles 04 grass, 08 brush, 0C forest, 20 floor are walkable), then fix the
  last steps by the position watch (wandering people block a square now and then).
  A new game has no monsters on Sosaria; they spawn ~1 in 19 turns and walk in (Start set below).
- Open: party hit/damage formulas, monster hit points per kind, starvation, which of a monster's two names a fight uses.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Ultima III: Exodus; title screen "Exodus / Ultima III / by Lord British / Copyright (C) 1983 Origin Systems"; menu "(C)-1983 By James R. Van Artsdalen and Lord British" (the PC port's programmer) (verified) |
| Platform / model used | IBM PC / MS-DOS, CGA 320x200 4 colours (black, cyan, magenta, grey) everywhere, no text mode; `game.json` model `svga-300` (see Emulation notes) (verified) |
| Release (region, year) | Apple II 1983; IBM PC 1983 (CGA, PC speaker, no music; built for a 4.77 MHz PC) (source: Wikipedia). This dump: GOG's release, folder `Ultima III/`, 51 files, one program ULTIMA.COM (loads BOOTUP.BIN for the menus, EXODUS.BIN for play); SHA-1 in `game.json` |
| Developer / publisher | Origin Systems; design Richard Garriott (Lord British) (source: Wikipedia); PC port by James R. Van Artsdalen (ROM text) |
| Genre | Party RPG: four characters move as one icon on a top-down 64x64 world (Sosaria) with towns and castles, a separate tactical combat screen, first-person dungeons of 8 levels, ships, moongates, a hidden second land (Ambrosia) |
| Players / save system | 1 player, roster of up to 20 characters, party of 1-4. **Q (Quit & Save) on the Sosaria map** writes PARTY.ULT + SOSARIA.ULT and play goes on ("00000008 moves / Please wait..."); entering a town, castle, dungeon or Ambrosia writes them too. Q in Ambrosia writes nothing (verified, `tools/cachecheck.py`) |

## Boot sequence
All macros are in `game.json`; every checkpoint was rebuilt from power-on in single runs (`tools/cachecheck.py`).
- Power-on starts ULTIMA.COM directly (one program, no DOSBox Pure menu). GOG's autoexec only runs `ultima.com`
  (`cycles=300`, `machine=svga_s3`, `core=simple`); its cloud-saves overlay mount is not reproduced.
- **Title** (verified, `work/scout/ultima-3/try_boot.png`): "Exodus" drawn line by line (f300), "Ultima III" (f900),
  "by Lord British / Copyright (C) 1983 Origin Systems" (f1800); a party of figures and a dragon walk along the
  bottom border. `TITLE` = `w2400` (checkpoint `title`). From about f2600 the lower half becomes the **attract
  demo**: a strip of the Sosaria map ("Ultima III") with ships, figures and monsters moving, "Press <Space>"
  (the moves come from DEMO.ULT/MOVES.ULT). Space is ignored while the title is still drawing (at f2400).
- **Main menu** (`MENU` = `w3000,space,w300`, checkpoint `menu`): "From the depths of hell... ...he comes for
  VENGEANCE!", "Option:" with Return to the View / Organize a Party / Journey Onward. **Every menu choice is a
  letter + Enter** (`o,w60,enter`); the letter alone only echoes the word.
- **Organize a Party** (`ORGANIZE`): Examine the Register / Create a Character / Form the Party / Disperse the
  Party / Terminate a Character / Look at a Character / Main Menu (letter + Enter).
- **Create** (`C_RYZ` etc.): "Entry#" two digits or one digit + Enter (1-20); then a form "Entry#01 Points:50":
  Name (typed, lower case kept, Enter), Sex M/F/O + Enter, Race H/E/D/B/F + Enter (Human, Elf, Dwarf, Bobbit,
  Fuzzy), Type F/C/W/T/P/L/B/D/I/A/R + Enter (Fighter, Cleric, Wizard, Thief, Paladin, Lark, Barbarian, Druid,
  Illusionist, Alchemist, Ranger), Strength, Dexterity, Intelligence, Wisdom as two digits + Enter each (50
  points), "O.K.?" `y` + Enter, then "Press <Space>". New characters start with 150 H.P., 150 food, 150 gold, a
  dagger and cloth (verified, Ztats). One key per token works at 300 cycles (no `type:` needed).
- **Party used here** (verified, Register "01- MHPG ryz" ...): 1 ryz Male Human Paladin (Str 20 Dex 10 Int 05
  Wis 15), 2 condi Female Elf Wizard (05/15/25/05), 3 ebo Male Dwarf Fighter (25/15/05/05), 4 cubi Female Bobbit
  Cleric (10/10/05/25). `FORM` = Form the Party, Player-1..4 = 1..4 (digit + Enter), "(Formed)", space.
  `PARTY` = `ORGANIZE,C_RYZ,C_CONDI,C_EBO,C_CUBI,FORM,m,w60,enter,w300` (checkpoint `party`).
- **Journey Onward** (`JOURNEY` = `j,w60,enter,w600`): the play screen; `NEWGAME` = `MENU,PARTY,JOURNEY`
  (checkpoint `start`): the party on the Sosaria map at **(2C,14)**, Lord British's castle at (2D,12) and the
  towne LCB at (2E,13) just north-east, moons "(0)(0)", each character H:0150 F:0149 L:01 (verified).
- Saved game: `sav:01_start,MENU,JOURNEY` resumes where Quit & Save was used (verified for 01_start, 02_endgame).

## Controls
One key per command on the play screen; the command echoes in the message area (bottom right) and asks for a
player number (1-4) and/or a direction (arrow key) where needed. Verified 2026-11-19 from `start`/`hero` unless
noted (sheets `work/scout/ultima-3/try_t5.png`, `try_t2.png`, `try_t4.png`).
| Context | Key | Action | Status |
|---|---|---|---|
| Sosaria, towns | arrows | move North/South/East/West; "Invalid Move!" on water, mountains, walls | verified |
| | (no key) | after 5 seconds of the PC clock the game passes a turn by itself ("Pass") | verified (code 0x1B82: DOS time) |
| | `space` | Pass | verified |
| | `a` | Attack + direction: a monster or person beside the party starts a combat ("---Conflict!!--- ->Orcs") | verified |
| | `b` | Board a horse or frigate standing on the square | code (0x1D01) |
| | `c` | Cast: "Cast by whom-" player, then "Cleric spell-" / "Wizard spell-" letter (Paladin ryz casts cleric spells, condi wizard ones) | prompt verified |
| | `d` / `k` | Descend / Klimb: "Descend<-What?" outside dungeons | verified (refusal) |
| | `e` | Enter the towne, castle or dungeon under the party ("Enter Castle! Please wait..."); "Enter <-What?" elsewhere | verified |
| | `f` | Fire the frigate's cannons + direction ("Fire Direct-East") | prompt verified |
| | `g` | Get Chest: "Plr to search-" player ("Not Here!" without a chest) | prompt verified |
| | `h` | Hand Equipment: From Player, To Player, item | prompt verified |
| | `i` | Ignite a torch: "Whose torch:" player (dungeons) | verified |
| | `j` | Join gold to: player (all gold to one character) | prompt verified |
| | `l` | Look + direction ("Look-North ->Grass") | verified |
| | `m` | Modify order: two players swap places ("Exchanged!") | verified |
| | `n` | Negate Time: "Whose Powd?" (uses a powder) | prompt verified |
| | `o` | Other command: "Whose action?" player, "Cmd:" a word + Enter: INSERT, DIG, SEARCH, BRIBE, PRAY (one key per letter) | verified (all five) |
| | `p` | Peer at gem: "Whose gem?" player: a miniature map of the whole land | verified |
| | `q` | Quit & Save (Sosaria map only), play continues | verified |
| | `r` | Ready weapon for # player, weapon letter | prompt verified |
| | `s` | Steal Chest + direction | prompt verified |
| | `t` | Transact: "Who will Transact?" player, direction: people talk, merchants over a counter open a shop, Lord British raises levels | verified |
| | `u` | Unlock + direction (keys) | prompt verified |
| | `v` | Volume (sound on/off: "Volume Off!") | verified |
| | `w` | Wear armour for # player, armour letter | prompt verified |
| | `x` | X-it the horse or frigate ("X-it Craft") | verified |
| | `y` | Yell: "Yell, whom?" player, "Word:" + Enter (EVOCARE at the Silver Snake) | verified |
| | `z` | Ztats for # player: one line per key press in the message area (name, Str, Dex, Int, Wis, H.P., H.M., Gold, Exp., Gems, Keys, Powd, Trch, cards and marks, Weapon, Armour, \*\*\*Weapons\*\*\* list, \*\*Armour\*\* list) | verified |
| Dungeons | `up` Advance, `down` Retreat, `left`/`right` Turn; `k`/`d` ladders; `i` torch ("It's dark!" without); A/B/E/F/L/Q/T/U/X/S: "Not a DNG cmd!" | | up, i verified; table from code 0x7708 |
| Combat | arrows move the active player; `a` + direction attacks; `c` casts; `r` readies; `space` passes; "----Player 1----" names whose turn it is | | move, attack verified |
| Prompts | player numbers 1-4; letters + Enter (menus, shop letters, card letters D/S/L/M) | | verified |

Input timing: the default press (hold 8, wait 40) works everywhere at 300 cycles. Town and dungeon entry need
`w300` ("Please wait..."); the whirlpool to Ambrosia `w300`; the ending text appears within `w600` after the
last card. Menus and prompts: letter, `w30`-`w60`, Enter.

## Game structure
Facts from the code and the map files, checked in play where marked (tools: `work/scout/ultima-3/tmap.py` prints
a map file).
- **Sosaria** (SOSARIA.ULT, 64x64, wraps): places by the Enter table (code DS:0x16E1, file DS:0x16BB):
  | Place | Square | File | Kind |
  |---|---|---|---|
  | Lord British's castle | (2D,12) | BRITISH.ULT | castle (enter at (20,3E)) |
  | Castle Exodus (the Castle of Fire, on the Isle of Fire) | (0A,35) | EXODUS.ULT | castle |
  | LCB (the towne beside the castle) | (2E,13) | LCB.ULT | towne (enter at (01,20)) |
  | Moon | (06,0D) | MOON.ULT | towne |
  | Yew | (22,10) | YEW.ULT | towne |
  | Montor East / Montor West | (31,3A) / (2F,3A) | MONTOR_E/W.ULT | townes |
  | Grey | (07,2C) | GREY.ULT | towne |
  | Dawn (only while it shows) | (25,35) | DAWN.ULT | towne |
  | Devil Guard | (12,1F) | DEVIL.ULT | towne |
  | Fawn | (1E,02) | FAWN.ULT | towne |
  | Death Gulch | (38,1F) | DEATH.ULT | towne |
  | Dungeon of Doom ("Welcome fools to your doom!!") | (13,39) | M.ULT | dungeon (enter at (1,1), level 1, facing east) |
  | Dungeon of Fire ("Beware the fires of hell!"), inside a lava ring | (31,22) | FIRE.ULT | dungeon |
  | Time dungeon ("Time awaits!"), walled in by mountains | (3A,1E) | TIME.ULT | dungeon |
  | Snake dungeon ("Clues to follow!"; name from the usual list, not shown in the game) | (3A,2C) | P.ULT | dungeon |
  | Perinian Depths | (38,06) | PERINIAN.ULT | dungeon |
  | Mines of Morinia | (09,1C) | MINE.ULT | dungeon |
  | Dardin's Pit | (2E,07) | DARDIN.ULT | dungeon |
  Dungeon names are the level-1 messages (ROM text); the Snake dungeon's name is (source) memory of the series.
- **Moons and moongates** (code 0x20AE, verified): two moons shown "(a)(b)" at the top; the first changes every 12
  turns, the second every 4. When the second changes, the gate moves to the square of the first moon's phase and
  leads to the square of the second moon's phase: 0 (08,08), 1 (39,2E), 2 (0F,1B), 3 (24,3A), 4 (0F,1D),
  5 (0C,37), 6 (1F,1F), 7 (3A,1F). Phase 7's square is the only way to the Time dungeon (verified `moongate`,
  `time`). **Dawn** appears at (25,35) in the Dark Forest when both moons were at phase 7 ("new") and vanishes
  when both were 0 (code; verified `dawn`). Lord British's hint: "West 8, South 35 and await Dawn!".
- **Wind** (code 0x5678, 4412 = DS:2A92): changes every 25 turns to calm (1 in 9) or North/East/South/West;
  a frigate cannot sail toward the side the wind is named after ("Invalid Move!" east into an East Wind,
  verified `system_wind`) and **cannot move at all in a calm** (code 0x7233). ~~`SHIP` calms it for 25 turns~~
  (capture 2026-11-19): `SHIP` sets the wind to calm, which blocks sailing; in practice the wind changed again
  within one or two passes after `SHIP`, which is why the scout's routes work. For a fixed wind poke 4412 right
  before the move (`poke:4412=03` = South Wind lets the frigate sail east).
- **Whirlpool**: a moving whirlpool on the sea; sailing (or standing) on it: "A huge swirling --WhirlPool--
  engulfs you and your ship dragging both to a watery grave! ... You awaken on the shores of a forgotten Land.
  Your ship and crew lost to the sea!" -> **Ambrosia** (AMBROSIA.ULT, 64x64), at (20,36), on foot. Ambrosia's
  own whirlpool at (21,3A) leads back to Sosaria in a frigate (code 0x2168, verified one way).
- **Ambrosia's four shrines** (code 0x6366, verified `shrine`): Enter on a shrine square, "Who enters?" player:
  "Welcome to the Shrine of ...", "Offering*100-": each 100 gold raises that statistic by 1 up to the race
  limit ("Shazam!"; "You can't cheat the Gods!" if the gold is short; "Then be off!" for 0). Strength (04,24),
  Dexterity (2D,34), Intelligence (06,06), Wisdom (37,1B) (statistic = x mod 4).
- **Cards** (code 0x7607, verified `card` and all four): Other SEARCH while standing on a shrine square: "A card,
  with strange marks!": Love at (04,24), Sol at (2D,34), Moons at (06,06), Death at (37,1B) (card = x mod 4),
  to the searching character only.
- **Marks** (code 0x9550, verified `rod`): a dungeon square "A red hot rod in the wall. Who will touch?": the
  player gets the mark (by x mod 4 of the square: Force, Fire, Snake, Kings), takes damage ("It left a mark!").
  Rods: Force: Dungeon of Fire level 8 (4,A), Doom level 8 (8,9); Fire: Fire level 8 (5,E), Mines level 8 (D,F),
  Perinian level 8 (5,5); Snake: Snake dungeon level 8 (6,F) only; Kings: Dardin's Pit level 2 (B,3) and level
  8 (3,3), Mines level 3 (3,5) and 8 (3,9), Perinian level 1 (F,B) (B,F) and 8 (B,B), Snake level 8 (F,F), Time
  level 2 (7,7) and 8 (F,B) (B,F) (from the dungeon files). Uses: Force = walk through force fields, Fire =
  walk on lava (each party member must have it, else damage), Snake = EVOCARE works, Kings = Lord British raises
  past level 5.
- **Lord British** (code 0x807B, verified `lordbritish`): Transact: "Welcome my child" then "Experience more!"
  (experience hundreds below max H.P. hundreds), "Thou art greater" (+100 max H.P.), "Seek ye, the Mark of
  Kings!" (at 500 max H.P. without the mark), "No more!" at 2500.
- **Time Lord** (verified `timelord`): Time dungeon level 8 (1,1): the TIME picture and "You see a vision of the
  Time Lord / He tells you / The one way is / Love, Sol, Moons & Death, / All else fails."
- **Exodus** (verified to the end, `exodus`, `exodus_slots`, `ending`):
  1. The Silver Snake blocks the strait at (0A,39)-(0A,3A). In a frigate at (0A,3B) (or (0A,38)), a character
     with the Mark of Snake yells EVOCARE ("y", player, `e,v,o,c,a,r,e`, Enter): the party moves to the other
     side (code 0x7458); without the mark "No effect!" (verified). The word: PRAY in Yew's Circle of Light at
     (30,30): "Yell 'Evocare'" (verified `try_t2.png`).
  2. Sail north to (0A,36), X-it, walk onto the castle (0A,35), Enter: Castle Exodus at (20,3E).
  3. Inside (EXODUS.ULT): lava and force fields in the corridors (marks), daemons, balrons, dragons, guards,
     two pinchers; four invisible "Floor" creatures at (1F-20,0D-0E) attack in front of the slots
     ("->Floor", verified). Exodus is the row of four slots at (1E-21,0B).
  4. INSERT (Other command), direction North, card letter D/S/L/M + Enter, from (1E,0C), (1F,0C), (20,0C),
     (21,0C) in this order: Love, Sol, Moons, Death. Each correct card makes its slot vanish; a wrong card or slot
     hurts the inserter (code 0x76C9). After the fourth (code 0xA4B9): the castle flashes, "Congratulations! Thou
     hast compleated Exodus: Ultima 3 in 00048xxx moves Report thy feat!" and in the map area "And so it came to
     pass that on this day EXODUS, hell-born incarnate of evil, was vanquished from Sosaria. What now lies ahead
     in the ULTIMA saga can only be pure speculation! Onward to ULTIMA IV!" The game stays there.
- **Exotics** (code 0x7534, verified): Other DIG on the islet square (21,03): "Exotics!" = one Exotic weapon to
  the digger; at (13,2C): one Exotic armour. Dawn's people: "<Dig> on isles", "<Dig> up Exotics".
- **Shops** (code 0x7FC6, verified for pub, weapons, horses, oracle, guild): Transact over a counter (letter
  tiles) with a merchant behind it; the kind follows the party's row (y mod 8): 0 pub ("Here, friend, have a
  drink! It costs 7 g.p."), 1 grocer (rations 1 g.p.), 2 clerical healing (curing 100, healing 200, resurrection
  500, recalling 900), 3 weapons, 4 armour, 5 Guild (keys 50, torches 6, powders 90, gems 75), 6 Radrion,
  Prophet of Life (offering per 100 gold, a long rhyme of hints), 7 Equine Emporium (horses). Where (party
  square, then `t`, player, direction):
  | Shop | Towne (square) |
  |---|---|
  | pub | LCB (11,10) up; Moon (2D,10) up; Grey (27,18) up |
  | grocer | LCB (30,31) down; Yew (1F,11) up |
  | healer | Lord British's castle (2E,1A) up; Dawn (15,2A) down |
  | weapons | LCB (27,13) up; Montor East (1A,0B) up |
  | armour | LCB (32,14) up; Montor West (33,1C) up |
  | Guild | Grey (21,15) up; Fawn (20,0D) up |
  | oracle | Lord British's castle (14,2E) up; Dawn (24,2E) down |
  | horses | Devil Guard (0B,0F) up; Dawn (28,17) up |
  Weapon prices (ROM text): Dagger 5, Mace 30, Sling 60, Axe 125, Bow 350, Sword 200, 2H Swd 250, +2 Axe 400,
  +2 Bow 1050, +2 Swd 800, Gloves 1200, +4 Axe 2700, +4 Bow 6550, +4 Swd 4550. Armour: Cloth 75, Leather 195,
  Chain 575, Plate 2500, +2 Chain 6130, +2 Plate 8250.
- **Dungeons** (8 levels of 16x16, wrap around; files DUNGEON-name.ULT: 8 x 256 bytes + level messages): squares
  wall, door, secret door, ladder up/down, chest, and specials: fountains by x mod 4 (verified in play: 0 poison
  "Yuck! Horrible!", 1 heal "How wonderful!", 2 hurt "Argh! Blah! Yuk!", 3 cure "Ah! That's nice!"), strange wind (torch out), traps, gremlins (eat food), misty writing (the level's message),
  rods (marks), the Time Lord. Empty squares can spawn a fight that leaves a chest. "LVL:0n" and "Head--East"
  frame the view (verified).
- **Combat** (verified `fight`): a separate 11x11 field (one of nine CNFLCT_x.ULT layouts; which one per terrain is open), the party at the bottom,
  monsters at the top; each player in turn, then the monsters; "Killed! Exp.+03", "\*\*\*\*Victory!\*\*\*\*", a
  chest left on the map square. Monsters on Sosaria are visible map objects that walk towards the party.
- **Death**: a character with status D; when all four are dead or out: "All Players Out!" and the game stops
  there (verified with a poke).
- **Talk** (Transact with a person, town files' message tables; ROM text): e.g. LCB "Quest ye unto Lost
  Ambrosia!", "Exodus lies beyond the Silver Snake!", "`Dawn' comes each new pair!"; Lord British's castle
  "West 8, South 35 and await Dawn!", "The Wise Cleric: 4 cards, 4 slots"; Montor West "Seek the Jester in castle
  Fire!"; Yew "Search and ye shall find!"; Fawn "<Pray> in the Circle of Light!"; Death Gulch "Exodus is four as
  one!"; Devil Guard "Hot metal leaves a `Mark'!". Full lists in design/content.md.

## Shot plan
**Captured 2026-11-19: set `main`, 260 shots in game order, every line in `shots.txt` (the plan below is done;
not captured: see Capture notes).** The scout's plan, for reference:
Planned main set: about 120 shots in game order; plan lines with routes are in `shots.txt` (comments: the route
to use). Categories: boot 0, title 3, menu 12, cutscene 3, gameplay ~25, hud 1, system ~25, map 2, inventory 6,
dialogue ~10, shop 8, battle ~10, boss 3, gameover 1, save 1, ending 3. Every command letter gets one shot
(prompt or result). How to reach each group:
- Title, demo, menus, roster, creation form (each field), register, form the party, look at a character:
  `title`, `menu`, `party` + the macros' steps (`C_RYZ` ends at "O.K.?"; Look = `l` + Enter + entry).
- First moments: `start` (status panel, moons, wind, the idle Pass), Ztats pages (`z,1` + `space` per line), Peer
  at gem, Look, Quit & Save, each command's prompt (`try_t5.png` lists the frames).
- Towns and castle: `towne` (LCB), `castle`, `lordbritish` (Experience more!), the late party's "Thou art
  greater" and "Seek ye, the Mark of Kings!" (`@hero,ENTER:2D:12,POS:20:0F,t,w30,1,w30,up,w300`, the second with
  `poke:2E5A=0F06`), talk lines (Transact with people: their squares in design/content.md), all eight shops
  (`SHOP:x:y:dir` after `ENTER`, table above), Bribe a guard, Steal a chest, Unlock a door; each towne once
  (`@hero,ENTER:x:y`), Dawn (`dawn`), Yew's Circle of Light + PRAY.
- Travel: horse (Devil Guard stables, or `poke:2E3A=0A,space`), frigate (`SHIP`), Fire cannons, wind, the
  moongate before/after (`moongate`, `time`), the whirlpool sequence to Ambrosia (`ambrosia`).
- Fights: `fight` (orcs), more kinds with `FOE:tile` (60 orc, 5C thief, 64 skeleton, 50 fighter, 68 giant, 6C
  daemon, 70 pincher, 58 wizard, 74 dragon, 78 balron; water: 34 serpent, 38 man-o-war, 3C pirate need a sea
  square), attack/hit/miss/kill/victory, a spell in combat, the chest after, Get chest (trap messages), a
  dungeon fight, the Floors (`exodus` + walk to (1F,0F)).
- Dungeons: `dungeon` (dark, torch, corridor, ladder, Klimb/Descend), `rod` (+ "It left a mark!"), fountain
  (`DNG:07:0A:07:03,up` in the Fire dungeon), misty writing, strange wind, gremlins, trap, `timelord`.
- Ambrosia: arrival, shrine offering ("Shazam!"), each card search (`card`; Love (04,24), Moons (06,06), Death
  (37,1B) with `POS:x:y+1,up`), Ambrosia's monsters (without `CALM`).
- Endgame: Exodus' lines, `serpent`, EVOCARE without/with mark (`evocare`), the Isle of Fire, `exodus` (lava,
  fields, monsters), the Floors, `exodus_slots`, each insert, the flashing castle, `ending` (both texts).
- Game over: all four with status D (`@start,poke:2E5D=44,poke:2E9D=44,poke:2EDD=44,poke:2F1D=44,space,w300`).

## Capture notes (2026-11-19)
How the set `main` (260 shots) was made; reuse before experimenting. Previews: `tools/try.py` sheets (with
`--crop 190,0,320,200` for the message area), then lines written into `work/shots/dos/ultima-3/main/shots.txt`
and shot with `shoot.py --only`; long fights interactively with `play.py` + `sample "space,w90" N` and the
message area of each frame tiled (pick the frame with the line wanted, then `do!` that many times).
- **Random numbers:** one generator, 16 bytes at 4413-4422 (code 0x514B), modelled by `tools/u3rng.py`.
  `poke:4413=` + 32 hex digits right before the deciding key forces the next rolls: all zero gives 0 first
  (an evaded trap check fails, a steal succeeds, Repond works); chest outcomes by state (first two bytes, rest 0):
  `0000` gold only, `025D` gold + 2-H-Swd, `035A` gold + Chain, `0089` acid (damage), `0080` poison, `0180` gas,
  `0082` bomb, `009D` acid evaded; steal (ryz) `42` Failed!, `43` Watch out!. Poke after the prompt's last key
  but before the key that decides: the idle loop calls the generator while a prompt waits (a poke before
  "Resurect whom?" did not survive the wait).
- **Monsters on the map:** `MON:pic:under:x:y:addr` (object 0 + the map byte; addr = 1A80 + y*64 + x) next to
  the party, a pass later the fight starts. Field by terrain: brush (17,09)/(17,0A) 1D17, forest (27,2F)/(27,30)
  26A7, frigate (3B,15) with a serpent at (3C,15) 1FFC or a dragon on the shore (3A,15) 1FFA, shore (2D,0E) with
  a man-o-war or pirates at (2D,0F) 1E6D. Pirate ship for cannons: object 0 picture 3C at (3E,15), map 1FFE.
- **Combat RAM:** field 11x11 at 3E44 (y*11 + x; 08 floor in dungeons, monster tile = picture/4); monsters x
  3EC4, y 3ECC, H.P. 3EDC (8 each, binary); players x 3EE4, y 3EE8. Moving a monster: poke its x/y and both map
  bytes (`battle_bow`).
- **Dungeons:** `tools/u3dng.py FILE.ULT kinds` lists specials with an approach `DNG:LL:XX:YY:FF` (facing two
  hex digits: `DNG:00:06:01:03`, a single digit fails the poke). Random fights: walk back and forth
  (`up,w60,right,w30,right,w30` three times from `dungeon` gave Goblins, checkpoint `dfight`).
- **Talk:** `tools/u3town.py FILE.ULT` lists every person with square, talk byte and line; people with the
  0x40 bit wander, so only the standing ones are reliable (talk shots: POS beside them, `t,w30,1,w30,dir`).
  Merchants also step along their counter: Dawn's weapons merchant is at (1A,11), so `SHOP:1A:13:up`.
- **Shops:** every answer is a letter or number plus Enter; lists are paged (a key shows the next page).
- **Whirlpools:** honest-looking route: frigate at (3B,15), `poke:1FFB=30` (the whirlpool under the ship),
  `space`; Ambrosia's way back: `@ambrosia,POS:21:3A,poke:2921=30,space,w300`.
- **Game over in play:** from `pinchers`, all four H.P. set low (12, 9, 15, 11), then 27 x `space,w90`.
- **Not captured:** Ready in combat (not a combat command), Surmandum's failure into ashes (the forcing poke did
  not hold), lava damage without the Mark of Fire (no damage seen in one step), the alternate-name rule.

## Start set (2026-11-22)
`shots/start/` (60): power-on, title, menu, creating the four (`C_*` steps), Form, Register, Look, Journey Onward, Ztats,
Look, LCB (walked: talk, pub, weapons, armoury, grocer), the first fight, the chest, the castle healer, Lord British,
Quit & Save. No pokes; every step walked (`work/plan/ultima-3/` had the BFS helper `tmap.py`, not committed).
- Chain `s_talk` (thief in the pub, "Exodus lies beyond the Silver Snake!") -> `s_weapons` (pub drink 10 g.p.: tip
  "Ambrosia, ever heard of it?") -> `s_armed` (Axe 125 for ryz, Ready E + Enter, Join gold to 1) -> `s_armour` (Leather
  195, Wear C + Enter) -> `s_food` (40 rations from (30,31) down) -> `s_out` (west gate: "Exit to Sosaria!" on (2E,13)) ->
  `s_skeleton` (`w20` + 84 x `space,w30`: a ghoul beside the party, west) -> `s_melee` (A + West: "Conflict!! ->Ghouls",
  one ghoul of 15 H.P.) -> `s_victory` (ryz misses with the axe, cubi's Pontori fails, cubi's bare hands kill it: Exp.+04)
  -> `s_chest` (Get Chest by ryz: Bomb trap!, Gold+59) -> `s_healer` (castle, counter (2E,1A)) -> `s_lordbritish`
  (healing 200 for ryz, "Experience more!") -> `s_back` (south gate) -> `s_saved` (Q: 00001932 moves; save `04_first_fight`).
- The fight depends on the turn timing from `s_out`: `w20` gives the ghoul at pass 84; `w90` a giant from the south at pass
  41 (too strong for a new party); other waits gave monsters stuck behind brush (findings.md). Search script pattern:
  play the route, then `space,w30` per turn and read the objects at 2C00/2C40/2C60 and 2E3C (80 = combat).
- Monster spawn code: 0x22A5 (EXODUS.BIN, see design/systems.md).
- Gold of a new party: 150 each; after the towne visit ryz holds 230 (joined), 89 after the healer.

## Strategy and walkthrough notes
- **Fastest route to the ending (verified, all checkpoints):** `hero` -> `POS:0A:3B,SHIP` -> `EVOCARE:1` ->
  `up,w60,up,w60,x,w60,up,w60,e,w300` -> `NOFLOORS,POS:1E:0C` -> `INSERT:1:l`, `right`, `INSERT:1:s`, `right`,
  `INSERT:1:m`, `right`, `INSERT:1:d`, `w600`.
- **Honest outline** (code + talk files, for captions): build levels by fighting, Lord British turns experience
  into hit points (100 per visit), the Mark of Kings past level 5; money buys arms; find a frigate (pirates);
  a whirlpool leads to Ambrosia: shrines for statistics, Search the shrines for the four cards; the marks from
  rods deep in the dungeons (all four needed by every member for the Castle of Fire); the moongate at moon phase
  7 to the Time dungeon for the card order; Pray in Yew for EVOCARE; Dig the exotics on two islets; the Silver
  Snake; Castle Exodus; insert the cards.
- Monsters walk towards the party on the map and in towns; a fight starts when one reaches it. Ambrosia's
  monsters stand near the shrines: `CALM` removes them (and puts the right terrain back), keeping the horses.
- The moves counter shows in Quit & Save and in the ending; `HERO` sets it to 48,317.
- Food goes down every few moves for each character (F:); `HERO` gives 1400-2000.

## Naming
Main character **ryz** (Paladin, leads), then condi, ebo, cubi, typed in the Create form one key per token
(lower case is kept: "ryz"). The roster keeps them as entries 1-4.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Position on any map | `POS:x:y` (hex) = poke x/y + a pass (the view redraws) | RAM | verified (Sosaria, towns, castles, Ambrosia) |
| Enter a place | `ENTER:x:y` = `POS` + `e` (squares in Game structure) | RAM | verified (castle, townes, dungeons) |
| Late-game party | `HERO` (table below) | RAM | verified (Ztats, panel) |
| A fight | `FOE:tile` beside the party at the start square (2C,14): the monster attacks on the pass | RAM | verified (60 orcs) |
| Dungeon square | `DNG:level:x:y:facing` (level 00-07, facing 0 N 1 E 2 S 3 W) after `ENTER` + `TORCH`, then `up` steps on | RAM | verified |
| Moongate | `GATE:a:b` sets the moons so that on the pass the gate opens at phase a's square and leads to phase b+1's | RAM, code | verified |
| Ambrosia | `AMBROSIA` (a whirlpool poked under the party at (2C,14) + pass) | RAM, code | verified |
| Calm Ambrosia | `CALM` (its monsters removed) | RAM | verified |
| Frigate | `SHIP` (party picture = frigate, wind calm for 25 turns) | RAM | verified |
| Other commands | `SEARCH:p`, `INSERT:p:letter`, `EVOCARE:p` (p = player) | | verified |
| No Floors | `NOFLOORS` (Exodus castle objects 12-15) | RAM | verified |
| Shops | `SHOP:x:y:dir` (Transact by player 1) | | verified |
| Marks/cards of one character | rec + 0x0E: bit 0 Love, 1 Sol, 2 Moons, 3 Death, 4 Force, 5 Fire, 6 Snake, 7 Kings (`poke:2E5A=FF` = all for ryz) | code, Ztats | verified |
| Monster beside the party | `MON:pic:under:x:y:addr` (see Capture notes) | RAM | verified (15 kinds) |
| Forced rolls | `poke:4413=<32 hex>` before the deciding key (`tools/u3rng.py`) | code | verified (chests, traps, steal, Repond) |
| Debug menus, level select, codes | none found (no web source reachable; nothing in the program's text) | | |

`HERO` values (realistic, below the race limits Human 75/75/75/75, Elf 75/99/75/50, Dwarf 99/75/50/75, Bobbit
75/50/75/99, Fuzzy 25/99/99/75):
| | Str Dex Int Wis | H.P. / max | Exp. (level) | Food | Gold | Gems Keys Powd Trch | Marks/cards |
|---|---|---|---|---|---|---|---|
| ryz | 71 66 38 63 | 2213 / 2300 | 2341 (24) | 1847 | 4352 | 4 3 5 6 | all marks, all cards |
| condi | 33 87 75 41 | 1784 / 1900 | 1937 (20) | 1592 | 2187 | 2 1 3 2 | all marks |
| ebo | 92 70 22 30 | 2316 / 2400 | 2486 (25) | 2034 | 3065 | 1 2 0 4 | all marks |
| cubi | 41 47 36 94 | 1653 / 1800 | 1863 (19) | 1416 | 1974 | 3 0 2 3 | all marks |
Everyone wears Exotic armour and readies an Exotic weapon and owns a few ordinary arms; moves 48,317.

### Saves (rom/saves/ultima-3/, never committed)
None downloaded (web hosts unreachable). Made here (committed): `saves/01_start.sav` (new party, Quit & Save at
the start), `saves/02_endgame.sav` (`HERO` party in a frigate south of the Silver Snake), `saves/04_first_fight.sav` (honest new party after the start set's first fight, Quit & Save on the castle square), `saves/03_pirate_frigate.sav`
(`HERO` party in a frigate east of LCB after beating a pirate crew, the captured frigate beside it), see
`saves/README.md`.

## RAM map (for `game.json` "ram" watches and pokes)
Physical addresses (DS:offset + 0x1980). BCD = packed decimal, **low byte first** (write with `set:A=N:2:bcd`).
| Address | Size | Meaning | How found |
|---|---|---|---|
| 1A80 | 4096 | the current 64x64 map (Sosaria, a town, Ambrosia): y*64 + x; tile = byte / 4 (00 water, 04 grass, 08 brush, 0C forest, 10 mountains, 14 dungeon, 18 towne, 1C castle, 20 floor, 24 chest, 28 horse, 2C frigate, 30 whirlpool, 34 serpent, 38 man-o-war, 3C pirate, 40 merchant, 44 jester, 48 guard, 4C Lord British, 50 fighter, 54 cleric, 58 wizard, 5C thief, 60 orc, 64 skeleton, 68 giant, 6C daemon, 70 pincher, 74 dragon, 78 balron, 7C Exodus's slots, 80 force field, 84 lava, 88 moongate, 8C wall, 98-FC letters A-Z on signs, F8 shrine) | file, code |
| 2280 | 2048 | dungeon: 8 levels at 2280 + level*256 + y*16 + x (00 open, 80 wall, A0 door, C0 secret door, 10 ladder up, 20 down, 40 chest, 01 Time Lord, 02 fountain, 03 wind, 04 trap, 05 rod, 06 gremlins, 08 writing) | code (DS:0x900) |
| 2A80 | 144 | dungeon level messages / town talk lines (DS:0x1100) | code |
| 2C00 / 2C20 / 2C40 / 2C60 / 2C80 | 32 each | map objects (monsters, people, ships): picture, terrain under it, x, y, movement/talk byte | code, verified |
| 2CA4 / 2CA5 | 1 each | moon phases (gate square / gate destination); 2CA6 / 2CA7 turns until each changes | code, verified |
| 2E3A | 1 | party picture: 3F on foot, 0A horse, 0B frigate | code, verified |
| 2E3C | 1 | where: 00 Sosaria, 01 dungeon, 02 towne, 03 castle, 04 a picture screen, 80 combat, FF Ambrosia | code, verified |
| 2E3D | 4, BCD | moves | verified |
| 2E41 | 1 | party size | code |
| 2E42 / 2E43 | 1 each | the Sosaria square saved on entering a place (PARTY.ULT copy) | code |
| 2E44 | 4 | roster numbers of players 1-4 | file |
| 2E4C + 0x40*k | 64 | player k+1 (= PARTY.ULT from offset 0x12; ROSTER.ULT uses the same 64-byte record) | file, verified |
| rec+00 | 14 | name | file |
| rec+0E | 1 | cards and marks (bits above) | code, Ztats |
| rec+0F | 1, BCD | torches | Ztats |
| rec+11 | 1 | status G good, P poisoned, D dead, A ashes | ROM text, verified |
| rec+12..15 | 1 each, BCD | Strength, Dexterity, Intelligence, Wisdom | verified |
| rec+16 / 17 / 18 | 1 each | race letter, class letter, sex letter | file |
| rec+19 | 1 | magic points (regenerate each turn) | panel |
| rec+1A / 1C / 1E | 2 each, BCD | H.P., max H.P. (H.M.), experience; level shown = experience / 100 + 1 | verified |
| rec+20 / 21 | 1 / 2 BCD | food fraction / food | verified |
| rec+23 | 2, BCD | gold | verified |
| rec+25 / 26 / 27 | 1 each, BCD | gems, keys, powders | Ztats |
| rec+28 | 1 | armour worn (0 skin, 1 cloth .. 6 +2 plate, 7 exotic) | Ztats |
| rec+29..2F | 1 each, BCD | armour owned: cloth, leather, chain, plate, +2 chain, +2 plate, exotic | Ztats |
| rec+30 | 1 | weapon readied (0 hands, 1 dagger .. 14 +4 sword, 15 exotic) | Ztats |
| rec+31..3F | 1 each, BCD | weapons owned: dagger, mace, sling, axe, bow, sword, 2-H sword, +2 axe, +2 bow, +2 sword, gloves, +4 axe, +4 bow, +4 sword, exotic | Ztats |
| 2F4C / 2F4D | 1 each | x / y on the current map (dungeon: 0-15) | find, verified |
| 2F4F | 1 | dungeon level 0-7 | code, verified |
| 3F1D | 1 | the square under the party (tile number) | code, verified |
| 4412 / 442A | 1 each | wind (0 calm, 1 North, 2 East, 3 South, 4 West) / turns until it changes | code, verified |
| 4413 | 16 | random number state (code 0x514B; `tools/u3rng.py`) | code, verified |
| 3E44 | 121 | combat field 11x11 (y*11 + x) | RAM |
| 3EC4 / 3ECC / 3EDC | 8 each | combat: monster x / y / hit points | RAM, verified |
| 3EE4 / 3EE8 | 4 each | combat: player x / y | RAM |
| 724C | 1 | dungeon facing (0 N, 1 E, 2 S, 3 W) | code, verified |
| 7E20 | 2 | Exodus slots filled (0-4; DS:0x64A0) | code |

## Emulation notes
- **Model `svga-300`.** GOG's config: `machine=svga_s3`, `cycles=300`, `core=simple`. The game's turns are
  timed by the DOS clock (the idle Pass comes after 5 seconds), so the cycle count changes only the drawing and
  sound delays: at 300 the title takes about 40 s to draw (2,400 frames) and the attract demo, town entry
  ("Please wait..." under 300 frames) and combat pace look like the original 8088; no key was lost with the
  default press. CGA palette (cyan, magenta, grey) on `svga`: identical frames after a state load (every
  checkpoint compared between an empty-cache rebuild and a cache hit), so no `ega` machine is needed.
- **Files written** (verified): Create/Form write ROSTER.ULT and PARTY.ULT; Quit & Save and entering any place
  write PARTY.ULT (party records and position) and SOSARIA.ULT (the map with its monsters, moons, whirlpool);
  folder in the save ZIP: `ULTI-III/`. The roster keeps the characters as they were when the party was formed;
  the live party is in PARTY.ULT.
- **Disk check** (verified 2026-11-19, `tools/cachecheck.py`, about 2 min): all 23 checkpoints rebuilt from an
  empty cache give the same frame and the same written files as a cache hit; Quit & Save after cache hits of
  `start`, `hero`, `time` and `ambrosia` writes the same files as the whole route from power-on.
- The play screen rarely settles (the idle Pass every 5 seconds scrolls the message area): `do` reports "still
  changing"; that is normal. Shots: `do!` + `wN`.
- After a position poke the view redraws on the next turn (`POS` includes a pass). Status panel values redraw on
  the next turn after a poke (verified with `HERO`).

## Checkpoints
`checkpoints.txt` (23): `title`, `menu`, `party`, `start`; new party: `towne` (LCB), `castle`, `lordbritish`;
late party (`HERO`): `hero`, `fight`, `dungeon`, `rod`, `moongate`, `time`, `timelord`, `dawn`, `ambrosia`,
`shrine`, `card`, `serpent`, `evocare`, `exodus`, `exodus_slots`, `ending`. Added by the capture (30 in all):
`won` (orcs beaten with Mittar and Repond, a chest south of the party), `pirates` (boarding fight on two decks),
`pirates_won` (pirates beaten, Quit & Save: save 03), `thieves` (Cutpurses on brush), `pinchers` (Snatches on
grass), `condi_dead` (after the pinchers, condi D), `dfight` (Goblins in Dardin's Pit level 1). Start set (44 in all): the honest `s_*` chain, see "Start set".

## Tools
- `tools/try.py FILE [--frames K] [--peek ADDR:LEN] [--crop x0,y0,x1,y1] [--cols N]`: many routes in parallel,
  one sheet (`work/scout/ultima-3/try_NAME.png`) (from Ultima II).
- `tools/cachecheck.py`: every checkpoint from an empty cache vs a cache hit (frames and written files), plus
  Quit & Save after four cache hits vs the whole route.
- `tools/u3rng.py STATE N`: the random generator's next outputs for a 16-byte state (forcing rolls).
- `tools/u3town.py FILE.ULT ...`: the people of a towne or castle map with squares, talk bytes and lines.
- `tools/u3dng.py FILE.ULT [kinds]`: special squares of a dungeon with a `DNG` approach.
- Scratch (not committed, in `work/scout/ultima-3/`): `tmap.py FILE.ULT` (a map file as characters with the
  letters on signs and odd tiles listed), `dis.py START END` (ndisasm listing range), `files.py ROUTE` (files
  written after a route).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| The game's own files (program text, code, maps, talk lines, dungeon files) | `rom/ultima-3.zip` | commands, messages, quest rules, places, coordinates, prices, RAM | 2026-11-19 |
| Wikipedia, Ultima III: Exodus | https://en.wikipedia.org/wiki/Ultima_III:_Exodus | release history, IBM PC version (no music, 4.77 MHz), story outline (marks, cards, Time Lord, Ambrosia), HP cap 2550 | 2026-11-19 |
| Web search result snippets (walkthroughs) | https://wiki.ultimacodex.com/wiki/Ultima_III_walkthrough | card order Love, Sol, Moons, Death from the Time Lord at the bottom of the Dungeon of Time, reached by moongate (snippets only) | 2026-11-19 |
| Unavailable | mikesrpgcenter.com, gamercorner.net (outside the network); GameFAQs, TCRF, StrategyWiki (403, known); ultimacodex.com (known) | | 2026-11-19 |

## Open questions
- ~~Combat formulas, spell effects and costs, which CNFLCT map per terrain~~ settled 2026-11-19 (design/rules.md:
  monster hit and damage, spells A-P of both lists with costs 5 x letter, the nine fields). Still open: the
  party's own hit and damage formulas, monster hit points per kind.
- ~~Class rules~~ settled (design/rules.md 3: weapon and armour limits per class, who casts which list).
- Starving: food 0 showed no message within 300 frames; the damage rule is not read.
- ~~Ambrosia's whirlpool back, the honest frigate~~ played 2026-11-19 (`cutscene_ambrosia_return`: back aboard
  a frigate; `system_frigate_taken`: a boarded pirate ship stays as an empty frigate).
- ~~Whether a square gives Exotics only once~~: it does not; each dig adds one (RAM, 2026-11-19).
- Which of a monster's two names (Orcs/Goblins, Thieves/Cutpurses ...) a fight uses.
