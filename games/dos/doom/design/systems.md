# Doom (DOS, registered 1.1) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/doom`.
Shot ids are from the `main` set (`../shots/main/index.md`) unless marked `start` (`../shots/start/index.md`).
The rules are those of The Ultimate Doom 1.9 (`games/dos/ultimate-doom/design/systems.md`) unless a row says
what 1.1 does differently.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The marine enters a map, moves through rooms and corridors in real time, opens doors and presses switches,
shoots the monsters that wake and come at him, and picks up weapons, ammunition, health, armor and power-ups
**(verified, start set E1M1)**. The exit switch ends the map with a tally of kills, items, secrets and time;
the next map loads with health, armor, weapons and ammunition carried over **(verified, start `20_tally` to
`23_e1m2_start`: E1M2 began at 100% health and 190% armor)**. Monsters get tougher and maps larger from
episode to episode; map 8 of each of the three episodes holds a boss and ends the episode with an end text
**(verified, `ending_e1`, `ending_e2`, `ending_e3`)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move, turn | Arrows move and turn; right Shift runs; Alt + arrow strafes | arrows, rshift, alt | turns land within 2 degrees of 1.9's turn table (verified, dnav routes) | playbook Controls | start `09_env_corridor`, `env_e2m1` | shown |
| Player verbs | Fire | Ctrl fires the weapon in hand; held for automatic fire | ctrl | see weapons | content.md | `weapon_pistol`, `weapon_chaingun` | shown |
| Player verbs | Use | Space opens doors, presses switches and starts lifts within reach | space | | | start `10_door`, `19_exit_room` | shown |
| Player verbs | Weapon select | Keys 1-7; key 1 gives the chainsaw when it is owned, the fist only otherwise (verified: with idkfa the first fist route showed the chainsaw) | 1-7 | 8 weapons in 7 slots | findings.md | `weapon_fist`, `weapon_chainsaw` | shown |
| Player verbs | Automap | Tab shows the explored map; the computer map shows all of it | tab | | interface.md | `automap_full`, `automap_things`, start `13_automap` | shown |
| Player verbs | View size | `=` and `-` grow and shrink the 3D window; 1.1 starts with a reduced window in a border, one `=` gives the full-width view over the status bar (verified) | =, - | | interface.md | `view_reduced`, start `07_e1m1_start`, `08_view_full` | shown |
| Player verbs | Cheats | iddqd, idkfa, idbehold v s i r a l, iddt, idspispopd, idchoppers, idmypos, idclev work; idclip does nothing (verified) | typed | | playbook Shortcuts | `cheat_god`, `cheat_idkfa`, `automap_things` | shown |
| Characters and progression | none | No statistics or levels; progress is the weapons and ammunition carried from map to map (verified, E1M1 to E1M2) | | | | none: no character system | described |
| Resources and economy | Health | 0-100%, more with bonuses and soulspheres; 0 is death | pickups | | | `face_100`, `face_67`, start `12_hit` | shown |
| Resources and economy | Armor | Green armor sets 100%, MegaArmor 200% | pickups | 100% / 200% (verified `pickup_armor`, `pickup_megaarmor`); MegaArmor in the E1M1 pool showed 196% after the walk out (verified start `16_blue_armor`) | | `pickup_armor`, `pickup_megaarmor`, start `16_blue_armor` | shown |
| Resources and economy | Ammunition | Bullets, shells, rockets, cells; caps 200/50/50/300 | pickups, idkfa | BFG uses 40 cells a shot (verified: 212 -> 172, `weapon_bfg_blast`); plasma 1 cell per bolt (verified, `weapon_plasma` 212 -> 203) | | `weapon_bfg_blast`, `weapon_plasma` | shown |
| Conflict | Hitscan and projectiles | Pistol, shotgun, chaingun hit along a line at once; rockets, plasma and BFG balls fly and burst | fire | | | `weapon_shotgun`, `weapon_rocket`, `weapon_plasma` | shown |
| Conflict | Melee | Fist and chainsaw reach only adjacent monsters; berserk strengthens the fist and tints the view red | fire at contact | | | `weapon_fist`, `weapon_chainsaw`, `power_berserk` | shown |
| Conflict | BFG spray | The BFG ball bursts and then strikes everything in front of the marine with tracers; the Spider Mastermind died from a spray while the view was turned away (verified, `boss_spider_tracers` then `boss_spider_dead`) | fire | Spider 3000 -> 2080 -> 1016 -> 210 -> dead over seven BFG shots, damage landing one round late (RAM) | findings.md | `boss_spider_tracers`, `boss_spider_bfg` | shown |
| Conflict | Pain flash and face | Every hit tints the view red and changes the face; five health bands and a dead face | none | seen at 100, 67, 40, 25, 16, 7, 0 in one fist-only fight on E1M3 (verified) | interface.md | `face_100`, `face_67`, `face_40`, `face_25`, `face_16`, `face_7`, `death_floor` | shown |
| Opponents | Monster roster | Ten kinds from zombieman to Spider Mastermind, each with its own attack | | Baron 1000, Cyberdemon 4000, Spider 3000 health (RAM) | content.md | `mon_sguys`, `mon_imp_fireball`, `mon_cacodemon`, `mon_lostsoul`, `boss_barons` | shown |
| Opponents | Waking and hunting | Monsters wake when they see the marine or hear a shot and come at him | | | | `mon_sguys`, `boss_barons` | shown |
| Items and equipment | Weapons | Eight weapons in seven slots, kept until death | 1-7 | | content.md | `weapon_fist` ... `weapon_bfg_blast` | shown |
| Items and equipment | Power-ups | Invulnerability (inverse grey), berserk (red), partial invisibility (weapon as fuzz), radiation suit (green), computer map, light amplification | pickups, idbehold | | content.md | `power_invuln`, `power_berserk`, `power_invis`, `power_radsuit`, `power_liteamp`, `automap_full` | shown |
| Abilities and magic | none | No spells or abilities beyond weapons and power-ups | | | | none: no magic | described |
| World and navigation | Maps and episodes | Three episodes of eight maps plus a secret ninth: 27 maps (verified, WAD) | | | playbook | `env_e1m1`, `env_e2m1`, `env_e2m2`, `env_e3m1`, `env_e3m8` | shown |
| World and navigation | Doors, lifts, walk triggers | Doors open with Space; the E1M8 lift lowers on use; crossing a line opens the barons' closets | space, walking | | | `boss_barons`, start `10_door` | shown |
| World and navigation | Hurting floors | Nukage and lava hurt without a radiation suit | | MegaArmor walk in the E1M1 pool: 86% -> 70% health (verified, checkpoints s_e1m1_zigzag -> s_e1m1_armor) | | `power_radsuit`, start `16_blue_armor` | shown |
| World and navigation | Secrets | Hidden areas counted on the tally; E1M1 has 2 in 1.1 (1.9: 3) | | Secret 50% after one (verified start `21_tally_done`) | | start `21_tally_done` | shown |
| Goals and gating | Exits, tally | Each map ends at its exit switch with Kills, Items, Secret, Time and Par | space | E1M1 par 30 s (verified) | | start `20_tally`, `21_tally_done`, `22_entering` | shown |
| Goals and gating | E1M8 ending | The barons' death opens the way; the episode ends only when the marine steps through the teleporter ring into the dark exit room, which takes 10% health (verified: 100 -> 90) | walking | text complete 2700 frames after the teleport, order page at 3300 (verified) | findings.md | `boss_barons`, `ending_e1`, `ending_e1_order` | shown |
| Goals and gating | E2M8 and E3M8 endings | The episode ends by itself when the boss's death animation finishes: no tally, the screen melts straight into the end text (verified) | | E2 text complete +3000 frames, picture +3600; E3 text +3300, rabbit picture +3600, scroll +4200 (verified) | | `boss_cyber_dies`, `ending_e2`, `ending_e2_deimos`, `boss_spider_dead`, `ending_e3`, `ending_e3_bunny`, `ending_e3_scroll` | shown |
| Goals and gating | Keys | Blue, yellow, red keycards and skull keys open coloured doors (source); idkfa fills all six slots (verified) | | | | `cheat_idkfa` | shown |
| Chance | Damage rolls | Every attack rolls damage; the random table restarts with each level, so the same keys repeat a fight exactly (verified: every route reproduces) | timing | | | `face_40` | shown |
| Failure and recovery | Death | At 0% the view drops to the floor and the face turns to the dead face; Space restarts the map with a pistol (source) | space | | | `death_floor` | shown |
| Saving and sessions | Save anywhere | Six named slots in `C:\DOOMDATA\` (1.1; 1.9 saves into the game folder); Save Game outside a game is refused | Esc, Save Game, F2 | 6 slots (verified) | | start `28_slots`, `29_typing_name`, `30_saved`, `load_empty`, `save_refused` | shown |
| Pacing and difficulty | Skill levels | Four skills in 1.1 (no Nightmare!); Hurt me plenty preselected (verified) | menu | skill 3 E1M1: 6 monsters (verified) | | `menu_skill`, `menu_skill_itytd`, `menu_skill_hntr`, `menu_skill_uv` | shown |
| Pacing and difficulty | Episode choice | Three episodes from the start in the registered 1.1 (verified) | menu | | | `menu_episode` | shown |

## 3. How the systems feed each other
- Exploring finds weapons and ammunition -> stronger weapons kill tougher monsters faster -> fewer hits taken.
- Health and armor lie through the map -> the face and the health number tell when to look for them.
- Secrets hold the best items (MegaArmor, shotgun on E1M1) -> the tally rewards finding them.
- Carry-over between maps -> a careless map leaves the next one harder.

## Open questions
- Key doors, the secret ninth maps and their tallies: not captured.
- Sound: all runs use `-nosound`; the sound cards were not tried.
