# Might and Magic II: Gates to Another World (DOS) - content (variety lens)

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
| Environments | 60 areas: 5 towns, 20 outdoor areas, 16 caverns, 5 castles, 10 dungeons and towers, 4 elemental planes **(verified)**; graphics sets town, cave, castle, outdoor terrains (tundra, desert, swamp, ocean, sky) **(source: file names)** | sample below | [world.md](world.md) |
| Opponents | over 250 kinds **(source)** | sample below | - |
| Items | weapons, armour, miscellaneous, quest items (Discs, Talons, Element Orb, keys, tickets, J-26 Fluxer, A-1 Todilor, N-19 Capitor, M-27 Radicon) **(source: area texts)** | sample below | - |
| Abilities / spells | 96 spells (48 cleric, 48 sorcerer, 9 levels) **(source)**; 15 secondary skills **(source)** | sample below | manual Appendix B |
| Characters and people | 8 classes, 5 races; 6 premade characters, hirelings (about 26), quest givers **(source / verified)** | sample below | - |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Town (Middlegate) | area 00 | blue-green stone walls, signboards over doors, sky above **(verified)** | gameplay_inn_start, dialogue_spirit_corak |
| Inn interior | each town | innkeeper at a desk **(verified)** | save_innkeeper |
| Forest and river | C2 outside Middlegate | trees, water, signposts **(verified)** | gameplay_outdoors_c2, gameplay_pegasus |
| Snow and tundra | A1 | white ground, rocks **(verified, survey frame)** | planned |
| Desert oasis | E2 | yellow sand, fruit trees **(verified, survey frame)** | planned |
| Mountains | E1 | grey mountain wall **(verified, survey frame)** | planned |
| Cavern | under Middlegate | green-grey stone, lit only by magic **(verified)** | gameplay_cavern_lit |
| Castle | Hillstone, Xabran ... | grey brick walls, blue checkered floor, banners **(verified, survey frame)** | gameplay_xabran_800 (outside), planned |
| Elemental planes | four corners | planned | planned |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Witch's Cat, Rabid Rodent | Middlegate (8,1) | magenta cat **(verified)** | first town fight | battle_encounter |
| Skeleton (13) | Middlegate (10,4) | skeleton **(verified)** | big town group | planned |
| Brain Eater + Merchant | Middlegate (13,12) | green beast **(verified)** | - | planned |
| Blood Sucker + Mugger | Middlegate (12,14) | red bat **(verified)** | - | planned |
| Orc, Mutant Swine | C2 | orc with shield **(verified)** | outdoor group | planned |
| Druid | C3 (outdoors) | green-robed druid **(verified, survey)** | - | planned |
| Carnage Spirit | cavern under Atlantium, a castle dungeon, Square Lake | pale demon **(verified)** | - | planned |
| Grim Reaper | Square Lake | robed reaper **(verified)** | - | planned |
| Phantasm, Nasty Witch, Gargoyle, Wraith, Iron Wizard, Guardian, Mummy, Court Jester, Warbot, Mystic Clown, Alien Probe | Square Lake, one group each **(verified)** | robots and aliens among them | final dungeon gauntlet | planned |
| Devil King (66) | Square Lake (11,14) **(verified)** | horned demon head | "66 Devil Kings attack!" | battle_square_lake_devils |
| Mega Dragon, elemental lords, Dread Knight, Baron Wilfrey, Dawn, Lich Lord, Sheltem | quest bosses **(source)** | - | - | planned |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Short Sword, Large Club, Small Knife | starting weapons **(verified)** | creation, premade characters | - | inventory_profile_ryz, inventory_premade |
| Air, Fire, Earth, Water Disc | quest **(source: area texts)** | Castle Xabran pedestals | open the shrines of the planes | planned |
| Air, Fire, Earth, Water Talon; Element Orb | quest **(source: area texts)** | shrines; Dawn's Mist | given to King Kalohn in the 9th century | planned |
| Black Ticket, coloured keys | quest **(source)** | Atlantium, locksmiths (Red Key 2,500 gold in Vulcania) | arenas, bishops | planned |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Light (cleric 1-5, sorcerer 1-5) | casters | 1 SP **(verified)** | one light unit | system_cast_spellbook |
| Lloyd's Beacon, Town Portal, Teleport, Time Distortion | sorcerer / cleric **(source)** | - | travel | planned |
| Enchant Item | sorcerer 9 **(source)**, bought from the master gemmaker (area text) | 50 per plus + 50 gems | raises an item's bonus | planned |
| Cartographer, Pathfinder, Mountaineer, Navigator, Crusader, Linguist ... | secondary skills **(source; three trainers verified)** | 10-2,000 gold | auto-map, terrain, quests | system_otto_mapper |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Sir Felgar, Terwin III, Sure Valla, Gene Eric, Cassandra, The Hermit | premade party **(verified)** | roster | menu_view_all |
| Spirit of Corak | greeting **(verified)** | Middlegate inn door | dialogue_spirit_corak |
| Innkeeper, Svendegard (blacksmith), waitress, temple cleric, Turkov's squires, Otto Mapper, Nordon | town people **(verified)** | Middlegate | save_innkeeper, shop_blacksmith_door, dialogue_waitress, system_temple, system_training, system_otto_mapper, dialogue_nordon |
| Guardian Pegasus | helper once a year if named **(verified)** | C2 (7,4) | gameplay_pegasus |
| Jurors of Mount Farview, Queen Lamanda, King Kalohn, Lords Slayer, Hoardall, Peabody, Yekop and Ybmug | quest givers **(source)** | D2, Luxus Palace, C4 (9th century), castles | planned |
| Hirelings (Sir Hyron, Drog, H K Phooey, Thund R., Mr. Wizard ...) | hire **(source)** | inns after quests | planned |

## Open questions
- Monster and item tables (MONSTERS.DAT 5,702 bytes, ITEMS.DAT 5,120 bytes in the game folder) are not decoded.
