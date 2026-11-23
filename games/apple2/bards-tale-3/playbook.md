# The Bard's Tale III: Thief of Fate - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `python3 tools/play.py --name bt3 start apple2/bards-tale-3 --route @wild` (factory party
  *Interplayers, wilderness by the refugee camp) or `@ryz_wild` (new level-1 party RYZ CONDI EBO CUBI DEDDO MNZ).
  Model `iie`. Disks: 1 boot (ProDOS 8), 2 character disk (roster, save, **all 10 city/wilderness maps**),
  3 dungeon side A, 4 dungeon side B. Dump: all four disks good; disk 3 (second upload) checked level by level,
  every side-A level loads and plays (section "Dump check").
- **Boot:** `TITLE` (w900; title animates, never `settle`) -> space -> "Please insert your Character disk" ->
  `disk:2,space` -> "Restore your last saved game? Yes/No". `CAMP` answers No (Camp of Skara Brae menu);
  `RESTORE` answers Yes: the character disk holds the previous owner's **endgame save** (checkpoint
  `tarjan_save`: BILBO, EL CID, SIR JASON, KNIGHT, MERLIN, ILURE + a Vampire Lord, levels 30-60, at Tarjan).
- **Position (verified):** north `0009`, east `000A`, facing `000B` (0 N, 1 E, 2 S, 3 W). `AT:NN:EE` pokes
  both (hex) and turns left+right so the game evaluates the square (enters buildings, fires messages and
  fights). Same in cities, wilderness and dungeons.
- **Warps (verified):** from `@cat_stairs` (catacombs arrival, stairs prompt):
  `LV:XX:I` side-A dungeon level XX (hex), `LVB:XX:I` side-B level, I = its index in the dungeon's level list;
  `CITY:CC:NN:EE` city map CC at square N,E. Tables in "Game structure". The arrival square is wherever the
  stairs offset puts you: follow with `AT`.
- **Dungeons are dark:** `LIGHT` (Morganna of the factory party casts MAFL) before any dungeon view. The automap
  is `?` (shift+slash) in a dungeon: a window around the party, only squares marked visited.
- **Fights:** random encounters are frequent outdoors and in cities and depend on the frame: pick waits by
  preview (`AT:0F:0A,w60` gets into Skara Brae clean, `w150` meets Hookfangs). `@fight_puma` = 1 Puma on
  leaving the Scrapwood tavern; `f`, then one key per member (`a` attack, `d` defend; ranks 4-6 cannot
  attack), `y` to confirm; the round text scrolls by itself (`w100` steps).
- **Party records (verified):** 0400 + 0x80*n (7 slots, slot 7 = summoned monster). Exp +15 and gold +19
  are 32-bit little-endian; HP and SP are big-endian (+20 max HP, +22 current, +24 max SP, +26 current).
- **Traps that cost calls:** a level warp that changes disk needs the disk in the drive *before* `y` (the macros
  do it); city maps are on disk 2, not disk 1; `play.py checkpoint` output piped to /dev/null hid a failure once:
  read it. The scan tool (`tools/scan.py`) groups random fights too: look at the sheet.
- **Enter with `k`:** `i` only bumps a gate or building square; `k` (or Return) enters (verified 2026-11-21).
- **Endgame:** Tarjan stands at east 3, north 2 of his realm: `@tarjan_save,AT:02:03` = checkpoint
  `tarjan_meet` (speech, 3 pages) -> `tarjan_fight` (2 High Priestesses, 30 Black Slayers, 30 Rock Demons,
  1 Lorini) -> `tarjan_cmds`. Not won: the veteran party loses two members per round and the monster counts
  were not found in RAM (searched 0000-BFFF, aux, LC for 2,30,30,1): the ending is still open.
- **Hi-res text:** `games/apple2/bards-tale-3/font.json` (taught 2026-11-21): `play.py text` / `preview.py
  --text` read message windows (a few `?` left: grow it with `tools/hirestext.py learn`).
- **Maps:** `tools/maps.py [LEVEL ...]` writes `design/maps/` (58 levels; 2A-2C Malefia not loaded).
  Full automap: `tools/fill.py ROUTE`: poke every row of the level with byte 4 bit 0 set (shot
  `map_mountain_full`).
- **Sequences (2026-11-21):** `seq-dungeon-walk` (29) from `w_stairs34` (UnterBrae 1 stairs down at E12 N14,
  dark) -> `w_lit35` (UnterBrae 2 arrival on the stairs up, lit); `seq-automap` (18) from `m_lit35` (UnterBrae 2 by
  `LV:35:01`, arrival 0,0, automap empty). **Doors are passed with `k`**, `i` only faces them. A Mage Flame lasts
  ~30 moves. Fight-free walking: `tools/safewalk.py @cp "l,w60;i,w60;..."` picks a wait before each step;
  routes between squares from the decoded map: `tools/mazeroute.py`. UnterBrae 2 squares (east,north): stairs up
  12,14, stairs down 0,5 (sealed pocket), messages 12,13 (dry rot, drains SP), 14,10, 10,0, 1,3 (riddle), 0,4;
  forced fights 1,11 3,2 4,5 4,6 4,8 5,14 6,14 7,13 8,10 9,8 11,11 13,0 13,3 13,9 13,11; darkness 8-10,11.
  UnterBrae 1: stairs down 12,14, up 14,0, magic mouth 11,14 (scans: `work/scout/bards-tale-3/scan34|35`).
- **State (2026-11-21 capture):** `start` 54 shots and `main` 110 shots published; saves `01_start`,
  `02_shrine_saved`. Open: won fight with rewards, game over, the ending, encounter switch, Chronomancer travel.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | The Bard's Tale III: Thief of Fate (title screen "Bard's Tale III / The Thief of Fate") (verified) |
| Platform / model used | Apple II, `iie` (see `game.json`); boots ProDOS 8 V1.4 17-APR-87 (verified) |
| Release (region, year) | North America, 1988 (source: Wikipedia) |
| Developer / publisher | Interplay Productions / Electronic Arts; design Rebecca Heineman, Bruce Schlickbernd, Michael A. Stackpole (source; Stackpole credit also in the Interplay building, verified) |
| Genre | first-person party RPG, dungeon crawler with an automap |
| Players / save system | 1 player; save anywhere with `s` ("Do you wish to save your game?") to the character disk, restored at boot (verified) |

Disks (game.json "header"): `1 Program.dsk` ProDOS volume /BARDS.TALE3 (SPLASH, BARDSUBS1/2, UTIL, MUSIC,
MAINPIC, BARD3.PIC, CHANTAPPLE, BARD.SYSTEM, PRODOS ...); disks 2-4 are not ProDOS: the game reads them by its
own file numbers and tells the sides apart (inserting side B when side A is asked re-asks, verified).

### Dump check (2026-11-21)
- First upload: disk 3 was 165 bytes short and differed from track 23 on (coordinator). Replaced by the
  owner's second upload (SHA-1 5321b9de..., 143360 bytes) before any level was loaded here; nothing below
  comes from the bad image.
- New disk 3: every level file on side A (34 levels: 00-19, 1D-1E, 28-29, 34-37) was loaded through the
  stairs code (`tools/levels.py`): names, header, row tables and square data all consistent, arrival events
  and fights fire, automap draws. Side B (27 levels) and the 10 city maps on disk 2 load the same way.
  Verdict: **the dump is complete and intact as far as play can show.**

### Character disk roster (verified)
Ironpants, Gwendolyn, Shadow, Greenbolt, Morganna, Runeflinger, *Interplayers (the factory party: Ironpants
Dwarf Paladin 2, Greenbolt, Gwendolyn, Shadow, Morganna Conjurer (casts MAFL), Runeflinger Gnome Magician 2,
2000 exp each), then the previous owner's KNIGHT, EL CID, SIR JASON, BILBO, ILURE, MERLIN, GALAHAD, Black
Death. New characters are added at the end (RYZ is entry 15). The restorable save is the owner's endgame party.

## Boot sequence
- Intake probe: `work/intake/apple2/bards-tale-3/sheet.png`: ProDOS banner (~f60-400), black, title from ~f450,
  the bard's fire flickers (no settle).
- `TITLE` = `w900` (verified). `CHARDISK` = `TITLE,space,w1200,disk:2,space,w900` -> restore prompt (verified
  as one route). `CAMP` = `CHARDISK,n,w900`; `RESTORE` = `CHARDISK,y,w600,disk:4,space,w1200` (verified).
- New party: `@camp,MAKE6,ADD6` (checkpoint `ryz_party`), `e,w900` (`WILD`) leaves to the wilderness.
  Factory party: `@camp,PARTY` (adds *Interplayers).

## Controls
| Context | Key | Action | Status |
|---|---|---|---|
| Title | space | load the game (asks for the character disk) | verified |
| Camp | A R C D S L E | add member (scroll list, Return), remove, create, delete, save the party, leave the game, enter wilderness (with a party) | A C E verified |
| Create | M/F, race 1-7, class 0 3-9, name + Return; ESC rerolls | Human Elf Dwarf Hobbit Half-Elf Half-Orc Gnome; Warrior Conjurer Magician Rogue Bard Paladin Hunter Monk | verified |
| Walking | `i` forward, `j`/`l` turn left/right | trees, walls and buildings block | verified |
| Walking | `k` (or Return) | enter the building or gate square ahead, pass a dungeon door (`i` only bumps) | verified (doors: seq-dungeon-walk) |
| Walking | `?` (shift+slash) | outdoors: position and time of day; in a dungeon: the automap | verified |
| Walking | `1`-`7` | view a member (stats, exp, gold; Pool gold, Trade gold) | verified |
| Walking | `b` `c` `u` `d` `n` `p` `s` | bard plays, cast (4-letter code + Return), use item, drop member, new order, party (Defend / Party attack / Use), save game | verified (prompts) |
| Walking | `esc` | pause | verified |
| Encounter | `f` `a` `r` | fight bravely, advance ahead (when offered), run away | f r verified |
| Combat round | `a` `d` `p` `c` `u` | attack, defend, party attack, cast, use item; then "Use these commands? Yes/No" | a d verified |

Input timing: the default press works everywhere tried. Keys pressed while a message types are lost: use
`w200`-`w300` after a building or prompt.

## Game structure
Skara Brae is in ruins; the party starts at the refugee camp (camp menu = guild). Outdoors the wilderness of
Skara Brae (20x20) holds the camp, Scrapwood tavern, the Shrine, the gate into the Skara Brae ruins and seven
gate sites to the dimensions; Chronomancer spells travel between dimensions (source). Every map is a grid of
squares; the game counts 10 city/wilderness maps and 61 dungeon levels.

### City/wilderness maps (disk 2; `CITY:CC:NN:EE`, verified)
| CC | Name | Size | Landmarks (east,north) |
|---|---|---|---|
| 00 | Wilderness (Skara Brae) | 20x20 | camp 15,12; Scrapwood tavern 17,12; Shrine 1,8; Skara Brae gate 10,15; Cold Peak 0,19; Old Dwarf Mine 2,3; grove (Twilight Copse) 6,5; Vale of Lost Warriors 10,10; Crystal Springs 17,17; Sulphur Springs 18,1; Shadow Rock 19,9 |
| 01 | Skara Brae (ruins) | 17x17 | gate 0,10; storage building (free gear) 3,10; statue of Tarjan 8,12; Temple of the Mad God 11,12 (say TARJAN: catacombs); Interplay credits 13,14; Review Board 15,14 |
| 02 | Arboria | 12x12 | old tower (Valarian's) 1,4; lake building 1,10; fisherman 1,11; oak tree (acorns) 4,3; Deep Pit (Festering Pit) 9,3; Arefolia leaves 10,9; Hawkslayer 10,11 |
| 03 | Ciera Brannia | 16x16 | Forest Lawn temple 4,11; Wizard's Guild hall (Advancement, Spell Acquiring, Buy a new spell) 6,6; Sacred Grove 7,10; King's Court 8,12; Hic Haven tavern 3,12 |
| 04 | Gelidia | 16x16 | Outpost (frozen half-elf) 5,12; Ice Keep entrance 10,6 |
| 05 | Lucencia | 12x12 | Alliria's tomb 1,6; violet mountain 1,10; decrepit tower (Cyanis') 4,1; blue rose bushes 1,5 3,1 3,10 |
| 06 | Celaria Bree | 16x16 | Wizard's Guild 5,4; Alliria temple 7,2; Cheers tavern 7,13; Bard's Hall 9,13 |
| 07 | Nowhere (Tenebrosia) | 11x11 | dense forest (Copse) 1,3; tar pit (Gooey Stuff) 2,7; canyon 7,2 |
| 08 | Dark Copse | 11x11 | black door in the ashes 5,5 (arrival squares 2,2 and 1,1 ask for side B: not scanned) |
| 09 | Black Scar | 16x16 | Bard's Hall 6,7; Wizard's Guild 9,7; Twilight temple 0,10; tavern 2,5; side-B dungeon entrance 13,0 |
Squares: wilderness byte at 107F + 20*(19-N) + E (00 open, E2/E3/F2 trees, 04 rocks, x1 specials: 15 camp,
21 tavern, 31 shrine); level name at 1040, width/height at 1050/1051, row pointers from 1055.

### Dungeon levels (`LV`/`LVB`, file = level + 0x27 = `0003`; all loaded and checked)
Side A (disk 3): 00-01 Festering Pit, 02 Palace, 03-06 Tower (Valarian's), 07 Sacred Grove, 08-0B White
Tower, 0C-0F Grey Tower, 10-13 Black Tower, 14-15 Ice Dungeon, 16-17 Ice Keep, 18-19 Mountain, 1D-1E
Alliria's Tomb, 28 Catacombs, 29 Tunnels, 34-37 UnterBrae.
Side B (disk 4): 1A-1C Cyanis' Tower, 1F Wasteland, 20 Tarmitia, 21 Berlin, 22 Stalingrad, 23 Hiroshima,
24 Troy, 25 Rome, 26 Nottingham, 27 K'un Wang, 2A-2C Malefia (arrival teleports), 2D Barracks, 2E Ferofist's,
2F Private Quarter, 30 Workshop, 31 Urmech's Paradise, 32 Viscous Plane, 33 Sanctum, 38 Tar quarry,
39 Shadow Canyon, 3A-3B Sceadu's Demense, 3C Tarjan. Sizes 5x5 to 22x22 (`work/scout/bards-tale-3/levels.txt`).
Level header (1040): name, 1050 flags, 1052-1059 the dungeon's level list, 105A/105B/105C exit square and
city, 105D monster file, 105E/105F width/height, 1060/1061 position offset, row pointers from 1062; squares
5 bytes each (bytes 0-1 walls, 2-3 specials, **byte 4 bit 0 = visited/automap**).

Critical path (source: Wikipedia): Skara Brae (catacombs -> UnterBrae, Brilhasti ap Tarj) -> Arboria ->
Gelidia -> Lucencia -> Kinestia -> Tenebrosia -> Tarmitia -> Malefia (Tarjan).

## Shot plan
`shots.txt` holds 46 previewed lines (title, camp and creation menus, wilderness, Skara Brae landmarks, Review
Board menu, storage gear, temple, tavern, shrine, Puma fight, catacombs automap, Arboria, four dungeons, the
endgame save, lit dungeons, cities). Still to add by the capture agent:
- [x] lit dungeon views (`LIGHT`) on 16 levels of both sides (`env_lvXX`, XX = level id)
- [x] sequence sets `seq-dungeon-walk` (29 steps) and `seq-automap` (18 steps), UnterBrae 2
- [x] automap: Mountain as found, after a walk, and filled by poke (`map_mountain_*`); UnterBrae 1 walk
- [ ] a won fight with its reward text (Puma and Black Dragon outlast 2+ rounds; find the monster HP/count bytes)
- [x] spell casting in combat (start set: ARFI), bard song in combat (start set)
- [ ] a party wipe (`gameover`): HP pokes at 0422.. changed only Ironpants's Hits column; find the condition byte
- [x] Ciera Brannia Wizard's Guild and King's Court from the street (not entered); [ ] Hawkslayer joining
- [x] save prompt, silent save, restore at boot (start set)
- [x] `start` set: power-on -> camp -> RYZ party -> walk to Skara Brae -> storage -> Review Board -> temple ->
  catacombs -> Nefastmaster (fled, EBO dead) -> shrine (900 gold) -> save (54 shots, honest)

## Strategy and walkthrough notes
- The new party has no gold and level 1; the storage building in the ruins gives free starting gear (Plate
  Armor, Halbard, Long Bows, Arrows, Wineskin, Lamp ...).
- The Review Board sends the party under Skara Brae: temple, say TARJAN, catacombs (dark, light first); say
  "Chaos" to reach UnterBrae (source); then return to the Review Board for the quest.
- Factory party at level 2 beats a single Puma in two rounds (verified `fight_confirm`).

## Naming
RYZ CONDI EBO CUBI DEDDO MNZ via `MAKE6` (sex, race, class per member: RYZ m Human Warrior, CONDI f Dwarf
Paladin, EBO m Hobbit Rogue, CUBI f Half-Elf Bard, DEDDO m Elf Conjurer, MNZ f Gnome Magician; stats are
rolled from the frame, verified). Names are typed with `type:NAME\n`; the game shows capitals.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Endgame save on the character disk | `RESTORE` (checkpoint `tarjan_save`) | the dump | verified |
| City/wilderness warp | `@cat_stairs,CITY:CC:NN:EE` | RAM (stairs-up code 7B9D) | verified |
| Dungeon level warp | `@cat_stairs,LV:XX:I` / `LVB:XX:I` | RAM (stairs code 7B7B, loader 68B0) | verified |
| Square warp | `AT:NN:EE`, `FACE:n` | RAM | verified |
| Light | `LIGHT` (factory party) | play | verified |
| Exp, gold | records 0400+0x80n, +15 / +19 little-endian | RAM | verified on screen |
| Full automap | set byte 4 bit 0 of every square (catacombs already full) | RAM | verified (clearing empties the map) |

### Saves (rom/saves/apple2/bards-tale-3/, never committed)
| Name | Contents | Status |
|---|---|---|
| 01_start | RYZ party level 1 saved in the wilderness by the camp (export; restored with `sav:01_start,CHARDISK,y,w1200`) | verified |
| 02_shrine_saved | RYZ party after the catacombs (EBO dead, no gold) saved by the Shrine; `sav:02_shrine_saved,CHARDISK,y,w1200` | verified (start `54_restored`) |

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| 0009 / 000A / 000B | 1 each | north, east, facing (0 N 1 E 2 S 3 W) | find + poke, "?" text |
| 0003 | 1 | loaded map file (city CC+1D, level XX+27) | code 6632/68B6 |
| 000C | 1 | city/wilderness map number (exit target) | code 662F |
| 000D | 1 | index of the current level in the dungeon's level list | code 7B79 |
| 0035 | 1 | file number for the loader (668D) | code |
| 0400 + 0x80n | 0x80 | party records: +00 name (16, high bit, FF pad), +10 St IQ Dx Cn Lk, +15 exp (4 LE), +19 gold (4 LE), +1D level, +20/+22 max/cur HP (BE), +24/+26 max/cur SP (BE), +30 items (3 bytes each) | dump + view screen |
| 1040-... | | current map: name, header, squares (see Game structure) | dump |
| 17200 (aux) | | roster copies of the records | find |

## Emulation notes
- Title animates (fire): never `settle` on it. Wilderness and city views settle.
- Random encounters follow the frame: change a `wN` before the step to get or avoid one.
- Dungeon arrival via `LV` may land on a trap or a fight (Tunnels: spiked pit).

## Checkpoints
`title`, `restore_prompt`, `camp`, `party` (factory), `wild`, `ryz_party`, `ryz_wild`, `tarjan_save`, `skara`,
`review_board`, `storage`, `temple`, `sideA_prompt`, `cat_stairs` (warp base), `catacombs`, `fight_puma`,
`fight_confirm`, city bases `arboria` `ciera` `gelidia` `lucencia` `celaria` `nowhere` `darkcopse` `blackscar`.
Capture 2026-11-21: start set chain `s_review` (Review Board) -> `s_temple` -> `s_cat_lit` -> `s_fight1`
(Nefastmaster) -> `s_fight1_cmds` -> `s_fled` -> `s_shrine` -> `s_save_prompt` -> `s_saved` (all honest walking
from `ryz_wild`); endgame `tarjan_meet`, `tarjan_fight`, `tarjan_cmds`, `dragon_cmds` (Black Dragon at 2,0).
Sequences 2026-11-21: `w_stairs34`, `w_lit35` (dungeon walk), `m_lit35` (automap).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/The_Bard%27s_Tale_III:_Thief_of_Fate | release, credits, dimension order | 2026-11-21 |
| Search snippets (sorcerers.net, trueachievements) | via web search | UnterBrae reached by "Chaos" from the catacombs; level passwords | 2026-11-21 |
| GameFAQs | gamefaqs.gamespot.com BT3 FAQs | unavailable (403) | 2026-11-21 |
| mocagh.org reference card, discmaster.textfiles.com solution | | unavailable (host not allowed) | 2026-11-21 |
| ROM/RAM | this dump | maps, warps, records | 2026-11-21 |

## Open questions
- Wilderness walk camp -> Skara Brae gate: S, W x5, N x3, W x2, N x2, E, E, then `k` (route in checkpoint `s_review`).
- Square bytes 0-1 (walls) decode as nibbles N E S W, side & 3 = wall/door/other; bit 3 meaning unknown (Tarjan's level uses 8/9). Flag bytes 2-3 not decoded; events are elsewhere.
- `LV:00` (Festering Pit 1) from `@cat_stairs` stays on the stairs prompt; `LVB:1A` asks for the character disk; `LV:08`/`10` arrive dark or on a passage prompt.
- Random encounter switch (no NOFIGHT yet). The wilderness scan met 15 kinds of monsters.
- Review Board Advancement with enough exp (not tried); Wizard's Guild prices.
- Shops: none seen in Skara Brae; spells are bought in Ciera Brannia's Wizard's Guild.
- Dark Copse not scanned (`tools/scan.py darkcopse OUT w60 11`); city landmark coordinates come from scans whose arrival facing differed: a building that answers only "To the south you see ..." wants another facing (`FACE`).
- Chronomancer gate travel in play (from the wilderness gate squares).
