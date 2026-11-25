# Spear of Destiny (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. The same shots
also appear in [interface.md](interface.md) (the screens) and [content.md](content.md) (the variety of what
fills the game); overlap is intended. Notation: [README.md](README.md). Shots are ids of the set `main`
(`../shots/main/index.md`) unless they start with a number (set `start`). Check:
`python3 tools/lenses.py dos/spear-of-destiny`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
B.J. Blazkowicz walks a grid of rooms in first person, opens doors, shoots the soldiers and dogs that see or
hear him, picks up ammunition, food, first aid, treasure and keys, and looks for pushwall secrets until he
finds the elevator. Each floor ends with a tally (time against par, kill, secret and treasure ratios, bonus
points). Every fifth or so floor ends with a boss; floor 18 holds the Spear, which carries him straight to the
Angel of Death on floor 21. Between loops the enemies get tougher and more numerous, and the wall sets change
from tunnels to dungeons to castle to ramparts.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move, turn, run, strafe | Free movement on a tile grid, walls block | W/S, A/D, Shift, Alt | 0.084 tile per frame walking, twice running; turn 1.75 degrees per frame (verified, playbook Controls) | playbook | `07_floor1_start`, `floor1_start` | shown |
| Player verbs | Fire | Fires the weapon in hand; holding fires again (machine gun and chain gun automatic) | Ctrl | one pistol bullet per press (verified: ammo 8 to 52 over the floor 1 fights) | below | `13_pistol_guard`, `weapon_pistol`, `weapon_machine_gun`, `weapon_chain_gun` | shown |
| Player verbs | Use (doors, pushwalls, elevator switch) | Space opens the door or pushes the wall ahead, or throws the elevator switch | Space | doors close again after about 5 s; a pushwall slides two tiles in about 256 frames (verified) | playbook | `08_pushwall`, `11_door_guard`, `18_treasure_door`, `elevator` | shown |
| Player verbs | Weapon choice | 1-4 pick knife, pistol, machine gun, chain gun if owned | 1 2 3 4 | (verified after MLI) | | `weapon_knife`, `weapon_pistol`, `weapon_machine_gun`, `weapon_chain_gun` | shown |
| Characters and progression | Score and extra lives | Points for kills and treasure; an extra life every 40000 | none | guard 100, officer 400, mutant 700, boss 5000 (verified: `17_guard3_down`, `enemy_officer_dies`, `enemy_mutant_dies`, `trans_grosse_dies`); treasure 100-500 (cross 100, chalice 500 by the room total 2400 for 8 pieces, inferred) | | `20_treasure_taken`, `trans_grosse_dies` | shown |
| Characters and progression | Weapons as progression | The best weapon owned stays for the game; lost on death (restart with the pistol) | pick up | (verified: `face_28` pistol after death) | | `hud`, `face_28` | shown |
| Resources and economy | Health | 0-100%, food, first aid, dog food restore it; at 0 a life is lost | walk over | health 100 -> 97 -> 82 -> 25 -> 16 in the honest start (verified, start set) | | `12_guard_fires`, `14_guard_close`, `16_west_door_guard` | shown |
| Resources and economy | Ammunition | One pool for pistol, machine gun and chain gun, max 99; clips +8 (dropped +4), the 25-clip box +25 | walk over | start 8; six clips in the secret room = 56 (verified `10_ammo_taken`); guards drop a clip (verified start) | | `09_ammo_room`, `10_ammo_taken`, `hud` | shown |
| Resources and economy | Treasure | Crosses, chalices, chests, crowns raise score and the treasure ratio | walk over | 8 pieces on floor 1 room = 2400 points (verified: score 300 -> 2700) | | `18_treasure_door`, `19_treasure_room`, `20_treasure_taken` | shown |
| Conflict | Hits and damage | Every shot is a roll; damage falls with distance; a hit flashes the screen red | none | Trans Grosse at 5+ tiles took B.J. 100 -> 86 -> 66 -> 52 -> 35 -> 7 -> 0 in 6 hits (RAM, `TGFIGHT,TF*N`) | | `12_guard_fires`, `face_9`, `face_18`, `ubermutant_hit` | shown |
| Conflict | Death of an enemy | A killed enemy plays a fall, leaves a body; guards and SS drop a clip | none | (verified) | | `15_guard_down`, `enemy_officer_dies`, `enemy_officer_dead`, `enemy_mutant_falls`, `trans_grosse_dead` | shown |
| Conflict | Status-bar face | B.J.'s face gets bloodier with each 1/7 of health lost; red-eyed dead face at 0 | none | stages seen at 100, 86, 66, 52, 7, 0 (verified `face_*`) | | `face_8`, `face_9`, `face_10`, `face_11`, `face_18`, `face_19` | shown |
| Opponents | Regular enemies | Guard, SS, officer, dog, mutant; standing ones wake when they see or hear B.J. | none | floor 1 skill 2: 18 enemies (RAM total) | [content.md](content.md) | `11_door_guard`, `enemy_officer`, `enemy_mutant` | shown |
| Opponents | Bosses | Trans Grosse (5), Barnacle Wilhelm (10), Ubermutant (16), Death Knight (18), Angel of Death (21); each idles until shot | none | Angel of Death 1650 hit points on "Bring 'em on!" (RAM 477EA, 1594 after the first burst); Trans Grosse died to about 450 frames of chain-gun fire (verified) | playbook | `trans_grosse_fight`, `barnacle_fight`, `ubermutant_fight`, `death_knight_rockets`, `angel_fireball` | shown |
| Opponents | Spectres | Ghosts on the Angel's floor float toward B.J. | none | 4 on the map (sodmap) | | `spectre` | shown |
| Items and equipment | Weapons | Knife, pistol, machine gun, chain gun | 1-4 | chain gun makes B.J. grin (Wolfenstein, inferred) | | `weapon_knife`, `weapon_chain_gun` | shown |
| Items and equipment | Keys | Gold and silver keys open the matching locked doors; shown on the status bar | walk over | (verified: MLI gives both, `hud`) | | `hud` | shown |
| Items and equipment | The Spear of Destiny | Taking it on floor 18 ends the floor and moves B.J. to floor 21 | walk over | (verified `spear_taken`) | | `spear_of_destiny`, `spear_taken` | shown |
| Abilities and magic | none | the game has no spells or abilities | | | | none: nothing to show | none |
| World and navigation | Floors | 21 floors: Tunnels 1-4, boss, Dungeons 1-4, boss, Castle 1-5, boss, Ramparts, Death Knight, two secret floors, Angel of Death | elevator | floor 21 shows "18" on the status bar (verified) | [content.md](content.md) | `env_f2` ... `env_f21` | shown |
| World and navigation | Pushwall secrets | Some walls slide when used, opening secret rooms (counted in the secret ratio) | Space | floor 1: 5 pushwalls (sodmap); one opened gives secret 1 (RAM) | | `08_pushwall`, `09_ammo_room` | shown |
| World and navigation | Elevators | Space on the switch ends the floor | Space | (verified `tally_floor1`) | | `elevator`, `tally_floor1` | shown |
| World and navigation | Secret elevators | A switch on floors 4 and 12 leads to the secret floors 19 and 20 | Space | tile positions from the map (sodmap) | | `env_f19`, `env_f20` | described (the switch looks like `elevator`) |
| Goals and gating | Floor tally | Time against par, kill/secret/treasure ratios, bonus | key | time 01:47 over par 01:30 gives bonus 0 (verified) | | `tally_floor1` | shown |
| Goals and gating | Victory | Killing the Angel of Death ends the game: B.J. collapses, You Win! with total time and averages, end pages | keys | averages divide the sum of the 20 floor records by 14 (RAM: 945/14 = 67%); total time sums all 20 (verified 66:12) | [findings.md](findings.md) | `angel_hit`, `bj_collapsed`, `victory_win`, `end_text` | shown |
| Chance | Hits and damage rolls | To-hit and damage are random and follow the frame timing | none | other waits gave other damage series (verified) | | `face_9` | shown |
| Failure and recovery | Death and lives | At 0% the view dissolves red; the floor restarts with pistol, 8 ammo, 100% | none | (verified `face_19` to `face_28`); lives counter stayed at 3 after the death (RAM, see findings) | [findings.md](findings.md) | `face_19`, `face_22`, `face_25`, `face_28` | shown |
| Failure and recovery | Out of lives / end of game | High Scores with name entry when the score qualifies | type a name, Enter | entry at 288150 above the id staff's 10000 (verified) | | `highscore_entry`, `highscore_ryz` | shown |
| Saving and sessions | Save and load | Save anywhere in 10 named slots from the Options menu | Esc, Save Game, type | slot 1 "Floor 1 treasure" (verified, save `01_start`) | | `22_slots`, `23_slot_name`, `24_saved`, `menu_load` | shown |
| Pacing and difficulty | Skill levels | Four skills set enemy numbers and toughness | menu | Angel of Death hit points 1650 on skill 2 (RAM) | | `menu_difficulty`, `menu_difficulty_daddy`, `menu_difficulty_hurt`, `menu_difficulty_death` | shown |
| Pacing and difficulty | Cheats and debug | M+L+I fills health/ammo/keys and gives the chain gun (and spoils the high score); `debugmode` adds god, warp, coordinates | keys | (verified) | playbook | `cheat_mli`, `debug_keys`, `debug_god`, `debug_warp`, `debug_coords` | shown |

## 3. How the systems feed each other
- Fights spend ammo and health; kills drop clips; treasure and kills raise the score, which buys extra lives.
- Exploring (pushwalls) gives ammo, food and treasure and raises the tally ratios, which pay a bonus.
- Keys gate parts of a floor; the Spear gates the last floor; the Angel gates the ending.
- Death resets the weapon and ammo, so a life lost late costs firepower for the rest of the floor.

## Open questions
- Exact damage formula per enemy and distance (only one series measured).
- Why the lives counter did not fall after a death in `TGFIGHT` (findings).
