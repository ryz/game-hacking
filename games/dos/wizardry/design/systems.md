# Wizardry: Proving Grounds of the Mad Overlord (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
Create characters, form a party, enter the maze, walk square by square and fight what comes, take the loot,
go back up to rest, level and shop, and go a little deeper each time (verified screens; resting levels:
source). Between loops the party grows in level and equipment, the floors get harder and the player's own
paper maps grow, since the game shows no map (DUMAPIC only reports the position: `system_dumapic`).

## 2. Systems
Go through every group; write "none" where the game has nothing, do not drop the group.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Walk and turn | W steps forward, A turns left, D turns right; walls stop you ("You can't walk through walls!") | W A D | 1 square per step | [maps](maps/floors.txt) | `gameplay_maze_f1_start` | shown |
| Player verbs | Kick a door | K moves through a door in front | K | - | - | (planned `gameplay_kick_door`) | described: used to enter Werdna's room |
| Player verbs | Camp | C opens camp: inspect, reorder, equip, leave; spells and items are used from the character sheet | C, 1-6, R, E, Enter | - | - | `gameplay_camp`, `inventory_camp_inspect` | shown |
| Player verbs | View toggles | O hides the command line and party window (full view); S toggles the party window | O, S | - | - | `gameplay_full_view` | shown |
| Player verbs | Inspect | I in the maze, # in the tavern and camp: the character sheet with read, trade, pool gold, spell, equip, drop, identify, use | I, 1-6 | - | - | `inventory_inspect_vet` | shown |
| Characters and progression | Creation | name, password, race (5), alignment (3), random bonus points spread over six statistics, then a class the statistics allow | letters, Enter, Up/Down, Esc | bonus 6-7 seen; statistics 3-18 | playbook Naming | (planned `create_*`) | described |
| Characters and progression | Classes | Fighter, Mage, Priest, Thief, Bishop, Samurai, Lord, Ninja; the list offers only those the statistics and alignment allow (verified: Fighter only at STR 11; Fighter, Mage, Priest, Bishop at IQ 15 PIE 14) | class letter | - | content §6 | (planned `create_class`) | described |
| Characters and progression | Levels | experience from fights; levels are made by resting at the inn (source); a level-13 fighter needs about 400,000 E.P. (source, series table) | rest | - | - | (planned `system_levelup`) | described |
| Characters and progression | Level drain | vampires drain levels: a Vampire Lord took 4 levels from ryz in one hit (13 -> 9) (verified) | - | - | - | (planned `boss_werdna_fight`) | described |
| Characters and progression | Age | kept in weeks, shown in years; starts at 14-16 (verified) | - | - | - | `inventory_inspect_vet` | shown |
| Resources and economy | Gold | each character carries gold; new characters start with 100-199 (verified); the tavern divides it, the sheet pools it | D)ivvy, P)ool | - | - | `shop_boltac` | shown |
| Resources and economy | Shops and services | Boltac's buys and sells (long sword 25, short sword 15, anointed mace 30, anointed flail 150, staff 10, dagger 5 ...), uncurses, identifies; inn rooms 0/10/50/200/500 gold per week; temple cures for gold | letters | prices verified | - | `shop_boltac_buy`, `menu_inn` | shown |
| Conflict | Rounds | each round every member gets an order, then everything happens in an order the game decides; messages tell each blow ("Condi charges at a Slime and hits once for 5 damage") | F P S D U R T, group number | messages stay about 160 frames (2.7 s) each | - | `battle_options`, `battle_spell_prompt` | shown |
| Conflict | Front and back rank | the first three members can fight; members 4-6 parry, cast or use items (verified: Cubi, Deddo, Mnz had no Fight) | - | 3 front | - | `battle_options` | shown |
| Conflict | Surprise | "You surprised the monsters!": a first round without spells (verified twice) | - | - | [findings](findings.md) | `battle_options` | shown |
| Conflict | Targets | Fight and group spells ask "Fight which group (#)?" when there is more than one group | 1-4 | up to 4 groups | - | (planned `battle_group_select`) | described |
| Conflict | Status conditions | asleep, paralyzed ("PARALY"), dead, and the others of the series (afraid, stoned, ashes, lost) | - | - | - | (planned) | described |
| Opponents | Groups | monsters come in up to four named groups with counts; names start unidentified ("Man in robes" = Werdna) | - | - | content §3 | `battle_options`, `boss_werdna` | shown |
| Opponents | Fixed fights | squares that always start a fight (floor 3, 4, 7 and Werdna on 10; disk data, Werdna verified) | - | - | [maps](maps/floors.txt) | `boss_werdna` | shown |
| Items and equipment | Chests | a won fight may leave a chest: open, Calfo (priest spell that names the trap), leave, inspect, disarm | O C L I D | - | - | `battle_chest` | shown |
| Items and equipment | Identification | items found are unidentified; a bishop identifies them, Boltac does for gold | I | - | - | (planned) | described |
| Abilities and magic | Spells | typed by name ("Spell name ?"), in battle and in camp; 21 mage and 29 priest spells in 7 levels, points per level ("Mage 2/0/0/0/0/0/0") | S, name, Enter | points per level | content §5 | `battle_spell_prompt`, `system_dumapic` | shown |
| World and navigation | Maze | ten floors of 20 x 20 squares, walls, doors, hidden doors, darkness, rooms where fights are likelier, stairs and elevators (floors 1-4 and 4-9) | - | 10 floors | [maps](maps/floors.txt) | `gameplay_maze_f1_start`, `gameplay_dark` | shown |
| World and navigation | Traps of the maze | pits, spinners, teleporters, a chute (floor 9 to 10), anti-magic areas, rock (instant death) | - | positions in maps | [maps](maps/floors.txt) | `gameover_rock` | shown (rock) |
| World and navigation | Signs | messages on squares ("** Area out of bounds! **", Werdna's office hours) | Enter | - | - | `dialogue_sign_f1`, `dialogue_werdna_sign`, `dialogue_f4_desk` | shown |
| Goals and gating | Main goal | Werdna's amulet on floor 10 (17,3), taken up to the castle | - | - | - | `boss_werdna`, `ending_congratulations` | shown |
| Goals and gating | Gates | blue ribbon for the floor 4 elevator, keys and statuettes on floors 1-3 (source, series) | - | - | - | (planned) | described |
| Chance | Random rolls | encounters, monster groups, hits, damage, bonus points are random; with a fixed route they repeat (verified) | - | - | - | - | described |
| Failure and recovery | Death and the cemetery | a party killed or in rock: "Your entire party has been slaughtered" and the cemetery; the dead stay in the maze for a rescue party; the temple revives for gold | Enter | - | - | `gameover_cemetery`, `gameover_rock` | shown |
| Saving and sessions | Scenario disk | the roster is written to the scenario disk while playing and when leaving the game; leaving in the maze leaves the party "out" (Utilities: restart an "out" party) | L)eave game | - | playbook Saves | `menu_utilities` | shown |
| Saving and sessions | Moving characters | Utilities M)ove characters: the way characters go to Wizardry II and III (source, owner) | M | - | - | `menu_utilities` | shown |
| Pacing and difficulty | Ramp | floor 1 Slimes, vampires and Werdna on floor 10 (verified ends); a fresh party is fragile (8 HP each) | - | - | - | `battle_options`, `boss_werdna` | shown |

## 3. How the systems feed each other
- Fights give experience and gold (and chests); experience becomes levels at the inn; levels give hit points
  and spell points; gold buys equipment at Boltac's and pays the inn and the temple (verified screens, source
  for the level rule).
- Spell points are spent in the maze and come back by resting; deeper floors need more of them.
- Death costs gold at the temple (or the character); level drain undoes levels.

- Hit points at creation are always 8 here (findings); how the level-up adds them is not seen yet.
- The first-round spell rule (surprise only, or every first round?).
- Text on the disk is encoded (monster and item names are not plain text): the item and monster tables are
  not decoded; item 94 is the amulet (verified by the ending).
