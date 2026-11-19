# Phantasy Star - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Phantasy Star / ファンタシースター (verified: title screen "PHANTASY STAR", "(C) SEGA 1988") |
| Platform / model used | Sega Master System, model `ntsc` (header region Export) |
| Dump | 512 KiB, SHA-1 `257ca76ebcd54c75a414ca7ce968fa59ea42f150`, CRC32 `e4a65e79`, header product 9500, version 2. Export (US/Europe) release; the copyright year 1988 and version 2 point to the first export revision (the "v1.2" that the SMS databases list; a later "v1.3" export revision exists). Not matched against a No-Intro list here: Dat-o-Matic, SMS Power and libretro-db are outside the allowed hosts. Genesis Plus GX's own database lists only the Japanese CRCs (6605D36A etc.). |
| Release (region, year) | Japan 1987-12-20 (Mark III/Master System, FM sound); North America and Europe 1988 (this dump); Brazil 1991 (Tec Toy, Portuguese) (source: Wikipedia) |
| Developer / publisher | Sega (design Kotaro Hayashida, program Yuji Naka, art Rieko Kodama, story Chieko Aoki, music Tokuhiko Uwabo) (source: Wikipedia) |
| Genre | Turn-based RPG: top-down towns and overworld, first-person 3D dungeons, first-person battles with animated monsters |
| Players / save system | 1 player; battery-backed cartridge RAM, 5 save slots, save anywhere outside battle (verified). No naming of characters or files in this release (verified: SAVE asks only for a slot number) |

## Boot sequence
- Intake probe: `work/intake/sms/phantasy-star/sheet.png`: black until ~frame 100, then the title (logo, Alis
  with sword, START / CONTINUE, "(C) SEGA 1988") from ~frame 120; no attract mode within 30 s. The cursor
  blinks (the title never settles; `settle` stops at its limit, harmless).
- `TITLE` = `w150` (verified). Inputs are read from about frame 240: a `down`/`up` before that is lost.
- `NEWGAME` = `b1,w300,PAGE*10,w30` with `PAGE` = `b1,w240` (verified from power-on as one `do`, and in the empty-cache check).
  `b1` (or `b2`) on START -> planet in space (w300) -> 10 pages: "SPACE CENTURY 342, CAMINEET ON PALMA",
  Nero beaten by Lassic's robotcops ("SCUM! DO NOT SNIFF AROUND IN LASSIC'S AFFAIRS!"), Nero's last words
  (4 pages, names Odin), Alis's vow (2 pages: "PROTECT ME, NERO!"), then control: Alis on the path in
  Camineet beside her house. An 11th press would open the field menu.
- `CONTINUE` (after `TITLE`) = `w90,up,w30,b2,w120,b2,w120,b2,w180` (verified with `sav:01_start`): `up` moves the
  cursor to CONTINUE (a single `down` did not move it), `b2` -> "CONTINUE GAME- YES / DELETE GAME- NO" -> YES
  -> "CONTINUE A GAME. SELECT A NUMBER." list 1-5 -> slot 1 -> Camineet. Without a valid save the title starts
  a new game.
- Other macros (`game.json`): `MENU` = `b1,w120` (field menu ready for input); `PACE` = `down:64,up:64` (walk
  back and forth for encounters); `TOWNPOS:XXXX:YYYY` = poke Alis's town position, bytes little-endian
  (`TOWNPOS:5006:4001` = X 0x650, Y 0x140), takes effect with the next step, towns only; `FLASH` = after the
  "PITCH BLACK" message with a FLASH carried: close it, ITEM, FLASH, USE (verified as one route from `cave_out`).
- Pages type out letter by letter: one press per page with a fixed wait (`PAGE`); a press while a page types
  completes it instead of turning it (seen with `b1,w150`).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | `up` / `down` | cursor START / CONTINUE (`up` from START goes to CONTINUE) | verified (`up`); `down` did not move it once (open question) |
| Title | `b1` or `b2` | choose | verified (both start a new game) |
| Intro / dialogue | `b1` or `b2` | next page (completes a page still typing) | verified (`b1` in the intro, `b2` in the shop) |
| Field, town | D-pad | walk; 1 pixel per frame, one tile = 16 frames (`left:16`); hold to keep walking | verified |
| Field, town | `b1` or `b2` | open the field menu STAS MAGC ITEM SRCH SAVE (over a picture of the current place) | verified |
| Field, town | walk into a door / shop / cave | enter | verified (house, shop, cave) |
| Menus | D-pad | cursor | verified |
| Menus | `b2` | confirm | verified |
| Menus | `b1` | cancel / close (closing the field menu returns to the map) | verified |
| Dungeon | `up` | step forward; `down` back (source) | verified (`up`) |
| Dungeon | `left` / `right` | turn 90 degrees | verified (`right`) |
| Battle | `b2` / `b1` | confirm command / cancel | verified (`b2` = ATTK) |
| Any | `pause` | pause (manual: pauses and mutes) | source; no visible change on the map (verified: `pause` in Camineet showed nothing) |

Input timing: the default press (hold 8, wait 40) works in menus and dialogue, but the field menu needs about
**120 frames** after it opens before it takes input (`b1,w60,down*2` left the cursor on STAS; `b1,w120` works):
macro `MENU` = `b1,w120`. Shop windows and the item list take `b2,w90` per step. Walking: `DIR:N` with N a
multiple of 16; blocked moves turn Alis without moving.

## Game structure
(source: manual, Wikipedia; verified where marked)
- Algol star system, three planets: **Palma** (green, forests, the start; Camineet, spaceport), **Motavia**
  (desert, Paseo the governor's town), **Dezoris** (ice). Travel by spaceship between planets (PASSPORT).
- Party of four with fixed names: **Alis** (verified, the heroine), **Myau** (talking cat, magic), **Odin**
  (warrior, heavy weapons and armour), **Noah** (esper, magic; Lutz in the Japanese version).
- Story: Lassic's robotcops kill Alis's brother Nero (verified, intro); Alis gathers Myau, Odin and Noah,
  defeats Lassic, then Dark Falz (source: Wikipedia). Where each joins and where Lassic lives: unverified
  recollection, confirm in play.
- Views: towns and overworld from above (verified); dungeons, towers and caves in first person, pixel-scrolled
  3D corridors (verified); battles first person with one animated monster and its HP (verified); shops and
  churches as a person behind a counter (verified: second-hand shop); dialogue with portrait windows.
- Field menu STAS / MAGC / ITEM / SRCH / SAVE (verified). STAS: weapon and armour, LV, EP, ATTACK, DEFENSE, MAX HP,
  MAX MP, MST (verified). ITEM: MST and up to 24 items, each USE / EQP / DRP (verified with FLASH: USE lit the cave).
  SRCH: "THERE DOESN'T SEEM TO BE ANYTHING" (verified). SAVE: slot 1-5 (verified).
- Battle commands ATTK MAGC ITEM TALK RUN (verified); a beaten monster may leave a treasure chest, "DO YOU WANT
  TO OPEN IT?" YES/NO -> meseta (verified: SWORM, 2 EP, chest with 3 meseta) or a trap (source).
- Vehicles: LANDROVER (fast on land), HOVERCRAFT (water), ICE DIGGER (ice walls on Dezoris); ROADPASS for the
  moving road; PASSPORT for the spaceport (source; item names verified in the item list).
- Dark dungeons need light: walking into the cave south-west of Camineet without it gives "CANNOT GO FORWARD,
  IT'S PITCH BLACK." (verified); a FLASH (second-hand shop, 20 MST) lights it (verified); MAG. LAMP later (source).
- Camineet (verified): Alis's house north of the start, three shops in a row to the south-west (one is the
  second-hand shop: FLASH 20, ESCAPER 10, TRANSER 48), a church (cross dome) to the south-east, a cave-like
  building north-east, EXIT gate in the south-east corner guarded by a robotcop; townspeople walk about.

## Shot plan
The routes are in `shots.txt` (early section with routes that replay; the rest as plan comments). Categories
and counts (about 75 shots, a large RPG):
- **early (routes ready, do first, ~20):** title, intro (planet, caption, Nero beaten, Nero dying, Alis's vow), first
  control in Camineet, Camineet shops/church, the field menu, STAS, ITEM (with a few items), SRCH message, SAVE
  slot list, CONTINUE prompt and slot list, second-hand shop (BUY/SELL, price list, purchase), overworld outside
  Camineet, first battle (SWORM: command menu, kill message, EXP, treasure chest), SCORPION, the dark cave
  message, the lit first-person dungeon, the HUD box.
- **later (play/pokes):** every town (names from recollection, unverified: Camineet, Parolit, Scion, Eppi,
  Gothic, Loar, Abion, Bortevo on Palma; Paseo, Uzo, Casba, Sopia on Motavia; Skure on Dezoris); spaceport
  and the spaceship flight; Myau joining (Paseo), Odin in the cave, Noah (Lutz) at Abion; party STAS with four
  members; every vehicle in use; each planet's overworld; towers and dungeons; the churches (revive);
  magic in and out of battle (spell names per the manual OCR summary: HEAL, CURE, FIRE, WALL, ROPE, BYE, FLY,
  CHAT, TELE, OPEN, RISE ...; confirm on MAGC); TALK with a monster; RUN; a trap chest; game over; bosses
  (Lassic, Dark Falz; others to be found); the ending and credits.
- **Distinctive systems to show:** the pixel-scrolled first-person dungeon (a clip of a step and a turn), the
  animated monster in battle, monster TALK, the vehicle travel, the spaceport, light in dark dungeons.

How to reach: early areas by play from the checkpoints below; later places by playing with pokes (party
stats, meseta, items through `C4xx`, see RAM map) and `gs:` for infinite HP. Overworld and town position pokes
do not warp (see Emulation notes); the capture agent should look for a map id / pending-transition variable
(`C308`/`C309` change between Camineet and the overworld) or use a late save. No downloaded save found.

## Strategy and walkthrough notes
- Alis starts alone at level 1, 16 HP, 0 meseta, no items, Short Sword and Leather Armour (verified). Early
  monsters (SWORM 8 HP, SCORPION 12 HP) are weak but Alis has 16 HP: hold HP with `gs:00C4-0110` (Alis 16) or
  poke `C401`/`C406` up while levelling by poke (realistic values: level 8-12, HP 60-70 for the mid game).
- Encounters on the overworld: none in ~30 short walks next to Camineet; the first came after ~10 long walks
  south-west into the forest (`battle` checkpoint). The forest/field south of the wall is the early hunting ground.
- Leaving Camineet: the walking route to the EXIT gate is long; the `palma` checkpoint pokes Alis next to the
  gate (`poke:C301=5006,poke:C305=4001,down:16`): in towns a position poke works when the next step
  enters the gate.
- The wall south-west of Camineet has a gap on its east side: `field_sw` -> `up:48,right:80,down:96` (route in
  `field_s`). The cave is then `down:32,left:160` and is entered from below (`down:16,left:16`).
- Dark caves: carry a FLASH (`poke:C4C0=27,poke:C4E2=01` = one FLASH) and USE it after the "PITCH BLACK"
  message: `b2` (closes the message, opens the menu), `w60,down*2,b2,w90` (ITEM), `b2,w90` (FLASH), `b2,w120` (USE).
- Critical path: no walkthrough was reachable (GameFAQs/StrategyWiki 403). Outline from the manual and
  Wikipedia (source): Alis seeks Odin (named by Nero), meets Myau on Motavia and Noah, gathers Laconian
  equipment, defeats Lassic, then Dark Falz. Order of towns and key items (PASSPORT, ROADPASS, LAC. POT,
  HAPSBY, PRISM, AMBR EYE, CRYSTAL ... all in the item list, verified) is **unverified recollection**: work it
  out from NPC dialogue while playing, or ask the coordinator to allow a walkthrough host.

## Naming
No character naming: the four heroes have fixed names (verified for Alis; source for the others). The US
SAVE takes no file name either (verified: slot number only; the manual's name-registration screen with
RUB/ADV/END belongs to the Japanese release or was not kept, open question). So **ryz** cannot be entered anywhere.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Meseta | `set:C4E0=8973:2` (16-bit, little-endian; shown in ITEM/STAS/shops when the window opens) | RAM search | verified |
| Items | `poke:C4C0=ID..` (one byte per slot, up to 24) + `poke:C4E2=N` (count) | RAM | verified (ids table below) |
| Alis stats | `C401` HP, `C402` MP, `set:C403=E:2` EXP, `C405` level, `C406` max HP, `C407` max MP | PAR code layout + RAM | verified on STAS |
| Infinite HP | `gs:00C4-X1VV` (X = 0 Alis, 1 Myau, 2 Odin, 3 Noah; VV = HP to hold), e.g. `gs:00C4-0110` | smstributes code list (via search snippet: "00C4 X1FF infinite HP", "00C4 X2FF infinite MP") | verified (Alis held at 16 through hits) |
| Infinite MP | `gs:00C4-X2VV` | same | source |
| Exit Camineet | `@start,poke:C301=5006,poke:C305=4001,down:16,w120` | own | verified (`palma`) |
| Light a dark cave | FLASH in the inventory, USE it | own | verified (`dungeon`) |
| Debug menu / sound test / level select | none known | TCRF page unavailable (403) | open |

### Saves (rom/saves/phantasy-star/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| (none) | GameFAQs refused automated access (403); no save fetched | - | - | - |
Own save: `games/sms/phantasy-star/saves/01_start.sav` (new game, slot 1), checkpoint `continue`.

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| `C400` + 16*n | 16 | character record, n = 0 Alis, 1 Myau, 2 Odin, 3 Noah: +0 alive (1), +1 HP, +2 MP, +3/+4 EXP (LE), +5 level, +6 max HP, +7 max MP, +8 attack, +9 defense, +A weapon, +B armour, +C shield (+A..+C are item ids: Alis `02` Short Sword, `10` Leather Armour) | PAR codes `00C4X1..` + peek + pokes shown on STAS (verified for Alis) |
| `C440` + 16*n | 16 | monster records in battle, same layout (+1 HP, +6 max HP, +8 attack, +9 defense); SWORM: HP 8, attack 13, defense 9 | RAM search (HP after a hit) |
| `C4C0` | 24 | inventory, one item id per slot | pokes, ITEM window |
| `C4E0` | 2 | meseta (LE binary) | pokes, ITEM window |
| `C4E2` | 1 | number of items carried | buying a FLASH 0 -> 1 |
| `C301`/`C302` | 2 | Alis X in pixels (towns and overworld; a tile = 16), copy at `C313` | RAM diff while walking |
| `C305`/`C306` | 2 | Alis Y in pixels, copy at `C311` | RAM diff |
| `C308`, `C309` | 1 | 04 in Camineet, 00 on the overworld: map/town id (inferred) | peek in three places |
| `C30A` | 1 | dungeon facing (0 at entry, +1 per right turn) | RAM diff |
| `C30C` | 1 | dungeon square, high nibble row, low nibble column (`DC` at the cave entry, `CC` after one step) | RAM diff |
| `C315` | 1 | 04 in the cave (dungeon id? inferred) | peek |
| cartridge RAM `0000` | 32 | "PHANTASY STAR         BACKUP RAM" signature; the game formats 8 KiB if it is missing | backend test |
| cartridge RAM `0201`.., `0400`+ | | slot used flags (inferred), slot 1 data from `0400` (a copy of `C300`... / `C400`...) | exported save |

Item ids (verified on the ITEM list, 0x41 and above are garbage):
`01` WOODCANE `02` SHT. SWD `03` IRN. SWD `04` WAND `05` IRN. FANG `06` IRN. AXE `07` TIT. SWD `08` CRC. SWD
`09` NEEDLGUN `0A` SIL. FANG `0B` HEAT. GUN `0C` LGT. SABR `0D` LASR. GUN `0E` LAC. SWD `0F` LAC. AXE `10` LTH. ARMR
`11` WHT. MANT `12` LGT. SUIT `13` IRN. ARMR `14` THCK. FUR `15` ZIR. ARMR `16` DMD. ARMR `17` LAC. ARMR `18` FRD. MANT
`19` LTH. SLD `1A` BRNZ. SLD `1B` IRN. SLD `1C` CRC. SLD `1D` GLOVE `1E` LASR. SLD `1F` MIRR. SLD `20` LAC. SLD
`21` LANDROVR `22` HOVRCRFT `23` ICE DIGR `24` COLA `25` BURGER `26` FLUTE `27` FLASH `28` ESCAPER
`29` TRANSER `2A` MAGC HAT `2B` ALSULIN `2C` POLYMTRL `2D` DUGN KEY `2E` SPHERE `2F` TORCH `30` PRISM
`31` NUTS `32` HAPSBY `33` ROADPASS `34` PASSPORT `35` COMPASS `36` CAKE `37` LETTER `38` LAC. POT
`39` MAG. LAMP `3A` AMBR EYE `3B` GAS. SLD `3C` CRYSTAL `3D` M SYSTEM `3E` MRCL KEY `3F` ZILLION `40` SECRETS

Party members: setting `C410` (Myau alive) and his HP/level did not add him to the party windows or STAS: the
party size lives elsewhere (open question).

## Emulation notes
- Model `ntsc` (export header). Deterministic; RNG follows frame timing (the same walk always meets the same SWORM).
- **Savestates do not carry cartridge RAM** (backend issue, reported): every checkpoint loaded from the cache
  starts with blank (FF) cartridge RAM, while the same route replayed from power-on has the game's
  signature in it. Effects: (1) an in-game SAVE made after `goto` of a cached checkpoint writes only the slot,
  without the signature, so the exported `.sav` is formatted away on the next power-on and CONTINUE starts a
  new game; (2) the CONTINUE slot list after a cache hit and after a cold replay can differ. Frames of all
  checkpoints are identical cold and cached (checked). Workaround used for `01_start`: make the save in one
  `play.py start --route "TITLE,NEWGAME,..."` from power-on (no `@checkpoint`), then `export`.
- The title cursor blinks and never settles; the overworld and towns settle. The intro caption screen fades in
  (a teal frame at `PAGE*1` with `w240`): pick its frame by eye.
- Position pokes: in towns `C301`/`C305` move Alis on the next step (used for the EXIT gate); on the overworld
  the poke did not move her and left a half-drawn screen (4 variants tried, `t21`).
- After a poke the HUD box (name, HP, MP) keeps the old value until the game redraws it (STAS showed the new
  values at once).
- The PC printed by `play.py` is often `0055`/`0058`/`0059` (the idle loop); `bank=None` on this platform.

## Checkpoints
| Name | What |
|---|---|
| `title` | title screen (cursor on START) |
| `start` | first control in Camineet after the intro |
| `camineet` | Alis by the three shops; church to the south-east |
| `shop` | inside the second-hand shop, BUY/SELL prompt (MST 0) |
| `menu` | field menu open in Camineet |
| `palma` | overworld just outside Camineet (EXIT reached by a position poke) |
| `battle` | first battle, one SWORM (HP 8), command menu |
| `field_sw` | overworld south-west of Camineet, north of the wall |
| `field_s` | south of the wall, through its east gap |
| `cave_out` | beside the cave entrance south-west of Camineet |
| `dungeon` | inside that cave, lit with a FLASH: first-person corridor |
| `continue` | `sav:01_start` loaded through the title's CONTINUE |

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| US manual (OCR, Internet Archive "Phantasy_Star_1988_U") | https://archive.org/stream/Phantasy_Star_1988_U/Phantasy_Star_1988_U_djvu.txt | controls, menus, battle commands, spells, vehicles, planets, characters | 2026-11-19 |
| Wikipedia | https://en.wikipedia.org/wiki/Phantasy_Star_(video_game) | release dates, staff, versions, plot | 2026-11-19 |
| smstributes.co.uk (via a web-search snippet only; host not reachable) | https://smstributes.co.uk/getinfo.asp?gameid=264 | PAR codes `00C4 X1FF` infinite HP, `00C4 X2FF` infinite MP, X = character | 2026-11-19 |
| Genesis Plus GX game database (`tools/gpgx/core/cart_hw/sms_cart.c`) | local | Japanese CRCs only, no entry for this dump | 2026-11-19 |
| TCRF, GameFAQs (FAQs, cheats, saves), StrategyWiki, gamehacking.org | tcrf.net, gamefaqs.gamespot.com, strategywiki.org, gamehacking.org | refused automated access (HTTP 403): unavailable | 2026-11-19 |
| Data Crystal | datacrystal.tcrf.net | no Phantasy Star (SMS) page (404) | 2026-11-19 |
| SMS Power, TASVideos, libretro-db, archive.org download mirrors | | outside the allowed hosts (not resolvable) | 2026-11-19 |

## Open questions
- Exact revision against No-Intro (v1.2 vs v1.3 export): needs Dat-o-Matic or SMS Power.
- Overworld warp: which variable holds the overworld position/map (pokes of `C301`/`C305` did not take there).
- Party size / membership variable (to add Myau, Odin, Noah by poke).
- Title `down` did not move the cursor in one test (`up` did); check once more.
- The manual describes save-name registration (RUB/ADV/END, 5 letters); the US cartridge asked for none.
- Debug menu / sound test: TCRF unavailable here.
- Critical-path details (who gives the PASSPORT, how Myau joins) are from memory of the standard walkthrough, not
  from a fetched source: confirm in play.
