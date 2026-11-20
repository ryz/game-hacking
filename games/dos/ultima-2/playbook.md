# Ultima II: The Revenge of the Enchantress (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"ROM text" = read from ULTIMAII.EXE or the TLK files; "code" = read from ULTIMAII.EXE with ndisasm (offsets are
code offsets = file offset - 0x200; the program is a COM-style EXE: CS = load segment 01A8, IP = code offset).

> **Tools moved (2026-11-20).** Where this playbook says `try.py`, `cachecheck.py` or `screen.py` (copies that
> lived in this game's `tools/`), use the shared tools: `python3 tools/preview.py dos/ultima-2 FILE` (`--frames K` is now
> a `?` mark inside the route or `--timeline N:STEP`; sheets in `work/preview/dos/ultima-2/`), `python3
> tools/cachecheck.py dos/ultima-2` (`--after TOKENS` for a save in the game, `--peek ADDR:LEN` for party tables) and
> `python3 tools/play.py text` / `preview.py --text` for text screens. Pictures are native size
> (`play.py shot --scale N` on demand).

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Ultima II: The Revenge of the Enchantress (title picture "Ultima II / Revenge of the Enchantress", menu "ULTIMA ][ REVENGE OF THE ENCHANTRESS") (verified) |
| Platform / model used | IBM PC / MS-DOS, CGA 320x200 4 colours (cyan/magenta/white palette) for play, 40-column text mode for menus, generation and Ztats; `game.json` model `svga-500` (see Emulation notes) (verified) |
| Release (region, year) | Original IBM PC version 1983 (Sierra On-Line); this is the later Origin release, menu "(C)-1983,1989 BY LORD BRITISH AND ORIGIN" (verified), as sold by GOG (folder `Ultima II/`, 111 files, one program ULTIMAII.EXE; SHA-1 in `game.json`). Wikipedia: Apple II 1982, IBM PC CGA and PC speaker only, CPU-timed (source) |
| Developer / publisher | Richard Garriott (Lord British); Sierra On-Line originally, Origin Systems for the re-release (source: Wikipedia) |
| Genre | Single-character RPG: top-down overworld in five time periods, towns and castles, first-person wireframe dungeons and towers, rocket flight to nine planets |
| Players / save system | 1 player, one character (file PLAYER). **Q on the surface of Earth saves** ("QUIT OR SAVE GAME. ONE MOMENT PLEASE!", play continues; writes PLAYER and the MONX file of the map) (verified); leaving a town also rewrites PLAYER (code) |

## Boot sequence
All macros are in `game.json`; every checkpoint was rebuilt from power-on in single runs (`tools/cachecheck.py`).
- Power-on starts ULTIMAII.EXE directly (one program in the ZIP, no DOSBox Pure menu). GOG's config only runs
  `ultimaII.exe` (cycles 500, svga_s3); its cloud-saves overlay is not reproduced.
- **Intro** (verified, `work/scout/ultima-2/boot2/sheet.png`): text "ORIGIN PROUDLY PRESENTS" (f60), "PART ][ OF
  THE #1 BEST SELLING FANTASY ROLE-PLAYING GAME BY LORD BRITISH" (f120), the CGA title picture (dragon head,
  "Ultima II Revenge of the Enchantress") from about f190 to f290, then the text menu from f300 on.
  `TITLE` = `w240` (checkpoint `title`); `MENU` = `w600` (checkpoint `menu` = `@title,w360`).
- **Menu** (text mode, `play.py text` reads it): "TYPE - 'D' - FOR A DEMONSTRATION, 'P' - PLAY A GAME OF ULTIMA
  ][, 'C' - CREATE A NEW CHARACTER, CHOICE:". `d` runs the demonstration: captions over the PIC* pictures
  ("BATTLE STRANGE CREATURES ACROSS THE FACE OF THE EARTH" over an overworld scene, "TRAVERSE DEEP DARK DEADLY
  DUNGEONS AND TALL TERRIFYING TOWERS" over a wireframe corridor, "AND CONQUER TIME ITSELF TO BATTLE MINAX THE
  ENCHANTRESS" over Minax's court, "SEARCH FOR CLUES IN CARELESS WORDS SPOKEN AT THE LOCAL PUB" over
  "SWASHBUCKLERS PUB AND PIZZA", ... about 300 frames each, then the title picture) (verified,
  `work/scout/ultima-2/demo/sheet.png`; ROM text lists also "PLEAD WITH MEDIEVAL KINGS FOR ASSISTANCE" and
  "TRAVEL THROUGHOUT THE GALAXY TO THE PLANETS OF OUR SOLAR SYSTEM").
- **Creation** `c` (checkpoint `gen`): "PLAYER GENERATION: POINTS LEFT TO DISTRIBUTE: 90", then Strength,
  Agility, Stamina, Charisma, Wisdom, Intelligence typed as numbers + Enter (one key per token), M/F, race
  1-4 (Human, Elf, Dwarf, Hobbit), type 1-4 (Fighter, Cleric, Wizard, Thief), name + Enter, "SATISFACTORY
  (Y/N)" `y` -> back to the menu, PLAYER written. A statistic below 10 (Wisdom 5 tried) clears the whole form
  and starts over (verified); 40 in one statistic was accepted. `STATS` types 25/20/15/10/10/10; Human adds
  Intelligence +5, Fighter Strength +20 (result Str 45 Agi 20 Sta 15 Cha 10 Wis 10 Int 15) (verified).
  `CREATE` = `c,w200,STATS,m,w60,1,w60,1,w60,r,y,z,enter,w60,y,w200`; `RYZ` = `MENU,CREATE`.
- `p` loads PLAYER and the map: `PLAY` = `p,w300`; `NEWGAME` = `RYZ,PLAY`; checkpoint `start` = ryz on the
  **1423 B.C.** surface at (14,14) in the woods: H.P. 400, food 399, exp. 0, gold 400, nothing owned (verified;
  the new-character file puts the player in period 2, which the sign calls "ANOS: 1423 B.C.", not 1990 A.D.).
- Saved game: `sav:01_start,MENU,PLAY` resumes where Q saved (verified for 01_start and 02_endgame).

## Controls
One key per command; the command echoes after "CMD:" in the four-line message area (bottom left) and asks for
what it needs (a direction is an arrow key). Verified 2026-11-19 from `start` unless noted
(`work/scout/ultima-2/try_cmds.png`).
| Context | Key | Action | Status |
|---|---|---|---|
| Surface, towns | arrows | move North/South/East/West; water: "SOUTH--INVALID MOVE!"; woods, grass, marsh walkable | verified |
| | (no key) | the game passes a turn by itself about once a second ("CMD: PASS"); monsters act on every turn | verified |
| | `space` | Pass | verified |
| | `a` | Attack: "ATTACK--" + direction; "--HIT!!!", "--MISS", "KILLED--GOLD+03--EXP.+04" | verified |
| | `b` | Board a horse, frigate, plane or rocket standing on its square ("BOARD ROCKET"; "BOARD WHAT?" elsewhere) | verified (rocket) |
| | `c` | Cast the readied spell ("CAST-NONE", "NEED WAND OR STAFF!") | prompt verified |
| | `d` | Descend a ladder (dungeons, towers) | prompt verified |
| | `e` | Enter the village, towne, tower, castle, dungeon or sign on the square ("ENTER-VILLAGE"); a sign: "-THE SIGN READS: ANOS: 1423 B.C." | verified |
| | `f` | Fire (vehicle guns) "FIRE WHAT?" | prompt verified |
| | `g` | Get ("GET WHAT?"; chests, weapons, armour on the floor: ROM text) | prompt verified |
| | `h` | Hyperwarp (space only; "HYPER WHAT?" elsewhere) | verified |
| | `i` | Ignite a torch ("IGNITE TORCH"; "NONE OWNED!") | verified |
| | `j` | "JUMP...WHEE..." | verified |
| | `k` | Klimb a ladder | prompt verified |
| | `l` | Launch the rocket or plane you are in ("LAUNCH WHAT?"); in space: request landing | verified |
| | `m` | Magic: "MAGIC SPELL READY #" (choose the readied spell) | prompt verified |
| | `n` | Negate time with a strange coin ("NEGATE TIME HOW? YOU'RE NOT EINSTEIN" without one) | verified (refusal) |
| | `o` | Offer gold: direction, "HOW MUCH (*100) ?" digit (see Game structure) | verified |
| | `q` | Quit or save game (surface of Earth only: "ONLY OUTDOORS!", "ONLY ON EARTH!") | verified |
| | `r` | Ready weapon: "1-DA, 2-MA, 3-AX, 4-BO, 5-SW, 6-GR, 7-LI, 8-PH. 9-QU, WHICH?" -> "QUICK SWORD READY." | verified |
| | `s` | Steal + direction ("NO LUCK!", "STEAL FOOD/ARMOUR/WEAPONS!" ROM text) | verified (NO LUCK) |
| | `t` | Transact + direction: shops over a counter, people talk | verified |
| | `u` | Unlock + direction (a key; "NO DOOR THERE!", "NO KEYS THAT FIT!") | verified ("NO DOOR THERE!") |
| | `v` | View ("VIEW WHAT?"; with a magical helm: ROM text) | prompt verified |
| | `w` | Wear armour: "1-CLOTH, 2-LEATHER, 3-CHAIN, 4-PLATE, 5-REFLECT, 6-POWER, WHICH?" | prompt verified |
| | `x` | X-it the vehicle | verified (rocket) |
| | `y` | Yell ("YELL WHAT?") | prompt verified |
| | `z` | Ztats (text screen: level, sex, race, type, readied weapon/armour/spell, torches, keys, tools, six statistics, owned weapons, armour, spells, items), any key back | verified |
| Dungeon, tower | `up` Advance ("-BLOCKED!"), `left`/`right` turn, `down` Retreat; `k`/`d` ladders; `i` torch (dark without: "IT'S DARK!") | | verified (up, left, right, down, i) |
| Space | arrows LEFT/RIGHT/CLIMB/DIVE (ROM text), `h` hyperwarp: three digits XENO, YAKO, ZABO; `l` landing request; any key while drifting over a planet = touch down | | h, l, landing verified |
| Prompts | digits and letters as shown; `y`/`n` | | verified |

Input timing: the default press (hold 8, wait 40) works everywhere at 500 cycles; `type:` was not needed (names
one key per token). Town entry `w300`; leaving a town `w300`; launch `w400`; a hyperwarp takes about 1,200
frames (`w1200`) before "YOU ARE ORBITING ...".

## Game structure
Facts from the code and the map/talk files, checked in play where marked.
- **Five periods of Earth** (sign text, verified for 1423 B.C.): 0 Legends ("ANOS: LEGENDS!"), 1 Pangea
  ("ANOS: 9,000,000 B.C."), 2 "1423 B.C.", 3 "1990 A.D.", 4 "2112 A.D." (Aftermath). Each surface is a 64x64
  map (MAPX00..MAPX40; 1423 B.C., 1990 and 2112 share today's continents, Pangea is one continent, Legends a
  round island). Each period has at most one place of each kind; entering loads that kind's map
  (`tools/u2map.py --list`):
  | Period | Village (1) | Towne (2) | Castle (3) | Tower (4) | Dungeon (5) | Sign |
  |---|---|---|---|---|---|---|
  | 0 Legends | - | - | Shadow Guard (20,20) | - | - | (20,36) |
  | 1 Pangea | (14,37) | - | - | - | (1F,08) | (21,3A) |
  | 2 1423 B.C. | (26,2E) | Towne Linda (24,1D) | Lord British (23,16) | (18,28) | (19,05) | (3A,33) |
  | 3 1990 A.D. | (22,14) | New San Antonio (0F,1A) | (23,16) | (26,1F) | (19,05) | (3A,33) |
  | 4 2112 A.D. | (2C,0E) (CCCP test launch, rockets) | - | - | - | (19,05) | (3A,33) |
  Coordinates (x,y) hex. Files present: MAPX00/03, 10/11/15, 20-25, 30-35, 40/41/45 (1423 B.C. and 1990 share
  the castle map).
- **Time doors** (code 0x26F9, verified): a door appears on one of four fixed squares per period (table at
  CS:0x2798) after 256 turns, then moves to the next square every 8 turns (only onto open terrain). Stepping on
  it saves the current map and loads period k (slot k, skipping the current period) at slot k's square there.
  Door squares: Legends (1D,38) (1F,38) (21,38) (23,38) (the walled islet south of Shadow Guard); Pangea
  (22,08) (2F,1C) (24,38) (14,25); 1423 B.C. (10,10) (30,18) (2A,18) (13,34); 1990 (38,34) (1C,0C) (21,17)
  (14,34); 2112 (12,17) (32,22) (34,18) (08,0B).
- **Towns** (verified in Linda, New San Antonio, Lord British's castle): people walk about (guards, merchants,
  jesters, fighters, clerics, wizards, thieves); Transact talks ("A GUARD SAYS: PAY YOUR TAXES!", "A MERCHANT
  SAYS: WILL YOU BUY MY APPLES?", ROM text for the others); up to five named people per map speak their line
  from the TLK file. Leave by walking off the edge. Shops by map quadrant (code 0x1590): towne NW weapons, NE
  armour, SE transport (horses: "I SELL YOU HORSE 0084 GOLD, DEAL, OK?" verified in New San Antonio), SW pub
  ("WELCOME TO THE PUB! 1-BUY, 2-TIP", verified); village NW oracle ("TIME AND TRAVEL MADE ME WISE, PRECIOUS
  GOLD, A CLUE IT BUYS! HOW MUCH WILL YOU PAY *100?" ROM text), NE food ("THE FOOD HERE COSTS .. PER 100"), SE
  cleric spells (clerics only: "RYZ YOU ARE NOT A CLERIC!" verified), SW wizard spells (wizards only, verified).
  Counter squares: `tools/u2shops.py` (scan; some hits are scenery, check in play).
- **Lord British** (castle of 1423 B.C. and of 1990, throne at (1F,0D)): Transact from (1F,0E): "WELCOME MY CHILD
  RYZ, FIRST MY 50 G.P. TRIBUTE! AND FOR IT I RAISE THEE 0300" (verified: H.P. 400 -> 700, gold -50);
  ~~the raise is 300 below 500 H.P., 200 below 750, 100 below 1,000~~ the test reads the high BCD byte of H.P.:
  +300 below 5000, +200 below 7500, +100 below 9900, none above (code; verified 3184 -> 3484 in 1990, capture
  2026-11-19).
- **Quest chain to the ending** (code + verified with the late character):
  1. **Enilno, the quicksword**: Offer 500 gold (`o`, direction, `5`) to Santre the Swashbuckler (jail of New
     San Antonio, 1990 A.D., cell at (35,06); stand at (36,06)): "ENILNO IS YOURS!" (verified, `enilno`).
     Readying it needs Agility above 72 in the game's own count (Agility 49 or more on screen) (code).
  2. **Father Antos's blessing**: on planet X (9-9-9), in the castle Ozys Place, Transact with Father Antos at
     (01,30) from (02,30): "You have earned my blessing. Return and claim the Ring!" (verified, `blessing`).
  3. **The ring**: Offer 500 gold to the old man under "A TREE" in New San Antonio (19,02), from (1A,02):
     without the blessing "EARN THE RING!" (gold taken anyway), with it "THE RING IS YOURS!" (both verified).
  4. **Space**: rockets stand at the CCCP test launch of the 2112 A.D. village (21,03) (26,03) (2B,03).
     Boarding needs an **ankh** ("A METALIC VOICE COMMANDS: YOU MUST HAVE AN ANKH!" ROM text); launching needs
     **tri-lithium** ("SHIP INCAPABLE OF LAUNCH!" ROM text; one per launch and per hyperwarp) and armour 5 or 6
     worn (reflect or power), else "YOU HAVE EXPLODED!" (verified). Planets by XENO-YAKO-ZABO: Earth 6-6-6,
     Mercury 5-4-5, Venus 3-3-4, Mars 6-2-3, Jupiter 1-3-4, Saturn 2-8-5, Uranus 9-4-6, Neptune 4-0-5, Pluto
     0-1-4, planet X 9-9-9 (code table CS:0x7012); 4-4-4 is the sun ("YOU HIT THE SUN!"); elsewhere "YOU ARE IN
     DEEP SPACE." and landing "REQUEST DENIED!" (verified). A hyperwarp that leaves a tri-lithium count with its
     two lowest bits set (3, 7, 13 ...) goes "SHIP OFF COURSE!" to random coordinates (code; seen: 9-9-9 with 3
     left ended at 7-1-1). Landing: the rocket drifts over the planet map until a key is pressed and lands only
     on grass (else the crash path); on a planet the rocket waits where it landed; landing on Earth always
     arrives in 2112 A.D. (code 0x71F9, verified).
  5. **Shadow Guard** (Legends, castle at (20,20)): force fields (tile 5C) do 1,000 damage ("FIELD CAUSES 1000
     DAMAGE!") unless the ring is owned ("RING PROTECTS FROM FIELD!") (both verified). Minax waits in "CHAMBER
     ONE" (3C,03) with two winged guardians; each hit that does not kill her sends her to the mirrored chamber
     ("CHAMBER TWO", (03,3C)): "SHE'S GONE!!!". She casts every turn ("MINAX CRIES: DIE FOOL!", about 100-300
     H.P.; a green idol may save: "SAVED BY IDOL!") (verified). She has 255 hit points; damage = (weapon number x
     8 + Strength) / 4: quicksword 35 at Strength 45, 42 at 62; bare hands 17 (verified). The code does not
     demand the quicksword: a bare-handed blow kills her too once her hit points are low (verified with a poke).
  6. **Ending** (verified, `minax_dead`, `ending`): "MINAX IS DEAD!! ALL HER WORKS SHALL DIE!", the castle
     breaks apart square by square, then "YOU HAVE SAVED THE UNIVERSE, AND COMPLETED ULTIMA ][! SEEK NOW TO
     CONQUER WICKED EXODUS, FOUND IN ULTIMA ]I[-D ]II[-P!" over an endless scroll of the 1990 map with ryz as a
     rocket (no return to the menu).
- **Items** (Ztats ITEMS, code): ring (fields), wand / staff (needed to cast: "NEED WAND OR STAFF!"), boots
  (save from leg paralysis), cloak (arm paralysis), helm (View), gem, ankh (rocket), red gem, skull key (planes:
  "STRANGE YOU CAN'T GET IN!"), green gem, brass button (planes: "FUNNY THIS PLANE IS MISSING A BRASS
  BUTTON!"), blue tassle (frigates: "THE CREW OF THIS SHIP WILL NOT LET YOU BOARD!"), strange coin (Negate
  time: 20 turns), green idol (Minax's spell), tri-lithium (rocket fuel). Killing a thief gives a random item
  and sometimes tools; a fighter torches and sometimes a helm; a wizard a wand or a staff; a guard 2 keys (code
  0x2CC5). A deep dungeon level holds tri-lithium ("Lithium packs the 16th level!", TLKX33; code 0x3760).
- **Pub tips** (ROM text): "SOME FIGHTERS WEAR MAGIC HELMS!", "AVIATORS USE SKULL KEYS!", "SAYLORS WEAR BLUE
  TASSLES!", "MAGES CARRY WANDS OR STAFFS!", "GUARDS CARRY KEYS!", "ANKHS OPEN SPACE!", "PLANES NEED BRASS
  BUTTONS!". Talk lines of every TLK file: `tools/u2town.py` lists who stands where; the lines are in
  design/content.md.
- **Hotel clerk, Flopy Fighter** (code 0x3D52, 0x3D7E): offering gold to the 1990 towne's type-83 person (the
  Flopy Fighter, (37,23)) gives a random weapon ("HERE TAKE THIS!"); to the type-84 person (the Hotel California
  clerk, (0A,39)) raises a random statistic by 4 per 100 gold ("ALAKAZAM!" ROM text) (not tried).
- **Dungeons and towers** (verified entry): first-person wireframe, dark until a torch is lit (`i`); start at
  (5,5) on level 0 below a ladder up (dungeon) / above a ladder down (tower). 16 levels of 16x16 per map file
  (inferred from the 4,096-byte maps).

## Shot plan
**Done 2026-11-19 (capture):** set `main`, 226 shots from power-on to the ending, all plan groups covered; the
finished list is `shots.txt` (game order). Not captured: see the end of this section.

Planned main set (scout 2026-11-19): about 120 shots in game order, routes for those with checkpoints are in
`shots.txt` (plan lines are comments with the route to use). Categories: boot 2, title 1, menu 6, cutscene 6,
gameplay ~30, hud 1, system ~35, map 2, inventory 3, dialogue ~12, shop ~8, battle ~8, boss 6, gameover 1,
save 1, ending 3. Every command letter gets one shot (prompt or result). How to reach each group:
- Boot, title, demonstration, creation: `title`, `menu`, `gen` + typed values (also the reset by a value
  below 10).
- First moments: `start` (H.P. 400 etc.), Ztats new, the idle PASS, a blocked move, the 1423 B.C. sign, every
  command letter's prompt (sheet `work/scout/ultima-2/try_cmds.png` shows the frames), Q save.
- Towns: `village`, `linda`, `castle`, `lordbritish`, `nsa`; people talk by Transact (guard, merchant, jester,
  fighter, cleric, wizard, thief lines: poke ryz beside one with `POS`); shops from `tools/u2shops.py` (pub buy
  and tip, transport, food, oracle, armour and weapons where a merchant stands; cleric/wizard refusals, or make
  ryz a cleric/wizard with a poke of 8ED7 to see the lists); steal (no luck / caught by guards).
- Quest people: `enilno`, `earn_ring`, `ring`, `blessing`; the TLK lines of Brother Antos, the Sightless Sage,
  the Phylosopher ("She's GOT to be at 9-9-9!"), the astronauts ("There is a planet 'X'!").
- Periods and doors: `door` (the door picture), `legends_arrive`, the five signs, each surface once
  (`TIME:0q` + `POS`), Pangea's village and dungeon, 2112's launch site.
- Fights: `fight` (devil: hit, kill message); other pictures by poking object 1 (see Shortcuts): 2C serpent,
  30 devil, 34 man, 38 robed figure, 3C winged daemon, F0 fighter, F8 wizard, FC thief; a miss; ryz's death
  ("RYZ IS DEAD!", gameover).
- Dungeon/tower: `dungeon`, `tower` (corridor, turn, a ladder, Klimb/Descend, a monster, a chest).
- Space: `rocket`, the explosion without armour, `space`, the hyperwarp prompt and the starfield, `orbit_x`,
  deep space and "REQUEST DENIED!", the sun, off course, `landed_x`, `ozys`, other planets' surfaces and towns
  (MAPG files: Mercury dungeon, Mars town, Jupiter village/tower/dungeon, Uranus village, Neptune village, Pluto
  towns, planet X town).
- Endgame: `shadowguard`, `field` (and the 1,000-damage variant), `minax`, a real hit + "SHE'S GONE!!!" +
  Chamber Two (`SWING`), "SAVED BY IDOL!", `minax_dead`, the crumbling castle, `ending`.

- Not captured (with reason): Up ladder and Blink spells (both answered FAILED in their only try), Kill spell
  (same frame as magic missile), a fleeing monster, natural monster loot, Uranus village talk (no named people in
  its object list), selling (the game has none), the kings demonstration picture (file missing).

## Capture notes (2026-11-19)
How the set was made; reuse these before experimenting.
- **Random numbers:** one lagged generator (code 0x5217): state DS:0x23F-0x244 = physical 90CF-90D4; output =
  [240] + [243] + [244] + 1 with carries. `poke:90D0=00,poke:90D3=00,poke:90D4=FF` right before the deciding key
  makes the next output 0 (a hit, a trap, a successful steal); `...90D4=00` makes it 1 (the clerk's ALAKAZAM on
  Agility); `...90D4=7F` makes it 0x80 (a gold chest).
- **Shops:** Transact needs a counter (7C or a letter tile 80+) in front and the merchant picture 68 on the square
  behind it. Merchants wander: `tools/u2merch.py ROUTE OBJ X,Y` prints pokes that move the object (and its map
  picture) to the square behind the counter; put them after `POS` (the pass redraws the view) and before `t`.
- **Talk:** the named people (types 81-85) start on the squares `tools/u2town.py MAP` lists; `POS` beside them
  and `t` + direction works in the first turns; `gen_talk`-style routes (POS, u2merch, t) for moving ones.
- **Surface monsters:** `tools/u2mon.py ROUTE slot:x:y:pic:hp[:type]` writes object and map pokes with the right
  tile under the monster. Pictures: 30 devil, FC thief, 34 hooded man (legs), 2C sea serpent, F0 fighter, 48
  pirate frigate, 38 robed figure (arms), F8 wizard (magic missile), 3C winged daemon (sleep). With a monster at
  (12,13) beside the late ryz at (14,14) the special attack fires on the 6th `space,w40` (shots `battle_*`).
- **Dungeons:** all 16 levels are in RAM at A690 + level*256 + y*16 + x (00 floor, 80 wall, C0 door, E0 secret
  door, 10 ladder up, 20 ladder down, 40 chest, 1-7 a creature). Level 8EB5, position 8E90, facing 8E92/93 can be
  poked and a `space,w60` redraws. A creature = object (x, y, H.P., picture 1-7, under = level) plus its picture
  number in the level map; without the map byte it is neither drawn nor hit. Dungeon creature slots: slot k sits
  on level k/2. Tri-lithium chests: level 0F, (1-3,1), (1,2), (3,2), (1-3,3) in the 1423 B.C. dungeon.
- **Vehicles:** the player picture byte 8EA3 = 22 horse, 24 frigate, 26 plane, 28 rocket; poking it on the
  surface puts ryz in that vehicle (frigate shots). Vehicles stand in towns: horses New San Antonio (3A,32..3A),
  frigates Pirates Cove (22,0C/0E/10) and Port Bonifice, planes Pirates Harbour (04..0B,09..0A), rockets (21/26/2B,03),
  one of each in Shadow Guard (24..27,18). A launched plane leaves the town and lands; `l` again flies over the
  surface, arrows steer, `l` lands on grass only (route of `system_plane_landed`).
- **Planets:** grass landing squares beside the places: Mercury (2A,0C), Venus (20,1E), Mars (20,1E), Jupiter
  (09,07), Saturn (20,1E), Uranus (1B,25), Neptune (1F,1A), Pluto (25,1F), X (0C,0D) / (09,1E); routes
  `@space,WARP:x:y:z,l,w300,TOUCH:x:y,x,w60` (fuel 4 left, never off course).
- **Minax honestly:** from `minax`, swing at her square (`a` + direction), read 8FE6/9006 before each swing and
  go to the other chamber after every hit: 8 swings, 7 hits, ryz 3084 -> 600 H.P. (checkpoints `mx1`,
  `minax_honest`, `ending_honest`).
- **Unlock** works east/west only; the jail cells of Lord British's castle ((0E,27) (0E,2B) (0E,2F), stand east)
  are reachable doors.

## Strategy and walkthrough notes
- **Fastest route to the ending (verified, all checkpoints):** `hero` (late character by poke) -> `TIME:03`,
  `ENTER:0F:1A` (New San Antonio) -> `SANTRE` (quicksword) -> `LEAVE`, `ROCKET`, `LAUNCH`, `WARP:9:9:9`, `l`,
  `TOUCH:0C:0D`, `x`, `up`, `e` (Ozys Place) -> `BLESS` -> `RETURN` (back to 2112) -> `TIME:03`, `ENTER:0F:1A`,
  `OLDMAN` (ring) -> `LEAVE`, `TIME:00`, `ENTER:20:20` (Shadow Guard), `r`, `9` (ready the quicksword), north
  through the field -> `POS:3B:03` -> `poke:9026=14` and `a`, `right` -> ending after about 1,500 frames.
- The honest fight: 255 hit points, 42 per hit with the late character, 7 hits; after every hit she is in the
  other chamber: alternate `POS:3B:03,a,right` and `POS:04:3C,a,left` (`SWING`), but a miss leaves her where she
  was, so check her square (8FE6/9006) before each swing. She takes about 200 H.P. per turn.
- Honest outline (for captions; code + talk files): money from fights and thieves, Lord British for hit points,
  buy a horse, get a frigate (blue tassle from sailors) or a plane (skull key + brass button), keys from guards,
  the quicksword from Santre, an ankh and tri-lithium (thieves, dungeon level 16), reflect or power armour, the
  rocket from 2112, planet X for the blessing, the ring, the time door to Legends, Shadow Guard.
- Walking about towns is slow (real-time turns); use `POS` and the squares in this playbook.
- Values on the status panel redraw on the next turn after a poke (verified: H.P., gold); Ztats reads RAM.

## Naming
Main character **ryz**: typed in the generation's NAME prompt one key per token (`r,y,z,enter`); the game
shows names in capitals ("RYZ"). No other names.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Change period | `TIME:0q` (q = 0 Legends .. 4 2112) from any Earth surface: puts ryz on (16,12), points door slot 0 of every period at (17,12), patches the door's destination to period q for one step, steps on, restores code and table. Arrival at (17,12) (open grass in all five periods). Fails if (17,12) holds a vehicle (land the rocket on (0F,0F)) | code | verified (0, 1, 3, 4 from 1423 B.C.; 3 from 2112; 0 from 1990) |
| Position on a map | `POS:x:y` (hex) = poke x/y + a pass; the view follows on the pass. Works on surfaces, in towns and castles | RAM | verified |
| Enter a place | `ENTER:x:y` = `POS` + `e` (coordinates in Game structure) | RAM | verified (all kinds) |
| Leave a town | `LEAVE` (walk off the south edge from (1F,3F)) | RAM | verified |
| Late-game character | `HERO` (Str 62 Agi 71 Sta 48 Cha 37 Wis 26 Int 43, H.P. 3184, food 2463, exp. 2083 = level 20, gold 6382, light sword readied, reflect armour worn, weapons, armour, items incl. ankh, 6 tri-lithium, torches 7, keys 4, tools 3) | RAM | verified (Ztats) |
| Quest offers | `SANTRE`, `OLDMAN` (in New San Antonio, 500 gold each), `BLESS` (in Ozys Place), `KING` (Lord British's castle) | RAM | verified |
| Space | `ROCKET` (from a surface: to 2112, into the village, board), `LAUNCH`, `WARP:x:y:z`, `l` + `TOUCH:x:y` (land on a grass square), `RETURN` (from Ozys Place back to 2112 at (0F,0F)) | RAM | verified |
| Blessing | `poke:8EFC=01` | code | verified (ring given) |
| Quest items | ring `poke:8F66=01`, quicksword `poke:8F0F=01`, ankh `poke:8F6D=01`, tri-lithium `poke:8F75=06`, reflect armour `poke:8F2B=01,poke:8EF2=05` | RAM | verified |
| A monster beside ryz | object 1: `poke:8FC8=X,poke:8FE8=Y,poke:9008=HP,poke:9028=PIC,poke:9048=UNDER,poke:9068=TYPE` and the picture into the map at A690 + Y*64 + X (e.g. `poke:ABA3=30` for (13,14)); object 0 is never found by attacks. Type 3 stays and fights, 1 wanders | RAM, code | verified (devil at (13,14)) |
| Minax's hit points | `poke:9026=HH` (255 at start; she is object 31: x 8FE6, y 9006) | RAM | verified |
| Debug menus, level select, codes | none found (no web source reachable; nothing in the ROM text) | | |

### Saves (rom/saves/ultima-2/, never committed)
None downloaded (web hosts unreachable). Made here (committed): `saves/01_start.sav` (new ryz, Q at the start),
`saves/02_endgame.sav` (late ryz with Enilno, the ring and the blessing outside New San Antonio), see
`saves/README.md`.

## RAM map (for `game.json` "ram" watches and pokes)
The data segment is load segment + 0x741 = physical **8E90** (DS:0 = 8E90); code CS:0 = physical 1A80.
BCD = packed decimal, high byte first (the status panel shows the digits). The **player record** is DS:0x36..0x135
(physical 8EC6..8FC5) = the first 256 bytes of the file PLAYER.
| Address | Size | Meaning | How found |
|---|---|---|---|
| 8E90 / 8E91 | 1 each | x / y on the current map (0-63) | code, poke |
| 8E92 / 8E93 | 1 each | facing in dungeons and towers as a step (1,0 east; FF,0 west; 0,FF north; 0,1 south) | RAM |
| 8EA4 | 1 | the view square under the player (map tile / 2; boarding checks it) | code |
| 8EB5 | 1 | dungeon/tower level (0 at entry) | code |
| 8EC6 | 16 | name ("RYZ") | file |
| 8ED6 / 8ED7 / 8ED8 | 1 each | sex ('M'/'F'), type (0 fighter, 1 cleric, 2 wizard, 3 thief), race (0 human, 1 elf, 2 dwarf, 3 hobbit) | code (Ztats) |
| 8ED9 / 8EDA | 1 each | period (0 Legends, 1 Pangea, 2 1423 B.C., 3 1990, 4 2112; on a planet: the planet number) / map (0 surface, 1 village, 2 towne, 3 castle, 4 tower, 5 dungeon) | code, verified |
| 8EDB..8EE0 | 1 each, BCD | Strength, Agility, Stamina, Charisma, Wisdom, Intelligence | code, verified |
| 8EE1 | 2, BCD | hit points | verified |
| 8EE3 | 3, BCD | food (two digits pairs + a fraction byte) | verified |
| 8EE6 | 2, BCD | experience; the first byte is the level ("A LEVEL 20") | verified |
| 8EE8 | 2, BCD | gold | verified |
| 8EEA / 8EEB | 1 each | surface x / y saved on entering a place | code |
| 8EF0 | 1 | selects the kind of monster created on the surface (open) | code |
| 8EF1 / 8EF2 / 8EF3 | 1 each | readied weapon (0 hands .. 9 quicksword), worn armour (0 skin .. 6 power), readied spell | code, verified |
| 8EF4 / 8EF5 / 8EF6 | 1 each, BCD | torches, keys, tools | verified (Ztats) |
| 8EF9 / 8EFA / 8EFB | 1 each | rocket landed on a planet (1) and its square | code |
| 8EFC | 1 | Father Antos's blessing (1) | code, verified |
| 8EFD | 1 | planet (0 Earth, 1 Mercury .. 8 Pluto, 9 planet X, 10 deep space) | code, verified |
| 8EFE / 8EFF | 1 each | time-door slot x 2 / turns until it moves | code, verified |
| 8F06 + i | 1 each, BCD | weapons owned, i = 1 dagger, 2 mace, 3 axe, 4 bow, 5 sword, 6 great sword, 7 light sword, 8 phaser, 9 quicksword (8F0F) | code, verified |
| 8F26 + i | 1 each | armour owned, i = 1 cloth .. 5 reflect (8F2B), 6 power | code, verified |
| 8F46 + i | 1 each | spells owned, i = 1 light, 2 down ladder, 3 up ladder, 4 passwall, 5 surface, 6 prayer, 7 magic missile, 8 blink, 9 kill | code |
| 8F66 + i | 1 each, BCD | items, i = 0 ring (8F66), 1 wand, 2 staff, 3 boots, 4 cloak, 5 helm, 6 gem, 7 ankh (8F6D), 8 red gem, 9 skull key, 10 green gem, 11 brass button, 12 blue tassle, 13 strange coin, 14 green idol, 15 tri-lithium (8F75) | code, verified |
| 8FC7 + i, 8FE7 + i, 9007 + i, 9027 + i, 9047 + i, 9067 + i | 32 each | objects (people, monsters) of the current map: x, y, hit points, picture, tile under, type (0 still, 1-3 movement, 81-85 named talker). Minax = object 31 | code, verified |
| 90FA / 90FB / 90FC / 90FD | 1 each | turns left: time negated (coin), legs paralysed, arms paralysed, asleep | code |
| 935A..935C | 1 each | hyperwarp target XENO, YAKO, ZABO | code |
| 90CF..90D4 | 6 | random number state (code 0x5217); see Capture notes | code, verified |
| 8EA3 | 1 | player picture / vehicle: 22 horse, 24 frigate, 26 plane, 28 rocket | code, verified |
| 8F67 / 8F68 | 1 each | wand / staff (needed to cast) | code, verified |
| 90FB..90FC (DS 26B/26C) | 1 each | turns of leg / arm paralysis left (0-15) | code |
| A690 | 4096 | the current map (y*64 + x; tile = byte / 4: 0 water, 1 marsh, 2 grass, 3 woods, 4 mountains, 5 village, 6 towne, 7 tower, 8 castle, 9 dungeon, 10 sign; 11-14 horse, frigate, plane, rocket as map tiles 44/48/4C/50; door C0; in towns 70 floor, 78 wall, 7C counter, 68 merchant, A0 locked door, 5C force field) | code, verified |
| 4218 | 40 | time-door table (CS:0x2798): period p, slot k at 4218 + 8p + 2k (x, y) | code, verified |
| 8A92 / 8A9C / 8AA6 | 10 each | planet coordinates XENO / YAKO / ZABO (CS:0x7012) | code |

## Emulation notes
- **Model `svga-500`.** GOG's config: `machine=svga_s3`, `cycles=500`, `core=simple`. The program times itself
  with CPU loops (Wikipedia: too fast on anything but an 8088); at 500 cycles the intro, the hyperwarp and the
  idle PASS (about one turn per second) run at a plausible pace and no key is lost with the default press. The
  game draws CGA mode 4 (palette cyan/magenta/white); on `svga` the palette survives state loads: every
  checkpoint's frame is identical between an empty-cache rebuild and a cache hit (`tools/cachecheck.py`), so no
  `ega` machine is needed (dos.md's palette loss concerns the `cga`/`tandy` machines).
- **Files written** (verified): creation writes PLAYER; Q writes PLAYER and MONXpm (and MAPXpm when a map
  changed); entering a place writes the surface's MAPX/MONX (code 0x22FD); leaving a town on Earth writes PLAYER.
  Planet maps are MAPGpm (the program switches the file letter X -> G when landing on a planet, code 0x720B) and
  are only read. The MAPG10..MAPG45 copies of Earth names are planet maps 1-4, not working copies. Folder in
  the save ZIP: `ULTIA-II/`.
- **Disk check** (verified 2026-11-19, `tools/cachecheck.py`, 95 s): all 29 checkpoints rebuilt from an empty
  cache give the same frame and the same written files as a cache hit; Q saves after cache hits of `fight`,
  `ring` (after the planet X round trip) and `earth_2112` write the same files as the whole route from power-on.
- Real-time turns: the overworld never settles (the idle PASS scrolls the message area); `do` reports "still
  changing" there, which is normal. Shots: `do!` + `wN`.
- After a position poke the view redraws on the next turn (`POS` includes a pass).

## Checkpoints
`checkpoints.txt` (29): `title`, `menu`, `gen`, `start` (new ryz, 1423 B.C.); places with the start character:
`village`, `linda`, `castle`, `lordbritish`, `dungeon`, `tower` (torch lit); late character (`HERO`): `hero`,
`fight` (devil beside ryz), `door` (time door visible), `legends_arrive`, `nsa`, `enilno`, `earn_ring`, `rocket`,
`space`, `orbit_x`, `landed_x`, `ozys`, `blessing`, `earth_2112`, `ring`, `endgame` (save 02_endgame),
`shadowguard`, `field`, `minax`, `minax_dead`, `ending`. Added by the capture: `hero_dungeon` (late ryz in the
1423 B.C. dungeon, torch lit), `legends`, `pangea`, `y1990`, `y2112` (late ryz at (17,12) of each period),
`mx1`, `minax_honest`, `ending_honest` (the honest Minax fight and its ending).

## Tools
- `tools/try.py FILE [--frames K] [--peek ADDR:LEN] [--crop x0,y0,x1,y1] [--cols N]`: many routes in parallel, one
  sheet (`work/scout/ultima-2/try_NAME.png`) (from Ultima I).
- `tools/cachecheck.py`: every checkpoint from an empty cache vs a cache hit (frames and written files), plus Q
  saves after three cache hits vs the whole route.
- `tools/u2map.py --list | --png DIR | --ascii NAME`: places and door squares of every surface, map pictures.
- `tools/u2town.py MAP`: a town/castle map as characters with its people and their types.
- `tools/u2objs.py ROUTE [X,Y]`: live objects after a route (+ the map bytes around X,Y).
- `tools/u2merch.py ROUTE OBJ X,Y`: pokes that move a merchant or talker to a square (shops, talk).
- `tools/u2mon.py ROUTE slot:x:y:pic:hp[:type] ...`: pokes that place surface or town monsters.
- `tools/u2shops.py`: candidate counter squares for every shop (scan; verify in play).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| The game's own files (ROM text, code, maps, talk files) | `rom/ultima-2.zip` | commands, messages, quest rules, places, coordinates, RAM | 2026-11-19 |
| Wikipedia, Ultima II | https://en.wikipedia.org/wiki/Ultima_II:_The_Revenge_of_the_Enchantress | release history, DOS version (CGA, CPU timing), periods, Minax and Enilno outline | 2026-11-19 |
| Web search result snippets (Ultima Codex walkthrough, wiki) | https://ultimacodex.com/archive/ultima2/u2walk.html | Santre gives the quicksword for 500 gold; Minax switches places until dead (snippets only) | 2026-11-19 |
| Unavailable | ultimacodex.com, wiki.ultimacodex.com, nerdlypleasures.blogspot.com, web.archive.org (outside the network); GameFAQs, TCRF, StrategyWiki (403, known) | | 2026-11-19 |

## Open questions
Settled by the capture (2026-11-19), details in Capture notes and design/:
- ~~Monster creation~~: one try per turn on a random square of the whole map, nine kinds in a cycle (counter
  8EF0), terrain must match: rare near the player (code + RAM).
- ~~Frigates, horses, planes~~: all boarded, ridden, sailed, flown and landed; cannons fired.
- ~~Shops~~: all eight kinds used; merchants placed by poke; prices follow Charisma + Intelligence (code).
- ~~Oracle, food, spells, clerk, Flopy Fighter~~: all tried (poem verses, 52 per 100 food, ALAKAZAM is 6/256).
- ~~Dungeon contents~~: map format, chests, traps, creatures and level 16 decoded and shown.
- ~~Other planets~~: all eight landed, towns entered on Mars, Uranus, Neptune, Pluto, X.
- ~~Death~~: the program loops forever after "RYZ IS DEAD!" (findings).
Still open:
- Natural monster loot (thief items, fighter torches/helms, guard keys) not seen on a poked kill.
- Up ladder and Blink failed in their one try each; their conditions are not read.
- No use found for the three gems.
