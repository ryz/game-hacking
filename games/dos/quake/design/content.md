# Quake (DOS, shareware 1.06) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Which kinds exist depends on the game, its genre and structure: keep the kinds this game has, drop the rest,
add its own (vehicles, tracks, puzzles, levels, minigames ...). For each kind say how many there are in total
if known, then show a sample that spans the range: early and late, common and rare, plain and strange, one of
each visual family. A complete table belongs in its own document (items.md, enemies.md) and is linked here.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | start map, hub, 8 shareware levels (map list) | base metal (E1M1), stone start halls, crypt (demo) | [playbook](../playbook.md) Game structure |
| Opponents | 9 types in the shareware maps: Grunt, Rottweiler, Ogre, Knight, Fiend, Scrag, Zombie, Shambler, Chthon (map data; no Enforcer, Death Knight, Spawn, Vore or Rotfish in Episode 1) | 8 (no Zombie close enough) | - |
| Items | ammunition (4 kinds), health, 3 armors, 4 power-ups, keys, backpacks | armors and power-ups all | - |
| Equipment | 8 weapons, all in the shareware (map data, verified in hand) | 8 | - |
| Abilities / spells | none | - | - |
| Characters and people | the player only | - | - |

## 2. Environments
One row per distinct look or place type (tile or wall set, terrain, interior, special place), not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Start map halls | start map | stone halls with skill text and slipgates | [09](../shots/start/quake_dos_na_09_gameplay_start_spawn.start.png) [10](../shots/start/quake_dos_na_10_gameplay_normal_hall.start.png) |
| Episode hub | start map | stone hall with four episode gates and signs | [11](../shots/start/quake_dos_na_11_gameplay_hub_arrival.start.png) [12](../shots/start/quake_dos_na_12_gameplay_env_hub_west.start.png) [14](../shots/start/quake_dos_na_14_gameplay_hub_e1_gate.start.png) |
| Slipgate base | E1M1 | brown metal corridors, computer rooms behind windows, sliding doors | [16](../shots/start/quake_dos_na_16_gameplay_e1m1_start.start.png) [17](../shots/start/quake_dos_na_17_gameplay_env_e1m1_corridor.start.png) [18](../shots/start/quake_dos_na_18_gameplay_env_e1m1_computers.start.png) [19](../shots/start/quake_dos_na_19_gameplay_env_e1m1_ledge.start.png) |
| Outdoor yard with water | E1M1 | rock walls, crates, a water channel | [25](../shots/start/quake_dos_na_25_battle_e1m1_yard_attack.start.png) [27](../shots/start/quake_dos_na_27_battle_e1m1_yard_clear.start.png) |
| Crypt | E1M3 (demo) | dark stone, torches | [03](../shots/start/quake_dos_na_03_title_demo_start.start.png) [04](../shots/start/quake_dos_na_04_title_demo_play.start.png) |
| Crypt and stone halls | E1M3 | dark grey stone, arched doorways | [env_e1m3_crypt](../shots/main/quake_dos_na_gameplay_env_e1m3_crypt.png) [weapon_ssg](../shots/main/quake_dos_na_inventory_weapon_ssg.png) |
| Grotto | E1M4 | mossy rock, demon-face panels, water | [env_e1m4_grotto](../shots/main/quake_dos_na_gameplay_env_e1m4_grotto.png) [weapon_nailgun](../shots/main/quake_dos_na_inventory_weapon_nailgun.png) [act_scrag](../shots/main/quake_dos_na_battle_act_scrag.png) |
| Keep under open sky | E1M5 | long brick hall, purple sky | [env_e1m5_hall](../shots/main/quake_dos_na_gameplay_env_e1m5_hall.png) [weapon_sng](../shots/main/quake_dos_na_inventory_weapon_sng.png) |
| Castle | E1M2, E1M6 | wooden beams, torches, stone | [weapon_shotgun](../shots/main/quake_dos_na_inventory_weapon_shotgun.png) [weapon_gl](../shots/main/quake_dos_na_inventory_weapon_gl.png) [act_ogre](../shots/main/quake_dos_na_battle_act_ogre.png) |
| Lava halls | E1M7, E1M8 | lava pits and pools under stone | [env_e1m7_lava](../shots/main/quake_dos_na_gameplay_env_e1m7_lava.png) [env_e1m8_lava](../shots/main/quake_dos_na_gameplay_env_e1m8_lava.png) [weapon_rl](../shots/main/quake_dos_na_inventory_weapon_rl.png) [weapon_lg](../shots/main/quake_dos_na_inventory_weapon_lg.png) [power_pentagram](../shots/main/quake_dos_na_system_power_pentagram.png) |
| Slime | E1M1 | green slime pool, deadly without the Biosuit | [power_biosuit](../shots/main/quake_dos_na_system_power_biosuit.png) |

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Grunt | E1M1 corridor and yard | human soldier with a shotgun | shoots from range, 12 health per hit on Normal (RAM); two shotgun hits kill it; drops a backpack | [20](../shots/start/quake_dos_na_20_gameplay_e1m1_door_grunt.start.png) [21](../shots/start/quake_dos_na_21_battle_e1m1_grunt_hit.start.png) [22](../shots/start/quake_dos_na_22_battle_e1m1_grunt_dead.start.png) [26](../shots/start/quake_dos_na_26_battle_e1m1_yard_fire.start.png) |
| Rottweiler | E1M1 yard (start set) | dog | runs in to bite (map data; not clearly in frame) | [25](../shots/start/quake_dos_na_25_battle_e1m1_yard_attack.start.png) |
| Rottweiler | E1M1 yard | dog | runs in and bites | [act_rottweiler](../shots/main/quake_dos_na_battle_act_rottweiler.png) [fire_axe](../shots/main/quake_dos_na_battle_fire_axe.png) |
| Ogre | E1M2, E1M6 | brute with a chainsaw and a grenade launcher | chainsaw up close, grenades from range (source) | [act_ogre](../shots/main/quake_dos_na_battle_act_ogre.png) |
| Fiend | E1M3 | long-armed demon | leaps at the player from range | [act_fiend](../shots/main/quake_dos_na_battle_act_fiend.png) [fire_sng](../shots/main/quake_dos_na_battle_fire_sng.png) |
| Scrag | E1M4 | floating wraith | hovers and spits (source) | [act_scrag](../shots/main/quake_dos_na_battle_act_scrag.png) |
| Knight | E1M4 | armoured swordsman | sword in melee | [act_knight](../shots/main/quake_dos_na_battle_act_knight.png) |
| Shambler | E1M8 (Normal), E1M3/E1M5 (Hard), E1M6 | huge white beast | claws up close; raises its arms and strikes with lightning from range; lightning hits it barely (source) | [act_shambler](../shots/main/quake_dos_na_battle_act_shambler.png) [act_shambler_charge](../shots/main/quake_dos_na_battle_act_shambler_charge.png) [act_shambler_lightning](../shots/main/quake_dos_na_battle_act_shambler_lightning.png) [fire_rl](../shots/main/quake_dos_na_battle_fire_rl.png) [fire_rl_hit](../shots/main/quake_dos_na_battle_fire_rl_hit.png) [fire_lg](../shots/main/quake_dos_na_battle_fire_lg.png) [gameover](../shots/main/quake_dos_na_gameover_gameover.png) |
| Chthon (boss) | E1M7 | lava demon rising from the pit | throws lava balls; only the level's lightning traps hurt it (source) | [boss_chthon](../shots/main/quake_dos_na_boss_boss_chthon.png) [boss_chthon_lava](../shots/main/quake_dos_na_boss_boss_chthon_lava.png) |

## 4. Items and equipment
A spread over types and tiers; the special ones (quest items, cursed, charged) marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Shells | ammunition | boxes, backpacks | shotgun ammunition | [03](../shots/start/quake_dos_na_03_title_demo_start.start.png) [04](../shots/start/quake_dos_na_04_title_demo_play.start.png) |
| Backpack | ammunition | dead Grunt | holds the Grunt's ammunition (source; not picked up here) | [23](../shots/start/quake_dos_na_23_gameplay_e1m1_backpack.start.png) |
| Shotgun | weapon | start | one shell per shot, spread | [21](../shots/start/quake_dos_na_21_battle_e1m1_grunt_hit.start.png) |
| Axe, Shotgun, Double-barreled Shotgun, Nailgun, Super Nailgun | weapons | start (axe, shotgun), levels | melee; hitscan spread (1 or 2 shells); nails (1 or 2 per shot) | [weapon_axe](../shots/main/quake_dos_na_inventory_weapon_axe.png) [weapon_shotgun](../shots/main/quake_dos_na_inventory_weapon_shotgun.png) [weapon_ssg](../shots/main/quake_dos_na_inventory_weapon_ssg.png) [weapon_nailgun](../shots/main/quake_dos_na_inventory_weapon_nailgun.png) [weapon_sng](../shots/main/quake_dos_na_inventory_weapon_sng.png) [fire_axe](../shots/main/quake_dos_na_battle_fire_axe.png) [fire_shotgun](../shots/main/quake_dos_na_battle_fire_shotgun.png) [fire_ssg](../shots/main/quake_dos_na_battle_fire_ssg.png) [fire_nailgun](../shots/main/quake_dos_na_battle_fire_nailgun.png) [fire_sng](../shots/main/quake_dos_na_battle_fire_sng.png) |
| Grenade Launcher, Rocket Launcher, Thunderbolt | weapons | levels | bouncing grenades, rockets with splash (rockets), a lightning beam (cells) | [weapon_gl](../shots/main/quake_dos_na_inventory_weapon_gl.png) [weapon_rl](../shots/main/quake_dos_na_inventory_weapon_rl.png) [weapon_lg](../shots/main/quake_dos_na_inventory_weapon_lg.png) [fire_gl](../shots/main/quake_dos_na_battle_fire_gl.png) [fire_rl](../shots/main/quake_dos_na_battle_fire_rl.png) [fire_lg](../shots/main/quake_dos_na_battle_fire_lg.png) |
| Green / Yellow / Red Armor | armor | E1M1 and others; Red only as a deathmatch item on the start map | armor 100 / 150 / 200 | [armor_green](../shots/main/quake_dos_na_inventory_armor_green.png) [armor_yellow](../shots/main/quake_dos_na_hud_armor_yellow.png) [armor_red](../shots/main/quake_dos_na_inventory_armor_red.png) |
| Quad Damage, Pentagram of Protection, Ring of Shadows, Biosuit | power-ups | E1M1 (Quad, Biosuit), E1M8 (Pentagram), E1M3 (Ring) | 30 s effects, see systems | [power_quad](../shots/main/quake_dos_na_system_power_quad.png) [power_pentagram](../shots/main/quake_dos_na_system_power_pentagram.png) [power_ring](../shots/main/quake_dos_na_system_power_ring.png) [power_biosuit](../shots/main/quake_dos_na_system_power_biosuit.png) |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|

## 6. Characters and people
Playable classes or characters, and the people of the world (shopkeepers, quest givers, rulers).

| Who | Role | Where | Shots |
|---|---|---|---|

## Open questions
What exists but was not seen, and how it could be reached.
