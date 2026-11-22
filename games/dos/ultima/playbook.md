# Ultima I: The First Age of Darkness (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"ROM text" = read from the game's own programs (`strings` on OUT.EXE, SPACE.EXE, MONDAIN.EXE), "code" = read
from OUT.EXE / MONDAIN.EXE with ndisasm (offsets are file offsets after the 512-byte EXE header).

> **Tools moved (2026-11-20).** Where this playbook says `try.py`, `cachecheck.py` or `screen.py` (copies that
> lived in this game's `tools/`), use the shared tools: `python3 tools/preview.py dos/ultima FILE` (`--frames K` is now
> a `?` mark inside the route or `--timeline N:STEP`; sheets in `work/preview/dos/ultima/`), `python3
> tools/cachecheck.py dos/ultima` (`--after TOKENS` for a save in the game, `--peek ADDR:LEN` for party tables) and
> `python3 tools/play.py text` / `preview.py --text` for text screens. Pictures are native size
> (`play.py shot --scale N` on demand).

## Read first
- Start: `python3 tools/play.py start ultima --name ultima --route @start` (ryz on the overworld, level 1). Boot
  macros `BOOT`, `TITLE`, `MENU`, `CREATE`, `RYZ`, `PLAY`, `NEWGAME` (Boot sequence below). Late states:
  checkpoints `mid` (save 03_midgame), `endgame` (save 02_endgame).
- Sets: `main` (201 shots, power-on to the ending, cheats allowed) and `start` (52 shots, the early game played
  honestly to the first Q save, checkpoints `s_*`, save 04_first_trip; section "Start set" below).
- Shortcuts for `main`-style shots: `WARP`, `GO`, `TPOS`/`TPOS2`, `SPAWN`, dungeon monster pokes (Shortcuts).
  Honest walking instead: `games/dos/ultima/tools/walk.py town X Y` (walks the live session to a town or castle
  square around the people) and `walk.py over X0 Y0 X1 Y1` (overworld tokens over grass and woods).
- Traps that cost calls: the status panel is not redrawn after pokes (save with Q, start from `sav:`); `type:`
  drops letters (one key per token); after a kill keep attacking only as often as needed (each extra `a` is a
  turn in which new monsters hit); `undo` is one level, checkpoint before each fight.
- Text: graphics mode only (no `play.py text`); the message log keeps three lines, so the player's own line
  ("Hit! Skeleton killed!") is scrolled away by the monster's answer: take frame `ROUTE,a,!` for it.
- Open: starbase docking, pub seduction, Steal spell (game.json "open").

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Ultima I: The First Age of Darkness (title text "Ultima I / The First Age of Darkness", picture "Ultima I"; menu "*** Ultima I *** from darkest dungeons, to deepest space!") (verified) |
| Platform / model used | IBM PC / MS-DOS, `svga-500` (`game.json`); the game picks EGA 16 colours (EGA*.BIN, CASTLE.16) by itself, 320x200 (verified) |
| Release (region, year) | 1986 remake (Apple II, December 1986); MS-DOS EGA version 1987 (Wikipedia); title screen "Copyright (C) 1987 Origin Systems, Inc."; credits "Conversion by: John Fachini" (verified). This dump is the owner's GOG folder `Ultima I/` (28 files, SHA-1 in `game.json`) |
| Developer / publisher | Richard Garriott (Lord British), Origin Systems; IBM conversion John Fachini (verified on screen) |
| Genre | Single-character RPG: top-down overworld with towns and castles, first-person wireframe dungeons, first-person space combat |
| Players / save system | 1 player, four character slots (PLAYER1-4.U1). **Q (Quit) on the overworld saves** ("Quit - saving game...saved.", play continues; "only allowed outdoors" elsewhere) (verified) |
| Programs | `ULTIMA.EXE` (title, menu, character selection) chains `GEN.EXE` (character generation), `OUT.EXE` (overworld, towns, castles, dungeons), `SPACE.EXE` (space flight) and `MONDAIN.EXE` (time machine, Mondain, ending). Each program replaces the running one ("Exec loader", ROM text) and they pass the character through `INUSE.U1` (code: OUT writes the 820-byte record to INUSE.U1 just before starting SPACE or MONDAIN) (verified: INUSE.U1 appears on the written disk at the first switch) |

## Boot sequence
All macros in `game.json`; every one ran as a single `do`/`try.py` run from power-on (verified 2026-11-19).
- Intake probe `work/intake/dos/ultima/sheet.png` shows only DOSBox Pure's start menu (five programs, GEN.EXE
  first). `ULTIMA.EXE` is the fifth: `BOOT` = `w120,down*4,enter` (verified). GOG's `dosboxULTIMA1.conf` only runs
  `ultima.exe` (no loadfix, no switches); its cloud-saves overlay is not reproduced.
- **Attract loop** (verified, `work/scout/ultima/attract/sheet.png`): text title "Ultima I / The First Age of
  Darkness / Copyright (C) 1987 Origin Systems, Inc." (~400 frames), Origin Systems logo drawn line by line with
  "Presents...", "...a new release of the best selling personal computer role-playing adventure...", "...Lord
  British's original fantasy masterpiece...", then the castle picture "Ultima I" (CASTLE.16) for ~1,100 frames,
  then the loop starts again. `TITLE` = `BOOT,w1800` lands on the castle picture (checkpoint `title`).
- Any key in the attract loop shows a credits card (Origin logo, "ULTIMA and LORD BRITISH are registered trademarks
  of Richard Garriott and Origin Systems, Inc.", "Conversion by: John Fachini") and then the main menu
  "a) Generate new character  b) Continue previous game  Thy choice:". `MENU` = `TITLE,space,w400` (checkpoint
  `menu`). No graphics or sound prompt: the game detects EGA itself (verified with `svga`).
- `a` starts GEN.EXE: **Character Generation** (checkpoint `gen`). `CREATE` (verified): 30 points over six
  statistics that all start at 10 (up/down choose, right/left add/remove; Strength +10, Agility +8, Stamina +7,
  Charisma +3, Intelligence +2), space; race `a` Human (b Elf, c Dwarf, d Bobbit; Human gave Intelligence +5);
  sex `a` Male (b Female); class `a` Fighter (b Cleric, c Wizard, d Thief; Fighter gave Strength +10 and Agility
  +10); name `r,y,z` (one key per press: `type:` loses letters at 500 cycles), `enter`; "Save this character?
  (Y-N)" `y` -> back to the main menu. Result: ryz, Str 30 Agi 28 Sta 17 Cha 13 Wis 10 Int 17, 150 hit points.
  `RYZ` = `MENU,a,w300,CREATE`.
- `b` -> **Character Selection** "1) ryz 2) 3) 4)  Type number of character you wish to use in Ultima I. Press
  ESCAPE to go to the main menu"; `1` starts OUT.EXE on the overworld. `PLAY` = `b,w200,1,w300`;
  `NEWGAME` = `RYZ,PLAY`; checkpoint `start` = ryz at (31,28) east of the Castle of Lord British: Hits 150, Food
  200, Exp. 0, Coin 100, leather armour and two daggers (verified).
- Saved game: `sav:01_start,MENU,PLAY` powers on with the exported PLAYER1.U1 and continues (verified).

## Controls
Single keys; every command echoes its name in the message area (bottom left) and asks for what it needs.
| Context | Key | Action | Status |
|---|---|---|---|
| Overworld, towns, castles | arrows | move one square (North/South/East/West); blocked terrain answers "You can't walk on water!", "Mountains are impassable!", "Aircars can't pass woods!", "Frigates like water!", "Rafts like water!", "Can't move on land!" (ROM text; water verified) | verified |
| | `space` | Pass (one turn) | verified |
| | `a` | Attack with <readied weapon>: direction (melee next square; "Missed!", "Hit the Thief! 30 damage", "Killed!") | verified |
| | `b` | Board a vehicle on the square ("Board Shuttle", "Board Time Machine", "Nothing to Board!", "X-it thy craft first!") | verified |
| | `c` | Cast the readied spell ("Cast Prayer "POTENTIS-LAUDIS!" Hmmmm... no effect!" outdoors) | verified |
| | `d` | Drop ("Drop Pence,Weapon,Armour:"; "Thou canst not leave it here!" in places) | prompt verified |
| | `e` | Enter the town, castle, dungeon or landmark on the square ("Entering... The city of Britian") | verified |
| | `f` | Fire the vehicle's guns ("Fire what?" on foot; cannons on a frigate, lasers on an aircar: ROM text) | prompt verified |
| | `g` | Get ("Get?") | prompt verified |
| | `h` | HyperJump ("HyperJump?" outdoors; in space only, see below) | verified |
| | `i` | Inform and search ("You are in the lands of Lord British"; in towns finds secret doors: ROM text) | verified |
| | `k` | K-limb ladders in dungeons ("Thou must face the ladder!") | prompt verified |
| | `n` | Noise on/off (sound) | verified |
| | `o` | Open (coffins and chests in dungeons and towns) | prompt verified |
| | `q` | Quit: save the game (outdoors only), play continues | verified |
| | `r` | Ready: `w`eapon / `a`rmour / `s`pell, then the item by letter in list order (armour a Skin, b Leather, ..., e Vacuum suit, f Reflect suit) | verified |
| | `s` | Steal (in shops: "Oh no! Thou wert caught!" guards attack) | prompt verified |
| | `t` | Transact with a shopkeeper (stand at the counter: "Transact-Buy, Sell:") or the king ("Dost thou offer pence or service:") | verified |
| | `u` | Unlock a cell door in a castle prison (needs a key: "Thou hast not a key!", "Thou hast not the correct key!", "The door is open!") | verified |
| | `v` | View change (vehicles; in space front/top view) | prompt verified |
| | `x` | X-it the vehicle | prompt verified |
| | `z` | Ztats: Inventory screen (statistics, coins as copper/silver/gold, armour, weapons, spells, vehicles, gems, enemy vessels; readied items red), space continues | verified |
| | `j l m p w y` | "Huh?" | verified |
| Dungeon | `up` forward, `left`/`right` turn, `down` turn around ("Forward", "Turn left/right", "Turn around") | | verified (up, left, right) |
| Dungeon (capture) | `a` attacks straight ahead (no direction); `k` climbs a ladder under the hero when facing north or south ("Thou must face the ladder!" otherwise); `u` opens a chest under the hero (trap roll), `o` a coffin; `c` casts the readied spell ahead. The first key after `TPOS2` is sometimes dropped: put `space,w60` after it | | verified |
| Space front view (capture) | `space` = "Center"; `f` fires (10 fuel); `v` refused while enemies remain; a hyperjump needs about 1,250 frames before "HyperJump completed." (`h,w1300`) | | verified |
| Space (SPACE.EXE, top view) | `up` Thrust, `down` Retro, `left` Counter-Clockwise, `right` Clockwise, `space` Pass, `i` Inform and Search = Sector Scan (7x7 map of the 49 sectors), `v` View (front view), `z` Ztats, `f` Fire, `h` HyperJump (front view only: "Lightspeed!") | | all verified 2026-11-19 (`@space`) |
| Mondain (MONDAIN.EXE) | arrows, `a` attack, `g` Get (Gem), `c` cast ("INTERFICIO-NUNC!" makes him stronger: ROM text); Quit, Transact, Steal refused | | arrows, a, g verified |
| Prompts | the letter shown; `y`/`n`; `space` "Press Space to continue"; `esc` back to the main menu in GEN and Character Selection | | verified |

Input timing: the default press (hold 8, wait 40) works in every menu at 500 cycles. `type:` (4-frame presses)
drops letters in the name prompt; type names one key per token. Town and dungeon entry: `w200`; a program
switch (shuttle, time machine): `w300` then the next key; space lift-off countdown: `w900` after `b`.

## Game structure
- **Sosaria** (verified with `tools/worldmap.py`, MAP.BIN 168x156 squares, 4 bits each: water, grass, woods,
  mountains, castle, landmark, town, dungeon) is four continents, one per quarter (code: continent =
  2*(y > 77) + (x > 83)): 0 north-west "the lands of Lord British", 1 north-east "of the Feudal Lords", 2
  south-west "of the Dark Unknown", 3 south-east "of Danger and Despair". Each has 8 towns, 2 castles, 2
  landmarks and 9 dungeons (84 places; ids, coordinates and names from OUT.EXE: `tools/worldmap.py --list`).
- **Castles and quests** (code + verified): each castle has a king (T = transact: "pence" buys hit points,
  "service" gives a quest). Odd castles send the player to a landmark ("Go forth and find ..."), even castles
  send him to kill a monster ("Go now and kill a ...") and pay with the continent's gem:
  | Castle (id) | Continent | Quest | Reward |
  |---|---|---|---|
  | The Castle of Lord British (33) at (28,26) | 0 | find The Grave of the Lost Soul (48, continent 3) (verified) | "For this I will give thee 8 points of strength." (verified: Strength 30 -> 38) |
  | The Castle of the Lost King (34) at (20,1B) | 0 | kill a Gelatinous Cube | red gem: "it requires all four gems to launch a time machine!" |
  | The Castle Barataria (35) at (7D,25) | 1 | find The Southern Sign Post (46) | Strength |
  | The Castle Rondorin (36) at (72,1D) | 1 | kill a Carrion Creeper | green gem: "the time machine must be used in order to win" |
  | The Castle of Olympus (37) at (29,76) | 2 | find The Pillar of Ozymandias (44) | Strength |
  | The Black Dragon's Castle (38) at (1E,7E) | 2 | kill a Lich | blue gem: "the princess will help a space ace through time!" |
  | The White Dragon's Castle (39) at (7F,74) | 3 | find The Tower of Knowledge (42) | Strength |
  | The Castle of Shamino (40) at (87,69) | 3 | kill a Balron | white gem: "to take nine items from my storerooms - but only nine!" |
  Visiting the landmark (or killing the monster) while the quest is open shows "A quest has been completed!";
  the king then gives the reward (code). The other landmarks give statistics when entered: The Grave of the Lost
  Soul "VAE VICTIS", "Thou dost gain 2 Stamina" (verified); Pillars of Protection, Tower of Knowledge,
  Pillars of the Argonauts, Pillar of Ozymandias ("MY NAME IS OZYMANDIAS, KING OF KINGS..."), the sign posts
  ("FORTES FORTUNA ADIUVAT!", "ULTIMA THULE!", "GO EAST TO GO EAST!") (ROM text).
- **Towns** (verified in Britian): Transport, Magic, Pub, Armour, Weapons, Food shops, guards, a jester; shops sell
  more as game time passes (code: the move counter; aircar, shuttle, vacuum and reflect suits from 3,000 moves).
  Britian: Scooter's Super Duper Transport (Horse 36, Cart 144, Raft 324, Frigate 576; Aircar 900 and Shuttle
  1,296 after 3,000 moves), The Armour Shop of Lord Eldric D'Charbonneux (Leather armor 45, Chain mail 90, Plate
  mail 135), weapon shop (Mace 8, Rope & Spikes 19), Mad Chad's Magic Shoppe (Open 5, Magic Missile 15, Ladder
  Down 25), Li'l Karelia's Finnish Grocery (10 food for 5 pence), Pub de Varg ("Here, have a cold one!", the
  tavern keeper's tips: ROM text) (all verified, checkpoint `britian`, `TPOS` per counter in Shot plan).
- **Dungeons** (verified: Mines of Mt. Drash II): first-person wireframe, "Level N" on top, facing on the bottom
  frame; chests, coffins, ladders; monsters attack on their own (a Skeleton on level 1, checkpoint `skeleton`).
  Monsters by depth (ROM text list): Ranger, Skeleton, Giant rat, Spider, Viper, Cyclops, Gelatinous cube, Ettin,
  Chest (mimic), Lizard man, Minatour, Carrion creeper, Tangler, Gremlin ("A gremlin stole some food!"),
  Wandering eyes, Wraith, Lich, Invisible seeker, Mind whipper, Zorn, Daemon, Balron.
- **Overworld monsters** (ROM text; several verified by spawning): Ness creature, Giant squid, Dragon turtle,
  Pirate ship (at sea), Hood, Bear, Hidden archer, Dark knight, Evil trent, Knight, Necromancer, Evil ranger,
  Wandering warlock; Thief and Orc seen too.
- **Space** (verified): buy a Shuttle, Board it: countdown "10..9..8.." "Thou hast lifted off!" -> SPACE.EXE, top
  view of the sector (planet Sosaria, sun, starbase, own ship); 7x7 = 49 sectors (Sector Scan); fly into the
  planet with the shuttle: "Thou hast landed safely!" -> OUT.EXE beside the launch square. Destroying 20 enemy
  vessels makes the player a Space Ace ("Thou hast achieved the rank of Space Ace!"); docking at a starbase costs
  500 pence and offers other ships ("Choose thy ship:") (ROM text).
- **Princess and time machine** (code + verified): every castle has a princess in one of two prison cells; killing
  the jester gives a key ("I've got the key!", "Thou hast found a key!") that opens one of the two cells (chosen at
  random on entry). Leading the freed princess out of the castle (she must be beside the player on the way out)
  gives 500 hit points, pence and experience; **if the player has destroyed at least 20 enemy vessels and has
  at least 7,000 experience (level 8)**, she adds "thou art now ready for time travel, and that there is a time
  machine far to the northwest!" and a Time Machine appears in the north-west part of the current continent
  (verified: at (10,0E) on route `rescued`).
- **The end** (verified to the ending text): Board the Time Machine with all four gems (without them: "Thou canst
  not determine how to operate the craft at this time.") -> MONDAIN.EXE: four pages of text, Mondain's chamber
  (time machine, player, the gem, Mondain). Get (Gem) next to it: "2196 damage!" (it costs the player most of his
  hit points) "The Gem is DESTROYED!". Mondain casts magic missile, mind blaster ("Stats are reduced!") and
  psionic shock; below 500 hit points he turns into a bat; at 0: "Mondain is dead!", "THOU ART VICTORIOUS!"
  (without the gem destroyed: "...or is he?"). Then the ending text (NIF.BIN, Lord British's reward, "Press
  CONTROL-ALT-DEL to Restart").

## Shot plan
**Set `start` (capture 2026-11-22): 52 shots, done** (section "Start set" in Strategy below; `shots/start/`).
**Done (capture 2026-11-19): set `main`, 195 shots, power-on to the ending text**; the replayable list is
`shots.txt` (game order), the published set `shots/main/`. Every target of the scout's 73-id plan was taken
except `system_starbase` (below); grouped ids got real names (`gameplay_continents` -> `gameplay_lands_*`,
`battle_overworld` -> `battle_orc_hit` and eight more, `battle_dungeon_*` -> 24 monster ids, `system_pub_tip` ->
`dialogue_pub_*`, `system_spell_cast` -> `system_spell_*`). The set covers, in game order:
- [x] boot and attract loop (5), title, credits, main menu; creation step by step (points, race, sex, class,
  name, save, another build) and Character Selection
- [x] start-character commands: HUD, Ztats, Ready weapon/armour, Inform, Cast Prayer, Noise, refusals, an orc
  fight, horse mount/ride/X-it, Quit-save, the three deaths (shuttle without fuel, starvation) and resurrection
- [x] Britian: town, every shop kind with buy, sell, refusals, food bought, pub ale and four tips, steal (success,
  caught), drop pence, Quit indoors
- [x] castles: Lord British (offer, pence -> hit points, landmark quest, busy, jester key, cell, no key, guards),
  the Lost King plan (monster quest, red gem), all four gem hints, Olympus's quest; all eight landmarks; the grave
  quest done and Lord British's reward
- [x] mid game (save 03_midgame): Ztats with More, Ready spell, the four lands, woods, blocked moves, cart, raft,
  frigate, at sea, three sea monsters, cannons, aircar, lasers, aircar vs woods, eight land monsters, the other
  seven town plans, shops by town parity and game time, castle storeroom theft
- [x] dungeons: level 1 to 10, door, ladder, K-limb down/out/facing, chest trap/gold, coffin, 24 monster kinds,
  quest kill, Magic Missile and the spells Ladder Down/Up, Blink, Create, Destroy, Kill, Open, Unlock
- [x] space (late character): Scooter's with aircar/shuttle, shuttle, countdown, top view, sector scan, front view,
  hyperjump, enemy, view refused, hit, alien fires, Space Ace, sun death, landing
- [x] the end: Ztats late, cell, princess, time machine (and without gems), four pages, Mondain, gem, hit, bat,
  "...or is he?", victory, ending text
Not captured: starbase docking and "Choose thy ship" (every port placement collided, design/findings.md), the
pub seduction (code read, not triggered), Iolo the Bard and the jester's songs (trigger not found), Prayer in a
dungeon (no visible effect), Steal spell (not sold anywhere seen), "Crunch!" against the starbase (seen once in
play, not reproduced in a route).
Ideas for a next round: the other 32 dungeon entrances look identical (fixed wireframe); a female or non-human
hero on the overworld looks the same (one hero picture).

### Start set (capture 2026-11-22, set `start`, 52 shots)
Played honestly from `@start` (no pokes, no warps; every step walked), the route is the chain of checkpoints
`s_castle_in` -> `s_king` -> `s_quest` -> `s_britian` -> `s_weapons` -> `s_mace` -> `s_armour` -> `s_food` -> `s_magic`
-> `s_pub` -> `s_iolo` -> `s_monster_seen` -> `s_monster_adjacent` -> `s_necro_killed` -> `s_grass` -> `s_at_dungeon`
-> `s_dungeon` -> `s_coffin_ahead` -> `s_coffin_open` -> `s_skeleton` -> `s_skel_hit1` -> `s_skel_killed` -> `s_thief`
-> `s_thief_killed` -> `s_ladder` -> `s_out_dungeon` -> `s_ranger` -> `s_ranger_hit` -> `s_ranger_killed` -> `s_return`
-> `s_king_pence` -> `s_king_hits` -> `s_left_castle` -> `s_saved` (verified: 52/52 reproduce from an empty cache).
What a new player meets (all verified on that route):
- Start (31,28): the castle is 2 up, 9 left (28,26); Britian is beside it at (27,27) (from the castle: left,
  down). Entering the castle puts ryz at its west gate (0,9); the king stands at (21,05) (walk.py town 21 5,
  about 45 steps; a guard at (1,6) blocks the first path). Leave by walking off the west edge from (0,9).
- On the walk through the castle "Gwino the jester sings: I've got the key!" appeared; leaving Britian by the
  south gate (13,11) "Iolo the Bard sings: Ho eyoh he hum!". Both are the songs the main capture never saw.
- Britian on foot: entry at the south gate (13,11); counters weapons (0C,0C), armour (06,0C), food (17,0C),
  magic (17,03), pub (20,05) (pub door 3F at (1D-1E,07)). Here the weapon shop is called "The Weapon Shop of Lord
  Eldric D'Charbonneux" and sells Mace 8, Rope & Spikes 19; the armour shop has the same name. Space at a
  Buy list leaves it ("Transact-Buy: nothing"). Bought: mace (100 -> 92), 6 packs of food (Food 193 -> 253,
  Coin 92 -> 62), an ale (1 pence, no tip on two tries).
- Overworld fights: 10 steps from Britian (right 5, down 5, to (2C,2C)) a Necromancer appears 7 squares east and
  walks up in 6 passes; 8 blows with the mace (many misses) kill it: "Killed the Necromancer! 6 copper! 2
  silver!", Exp. 17. On the way back (right of the dungeon, (29,3D)) an Evil ranger blocks: 3 blows, "3 copper!
  1 silver!", Exp. 74.
- The Mines of Mt. Drash II (27,3C), entered from the south (path `walk.py over 2C 2C 27 3C`): level 1 facing
  south, coffins at (1,6) (5 copper) and (1,8) (a Skeleton attacks right after the Open); a second Skeleton and
  a Thief (it took a dagger) come on the way back to the ladder (1,1); K-limb facing north: "Thou dost gain 54
  hit points".
- Lord British for pence: 60 pence -> 90 hit points (Hits 116 -> 206). Q outside the castle saves.

## Strategy and walkthrough notes
- **Cheat freely, but through the game's own transitions.** Values on the status panel (Hits, Food, Exp., Coin)
  are drawn only when the game changes them, so pokes do not show until the next change in play or the next
  program start. For shots with poked values: poke, save with `q`, and start a route from the save
  (`sav:NAME,MENU,PLAY`), as `endgame` does with `02_endgame`; or poke before a program switch (SPACE, MONDAIN
  redraw the panel from the record).
- **Coin is copper pence, capped at 9,999** (purchases with more set it to 9999); Ztats splits it into copper,
  silver (10) and gold crowns (100). Realistic: 8973.
- **Fastest route to the ending (verified):** `endgame` (save 02_endgame: level 8, four gems, 23 vessels) ->
  `princess_freed` (key poked, cell door at (1F,0F) from below) -> `rescued` (princess poked beside the player at
  the gate (0,9), step left) -> the time machine is placed far to the north-west of the continent (at (10,0E)
  in this route; read it from the object list) -> `WARP` beside it, step on, `b` -> four pages -> `mondain` ->
  10 steps right, `g` (the gem costs 2,196 hits: have more than that) -> attack with the blaster -> poke
  Mondain's hit points (bat below 500, dead at 0) -> `victory` -> `ending`.
- **Honest route outline** (for captions; ROM text and code): get money and gear in towns, do Lord British's
  landmark quest for strength, the four gem kings' monster quests (deep dungeons: Gelatinous Cube, Carrion
  Creeper, Lich, Balron), buy a shuttle after 3,000 moves, shoot 20 enemy vessels in space, reach level 8
  (7,000 experience), rescue a princess, find the time machine, destroy the gem, kill Mondain.
- Dungeons: monsters come quickly; with 150 hit points a Skeleton is harmless (2 damage). Food runs down one
  per few moves; buy food (10 for 5 pence).
- Space: without a shuttle's fuel and shields you die at lift-off (a spawned shuttle has none: give record
  +0xB0/+0xB2 = 1000 or buy the shuttle).

## Naming
Main character **ryz** (owner's rule): typed in GEN.EXE's name prompt one key per press (`r,y,z,w30,enter`);
`type:ryz\n` loses letters at 500 cycles (verified: "rz"). No other names in this game.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Overworld warp | `WARP:x:y` (hex) = player x/y and the player's map object, then a Pass: the map redraws around the new square | RAM | verified |
| Enter a place directly | `GO:x:y` = `WARP` without the Pass, then `e` (coordinates in `tools/worldmap.py --list`) | RAM | verified (town, castle, dungeon, landmark) |
| Town/castle position | `TPOS:x:y` = town x/y, then Ztats + space to redraw (without the redraw the old player picture stays) | RAM | verified |
| Spawn a vehicle or monster on the overworld | `SPAWN:type:x:y` writes overworld object 1 (type, 1, x, y) and sets the object count to 1 (it replaces object 1). Types: 0B horse ... 11 shuttle, 12 time machine (code), 23-30 land monsters (verified: Evil trent, Thief, Orc, Knight, Necromancer, Evil ranger, Wandering warlock among them; hit points in the fifth word, e.g. 0052) | RAM, code | verified (12, 11, 23-30) |
| Time machine without the princess | `GEMS,SPAWN:12:x:y` then step on and `b` | code | verified |
| Gems | `GEMS` (record +0x4C..+0x53 = 1 each) | code | verified |
| Late-game character | `ENDGAME` (statistics, money, experience, food, reflect suit, pistol, blaster readied, gems, 23 vessels), then `q` and the save | RAM | verified |
| Shuttle and aircar in shops | `set:17AF8=4127:2` (game moves past 3,000) | code | verified |
| Prison key | `poke:17AF0=01` (as if the jester's key were taken) | code | verified |
| Princess out | `RESCUE` (player to the gate (0,9), princess beside him, step out) | RAM | verified in Lord British's castle |
| Mondain's hit points | `poke:756E=XXXX` in MONDAIN.EXE (1000 at the start; 1-500 bat; 0 dead) | code | verified |
| Overworld object types (complete, capture) | 0A the hero's picture, 0B horse, 0C cart, 0D raft, 0E/0F frigate, 10 aircar, 11 shuttle, 12 time machine; sea monsters 13/14 Ness creature, 15/16 Giant squid, 17/18 Dragon turtle, 19/1A Pirate ship; land 1B/1C Hood, 1D/1E Bear, 1F/20 Hidden archer (invisible), 21/22 Dark knight, 23/24 Evil trent, 25/26 Thief, 27/28 Orc, 29/2A Knight, 2B/2C Necromancer, 2D/2E Evil ranger, 2F/30 Wandering warlock (two animation pictures each); 31-33 unknown pictures (no attack). Monster hit points: `poke:12A94=HHHH` after `SPAWN` | RAM | verified |
| Mid-game character | `MIDGAME` (level 5, 1487 hits, sword, chain mail, spells, horse and frigate, 2417 moves), then `q`: save `03_midgame`, checkpoint `mid` | RAM | verified |
| Position in a town, castle or dungeon for a character whose Ztats has two pages | `TPOS2:x:y` (= `TPOS` with a second space) | RAM | verified |
| A dungeon monster of any kind | facing east from (1,1): `poke:19CA2=02,poke:19CA0=LL,poke:19D60=KK00,poke:19D64=HHHH,TPOS2:01:01,space,w60` (LL level, KK monster id, HHHH its hit points). Ids: 0 Ranger, 1 Skeleton, 2 Thief, 3 Giant rat, 4 Bat, 5 Spider, 6 Viper, 7 Orc, 8 Cyclops, 9 Gelatinous cube, 10 Ettin, 11 Mimic, 12 Lizard man, 13 Minatour, 14 Carrion creeper, 15 Tangler, 16 Gremlin, 17 Wandering eyes, 18 Wraith, 19 Lich, 20 Invisible seeker, 21 Mind whipper, 22 Zorn, 23 Daemon, 24 Balron | RAM | verified (all 25) |
| A dungeon fight away from the entry ladder | the (1,1) shortcut shows the ladder up through the ceiling in every frame. Mt. Drash II level 1 map (`mdungeon`): clear its three monsters (`poke:19FE0=FFFF,poke:19FA0=FFFF,poke:1A000=FFFF`), face north (`poke:19CA2=03`), stand at (5,6) (`TPOS2:05:06`: doors both sides, wall ahead) with the monster at (5,5) (`poke:19E88=KK00,poke:19E8C=HHHH`), or at (5,7) to see it two squares off (`19E78`/`19E7C`). Cell address: 19CA6 + x*0x58 + y*8. A kill frame mid-corridor cannot be caught: a new monster is placed and attacks in the same turn | RAM | verified (`battle_*_corridor`, `env_dungeon_*`) |
| Chest or coffin under the hero in a dungeon | `poke:19D0A=0400` (chest) / `0500` (coffin) before `TPOS2:01:01` | RAM | verified |
| Choose a roll | `poke:115CC=XXXX` right before the key that rolls (pub tips: 00F0 space, 0030 princess, 0050 Mondain, 0010 lakes; castle weaponry theft: 0060 Light Sword, 0080 Blaster; jester hit: 0000) | RAM, code | verified |
| Kill a castle person in one blow | the people table 19C1C + 8*i (hit points, type, x, y; jester in Lord British's castle i = 7: `poke:19C54=0100`, `freeze:19C58=24000700` keeps him beside the hero at (23,07)) | RAM | verified |
| Space: sure hit, Space Ace | `poke:9A32=96004600,poke:9A3A=0600,f` hits; `poke:E922=1300` makes the next kill the 20th | RAM | verified |
| Space: into the sun | `poke:B9F2=A0004600,up` (late character's lift-off sector) | RAM | verified |
| Debug menus, level select | none found (no TCRF page reachable; nothing in the ROM text) | | |

### Saves (rom/saves/ultima/, never committed)
None downloaded (GameFAQs refuses automated access). Made here: `saves/01_start.sav`, `saves/02_endgame.sav`,
`saves/03_midgame.sav` (capture), `saves/04_first_trip.sav` (start set, honest)
(see `saves/README.md`).

## RAM map (for `game.json` "ram" watches and pokes)
OUT.EXE runs at segment 01AD; its data segment is 0EF5 (physical 0EF50). The **player record** (820 bytes, the
same bytes as PLAYERn.U1 and INUSE.U1) is at **129C8** in OUT.EXE and at **9498** in MONDAIN.EXE (SPACE.EXE: not
searched). Words are little-endian. Offsets into the record:
| Offset | Address (OUT) | Size | Meaning | How found |
|---|---|---|---|---|
| +00 | 129C8 | 16 | name | file + memory |
| +10 / +12 | 129D8 / 129DA | 2 | race / class as the list index (0 Human/Fighter, 1 Elf/Cleric, 2 Dwarf/Wizard, 3 Bobbit/Thief). ~~twice the list index~~: a new thief has 3 here (capture 2026-11-19, peeked); the steal and chest-trap code compares the class with 3 | code, RAM |
| +14 | 129DC | 2 | sex (0 male, else female) | poke, Ztats |
| +16 | 129DE | 2 | hit points | file, Ztats |
| +18..+22 | 129E0..129EA | 2 each | Strength, Agility, Stamina, Charisma, Wisdom, Intelligence | file, Ztats |
| +24 | 129EC | 2 | coin in copper pence (max 9999) | file, shop |
| +26 | 129EE | 2 | experience (level = experience / 1000 + 1) | code |
| +28 | 129F0 | 2 | food | file |
| +2A / +2C / +2E | 129F2 / 129F4 / 129F6 | 2 | readied weapon / spell / armour (list index) | poke, Ready |
| +30 | 129F8 | 2 | vehicle in use (0 on foot) | code |
| +34 / +36 | 129FC / 129FE | 2 | overworld x / y | RAM diff |
| +3A + 2*k | 12A04.. | 2 | quest of castle k (1 Lord British .. 8 Shamino): -1 given, 1 done (go back), 0 none | code |
| +4C..+52 | 12A14..12A1A | 2 each | red, green, blue, white gems | code, Ztats |
| +54..+5E | 12A1C.. | 2 each | armour owned: Skin (-1), Leather armor, Chain mail, Plate mail, Vacuum suit, Reflect suit | poke, Ztats |
| +60..+7E | 12A28.. | 2 each | weapons: Hands (-1), Dagger, Mace, Axe, Rope & Spikes, Sword, Great Sword, Bow & Arrows, Amulet, Wand, Staff, Triangle, Pistol, Light Sword, Phazor, Blaster | poke, Ztats |
| +80..+94 | 12A48.. | 2 each | spells: Prayer (-1), Open, Unlock, Magic Missile, Steal, Ladder Down, Ladder Up, Blink, Create, Destroy, Kill | file, ROM text |
| +96..+A4 | 12A5E.. | 2 each | vehicles: Foot (-1), Horse, Cart, Raft, Frigate, Aircar, Shuttle (+A2), Time Machine (+A4) | file, code |
| +A6 | 12A6E | 2 | enemy vessels destroyed (20 = space ace) | code (Ztats, princess) |
| +AA | 12A72 | 2 | overworld object count (saved copy) | code |
| +AC | 12A74 | 4 | game moves (saved copy) | code |
| +B0 / +B2 | 12A78 / 12A7A | 2 | ship shield / fuel (1000 each for a new shuttle) | file diff |
| +B4 + 16*i | 12A7C.. | 16 | overworld objects (i = 0 the player; up to 39): type, flag, x, y, hit points | code (0xB502) |
Live variables outside the record (OUT.EXE):
| Address | Size | Meaning | How found |
|---|---|---|---|
| 17AF6 | 2 | overworld object count (last index) | code |
| 17AF8 | 4 | game moves (shops: 3,000+ for aircar, shuttle, vacuum and reflect suits) | code |
| 17AEA | 2 | place type (0 overworld, 2 castle, 3 dungeon) | code |
| 17AEE | 2 | princess freed | code, verified |
| 17AF0 | 2 | prison key held | code, verified |
| 19C8E / 19C90 | 2 | town, castle and dungeon x / y | RAM diff |
| 19C92 | 2 | ~~dungeon level - 1~~ the map number of the town/castle buffer (town plans 2-9, castle plans 0-1; 0 outdoors and in dungeons) | code, RAM (capture) |
| 19CA0 | 2 | dungeon level (1-10; 0 = overworld). Poke it before `TPOS2` to show "Level N" and get that depth's monsters | code (K-limb), verified |
| 19C9A | 2 | place id (1-84, as in `worldmap.py`) | code |
| 19CA2 | 2 | dungeon facing: 1 West, 2 East, 3 North, 4 South (all four verified; ladders need 3 or 4) | RAM, verified |
| 19CA6 | 968 | dungeon level map, 11x11 cells of 8 bytes at 19CA6 + x*0x58 + y*8: +0 square (0 corridor, 1 wall, 2 secret door, 3 door, 6 ladder down, 7 ladder up, 8 force field; 4, 5, 9, 10 look like corridor), +2 monster (FFFF none, else the dungeon monster id 0-24, see Shortcuts), +4 item on the floor (4 chest, 5 coffin), +6 monster hit points. Cell (2,1) = 19D5E, (1,1) = 19D06 | code, verified |
| 19C96 | 2 | town alarm (1 = the next theft is caught) | code, verified |
| 19C98 | 2 | ales drunk in this pub visit | code |
| 115CC | 2 | the random number generator's state (advances only when the game rolls: poke it right before a roll to choose the outcome) | code, verified |
| 17AFE | 3 x 684 | town/castle map buffer, map number 19C92: 17AFE + n*0x2AC, column-major (x*18 + y, 38 x 18). Shop floor squares: 3E transport, 36/37 armour (customer/merchant side), 3A/3B weapons, 38/39 food, 3C magic, 3D pub; counters 0B-10. Steal works on 37, 3B, 39 (behind the counter) | RAM, code |
| 19C1C + 8*i | 8 | town people: hit points, type, x, y (castles: entry 0 = princess type 16, guards 11, jester 13) | RAM, verified in Lord British's castle |
MONDAIN.EXE (data segment 0744, physical 07440): record at 9498 (hit points 94AE); Mondain's hit points 756E
(1000); his form 7680 (2 wizard, 0B bat); gem destroyed 7688 (code + verified).

SPACE.EXE (capture 2026-11-19; code segment 01AD, data segment 08DA = physical 8DA0; disassembly from the file
after its 512-byte header, data at module offset 0x72D0): record at E87C (kills +A6 = E922, verified: poke 13 =
19 before the 20th kill shows the Space Ace box); gun sight x/y 8EDA/8EDC (159, 79); current enemy x/y
9A32/9A34 and its distance index 9A3A (0 far .. 6 near; a hit needs the enemy inside the sight's box for that
distance: poke 9A32=96004600 and 9A3A=0600 then `f` always hits); current sector 8F8E/8F90 (3,3 at lift-off);
sector table at 8DA0+0x26C0 + sx*0x196 + sy*0x3A: 10-byte header (enemy count, sun x/y, starbase x/y) and objects
of 12 bytes (x, y, type, shield, fuel, heading); the player's object index at EBB4 (2 at lift-off: object at
B9F2); velocity 8EC8/8ECA; docking port tables 988E (x) / 98A6 (y), 4 ports x 3 ship types.

## Emulation notes
- **Model `svga-500`.** GOG's config: `machine=svga_s3`, `cycles=500`, `core=simple`, `sbtype=sb16`. 500
  cycles is GOG's choice (a little faster than a 4.77 MHz PC); the game is turn-based (monsters move when the
  player moves or passes), the attract loop and the countdown look right at this speed, keys are not lost with the
  default press. The game detects EGA on `svga` and uses the 16-colour files; `svga` reloads states exactly
  (dos.md: `cga`/`tandy` lose the palette). No sound-device prompt (PC speaker).
- **Program switches work with savestates and the cache** (verified 2026-11-19, `tools/cachecheck.py`, run again after the coordinator's play.py fix: all same):
  all 22 checkpoints rebuilt from an empty cache give the same frames and the same written files (PLAYER1.U1,
  INUSE.U1) as cache hits, including those after GEN -> ULTIMA -> OUT, OUT -> SPACE -> OUT and OUT -> MONDAIN;
  a Q save after a cache hit of `landed` writes the same PLAYER1.U1 as the whole route from power-on.
- Files written: PLAYER1.U1 (GEN at "Save this character", Q outdoors), INUSE.U1 (before each program switch).
- The status panel is not redrawn after pokes (see Strategy).
- After `TPOS` the old player picture stays until a redraw: the macro does Ztats + space.
- The map does not follow a poked position until the player object moves too (`WARP` pokes both).

## Checkpoints
`checkpoints.txt` (27): `title`, `menu`, `gen` (GEN.EXE), `start` (OUT.EXE), `britian`, `lb_king`, `dungeon`,
`skeleton`, `shuttle`, `space` (SPACE.EXE), `landed` (back in OUT), `endgame` (from save 02_endgame),
`princess_freed`, `rescued`, `time_machine_found`, `time_machine` (MONDAIN.EXE), `mondain`, `gem_destroyed`,
`hit_mondain`, `mondain_bat`, `victory`, `ending`; added by the capture: `mid` (save 03_midgame on the
overworld), `mdungeon` (mid character in the Mines of Mt. Drash II, level 1), `eshuttle` (late character, shuttle
bought), `espace` (late character lifted off), `ejump` (late character after a hyperjump, an enemy fighter in
view). The scout's `shuttle`, `space` and `landed` (start character with poked coin) are no longer used by shots;
the set uses the late-character versions.

## Tools
- `tools/try.py FILE [--frames K] [--peek ADDR:LEN] [--crop x0,y0,x1,y1] [--cols N]`: many routes in parallel,
  one sheet (`work/scout/ultima/try_NAME.png`) (copied from Wizardry III).
- `tools/cachecheck.py`: every checkpoint rebuilt from an empty cache vs a cache hit (frames and written files), plus Q saves after `landed` and `skeleton` against the whole route from power-on (all same, 2026-11-19, 70 s).
- `tools/shops.py [--castles]`: where to stand at each shop counter in all 32 towns (from checkpoint `mid`).
- `tools/worldmap.py --list | --png OUT`: the 84 places (id, kind, continent, x, y, name) and a map picture from
  MAP.BIN and OUT.EXE.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| The game's programs (ROM text, code) | `rom/ultima.zip` | commands, names, prices, quest rules, RAM | 2026-11-19 |
| Wikipedia, Ultima I | https://en.wikipedia.org/wiki/Ultima_I:_The_First_Age_of_Darkness | release history, 1986 remake changes, quest outline | 2026-11-19 |
| Ultima I manual scans (archive.org full text) | https://archive.org/details/Ultima_I-Manual , https://archive.org/details/c64man_ultima1 | monster and spell names, space flight description (OCR, garbled) | 2026-11-19 |
| Unavailable | shrines.rpgclassics.com, guides.gamercorner.net, wiki.ultimacodex.com (outside the network); GameFAQs, TCRF, StrategyWiki (403) | | 2026-11-19 |

## Open questions
- ~~SPACE.EXE: enemy ships, firing, docking, ship choice and the Space Ace message not played~~ played except
  docking (capture): every placement on a free port collided ("Crunch!"); the port tables and the dock code are in
  the RAM map. Next try: approach a port at different speeds from further out, or the CGA model.
- ~~Dungeon: level change by ladders and spells, the facing values, coffins~~ done (capture).
- ~~Which towns sell which weapons and spells~~ done: by town parity and game time (design/systems.md 3.5).
- ~~The king's pence offer, landmark statistics~~ done: 3 hits per 2 pence; (value + 8) / 10 per landmark. The
  Eastern Sign Post gave nothing seen; Lord British's 8 Strength may be a formula too (one sample).
- Thieves stealing on the overworld, the pub seduction: not seen. ~~Iolo the Bard's and the jester's songs~~ seen
  in set `start` (`17_jester_sings`, `31_iolo_sings`); what triggers them is not read from the code.
- Where the jester stands in every castle and which cell holds the princess (random per entry: two cells).
