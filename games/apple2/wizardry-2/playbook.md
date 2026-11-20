# Wizardry II: The Knight of Diamonds (Apple II) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"disk data" = decoded from the disk images with `tools/maps.py` / `tools/data.py`.
The same game is documented in depth for its DOS port (`games/dos/wizardry-2/`: playbook, design documents,
212 shot routes), and the engine is Apple II Wizardry I's (`games/apple2/wizardry/playbook.md`: read its
Controls table, it applies here). This file says what was checked here and what differs. For tools always write
`apple2/wizardry-2` (the slug exists on dos and nes), and give `play.py` a session name (`--name wiz2`).

> **Tools moved (2026-11-20).** Where this playbook says `try.py`, `cachecheck.py` or `screen.py` (copies that
> lived in this game's `tools/`), use the shared tools: `python3 tools/preview.py apple2/wizardry-2 FILE` (`--frames K` is now
> a `?` mark inside the route or `--timeline N:STEP`; sheets in `work/preview/apple2/wizardry-2/`), `python3
> tools/cachecheck.py apple2/wizardry-2` (`--after TOKENS` for a save in the game, `--peek ADDR:LEN` for party tables) and
> `python3 tools/play.py text` / `preview.py --text` for text screens. Pictures are native size
> (`play.py shot --scale N` on demand).

## Read first (capture 2026-11-20)
- Sets: `start` (35 shots, transfer to the party formed, `games/apple2/wizardry-2/shots/start/`) and `main`
  (229 shots: utilities, transfer, castle and every service, camp and sheets, all six floors, 18 message squares,
  14 random encounters, every guardian, chests, the quest, ending, cemetery). Lenses in `design/` clean.
- Always `apple2/wizardry-2` and `play.py --name wiz2`. Saves `00_transfer`, `01_start`, `02_ending` must be in
  `rom/saves/apple2/wizardry-2/` (rebuild: Saves below).
- Work in batches: `preview.py apple2/wizardry-2 FILE` (text screens: `--text`; maze/battle: `--crop 0,0,560,262`
  for the message area, `--timeline N:60` for battle and chest messages, which are timed and never wait).
- Checkpoints to start from: `s_util`, `s_imported`, `s_castle`, `s_training`, `s_wiped` (start set chain);
  `start`, `gcastle` (geared party in the Castle), `gcamp`, `gmaze` (floor 1 entrance); fights `battle`,
  `chest`, `b_mant` (floor 3 manticores), `b_demons`, `b_skulls` (floor 6); `guard1`-`guard5`, quest chain
  `sphinx` ... `final`.
- `WARP:FF:XX:YY` from `@gmaze`: the view is NOT redrawn on arrival: add `l,w200,r,w200` (or `poke:730E=0N00`
  first to choose the facing) before a shot. Message squares fire on arrival (sage, floor 6 (11,17)), others
  need a step in (`f,w600,w600`, `k` through doors). Warp arrival rolls fights only on floor 1; on floors 2-6 kick
  through a door into a room (`games/apple2/wizardry-2/tools/doors.py`: outside square, face the room, `k,w600,w900`;
  13 of 38 doors met a group). Floor 4 has no room doors.
- Battle messages: a round of six orders lasts ~1,800 frames; frame +K of `ROUTE,enter` is `ROUTE,enter,w60*N,!`.
  Victory E.P. at +300 after `WIN,enter`; the chest settles after `w600`.
- Temple: status poke (`7476=0500` CONDI dead), Tavern `r,2` (the patient must be outside the party), `c`,
  `type:CONDI\n`, payer digit: EBO (party place 2 after the removal) can pay 3,250, RYZ cannot ("CHEAP APOSTATES").
- Inn level-up: RYZ's E.P. at `73FA` (6 bytes, 3 words of 0-9999): `poke:73FA=B50445000000` = 691,205 -> level 14.
- Unknown and cursed items: item slot = 4 words (equipped, cursed, identified, number): RYZ slot 5 `73DA`,
  CONDI count `7488` slot 5 `74AA`, MNZ count `77C8` slot 5 `77EA`.
- Game over: `@guard4_costly,poke:73A6=0500,poke:7476=0500,c,w900,l,w900` -> the cemetery.
- Not shown: R)un (no message), Q)uick and S)tatus (no visible change), Dispell's effect, the staff in use,
  paying a fee, floor 4 random groups, floor 6 fixed fights.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wizardry II: The Knight of Diamonds (title picture "Wizardry / KNIGHT of DIAMONDS"; copyright screen "** THE KNIGHT OF DIAMONDS **"; scenario header "THE KNIGHT OF DIAMONDS") (verified) |
| Version | "VERSION PV3S2V1 OF 10-MAR-82  SER:??????" (verified); volumes `KODBV2` (disk 1, boot) and `KODBTTM` (disk 2, scenario) |
| Platform / model used | Apple II, `game.json` model `iiplus-wp1`: a II Plus with disk 1 write-protected (as Wizardry I: Pascal shows 80 columns on a //e; the boot program wants its disk protected) |
| Release (region, year) | North America, 1982 (copyright screen "COPYRIGHT (C)1982 ... ANDREW GREENBERG, INC & ROBERT WOODHEAD, INC.") |
| Developer / publisher | Andrew Greenberg, Robert Woodhead / Sir-Tech Software (copyright screen; publisher: source, DOS playbook) |
| Genre | First-person party RPG, the second Wizardry scenario: veterans moved over from Wizardry I enter six wireframe floors of 20 x 20 under the city of Llylgamyn (the screens write "LLYLGAMN") |
| Players / save system | 1 player; a roster of 20 characters on the scenario disk, written by the game as it goes; no other save |
| Runtime | Apple Pascal (p-code): disk 1 `SYSTEM.PASCAL`, `SYSTEM.STARTUP` (title, menu, utilities), `KODIMAGE` (title picture), `WIZARDRY.CODE`; disk 2 `WIZARDRY.CODE`, `SCENARIO.DATA` (from block 148), `SCENARIO.MESGS` (scrambled text) (disk data) |

## The dump: two disks
`rom/apple2/wizardry-2.zip` (never committed) = `1 Disk 1.dsk` + `2 Disk 2.dsk`, 140 KiB sector images in DOS 3.3
sector order (SHA-1s in `game.json` "header"). Owner's upload 2026-11-19.
- **verified** Both boot and play; the serial number reads `??????`.
- **verified** Disk 2 is **not a factory disk**: its roster holds four characters of an earlier player, THUG
  (L38 fighter), HALIG (L29 bishop), KELRACH (L28 lord), FURY (L28 samurai), no passwords, all with the chevron
  and marks `G` or `K`, carrying four of the five Knight of Diamonds pieces (THUG gauntlets 128, KELRACH armor
  129, FURY Hrathnir 125, helmet 126, shield 127). **While a piece is in the roster its guardian does not
  appear** (below, Game structure): the macro `WIPE` deletes the four, and it is part of `PARTY`.
- **verified** No duplicate scenario disk is needed: "SCENARIO MASTER IN DRV 1, PRESS [RET]" and
  "MASTER/DUPLICATE IN DRV 1, PRESS [RET]" both accept the registered disk 2.

## Boot sequence
Macros (all in `game.json`): `TITLE`, `MENU`, `XFER:letter`, `IMPORT`, `START`, `CASTLE`, `TRAINING`, `DEL:name`,
`WIPE`, `ADD:name`, `ADDPARTY`, `PARTY`, `RESUME`, `MAZE`, `REST`, `GEAR`, `EQUIP`, `WARP:floor:x:y`, `SOLO`,
`KOD`, `STAFF`, `HOME`, `KNIGHTS`, `REFORM`, `WIN`. `PARTY` was run as one route from power-on; all others inside
checkpoint routes replayed cold (Checkpoints).
- **verified** Power-on: black with a cursor (Pascal loading), then the title picture from about frame 900
  (the Wizardry logo, a knight and a dragon, "KNIGHT of DIAMONDS"). It is a still picture: no animation as in
  Wizardry I. `TITLE` = `w1200`.
- **verified** **Return** leaves the title (about 5 s, then the copyright screen with `S)TART GAME  U)TILITIES
  T)ITLE PAGE`). **Space does nothing here** (Wizardry I takes any key): `MENU` = `TITLE,enter,w900`. Other
  keys were not tried one by one (in one run `u` seemed to leave the title too).
- **verified** The transfer of the Wizardry I party (route prefix `sav:00_transfer`: the Wizardry I scenario
  disk becomes disk 3). On the menu `U` opens "WIZARDRY UTILITIES - R)ECOVER T)RANSFER B)ACKUP M)AKE SCENARIO
  DISK U)PDATE C)HANGE NAMES L)EAVE". `T`: "MOVE CHARS BETWEEN SCENARIOS - PRESS [RET] TO BEGIN OR [ESC] TO
  EXIT"; Return: "INSERT SCENARIO WITH CHAR(S) TO BE MOVED / PLACE SCENARIO IN DRIVE 1, PRESS RETURN" ->
  `disk:3,enter`; the source disk's name and its characters by slot letter ("PROVING GROUNDS OF THE MAD
  OVERLORD! A - RYZ  B - CONDI  C - EBO  D - CUBI  E - DEDDO  F - MNZ", "NOTE - CHARS MUST BE LIVE & IN CASTLE",
  "ENTER LETTER OF CHAR TO MOVE, OR PRESS [RETURN] TO EXIT"); a letter: "MOVING RYZ / PASSWORD >" -> `enter`
  (no password); "INSERT SCENARIO TO MOVE CHAR(S) TO / PLACE SCENARIO IN DRIVE 1, PRESS RETURN" ->
  `disk:2,enter`; "CHAR HAS BEEN MOVED - PRESS [RET]" -> `enter`, back on the Utilities menu. **One character
  per pass, two disk changes each**; the letters stay with the slots (after RYZ the list starts at B).
  `XFER:a` = `t,w400,enter,w300,disk:3,enter,w600,a,w300,enter,w400,disk:2,enter,w600,enter,w400`;
  `IMPORT` = `u,w600,XFER:a,...,XFER:f`.
- **verified** `L)EAVE` of the Utilities: "PLACE BOOT DISK IN DRIVE 1, PRESS RETURN" -> `disk:1,enter`, the
  copyright menu again.
- **verified** `S`: "SCENARIO MASTER IN DRV 1, PRESS [RET]" -> `disk:2,enter`; "MASTER/DUPLICATE IN DRV 1, PRESS
  [RET]" -> `enter`; the Castle ("LLYLGAMN ... MARKET") about 10 s later. `START` =
  `s,w400,disk:2,enter,w600,enter,w900`; `CASTLE` = `MENU,START`.
- **verified** `PARTY` = `MENU,IMPORT,l,w600,disk:1,enter,w900,START,TRAINING,WIPE,enter,w400,g,w300,ADDPARTY,
  enter,w300` (after `sav:00_transfer`): transfer, Castle, Training Grounds, delete the four stock characters,
  back to the Castle, Tavern, add the six by name. Checkpoint `start`.
- **verified** `RESUME` = `CASTLE,g,w300,ADDPARTY,enter,w300` after `sav:01_start` or `sav:02_ending`.
- **verified** `MAZE` (Castle) = `e,w300,m,w1500,l,w400,n,w300`: Edge of Town, Maze, the Camp, L)eave, "STAIRS
  GOING UP. TAKE THEM (Y/N) ?" N: floor 1 (0,0) facing north. The camp load takes 900 to 1500 frames depending
  on what the disk did before (a route with `m,w900` lost the `l`); `w1500` held on the first, second and third
  entry of a session.
- **verified** **Characters cannot be created**: the Training Grounds say "YOU CANNOT CREATE CHARACTERS IN
  LLYLGAMN BECAUSE THEY WOULD NOT SURVIVE. THEY SHOULD BE CREATED AND DEVELOPED IN THE "PROVING GROUNDS" AND
  THEN TRANSFERRED HERE WHEN 13TH LEVEL OR SO." A typed name opens inspect and delete; `*ROSTER` lists.
  **Going to the Training Grounds disbands the party** (the Castle list is empty afterwards: add them again).

## Controls
Apple II Wizardry I's table (`games/apple2/wizardry/playbook.md`, Controls) applies key for key; checked here:
| Context | Key | Action | Status |
|---|---|---|---|
| Title | `enter` | to the copyright menu (space: nothing) | verified |
| Menu | `s` / `u` / `t` | start game / utilities / title page | s, u verified; t seen by accident (reloads the picture) |
| Utilities | `t`, `l` | transfer (above), leave (asks for the boot disk) | verified; `r b m u c` not used |
| Disk prompts | `disk:N,enter` | "PLACE ... IN DRIVE 1, PRESS RETURN", "... IN DRV 1, PRESS [RET]" | verified |
| Castle | `a` `g` `b` `c` `e` | Inn, Tavern, Boltac's, Temple of Cant, Edge of Town | a, g, e verified; b, c not opened |
| Tavern | `a` + name + Return + Return (password); `r` + digit; digit; Return | add; remove ("WHO WILL LEAVE ([RETURN] EXITS) >"); see a member; leave | all verified |
| Inn | digit, `a`-`e`, Return, Return | "WHO WILL STAY", room (A stables free ... E royal suites 500), "YOU NEED n MORE EXPERIENCE POINTS TO MAKE LEVEL / PRESS [RETURN] TO LEAVE", then Return leaves the room list | a (stables) verified: spell points restored |
| Edge of Town | `m` `t` `c` `l` | Maze, Training Grounds, Castle, Leave game ("PRESS [RETURN] FOR MORE WIZARDRY", then the scenario master prompt) | m, t, l verified |
| Training Grounds | name + Return, then Return (password), `d`, `y`; `*ROSTER`, `l`; Return | delete a character; roster; back to the Castle | verified (`WIPE`) |
| Camp | digit; `e`; `l` | inspect; equip everyone ("SELECT WEAPON FOR RYZ ... WHICH ONE ([RET] FOR NONE) ? >": one prompt per slot kind that has a usable item); leave | verified; `r` `d` not used |
| Maze | `f` `l` `r` `k`; `c` | forward, turn left, turn right, kick through a door; camp | verified (`w a d` are printed as the cluster; not tried) |
| Stairs, messages | `y` / `n`; Return | "STAIRS GOING UP/DOWN. TAKE THEM (Y/N) ?"; "[RET] FOR MORE", "PRESS [RET]" | verified |
| Riddles | text + Return | "ANSWER ?" | verified (Gnilda's temple) |
| Battle | `f` (then group digit when there are several groups), `s` + spell name + Return, `p`, `r`, `u`; Return or `b` | fight, spell, parry, run, use; "PRESS [RET] TO FIGHT, OR GO B)ACK AND RE-ENTER." | f, s, p, r, Return verified |
| Chest | `o` `c` `l` `i` `d` | open, Calfo, leave, inspect, disarm | menu and `l` verified |
| Awards (ending) | Return, then `y`/`n` | "PRESS [RET] TO ASSIGN AWARDS", "KNIGHTHOODS LEFT : 5 / AWARD ONE TO CONDI (Y/N) ? >" | verified |

Input timing: default press (hold 8, wait 40); one key at a time, and keys during a disk load are lost without
a trace. Waits that worked: menus `w300`, a typed name `type:NAME\n,w300`, password Return `w400`, the camp
after `m` `w1500`, equip prompts `w400` each (`e,w900` first), a step or turn `w200`, a kick into a fight
`w600,w900`, a warp `w600`, battle orders `w150`, a round `w1500`-`w3000`, message pages `enter,w600`.

## Game structure
- **Castle** (verified menus): Adventurer's Inn, Gilgamesh' Tavern, Boltac's Trading Post, Temple of Cant, Edge
  of Town (Maze, Training Grounds, Castle, Leave the game). Utilities are on the boot menu.
- **What the transfer keeps** (verified, sheets and roster): everything of the Wizardry I `02_ending` record:
  level 13, hit points, E.P., gold, age, scores, spells, the chevron; the packs were empty already. Spell
  points come over as they were (DEDDO had 0 of level 7: he cast Tiltowait at Werdna); one free night in the
  stables restores them (`REST`: DEDDO 9/9/9/7/5/4/3) and nobody gains a level (DEDDO needs 64,112 more).
  On the Wizardry I disk the moved characters are gone. They land in the free roster slots 0, 4, 6, 7, 8, 9.
- **Maze** (disk data, `design/maps/floors.txt`, rebuilt with `python3 games/apple2/wizardry-2/tools/maps.py
  --out ...`): six floors of 20 x 20, x east, y north. **The floors are the DOS port's** (the two map files
  differ in one number: floor 3's message square (8,10) has 10 where DOS has 11), so the DOS playbook's
  coordinates apply:
  | Floor | Arrive | Guardian square: group | Stairs down -> | Piece (item) |
  |---|---|---|---|---|
  | 1 | (0,0) from the castle | (15,2): 1 MAGIC ARMOR (monster 77, 305 hit points, AC -10) | (16,2) -> floor 2 (11,10) | KOD'S ARMOR (129) (verified: `guard1_won`) |
  | 2 | (11,10) | (2,6): 1 MAGIC SHIELD (75; first shown as "ANIMATED OBJECT") | (1,6) -> floor 3 (0,0) | KOD'S SHIELD (127) (verified: `guard2_won`) |
  | 3 | (0,0) | (14,13): 1 MAGIC SWORD (73) | (13,14) -> floor 4 (7,12) | HRATHNIR (125) (verified: `guard3_won`) |
  | 4 | (7,12) | (10,4): 1 MAGIC HELMET (74) | (9,4) -> floor 5 (1,18) | KOD'S HELMET (126) (verified) |
  | 5 | (1,18) | (10,9): 2 MAGIC GAUNTLETS (76) | (10,10) -> floor 6 (0,0) | KOD'S GAUNTLETS (128) (verified) |
  | 6 | (0,0) | fixed-fight squares (5,15), (5,16), (18,18), (18,19), (19,19): monster 47 HIGH PRIEST (not visited) | none | - |
  Floor 6 (1,2), kicked into from (1,1): the sphinx (verified, `sphinx` ... `temple_door`): "LYING IN FRONT OF
  THE DOOR IS A BEAST WITH THE HEAD OF A MAN AND THE BODY OF A LION. IN AN HYPNOTIC VOICE IT INTONES:" /
  ""ENTER HERE, THE VERY FEW WHO CAN GIVE THE ANSWER TRUE OF THIS RIDDLE ASKED OF YOU." / "SEARCH THIS LEVEL, IF
  YOU DARE SEARCH EACH DEN AND MONSTER LAIR THREE CLUES HAVE I HIDDEN THERE." / "SEARCH EACH PASSAGE AND EACH ROOM
  FOR A KING WITHIN HIS TOMB FOR THE ANSWER WAS HIS DOOM." / "IF YOU LIVE, YOU SHOULD NOT LOSE FOR THE ANSWER TO
  THIS RUSE LIES CONFUSED AMONG THE CLUES." (five Returns), "ANSWER ?": `THE KNIGHT OF DIAMONDS` -> "RIGHT!" (the
  party stays; anything else: "WRONG!" and back on (1,1)). Kick north: (1,3) "THE APPARITION REAPPEARS AND
  INTONES: "ONE ALONE.""; kick north again: (1,4) teleports to floor 1 (9,9), facing north at the door of
  Gnilda's temple (9,10). The doors here need K)ick (F)orward says "OUCH!").
- **A guardian appears only while its piece is not in the roster** (verified, and the main trap of this dump):
  with the four stock characters on the disk every guardian square gave "AN ENCOUNTER" with an ordinary random
  group, on entering, re-entering, after winning and after running (about fifteen tries on floors 1-5); after `WIPE` the
  same routes meet MAGIC ARMOR, SHIELD, SWORD, HELMET and GAUNTLETS. Piece by piece: with only THUG (the
  gauntlets' holder) deleted, floor 5's square met "2 OBJECTS" with the gauntlet picture and floor 2's square
  (shield, held by FURY) still a random group (verified, two routes). So a party that already carries a piece
  should not meet its guardian again (inferred; not tried with our own party).
- **Random fights are harsher and more frequent than on DOS**: arriving on a fight-zone square by stairs or
  warp, and kicking a door into a room, met a group almost every time (seen on floors 1-5: 5 MEN IN ARMOR + 5
  PRIESTS, 6 WERETIGERS, 5 TROLLS + 3 OGRES, 5 DEMONIC FIGURES + 1 LVL 8 NINJA; unidentified names until the
  group is known). The monster table
  (78 entries, `tools/data.py monsters`) is not the DOS one row for row (no kobold kings on floor 1).
- **The quest** (verified): Gnilda's temple, floor 1 (9,10), entered by kicking the door north from (9,9).
  A party of six, or RYZ alone only carrying the five: "AS YOU ENTER, AN EERIE GLOW FILLS THE ROOM. WITH A
  BRILLIANT FLASH, A TOWERING APPARITION APPEARS BEFORE YOU. SHE SPEAKS:" (the speech; later pages not paged).
  **One character alone, wearing the five**: "A FIERY FACE APPEARS BEFORE YOU AND DEMANDS, "WHAT IS THE ANSWER
  TO THE RIDDLE OF THE SPHINX ?" THE IMAGE DISAPPEARS. PRESS [RET]", "ANSWER ?" -> `THE KNIGHT OF DIAMONDS`
  (capitals) -> "A NOW FAMILIAR APPARITION APPEARS AND SAYS: "THROUGH YOUR VALOR, WIT, AND PRESENCE OF MIND, YOU
  HAVE PROVED YOURSELF THIS DAY. BY OBTAINING THE FULL REGALIA OF THE LEGENDARY KNIGHT AND PRESENTING IT HERE
  BEFORE ME, YOU HAVE DEMONSTRATED THE WORTH OF YOUR ILK. I SHALL RECLAIM THOSE ARTIFACTS, ... BUT ALSO WILL I
  PRESENT YOU WITH A GIFT. RECEIVE THE STAFF OF GNILDA!" (three Returns), "RYZ GOT ITEM": his whole pack is
  replaced by the staff (item 124).
- **Ending** (verified, `ending`): RYZ alone up the floor 1 stairs with the staff: a text screen "*** GAUDEAMOUS
  *** HAIL VALOROUS HERO! HAIL SAGE WARRIOR! THE STAFF OF GNILDA ONCE AGAIN PROTECTS OUR FAIR CITY! I, QUEEN
  MARGDA, BESTOW UPON YOU THE RANK AND TITLE OF KEEPER OF THE HOLY STAFF OF GNILDA. I ALSO RECOGNIZE THAT WITHOUT
  THE AID OF YOUR FELLOWS YOU WOULD NEVER HAVE BEEN ABLE TO COMPLETE YOUR QUEST. AND SO TO REWARD THEM, I GRANT TO
  YOU THE RIGHT TO CREATE 5 KNIGHTS OF THE CITY OF LLYLGAMN  PRESS [RET] TO ASSIGN AWARDS". Then "KNIGHTHOODS
  LEFT : 5 / AWARD ONE TO CONDI (Y/N) ? >" for the other roster characters in roster order; the counter starts at five (only five
  others were in the roster, so what happens to a sixth was not seen; DOS asks for every character). The staff is taken; RYZ gets `">G"` and 300,000 E.P.
  (686,327 -> 986,327), the knights `">K"`.
- **A party of six with the staff gets the ending too, and it damages the roster** (verified with the poked
  staff, `@start,STAFF,MAZE,HOME` + five Y: DOS gives six no ending). The award step uses the second party
  place for each candidate: afterwards the Castle lists RYZ, MNZ, EBO, CUBI, DEDDO, MNZ, and after L)eave game
  the roster has MNZ's record in CONDI's slot (CONDI is gone, MNZ exists twice). Through the event the bearer
  is alone anyway (Gnilda's test wants one alone and there is no way to add members below). **Always go up
  alone (`SOLO`) when `STAFF` is used.**
- **Game over**: as Wizardry I (not seen here). The helmet and the gauntlets killed four of six in one round.

## Differences a capture agent trips over
From the DOS version:
- the transfer is on the boot menu's Utilities, one character per pass with disk changes (DOS: Edge of Town,
  Utilities, M)ove, no prompts); there are no stock veterans to fall back on, only the four leftovers;
- guardians need `WIPE` (above); DOS routes that kick straight into a guardian work only after it;
- no Utilities and no Training menu in the Edge of Town; Training is a name prompt and disbands the party;
- Tavern add is by typed name + password Return, remove by number; leave screens with `l` or Return as printed;
- battle: S)PELL is on RYZ's first-round menu in most fights, in some surprise rounds too and in others not
  (rule, capture 2026-11-20: no S)PELL in the round after "YOU SURPRISED THE MONSTERS!"; DOS: no spells in round 1);
  spell names in capitals; a fight against several groups asks "FIGHT AGAINST GROUP# ?" after `f`;
- a party of six with the staff gets the ending (DOS: no) and loses a character to it (Game structure);
- the ending is a text screen with other words, Queen Margda, five knighthoods at most;
- the riddle answer is typed in capitals; "LLYLGAMN" is the screens' spelling;
- memory: position at `730E`-`7314`, party at `737E`, battle group at `6DCA` (RAM map); 16-byte monster records
  as on DOS (Wizardry I on the Apple II has 14).
From Apple II Wizardry I:
- Return, not any key, on the title; the title is a still; `TITLE` is `w1200`, not `w2100`;
- addresses moved by different amounts (position -0x1C, party -0x12, floor buffer -0xF8, battle group other
  layout): none of the Wizardry I pokes may be reused unchanged;
- `WARP` rewrites special 5 (the stairs to the castle at (0,0)), not special 2;
- no character creation, so no `MAKE`/`PARTYMAKE`; `DEL` and `ADD` are the same;
- the maze load needs `w1500`.

## Shot plan
Done 2026-11-20 (sets `start` and `main`, see Capture results); what is not shown is listed in Read first.
Target: the DOS set's coverage (213 shots, `games/dos/wizardry-2/shots/main/shots.txt`) replayed here, plus
what only this version has. Ids keep the DOS ids where the content is the same. By category:
- boot/title/menu (6): `title_logo` (`@title`), `menu_copyright` (`@menu`), `menu_utilities` (`@menu,u,w600`),
  the loading cursor is not a shot.
- the transfer, step by step (10): `sav:00_transfer,MENU,u,w600,t,w400` (begin prompt), `enter,w300` (source
  prompt), `disk:3,enter,w600` (the Wizardry I list), `a,w300` (password), `enter,w400` (target prompt),
  `disk:2,enter,w600` (moved), the list on the second pass (A gone), the boot disk prompt on L)eave, both
  scenario prompts of S)tart.
- Castle and services (about 35): castle empty (`sav:00_transfer,MENU,IMPORT,l,w600,disk:1,enter,w900,START`),
  Training Grounds text (no creation), `*ROSTER` with the four stock characters and ours, a stock character's
  sheet (THUG: level 38, the gauntlets, marks), delete confirm, Tavern add / password / full / remove, Inn list
  and result, Temple, Boltac's pages, buy, sell, identify (the pieces drop unidentified: `guardN_won`),
  uncurse, Edge of Town, leave game.
- inventory (about 12): six sheets with gear (`@gcastle`), spell books, equip prompts (`@rested,GEAR,e,w300,
  m,w1500,e,w900`), the five pieces worn (AC "LO", hits "112+"), the staff in the pack (`@staff,c,w400,1,w400`),
  sheets with `">G"` and `">K"` (`@final`).
- gameplay (about 30): a view per floor (`@gmaze,WARP`), doors, darkness (floors 1, 2, 5, 6), stairs prompts,
  pits, chutes (floor 5), teleports, rock (floors 3, 4), spinners (floor 6), every message square of the DOS
  survey (same coordinates), camp, the maze command list.
- battle (about 45): encounter starts per monster picture (pictures numbered 0-29 in the table; warp to fight-zone squares of every
  floor and vary `wK` before `WARP`), surprise both ways, friendly groups ("A FRIENDLY GROUP OF LVL 7 PRIESTS.
  THEY HAIL YOU IN WELCOME! YOU MAY F)IGHT OR L)EAVE IN PEACE." seen), orders, group prompt, spells, round
  messages, victory and E.P., chest menu and commands (`@chest`).
- boss (about 15): the five guardians' first screens (`guard1`-`guard5`), a round each, the drops
  (`guardN_won` + sheet), the lost round against the helmet (`@guard4` + the `guard3_won` orders: four dead).
- quest end and ending (12): sphinx pages (`@sphinx`, Return), "ONE, ALONE." (floor 6 (1,3)), Gnilda with six
  (`@gcastle,KOD,MAZE,WARP:01:09:09,poke:730E=0000,k,w900` met the speech once; a random group can come
  first), `gnilda_test`, `gnilda_answer`, `staff_gift` and its pages, `staff`, `ending`, each award prompt,
  `knights`, `final`.
- gameover (2): cemetery (status pokes + camp, or the helmet's round continued).
- save/extra (3): Utilities entries (change names, backup prompt), "PRESS [RETURN] FOR MORE WIZARDRY".
How to reach: everything from `@start`, `@gcastle`, `@gmaze` + `WARP`, the guardian and quest checkpoints.

## Capture results (2026-11-20)
- **Method:** no interactive session; plan files previewed (`--text` for town screens, cropped sheets and
  `--timeline` for maze and battle messages), then appended to the work `shots.txt` and shot with `--only`.
  About 110 tool calls for both sets.
- **Verified here** (new): utilities' first screens; Training Grounds options (inspect, delete, change class,
  set password); Boltac's six stock pages, purchase, unusable confirm, sell, identify, uncurse; Inn rooms,
  stables, cot healing (1 hit point per 10 gold), level-up; Temple flow and "CHEAP APOSTATES! OUT!"; camp
  reorder, disband, equip prompts, sheets, spell books (21 mage, 29 priest), cast, DUMAPIC, MALOR, use, trade
  (gold first), drop, bishop identify; maze T)ime ("NEW DELAY (1-9999)"), I)nspect ("LOOKING......."); the
  message squares of every floor (pages in `main`); battle rules: back rank has no F)ight, no S)PELL in the
  round after "YOU SURPRISED THE MONSTERS!", spells are not named in round messages; chest inspect, Calfo,
  disarm by typed trap name, the teleporter trap; guardians' round messages and drops ("DEDDO FOUND - PLATE
  ARMOR" ...); the cemetery.
- **Encounter recipes** (shots `battle_*`): floor 1 `@gmaze,wK,WARP:01:08:0E,w900` (K 1: men in armor + mages,
  K 9: swarms); floors 2-6 door kicks, routes in `shots.txt`.
- **Floor 3 (8,10)**: after "MAPIRO MAHAMA DIROMAT" the party is in the Castle; the well's Y did the same.
- **Riddle of floor 2**: seven pages, then "ANSWER ?"; SHIELD -> "RIGHT!".

## Strategy and walkthrough notes
- Cataloguing: never grind. `REST` + `GEAR` + `EQUIP` give a rested party with Boltac-priced gear (AC 0 -1 3 5
  9 5); `WARP` from floor 1 reaches any square; `KOD` + `SOLO` pass Gnilda's test; `HOME` ends the quest.
- Guardians against that party (all from `guardN`, orders two blows, MALIKTO, parry, TILTOWAIT, LAHALITO):
  the Magic Sword dies in round 1, nobody hurt (`guard3_won`, a real win); the Magic Armor (305 hit points)
  and the Magic Shield (76 hit points left after the round) were still standing after the three spells; the Magic Helmet and the Magic Gauntlets
  answer with spells and blows that leave four dead. For those: poke the hit points to 1 during the orders
  (`poke:6DD6=0100`, second monster `6DE6`) and let a fighter's blow land (`guard2_won`, `guard4_won`,
  `guard5_won`), or `WIN` (the armor: its AC -10 was not hit in three tries; the helmet: it acts before the
  fighters and killed three or four members in all thirteen waits tried, `guard4_costly` keeps one such round,
  `guard4_won` uses `WIN` and nobody is hurt).
- The finder of a piece varies with timing (armor: DEDDO; shield: RYZ or DEDDO; helmet: RYZ or DEDDO; sword: MNZ; gauntlets: CONDI or EBO).
  Pieces arrive unidentified ("ARMOR", "SHIELD" ...): MNZ's I)dentify or Boltac's.
- Critical path: five guardians -> one bearer wears all five -> floor 6 sphinx -> "ONE, ALONE." -> teleport to
  floor 1 (9,9) -> the others out in the Tavern (`SOLO`) -> (9,10) answer -> staff -> floor 1 (0,0) stairs ->
  ending -> awards. The checkpoint chain uses `KOD` for the five (the fights are separate checkpoints): a
  chain that carries the real drops to one bearer was not built.
- Gnilda takes the bearer's whole pack: RYZ ends with nothing (`final`: AC 10 after a camp trip).
- **Timing**: every fight depends on all frames before it. Timing-bound checkpoints: `battle`, `chest`,
  `guard1`-`guard5` (which group, surprise), `guard2_won`, `guard3_won`, `guard4_costly`, `guard5_won` (the
  round), `gnilda_test` (no random group came when the door was kicked; the same route from `@start` without
  gear met one every time, over twenty variants tried: which rooms hold a group is rolled when the floor is
  first loaded in a session), `temple_door` (the two kicks met nothing). Do not edit a macro or wait earlier in the chain: add checkpoints.

## Naming
No naming: the six come from Wizardry I (RYZ CONDI EBO CUBI DEDDO MNZ). Utilities C)HANGE NAMES exists ("ENTER
THE CURRENT NAME OF THE CHAR & THEN THE NEW NAME", program text; not used).
| Name | Race | Align | Class | Level | HP | Gold (after `GEAR`) | Roster slot |
|---|---|---|---|---|---|---|---|
| RYZ | Human | Good | Fighter | 13 | 112 | 4817 (2442) | 0 |
| CONDI | Dwarf | Good | Fighter | 13 | 124 | 9342 (6217) | 4 |
| EBO | Gnome | Good | Priest | 13 | 71 | 7165 (5095) | 6 |
| CUBI | Hobbit | Neutral | Thief | 13 | 66 | 6284 (4249) | 7 |
| DEDDO | Elf | Good | Mage | 13 | 49 | 5077 (2062) | 8 |
| MNZ | Elf | Good | Bishop | 13 | 58 | 8930 (7100) | 9 |

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| The Wizardry I party | `sav:00_transfer,PARTY` (checkpoint `start`) | game's own T)RANSFER | verified |
| Guardians appear | `WIPE` (Training Grounds: delete THUG, HALIG, KELRACH, FURY), inside `PARTY` | scout | verified |
| Spell points | `REST` (Castle: stables for members 5, 3, 6) | game | verified |
| Gear | `GEAR` (Castle or camp, party in slots 1-6): packs poked, gold reduced by the prices: RYZ long sword, plate mail, shield + 1, helm; CONDI long sword, plate mail + 1, shield + 1, helm; EBO anointed mace, chain mail + 1, large shield, Dios potion; CUBI short sword, leather + 1, small shield, scroll/Katino; DEDDO staff + 2, robes, scroll/Halito; MNZ staff, leather + 1, small shield, Latumofis potion. `EQUIP` in the camp: `e,w900` + 19 x `1,w400` (19 prompts for exactly this gear) | DOS macro, new addresses and cheaper items (the Wizardry I ending left 4,817-9,342 gold) | verified (`gcamp`) |
| Warp anywhere (from floor 1) | `WARP:FF:XX:YY` (hex): puts the party on (0,1) facing south, turns, steps onto the stairs to the castle, rewrites that staircase (special 5 of the floor in play: AUX0 floor `5E2C`, AUX2 x `5E6C`, AUX1 y `5E4C`) and answers Y. Works only while floor 1 is loaded. Arriving on stairs shows their prompt; arriving on a fight-zone square usually starts a fight; ~~a message square does not fire on arrival~~ some do (the sage, floor 6 (11,17)), others need a step in; the view is not redrawn until a turn (capture 2026-11-20) | DOS recipe | verified (floors 1-6) |
| Facing | `poke:730E=0N00` before `k` or `f` (0 N, 1 E, 2 S, 3 W); the view redraws on the next move | scout | verified |
| Win a fight | `WIN` = `poke:6DCA=0000` (group 1 alive count) during the orders, then Return; second group `poke:6F00=0000`: counts as killed, E.P., chest or drop | DOS recipe | verified (`guard1_won`, `chest`) |
| Monster hit points | `poke:6DD6=0100` (group 1, monster 1; next monsters +0x10) during the orders | scout | verified (shield 76, armor 305, ninja read; kills in `guardN_won`) |
| Lone bearer | `SOLO` (Castle): Tavern, remove 6, 5, 4, 3, 2 | DOS macro | verified |
| The five pieces | `KOD`: RYZ's pack = armor, Hrathnir, helmet, shield, gauntlets, all equipped and identified (replaces his pack) | DOS macro | verified (Gnilda's test) |
| The staff | `STAFF`: RYZ's pack = staff of Gnilda (item 124); with `SOLO`, `MAZE`, `HOME` the ending (`ending_poke`). Never with six (Game structure) | DOS macro | verified |
| Home | `HOME` (any floor-1 square): poke (0,1) facing south, step onto the stairs, Y | DOS macro | verified (`ending`) |
| Awards | `KNIGHTS`: Return, then Y five times (CONDI EBO CUBI DEDDO MNZ: the only other roster characters after `WIPE`) | scout | verified |
| Re-form | `REFORM`: Tavern, add the five by name | scout | verified |
| Tables | `python3 games/apple2/wizardry-2/tools/data.py items|monsters|roster|toc [FILE]` (130 items, 78 monsters, 20 roster slots; FILE = a `.dsk`, a `.sav` or the game ZIP; also reads a Wizardry I disk) | disk data | roster and item numbers verified in play; monster dice fields are a reading of the record |
No codes, downloadable saves or debug features were looked for on the web (no web source was fetched in this
run: the disks and the DOS documents answered what was needed).

### Saves (`rom/saves/apple2/wizardry-2/`, never committed: whole disk images)
`play.py export` writes a ZIP of the written images (`2 Disk 2.dsk` and `T Wizardry I.dsk`); only the table in
`saves/README.md` is committed. Rebuild: `play.py start apple2/wizardry-2 --route ROUTE`, `play.py export NAME`.
| Name | Contents | Route | SHA-1 (.sav, this build) | Status |
|---|---|---|---|---|
| 00_transfer | input, made by the Wizardry I scout: `T Wizardry I.dsk` with the six after Werdna | `games/apple2/wizardry/tools/transfer.py` | `646deb548d50937b94eb3e26bcffc69cc981fca2` | verified (`start`) |
| 01_start | roster after the transfer and `WIPE`: the six, level 13, chevron, no items | `@start,e,w300,l,w900` + export | `83686fb50ef7f027b35c4f6d3fd1bac84bca4004` | verified (`resume`) |
| 02_ending | after the ending: RYZ `>G` 986,327 E.P. without items, the five `>K` with their gear | `@final,e,w300,l,w900` + export | `9e3cd5b3f5897824db0f8f34ad5eeb4be036019e` | verified (`resume_end`, `data.py roster`) |
| 03_ending_noitems | after the shortcut ending without gear (`ending_poke`): RYZ `>G`, the five `>K`, original gold, no items at all | `@plain_final,e,w300,l,w900` + export | `31cff46670841c8a7269928ff75245e23d10faba` | verified (`data.py roster`) |

### The transfer disk for Wizardry III (`rom/saves/apple2/wizardry-3/00_transfer.sav`, never committed)
`python3 games/apple2/wizardry-2/tools/transfer.py` stores the `2 Disk 2.dsk` image of `02_ending.sav`,
unchanged, as `T Wizardry II.dsk` in a new ZIP (fixed date: the same image gives the same ZIP).
- ZIP SHA-1 `6a1f0c9daa6157f442ffa9982073b1704359cce3`; image SHA-1 `57d5359a9a92c1ecfc37eb75effac909c6b71fcd`
  (143,360 bytes, DOS 3.3 sector order, volume `KODBTTM`).
- On it: RYZ (slot 0, `>G`, no items), CONDI, EBO, CUBI, DEDDO, MNZ (slots 4, 6-9, `>K`, items 1 24 25 14 /
  3 23 8 15 / 2 22 7 21 / 32 9 28 / 5 22 7 16), all OK, in the Castle, no passwords; 14 free slots; the
  unchanged Wizardry II scenario.
- Not tried in Wizardry III. Risk: this game's own transfer refuses "** CHAR HAS NON-XFERRABLE ITEMS **"
  (program text; which items is not known). For that case a second disk exists:
  `rom/saves/apple2/wizardry-3/00_transfer_noitems.sav` (`transfer.py rom/saves/apple2/wizardry-2/03_ending_noitems.sav
  rom/saves/apple2/wizardry-3/00_transfer_noitems.sav`), ZIP SHA-1 `ae1ec27e0f57bdd2fb2c92314075fe9adec828f8`,
  image SHA-1 `dabe4ea8700db6fc78e3a241a13781c5760bf993`: the same six with the same marks, original gold,
  empty packs. Its ending came from the `STAFF` poke, not from Gnilda (an item-free run through the temple
  always met a random group at the door).

## RAM map (for `game.json` "ram" watches and pokes)
Addresses in the 64K the program sees (main memory below `C000`); the same on every run of these routes.
Words are little-endian. "stack" = a local variable, valid on the screen named.
| Address | Size | Meaning | How found |
|---|---|---|---|
| `730E` | 2 | facing: 0 N, 1 E, 2 S, 3 W | peek over a turn; poke + kick (verified) |
| `7310` | 2 | floor: 0 castle, 1-6 (65535 in the Castle after the ending) | warp (verified) |
| `7312` | 2 | y, 0-19 north | peek over a step; warp (verified) |
| `7314` | 2 | x, 0-19 east | warp (verified) |
| `737E + n*0xD0` | 208 | party member n (0-5, party order): the character record (layout: Wizardry I playbook, re-checked here through `GEAR`, `KOD`, the sheets and `data.py roster`); RYZ: status `73A6`, gold `73B2`, item count `73B8`, items `73BA` (8 x 4 words: equipped, cursed, identified, item number), hit points `7404`, marks `744C` | name search (verified; spacing checked on all six by `GEAR` and the cold check's party line) |
| `5B22` | 894 | stack: the floor in play (TMAZE layout, `tools/maps.py`); other copies at `7A56` and (partly) `50C6` | match with the disk + warp (verified) |
| `5E2C`, `5E4C`, `5E6C` | 2 each | stack: special 5 of floor 1 (stairs to the castle): AUX0 floor, AUX1 y, AUX2 x (`WARP`) | computed from `5B22`, verified by warps |
| `6DCA` | 6 + 16k | battle group 1: alive count, count, monster number; then 16-byte monster records from `6DD0` (hit points at +6: `6DD6`, `6DE6` ...) | dump in three fights; pokes (verified) |
| `6F00` | 6 | battle group 2: alive count, count, monster number (its records do not line up with group 1's at the same spacing: not decoded) | dump of one fight; poke alive 0 (verified in `chest`) |
| `6E60` | 64 | group 1's names (unknown singular and plural, real singular and plural, 16 bytes each) | dump (read) |
Marks word (`+CE`): bit 0 `>` chevron, bit 11 `K` Knight of the City, bit 14 `G` Keeper of the Staff (verified:
`744C` = `4001` for RYZ, `751C` = `0801` for CONDI after the awards; the stock characters carry the same bits).
Disk (block order, `maps.blocks()`): SCENARIO.DATA from block 148 (`maps.file_block` reads the directory); its
table of contents: MAZE +6 (6 floors, floor N at byte `13400 + (N-1)*400`), ENEMY +18 (78), REWARD +44 (24),
OBJECT +52 (130), CHAR +72 (20; slot n at `(148+72)*512 + (n div 4)*400 + (n mod 4)*D0`), SPCCHRS +82, EXP +112.

## Emulation notes
- **Model `iiplus-wp1`**, for Wizardry I's reasons. `iie` and an unprotected disk 1 were **not tried here**
  (taken from Wizardry I; the dispatch said so).
- Text screens (Castle, Tavern, Inn, Training, camp, sheets, the ending, Utilities) are text page 1:
  `python3 tools/play.py --name SESSION text` prints them; `tools/try.py FILE
  --text` prints the end screen of many routes run in parallel. The maze, fights, chests and maze messages are
  hi-res: look at frames (`try.py` sheets are 1x and cheap to read). After a hi-res screen the text page still
  holds the last text screen (the camp): `--text` shows stale text there.
- Text prompts never settle (blinking cursor): `settle` runs its 300 frames; the checkpoint routes contain those.
- A key during a disk load is lost; the camp load varies (Boot sequence, `MAZE`).
- Pokes to the party show at once on a sheet; the Castle list and AC update on a menu change or a camp visit
  (AC "LO" stays on RYZ after Gnilda takes the pieces until the next camp).
- RNG follows frame timing; which random group waits in a room is fixed when the floor is loaded (a wait
  before the kick changed nothing, a wait before `WARP` changed the group).
- `play.py checkpoint` writes the session's route with its settles; the hand-written routes in
  `checkpoints.txt` are the same tokens without them where a macro was used.

## Checkpoints
| Name | What |
|---|---|
| `title`, `menu` | title picture; copyright menu |
| `start` | Castle, the six moved from Wizardry I, stock characters deleted, party formed |
| `edge`, `camp`, `maze1` | Edge of Town; first camp; floor 1 (0,0) facing north (no gear) |
| `rested` | Castle after the stables for DEDDO, EBO, MNZ |
| `gcamp`, `gcastle`, `gmaze` | the party with gear: camp, Castle, floor 1 (0,0) |
| `battle`, `chest` | floor 1 (14,2): 5 DEMONIC FIGURES + 1 LVL 8 NINJA, the party surprised them; the chest after `WIN` |
| `guard1` ... `guard5` | the five guardians at RYZ's options |
| `guard1_won` ... `guard5_won` | after each guardian (1, 4: `WIN`; 2, 5: hit points poked to 1 + a real blow; 3: a real win), nobody dead, piece in a pack (DEDDO 129, DEDDO 127, MNZ 125, DEDDO 126, CONDI 128) |
| `guard4_costly` | the helmet beaten by a real blow after its spell: four dead |
| `sphinx`, `sphinx_answer`, `sphinx_right`, `one_alone`, `temple_door` | floor 6 (1,2): the riddle's first page, "ANSWER ?", "RIGHT!"; (1,3) "ONE ALONE."; floor 1 (9,9) after the teleport |
| `ending_poke`, `plain_final` | the ending by `SOLO` + `STAFF` without gear; the Castle after its awards and `REFORM` (nobody carries an item) |
| `gnilda_test`, `gnilda_answer`, `staff_gift`, `staff` | RYZ alone with the five at the temple: the fiery face, "ANSWER ?", the gift's first page, "RYZ GOT ITEM" |
| `ending`, `knights`, `final` | GAUDEAMOUS; Castle after the five awards; Castle with the party re-formed |
| `s_util`, `s_imported`, `s_castle`, `s_training`, `s_wiped` | start set: Utilities with the Wizardry I disk; after the six transfers; Castle before a party; Training Grounds; after `WIPE` |
| `b_mant`, `b_demons`, `b_skulls` | fights met by door kicks: floor 3 4 manticores; floor 6 greater demons + ninjas + demonic figures; floor 6 evil eyes + skulls (surprised) |
| `resume`, `resume_end` | Castle from `sav:01_start` / `sav:02_ending` (need the files in `rom/saves/apple2/wizardry-2/`) |
Cold check: `python3 tools/cachecheck.py apple2/wizardry-2` builds every checkpoint from an empty cache
and compares it with a cache hit in a fresh process (frame, memory 0000-BFFF, written disks), prints each
checkpoint's floor, square, packs and marks, and writes each frame to `work/scout/apple2/wizardry-2/cc_NAME.png`.
Last run 2026-11-19 on model `iiplus-wp1`: all 39 checkpoints identical cold, from the cache and against the
cache that existed before (frame, memory and written disks). The frames of the fight, quest and ending
checkpoints were looked at on one sheet afterwards: that look is what showed four dead in the first helmet
win (now `guard4_costly`), which the hashes could not. A run takes about 12 minutes; with names as arguments
it still empties the whole cache first.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| the disks | `rom/apple2/wizardry-2.zip` | program text of the boot program (prompts of the utilities), version, roster, maps, items, monsters | 2026-11-19 |
| DOS playbook and design documents | `games/dos/wizardry-2/` | quest chain, floors, guardians, riddle answer, macros; each fact used here was re-checked on the Apple II or is marked | 2026-11-19 |
| Apple II Wizardry I playbook and tools | `games/apple2/wizardry/` | boot, keys, record layout, tools (copied and adapted) | 2026-11-19 |
No web source was fetched (the time went to the emulator). The manual was not read.

## Open questions
- Whether each guardian checks only its own piece (inferred), and what else reads the roster's items.
- Why the temple door met no random group in `gnilda_test` and always one from `@start` without gear; a fight
  there can be ended with `WIN` and the square entered again (not tried).
- Group 2-4 record layout in battle; `WIN` for a third and fourth group.
- Floor 2's riddle (3,6) (DOS: "shield"), floor 6's fixed fights, the other message squares: not tried here.
- Whether the six-member ending also loses a character when the staff comes from Gnilda (cannot happen in
  play as far as seen).
- ~~Temple, Boltac's, Inn level-up, chest open/disarm, U)se, trade~~: captured 2026-11-20.
- Utilities R)ECOVER, B)ACKUP, M)AKE SCENARIO DISK, U)PDATE, C)HANGE NAMES: text read, not used.
- Whether Wizardry III accepts characters with items (above).
- The other keys on the title; `iie` and an unprotected boot disk on this game.
