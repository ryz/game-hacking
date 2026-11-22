# Dragonflight - content (variety lens)

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
| Environments | land (forest, river, road, mountains), walled towns, first-person dungeons, combat side views **(verified / RAM for dungeons)** | land, Pegana, a combat meadow | - |
| Opponents | 15 kinds named in the game text **(RAM)** | Snake | section 3 |
| Items | 79 names incl. 10 potions, gems, quest letters and notes **(RAM)** | torch, piece of map, Worldmap | section 4 |
| Equipment | 15 weapons, 6 armours, 4 rings **(RAM)** | sword | section 4 |
| Abilities / spells | 29 spells in three schools **(RAM)** | none known at the start | section 5 |
| Characters and people | 4 fixed heroes; towns with named residents | the heroes, a red-haired young man | section 6 |
| Places | 17 place names in the game text: Stormwind, Clearlight, Gemshine, Farout, Crystaleye, Thunderroar, Deepsea, Darkmoon, Pegana, Port Pylon, Brindil-Bun, Nimraviel, Scatterbone, Drombul, Bagnol, Luthag, Trolian, Negame, Sotul, Orc Village **(RAM)** | Pegana | - |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Town streets | Pegana | grey cobbles, red-roofed timber houses, a blue fountain, grey city wall | `env_pegana_square`, `env_pegana_road`, `gameplay_door_nobody` |
| Land: river and road | around Pegana | grass, roads, a winding river, the town icon | `env_land_river`, `hud_land` |
| Land: forest | south of Pegana | dense trees | `env_land_forest` |
| Land: bridge and mountains | east of Pegana | wooden bridge, grey mountains with a cave arch, the sea | `env_land_bridge` |
| Camp | anywhere on the land | night scene with a campfire | `system_camp` |
| Combat meadow | land fights | side view: flowered meadow under a blue sky | battle_start (live play only, not in the set: fights do not reproduce, see playbook), battle_hit (live play only, not in the set: fights do not reproduce, see playbook) |
| Sage's room | intro | stone room, fireplace, the sage | `cutscene_sage` |

## 3. Opponents
Named in the game text **(RAM)**: Orc, Skeleton, Ghost, Bear, Snake, Beast, Gnoll, Troll, Ghoul, Energyball,
Balron, Statue, Guardian, Unicorn (a banned unicorn, freed in a story scene), Shadow. Groups carry weapons
(no weapons, thorns, daggers, short swords, swords, broadswords, battleaxes, battlehammers) **(RAM)**.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Snake | land south-east of Pegana | green snake | ambushes ("surprises you"), no weapons; took several rounds to wound a hero at 1 hit point **(verified)** | battle_encounter (live play only, not in the set: fights do not reproduce, see playbook), battle_close (live play only, not in the set: fights do not reproduce, see playbook), battle_wounded (live play only, not in the set: fights do not reproduce, see playbook) |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Torch | light | every hero at the start | "The torch has been lighted!" **(RAM)** | `inventory_items` |
| Piece of map 02 | quest | Rinakles at the start | added to the Worldmap with Use **(verified)** | `inventory_map_piece`, `inventory_examine`, `map_worldmap_added` |
| Sword | weapon | Blacksmith **(inferred)**; poked here | melee weapon, 27 damage seen **(verified)** | `inventory_weapon`, battle_hit (live play only, not in the set: fights do not reproduce, see playbook) |
| Weapons | Dagger, magic Dagger, short Sword, Sword, Broadsword, Crystalblade, Stiletto, Battleaxe, Battlehatchet, mag. Battlehatchet, Battlehammer, Bow, Longbow, Elvenbow, Staff of Stone **(RAM)** | - | - | - |
| Armour | Leather, studded Leather, light/medium/heavy/magic Chainmail **(RAM)** | - | - | - |
| Others | rings (small, medium, large, Dragonring), 10 potions, Phial, Mushrooms, gems, jewellery, Flute, Compass, Key, Book, Sphere, Treaty, letters and notes, Beer, Mead, scrolls, Levelmap, +1 to +5 weapon oils **(RAM)** | - | - | - |

## 5. Abilities and spells
White (w): Light, Dispell undead, Magic arrow, Dazzle, Speed, Protect Player, Protect Party, Healing, Healing
trance, Templeteleport, Teleportation. Black (b): Light, Magic arrow, Fire-ball, Lightning, Fear, Shockwave,
Area of lightning, Nameless spell, Leave dungeon. (c): Heal a tree, Wood hardening, Fertility, Moulded stones,
Glowing stone, Stone hardening, Feeling ore, Conservation, Clearing fog **(RAM)**. Passwords to the schools of
magicians: In the desert, Dorinthannon North and South, the island between the claws, the desert of ice
**(RAM: in-game note)**.

| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| (none known at the start) | Rinakles, Bladus, Andariel have magic points | - | "No spell prepared" **(verified)** | `inventory_spells`, `system_cast_no_spell` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Bladus | human fighter, 100 HP, 5 magic **(verified)** | party | `inventory_status` |
| Rinakles | human wizard, 50 HP max, 10 magic **(RAM)**, carries the map part | party | `inventory_map_piece` |
| Dobranur | dwarf fighter, 120 HP, no magic **(verified)** | party | `inventory_status_dobranur` |
| Andariel | elf, 60 HP, 8 magic **(verified)** | party | `17_status_andariel` (start set) |
| The sage | gives the Rings of Stasis and a map part | intro | `cutscene_sage` |
| Red-haired young man | brother of the torch trader in Drombul (north-eastern forest) | Pegana | `dialogue_redhair`, `dialogue_show` |
| Erik Simon, Udo Fischer, Jochen Hippel | authors | credits | `credits_team` |

## Open questions
What exists but was not seen: every opponent but the Snake, the shops, spells in use, dungeons, the ship, the
dragon. Encounters come at random on the land; shops sit behind town doors not yet found.
