# Quake (DOS, shareware 1.06) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
Enter a level, move through it in real time, open doors and ride lifts, kill the monsters that wake up, pick
up ammunition and health, find the exit; between levels nothing carries over but health, armor and weapons
(source: manual). Secrets and kills are counted on the TAB overlay [28](../shots/start/quake_dos_na_28_hud_e1m1_scores.start.png) (verified).

## 2. Systems
Go through every group; write "none" where the game has nothing, do not drop the group.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move, turn, jump, swim, fire, look up/down, choose weapon | Arrow keys move and turn in real time; Ctrl fires the current weapon; walking into buttons and slipgates uses them | arrows, Ctrl, Space, A/Z, 1-8 | turning about 1.95 degrees per frame (RAM); one Ctrl tap fires one shotgun shell (RAM) | [playbook](../playbook.md) Controls | [08](../shots/start/quake_dos_na_08_menu_help_movement.start.png) [09](../shots/start/quake_dos_na_09_gameplay_start_spawn.start.png) [21](../shots/start/quake_dos_na_21_battle_e1m1_grunt_hit.start.png) [26](../shots/start/quake_dos_na_26_battle_e1m1_yard_fire.start.png) | shown |
| Characters and progression | none beyond weapons and items | One unnamed marine; no levels or statistics: what grows is the arsenal and the items carried (source: manual HELP.TXT) | - | - | - | [16](../shots/start/quake_dos_na_16_gameplay_e1m1_start.start.png) (status bar: all there is) | described |
| Resources and economy | Health, armor, ammunition | Health starts at 100, armor 0, 25 shells; each shotgun shot costs one shell (verified: 25 to 20 over five shots); a killed Grunt drops a backpack of ammunition (verified 23; this route walks past it) | - | health 100 to 88 to 76 by Grunt shots of 12 (RAM) | - | [16](../shots/start/quake_dos_na_16_gameplay_e1m1_start.start.png) [23](../shots/start/quake_dos_na_23_gameplay_e1m1_backpack.start.png) [27](../shots/start/quake_dos_na_27_battle_e1m1_yard_clear.start.png) | shown |
| Conflict | Real-time hitscan and melee combat | Shots hit at once (hitscan shotgun, spread); monsters wake on sight or sound and close in; two shotgun hits kill a Grunt (verified) | aim by turning, Ctrl | Grunt hit takes 12 health on Normal (RAM, twice) | - | [20](../shots/start/quake_dos_na_20_gameplay_e1m1_door_grunt.start.png) [21](../shots/start/quake_dos_na_21_battle_e1m1_grunt_hit.start.png) [22](../shots/start/quake_dos_na_22_battle_e1m1_grunt_dead.start.png) [25](../shots/start/quake_dos_na_25_battle_e1m1_yard_attack.start.png) [26](../shots/start/quake_dos_na_26_battle_e1m1_yard_fire.start.png) [27](../shots/start/quake_dos_na_27_battle_e1m1_yard_clear.start.png) | shown |
| Opponents | Monsters placed per skill | Every monster and item has a skill mask in the map: E1M1 has 23 monsters on Normal (verified on TAB), more on Hard (map data) | - | Grunt, Rottweiler in the first yard (map data) | [content.md](content.md) | [20](../shots/start/quake_dos_na_20_gameplay_e1m1_door_grunt.start.png) [25](../shots/start/quake_dos_na_25_battle_e1m1_yard_attack.start.png) | shown |
| Items and equipment | Weapons, ammo, armor, health, power-ups, keys | Picked up by walking over them; the demo shows the pickup messages (verified 04); the start route picks up nothing | walk over | - | [content.md](content.md) | [04](../shots/start/quake_dos_na_04_title_demo_play.start.png) [23](../shots/start/quake_dos_na_23_gameplay_e1m1_backpack.start.png) | shown |
| Abilities and magic | none | No spells; power-ups (Quad Damage, Pentagram, Ring, Biosuit) are timed items (source) | - | - | - | none: no power-up before the first save | described |
| World and navigation | Start map, hub, levels; doors, buttons, lifts, water, secrets | Skill is chosen by the hall walked into; slipgates move between maps; doors slide open on approach; a button sends the lift down; water is swimmable; 6 secrets in E1M1 (verified on TAB) | walk, Space to swim up | E1M1 load about 35 frames (verified) | [playbook](../playbook.md) Game structure | [10](../shots/start/quake_dos_na_10_gameplay_normal_hall.start.png) [11](../shots/start/quake_dos_na_11_gameplay_hub_arrival.start.png) [12](../shots/start/quake_dos_na_12_gameplay_env_hub_west.start.png) [14](../shots/start/quake_dos_na_14_gameplay_hub_e1_gate.start.png) [15](../shots/start/quake_dos_na_15_system_loading.start.png) [17](../shots/start/quake_dos_na_17_gameplay_env_e1m1_corridor.start.png) [18](../shots/start/quake_dos_na_18_gameplay_env_e1m1_computers.start.png) [19](../shots/start/quake_dos_na_19_gameplay_env_e1m1_ledge.start.png) [24](../shots/start/quake_dos_na_24_gameplay_e1m1_button.start.png) | shown |
| Goals and gating | Level exit; shareware gate | Reach each level's exit; episodes 2-4 are closed in the shareware with a register message (verified) | - | 4 episodes, 1 playable | - | [13](../shots/start/quake_dos_na_13_gameplay_hub_shareware.start.png) [07](../shots/start/quake_dos_na_07_menu_ordering.start.png) | shown |
| Chance | Monster reactions and spread | Monster aim and shotgun spread vary with timing: the same route always gives the same fight, a changed wait gives another (verified) | timing | - | [playbook](../playbook.md) Strategy | [25](../shots/start/quake_dos_na_25_battle_e1m1_yard_attack.start.png) | shown |
| Failure and recovery | Death restarts the level | At 0 health the player dies and restarts the level or loads a save (source) | - | - | - | none: the honest start route takes 12 damage and never dies | described |
| Saving and sessions | Save anywhere, 12 slots | F2 or the Single Player menu saves to a slot named after the level with kills; F6 quicksave (source) | F2, Enter | slot 1 = ID1/S0.SAV (verified) | - | [33](../shots/start/quake_dos_na_33_save_menu.start.png) [34](../shots/start/quake_dos_na_34_save_saved.start.png) [35](../shots/start/quake_dos_na_35_save_load_menu.start.png) | shown |
| Pacing and difficulty | Skill by hall; HUD scores | Easy/Normal/Hard halls, a hidden Nightmare; the first level teaches doors, buttons, lifts and single Grunts before groups (verified on Normal) | walking | TAB: Monsters 2/23, Secrets 0/6 at 0:24 (verified) | - | [10](../shots/start/quake_dos_na_10_gameplay_normal_hall.start.png) [28](../shots/start/quake_dos_na_28_hud_e1m1_scores.start.png) | shown |

## 3. How the systems feed each other
- Fights cost health and shells; killed Grunts drop backpacks (verified 23; not picked up on this route); health and ammunition
  boxes in the level close the loop (map data).
- Skill chosen in the start map decides which monsters and items exist in every level (map data, skill masks).

## Open questions
