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
| Opponents | Grunt, Rottweiler seen; more in later levels (source) | 2 | - |
| Items | shells, backpack, Grenade Launcher in the demo | 3 | - |
| Equipment | weapons only (axe, shotgun at the start) | shotgun | - |
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

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Grunt | E1M1 corridor and yard | human soldier with a shotgun | shoots from range, 12 health per hit on Normal (RAM); two shotgun hits kill it; drops a backpack | [20](../shots/start/quake_dos_na_20_gameplay_e1m1_door_grunt.start.png) [21](../shots/start/quake_dos_na_21_battle_e1m1_grunt_hit.start.png) [22](../shots/start/quake_dos_na_22_battle_e1m1_grunt_dead.start.png) [26](../shots/start/quake_dos_na_26_battle_e1m1_yard_fire.start.png) |
| Rottweiler | E1M1 yard | dog | runs in to bite (map data; not clearly in frame) | [25](../shots/start/quake_dos_na_25_battle_e1m1_yard_attack.start.png) |

## 4. Items and equipment
A spread over types and tiers; the special ones (quest items, cursed, charged) marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Shells | ammunition | boxes, backpacks | shotgun ammunition | [03](../shots/start/quake_dos_na_03_title_demo_start.start.png) [04](../shots/start/quake_dos_na_04_title_demo_play.start.png) |
| Backpack | ammunition | dead Grunt | holds the Grunt's ammunition (source; not picked up here) | [23](../shots/start/quake_dos_na_23_gameplay_e1m1_backpack.start.png) |
| Shotgun | weapon | start | one shell per shot, spread | [21](../shots/start/quake_dos_na_21_battle_e1m1_grunt_hit.start.png) |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|

## 6. Characters and people
Playable classes or characters, and the people of the world (shopkeepers, quest givers, rulers).

| Who | Role | Where | Shots |
|---|---|---|---|

## Open questions
What exists but was not seen, and how it could be reached.
