# Alien vs Predator - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. The same shots
also appear in [interface.md](interface.md) (the screens) and [content.md](content.md) (the variety of what
fills the game). Notation: [README.md](README.md). Check: `python3 tools/lenses.py jaguar/alien-vs-predator`.
Shot ids in backticks are in `../shots/main/` unless marked `start:` (the `start` set, `../shots/start/`).

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
A first-person action game on a tile grid (64 by 64 cells per level) **(RAM)**. The player picks one of three
species **(verified: `select_alien`, `select_predator`, `select_marine`)**; each has its own goal, HUD and
abilities. Moment to moment: move through corridors and rooms, open doors, meet Aliens (and, for the Alien
and the Predator, Marines), fight in real time, pick up what the dead leave. Between fights the Marine reads
terminals for maps and logs, rides lifts and crawls through air ducts to the next of five sublevels and the
two docked ships; the score (Marine, Alien) or honor points (Predator) rise with every kill **(verified:
`start:14_alien_killed`, `predator_cannon_kill`)**.

## 2. Systems
| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move and turn | Pad up/down walks forward/back, left/right turns; turning accelerates the longer it is held **(RAM)** | d-pad; C + left/right sidesteps **(source)** | a quarter turn takes about 64 frames held; walking about one cell per 40 frames **(RAM)** | playbook RAM map | `start:09_brig_corridor`, `env_sublevel1` | shown |
| Player verbs | Use / open | A opens doors and cell bars, uses terminals, enters vents and lifts **(verified)** | A | - | | `marine_cell_open`, `vent_entered`, `lift_inside`, `terminal_menu` | shown |
| Player verbs | Attack | B fires the selected weapon (Marine, Predator); A/B/C are claw, bite, tail for the Alien **(source)** | B (A/B/C Alien) | | section Conflict | `marine_pulse_rifle_hit`, `predator_cannon` | shown |
| Player verbs | Weapon select | Keypad 1-4 picks a weapon the character owns **(verified)** | keypad 1-4 | | | `hud_marine`, `predator_combistick`, `predator_smartdisc` | shown |
| Player verbs | Pause and save | Pause stops the game; Pause then Option opens HUD brightness and the three save slots; B saves **(verified)** | Pause, Option, up/down, B | 3 slots | interface.md | `pause_paused`, `pause_options`, `start:26_save_slot` | shown |
| Player verbs | Reset | * and # held together return to the title from anywhere **(verified: `start:28_restore_list` route)** | * + # | held about 30 frames; a short press does nothing **(verified)** | | `start:28_restore_list` | shown |
| Characters and progression | Three species | Marine, Alien, Predator, chosen on a rotating carousel; each has its own briefing and goal **(verified)** | left/right, fire | 3 | content.md | `select_alien`, `select_predator`, `select_marine`, `brief_alien`, `brief_predator`, `brief_marine` | shown |
| Characters and progression | Marine security clearance | Cards 1-10 taken from dead staff raise the clearance shown in the HUD; doors and First Aid need a level **(source)**; card 10 is needed for the self-destruct **(source)** | walking over cards | starts at 00 **(verified: `marine_brig`)** | | `hud_marine` (07) | described: no card picked up in play (poked value shown) |
| Characters and progression | Predator honor weapons | Honor points unlock combistick at 150,000, smart disc at 350,000, shoulder cannon at 750,000 **(source)**; passing 750,000 shows SHOULDER CANNON ATTAINED **(verified)** | kills while visible | +5000 for an Alien killed with the shoulder cannon **(RAM)** | | `predator_attained`, `predator_cannon_kill` | shown |
| Characters and progression | Alien cocoons | Claw, tail, claw stuns a Marine; walking over him makes a cocoon, an extra life; at most three **(source)** | A, C, A | 3 | | none: no Marine enemy met by the Alien within budget | described |
| Resources and economy | Energy | Marine 1000, Alien about 1125, Predator 3000 at the start **(RAM)**; the bar in the HUD falls with each hit **(verified)** | - | | | `hud_marine`, `marine_hurt` | shown |
| Resources and economy | Ammunition | Each Marine weapon has its own ammo bar; shotgun 1 round per shot, pulse rifle 4 rounds per short burst **(RAM)**; dead Marines and lockers give weapons and rounds **(verified)** | walking over | shotgun starts with 15 rounds when collected **(RAM)**; maxima 44, 264, 88, 88 **(RAM)** | | `pickup_shotgun`, `pickup_rounds`, `hud_marine` | shown |
| Resources and economy | Healing | Marine: First Aid on blue med-lab terminals with card 4+, refill by clearance; Predator: medkit reserve (keypad 5); Alien cannot heal **(source)** | A at terminal; keypad 5 | card 4-6 up to 50% **(source)** | | none: med-lab not reached | described |
| Resources and economy | Score | Marine: 10,000 per Alien killed **(verified: `start:14_alien_killed`, `marine_alien_dead`)** | - | 10000 | | `start:17_second_alien_killed` | shown |
| Conflict | Damage to the player | A hit flashes the screen: red (Marine), purple (Alien), yellow-green (Predator) **(verified)**; Alien hits on the Marine cost 20-130 energy each **(RAM)** | - | 1000 -> 900 -> 870 -> 850 -> 800 -> 670 over one fight **(RAM)** | | `start:15_second_alien_hit`, `marine_hurt`, `alien_hurt`, `predator_hurt` | shown |
| Conflict | Marine weapons | Shotgun, pulse rifle, flamethrower, smart gun **(verified)**; hits throw sparks, a killed Alien leaves acid on the floor **(verified)** | 1-4, B | pulse rifle kills an Alien with about three bursts **(RAM)** | | `marine_shotgun`, `marine_pulse_rifle_hit`, `marine_pulse_rifle_kill`, `marine_flamethrower`, `marine_smartgun`, `marine_alien_dead` | shown |
| Conflict | Predator weapons | Wrist blade from the start; combistick, smart disc, shoulder cannon by honor **(source)**; the cannon fires a blue bolt **(verified)** | 1-4, B | | | `predator_combistick`, `predator_cannon`, `predator_cannon_kill`, `predator_smartdisc` | shown |
| Conflict | Honor rule | Killing while cloaked costs honor points **(source)** | Option (cloak) | | | `predator_cloak` | described: no cloaked kill made |
| Conflict | Acid blood | A killed Alien leaves a yellow acid splash on the floor **(verified)** | - | | | `marine_alien_dead`, `predator_cannon_kill` | shown |
| Opponents | Aliens | Run in from side rooms and charge; strike at close range **(verified)**; also in the air ducts **(verified: `airduct_alien`)** | - | several per level, placed at random per simulation **(source)** | content.md | `start:12_alien_enters`, `marine_alien_sublevel4`, `marine_alien_sublevel5`, `marine_alien_office`, `lift_arrived` | shown |
| Opponents | Unseen attacker at the Alien start | The Alien loses energy in its first seconds in its own ship and on sublevels (purple flashes) with no enemy in view **(verified)** | - | about 200 in 10 s **(RAM)** | findings.md | `alien_hurt` | open |
| Opponents | Marines, Predator, facehuggers, Queen | Marines for the Alien and Predator to fight; facehuggers to shake off; the Alien Queen as a boss **(source)** | - | | | none: not met within budget | described |
| Items and equipment | Pick-ups | Walking over an item takes it, a large message names it **(verified)** | - | | | `pickup_shotgun`, `pickup_rounds`, `start:08_shotgun_collected` | shown |
| Items and equipment | Motion tracker | HUD radar with a distance readout; found on a dead Marine on sublevel 5 **(source)** | - | | | `marine_tracker` | shown |
| Abilities and magic | Predator cloak and vision | Option toggles invisibility; keypad 6 cycles five vision filters **(verified for cloak and one filter)** | Option, 6 | 5 filters **(source)** | | `predator_cloak`, `predator_filter` | shown |
| World and navigation | Levels | Sublevels 1-5, eight air ducts, the Alien ship and the Predator ship **(verified: warp to every level)**; each sublevel is a 64x64 grid **(RAM)** | - | 15 areas | content.md | `env_sublevel1`, `env_sublevel2`, `env_sublevel3`, `env_sublevel4`, `env_alien_ship`, `env_predator_ship` | shown |
| World and navigation | Arrival banner | Entering a level shows ENTERING SUBLEVEL N for about 3 seconds **(verified)** | - | | | `entering_sublevel` | shown |
| World and navigation | Doors and airlocks | Doors open with A; airlocks must be closed behind before the next opens **(source)** | A | | | `door_closed`, `airlock_door`, `start:11_door` | shown |
| World and navigation | Lifts | Open the hatch with A, then up + A / down + A rides a level; an Alien may wait outside **(verified)** | A, up/down + A | | | `lift_hatch`, `lift_inside`, `lift_arrived` | shown |
| World and navigation | Air ducts | A at a wall vent moves the Marine into a duct level **(verified)** | A | 8 ducts | | `vent`, `vent_entered`, `airduct_alien` | shown |
| World and navigation | Terminals and map | Terminals give a level schematic with a room legend and a paged General Log **(verified)** | A, up/down, B select, A next, C exit | log 3-4 pages per terminal **(verified)** | interface.md | `terminal`, `terminal_menu`, `map_level3`, `log_page1`, `log_page2`, `log_page3` | shown |
| World and navigation | Wall signs | Signs name rooms (BRIG, CANTEEN, ELEVATOR, SUB LEVEL 3) **(verified)** | - | | | `sign_brig`, `sign_sublevel` | shown |
| Goals and gating | Species goals | Marine: arm up, card 10, self-destruct, escape pod on sublevel 5; Alien: rescue the Queen from the Predator ship; Predator: take the Queen's skull from the Alien ship **(source; briefings verified)** | - | | | `brief_marine`, `brief_alien`, `brief_predator` | shown |
| Chance | Placement | Enemies, ammo, food and medkits are regenerated at random on every simulation and after a restore **(source)** | - | | | none: a rule with no screen of its own | described |
| Failure and recovery | Death | Energy at 0: USCM badge and SIMULATION TERMINATED, then the high score table **(verified)** | - | | | `gameover`, `highscore_entry` | shown |
| Failure and recovery | High scores | A score that beats the fifth entry asks for three letters (up/down letter, left/right cursor, fire done) **(verified)** | up/down, left/right, A | five places | interface.md | `highscore_entry`, `highscore_ryz`, `highscores` | shown |
| Saving and sessions | EEPROM save | Three slots; a save keeps location, score, clearance, weapons, ammo, energy (Marine) **(source)**; RESTORE GAME lists the slots in each species' font **(verified)** | Pause, Option, B | 3 slots | | `pause_options`, `menu_restore`, `start:27_saved`, `start:28_restore_list` | shown |
| Pacing and difficulty | Start | The Marine starts unarmed; the first weapon lies two cells from the cell; two Aliens attack within the first minute **(verified: start set)** | - | | | `start:07_cell_open`, `start:13_alien_attack` | shown |

## 3. How the systems feed each other
- Marine: kills -> score; dead staff -> weapons, rounds, cards -> clearance -> armouries, med-lab healing,
  self-destruct -> escape.
- Predator: visible kills -> honor -> weapons; cloaked kills -> honor lost; medkits -> health reserve.
- Alien: stunned Marines -> cocoons -> extra lives; no healing, so cocoons are its only recovery.
- Terminals feed navigation: the schematic shows where lifts (E) and airlocks are.

## Open questions
- What drains the Alien's energy at its start (`alien_hurt`): no attacker was found on screen.
- Cocooning, facehuggers, Marines as enemies and the Alien Queen were not reached within the budget.
- Damage per weapon against Aliens was not measured per hit (Alien health not located).
