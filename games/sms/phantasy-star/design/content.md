# Phantasy Star - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.
Coverage: the early game only (Camineet, the fields around it, the first cave).

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | three planets, many towns, caves, towers **(source)** | Camineet, Palma fields, one cave, one passage | section 2 |
| Opponents | many monsters **(source)** | 3 | section 3 |
| Items | 64 item names in the item table **(RAM: ids 01-40, playbook)** | 9 | playbook item table |
| Equipment | weapons, armour, shields among those **(RAM)** | 6 | playbook item table |
| Abilities / spells | spells for Alis, Myau, Noah **(source)** | none yet | section 5 |
| Characters and people | 4 heroes, townspeople, shopkeepers, priests **(source)** | Alis, Nero, robotcops, 3 shopkeepers, priest, townspeople | section 6 |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Town (Camineet) | Palma | walled, stone paths, domed houses, SHOP buildings **(verified)** | `camineet_start`, `camineet_shops`, `camineet_gate` |
| Town interiors | Camineet | a room picture per building type: house, shops (three looks), church **(verified)** | `alis_home`, `shop_secondhand`, `shop_food`, `shop_armory`, `camineet_church` |
| Palma surface | around Camineet | grass, forests, walls with gaps, a bridge **(verified)** | `palma_camineet`, `palma_forest`, `palma_cave` |
| Field-menu pictures | town, forest | a still picture of the place behind the menu **(verified)** | `hud_menu`, `menu_forest` |
| Cave (blue walls) | south-west of Camineet, dark | first person, needs a FLASH, chests on squares **(verified)** | `cave_dark`, `dungeon_corridor`, `dungeon_chest` |
| Passage (green walls) | under the grey dome in Camineet | first person, lit **(verified)** | `camineet_passage` |
| Intro space and town | intro | planet in space, Camineet street **(verified)** | `intro_planet`, `intro_camineet` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Sworm | forest near Camineet | flying insect | HP 8, attack 13, defense 9 **(RAM)**; bites for 1-2 **(verified)**; 2 EP, may leave a chest | `battle_sworm`, `battle_attack`, `battle_hit`, `battle_talk` |
| Scorpion | by the cave | red scorpion | HP 12 **(verified)** | `battle_scorpion` |
| Wing Eye | in the cave | winged eyeball | HP 11, attack 12, defense 10 **(RAM)** | `battle_wing_eye`, `battle_died` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| SHT. SWD | weapon | start | Alis's first weapon **(verified)** | `menu_status` |
| LTH. ARMR | armour | start | **(verified)** | `menu_status` |
| LTH. SLD | shield | armory, 30 | +3 defense **(verified)** | `shop_armory`, `item_equip`, `status_shield` |
| IRN. SLD, CRC. SLD | shields | armory, 520 / 1400 | not bought | `shop_armory` |
| COLA, BURGER | food | food shop, 10 / 40 | BURGER healed 7 HP to the maximum **(verified)** | `shop_food`, `item_use_burger` |
| FLASH | tool | second-hand shop, 20 | lights a dark cave **(verified)** | `shop_list`, `dungeon_corridor` |
| ESCAPER, TRANSER | tools | second-hand shop, 10 / 48 | escape and transport **(source)**; ESCAPER sells for 5 | `shop_list`, `shop_sell_offer` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| (spells) | Myau, Noah, later Alis **(source)** | MP | | none: no spell in the early game (Alis has 0 MP) |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Alis | heroine, the player | everywhere | `intro_alis_vow`, `camineet_start` |
| Nero | Alis's brother, killed in the intro | intro | `intro_nero_beaten`, `intro_nero_dying` |
| Robotcops | Lassic's guards | intro, Camineet gate | `intro_nero_beaten`, `camineet_gate` |
| Shopkeepers | three, one per shop, each in a different room | Camineet | `shop_secondhand`, `shop_food`, `shop_armory` |
| Priest | resurrects the dead | Camineet church | `camineet_church` |
| Townspeople | walk the streets | Camineet | `camineet_gate`, `camineet_shops` |

## Open questions
- Myau, Odin, Noah and the other planets: later shots (shots.txt LATER section).
- What the 08 squares of the Camineet passage hold (nothing showed on one of them, `design/findings.md`).
