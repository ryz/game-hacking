# The Ultimate Doom (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultimate-doom`.
Shot ids are from the `main` set (`../shots/main/index.md`) unless marked `start` (`../shots/start/index.md`).

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The marine enters a map, moves through rooms and corridors in real time, opens doors and presses switches,
shoots the monsters that wake and come at him, and picks up weapons, ammunition, health, armor and power-ups
lying around **(verified, start set E1M1)**. Reaching the exit (a switch or a walk-over line) ends the map with
a tally of kills, items, secrets and time, then the next map loads with health, armor, weapons and ammunition
carried over **(verified, start `24_tally` to `27_e1m2_start`)**. Between loops the monsters get tougher and
more numerous, the weapons stronger, the maps larger and darker; each episode ends on a boss map and an end
text **(verified, `ending_e1`)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move, turn, run, strafe | Arrows move and turn; right Shift runs; Alt + arrow strafes | arrows, rshift, alt | walk about 3.7 units per frame, run about twice that; turn 1.76 then 3.52 degrees per tic (verified, playbook Controls) | playbook | `env_e1m1`, start `08_env_corridor` | shown |
| Player verbs | Fire | Ctrl fires the weapon in hand; hold for automatic fire | ctrl | see weapons row | | `weapon_pistol`, `weapon_chaingun` | shown |
| Player verbs | Use | Space opens doors, presses switches and starts lifts within 64 units of the line | space | 64 units (verified: opened from 16, failed from 76) | | start `09_door`, `23_exit_room` | shown |
| Player verbs | Weapon select | Keys 1-7 pick a weapon slot; 1 is fist or chainsaw | 1-7 | 8 weapons | content.md | `weapon_fist`, `weapon_chainsaw` | shown |
| Player verbs | Automap | Tab shows the map of the explored part of the level | tab, F, M, C, +, -, 0 | | interface.md | `automap_full`, start `13_automap` | shown |
| Characters and progression | none | The marine has no statistics or levels; progress is the weapons and ammunition carried from map to map **(verified, E1M1 to E1M2 carry-over)** | | | | none: no character system | described |
| Resources and economy | Health | 0-100%, up to 200% with soulspheres and health bonuses; 0 is death | pickups | stimpack 10, medikit 25 (source); medikit seen 30 -> 52 with a pickup in between (verified start `20_medikit`) | | `face_88`, start `20_medikit` | shown |
| Resources and economy | Armor | Green armor sets 100%, MegaArmor (blue) 200%; armor absorbs a third (green) or half (blue) of damage | pickups | 100% / 200% (verified `pickup_armor`, `pickup_megaarmor`); absorption (source: id source code) | | `pickup_armor`, `pickup_megaarmor`, start `19_megaarmor` | shown |
| Resources and economy | Ammunition | Four kinds: bullets (pistol, chaingun), shells, rockets, cells (plasma, BFG); caps 200/50/50/300, doubled by a backpack | pickups | caps on the status bar (verified); BFG uses 40 cells a shot (verified: 212 -> 172 cells, `weapon_bfg_blast`) | | `weapon_bfg_blast`, start `17_secret_ammo` | shown |
| Conflict | Hitscan and projectiles | Pistol, shotgun, chaingun hit at once along a line; rockets, plasma and BFG balls fly and burst | fire | | | `weapon_shotgun`, `weapon_rocket`, `weapon_plasma` | shown |
| Conflict | Melee | Fist and chainsaw reach only adjacent monsters; berserk multiplies fist damage by ten (source) and tints the view red | fire at contact | | | `weapon_fist`, `weapon_chainsaw`, `power_berserk` | shown |
| Conflict | Pain flash and face | Every hit tints the view red and changes the face; the face shows five health bands (80+, 60-79, 40-59, 20-39, 1-19) and a dead face | none | bands (source: id source; seen at 88, 55, 28, 16, 4 and 0: verified) | | `face_88`, `face_55`, `face_28`, `face_16`, `face_4`, `death_floor` | shown |
| Conflict | Gibbing | A blast that takes a monster far below zero health makes it burst into gibs instead of the normal death | | | | `mon_gibs` | shown |
| Conflict | Infighting | Monsters hit by another monster's attack turn on it (source); five shotgun guys and zombiemen died in a fist-only fight on E1M3 (inferred from the kill count 5) | | | findings.md | none: not caught in a frame | described |
| Opponents | Monster roster | Ten kinds from zombieman to Spider Mastermind, each with its own attack (hitscan, fireball, bite, charge) | | hit points from the id source (zombieman 20 ... Cyberdemon 4000, verified in memory: Cyberdemon 4000, Spider 3000, Baron 1000) | content.md | `mon_demon`, `mon_imp_fireball`, `mon_cacodemon`, `boss_barons`, `boss_baron_fireball` | shown |
| Opponents | Waking | Monsters sleep until they see the marine or hear a shot in a connected area; then they hunt him | | | | `weapon_chaingun` | shown |
| Items and equipment | Weapons | Eight weapons in seven slots, picked up on the maps and kept until death | 1-7 | | content.md | `weapon_fist` ... `weapon_bfg_blast` | shown |
| Items and equipment | Power-ups | Invulnerability (inverse grey view), berserk (red), partial invisibility (weapon drawn as fuzz), radiation suit (green, no nukage damage), computer map (whole map on the automap), light amplification (full brightness) | pickups | durations from the source (invulnerability 30 s, radiation suit 60 s, light amp 120 s) | | `power_invuln`, `power_berserk`, `power_invis`, `power_radsuit`, `automap_full`, `power_liteamp` | shown |
| Items and equipment | Soulsphere | +100% health up to 200% (source) | pickup | | | `item_soulsphere` | shown |
| Abilities and magic | none | No spells or abilities beyond weapons and power-ups | | | | none: no magic | described |
| World and navigation | Maps and episodes | Four episodes of eight maps plus one secret map each, 36 maps; maps of varying floor and ceiling heights | | 36 maps (verified, WAD) | playbook | `env_e2m1`, `env_e2m2`, `env_e3m3`, `env_e4m1`, `env_e4m6` | shown |
| World and navigation | Doors, lifts, switches | Doors open with Space and close again; lifts lower when used and rise after about 3 s; walk-over lines open closets (E1M8 barons) | space, walking | lift on E1M8 raised 104 units (verified, playbook) | | `boss_barons`, start `09_door` | shown |
| World and navigation | Hurting floors | Nukage and lava hurt every second without a radiation suit | | MegaArmor pickup in the E1M1 pool cost about 15% health (verified start `19_megaarmor`) | | `power_radsuit`, `pickup_megaarmor` | shown |
| World and navigation | Secrets | Hidden areas counted on the tally; E1M1 has 3 | | Secret 33% after one (verified start `25_tally_done`) | | `tally_e1m1`, start `17_secret_ammo` | shown |
| Goals and gating | Exits and episode ends | Each map ends at its exit; map 8 ends the episode with an end text, then (E1) the id credits | | | | `tally_e1m1`, `entering_e1m2`, `ending_e1`, `credits_id` | shown |
| Goals and gating | Boss gates | E1M8 seals two Barons of Hell behind walk triggers; E2M8 ends when the Cyberdemon dies, E3M8 when the Spider Mastermind dies (source) | | | playbook | `boss_barons`, `boss_cyber_close`, `boss_spider` | shown |
| Goals and gating | Keys | Blue, yellow and red keycards and skull keys open coloured doors (source; status bar slots verified with idkfa) | | | | none: key doors not routed this run | described |
| Chance | Damage rolls | Every attack rolls its damage; Doom's random table restarts on every level, so the same keys repeat a fight exactly **(verified: routes reproduce)** | timing | | findings.md | `face_28` | shown |
| Failure and recovery | Death | At 0% the view drops to the floor and the face turns to the dead face; Space restarts the map with a pistol | space | | | `death_floor`, `death_barons` | shown |
| Saving and sessions | Save anywhere | Six named slots, any time in a map | Esc, Save Game, F2 | 6 slots (verified) | | start `31_save_menu`, `33_saved` | shown |
| Pacing and difficulty | Skill levels | Five skills; Hurt me plenty is the default; Nightmare! respawns monsters and asks for confirmation (source) | menu | | | `menu_skill` | shown |

## 3. How the systems feed each other
- Exploring finds weapons and ammunition -> stronger weapons kill tougher monsters faster -> fewer hits taken.
- Health and armor pickups are spread through the map -> the face and the health number tell when to look for them.
- Secrets hold the best items (MegaArmor, shotgun on E1M1) -> the tally rewards finding them.
- Carry-over between maps -> a careless map leaves the next one harder (E1M2 started at 19% health in the start set).

## Open questions
- Spectre in action, key doors, the E2 and E3 end texts: not captured this run (see findings: bosses took no
  damage in the routes tried).
