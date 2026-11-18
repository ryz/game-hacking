# Shin Megami Tensei (Super Famicom, English translation patch) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Facts marked **recalled** come from the scout's general knowledge of the game because the sites that
would confirm them were unreachable on 2026-11-17 (see Sources): treat them as leads, not as facts.
Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Shin Megami Tensei / 真・女神転生 (title screen shows both, plus "(C)2002 AEON GENESIS") |
| Platform / model used | Super Famicom, `snes` / `ntsc` (see `game.json`); LoROM, 2 MiB ROM, 8 KiB battery RAM |
| Release (region, year) | Japan, 30 October 1992 (source: Wikipedia). Never released in English on this console. |
| Developer / publisher | Atlus / Atlus (source: Wikipedia; Atlus logo at boot verified) |
| Version catalogued | Japanese cartridge + the Aeon Genesis English translation (2002) + its bug-fix patch, built by `tools/mkrom.py` (`game.json` "source"). All text seen so far is English (verified up to the town map). |
| Genre | First-person dungeon RPG with demon negotiation and fusion |
| Players / save system | 1 player; battery save, 2 files (verified: "FILE 1" / "FILE 2") |

## Boot sequence
- Intake probe: `work/intake/shin-megami-tensei/sheet.png` (no input: Atlus logo, magic circle, "199X Kichijoji,
  Tokyo", then a 512x448 hi-res "terminal" text sequence from about frame 1900, with 256x224 scene cuts between).
- Start skips the intro: one press during the Atlus logo jumps to the magic circle, a second one to the title
  (verified). `TITLE` = `w300,start,w120,start,w240,settle`. The title settles (static).
- Title menu: `START` / `CONTINUE`, Left/Right moves, A or Start confirms (verified).
- New game: there is no file or name menu. `START` drops straight into a **dream**: the game walks by itself
  through a red corridor (about 700 frames) to a talking door, then to three scenes. Buttons only advance text;
  the three name entries and stat allocations happen here (verified):
  1. the door asks the hero's name -> `ryz`, 18 stat points;
  2. a crucified man (the Law hero) -> `condi`, 18 points;
  3. a man held down by a demon (the Chaos hero) -> `ebo`, 18 points;
  4. a woman bathing in a pond introduces herself as "Yuriko" (no name entry here);
  then the hero wakes in his room, receives the Demon Summoning Program by mail (long text) and the first menu
  appears: `Computer / Save / Go to sleep / Leave the room`.
- `NEWGAME` = `DREAM,DREAM_RYZ,DREAM_CONDI,DREAM_EBO,WAKE` (from the title; about 80 s to replay, 20,000 frames).
- The **heroine** is not named in the dream. Recalled: she is named later in the story (when she joins after the
  Shinjuku events); use `cubi` there. Not reached by the scout.
- Checkpoints: `title`, `dream` (door's first message), `start` (room menu), `apartment` (free movement),
  `kichijoji` (town map), `lv23` (poked hero).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Intro | Start | skip to the next part / to the title | verified |
| Title | Left / Right | START / CONTINUE | verified |
| Title | A or Start | confirm | verified (`@title,start` and `@title,a`) |
| Text boxes | A (also B, X, Y, Start) | next page; a press while the text is still typing is swallowed or lost | verified (mother's dialogue advanced with each of them) |
| Name entry | D-pad | move over the letter grid (10 columns, 5 rows) | verified |
| | A | type the letter | verified |
| | B | delete the last letter | verified |
| | X | switch upper / lower case | verified |
| | Start | jump to `End`; then A confirms; then Yes/No | verified |
| Stat allocation | Up / Down | choose STR INT MAG VIT SPD LUK | verified (needs a 4-frame hold, see Input timing) |
| | Right or A / Left | add / take back a point | verified |
| | A at 0 points left | "This okay?" Yes/No appears by itself when the last point is spent; A = Yes | verified |
| Menus | Up / Down, A / B | move, confirm / back | verified |
| Battle | A on FIGHT / ESCAPE / TALK / AUTO (`D` to move) | party command; FIGHT -> per character SWORD / GUN / COMP / ITEM / DEFEND -> "Is this all right?" Yes | verified (run 2) |
| Battle text | `a,w90` per message | every message waits for a button; one `a,w90` per message is reliable | verified |
| Negotiation | A (`a,w150` per page) | next page; Yes/No and two-choice prompts start on the first entry | verified |
| 3D view, COMP | A, A, then `D` x4, A | Auto-Mapping (after the day-2 mail): grid of the squares walked | verified |
| 3D view (buildings, dungeons) | Up | step forward | verified |
| | Left / Right | turn 90 degrees | verified |
| | Down | turn around (180 degrees) | verified |
| | L / R | turn left / right (same as Left / Right as far as seen) | verified once each; strafing not seen |
| | A | command menu: `COMP / MAGIC / ITEM / STATUS` (yen and MAG shown while open) | verified |
| | B | close the menu | verified |
| | X, Y, Start, Select | nothing at the start of the game | verified (Y is the automap once a mapping spell or item exists: recalled) |
| Town map (2D) | D-pad | move the blue marker along the streets, one square per press (`MU MD ML MR` = 16-frame hold, wait 60) | verified |
| | A | ~~nothing~~ opens the command menu over a street view (seen on the squares with a police line after their scene; the scout saw nothing at the apartment square) | verified |
| | X, Y | nothing seen at the start | verified |
| Town map, walking into a building | D-pad toward it | enters the 3D view (clinic: left from 32,89; arcade: up from 39,8C) | verified |
| Shops | A / B | choose / back; B on the shop's main menu leaves the shop | verified |
| Exit squares | Yes / No prompt ("There is an exit here. Will you leave?"), default **No** | Up then A | verified in the apartment by the scout; in the clinic and the arcade the cursor starts on **Yes** (one `a` leaves) |

Input timing (verified):
- Default press (hold 8, wait 40) works for A/B and for Left/Right everywhere.
- **Up/Down in vertical lists move two rows with an 8-frame hold** (stat allocation, room menu). Use the macro
  `D` = `down:4,w30` (or `up:4,w30`). In the letter grid an 8-frame Up/Down moves one row.
- Text is typed slowly. A press that arrives while a page is still being typed is not reliably counted, so
  `a*10` or `mash` gives a different page count every time the spacing changes. Routes use `a,w150` per page
  (`a,w90` for short pages): then one press is exactly one page.
- ~~A macro cannot be repeated (`A*3` with a macro `A` fails: "unknown token"); repeats work on plain tokens only.~~
  True now (capture run, 2026-11-17): `MD*10`, `P*3` work. But `down:16,w60*10` repeats only the last token
  (`w60`): put the pair in a macro (`MD`) and repeat that.
- **A step given 60 frames after a door, a room scene or a text box can be lost** (arcade: leaving 5,5 north,
  leaving the cafe). Check the `x`/`y` watches after each leg, or add `w60` after such squares.
- A press right after pokes inside one `do` can arrive while a prompt is still typing: `F,poke:..,a` lost the
  `a`; use `F,w120` in one `do`, then `poke:..,w30,a,w150`.
- Screens with a blinking "more" arrow or the moon window never settle (`screen still changing`): normal.

## Game structure
Verified so far:
- **Dream** (automatic walk, naming) -> **hero's room** (menu: Computer = mail from STEVEN and the Demon
  Summoning Program manual; Save; Go to sleep; Leave the room) -> **mother** (gives 10000 yen, asks for coffee
  from the cafe in the mall; menu `Go to your room / Go outside`) -> **apartment corridor** (3D view) -> exit
  prompt -> **Kichijoji town map** (2D overhead, blue marker, "MOON'S AGE" and "PLACE" windows). A policeman
  blocks the edge of the district ("this area is currently off-limits").
- Three view modes: 3D first-person (buildings and dungeons, with a window showing moon phase, floor and
  facing), 2D town map, and full-screen menus (status, save/load).
- The moon phase advances as you walk (NEW MOON -> 1/8 -> 2/8 -> 3/8 during the dream and after).
- Command menu: `COMP` (Summon Minion / Return Minion / Dismiss Minion / Change Formation: the translation
  calls allied demons "minions"), `MAGIC`, `ITEM`, `STATUS`.
- Status screen: LVL, HP, MP, EXP, Next, Stat(us), equipment slots Swd / Gun / Ammo / Head / Body / Arm / Leg,
  derived values Power / Accur (sword and gun columns) / Defense / Evade / M.Power / M.Effect, and six stat
  bars STR INT MAG VIT SPD LUK.
- Saving: in the hero's room at the start (verified). Recalled: later at the terminals found in most districts,
  which also warp between each other once visited.

Verified by the capture run (2026-11-17), all in Kichijoji before any story progress:
- **Town map**: streets only. The marker starts at tile 32,86 (hex, RAM map). Squares marked with a pair of X
  are police lines: stepping on one plays the policemen's scene and nothing else (tried: 32,86 from the south,
  3F,86, the Inokashira Park entrance 34,94).
- **Clinic** (two red roofs): from `@map2` one `ML`. Four squares; `R,F,L,F,L,F` reaches the doctor, who says
  his daughter is out (two pages) and pushes the hero back. Checkpoint `bldg_red`.
- **Arcade** (yellow cross-shaped roof): `@map2,MD*3,MR*7,MU` (checkpoint `arcade`, square 7,6 facing north).
  Map from `tools/explore.py` (x,y in hex digits; north is up; walls drawn, gaps are open; incomplete):
  ```
           |71
  +--+--+--+
  |42 52|62 72
  +  +  +  +
  |43 53   |73
  +  +  +  +
     |54   |74
  +  +--+  +
     |55 65 75
  +  +--+  +
     |56 66|76
  ```
  Knife shop: west of 7,3 (`@arcade,F,F,F,L,F`; checkpoint `knifeshop` is its menu). Antique shop: north of 6,2.
  Cafe: north of 5,2 (the Master's three pages finish the mother's coffee errand: he will bring it to the house).
  A woman on 5,2 (walk north from 5,3) tells the hospital-director rumour, three pages. Other people stand west
  of 7,4 and around 4,2/4,3 (pages kept in `work/capture/explore/arcade/`, not captured).
  The step south from 5,3 to 5,4 failed several times in a row and then worked (input lost, not a wall).
- Checkpoints `armed` (Attack Knife bought and equipped, 5000 yen) and `coffee` (errand done).
- ~~**Not found: the way back into the apartment** from the map. The hero leaves onto 32,86; from there Up and
  Left do nothing, and coming back onto it from the south plays a police scene.~~ Solved in run 2: the
  apartment exit square is **32,88**, not 32,86 (run 1 read the decimal watch 134/136 as hex; the `home_map`
  checkpoint therefore warps to the wrong square, two north of the door). The apartment is entered with
  **Left from 32,88** (door table record `31 88 -> map 1A, square 2,1 facing west`). The apartment and the
  clinic are the same 3D map (1A; the doctor is "the doctor next door"); the home door is square 0,0, entered
  north from 0,1. Run 2 reached it before knowing this by entering the clinic and poking 7E070C/D = 0,1
  (checkpoint `home_back`); both ways give the same mother scene.

Verified in run 2 (2026-11-17), day 1 evening to day 2:
- Back home after the errand the mother talks about the park murder and Pascal (the dog). "Go to sleep"
  then only says "ryz went to sleep..." and the next morning repeats day 1 (the police sirens page): **the
  second dream needs story flag 9 (7E07C1 bit 02)**, which nothing seen so far had set (the event that sets it
  is unknown: not the cafe, the park police or the roadblock). Poking it (`poke:7E07C1=02` before "Go to
  sleep", checkpoint `dream2`) plays the second dream normally. Leads for the real trigger: the people in the
  arcade not talked to (west of 7,4, around 4,2/4,3) or a later line of the mother's ("Some strange old man was
  looking for you").
- **Second dream**: blue corridor, automatic walk; condi and ebo join the party table (ryz 22, condi 20/14 MP,
  ebo 22/9 MP), Yuriko appears, then a ceremony: hooded priests sacrifice a girl. "Will you save the girl?"
  (Yes), the girl asks to be called by name: **heroine name entry -> cubi**, Yes, then "Divide 18 points"
  (STR 7 INT 9 MAG 10 VIT 6 SPD 8 LUK 8, 16 HP 14 MP). She says they will not meet again until later.
- **Day 2 morning**: mother wakes ryz; new mail from STEVEN with the **Auto-Mapping Program**; the mother asks
  about the girl next door (cubi). Leaving the room: corridor 0,1 facing south; the exit is Left, F, F, F
  (square 3,1), Yes -> town map at 32,88.
- **Random encounters start on day 2 on the town map**: the first came at 32,93 (walking south from 32,88,
  then right/down toward the park), two Jirae Brownies. Battles are shown in the street view.

Recalled outline of the critical path (not verified, order from memory; Wikipedia confirms the three acts):
1. 199X Tokyo: Kichijoji (arcade/mall, Inokashira Park murder, hospital, the "Echo Building" terminal), then
   Shinjuku, the three factions (Gotou's coup, the US ambassador Thorman, the resistance), ending with the
   missile strike on Tokyo.
2. Kongokai (the Diamond Realm) and return to a ruined Tokyo 30 years later: Shinjuku, Shibuya, Roppongi,
   Ginza, Tokyo Tower, Shinagawa, Ueno, Ikebukuro; Law (Messians) against Chaos (Gaians); the flood.
3. The Cathedral: upper floors (Law side) and basement (Chaos side); the final bosses depend on alignment;
   three endings (Law, Neutral, Chaos) on the cathedral roof (source: Wikipedia).
Systems to expect (source: Wikipedia, except where marked): demon negotiation (talk to recruit, or get items
or money), fusion of two or three demons at the Cathedral of Shadows, alignment (Law / Neutral / Chaos) that
changes which demons join and which areas open, Magnetite (MAG) consumed by summoned demons while walking,
moon phases affecting negotiation (recalled: demons do not talk at full moon), guns with ammunition next to
swords (verified on the status screen), shops, healing stations, the casino and the "rag's shop" (recalled).

## Shot plan
Target about 45 shots (large RPG). Ids and categories; routes for the reachable ones are in `shots.txt`.
"Reach" says how. Both frame sizes are expected: 256x224 normally, 512x448 for the hi-res terminal intro.

Reachable now (routes in `shots.txt`):
- [x] `boot_atlus` boot - Atlus logo
- [x] `intro_circle` cutscene - magic circle of the intro
- [x] `intro_199x` cutscene - "199X Kichijoji, Tokyo"
- [x] `intro_terminal` cutscene - hi-res terminal text (512x448)
- [x] `title_screen` title - title with START / CONTINUE
- [x] `dream_door` dialogue - the talking door asks who passes
- [x] `name_entry` system - letter grid with "ryz" typed
- [x] `stat_allocation` system - dividing 18 points among six stats
- [x] `dream_law_hero` cutscene - crucified man and the messenger
- [x] `dream_chaos_hero` cutscene - demon holding a man down
- [x] `dream_pond` cutscene - the woman at the pond
- [x] `room_menu` menu - hero's room: Computer / Save / Go to sleep / Leave the room
- [x] `room_mail` dialogue - STEVEN's mail with the Demon Summoning Program
- [x] `save_files` save - "Save which file?" with FILE 1 / FILE 2
- [x] `load_files` menu - CONTINUE: "Load which file?" with the file summary
- [x] `home_mother` dialogue - mother hands over the allowance
- [x] `apartment_corridor` gameplay - first free 3D movement (also the `hud`: moon, floor, facing, party table)
- [x] `menu_command` menu - COMP / MAGIC / ITEM / STATUS with yen and MAG
- [x] `menu_comp` system - COMP: Summon / Return / Dismiss Minion, Change Formation
- [x] `status_hero` inventory - status screen (use `@lv23` for a mid-game look, or the start for level 1)
- [x] `exit_prompt` gameplay - street view with the exit prompt
- [x] `map_kichijoji` map - Kichijoji town map
- [x] `kichijoji_police` dialogue - policemen blocking the district

To be reached by the capture agent (play from `@kichijoji`; see Strategy):
- [x] `arcade_mall` gameplay - Kichijoji arcade (shops, cafe)
- [x] `shop_buy` shop - a shop's buy list with prices
- [x] `first_battle` battle - first demon encounter: command menu (run 2; also `battle_commands`, `battle_enemy_spell`, `battle_escape`, `battle_death`, `encounter_pixie`)
- [x] `battle_attack` battle - sword / gun attack result (sword; `battle_result` = EXP and yen)
- [ ] `battle_magic` battle - a spell being cast (needs the Law hero or a demon)
- [x] `demon_talk` system - TALK: Friendly / Threatening choice (plus `demon_talk_tease`, `demon_talk_ask`, `talk_fullmoon`)
- [x] `demon_talk_offer` system - a demon asking for yen / MAG / an item (plus `demon_talk_fail`: no Bead)
- [ ] `demon_joins` system - a demon becomes a minion (Pixies ask for a Bead after the yen; the item list RAM is not found, so no Bead could be given)
- [ ] `comp_summon` system - summoning a minion (MAG cost shown)
- [ ] `party_with_demons` hud - party table with humans and demons
- [ ] `cathedral_shadows` system - Cathedral of Shadows: fusion menu
- [ ] `fusion_result` system - fusion preview / result
- [x] run 2 story shots: `dream2_condi`, `dream2_yuriko`, `dream2_ceremony`, `dream2_save_girl`, `name_heroine`
- [x] extras captured outside the plan: `intro_scene`, `clinic_doctor`, `police_roadblock`, `shop_menu`, `shop_antique`, `arcade_rumor`, `cafe_master`
- [ ] `terminal_save` save - a terminal (save and warp list)
- [x] `automap` map - dungeon automap (COMP > Auto-Mapping, day 2, apartment corridor)
- [ ] `healing_station` shop - healing prices
- [x] `equipment` inventory - equipment screen with sword, gun, ammo, armour
- [ ] `items` inventory - item list
- [ ] `boss_first` boss - first story boss
- [x] `level_up` system - level-up with a stat point to place
- [x] `full_moon` system - full-moon window (town map only; the demon refusing to talk is still open)
- [ ] `alignment_choice` dialogue - a Law / Chaos choice
- [ ] `ruined_tokyo_map` map - Tokyo map after the 30-year jump (needs a late state: see Shortcuts)
- [x] `gameover` gameover - game-over sequence (first fight, hero poked to 1 HP)
- [ ] `ending`, `credits` - only with a late save

## Strategy and walkthrough notes
- From `@kichijoji`: the mother's errand (coffee from the cafe in the mall) is the first goal (verified text).
  Recalled: the arcade is entered from the town map; events there and a night's sleep ("Go to sleep" in the
  room) advance the story; the second dream gives the hero's first allies; the first demons appear after the
  program is used and the Law and Chaos heroes join. None of this was played by the scout.
- Never grind. Verified pokes that the game accepts and shows correctly: yen, MAG, hero level, the six stats,
  HP and maximum HP (`POKE_LV23`). The derived values on the status screen (Defense, Evade, M.Power, M.Effect)
  are **not** recalculated by a stat poke; "Next" is. Expect them to refresh at a level-up or equipment change
  (not tested): for a clean status shot gain one level after poking, or poke the derived words too (RAM map).
- With hero level 23 and 170 HP the early game cannot be lost by accident; for the `gameover` shot use the
  unpoked `@kichijoji` state.
- Negotiation outcomes depend on RNG, which follows frame timing: vary `wN` before the deciding press.
- Text: one `a,w150` per page. Before any Yes/No or naming prompt stop and look (the heroine's name entry comes
  unannounced after a dialogue).

## Naming
Hero **ryz**; Law hero **condi**; Chaos hero **ebo** (order in which the game asks, per the owner's party
order); heroine **cubi** when the game asks (not reached). Up to 8 characters; upper and lower case, digits and
some symbols; an empty name is refused (verified: the grid stays open). The grid opens in upper case with the
cursor on `A`; `x` switches to lower case and keeps the cursor.
- `NAME_RYZ` = `x,down,right*7,a,down,left*3,a,right,a,start,a` (ends on the Yes/No prompt; then `OK3`).
- `NAME_CONDI` = `x,right*2,a,down,right*2,a,left,a,up,a,right*5,a,start,a`
- `NAME_EBO` = `x,right*4,a,left*3,a,down,right*3,a,start,a`
- `OK3` = three pages (`Yes`, "has dormant power", "Divide 18 points") -> the stat screen.
- Stats (all six start at 5, 18 points to place; HP and MP follow VIT and MAG/INT as you place them):

| Character | STR | INT | MAG | VIT | SPD | LUK | HP | MP | Macro |
|---|---|---|---|---|---|---|---|---|---|
| ryz (hero, no magic) | 11 | 5 | 5 | 10 | 9 | 8 | 22 | - | `STATS_RYZ` |
| condi (Law hero) | 7 | 10 | 11 | 7 | 7 | 6 | 20 | 14 | `STATS_CONDI` |
| ebo (Chaos hero) | 10 | 6 | 8 | 9 | 8 | 7 | 22 | 9 | `STATS_EBO` |

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Skip the intro | `start` twice (`TITLE`) | found here | verified |
| Own save at the start | `sav:01_start,TITLE,CONTINUE` -> apartment corridor, file "Home, ryz Lev:01" | made here | verified |
| Yen | `set:7E0405=8973:4` | code list (address) + RAM search | verified (shown as 8973) |
| Magnetite | `set:7E0409=311:4` | found here | verified (MAG 311) |
| Mid-game hero | `POKE_LV23` (level 23, STR 19 INT 9 MAG 7 VIT 18 SPD 16 LUK 13, HP 167/178, 8973 yen); checkpoint `lv23` | found here | verified on the status screen; derived values stay at level-1 numbers |
| Pro Action Replay codes | Almar's Guides lists per-character and per-demon codes (e.g. character 1 strength `7E1010xx`, character 2 level `7E106Axx`, money from `7E0405`), "no random battles", item codes | almarsguides.com (search result only: the host is not reachable from the container) | the three addresses seen in the search result match the layout found here; the rest unread. Ask the coordinator to allow the host or the owner to save the pages. |
| Debug features | TCRF has a page for the game (the search result mentions a flag editor shared with the later games) | tcrf.net/Shin_Megami_Tensei_(SNES) | unavailable (403); not tried. Most valuable open lead for late-game states. |
| Late-game save from the web | GameFAQs "Saves" section | gamefaqs.gamespot.com | unavailable (403); a save made for the Japanese ROM should load in the patched ROM if the translation keeps the save layout (untested) |
| Town-map warp | at any exit prompt: `poke:7E07F5=XX,poke:7E07F6=YY,w30,a,w150` puts the marker on tile XX,YY with the map drawn correctly (used: arcade exit -> 32,86, checkpoint `home_map`; note 32,86 is two squares north of the apartment door 32,88). The tile must be a street, or the marker cannot move. Poking the tile while on the map does nothing useful. | found here | verified |
| 3D warp inside a building | `poke:7E070C=XX,poke:7E070D=YY` then turn: the view is redrawn from the new square (used: arcade 5,4 -> 7,6) | found here | verified |
| Moon phase | `poke:7E040F=70` then walk: the window turns to FULLMOON when the counter reaches 80 hex | found here | verified (`full_moon`) |
| Second dream | `poke:7E07C1=02` (story flag 9) at the room menu after the errand, then Go to sleep (checkpoint `dream2`) | found here (bit-by-bit test of 7E07C1) | verified |
| Back home from anywhere in Kichijoji | walk to 32,88 and press Left; or inside the clinic `poke:7E070C=00,poke:7E070D=01`, face north, step (checkpoint `home_back`) | found here | verified |
| Late state by poking | story flags found (7E07C0..), map id 7E0710; the meaning of most flags is unknown | - | open: see Open questions |

### Saves (rom/saves/shin-megami-tensei/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| none downloaded | GameFAQs and other save hosts were not reachable (403 / not allowed) | - | - | - |

Own saves (committed, `saves/README.md`): `01_start` (hero's room after the dream, File 1; `.sav` + `.state`), `03_second_dream` (day 2 morning in the hero's room after the second dream, cubi named, File 1; `.sav` + `.state`).

## RAM map (for `game.json` "ram" watches and pokes)
Work RAM, patched ROM. "poke" = written and seen on screen; "read" = value matched the screen, not written.
| Address | Size | Meaning | How found |
|---|---|---|---|
| 7E0405 | 4, little-endian | yen | `find "new == 10000"` after the allowance; poke 8973 shown. A byte written to 7E0408 changed the yen display (that is why it is 4 bytes) |
| 7E0409 | 4 (2 tested) | magnetite (MAG) | poke 0137 -> "MAG 311" |
| 7E0410 | 8 | hero's name, `FF`-padded (letter codes: `a`=25 ... `z`=3E) | read ("ryz" = 36 3D 3E) |
| 7E0418 | 8 | heroine's name (empty at the start) | inferred from the position |
| 7E0420 | 8 | Law hero's name | read ("condi") |
| 7E0428 | 8 | Chaos hero's name | read ("ebo") |
| 7E1000 | 0x60 each | character records: +000 hero, +060 heroine (blank: all stats 5), +0C0 Law hero, +120 Chaos hero; demons follow (per the code list, unread) | read against the three stat sets |
| record+0A | 2 | level | poke (hero 23) |
| record+10 / 12 / 14 / 16 / 18 / 1A | 2 each | STR / INT / MAG / VIT / SPD / LUK | poke (hero), read (condi, ebo) |
| record+26 / 28 / 2A / 2C | 2 each | Defense / Evade / M.Power / M.Effect as shown on the status screen | read (hero 10 / 12 / 6 / 6); not recalculated after a stat poke |
| record+2E / 30 | 2 each | HP / maximum HP | poke (167 / 178) |
| record+32 / 34 | 2 each | MP / maximum MP | read (condi 14 / 14, ebo 9 / 9) |
| record+0C | ? | EXP (0 at the start) | inferred, unverified |
| 7E09F3, 7E09F7, 7E0E00.. | 1 | change with every step in the 3D view (animation or step state, not coordinates) | `find` |
| 7E070C / 7E070D | 1 each | 3D position x / y inside the current building (west and north decrease) | RAM dumps before and after steps (`work/capture/ramdiff.py`); poke + turn redraws the view |
| 7E070E / 7E070F | 1 each | the square the building was entered on (clinic 02,03; apartment 0F,0E) | read only, inferred |
| 7E040D | 1 | facing: 0 north, 1 east, 2 south, 3 west (reads other values for a moment during scenes) | read against the window over eight turns |
| 7E040F | 1 | step counter; high nibble = moon phase in eighths (40 half moon, 80 full moon). +1 per 3D step, +16 at a time on the town map | read; poke 70 + walking gave FULLMOON |
| 7E0724, 7E07EE | 1 each | also +1 per 3D step (other step counters) | read |
| 7E07F5 / 7E07F6 | 1 each | town-map tile x / y of the marker (apartment exit 32,86; clinic door 32,89; arcade door 39,8B; park entrance 34,94) | RAM dumps; used for the exit-prompt warp |
| 7E0B04 / 7E0B06 (and 7E0B08 / 7E0B0A) | 2 each | town-map marker position in half squares (2 per square) and a scrolled copy; poking them does not move anything | read |
| 7E0710 | 1 | 3D map id: 07 arcade map (and town), 1A clinic + apartment building, set on entry from the door table | frame trace across the clinic entry |
| 7E0711 | 1 | zone inside the map (apartment corridor 0D, clinic 0A, hero's room 0E, arcade 07..0B): which scripts run | RAM diffs |
| 7E0714 | 1 | last building region entered (03 apartment, 04 clinic, 05 arcade); poking it inside a building gives "ERROR 00 01 SIGN A" | RAM diffs; do not poke |
| 7E07C0.. | bits | story flags, flag n = byte 7E07C0 + n/8, bit 1 << (n mod 8): flag 2 (07C0 04) set from the start, flag 3 (07C0 08) set while outside, flag 7 (07C0 80) set, flag 9 (07C1 02) opens the second dream, flag 12 (07C1 10) set while inside the cafe errand, flag 23 (07C2 80) coffee errand done | RAM diffs; flag 9 poked and the dream played |
| ROM 0x135C3 | 8 per entry | door table of the town map: x, y, square x in the building, y + facing (top 2 bits: 0 N 1 E 2 S 3 W), map id, 3 zero bytes (e.g. `31 88 02 C1 1A` = apartment, `31 89 02 C3 1A` = clinic, `39 8B 07 06 07` = arcade) | read; matches three doors |
| ROM 0x48F50 | FF-separated | item names (Attack Knife first ... Bead, Hiranya, Dis-Poison ...) | read |
| not found | - | floor, party list, demon records, item list (7E0781 changes when a sword is bought, but poking 7E0780.. did not put items in the ITEM list) | - |

## Emulation notes
First SNES game here; Mesen-S libretro backend. What was seen (2026-11-17):
- Colours, sizes and input are right: 256x224 for normal frames, 512x448 for the hi-res terminal intro (probe
  sheet); no garbage, no half-width text. All twelve buttons register.
- Deterministic: every checkpoint rebuilt from power-on with an empty cache gives the same frame as a cache hit
  (`work/scout/shin-megami-tensei/verify.sh`).
- Speed: about 250 frames per second (4x real time; the NES core runs about 520). `@start` from power-on takes
  about 85 s because the dream is 20,000 frames of slow text. Use checkpoints.
- `status` PC is almost always `0082f8` / `0081fc` (the frame-wait loop): useless as a hang detector here.
- No hang, no garbage and no untranslated text met up to the town map. Two cosmetic oddities of the translation:
  the facing word in the 3D window sometimes shows a trailing underscore (`EAST_`, `SOUTH_`) after moving, and
  the Chaos hero's stat prompt reads "paramenters". Neither is an emulator problem (the same frames replay).
- The dream walks by itself; there is nothing to steer until the room menu.

## Checkpoints
`title` (static), `dream` (door's first message; nothing named yet: start here to redo names or stats),
`start` (room menu: the first free choice, and the place to save), `apartment` (first free movement, 10000
yen), `kichijoji` (town map; its route contains the scout's control tests in the corridor, harmless),
`lv23` (apartment with the poked hero for menu shots), `lv23ready` (same after opening the status screen once,
so the party table shows 167/178), `map2` (town map at 32,89 beside the clinic), `bldg_red` (clinic entrance
square), `map_park` (park entrance after the police scene, command menu open: press `b`), `arcade` (arcade
entrance 7,6), `knifeshop` (knife shop menu), `armed` (knife equipped, arcade 7,3 facing east), `coffee`
(arcade 5,2 facing south, errand done), `home_map` (town map at the apartment square 32,86, warped there).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Shin_Megami_Tensei_(video_game) | release date, developer, systems, three acts, endings, translation group and year | 2026-11-17 |
| Almar's Guides, Pro Action Replay codes | https://almarsguides.com/retro/walkthroughs/snes/games/ShinMegamiTensei/ProActionReplay/ | three addresses visible in the search result (money 7E0405, character 1 strength 7E1010, character 2 level 7E106A) | 2026-11-17: host not reachable from the container (not on the allowed list) |
| The Cutting Room Floor | https://tcrf.net/Shin_Megami_Tensei_(SNES) | debug features (not read) | 2026-11-17: 403 |
| GameFAQs | https://gamefaqs.gamespot.com/snes/564888-shin-megami-tensei/faqs | walkthroughs, saves (not read) | 2026-11-17: 403 |
| StrategyWiki | https://strategywiki.org/wiki/Shin_Megami_Tensei | controls, walkthrough (not read) | 2026-11-17: 403 |
| Data Crystal | https://datacrystal.tcrf.net/ | no RAM map page for this game turned up in the search | 2026-11-17 |
| The game itself | `@start`, `@apartment`, `@kichijoji` | everything marked verified | 2026-11-17 |

## Open questions
- ~~How to re-enter the apartment from the town map~~ Left from 32,88 (run 2).
- Which day-1 event sets story flag 9 (the second dream). Not the cafe, park police or roadblock.
- Item list in RAM (needed to give a Bead and get the first minion). Next try: buy something at an item shop
  (not found in the arcade yet) and diff RAM before/after; or read the shop's buy code.
- Battle controls still to see: AUTO, magic (condi and ebo are only in the dream party so far), COMP summon.
- Map/area id and story flags (reading 7E0700-7E0730 at `@apartment`, `@bldg_red` and `@map2`
  showed only the position block changing; 7E0710 was 1A in all three; the arcade was not compared).
- ~~Position, facing~~ found (RAM map). Floor, map id and the story flags are not located: needed for a real
  late-game state. The TCRF page may describe a flag editor.
- Are the derived status values refreshed by a level-up or by equipping? (For clean poked status screens.)
- Party membership list (which records are in the active party) and the demon records: unread.
- Does a save made on the Japanese ROM load in the patched ROM?
- Where the heroine is named, and whether Y opens an automap from the start of the first dungeon.
- The recalled walkthrough outline needs a readable source (owner: a saved copy of a FAQ would do).
