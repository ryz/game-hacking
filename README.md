# game-hacking

A game database built by taking games apart: for each game, reproducible screenshot sets, a design reference of
how it works, a playbook for automated play and, where there is one, a fan translation with its patch tools and
reverse-engineering notes. No game data is included: everything runs from your own dump, verified by checksum.

## Games

<!-- games:begin -->
| Game | Platform | What is here |
|---|---|---|
| [Wizardry Empire](games/gbc/wizardry-empire/README.md) | Game Boy Color | English translation (`translation/`: script, VWF engine, build chain, RE notes), design docs, tech docs, floor maps, reference screenshots |
| [Pokémon Blue Version](games/gb/pokemon-blue/playbook.md) | Game Boy | screenshot sets and sequences, design reference, saves |
| [Deep Dungeon III: Yuushi e no Tabi](games/nes/deep-dungeon-3/playbook.md) | Famicom (Japanese) | screenshot set (74, to the ending), 16 floor maps + towns, design reference, saves |
| [Dragon Quest (Famicom, English translation patch)](games/nes/dragon-quest/playbook.md) | Famicom (English translation patch) | screenshot set, design reference, password tools |
| [Dungeon Magic: Sword of the Elements (NES, USA)](games/nes/dungeon-magic/playbook.md) | NES | screenshot set (41), floor maps of all 39 floors + overworld, design reference, saves |
| [Digital Devil Story: Megami Tensei (Famicom, English translation patch)](games/nes/megami-tensei/playbook.md) | Famicom (English translation patch) | screenshot set (88, to the ending), 35 floor maps, design reference, passwords |
| [Digital Devil Monogatari: Megami Tensei II (Famicom, English translation patch)](games/nes/megami-tensei-2/playbook.md) | Famicom (English translation patch) | screenshot set (67), overhead maps, design reference, saves |
| [Might and Magic: Secret of the Inner Sanctum](games/nes/might-and-magic/playbook.md) | NES | screenshot set (93, to the ending), 55 area maps with terrain and exits, design reference, saves |
| [Wizardry: Proving Grounds of the Mad Overlord (NES, USA)](games/nes/wizardry/playbook.md) | NES | screenshot set (71, to the ending), 10 floor maps with special squares, design reference, saves |
| [Wizardry: Knight of Diamonds - The Second Scenario (NES, USA)](games/nes/wizardry-2/playbook.md) | NES | screenshot set (91, to the ending), 6 floor maps, design reference, roster tool, saves |
| [Shin Megami Tensei (Super Famicom, English translation patch)](games/snes/shin-megami-tensei/playbook.md) | Super Famicom (English translation patches) | screenshot set, design reference, saves |
| [Phantasy Star](games/sms/phantasy-star/playbook.md) | Master System (US/EU release, v1.2 header) | screenshot set (109, all three planets and most bosses; ending not reached), battles set (12), four dungeon sequences, three lens documents, warp/dungeon/fight/party macros, ROM table tools, save |
| [Sword of Vermilion](games/md/sword-of-vermilion/playbook.md) | md | sets main (136), start (35, to the first save), seq-aries (7), seq-boss (14) and seq-ending (12) published and verified 2026-11-20; three lenses; 56 checkpoints to Parma, the Ring of Wisdom, two caves and seven later towns by Aries; outdoor talk shots in 7 towns; overworld encounters with the full area map; all 14 bosses and the ending reached by poke; RAM and code map; townspeople/talk planner tools/npcs.py; save 01_start |
| [Beyond Zork: The Coconut of Quendor (DOS)](games/dos/beyond-zork/playbook.md) | DOS, Release 57 / 871221, Infocom's own interpreter BZORK.EXE (Frotz 2.32 in the bundle for comparison) | sets main 100 and start 34 (verified, published 2026-11-21; Bzork.exe in palette 6, black on light grey, set at boot; 640x200 row-doubled to 640x400): menus, character creation, all six palettes and monochrome, village, cellar, moors, Mizniaport shop, two deaths, 13 Frotz 2.32 comparison shots; three lenses clean |
| [Might and Magic Book One: The Secret of the Inner Sanctum (DOS)](games/dos/might-and-magic/playbook.md) | DOS (GOG release) | screenshot set (249, to the ending text: every command, 45 monster groups, all looks), three lens documents (systems, interface, content), area warp and survey of all 55 areas, saves |
| [Might and Magic II: Gates to Another World (DOS)](games/dos/might-and-magic-2/playbook.md) | DOS (GOG release, boots via `loadfix -4`) | screenshot sets main (228, to the Congratulations ending: Kalohn, Sheltem, override code, cryptogram) and start (52, honest new party from power-on to the first sign-in, lost orc fight included), three lens documents, warp to all 60 areas and centuries, event lister, saves |
| [Ultima I: The First Age of Darkness (DOS)](games/dos/ultima/playbook.md) | DOS (GOG, five programs) | screenshot set (195, to the ending text: creation, towns, castles, landmarks, dungeons 1-10, space, Mondain), three lens documents, warp to 84 places, shop tool, saves |
| [Ultima II: The Revenge of the Enchantress (DOS)](games/dos/ultima-2/playbook.md) | DOS (GOG) | screenshot set (226, to the ending text: five periods, planets, quest chain, honest Minax fight), three lens documents, period warp, map/town/shop/monster tools, saves |
| [Ultima III: Exodus (DOS)](games/dos/ultima-3/playbook.md) | DOS (GOG) | screenshot set (260, to the ending text: party of four, nine combat fields, Ambrosia, moongates, dungeon rods, Time Lord, Exodus), three lens documents plus rules.md, warps, town/dungeon/RNG tools, saves |
| [Wizardry: Proving Grounds of the Mad Overlord (DOS)](games/dos/wizardry/playbook.md) | DOS (1984 booter via the 1998 loader, disk images) | screenshot set (208, to the ending: Werdna beaten on screen), three lens documents, ten floor maps from the disk, items with prices, floor warp, saves incl. the Wizardry II transfer source |
| [Wizardry II: The Knight of Diamonds (DOS)](games/dos/wizardry-2/playbook.md) | DOS (same loader) | screenshot set (212, to the ending: Wizardry I party imported in the game, five guardians, Staff of Gnilda, knights), three lens documents, six floor maps, items, floor warp, saves incl. the Wizardry III transfer source |
| [Wizardry III: Legacy of Llylgamyn (DOS)](games/dos/wizardry-3/playbook.md) | DOS (same loader) | screenshot set (228, to the ending: Wizardry II party legated, both halves and guardians, Neutral Crystal made in play, orb, stars), three lens documents, six floor maps, all messages, items, floor warp, saves |
| [The Bard's Tale: Tales of the Unknown](games/apple2/bards-tale/playbook.md) | apple2 | captured 2026-11-21: main 132 shots (city, every service, all 16 dungeon levels lit, 25 monster groups, spells, Mangar, game over, ending), start 45 (honest new party to the first save), 16 decoded level maps, three lenses |
| [The Bard's Tale III: Thief of Fate](games/apple2/bards-tale-3/playbook.md) | apple2 | captured 2026-11-21: main 110 shots (camp, ruins and services, 16 lit dungeon levels on both sides, cities, automap partial and full, fights, the endgame at Tarjan), start 54 shots (honest RYZ party to the first save), sequences seq-dungeon-walk 29 and seq-automap 18 steps (UnterBrae 2), 58 decoded level maps, three lenses |
| [Might and Magic Book One: The Secret of the Inner Sanctum](games/apple2/might-and-magic/playbook.md) | Apple II (four disk sides, cracked side 1) | registered 2026-11-18; plays from power-on through disk changes into Sorpigal and the wilderness, inn save; screenshot set (308, to the ending: the DOS set's routes replayed plus every area once and the disk prompts), three lens documents over the DOS detail documents, area warp, macros, checkpoints |
| [Might and Magic II: Gates to Another World](games/apple2/might-and-magic-2/playbook.md) | apple2 | captured 2026-11-20: main 220 shots (boot to Sheltem's fight, all towns, outdoors, caverns, dungeons, castles, year 800), start 45 shots (power-on to the first save), automap (walked and filled: Middlegate, C2, cavern), three lens documents; century byte found |
| [Wizardry: Proving Grounds of the Mad Overlord](games/apple2/wizardry/playbook.md) | Apple II (1981 original, boot + scenario disk, model `iiplus-wp1`) | screenshot set (304, to the ending: Werdna beaten in play, every castle service, creation, about 40 monster groups, plain maze views), `start` set (47, the early game played honestly to the first save), three lens documents, ten floor maps and data tools, floor warp, 26 checkpoints |
| [Wizardry II: The Knight of Diamonds](games/apple2/wizardry-2/playbook.md) | Apple II (1982, two disks) | captured 2026-11-20: main 229 shots (utilities, transfer, castle and services, all six floors, 14 encounters, five guardians, quest, ending, cemetery), start 35 shots (transfer to the party formed), three lens documents |
| [Wizardry III: Legacy of Llylgamyn](games/apple2/wizardry-3/playbook.md) | Apple II (2 disk sides) | registered 2026-11-19 (boots to the title); not scouted |
| [Wizardry IV: The Return of Werdna](games/apple2/wizardry-4/playbook.md) | Apple II (6 disk sides) | registered 2026-11-19 (boots to the title); not scouted |
| [Wizardry V: Heart of the Maelstrom](games/apple2/wizardry-5/playbook.md) | Apple II (9 disk sides) | registered 2026-11-19 (boots to the title); not scouted |
| [Dragonflight](games/amiga/dragonflight/playbook.md) | Amiga (English, CLS crack, A500 with Kickstart 1.3) | start set (24 shots) and main set (93) published 2026-11-22: boot, menus, intro, Pegana, land, camp, status/inventory, talk, combat (13 opponent kinds, orders, hit, deaths, game over), magic (Light succeeds in a dungeon, Magic arrow in a fight), ten potions drunk, the Great Map, a first-person dungeon (torch, doors), two temples, Drombul, Orc Village, save/load; three lenses |
| [Dungeon Master](games/amiga/dungeon-master/playbook.md) | Amiga (v3.60, cracked ADF, A500 with Kickstart 1.3) | screenshot set (111, to the ending: all 14 levels, 22 creature kinds, Lord Chaos fused, the Grey Lord), `start` set (37, played honestly to the first save), three lens documents, maps of all 14 levels, level warp, pointer macros, saves |
| [Phantasie](games/c64/phantasie/playbook.md) | c64 | captured 2026-11-21: main set 77 shots (town, guild, wilderness, dungeon 1, three fights), start set 39 shots (power-on to the first save), three lenses, 21 checkpoints, BASIC-variable RAM map with a position warp |
| [Wasteland](games/c64/wasteland/playbook.md) | c64 | captured 2026-11-22: start set (49 shots, power-on to the first save in Highpool, honest) and main set (62: title, Ranger Center, creation, world map, field commands, Highpool shop/infirmary/workshop, Agricultural Center, combat to result); lenses written; world map decoded in RAM |
<!-- games:end -->

This table is written by `python3 tools/gamestable.py` from each game's `game.json`; sets, lens documents and
open items per game: [docs/status.md](docs/status.md).

Platforms: Game Boy / Game Boy Color, NES / Famicom, SNES / Super Famicom, Master System / Mark III and Mega Drive / Genesis cartridges, DOS games (a ZIP of the
game's files), Apple II disks and Amiga floppies. Another system is one backend class in
`tools/platforms.py`. Current state of the tooling: [docs/status.md](docs/status.md).

## Layout

| Path | What |
|---|---|
| `games/<platform>/<slug>/` | Everything about one game: `game.json` (identity), `playbook.md` (controls, strategy, shortcuts, RAM), `checkpoints.txt`, `shots.txt` and `shots/<set>/` (screenshots), `design/` (design reference), `saves/`, `tools/` (game-specific helpers). A game with a translation or deeper reverse engineering adds `translation/` and `tech/`. |
| `games/_template/` | Starting files for a new game. |
| `tools/` | Shared tooling for every game: register a ROM, drive the emulators, play, capture and verify screenshot sets. |
| `tests/` | Tests for the shared tooling. |
| `docs/` | How the tooling is used: [emulator guide](docs/emulator/README.md) (general rules, plus one file per platform: Game Boy, NES, SNES, Master System, Mega Drive, DOS, Apple II, Amiga), [capture guide](docs/capture-guide.md), status and history. |
| `skills/` | Working procedures for the AI agents that do much of the work, each with its open lessons and a feedback log ([index](skills/skill-index.md)). |
| `agent-log/` | One line per agent run: who, what, which files, outcome. |
| `AGENTS.md` | Rules for all work in this repository (also read through `CLAUDE.md`). |
| `rom/`, `work/` | Your ROMs, downloaded saves and patches; states, caches and scratch. Ignored by git. |

## How a game gets into the database

```
ROM --tools/intake.py--> games/<platform>/<slug>/ --scout--> playbook + checkpoints --capture--> shots/<set>/ --> commit
```
1. **Intake:** `python3 tools/intake.py /path/game.gbc` identifies the ROM (header, SHA-1, CRC32), copies it to
   `rom/` (never committed), creates `games/<platform>/<slug>/` and films the first seconds after power-on.
2. **Scout** (`skills/game-scout/`): researches the game, verifies boot route, controls, RAM and shortcuts in
   the emulator, writes the playbook and the shot plan.
3. **Capture** (`skills/game-capture/`): plays toward the shot plan, snaps each target, verifies that every shot
   replays from power-on, publishes the set, extends the design reference.
4. **Review:** the coordinator reruns the verification, looks at the contact sheet and commits.

A set is one PNG per shot (native resolution, raw framebuffer; enlarged copies on demand with
`python3 tools/x3.py FOLDER`), `index.json` (identity and per shot: category, caption, route, model, ROM SHA-1, date),
`index.md`, a contact sheet and the routes in `shots.txt`. File names carry their context
(`docs/capture-guide.md`, "File names"): `<game>_<platform>_<region>_<category>_<id>.png`, e.g.
`dragon-quest_nes_jp_battle_battle_slime.png`.

## Quick start

```sh
sh tools/setup_emu.sh                                   # builds the emulators into tools/ (once)
python3 tools/intake.py ~/roms/mygame.nes --region na  # region of the dump: jp, na or eu
python3 tools/play.py start mygame                     # explore: one emulator kept running
python3 tools/play.py do "w300,start"
python3 tools/play.py snap title_screen title "Title screen"
python3 tools/preview.py mygame plan.txt               # or: many candidate routes at once, one sheet
python3 tools/shoot.py mygame main --verify            # every shot replays from power-on
python3 -m pytest -q tests
```

Building the Wizardry Empire translation: [games/gbc/wizardry-empire/translation/README.md](games/gbc/wizardry-empire/translation/README.md).

## Rules in short
- Never commit game data: ROMs, savestates, downloaded saves or patched builds (`.gitignore` covers them).
- Screenshots are catalogue pieces, not a fair playthrough: saves, codes and RAM pokes are used whenever faster,
  with realistic values on screen. Every shot keeps the route that reproduces it.
- Translations are edited in script files, never in a ROM.
- Every area keeps a current snapshot (`status.md`) and an append-only history (`progress-log.md`).

## Licence

Tools, patches and documentation: MIT. Original game text appears only where a translation needs it to check
its work against the source. Do not share patched ROMs.
