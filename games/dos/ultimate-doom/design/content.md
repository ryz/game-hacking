# The Ultimate Doom (DOS) - content (variety lens)

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
| Environments | 36 maps in 4 episodes: techbases, Deimos, Hell (verified, WAD) | 9 | playbook "Maps" |
| Opponents | 10 monster kinds (verified, WAD thing list) | 9 | `games/dos/ultimate-doom/tools/wadmap.py` |
| Items | health, armor, ammunition, power-ups, keys | 9 | |
| Equipment | 8 weapons | 8 | |
| Abilities / spells | none | | |
| Characters and people | the marine only | 1 | |

## 2. Environments
One row per distinct look, not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Hangar techbase | E1M1 | grey tech walls, brown wood panels, nukage pool | `env_e1m1`, `pickup_megaarmor` |
| Computer rooms | E1M1 | blue computer walls, red ceiling lights | `weapon_pistol` (start set too), `mon_gibs` |
| Phobos outdoors | E1M1, E1M8 | brown hills sky, green nukage | start `18_env_yard` |
| Deimos base | E2M1, E2M2 | dark corridors, lit tech ceilings | `env_e2m1`, `env_e2m2` |
| Tower of Babel | E2M8 | open grey arena under a red sky | `boss_cyberdemon`, `boss_cyber_close`, `boss_cyber_dies` |
| Hell marble | E3M3 | green marble corridors with skull lamps | `env_e3m3`, `mon_demon` |
| Hell flesh and lava | E3M3, E3M1 | red walls, lava floors, red skies | `mon_cacodemon`, `weapon_rocket` |
| Dis | E3M8 | green ground, red sky, the Spider's arena | `boss_spider`, `boss_spider_dies` |
| Unto the Cruel (name: source) | E4M8 | wooden fort walls under an orange sky, the Spider's yard | `boss_spider_e4_dies` |
| Thy Flesh Consumed | E4M1, E4M6 | dark brick halls; rocky ground under an orange sky with a dead tree | `env_e4m1`, `env_e4m6` |
| Phobos Anomaly | E1M8 | wood and stone hall before the baron closets | `boss_barons` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Zombieman | E1M1 on | former human, rifle | hitscan shots; drops a clip | `mon_gibs`, `face_16` |
| Shotgun guy | E1M3 on | former human, black armour | three-pellet shotgun | `weapon_shotgun`, `face_55`, `face_28` |
| Imp | E1M1 on | brown, spiked | throws fireballs, claws up close | `mon_imp_fireball`, `weapon_rocket`, `face_16` |
| Demon | E1M2 on | pink, horned | charges and bites | `mon_demon`, `weapon_fist`, `weapon_pistol`, `weapon_plasma` |
| Spectre | E1M3 on | a demon drawn as fuzz | same as demon, hard to see | none: not caught in view this run |
| Lost soul | E2 on | flaming skull | flies at the marine | `weapon_chainsaw`, `weapon_chaingun` |
| Cacodemon | E2 on | red floating ball, one eye | spits lightning balls | `mon_cacodemon` |
| Baron of Hell (boss of E1) | E1M8, later as ordinary monster | horned, goat legs | green fireballs, claws; 1000 health (RAM) | `boss_barons`, `boss_baron_fireball`, `death_barons` |
| Cyberdemon (boss of E2) | E2M8 | huge, rocket arm | fires rockets; 4000 health (RAM), immune to splash; killed with 9 BFG balls and 4 rockets (RAM) | `boss_cyberdemon`, `boss_cyber_close`, `boss_cyber_dies` |
| Spider Mastermind (boss of E3) | E3M8 | brain on mechanical legs | super chaingun; 3000 health (RAM); 3000 -> 2032 -> 643 -> 0 under BFG balls (RAM); also the boss of E4M8 | `boss_spider`, `boss_spider_bfg`, `boss_spider_dies`, `boss_spider_e4_dies` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Fist | weapon, slot 1 | start | melee; berserk boosts it | `weapon_fist` |
| Chainsaw | weapon, slot 1 | E1M2 and later maps | continuous melee | `weapon_chainsaw` |
| Pistol | weapon, slot 2 | start | single bullets | `weapon_pistol`, start `10_zombie_fires` |
| Shotgun | weapon, slot 3 | E1M1 secret, zombies drop it | seven pellets | `weapon_shotgun`, `mon_imp_fireball` |
| Chaingun | weapon, slot 4 | maps | rapid bullets | `weapon_chaingun` |
| Rocket launcher | weapon, slot 5 | maps | rockets with blast damage; gibs | `weapon_rocket`, `mon_gibs` |
| Plasma rifle | weapon, slot 6 | E2 on | rapid plasma bolts, uses cells | `weapon_plasma` |
| BFG9000 | weapon, slot 7 | E3M3 and later | huge green ball, 40 cells | `weapon_bfg_blast`, `boss_spider_bfg` |
| Green armor | armor | maps | 100% armor | `pickup_armor` |
| MegaArmor | armor | E1M1 nukage pool and later | 200% armor | `pickup_megaarmor`, start `19_megaarmor` |
| Medikit | health | maps | +25% | start `20_medikit` |
| Soulsphere | power-up | secrets | +100% health | `item_soulsphere` |
| Invulnerability | power-up | maps | no damage, inverse grey view | `power_invuln` |
| Berserk | power-up | maps | strong fist, red view, full health | `power_berserk`, `weapon_fist` |
| Partial invisibility | power-up | maps | monsters miss more; weapon drawn as fuzz | `power_invis` |
| Radiation suit | power-up | maps | no floor damage, green view | `power_radsuit` |
| Computer map | power-up | maps | whole map on the automap | `automap_full` |
| Light amplification | power-up | maps | full brightness | `power_liteamp` |
| Box of shells | ammunition | E1M1 secret | +20 shells | start `17_secret_ammo` |

## 5. Abilities and spells
None: the game has weapons and power-ups only.

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| The marine | the player, seen as the face on the status bar and on the title picture | everywhere | `title_screen`, `face_88` |

## Open questions
- Spectre in view, key doors and keycards, the E2-E4 end texts and the secret maps were not shot this run.
