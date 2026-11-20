# Capture guide - what goes into the database

A game's set should let someone who never played it see what it is: how it starts, how it looks while playing,
and each system that makes it this game. Aim for **20-40 shots** for a typical game; more for large RPGs, fewer
for small arcade games. Quality beats count.

## Categories (`category` field; `tools/shoot.py` warns about others)
| Category | What | Typical count |
|---|---|---|
| `boot` | publisher/developer logos, licence screens | 1-2 |
| `title` | title screen (and attract-mode variants if distinct) | 1-2 |
| `menu` | main menu, file select, mode select, pause menu | 1-3 |
| `options` | settings, sound test, controls | 0-2 |
| `cutscene` | intro and story scenes | 1-3 |
| `gameplay` | the core loop, one per distinct area/world/vehicle/mode | 6-15 |
| `hud` | a clean frame that shows the whole HUD (with numbers readable) | 1 |
| `system` | a distinctive mechanic in action (crafting, transformations, day/night, upgrades, puzzles) | 2-6 |
| `map` | world map, dungeon map, level select | 1-3 |
| `inventory` | items, equipment, status/character screens | 1-3 |
| `dialogue` | NPC talk, text boxes | 1-2 |
| `shop` | buying/selling | 0-1 |
| `battle` | battle screens of RPGs: command menu, attack, magic, results | 2-5 |
| `boss` | boss fights | 1-4 |
| `minigame` | minigames, bonus stages | 0-3 |
| `gameover` | game-over / continue screen | 1 |
| `save` | save/password/load screens | 0-1 |
| `ending`, `credits` | only if reachable within the session (checkpoint/password/poke) | 0-2 |
| `extra` | anything notable that fits nowhere else (secrets, debug menus) | 0-3 |

## Must-have list (every game)
title - main menu - first moment of control - HUD - at least 5 gameplay shots from different areas or
situations - every core system the playbook lists - one boss (if the game has bosses) - game over (if any).

Standard environment shots (owner's rule 2026-11-19): besides the shots where something happens, every set has
a few plain views of each kind of place with nothing special going on: no message, no menu, no enemy, no
event square. They show what the game looks like most of the time (a corridor, a junction, a door, a stretch of
overworld, a town street). Take several per look, from different places and depths (in a dungeon game: some
on the first floor, some on the last), category `gameplay`, ids `env_<place>_<what>`; the caption says where
and adds nothing that is not on screen. They are exempt from the "Representative" rule below.

Breadth (owner's rule 2026-11-18): rather more features, mechanics, systems and shots than fewer. Every command
the game offers gets a shot of it at work, minor ones included; several battles with different, interesting
enemies; each distinct visual environment once. Details: `skills/game-capture/skill.md`, step 6.

## Quality rules
- **Settled and complete:** text fully typed, no fade, no transition half-drawn. `settled: no` is acceptable only
  for genuinely animated screens; then pick the frame by eye (`do!` + `wN`) so nothing is cut off.
- **Representative:** enemies and items on screen, not an empty corridor; the player visible; mid-action beats
  standing still. Avoid the pause overlay unless the shot is of the pause menu.
- **Readable:** cursor not covering text.
- **Plausible:** cheated values look like a real save (`docs/emulator/README.md`, realistic values): 8973 gold, not 9999.
  The main character is named **ryz** where the game allows naming.
- **No duplicates:** two shots must differ in content, not only in a few pixels.
- **Captions:** factual, what is on screen, max ~80 characters: "World 1-2: underground level, Koopa shells"
  is better than "Cool level". Use the game's own names (from the playbook glossary/sources).
- **Ids:** lowercase `area_thing` (`title_screen`, `w1_forest_start`, `battle_magic`, `boss_dragon`). Stable:
  they name the files.

## File names (owner's rule 2026-11-18)
Every image and GIF says what it shows without its folder, so a file keeps its context wherever it is copied:

```
<game>_<platform>_<region>_<area>_<id>[.<set>].<ext>
```

| Field | From | Characters | Example |
|---|---|---|---|
| `game` | `game.json` "slug": the short normalized game name, without the platform | `a-z0-9-` | `might-and-magic` |
| `platform` | `game.json` "platform" (the folder under `games/`) | `a-z0-9` | `nes` |
| `region` | `game.json` "region": where the registered dump was released | `jp`, `na`, `eu` | `na` |
| `area` | the shot's category (table above) | `a-z` | `battle` |
| `id` | the shot id, unchanged; in a `seq-<action>` set `seq-<action>_<id>` | `a-z0-9_-` | `battle_sprites` |
| `.set` | the set name, for every set but `main` and `seq-*` | `a-z0-9-` | `.compare-maze` |

- Examples: `might-and-magic_nes_na_inventory_view_profile.png`, `dragon-quest_nes_jp_battle_battle_slime.png`,
  `wizardry_nes_na_gameplay_maze_f1.compare-maze.png`, `pokemon-blue_gb_na_gameplay_seq-fishing_07_cast_clip.gif`.
- The first four fields never hold a `_`: `name.split("_", 4)` gives game, platform, region, area and the rest.
- **Region is the release of the dump, not the language on screen:** a Japanese ROM with an English patch is
  `jp`. `nes` covers NES and Famicom, `snes` SNES and Super Famicom: the region tells them apart. DOS games
  take the region of the release (`na` for a US release). `tools/intake.py --region` sets it.
- **Set `start`** (owner's rule 2026-11-20): its ids are `NN_<step>` and the step number moves in front of the
  area, so the files list in play order: `<game>_<platform>_<region>_<NN>_<area>_<step>.start.png`
  (`dungeon-master_amiga_eu_01_boot_crack_note.start.png`). Here `name.split("_", 5)` gives game, platform,
  region, number, area and step. `tools/shoot.py` refuses an unnumbered id in this set.
- An id that starts with its category repeats it (`..._battle_battle_slime`): accepted, ids are not shortened.
- The 3x copy has the same name in `3x/`.
- Files about the whole set use the area `set`: `<game>_<platform>_<region>_set_sheet[.<set>].png`, in a
  sequence `..._set_seq-<action>_strip.png`, `_steps.gif`, `_full.gif`. `index.json`, `index.md` and
  `shots.txt` keep their names.
- The tools build the names (`tools/shoot.py`: `stem()`, `set_file()`); nobody types them. Changing a shot's
  category, or the slug or region in `game.json`, renames the files on the next `shoot.py` run.
- Wizardry Empire (its own `translation/tools/shoot.py`) uses the same scheme with the set always written and
  the ROM last: `wizardry-empire_gbc_jp_menu_camp.rev1-tour.en.png`.

## Action sequences and clips (owner's request 2026-11-15)
Some actions are best shown as what happens, step by step (fishing, fast travel, a level-up, a transformation).
- **File names:** in a sequence set the id part of every file name starts with the set name (owner's rule
  2026-11-15, inside the scheme of "File names" since 2026-11-18): `pokemon-blue_gb_na_gameplay_seq-fishing_01_shore.png`,
  `..._seq-fishing_07_cast_clip.gif`, `pokemon-blue_gb_na_set_seq-fishing_full.gif`, `..._set_seq-fishing_strip.png`.
  The shot ids stay short (`01_shore`); the tools add the rest.
- **Sequence set** `seq-<action>` (e.g. `seq-fishing`): one shot per step, in the order the player sees them,
  ids `01_<step>`, `02_<step>`, ... (the order of the shot list is the order of the steps). Start from the
  last normal gameplay frame before the action and end on the first normal frame after it. Every menu, prompt
  and text box of the action is a step; captions say what the player did ("Select SUPER ROD, USE").
  shoot.py adds `..._strip.png` (all steps, numbered), `..._steps.gif` (stills only, 1.5 s each) and **`..._full.gif`**
  (owner's request: every step stitched in order - stills held 1.5 s, the first 2 s and the last 3 s, clips
  played in full at game speed), each also as a 3x copy in `3x/`. They are rebuilt on every snap/record, full --verify and publish.
- **Clips** for the motion itself (an animation between two steps: casting, take-off, landing, a transition):
  `play.py record ID CATEGORY FRAMES "caption" --every K --set seq-<action>` -> a `.gif` (and `3x/`) at game
  speed (poster frame: the `.png` of the same name). Keep clips short (1-6 s: FRAMES 60-360) and K=2 (30 fps) for smooth motion,
  K=3-4 for slow scenes; a clip is part of the step order like any shot. A clip takes the category of what it
  shows (gameplay, battle, map); there is no `clip` category.
- **Poster:** the clip's still (its `.png`, its picture in the strip and the steps GIF) is kept frame 0 unless chosen:
  `record` prints `work/play/NAME/clip_<id>.png` with every kept frame numbered; pick the frame that shows the
  action (not the frame of the step before, not a white fade) and re-record with `--poster N` after `undo`, or
  add `:N` to the clip's `rec:` token and reshoot it with `shoot.py --only`.
- Same quality rules as stills: realistic values, nothing broken; a sequence uses one consistent situation
  (same place, same party) from start to end.

## Design reference
Shots are evidence for `games/<platform>/<slug>/design/`: when a shot shows a rule or a number (a shop price list, a level-up
screen, a status screen), link it from the design document that states the rule.

## Three lenses: systems, interface, content (owner's request 2026-11-18)
Every game is documented three times over the same shots: for game design, for UI/UX, and for the variety of
its content. Overlap is intended: a shop screen is evidence for the economy, an interface in its own right,
and shows items. In general the shots of a set should cover all three; how much of each depends on the game,
its genre and structure.
- **Systems** (`design/systems.md`): the index of every feature, system and mechanic, in fixed groups (player
  verbs, characters and progression, resources and economy, conflict, opponents, items, abilities, world and
  navigation, goals and gating, chance, failure and recovery, saving, pacing). One row each: the rule in one
  line, the player's inputs, the numbers known, the document with the details, the shots, a status. A group
  the game does not have says "none".
- **Interface** (`design/interface.md`): conventions (input, layout, text, feedback, state visibility, help),
  then an inventory with one row per screen, menu, prompt, message type and permanent element (purpose, what it
  shows, what it accepts, how it answers, where it leads), the screen flow, and the main screens element by
  element. Judgements are marked **Observation:**.
- **Content** (`design/content.md`): what fills the game, as a reasonable variety, not a full set: the kinds of
  content this game has (environments, opponents, items, equipment, abilities, people, and its own kinds:
  vehicles, levels, puzzles ...), the total of each if known, and a sample that spans the range (early and late,
  common and rare, one of each visual family). Complete tables live in their own documents and are linked.
- Shots serve all three: when choosing what to capture, ask "which rule does this show?", "which screen or
  element is this?" and "which piece of content does this add?". A prompt with nothing behind it is still an interface row; a rule with no screen of its
  own (a hidden roll) is still a systems row, status `described`.
- `python3 tools/lenses.py SLUG [SET]` lists shots that no document mentions and rows without a shot. A
  set is not finished while a shot is unused or a row says neither which shot shows it nor why there is none.
Templates: `games/_template/design/systems.md`, `interface.md`, `content.md`.

## Sets
- `start` (owner's request 2026-11-19): the early game as a new player meets it, in play order, ending with the
  first save: power-on and title, the way into a new game, making the character or party, the first screens of
  control, first shop and equipment, first steps, the first fight and its reward, the first return to safety
  (healing, level check) and saving. Played honestly from the game's own starting state: no strengthened
  party, no warps, no pokes of values (a position shortcut is acceptable only where walking is long and
  shows nothing). Shots that also exist in `main` are taken again here with their routes, so the set stands on
  its own; 30-60 shots. Its checkpoints are named `s_...`. It needs no lens documents of its own.
  **Sequential order** (owner's rule 2026-11-20): ids are numbered in play order like a sequence set,
  `01_<step>`, `02_<step>`, ... (two digits, three past 99), and the set's `shots.txt` lists them in that
  order, so `index.md`, the contact sheet and the ids read as one playthrough. A shot added later between two
  steps renumbers the ones after it (the files are renamed on the next `shoot.py` run). In this set only, the
  step number goes before the area in the file name (owner's rule 2026-11-20, "File names"), so a folder
  listing is the play order too.
- `main` is the database set. Other sets for variants: `dmg` / `sgb` (another model), `jp` (another region/ROM
  revision, separate game slug).
- A set is finished when `tools/shoot.py SLUG main --verify` reproduces every shot and the contact sheet
  (`<game>_<platform>_<region>_set_sheet.png`) has been looked at as a whole (variety, no duplicates, nothing broken).
