# Status - game database

Current snapshot of the shared tooling and the games (rewritten as a snapshot 2026-11-20). History, newest first:
[progress-log.md](progress-log.md). Tool work that is wished for or planned: [backlog.md](backlog.md). The notes
this file accumulated from 2026-11-15 to 2026-11-20: [archive/status-2026-11-20.md](archive/status-2026-11-20.md).

Keep this file short: one line per platform and tool, the generated game table, what is next. A finished run
changes `game.json` ("work", "open") in its game folder and one line in the progress log, not this file.

## Platforms
Each session builds only the emulator it needs (`sh tools/setup_emu.sh PLATFORM`; no setup script, decided
2026-11-18). All backends: deterministic, exact savestates, peek/poke/RAM search, battery or file saves through
`play.py export` and `sav:`. RAM watches and `set:` follow the CPU's byte order (backend attribute `ENDIAN`).

| Platform | Backend (pinned commit) | Build | A game is | Not supported or untested | Notes |
|---|---|---|---|---|---|
| `gb`, `gbc` | gbemu-cli (headless SameBoy) | 9 s | `.gb` / `.gbc` | `--model sgb` hangs on the SGB transfer screen (capture in dmg) | [gb.md](emulator/gb.md) |
| `nes` | Mesen libretro core | 57 s | `.nes` (NES and Famicom) | Famicom Disk System, second controller, 6-letter Game Genie codes on bank-switched games | [nes.md](emulator/nes.md) |
| `snes` | Mesen-S libretro core | 53 s | `.sfc` / `.smc` | special-chip games untested | [snes.md](emulator/snes.md) |
| `sms` | Genesis Plus GX libretro core | 11 s | `.sms` | Game Gear, SG-1000, light gun, paddle, Reset button, Sega Card | [sms.md](emulator/sms.md) |
| `md` | Genesis Plus GX libretro core (the `sms` build) | 11 s | `.md` / `.gen` / `.bin` (Mega Drive and Genesis) | Mega-CD, 32X, lock-on, second pad, mouse, light guns, `.smd` dumps; no game registered yet (backend 2026-11-20) | [md.md](emulator/md.md) |
| `dos` | DOSBox Pure libretro core | 32 s | a ZIP of the game's files | CD images and installers, mouse tokens, sound card choice; `cga`/`tandy` lose the palette on a state load (use `ega`) | [dos.md](emulator/dos.md) |
| `apple2` | AppleWin libretro core (needs cmake) | 78 s | a disk image or a ZIP of disk images | reset keys, hard disk images with a real game, held keys / auto-repeat | [apple2.md](emulator/apple2.md) |
| `amiga` | PUAE libretro core | 90 s | an ADF or a ZIP of ADFs; Kickstart ROMs in `rom/kickstart/` | `.ipf`, hard disk / WHDLoad, CD32 / CDTV, write-protected disks | [amiga.md](emulator/amiga.md) |

## Tools
| Tool | State |
|---|---|
| `intake.py`, `patch.py` | register a ROM (header, hashes, boot probe), owner's patches applied in order (IPS, BPS, UPS) |
| `emu.py` | tokens, macros with arguments, checkpoints; a checkpoint chain is built once, each link cached, under a lock (2026-11-20) |
| `play.py` | persistent session for exploring: do / undo / snap / checkpoint / goto / find / dump / diff / sample / record / export / text; native pictures, `call=N` in every status line (2026-11-20) |
| `preview.py` | candidate routes or a plan file in parallel on one sheet, played as `shoot.py` plays them; `?` marks, `--timeline`, `--text`, `--peek`, `--set` (2026-11-20; replaces ten per-game `try.py` copies) |
| `shoot.py` | replay, `--verify`, `--publish[-only]`, `--only`, `--prune`; `--jobs N` (default 4); identical pictures reported by `--only` and by `snap`; the set's own `shots.txt` gives the order (2026-11-20) |
| `cachecheck.py` | every checkpoint: flat replay vs chained build vs cache hit vs the existing cache, with a sheet (2026-11-20; replaces five per-game copies) |
| `lenses.py` | which shots the three lens documents use, rows without a shot |
| `x3.py` | enlarged copies on demand; sets hold native pictures only (owner's rule 2026-11-20) |
| `gamestable.py` | writes the game tables below and in `README.md` from each `game.json` |
| `dis6502.py` | 6502 disassembler for NES games |

Tests: `python3 -m pytest -q tests` (62, on generated test ROMs and disks for all eight platforms; a platform's
tests are skipped when its emulator is not built).

**Published sets re-verified with the 2026-11-20 tools** (chained checkpoint builds, parallel replays), each
from an empty cache against the committed pictures (`shoot.py SLUG SET --verify --published`):

| Set | Result | Cold verify |
|---|---|---|
| `dos/wizardry-3` main | 228/228 (2026-11-20) | 64 s with 4 processes, 201 s with 1 (the capture run reported about 15 minutes with the old tools) |
| `snes/shin-megami-tensei` main | 56/56 (2026-11-20) | 428 s with 4 processes: 41 checkpoints in one line (depth 37), so the chain is built by one process while the others wait; no cold figure from the old tools to compare with |

Still to do as dumps arrive: `apple2/wizardry` (main, start), `amiga/dungeon-master` (main, start),
`nes/megami-tensei-2`; optional `gb/pokemon-blue`, `sms/phantasy-star`. The Apple II
and Amiga sets need their uncommitted save disks rebuilt first (routes in each `saves/README.md`).

## Games
Generated by `python3 tools/gamestable.py` from each game's `game.json` ("work", "open"), its published sets and
its lens documents. Do not edit between the markers.

<!-- games:begin -->
| Game | Folder | Sets (shots) | Three lenses | Open |
|---|---|---|---|---|
| Wizardry Empire | `games/gbc/wizardry-empire/` | own tools | - | see games/gbc/wizardry-empire/translation/docs/status.md |
| Pokémon Blue Version | `games/gb/pokemon-blue/` | [main](../games/gb/pokemon-blue/shots/main/index.md) 92, [seq-fishing](../games/gb/pokemon-blue/shots/seq-fishing/index.md) 15, [seq-fly](../games/gb/pokemon-blue/shots/seq-fly/index.md) 9 | no | trainer "!" spotting, a PC box with Pokémon, Safari BAIT, stone evolution, Rocket Hideout; the MID recipe has never been shown on screen; model sgb hangs on the transfer screen (capture in dmg) |
| Deep Dungeon III: Yuushi e no Tabi | `games/nes/deep-dungeon-3/` | [main](../games/nes/deep-dungeon-3/shots/main/index.md) 74 | no | castle master, other towns' item shops/temples, lit cave |
| Dragon Quest (Famicom, English translation patch) | `games/nes/dragon-quest/` | [main](../games/nes/dragon-quest/shots/main/index.md) 67 | no | shop_keys, swamp, bridge, check_command, a rainbow-bridge clip set, the middle floors of the Dragon King's castle, a retake of commands_window (cursor blinked off) |
| Dungeon Magic: Sword of the Elements (NES, USA) | `games/nes/dungeon-magic/` | [main](../games/nes/dungeon-magic/shots/main/index.md) 41 | no | the King, camp, swords, bosses beaten, Darces, ending |
| Digital Devil Story: Megami Tensei (Famicom, English translation patch) | `games/nes/megami-tensei/` | [main](../games/nes/megami-tensei/shots/main/index.md) 88 | no | other sections' wall graphics after a warp, stairs prompt shot |
| Digital Devil Monogatari: Megami Tensei II (Famicom, English translation patch) | `games/nes/megami-tensei-2/` | [main](../games/nes/megami-tensei-2/shots/main/index.md) 67 | no | a CHAT join, automap, Nebro and later bosses, first-person maze maps |
| Might and Magic: Secret of the Inner Sanctum | `games/nes/might-and-magic/` | [main](../games/nes/might-and-magic/shots/main/index.md) 93 | no | services in the other towns, spells above level 1, Bribe/Giveup |
| Wizardry: Proving Grounds of the Mad Overlord (NES, USA) | `games/nes/wizardry/` | [main](../games/nes/wizardry/shots/main/index.md) 71, [compare-maze](../games/nes/wizardry/shots/compare-maze/index.md) 9 | no | Identify, spinner, teleport square; party_dead retake |
| Wizardry: Knight of Diamonds - The Second Scenario (NES, USA) | `games/nes/wizardry-2/` | [main](../games/nes/wizardry-2/shots/main/index.md) 91, [compare-maze](../games/nes/wizardry-2/shots/compare-maze/index.md) 11 | no | Sell/Identify, darkness, spinner, level drain, floor 4 room fight |
| Shin Megami Tensei (Super Famicom, English translation patch) | `games/snes/shin-megami-tensei/` | [main](../games/snes/shin-megami-tensei/shots/main/index.md) 56 | no | no demon has joined (negotiation needs a Bead; item list not found in RAM), so no summoning, fusion or terminals; the second dream needs a flag poke (real trigger unknown) |
| Phantasy Star | `games/sms/phantasy-star/` | [main](../games/sms/phantasy-star/shots/main/index.md) 109, [battles](../games/sms/phantasy-star/shots/battles/index.md) 18, [loops](../games/sms/phantasy-star/shots/loops/index.md) 4, [seq-dungeon-door](../games/sms/phantasy-star/shots/seq-dungeon-door/index.md) 4, [seq-dungeon-stairs](../games/sms/phantasy-star/shots/seq-dungeon-stairs/index.md) 4, [seq-dungeon-turn](../games/sms/phantasy-star/shots/seq-dungeon-turn/index.md) 6, [seq-dungeon-walk](../games/sms/phantasy-star/shots/seq-dungeon-walk/index.md) 6 | yes | the ending (Dark Falz trigger, likely floor 3B/3C squares coded 7), Noah joining, Odin's cure, vehicles in use, RUN/DRP, spells cast, a trap, milestone saves, battle retakes in the real boss rooms |
| Sword of Vermilion | `games/md/sword-of-vermilion/` | [main](../games/md/sword-of-vermilion/shots/main/index.md) 136, [seq-aries](../games/md/sword-of-vermilion/shots/seq-aries/index.md) 7, [seq-boss](../games/md/sword-of-vermilion/shots/seq-boss/index.md) 14, [seq-ending](../games/md/sword-of-vermilion/shots/seq-ending/index.md) 12, [start](../games/md/sword-of-vermilion/shots/start/index.md) 35 | yes | the bosses' real cave squares and the ring quest played on foot (bosses and ending are poked); rings after Wisdom; Watling, Barrow, Tadcaster, Swaffham and Hastings not shot; Malaga talk; message-speed option; Sangua and other spells cast; a church save after Parma |
| Might and Magic Book One: The Secret of the Inner Sanctum (DOS) | `games/dos/might-and-magic/` | [main](../games/dos/might-and-magic/shots/main/index.md) 249 | yes | surprise message, search find, rest interrupted, surrender accepted, impostor, Eye of Goros, Astral door, wall sets decoded from WALLPIX.DTA, Fire Ball hitting the party (unexplained) |
| Might and Magic II: Gates to Another World (DOS) | `games/dos/might-and-magic-2/` | [main](../games/dos/might-and-magic-2/shots/main/index.md) 228 | yes | hireling hire, Cartographer automap, elemental shrines and lords, bashing a locked door, time travel by the game's own means (YEAR poke used), temple cure and spell purchase transactions |
| Ultima I: The First Age of Darkness (DOS) | `games/dos/ultima/` | [main](../games/dos/ultima/shots/main/index.md) 195 | yes | starbase docking and ship choice, pub seduction, bard/jester songs, Steal spell |
| Ultima II: The Revenge of the Enchantress (DOS) | `games/dos/ultima-2/` | [main](../games/dos/ultima-2/shots/main/index.md) 226 | yes | Up ladder and Blink spells, fleeing, natural-kill loot |
| Ultima III: Exodus (DOS) | `games/dos/ultima-3/` | [main](../games/dos/ultima-3/shots/main/index.md) 260 | yes | Surmandum failing into ashes, lava damage without the Mark of Fire, starvation and poison per turn |
| Wizardry: Proving Grounds of the Mad Overlord (DOS) | `games/dos/wizardry/` | [main](../games/dos/wizardry/shots/main/index.md) 208 | yes | Murphy's ghost and the keys (floor 1 statues never offer a search), spinner, criticals, stoning, body recovery |
| Wizardry II: The Knight of Diamonds (DOS) | `games/dos/wizardry-2/` | [main](../games/dos/wizardry-2/shots/main/index.md) 212 | yes | floor 2 (16,3) room (doors open outward only), floor 6 fixed fight, spinners, stones |
| Wizardry III: Legacy of Llylgamyn (DOS) | `games/dos/wizardry-3/` | [main](../games/dos/wizardry-3/shots/main/index.md) 228 | yes | Abdul's sale and coffer (floor 5), floor 6 dragon room fight |
| Might and Magic Book One: The Secret of the Inner Sanctum | `games/apple2/might-and-magic/` | [main](../games/apple2/might-and-magic/shots/main/index.md) 308 | yes | not scouted as a game of its own (the DOS routes were carried over); disk side 4 not reached |
| Might and Magic II: Gates to Another World | `games/apple2/might-and-magic-2/` | none | no | year/century variable not found (no YEAR macro, so King Kalohn in year 800 is untested); Sheltem fight not won (monster HP poke at 0283 had no visible effect); record bytes for quest marks, items' charges and skills not decoded |
| Wizardry: Proving Grounds of the Mad Overlord | `games/apple2/wizardry/` | [main](../games/apple2/wizardry/shots/main/index.md) 304, [start](../games/apple2/wizardry/shots/start/index.md) 47 | yes | see the playbook, "Not captured" |
| Wizardry II: The Knight of Diamonds | `games/apple2/wizardry-2/` | [main](../games/apple2/wizardry-2/shots/main/index.md) 229, [start](../games/apple2/wizardry-2/shots/start/index.md) 35 | yes | not shown: R)un, Q)uick, S)tatus, Dispell's effect, the staff in use, paying a fee (the well's Y returned to the Castle), floor 4 random groups, floor 6 fixed fights (High Priest) |
| Wizardry III: Legacy of Llylgamyn | `games/apple2/wizardry-3/` | none | no | not scouted: next step game-scout with rom/saves/apple2/wizardry-3/00_transfer.sav (rebuilt by wizardry-2's tools/transfer.py) |
| Wizardry IV: The Return of Werdna | `games/apple2/wizardry-4/` | none | no | not scouted |
| Wizardry V: Heart of the Maelstrom | `games/apple2/wizardry-5/` | none | no | not scouted |
| Dungeon Master | `games/amiga/dungeon-master/` | [main](../games/amiga/dungeon-master/shots/main/index.md) 111, [start](../games/amiga/dungeon-master/shots/start/index.md) 37 | yes | a teleporter, pressure plate, chest, scroll, three creature kinds, Gando's mirror, a few actions (KICK, WAR CRY, CALM, INVOKE) |
<!-- games:end -->

## Container notes
- Dumps, patches, downloaded saves, Kickstart ROMs and transfer disks exist only in the container that received
  them. A new container needs the owner's uploads again; the Apple II Wizardry transfer disks are rebuilt from
  the `final` checkpoints with each game's `tools/transfer.py`.
- Research hosts allowed by the environment: GameFAQs, TCRF, Data Crystal, StrategyWiki, Wikipedia,
  gamehacking.org, Kodewerx, archive.org. GameFAQs, TCRF and StrategyWiki answer automated requests with 403:
  agents note them as unavailable and do not work around it.

## Next
- Queue (halted by the owner 2026-11-19): Wizardry II (Apple II) capture; Wizardry III, IV, V (Apple II) scouts.
- Re-verify published sets with the new tools as dumps become available (above).
- Playbooks written before 2026-11-20 have no "Read first" block: the next run on a game writes it
  (`skills/game-capture/skill.md`, step 8).
- Twelve `maps.py`, four `roster.py` and four `transfer.py` still live per game; the Wizardry ones on one
  engine are candidates for a shared module (`backlog.md`). Not touched without the dumps to test against.
- Might and Magic 1 exists on NES, DOS and Apple II: a comparison of the three versions is possible from the sets.
- A database export step once the target schema is known.
