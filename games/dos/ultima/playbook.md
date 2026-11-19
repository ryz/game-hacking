# Ultima I: The First Age of Darkness (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"ROM text" = read from the game's own programs (`strings` on OUT.EXE, SPACE.EXE, MONDAIN.EXE), "code" = read
from OUT.EXE / MONDAIN.EXE with ndisasm (offsets are file offsets after the 512-byte EXE header).

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
Main set, to the ending. Routes from checkpoints; ids are the shot ids for `shots.txt`. Three lenses: S =
systems row, I = interface row, C = content row it serves.
| # | id | category | What / where | How to reach | Lens |
|---|---|---|---|---|---|
| 1 | `boot_title_text` | boot | text title "Ultima I / The First Age of Darkness" | `BOOT,w200` | I |
| 2 | `boot_origin` | boot | Origin Systems logo "Presents..." | `BOOT,w1000` (pick frame) | I |
| 3 | `title_castle` | title | castle picture "Ultima I" | `@title` | I, C |
| 4 | `boot_credits` | boot | credits card "Conversion by: John Fachini" | `BOOT,w300,space,w200` | I |
| 5 | `menu_main` | menu | Generate new character / Continue previous game | `@menu` | I |
| 6 | `gen_points` | menu | Character Generation, 30 points | `@gen` | S, I |
| 7 | `gen_stats_done` | menu | points distributed (0 left) | `@gen` + the stat keys of `CREATE` | S |
| 8 | `gen_race` | menu | race list (Human, Elf, Dwarf, Bobbit) | ... `space,w60` | S, C |
| 9 | `gen_class` | menu | class list after race and sex | ... `a,w60,a,w60` | S, C |
| 10 | `gen_save` | menu | "Save this character? (Y-N)" with ryz | ... name, `enter` | I |
| 11 | `menu_select` | menu | Character Selection 1) ryz | `@menu`-like, `b,w200` | I, S (four slots) |
| 12 | `start_overworld` | gameplay | first moment of control, castle to the west | `@start` | S, I, C |
| 13 | `hud_status` | hud | status panel Hits/Food/Exp./Coin and the message log | `@start` (crop not needed) | I |
| 14 | `inventory_ztats` | inventory | Ztats at the start | `@start,z,w60` | I, C |
| 15 | `inventory_ztats_late` | inventory | Ztats late game (gems, enemy vessels, blaster) | `@endgame,z,w60` | S, C |
| 16 | `gameplay_inform` | gameplay | I: "You are in the lands of Lord British" | `@start,i,w100` | S |
| 17 | `gameplay_continents` | gameplay | one overworld shot per continent (mountains, sea) | `@start,WARP:x:y` (e.g. 95,30 / 30,95 / 95,95) | C |
| 18 | `gameplay_britian` | gameplay | town Britian with shop signs | `@britian` | C, I |
| 19-24 | `shop_transport`, `shop_armour`, `shop_weapons`, `shop_magic`, `shop_food`, `shop_pub` | shop | each counter: `TPOS:07:05`, `06:0C`, `0C:0C`, `17:03`, `17:0C`, `20:05` + `t,w100,b,w100` | `@britian` | S (economy), I, C |
| 25 | `shop_transport_space` | shop | Aircar and Shuttle on sale | `@start,set:17AF8=4127:2,GO:27:27,TPOS:07:05,t,w100,b,w100` | S |
| 26 | `shop_sold` | shop | "Sold!" | `@britian`, transport, `a` | I |
| 27 | `gameplay_castle` | gameplay | Castle of Lord British: hall, prison, king | `@lb_king` | C |
| 28 | `dialogue_king_offer` | dialogue | "Dost thou offer pence or service:" | `@lb_king,t,w100` | I |
| 29 | `dialogue_king_quest` | dialogue | "Go forth and find The Grave of the Lost Soul" | `@lb_king,t,w100,s,w150` | S (quests) |
| 30 | `dialogue_king_pence` | dialogue | buying hit points from the king: "How much?" | `@lb_king,t,w100,p,w100` (verified), then an amount and `enter` | S |
| 31 | `system_landmark_grave` | system | The Grave of the Lost Soul "VAE VICTIS"; after it "A quest has been completed!" "Thou dost gain 2 Stamina" | `@lb_king,t,w100,s,w150,space,w60,poke:19C8E=00,poke:19C90=09,left,w200,WARP:62:58,e,w200` (+`space,w100`) (verified) | S, C |
| 32 | `dialogue_quest_done` | dialogue | back at Lord British: "Ah, ryz! Thou hast completed thy quest. For this I will give thee 8 points of strength." | route of 31 + `space,w100,GO:28:26,TPOS:21:05,t,w100,s,w150` (verified) | S |
| 33 | `dialogue_gem` | dialogue | a gem king: "The king gives thee a red gem" | Lost King (20,1B), quest, poke the quest done (record +0x3E = 1), T | S, C |
| 34 | `gameplay_dungeon` | gameplay | dungeon corridor with a chest, Level 1 | `@dungeon` | C, I |
| 35 | `battle_skeleton` | battle | Attacked by Skeleton | `@skeleton` | S, C |
| 36-39 | `battle_dungeon_*` | battle | three or four deeper monsters (Gelatinous cube, Carrion creeper, Lich, Balron) | dungeon level poke (record/level byte) or ladders; walk until met | C |
| 40 | `gameplay_coffin` / `gameplay_chest` | gameplay | Open a coffin or chest, "Thou dost find ..." | `@dungeon,up,w60,up,w60,o,w60` | S |
| 41 | `battle_overworld` | battle | an overworld monster attacks (Thief, Orc, Knight, Evil trent) | `@start,SPAWN-like poke: 12A8C=<type>000100320028005200...,17AF6=01,space,w60,a,w30,right` (types 23-30 hex) | S, C |
| 42 | `gameplay_vehicles` | gameplay | horse, cart, raft, frigate (bought in Britian), at sea with a frigate | `@britian` transport, leave, `b` | S, C |
| 43 | `system_frigate_fire` | system | frigate cannons at a sea monster | frigate + sea monster spawn, `f` | S |
| 44 | `gameplay_aircar` | gameplay | aircar | as 25, buy `e` | C |
| 45 | `gameplay_shuttle` | gameplay | shuttle parked by Britian | `@shuttle` | C |
| 46 | `system_liftoff` | system | countdown "10..9..8.." | `@shuttle,up,w60,b,w150` (pick frame) | S, I |
| 47 | `gameplay_space_top` | gameplay | space, top view: Sosaria, sun, starbase | `@space` | C, I |
| 48 | `map_sector_scan` | map | Sector Scan, 49 sectors | `@space,i,w100` | I, S |
| 49 | `gameplay_space_front` | gameplay | front view starfield | `@space,v,w60` | I |
| 50 | `system_hyperjump` | system | "Lightspeed!" streaks | `@space,v,w60,h,w60` (pick frame) | S |
| 51 | `battle_space` | battle | enemy fighters in front view, firing | hyperjump to a sector with enemies (Sector Scan), `f` | S, C |
| 52 | `system_space_ace` | system | "Thou hast achieved the rank of Space Ace!" | kill count poked to 19 (record +0xA6) before lift-off, then one kill | S |
| 53 | `system_starbase` | system | Docked! Welcome to base!, Choose thy ship | fly onto the starbase | S, I |
| 54 | `system_landing` | system | "Thou hast landed safely!" | `@landed` | S |
| 55 | `system_jester_key` | system | kill the jester: "I've got the key!" | `@lb_king`, walk to the jester (24,07), `a` | S |
| 56 | `system_cell_open` | system | "The door is open!" princess free | `@princess_freed` | S |
| 57 | `system_princess_reward` | system | "Thou hast saved the princess Julia ... time machine far to the northwest!" | `@rescued` | S, C |
| 58 | `gameplay_time_machine` | gameplay | the time machine on the overworld | `@time_machine_found` | C |
| 59 | `cutscene_time_machine` | cutscene | the four holes R G B W | `@time_machine` | S, I |
| 60-62 | `cutscene_launch`, `cutscene_pulled`, `cutscene_face_to_face` | cutscene | the three following pages | `@time_machine,space,w300` (x1, x2, x3) | C |
| 63 | `boss_mondain` | boss | Mondain's chamber | `@mondain` | C |
| 64 | `boss_gem_destroyed` | boss | "Get (Gem)... 2196 damage! The Gem is DESTROYED!" | `@gem_destroyed` | S |
| 65 | `boss_hit_mondain` | boss | "Hit Mondain! 51 damage!" | `@hit_mondain` | S |
| 66 | `boss_mondain_bat` | boss | Mondain as a bat | `@mondain_bat` | C |
| 67 | `ending_victorious` | ending | "Mondain is dead!" "THOU ART VICTORIOUS!" | `@victory` | S |
| 68 | `ending_text` | ending | the ending text, "Press CONTROL-ALT-DEL to Restart" | `@ending` | C, I |
| 69 | `gameover_dead` | gameover | "ryz, thou art dead", skull, "Attempting resurrection!" | lift off in a shuttle spawned without fuel: `@start,SPAWN:11:31:27,space,w60,up,w60,b,w300,w900`; or hits poked to 1 before a fight | S, I |
| 70 | `save_quit` | save | "Quit - saving game...saved." | `@start,q,w200` | S, I |
| 71 | `system_pub_tip` | dialogue | a tavern keeper's tip ("Thou had best know about space travel...") | pub, `t,b` repeated | S |
| 72 | `system_steal` | system | Steal at a counter, "Oh no! Thou wert caught!" | shop counter, `s` | S |
| 73 | `system_spell_cast` | system | a spell in a dungeon (Magic Missile / Ladder Down) | buy at Mad Chad's, `r,s`, `c` in a dungeon | S, C |
More gameplay shots for breadth: each continent's towns look alike but three town layouts and two castle
layouts exist (Wikipedia: remake added a castle variant and three town maps): take one of each.

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
| Debug menus, level select | none found (no TCRF page reachable; nothing in the ROM text) | | |

### Saves (rom/saves/ultima/, never committed)
None downloaded (GameFAQs refuses automated access). Made here: `saves/01_start.sav`, `saves/02_endgame.sav`
(see `saves/README.md`).

## RAM map (for `game.json` "ram" watches and pokes)
OUT.EXE runs at segment 01AD; its data segment is 0EF5 (physical 0EF50). The **player record** (820 bytes, the
same bytes as PLAYERn.U1 and INUSE.U1) is at **129C8** in OUT.EXE and at **9498** in MONDAIN.EXE (SPACE.EXE: not
searched). Words are little-endian. Offsets into the record:
| Offset | Address (OUT) | Size | Meaning | How found |
|---|---|---|---|---|
| +00 | 129C8 | 16 | name | file + memory |
| +10 / +12 | 129D8 / 129DA | 2 | race / class, as twice the list index (0 Human/Fighter, 2 Elf/Cleric, 4 Dwarf/Wizard, 6 Bobbit/Thief) | code (Ztats) |
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
| 19C92 | 2 | dungeon level - 1 | code |
| 19C9A | 2 | place id (1-84, as in `worldmap.py`) | code |
| 19CA2 | 2 | dungeon facing (seen: 1 West, 2 East, 3 North, 4 South) | RAM, verified |
| 19C1C + 8*i | 8 | town people: hit points, type, x, y (castles: entry 0 = princess type 16, guards 11, jester 13) | RAM, verified in Lord British's castle |
MONDAIN.EXE (data segment 0744, physical 07440): record at 9498 (hit points 94AE); Mondain's hit points 756E
(1000); his form 7680 (2 wizard, 0B bat); gem destroyed 7688 (code + verified).

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
`checkpoints.txt` (22): `title`, `menu`, `gen` (GEN.EXE), `start` (OUT.EXE), `britian`, `lb_king`, `dungeon`,
`skeleton`, `shuttle`, `space` (SPACE.EXE), `landed` (back in OUT), `endgame` (from save 02_endgame),
`princess_freed`, `rescued`, `time_machine_found`, `time_machine` (MONDAIN.EXE), `mondain`, `gem_destroyed`,
`hit_mondain`, `mondain_bat`, `victory`, `ending`.

## Tools
- `tools/try.py FILE [--frames K] [--peek ADDR:LEN] [--crop x0,y0,x1,y1] [--cols N]`: many routes in parallel,
  one sheet (`work/scout/ultima/try_NAME.png`) (copied from Wizardry III).
- `tools/cachecheck.py`: every checkpoint rebuilt from an empty cache vs a cache hit (frames and written files), plus Q saves after `landed` and `skeleton` against the whole route from power-on (all same, 2026-11-19, 70 s).
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
- SPACE.EXE: enemy ships, firing, docking, ship choice and the Space Ace message not played; its RAM (kill
  counter) not searched (the record's +A6 is read at lift-off).
- Dungeon: level change by ladders (`k`) and by spells, the facing values for all four directions, coffins.
- Which towns sell which weapons and spells (each town shows a subset; the 1,500-move "eras" in the weapon shop code).
- The king's "pence" offer (hit points per pence), landmark statistics per landmark, whether the strength reward is always 8.
- Thieves, gremlins and the Pub's wench/lecher text not seen.
- Where the jester stands in every castle and which cell holds the princess (random per entry: two cells).
