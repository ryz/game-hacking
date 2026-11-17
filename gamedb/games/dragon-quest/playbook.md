# Dragon Quest (Famicom, English translation patch) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

Scouted 2026-11-17 (first NES game in the database). **Read "Emulation notes" before making routes:** a
checkpoint loaded from the cache runs one frame more than the same checkpoint freshly built, and this game's
NPC movement and encounters follow the frame count.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Dragon Quest / ドラゴンクエスト (released in North America in 1989, reworked, as Dragon Warrior) |
| Platform / model used | Famicom, `ntsc`; mapper 3 (CNROM), 32 KiB PRG + 32 KiB CHR, no cartridge RAM (see `game.json`) |
| Release (region, year) | Japan, 27 May 1986 (source: Wikipedia) |
| Developer / publisher | Chunsoft / Enix (source: Wikipedia; title screen shows "(C)1986 ENIX", verified) |
| Genre | Role-playing game: one hero, top-down overworld/towns/caves, first-person turn-based battles one on one |
| Players / save system | 1 player. **No battery.** Progress is a 20-symbol password ("Return Spell") told by the king |
| ROM catalogued | the owner's Japanese dump with an English fan-translation IPS applied (`game.json` "source"). All text is English; names follow the Japanese game (Loto, Dragon King, Hoimi...), not Dragon Warrior |
| Variant `rom:jp` | the untouched Japanese ROM, rebuilt from the patched ROM by `rom/patches/dragon-quest/jp.ips` (made by the scout as the byte difference; SHA-1 of the result = `source.base_sha1`, verified). For kana comparison screens |

## Boot sequence
- Intake probe: `work/intake/dragon-quest/sheet.png`. Logo alone until about frame 700, then the title menu
  appears and stays (no attract mode within 2400 frames). The sword on the logo sparkles now and then, the
  screen still settles.
- `TITLE` = `w760,settle` (verified). Checkpoint `title` = `pow,w760,settle,settle`.
- Title menu (verified): Up/Down chooses START / CONTINUE, Left/Right sets MESSAGE SPEED (SLOW / NORMAL / FAST,
  default NORMAL), Start confirms. `FAST` = `right`.
- `NEWGAME` = `FAST,start,w60,settle,NAME_RYZ,KING_INTRO` (verified): name entry, then the king's speech
  (8 pages + closing the last one with B). Checkpoint `start` = `@title,NEWGAME`: ryz stands below the king at
  (3,4) in the throne room (map 5), LVL 1, HP 15, 0 G.
- `CONTINUE` = `FAST,down,start,w60,settle`: the password entry screen (checkpoint `password_entry`).
- `LATE` = `CONTINUE,PW_LATE,KING_RETURN`: enters the scout's password and fixes the name (see Shortcuts).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Up/Down, Left/Right | START/CONTINUE, message speed | verified |
| Title | Start | confirm the menu choice | verified (A not tried) |
| Field | D-pad | walk one tile per 16 frames held (`right:16`); walking over chests is allowed; NPCs block | verified |
| Field | A | open the Commands window | verified |
| Field | B, Start, Select | nothing seen | B verified (closes windows only); Start: no effect in the command window; Select not tried |
| Field | (stand still) | the status window (name, LVL, HP, MP, G, E) pops up by itself after about a second without input | verified |
| Commands window | D-pad, A, B | move (2 columns x 4 rows), choose, close | verified |
| Commands | Talk | opens a compass (N/W/E/S): press the direction of the person. The hero has no facing in this version | verified (king: `a,a,w20,up`) |
| Commands | Stats | status sheet: Lvl, Power, Speed, Max HP, Max MP, AtkPwr, DefPwr, Wpn, Armr, Shld | verified |
| Commands | Stairs | take the stairs the hero stands on (walking onto stairs does nothing) | verified (throne room (8,8) -> castle 1F) |
| Commands | Door | open a door next to the hero with a Key | command verified ("No doors here!"); opening a locked door not tried |
| Commands | Take | take the contents of the chest the hero stands on | verified (120 Gold at (4,4)) |
| Commands | Check | search the ground under the hero | source (not tried) |
| Commands | Spell / Items | lists (see Game structure) | windows verified, using one not tried |
| Dialogue | A (or B) | next page at the down arrow; closes the last page | verified |
| Battle | D-pad, A | Fight / Spell / Flee / Items (2 x 2) | verified (Fight wins vs Slimess) |
| Name / password entry | D-pad, A | move over the grid, type the symbol. `Del`/`Bck` = back one, `Frw` = forward, `End` = finish (name only: a 20-symbol password is checked as soon as the 20th symbol is typed) | verified (End, auto-accept); Del/Bck/Frw source |

Input timing: the default press (hold 8, wait 40) works everywhere tried (title, name grid, menus, dialogue,
battle). `down:16` inside a menu moved the cursor two entries (key repeat): use plain `down` in menus. The menu
cursor blinks, so a screenshot may show no cursor; that is not a missed press.

## Game structure
- **Flow:** title -> name entry (new game) or password (continue) -> throne room. There is no file select and no
  options screen besides the message speed on the title.
- **Maps** (RAM `0045`; ids as in the Dragon Warrior RAM map, the starred ones verified here): 1* overworld
  (120 x 120), 2* Dragon King's castle (Charlock) ground floor, 3 ruined town (Hauksness / Domdora), 4* Tantegel
  Castle, 5* throne room, 6 Dragon King's lair (bottom floor), 7 Kol (Maira), 8* first town (Brecconary /
  Radatome town), 9 Garinham (Garai), 0A Cantlin (Mercado), 0B Rimuldar, 0C sun shrine, 0D rain shrine,
  0E temple of the rainbow drop, 0F-14 Dragon King's castle B1-B6, 15 swamp cave, 16-17 mountain cave,
  18-1B Garin's grave, 1C-1D Loto's cave. The patch's own town names were not seen yet: use what the screen
  shows in captions.
- **Critical path** (source: common knowledge of the game, same in every version): throne room chests ->
  first town (equipment) -> Loto's cave (tablet) -> Garinham -> Kol (Fairy Flute by Check) -> swamp cave (green
  dragon, princess) -> Rimuldar (keys) -> Garin's grave (Silver Harp) -> rain shrine (Harp -> Staff of Rain) ->
  Cantlin (Golem at the gate; Fairy Flute puts it to sleep) -> Loto's Mark (Check in the swamp south of
  Cantlin) -> sun stones (Tantegel cellar) -> temple (Staff + Stones + Mark -> Rainbow Drop) -> rainbow bridge ->
  Dragon King's castle: hidden stairs behind the throne (Check), Loto's Sword on the way down, Dragon King
  (two forms) at the bottom -> return to the king -> ending.
- **Menus seen** (verified): field Commands = Talk, Spell / Stats, Items / Stairs, Check / Door, Take. Battle
  Commands = Fight, Spell / Flee, Items. Items window lists Herb n, Key n, then up to 8 items.
- **Names this patch uses** (verified on screen): Loto (Erdrick), Dragon King (Dragonlord), Light Orb, Return
  Spell (password), Slimess (red slime); spells Hoimi, Gira, Laliho, Remira, Mahot.., Riremi.., Lulra, Toher..,
  Behoi.., Begira.. (the spell window cuts long names); items Herb, Key, Drop (Rainbow Drop, with an icon),
  Love, Mark, Scale, Wing, Torch; equipment shown with an icon: Loto's (sword), Loto's (armour), Mirror (shield).
- **Death** (source): the hero wakes before the king with half his gold; there is no game-over screen.

## Shot plan
Target 40-45 shots; `shots.txt` has the plan lines (routes are filled in by the capture agent). Reach column:
S = from `@start` by play, L = from `@late` and its children, W = position warp (Shortcuts), P = pokes.
- boot/title/menu: `boot_logo` (logo alone, `pow,w300,!`), `title_screen` (@title), `name_entry` (ryz typed),
  `password_entry` (@password_entry), `password_typed` (20 symbols before the last press).
- cutscene/dialogue: `king_intro` (first page), `king_gifts` ("Take the gifts..."), `npc_talk` (compass open),
  `npc_soldier` (a soldier's hint), `king_password` (the king tells the Return Spell: save category).
- gameplay (S): `throne_room_start`, `throne_room_chest` (Take: 120 Gold), `throne_room_door` (Door with the
  key), `castle_1f`, `overworld_tantegel` (castle, town and the Dragon King's castle across the water in one
  frame: the game's famous first view).
- gameplay (L + W): `town_first`, `town_kol`, `town_rimuldar`, `town_cantlin`, `ruins_hauksness`,
  `cave_dark` (no torch: only the hero's tile lit), `cave_torch` (Torch), `cave_remira` (wider light),
  `swamp` (damage floor), `bridge`, `charlock_entrance`, `charlock_lair` (bottom floor, bright).
- system: `commands_window`, `stairs_command`, `door_command`, `check_command`, `spell_field` (Hoimi),
  `inn_stay`, `rainbow_bridge` (using the Rainbow Drop: a `seq-rainbow` sequence is worth it), `lura_return`.
- hud: `hud_status_popup` (status window after standing still).
- inventory: `stats_sheet`, `items_window`, `spell_window`.
- shop: `shop_weapons` (price list), `shop_tools`, `shop_keys`.
- battle: `battle_slime` (first enemy), `battle_command`, `battle_spell`, `battle_levelup`, `battle_late`
  (a strong enemy near Cantlin or in the castle).
- boss: `boss_golem`, `boss_green_dragon`, `boss_dragon_king_1`, `boss_dragon_king_2`, `dragon_king_offer`
  (the half-the-world question).
- gameover: `death_king` (the king's speech after dying; set HP to 1 in a battle).
- ending/credits: `ending_king`, `ending_credits` if the Dragon King falls within the session.
- extra: `jp_password_entry`, `jp_title` (`rom:jp`: the original kana screens, for comparison).

Special effort: the Dragon King (walk the castle floors with the stairs warp, then win: freeze HP `00C5`);
the princess (state flags, see RAM map, unverified bits); the rainbow bridge (needs the three relics or the
Drop in the right spot at about (65,49), source).

## Strategy and walkthrough notes
- Do not play the early game for progress: `@late` (level 21, best equipment, 6135 G) plus the position warp
  reaches every map in a few tokens. Play from `@start` only for the opening shots (chests, door, first battle).
- Level and stats are recomputed from E (experience) when a password loads and on level-up, not when E is
  poked. To change the level: poke E, talk to the king for a new password, enter it (how `LATE` was made).
- A battle that must be won: `freeze:00C5=95` (HP) hides nothing ugly if the value stays below Max HP; enemy HP
  is `00E2` (seen 04 for a Slimess; poke not tested).
- Caves are dark: Torch (item) or Remira; the light radius is `00D0` (source).
- Random encounters and wandering NPCs depend on frame timing: add `wN` variations, and make a checkpoint as
  soon as a wanted encounter is on screen.
- Message speed FAST is in all scout checkpoints except `title`.

## Naming
Main character: **ryz**. Name entry (verified): 4 symbols, grid of 10 columns:
`ABCDEFGHIJ / KLMNOPQRST / UVWXYZ a b / cdefghijkl / mnopqr s t / uvwxyz Del End`, cursor starts on A.
`NAME_RYZ` = `down*4,right*5,a,down,left,a,right,a,right*3,a,w60,settle` (r, y, z, End).
**Passwords lose the name:** the password keeps 6 bits per name symbol, so `ryz` comes back as `r56`
(verified). `NAME_FIX` = `poke:00B5=3B45465F` restores it (verified: status window, Stats, the king's farewell);
`KING_RETURN` includes it. Use it after every password.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Late-game state, name ryz | `@late` (= `@title,LATE`). Password `R[axe]5g5 M98**36 HbSaj R[axe]k` = `Ru5g5 M98**36 HbSaj Ruk` in `tools/pw.py` notation: LVL 21, HP 149, MP 122, 6135 G, E 34218, Loto's sword and armour, Mirror shield, Herb 4, Key 3, Drop, Love, Mark, Scale, Wing, Torch, all ten spells | made here: pokes at `@start` (`set:00BA=34218:2,set:00BC=6135:2,poke:00BE=FF,poke:00BF=03,poke:00C0=04,poke:00C1=8E471300,poke:00DF=08`), then Talk to the king | verified |
| Japanese-version passwords | They work unchanged: the patch keeps the kana grid cell for cell, only the glyphs differ. `python3 games/dragon-quest/tools/pw.py tokens "ふるいけや かわずとびこむ みずのおと ばしや"` gives the tokens to type one from `@password_entry`; `pw.py en KANA` / `pw.py jp EN` convert. The name comes out as patch-font symbols (here `4U[axe]J`): follow with `NAME_FIX` | the well-known "furuike ya" password | verified: LVL 10, HP 51, MP 40, 15143 G, E 2898 |
| Make any password | Poke the state at a point where the king talks normally (`00DF` bit 3 set = "has left the throne room"), Talk to him: after the experience line he says the Return Spell. Read it off the screen (zoom: the icons are symbols of the grid too) | scout | verified |
| Position warp | `poke:003A=XXYY,poke:008E=XXYY,poke:0090=<X*16 as 2 bytes low first><Y*16 the same>`, then walk one step: the game checks the tile it arrives on. Onto a town/cave tile of the overworld = enter it; off the edge of a town map = leave. The screen is wrong for that one step only | scout | verified: castle edge -> overworld; (47,41)+right -> first town; (47,48)+right -> Dragon King's castle |
| Overworld coordinates | Tantegel (43,43) verified, first town (48,41) verified, Dragon King's castle (48,48) verified. Others from Dragon Warrior (source, check each): Garinham (2,2), Kol (104,10), Rimuldar (102,72), Cantlin (73,102), Hauksness (25,89), swamp cave (104,44)/(104,49), mountain cave (29,57), Loto's cave (28,12), rain shrine (81,1), sun shrine via Tantegel cellar, rainbow temple (108,109) | Dragon Warrior maps, from memory | source |
| Stairs warp inside a map | The same poke onto a stairs tile, then Commands > Stairs | scout idea | not tried |
| Hold values | `freeze:00C5=HH` (HP), `freeze:00C6=HH` (MP) | RAM map | addresses verified by watch, freeze not tried |
| Game Genie | none found for the Japanese ROM; Dragon Warrior (U) codes address another PRG layout and will not apply | gamehacking.org not reachable from here (not tried further) | none found |
| Debug menu / level select | none known for this game | TCRF page returned 403 | none found |

### Saves (rom/saves/dragon-quest/, never committed)
None: the cartridge has no battery, `play.py export` does not apply. Passwords above are the saves; for the
owner, the `late` password typed on the patched ROM's CONTINUE screen gives the state by hand (name r56).

## RAM map (for `game.json` "ram" watches and pokes)
Zero page. The layout matches the Dragon Warrior (U) RAM map on Data Crystal wherever checked.
| Address | Size | Meaning | How found |
|---|---|---|---|
| `003A`, `003B` | 1+1 | hero X, Y on the current map (tiles) | verified (watch while walking) |
| `008E`, `008F` | 1+1 | second copy of X, Y | verified (must be poked too for a warp) |
| `0090`-`0093` | 2+2 | X*16, Y*16 (low byte first) | verified (same) |
| `0045` | 1 | map id (list in Game structure) | verified: 1, 2, 4, 5, 8 |
| `00B5`-`00B8` | 4 | hero name, font codes (`3B 45 46 5F` = "ryz ") | verified (poke) |
| `00BA` | 2 | E, experience (low byte first) | verified (`set:` + status window) |
| `00BC` | 2 | G, gold | verified (`set:` + status window) |
| `00BE` | 1 | equipment: bits 7-5 weapon, 4-2 armour, 1-0 shield; `FF` = Loto's sword, Loto's armour, Mirror shield | `FF` verified; other values source |
| `00BF`, `00C0` | 1+1 | Keys, Herbs | verified (3, 4 in the Items window) |
| `00C1`-`00C4` | 4 | 8 item slots, one per half byte, low half first: 1 Torch, 2 fairy water, 3 Wing, 4 Scale, 5 fairy flute, 6 fighter's ring, 7 Mark, 8 Love, 9 cursed belt, A silver harp, B death necklace, C sun stones, D staff of rain, E Drop | 1, 3, 4, 7, 8, E verified; rest source |
| `00C5`, `00C6` | 1+1 | HP, MP | verified (watch) |
| `00C7` | 1 | level (derived from E on password load / level-up) | verified (watch) |
| `00C8`-`00CD` | 6 | Power, Speed, Max HP, Max MP, AtkPwr, DefPwr | verified against the Stats sheet (95, 82, 149, 122, 135, 91) |
| `00CE` | 1 | spells 1-8 learned, one bit each | `FF` at level 21 seen; bits source |
| `00CF` | 1 | bits 0-1 spells 9-10; bit 2 hidden stairs found, 3 rainbow bridge built, 4 Scale worn, 5 ring worn, 6 belt, 7 necklace | `13` at `late`; bits source |
| `00D0` | 1 | light radius in caves (1, 3, 5, 7) | source |
| `00DF` | 1 | bit 0 carrying the princess, 1 princess returned, 2 death necklace found, 3 has left the throne room | bit 3 verified (king's dialogue changes); `0E` after the `late` password; rest source |
| `00E0` | 1 | enemy id in battle | seen 01 for Slimess; source |
| `00E2` | 1 | enemy HP | seen 04; source |
| `00E4` | 1 | bit 1 Golem dead, 2 Dragon King dead, 6 green dragon dead | source |

## Emulation notes
- Model `ntsc`. Colours and input fine; no crash, no hang seen. `status` PC is always `c77f` (the game's
  wait-for-frame loop), so the PC does not help to detect hangs here.
- **Backend bug (reported to the coordinator, open): a checkpoint loaded from `work/cache/` is one frame ahead
  of the same checkpoint when it has just been built.** `tools/lrcore.py` `Core.image()` runs one frame when no
  frame has been drawn yet, which is the case right after a savestate is loaded into a new core, and right after
  power-on when `emu.py` takes its `00_start` picture. Measured: `@start,w10` on a cache hit equals `@start,w9`
  when built. In this game NPC steps and encounters follow the frame count, so the same route gives different
  guard positions, and an encounter can come a step earlier or later, depending on whether the cache existed.
  Fixed parts of a screen (hero, map, windows, numbers) are the same. Until it is fixed: do not rely on
  `--verify` for shots with wandering NPCs or random encounters, and take such shots a short route after a
  checkpoint made at the moment itself.
- `late_battle` depends on that: both variants reach the Slimess battle (checked), on different steps.
- After a map change the first settled frame can be black (`w60` was not enough for the town entry): use `w90`.
- The status window appears on its own when idle; `settle` waits long enough for it most of the time. A shot
  without it needs `!` right after the last step.
- Guards and townspeople wander: screens with NPCs still settle between their steps.

## Checkpoints
`title`, `password_entry`, `start` (new game, first control), `late` (password state in the throne room),
`late_castle` (Tantegel 1F), `late_overworld` (south of Tantegel), `late_brecconary` (first town),
`late_charlock` (Dragon King's castle entrance), `late_battle` (Slimess). All nine rebuilt from power-on with
an empty cache on 2026-11-17 and looked at (`work/scout/dragon-quest/checkpoints_build_vs_hit.png`: top row
built, bottom row loaded from the cache).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Data Crystal, Dragon Warrior RAM map | https://datacrystal.tcrf.net/wiki/Dragon_Warrior/RAM_map | RAM layout, item codes, map ids, flag bits (for the US version; checked here where marked) | 2026-11-17 |
| Wikipedia, Dragon Quest (video game) | https://en.wikipedia.org/wiki/Dragon_Quest_(video_game) | release date, staff, differences to Dragon Warrior | 2026-11-17 |
| Dragon Quest Wiki, Spell of Restoration | https://dragon-quest.org/wiki/Spell_of_Restoration | password is 20 kana in a 5-7-5-3 pattern (search result summary only; host not on the allowed list) | 2026-11-17 |
| TCRF, Dragon Quest (NES) | https://tcrf.net/Dragon_Quest_(NES) | unavailable (HTTP 403) | 2026-11-17 |
| StrategyWiki, Dragon Warrior | https://strategywiki.org/wiki/Dragon_Warrior/Walkthrough | unavailable (HTTP 403) | 2026-11-17 |
| GameFAQs | - | not fetched (time; 403 in the earlier scout) | - |
| The ROM itself | `rom/dragon-quest.nes` vs `rom/src/dragon-quest-j.nes` | the patch changes text in PRG 0000-0FFF, 5 bytes at 6xxx and the CHR font; the password code is untouched | 2026-11-17 |

The critical path, overworld coordinates and the level table are written from the scout's memory of the game
and are tagged source: nothing was fetched for them.

## Open questions
- Flag bits in `00CF`, `00DF`, `00E4` in this ROM (Golem, green dragon, princess, bridge): which does a password
  keep? The `late` password shows the princess in the throne room (Love in the inventory).
- Does the stairs warp work, and what are the stairs coordinates down the Dragon King's castle?
- Overworld coordinates of every place other than the three verified.
- Opening a locked door (Door + Key), Check, shops and inns: not tried.
- Start/Select in the field; A on the title menu.
- The patch's names for towns, the king and the princess; whether any text is left in Japanese.
- Experience table (seen: level 11 at 2900; 34218 gives level 21).
