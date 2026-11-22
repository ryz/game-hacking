# WASTELAND - content (variety lens)

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
| Environments | world map plus about a dozen major locations and many small ones (source) | world grass and mountains, lake, river, Ranger Center, Highpool (desert, creek, pool, store, workshop), Agricultural Center | |
| Opponents | many groups (source) | Animals: Radioactive Vermin, Wild Canines | |
| Items | dozens (source) | the Highpool shop's nine items, pistol and clips | |
| Equipment | weapons from fists to energy weapons (source) | Fists, M1911A1 .45 pistol, the pre-made rangers' 9 mm pistol shown as `VP912 9` (name truncated, inferred VP91Z) | |
| Abilities / spells | skills, no magic | nine creation skills | |
| Characters and people | rangers, townspeople, recruits (source) | RYZ and three pre-made rangers, storekeeper, doctor, Highpool kid, farmers (in text) | |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Grass and mountain ridges | world map near the Ranger Center | green speckled grass, white-capped ridges that block | `world_start`, `world_full`, `env_world_valley` |
| Lake | world map west of Highpool | blue water with a curved shore | `env_world_lake`, `env_world_lake_south` |
| River | world map north-west of the lake | current that drags and hurts the party | `world_river_current` |
| Ranger Center | south-east corner | the building picture instead of a map | `rc_roster` |
| Highpool desert | Highpool, north part | dark red ground, grey stone walls, bushes | `hp_desert` |
| Highpool creek and pool | Highpool valley | blue creek, white bridge, pool, huts | `env_hp_creek`, `env_hp_pool`, `hp_creek_wade` |
| Store and gaming hall | Highpool | red-brown walls, counter, purple bed, door | `hp_store_entry` |
| Workshop | Highpool, bottom left building | small room with machine parts, pump and cot | `hp_workshop`, `hp_workshop_parts`, `hp_workshop_pump` |
| Agricultural Center | west of Highpool | adobe walls with scorch marks, sales booth, farmers | `ag_center`, `ag_center_walk`, `loc_agcenter` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Animals / Radioactive Vermin | world map at the Ranger Center | brown rodent portrait | groups of 3, bites for about 7 **(verified)** | `battle_appears`, `battle_menu`, `battle_round`, `battle_radrat` |
| Animals / Wild Canine | world map north-west of the Ranger Center | grey wolf portrait | groups of 4, bites for 5 to 13, pounces **(verified)** | start set `29_fight`, `33_battle_round`, `35_battle_won` |
| Highpool kid | Highpool creek | a small blue figure | appears after the party slips in the creek; more kids, a Chubby Kid and the Red Ryder follow (source) | `hp_creek_kid` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| M1911A1 .45 pistol | weapon (clip pistol) | RYZ's starting pack | needs .45 clips; equipped with Weapon | `char_items`, `battle_weapon` |
| .45 clip | ammunition | starting pack (8) | reloads the pistol | `char_items` |
| Fists | weapon | everyone | the default in hand | `world_start` |
| Book, Canteen, Crowbar, Gas mask, Geiger counter, Hand mirror, Jug, Map, Match | tools | Highpool shop, $1 to $300 | the Crowbar forces doors, the Match lights dark caves (source) | `hp_shop_buy`, `hp_shop_bought` |
| Rope | tool | sold for 19 in the Sell list | lets the party enter Highpool's cave (source) | `hp_shop_sell` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Clip pistol, Rifle | any ranger | 1 skill point each at creation | better hits with pistols and rifles (source) | `rc_skills`, `char_skills` |
| Perception | IQ 6 or more | 1 point | search a square; "You see nothing special." when empty | `field_perception` |
| Brawling, Climb, Knife fight, Pugilism, Swim, Knife throw | any ranger | 1 point | fighting and travel skills (source) | `rc_skills` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ | the owner's ranger, created in place of Hell Razor | party | `char_stats`, `rc_party` |
| Hell Razor, Angela Deth, Thrasher, Snake Vargas | pre-made rangers | Ranger Center | `rc_roster` |
| Storekeeper | shop | Highpool store | `hp_shop` |
| Doctor | infirmary | Highpool | `hp_infirmary`, `hp_infirmary_exam` |
| Farmers | ten men with axes, hoes and shovels, in despair | Agricultural Center sales booth | `ag_center` |
| Teens, children | heard and seen in Highpool | dorm, creek | `hp_dorm`, `hp_creek_slip` |

## Open questions
- Later towns (Quartz, Needles, Las Vegas) and their opponents: not reached in this run.
- Whether the Sell list shows the shop's buying offers for any item or only for items the party carries.
