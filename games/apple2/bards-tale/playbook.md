# The Bard's Tale: Tales of the Unknown - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.


> **Text (2026-11-21).** `font.json` (tools/hirestext.py) knows 50 glyphs taught on the cellar stairs, the first
> fight and the Guild: `play.py text` and `preview.py --text` read message windows. Teach more with
> `python3 tools/hirestext.py learn apple2/bards-tale --route @cp "line" ...` when `?` remain.

## Read first
- **Start:** `python3 tools/play.py --name bt start apple2/bards-tale --route @city` (new party RYZ CONDI EBO
  CUBI DEDDO MNZ outside the Guild) or `@city_hero` (same party poked to levels 8-9, status redrawn) or
  `@city_parker` (the archive's played party, level-13 monk). Model `iie`. Disks: 1 boot, 2 character,
  3 dungeon (everything seen so far), 4 second dungeon disk (not asked for yet).
- **Boot:** `TITLE` (w1100, title still black and white) -> space -> "Insert CHARACTER disk" -> `disk:2,space`
  -> Utilities menu -> `s` -> Guild. Macro `GUILD` does it all. Every dungeon entrance asks "Insert DUNGEON
  disk and press a key": `disk:3,space,w900..1200`. Taking the stairs out of a dungeon swaps nothing back:
  the game reads the character disk only in the Guild.
- **Warp in the city (verified):** `GO:XX:YY` = poke east coordinate (0001) and north coordinate (0000) in hex,
  then `j` (turn left) so the game evaluates the square: stand inside any building or on any special square.
  Building table below (City map). Facing: `FACE:n` (0 N, 1 E, 2 S, 3 W).
- **In a dungeon** the same `AT`/`GO` pokes move the party on the current level (22x22, wraps). Stairs prompts
  appear when you **step** onto the stairs square (`k`), not on a turn.
- **Level warp (verified 2026-11-21):** `@stairs_hero,LV:I-1:I:ID` loads level ID (hex) as index I of its
  dungeon (I-1 = FF for I = 0). IDs: 00 cellar, 01-03 Sewers, 04-06 Catacombs, 07-09 Castle, 0A Kylearan's
  tower, 0B-0F Mangar's Tower 1-5 (all on disk 3; disk 4 is never asked for). Add `NOFIGHT` before `LV` when
  the arrival square forces a fight (Catacombs 2, Castle 1, Mangar 1); then `GO:XX:YY` onto any square.
  Every level: `design/maps/` (`tools/allmaps.py`).
- **Final fight and ending:** `GO:0A:14` on Mangar 5, `space`x2 -> 2 Greater demons, 3 Vampire lords, Mangar;
  `poke:0408=000000` (group counts) + `f` + six `d` + `y` -> Treasure, Kylearan, 300,000 bonus (main set
  `ending_*`). Party wipe: poke HP low (`gameover_party_dead`).
- **Movement keys (verified):** `i` forward (bumps doors: "Ouch!"), `k` kick = forward through doors and into
  buildings, `j`/`l` (or `left`/`right`) turn, `shift+slash` (?) = where am I and time of day, `c` cast,
  `u` use item, `n` new order, `1`-`6` view a character, `p` party attack (attack own party), `b` bard plays a tune (needs an instrument). `up` does nothing in a dungeon.
- **Party records (verified):** 2CA80 + 0x80*n. HERO pokes them; the status lines redraw only after a change:
  `HEROP` = HERO + New order 1-5 (redraws). Gold and experience are decimal digits, one per byte.
- **Fights:** `@fight1` = 4 Skeletons + 1 Kobold on Main Street for the new party (honest, level 1: CONDI dies
  in round 1). Sewers fixed encounters with `GO` (Spinners, Black widows, a human party) for big parties.
- **Traps that cost calls:** `n` is New order (do not answer a Y-N prompt that is already gone with `n`);
  the title animates (never `settle` on it); the battle text scrolls by itself (pick frames with `w60` steps);
  scanning tools take 3-5 minutes (run in background).
- **More macros:** `SPELLS` (DEDDO Conjurer 4, MNZ Magician 4 + Conjurer 2), `ITEMS` (gear for the HERO party,
  EBO's Mandolin: bard songs need an equipped instrument), `KEEPFLAGS` (arrival square keeps its flags, maps).
- **State:** captured 2026-11-21: main 132 shots and start 45 published and verified, 16 level maps. Open:
  riddle answers and quest objects in play, bard tune effects, an honest won fight with rewards.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | The Bard's Tale: Tales of the Unknown (title screen: "The Bard's Tale / By Michael Cranford") |
| Platform / model used | Apple II, `iie` (see `game.json`) |
| Release (region, year) | North America, 1985 (title "(c) 1985 Interplay Productions"); cracked copy "Soft-cracked by Number 6", "Thanks to the artist 08/12/85" (verified) |
| Developer / publisher | Interplay Productions (Michael Cranford) / Electronic Arts (verified, title + EA logo) |
| Genre | first-person party RPG, dungeon crawler |
| Players / save system | 1 player; characters saved on the character disk at creation and on leaving dungeons/Guild; parties by name ("Save party", appear as `*NAME` in the roster) (verified) |

Disks (game.json "header"): `1 Program.dsk` boots; `2 Character.dsk` holds a **played roster**, not the factory
one (verified, Check roster): SCHENKER Hu, KLAUS Wa, LEGOLAS Ma, ALFAR Mo, *PARKER, PARKER Co,
*PARKER SS MGC, AURFAY Ba, LOJAI Ba, DEF Wa, *MANU, ALPHA Wa, BETA Wa, GANDALF Ma, ARAGORN Pa, ATHNALKOR Pa,
ELENDIL Pa, GAMMA Wa, DELTA Co, DARK Ma, PSYCHE Ma, EPSILON Wa (`*` = saved parties). *PARKER SS MGC =
ALFAR (Human Monk, level 13, 234 HP, 234785 exp), ELENDIL Pa, SCHENKER Hu, KLAUS Wa (dead), PARKER Co
(19 SP), AURFAY Ba: the HP values look hand-edited (three at 234). The scout's new characters and
*RYZ PARTY are added at the end of the list (export 01_start).

## Boot sequence
- Intake probe: `work/intake/apple2/bards-tale/sheet.png`: Apple //e, crack banner, "Soft-cracked by Number 6"
  + EA logo (~f250), black, the title picture drawn in black and white (~f400-1100), then in colour with
  "The song I sing / Will tell the tale / Of a cold and wintery day;" (~f1150 on), the bard animates.
- `TITLE` = `w1100` (black-and-white title; `@title,w300,!` = colour title). Verified.
- `GUILD` = `TITLE,space,w900,disk:2,space,w600,s,w600` -> "Thou art in the Guild of Adventurers" (verified).
  The space at the title loads the game screen and asks "Insert CHARACTER disk and press a key"; then the
  UTILITIES menu: (S)tart game, (C)opy char's, (M)ake a disk, (T)ransfer char's.
- New party: `@guild,MAKE6,ADD6` (checkpoint `party`), then `e,w900` exits to the city (checkpoint `city`).

## Controls
| Context | Key | Action | Status |
|---|---|---|---|
| Title | any key (space) | load the game | verified |
| Utilities | S / C / M / T | start, copy characters, make a disk, transfer characters | S verified |
| Guild | C A R D N 1-6 E | check roster, add member (type name, `*NAME` for a party), remove, disk options, new order, view, exit | verified (R untested) |
| Disk options | C S D L E | create member, save party, delete member, leave the game, exit | C S verified |
| Create | 1-7 race, then class key, then name + Return | Human Elf Dwarf Hobbit Half-Elf Half-Orc Gnome; classes 0 Warrior 3 Conjurer 4 Magician 5 Rogue 6 Bard 7 Paladin 8 Hunter 9 Monk (offered per race); ESC aborts | verified |
| View member | any key -> items page; E T D P (equip, trade, drop, pool gold); space leaves | stats page, then items with Sorc/Conj/Magi/Wizd spell levels | verified |
| City / dungeon | i | forward (stops at doors and building fronts) | verified |
| | k | kick: forward through a door, into a building | verified |
| | j / l, left / right | turn left / right ("Facing north" in the city) | verified |
| | ? (`shift+slash`) | street name / time of day ("You are on Main Street. It's now early morning.") | verified |
| | c, member, code + Return | cast (MAFL lights the dungeon; asks a target in fights) | verified |
| | u | "Who will use an item?" | verified |
| | n | New order (5 picks, the last is implied) | verified |
| | 1-6 | view member | verified |
| | y / n | answer Y-N prompts (stairs, portals) | verified |
| | up / down | nothing in a dungeon; up = forward in the city? | unclear |
| Shops | 1-6 member, B S I P E | buy, sell, identify, pool gold, exit; list: P)urchase F)orward B)ack | verified (list) |
| Tavern | O (who, drink letter) T E | order a drink (A B M F G W), talk to the barkeep, exit; Wine at the Scarlet Bard = cellar | verified |
| Temple | 1-6 / E | heal / exit | verified (screen) |
| Review Board | A S C E, member | advancement ("still needeth 2000 experience"), spell acquiring, class change | verified |
| Fight | F / R | fight or run | verified |
| Round orders | A (group a-d) P D U C (spell, target) and B? (bard song) | attack (places 1-3 only), party attack, defend, use, cast; "Use these attack commands? (Y-N)" | verified |

Input timing: the default press (hold 8, wait 40) works everywhere seen; menus need `w300`-`w400` after a key,
disk loads `w600`-`w1500`. Typing names with `type:NAME\n` works (capitals).

## Game structure
Guild (party) -> Skara Brae (city, 30x30, buildings below) -> dungeons in order: Wine cellar (1 level, under
the Scarlet Bard) -> Sewers (3) -> Catacombs (3, under the Mad God's temple, password TARJAN) -> Harkyn's Castle
(3) -> Kylearan's Amber Tower (1) -> Mangar's Tower (5) **(source: Wikipedia; entrances verified)**. The city
gate is blocked by snow; guardian statues (Stone Golem, Stone giant, Grey Dragon) bar the way to the castle
and towers; iron gates close Kylearan's and Mangar's towers ("beyond which stands ..."); a magic mouth
guards Mangar's: "none save Mangar may enter" **(verified)**. Poking the party onto an entry chamber skips
the gates and statues.

### City map (verified by `tools/cityscan.py city_parker`, coordinates x east, y north, hex for `GO`)
| Place | x,y | `GO` | Notes |
|---|---|---|---|
| Guild of Adventurers | 24,15 | 18:0F | start: party exits to 25,15 facing east |
| "Bard's Tale" credits room (Michael Cranford portrait) | 26,15 | 1A:0F | the building in front of the start (`k`) |
| Garth's Equipment Shoppe | 26,18 | 1A:12 | |
| Review Board | 23,20 | 17:14 | |
| Roscoe's Energy Emporium | 12,21 | 0C:15 | |
| Temple of the Mad God | 18,13-16 | 12:0D | S)peak to priest, type TARJAN -> Catacombs (disk 3) |
| Temples: 100 Blessings 8,25; Greatest gods 12,14; Great gods 14,18; Tmpl of Kiosk 21,3; Thief Temple 26,9 | | 08:19 ... | 15 temple squares in all |
| Taverns: Skull Tavern 1,8; Drawnblade 11,18; Archmage Inn 20,1; Ask Y'Mother 20,6; Dragonbreath 21,7; Sinister Inn 23,19; Scarlet Bard 28,5 | | 1C:05 = Scarlet Bard | Wine at the Scarlet Bard -> Cellars |
| Sewer portal ("Portal...") | 1,1 | 01:01 | Y -> Sewers (level byte 2), stairs "a long way up" |
| City Gate (snow drift) | 0,15 | 00:0F | |
| Harkyn's Castle entry chamber | 4,24 | 04:18 | T)ake stairs up -> Castle |
| Kylearan's Amber Tower entry chamber | 27,27 | 1B:1B | T)ake stairs -> Tower |
| Iron gates of Kylearan's tower | 25,27 / 27,25 | 19:1B | |
| Iron gates of Mangar's tower | 2,4 / 4,2 | 02:04 | |
| Magic mouth (Mangar's tower) | 2,2 | 02:02 | "none save Mangar may enter" |
| Guardian statues: Grey Dragon 6,24; Stone giant 4,26 and 21,2; Stone Golem 6,22 and 6,26 | | 06:16 | A)ttack / L)eave |
| Five squares 3,6 3,14 6,6 22,3 27,6 | | | blank message on a turn: unknown (statues? event squares) |
All other buildings: "You are in an empty building. (E)xit building".

## Shot plan
The plan is in `shots.txt` (48 lines, all previewed 2026-11-21: `work/preview/apple2/bards-tale/shots*.png`):
boot 1, title 2, menu 4 (utilities, guild, disk options, roster), system 8 (race, class, review x2, Roscoe,
temple, MAFL, ...), inventory 2, hud 1, gameplay ~17 (env city x2, where, gate, guardian, iron gate, magic mouth,
castle entry, cellar, sewers env/inscriptions/trap, catacombs, castle, tower), shop 3, dialogue 3, battle 8,
extra 1 (credits room). Still to add by the capture run:
- [x] env shots in every dungeon, lit (all 16 levels except Sewers 1 and Mangar 4: `env_*`)
- [x] victory report (`ending_treasure`, counts poked), party dead (`gameover_party_dead`); [ ] an honest won fight
- [x] bard song prompt (EBO with the poked Mandolin); [ ] a song in a fight and its effect
- [x] maps: `design/maps/` (16 levels, text + PNG, `tools/allmaps.py`)
- [x] Mangar's Tower, Mangar, ending (`boss_*`, `ending_*`)
- [x] `start` set: 45 shots, honest, ends with Save party (`s_saved`, export `02_first_save`)

## Strategy and walkthrough notes
- A level-1 party dies in the first city fight (4 Skeletons kill CONDI with 8 points); use `@city_hero`
  (levels 8-9, 33-87 HP) or `@city_parker` for anything beyond the first fight shots.
- Light: the dungeons are dark; MAFL (conjurer, 2 SP) shows the walls; without light the view is black.
- Doors: `i` bumps ("Ouch!"), `k` goes through. Stairs: step onto them with `k`/`i`, answer Y.
- Wine cellar stairs down at 7,18 (enter from 7,17 facing north with `k`) -> Sewers level 1 at 7,18.
- Catacombs: Mad God temple, `s`, type `TARJAN`, disk 3. **(verified)**
- Order of dungeons and their keys (Crystal Sword, Eye, Jade/Master key, riddles "SHIELDS", "SKULL TAVERN")
  **(source: GameFAQs summaries via search; not checked)**.

## Naming
Names are typed in capitals with `type:RYZ\n` after "Enter a name--". `MAKE:race:class:NAME` creates one
character (written to the character disk at once); `MAKE6` makes RYZ (Human Warrior), CONDI (Dwarf Paladin),
EBO (Human Bard), CUBI (Human Monk), DEDDO (Elf Conjurer), MNZ (Elf Magician); `ADD6` adds them. Rolled stats
depend on the frames before the race key (different routes give other numbers: RYZ had 6 HP in one route, 17 in
the checkpoint). There is no re-roll key: ESC and create again.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| City warp | `GO:XX:YY` (pokes 0001, 0000, then `j`) | RAM | verified |
| Dungeon position | `AT:XX:YY`, `FACE:n`, `WARPC:XX:YY:F` on the loaded level | RAM | verified (moves; events fire on step/turn) |
| Strong party | `HEROP` (levels, HP, SP, gold, exp of all six; redrawn by New order) | RAM | verified |
| Played party on the disk | `LOAD:*PARKER SS MGC` in the Guild (`@city_parker`) | archive | verified |
| Skip gates/statues | `GO` onto the castle/tower entry chambers | RAM | verified |
| Level warp | `@stairs_hero,LV:I-1:I:ID` (+`NOFIGHT`): pokes the level index `001E` and the dungeon's level table `2FC00+I`, then takes the cellar stairs; the stairs code (A7D3: INC 1E, LDA FC00,X -> E0, JMP 08B1 loader) loads the level | code | verified (all 16 levels) |
| No forced fight on arrival | `NOFIGHT` = `poke:A830=EAEA` (the INC $ED of the forced-fight square check) | code | verified |
| End the final fight | `poke:0408=000000` (counts of the up-to-four monster groups, text page memory) before the round | RAM | verified |
| Cheat codes | none known for the Apple II version; the web hosts with the manual and editors were not reachable | - | - |

### Saves (rom/saves/bards-tale/, never committed)
None downloaded. Own export: `01_start` (see `saves/README.md`), loads with `sav:01_start,GUILD,LOAD:*RYZ PARTY`
(verified).

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| 0000 | 1 | north coordinate (0 = south edge; city 0-29, dungeon 0-21) | diff + poke, verified |
| 0001 | 1 | east coordinate | diff + poke, verified |
| 0002 | 1 | facing 0 N, 1 E, 2 S, 3 W | poke + "Facing" message, verified |
| 0007 / 0008 | 1 | view-drawing scratch copies of y / x | code at AB34 |
| 0042 | 1 | monster level of the current level (copied from 2FC10 at A62D) | code |
| 001E | 1 | index of the current level in its dungeon (FC00 table); FF/below 0 -> back to the city at 2FC13/14 | code A7D3-A7F5, verified |
| 00E0 | 1 | level id handed to the level loader `08B1` | code |
| 0408 | 4 | monster group counts in a fight (Mangar: 02 03 01) | find, poke verified |
| 2CA80 + 0x80*n | 0x80 | party member n (0-5) record, also the roster buffer: +00 name (high ASCII, FF padded, 16), +10 4 bytes packed attributes, +1A..1F experience (6 decimal digits, one per byte; more digits may start at +14), +20 level, +22 max level (16-bit big-endian), +2A..2F gold (6 decimal digits), +30 max HP, +32 HP, +34 max SP, +36 SP (16-bit BE), +38 class (0 Warrior, 3 Conj, 4 Magi, 6 Bard, 7 Pala, 9 Monk; 1,2,5,8 by elimination: ?), +39 race (0 Human, 1 Elf, 2 Dwarf ...), +40..43 spell levels Sorc, Conj, Magi, Wizd (verified: Review Board purchase), +50..5F eight item slots of (status, id): status 0 carried, 1 equipped, 2 unusable; ids follow Garth's list (01 Torch .. 09 Staff), 08 Mace, 12 Leather Gloves, 14 Mandolin, 20 Mithril Dagger | records compared, pokes viewed, verified (gold, level, exp, HP, SP, items, spell levels) |
| 2F803 | 900 | city: building type per square (1-4 houses, others special), index uncertain | dump |
| 2F800 | 484 | dungeon walls, index y*22+x: bits 7-6 west, 5-4 east, 3-2 south, 1-0 north; 0 open, 1 wall, 2 door, 3 secret door? | verified against bumps at the cellar stairs |
| 2FA00 | 484 | dungeon square flags (dungeon code A80C, mask table B0B8): 01 stairs up, 02 stairs down, 04 special event, 08 darkness ("Darkness!", puts out light), 10 trap (cleared when it fires), 20 portal down (key D), 40 portal up (key E, needs levitation), 80 forced fight (cleared). ~~10 darkness~~ was wrong (scout) | code + verified |
| 2FC00 | 8 | level ids of this dungeon (cellar/sewers 00 01 02 03, Catacombs 04-06, Castle 07-09, Kylearan 0A, Mangar 0B-0F) | dump, verified |
| 2FC13 / 2FC14 | 1+1 | city y / x to return to when the party leaves upwards | code A7E9 |
| 2FC15 | 1 | stairs direction parity (0 dungeons go down, 3 towers and castle go up) | code A7A3 |
| 2FC10 | 1 | level number in the dungeon file (cellar 0, sewers 1 = 1, portal sewers 2; city 03 = other data) | dump |
| 2FC16 | 10 | level name, high ASCII ("Sewers", "Cellars") | dump |

## Emulation notes
- `iie` works; no write protection needed. The character disk is written when characters are created and when
  a party is saved; exports hold the whole disk images.
- The title animates (bard) and the fight portraits animate: end routes there with `!` or a fixed wait.
- Fight text scrolls automatically, about a line every 30 frames.
- `tools/cityscan.py CHECKPOINT OUT [WAIT] [SIZE] [EXTRA]` pokes the party onto every square and groups the
  screens (city 5 min, a dungeon level 3 min); `tools/groupsheet.py` makes a sheet of the groups;
  `tools/maps.py ROUTE` prints the loaded dungeon level as a text map with stairs/events/darkness.
- Random encounters come with time and steps: `PACE*3` from `@city` met the skeletons; the same route always
  meets them (deterministic).

## Checkpoints
| Name | What |
|---|---|
| title, guild, party, city | boot chain; party = six new characters added |
| city_hero, cellar_hero, cellar_hero_lit | HERO party in the city, at the cellar stairs, lit |
| fight1 | first random encounter (new party) |
| city_parker, cellar_parker, sewers1_parker | archive party; Cellars; Sewers level 1 from the cellar |
| sewers_portal, sewers_portal_lit | Sewers via the city portal (level byte 2) |
| catacombs_parker, castle_parker, tower_parker | Catacombs 1 (TARJAN), Harkyn's Castle, Kylearan's tower |
| stairs_hero | HERO party lit, facing the cellar stairs down: base of the level warp `LV` |
| s_fled, s_healed, s_bought, s_saved | start set: first fight run from, temple, Garth's, party saved (export `02_first_save`) |

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/The_Bard's_Tale_(1985_video_game) | release, classes, dungeon list and level counts | 2026-11-21 |
| GameFAQs / StrategyWiki | gamefaqs.gamespot.com (PC/NES guides), strategywiki.org | refused (403) | 2026-11-21 |
| Manual scans | archive.org `The_Bards_Tale_Manual_HQ` (redirects to a download host outside the allowed list), mocagh.org, oldgames.sk, bardstaleonline.com | unreachable from the container; ask the owner to allow `*.archive.org` download hosts for the manual (spell codes, keys) | 2026-11-21 |
| comp.sys.apple2 thread (search snippet) | groups.google.com | names on the character disk are high ASCII | 2026-11-21 |

## Open questions
- ~~Level warp~~ solved (LV). ~~Which Sewers level the portal leads to~~: Sewers 3 (walls identical).
- Mangar's Tower: the honest entry route (Kylearan's tower, the three shapes) not played; disk 4 was never
  asked for (Mangar's Tower is on disk 3): what disk 4 holds is unknown.
- Riddle answers (Kylearan's magic mouths, "What can bind the mightiest foes?" = Spectre Snare per the rumour).
- Class codes 1, 2, 5, 8 and race codes 3-6 in the record; item list format at +40.
- Spell codes beyond MAFL and ARFI (manual not reachable); bard songs need an instrument?
- The five blank-message city squares (3,6 3,14 6,6 22,3 27,6).
