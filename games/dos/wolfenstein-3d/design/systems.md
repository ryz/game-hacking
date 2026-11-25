# Wolfenstein 3D (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The player starts a floor with what was carried out of the last one, walks the tile-grid corridors, opens
sliding doors, shoots the guards, dogs, SS, officers and mutants that see or hear him, and picks up ammunition,
food, first aid, treasure and keys (verified: start set, `e1m1_start` to `21_machine_gun`). Each floor ends at
an elevator switch, followed by a tally of time, kills, secrets and treasure (verified: `tally_floor1`). The
ninth floor of each episode holds a boss; killing it and reaching the exit wins the episode (verified:
`boss_hans`, `victory_run`). Between loops the weapons, ammunition, score and lives carry over; health and keys
matter only within a floor (keys) or until the next pickup (health) (source: game manual knowledge).

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move and turn | Walk forward/back, turn left/right on a free (non-tile-locked) position over a tile grid | W/S, A/D (this bundle), Alt strafe, Shift run | 0.08 tile per frame walking; 1.75 degrees per frame turning (RAM) | playbook Controls | `e1m1_start`, `env_e2m1` | shown |
| Player verbs | Fire | Uses the weapon in hand; held fire repeats for the machine gun and chain gun | Ctrl | pistol 1 bullet per shot (verified: ammo 8 to 5 in `14_guard_fire`) | 3.1 | `weapon_pistol`, `weapon_machine_gun`, `weapon_chain_gun`, `weapon_knife` | shown |
| Player verbs | Use (doors, pushwalls, switch) | Space opens the door ahead, pushes a secret wall, flips the elevator switch | Space | door opens in about 60 frames; pushwall slides 2 tiles in about 256 frames (verified) | 3.4 | `11_door_open`, `21_pushwall`, `elevator` | shown |
| Player verbs | Weapon select | Number keys pick any weapon already owned | 1-4 | knife, pistol, machine gun, chain gun (verified) | 3.1 | `hud`, `weapon_knife` | shown |
| Characters and progression | Score and extra lives | Points for kills and treasure; an extra life every 40000 points | none | guard 100, officer 400, mutant 700, Hans Grosse 5000, cross 100 (verified: score on the status bar); extra life at 40000 (RAM) | 3.2 | `15_guard_dead`, `enemy_officer_dies`, `enemy_mutant_dies`, `e1m9_exit`, `treasure_pickup` | shown |
| Characters and progression | Weapons carried | The best weapon found stays for the rest of the game (until death) | walk over it | start: knife and pistol; machine gun and chain gun found on floors (verified: `22_secret_room`, `23_machine_gun`) | 3.1 | `23_machine_gun` | shown |
| Resources and economy | Ammunition | One shared bullet count for pistol, machine gun and chain gun, cap 99 | clips from the floor and from dead guards | start 8; clip from a guard +4 (verified: ammo 0 to 4, `20_clip`); cheat 99 (verified) | 3.1 | `20_clip`, `hud` | shown |
| Resources and economy | Health | 0-100%; food and first aid restore it, not taken at 100% | walk over items | start 100% (verified); first aid kits left lying at 100% (verified: `22_secret_room`) | 3.3 | `22_secret_room`, `damage_flash` | shown |
| Resources and economy | Treasure | Crosses, chalices, chests and crowns: points and the treasure ratio | walk over | cross 100 (verified); others: source (chalice 500, chest 1000, crown 5000) | 3.2 | `treasure_room`, `treasure_pickup` | shown |
| Conflict | Hits and damage | Every shot is a roll; damage falls with distance; a hit flashes the screen red | none | guard needed 3-4 pistol shots, the second guard 2 (verified); Hans Grosse died to about 50 chain-gun bullets (verified: ammo 99 to 49) | 3.3 | `17_guard2_hit`, `damage_flash`, `boss_hans_hit` | shown |
| Conflict | Death of an enemy | A killed enemy falls, leaves a body and, for guards and SS, a clip or weapon | none | (verified: `18_guard2_falls`, `20_clip`) | 3.2 | `18_guard2_falls`, `enemy_mutant_dies`, `enemy_officer_dies` | shown |
| Opponents | Regular enemies | Guard, dog, SS, officer, mutant: stand or patrol until they see or hear the player, then attack | none | 5 kinds (verified: map data) | [content.md](content.md) 3 | `13_hall_guard`, `enemy_dogs`, `enemy_ss`, `enemy_mutant_fire`, `enemy_guard_fires` | shown |
| Opponents | Alerting | Gunfire is heard through open space; enemies behind closed doors stay unaware | none | a teleported player was ignored until he shot the boss (verified: `boss_otto` route) | 3.3 | `boss_otto`, `enemy_ss` | shown |
| Opponents | Bosses | One per episode on floor 9, many hit points, chain guns, rockets or syringes | none | 6 bosses (verified: map data) | [content.md](content.md) 3 | `boss_hans`, `boss_schabbs`, `boss_hitler`, `boss_otto`, `boss_gretel`, `boss_fett` | shown |
| Items and equipment | Pickups | Food, first aid, ammo clips, weapons, keys, treasure, extra-life spheres: taken by walking over them | walk over | (verified for clips, machine gun, key, cross) | 3.1 | `key_gold_taken`, `23_machine_gun`, `treasure_pickup` | shown |
| Abilities and magic | none | No spells or abilities; the cheats and debug keys stand outside the game rules | | | 3.6 | none: the game has no abilities | described |
| World and navigation | Floors and episodes | 6 episodes of 9 floors plus a secret floor; any episode can be started from the menu | menu | 60 maps (verified: map data) | playbook Game structure | `menu_episodes`, `env_e1m3`, `env_e6m6` | shown |
| World and navigation | Doors and locks | Sliding doors open with Space; gold and silver doors need the key of their colour | Space | (verified: `door_gold`) | 3.4 | `door_gold`, `11_door_open` | shown |
| World and navigation | Secrets (pushwalls) | A wall pushed with Space slides back 2 tiles and opens a hidden room; counted in the secret ratio | Space | E1M1 has 5 (verified: map data) | 3.4 | `21_pushwall`, `22_secret_room` | shown |
| Goals and gating | Floor exit | The elevator switch ends the floor; the tally follows | Space | (verified) | 3.5 | `elevator`, `tally_floor1` | shown |
| Goals and gating | Keys | The gold key opens gold doors on its floor; on boss floors the boss drops it | walk over | (verified: `key_gold_taken`; Hans's gold door `e1m9_exit`) | 3.4 | `key_gold`, `key_gold_taken`, `e1m9_exit` | shown |
| Goals and gating | Episode end | After the boss, the exit tile starts the run out of the castle, the "You Win!" screen and the end text | walk | (verified) | 3.5 | `victory_run`, `victory_win`, `episode_end_text`, `episode_end_text_2` | shown |
| Goals and gating | Floor tally | Bonus for beating par time, plus ratios of kills, secrets and treasure | key to continue | bonus 500 points per second under par (computed: 43000 for 4 s against 1:30); 0 over par (verified) | 3.5 | `tally_floor1` | shown |
| Chance | Random hits | Hits, damage and enemy shots are rolled; drops are fixed | none | guards fell after 2 to 4 pistol shots (verified) | 3.3 | `14_guard_fire` | shown |
| Failure and recovery | Death and lives | At 0% health the view flashes red and dissolves; a life is lost and the floor restarts | none | 3 lives at the start (verified) | 3.7 | `damage_flash`, `death_fizzle` | shown |
| Failure and recovery | Out of lives | No game-over screen: the High Scores table, with name entry when the score qualifies | type a name, Enter | entry at 12650 above the 10000 of the id staff (verified) | 3.7 | `highscore_entry`, `highscore_ryz` | shown |
| Saving and sessions | Save and load | Save anywhere from the in-game Options menu, 10 named slots | Esc, Save Game, type a name | (verified) | 3.8 | `28_save_slots`, `29_save_name`, `menu_load` | shown |
| Pacing and difficulty | Skill levels | Four skills decide which enemies appear and how hard they hit | menu | E1M1 has 20 enemies at "Bring 'em on!" (verified: map data) | 3.9 | `menu_difficulty` | shown |
| Pacing and difficulty | Cheats and debug | M+L+I gives full health, ammo, keys and weapons; the goobers debug keys give god mode, warp, coordinates | M+L+I; Tab+G/W/F | (verified) | 3.6 | `cheat_mli`, `debug_on`, `debug_god`, `debug_warp`, `debug_coords` | shown |
| Pacing and difficulty | Attract mode | Title, credits, high scores and a recorded demo loop until a key is pressed | any key | demo on floor 38 (E4M8) (verified) | 3.10 | `demo`, `credits_id`, `high_scores` | shown |

## 3. Details
### 3.1 Weapons and ammunition
Four weapons: knife (no ammunition, must stand next to the enemy), pistol (single shots), machine gun and
chain gun (held fire, the chain gun about twice as fast) (verified: `weapon_knife`, `weapon_pistol`,
`weapon_machine_gun`, `weapon_chain_gun`). All guns share one bullet count, at most 99 (verified: MLI gives 99).
A 300-frame burst of the chain gun spent 50 bullets, about one bullet per 6 frames (RAM: ammo 99 to 49).
Killed guards drop a clip; one clip gave 4 bullets (verified: `20_clip`).

### 3.2 Score
Kill points seen on the status bar: guard 100, officer 400, mutant 700, Hans Grosse 5000 (verified); dog and SS
not measured (source: 200 and 500). Cross 100 (verified: `treasure_pickup`). An extra life every 40000 points
(RAM: the next-extra-life value starts at 40000).

### 3.3 Combat
Shots hit by chance; the screen flashes red when the player is hit (verified: `damage_flash`,
`boss_hans_hit`). Enemies wake when they see or hear the player; gunfire in an open hall wakes the others
(verified: start set, the hall guard). A player put next to a boss by a debug teleport was ignored until he
fired at it (verified: `boss_otto` and `boss_schabbs` routes) (inferred: the boss had not been told the player's
area was connected to his).

### 3.4 Doors, locks and secrets
Doors slide open with Space and close again after about 5 seconds (verified). Gold and silver doors need their
key (verified: `door_gold` without a key, opened on E1M9 with one). Pushwalls are ordinary-looking walls
(often a picture) that slide back 2 tiles (verified: `21_pushwall`).

### 3.5 Ending a floor and an episode
The elevator switch (Space) ends the floor (verified: `elevator`). The tally shows bonus, time against par and
the three ratios as percentages of kills, secrets and treasure found (verified: 12 of 20 kills = 60%, 2 of 5
secrets = 40%, 9 of 23 treasure = 39%, `tally_floor1`; integer percentages, rounded down) (RAM). On a boss floor
the exit tile behind the boss's gold door starts the episode end: B.J. runs out (`victory_run`), "You Win!"
with total time and average ratios and a code (`victory_win`), then two pages of end text
(`episode_end_text`, `episode_end_text_2`) (verified).

### 3.6 Cheats and debug keys
M+L+I (held together): 100% health, 99 ammunition, both keys, all weapons, with a warning that the score is
"basically eliminated" (verified: `cheat_mli`; the score was set to 0). Start parameter `goobers` plus Left
Shift+Alt+Backspace unlock the debug keys (verified: `debug_on`): Tab+G god mode, Tab+W warp, Tab+F
coordinates, Tab+I free items, Tab+E end the floor (verified).

### 3.7 Death and the end of a game
At 0% the screen turns red and the view dissolves in red pixels (verified: `damage_flash`, `death_fizzle`).
With lives left the floor restarts; with none the game goes to the High Scores, where a qualifying score gets a
name line (verified: `highscore_entry`, `highscore_ryz`). There is no separate game-over picture (verified).

### 3.8 Saving
Ten slots, each named by the player, saved from the Options menu in play (verified: start set
`28_save_slots` to `30_saved`).

### 3.9 Difficulty
Four skills: "Can I play, Daddy?", "Don't hurt me.", "Bring 'em on!", "I am Death incarnate!" (verified:
`menu_difficulty`). Each enemy on a map is marked for the lowest skill it appears on (verified: map data).

### 3.10 Attract mode
Title, id credits, High Scores, a recorded demo (verified: `title_screen`, `credits_id`, `high_scores`, `demo`).

## 4. How the systems feed each other
Kills and treasure give score; score gives extra lives every 40000; lives buy retries of a floor. Guards drop
ammunition, so fighting pays for fighting; secrets hold weapons (the machine gun in E1M1) and treasure. Keys
gate the way to the elevator and, on boss floors, the exit. The tally rewards speed (par bonus) and
thoroughness (ratios), two goals that pull against each other.

## Open questions
- Damage per weapon and distance, enemy hit points: not measured (source code knowledge only).
- Silver key door not shown; extra-life sphere not picked up on camera.
- Chain gun and machine gun fire rates measured only roughly.
