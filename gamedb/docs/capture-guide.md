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

## Quality rules
- **Settled and complete:** text fully typed, no fade, no transition half-drawn. `settled: no` is acceptable only
  for genuinely animated screens; then pick the frame by eye (`do!` + `wN`) so nothing is cut off.
- **Representative:** enemies and items on screen, not an empty corridor; the player visible; mid-action beats
  standing still. Avoid the pause overlay unless the shot is of the pause menu.
- **Readable:** cursor not covering text.
- **Plausible:** cheated values look like a real save (`docs/emulator.md`, realistic values): 8973 gold, not 9999.
  The main character is named **ryz** where the game allows naming.
- **No duplicates:** two shots must differ in content, not only in a few pixels.
- **Captions:** factual, what is on screen, max ~80 characters: "World 1-2: underground level, Koopa shells"
  is better than "Cool level". Use the game's own names (from the playbook glossary/sources).
- **Ids:** lowercase `area_thing` (`title_screen`, `w1_forest_start`, `battle_magic`, `boss_dragon`). Stable:
  they name the files.

## Action sequences and clips (owner's request 2026-11-15)
Some actions are best shown as what happens, step by step (fishing, fast travel, a level-up, a transformation).
- **Sequence set** `seq-<action>` (e.g. `seq-fishing`): one shot per step, in the order the player sees them,
  ids `01_<step>`, `02_<step>`, ... (the order of the shot list is the order of the steps). Start from the
  last normal gameplay frame before the action and end on the first normal frame after it. Every menu, prompt
  and text box of the action is a step; captions say what the player did ("Select SUPER ROD, USE").
  shoot.py adds `strip.png` (all steps, numbered) and `steps.gif` (1.5 s per step).
- **Clips** for the motion itself (an animation between two steps: casting, take-off, landing, a transition):
  `play.py record ID CATEGORY FRAMES "caption" --every K --set seq-<action>` -> `<id>.gif` / `@3x.gif` at game
  speed (poster frame `<id>.png`). Keep clips short (1-6 s: FRAMES 60-360) and K=2 (30 fps) for smooth motion,
  K=3-4 for slow scenes; a clip is part of the step order like any shot. A clip takes the category of what it
  shows (gameplay, battle, map); there is no `clip` category.
- **Poster:** the clip's still (`<id>.png`, its picture in strip.png / steps.gif) is kept frame 0 unless chosen:
  `record` prints `work/play/NAME/clip_<id>.png` with every kept frame numbered; pick the frame that shows the
  action (not the frame of the step before, not a white fade) and re-record with `--poster N` after `undo`, or
  add `:N` to the clip's `rec:` token and reshoot it with `shoot.py --only`.
- Same quality rules as stills: realistic values, nothing broken; a sequence uses one consistent situation
  (same place, same party) from start to end.

## Design reference
Shots are evidence for `games/<slug>/design/`: when a shot shows a rule or a number (a shop price list, a level-up
screen, a status screen), link it from the design document that states the rule.

## Sets
- `main` is the database set. Other sets for variants: `dmg` / `sgb` (another model), `jp` (another region/ROM
  revision, separate game slug).
- A set is finished when `tools/shoot.py SLUG main --verify` reproduces every shot and the contact sheet
  (`sheet.png`) has been looked at as a whole (variety, no duplicates, nothing broken).
