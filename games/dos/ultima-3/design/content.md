# Ultima III: Exodus (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima-3`.

Which kinds exist depends on the game, its genre and structure: keep the kinds this game has, drop the rest,
add its own (vehicles, tracks, puzzles, levels, minigames ...). For each kind say how many there are in total
if known, then show a sample that spans the range: early and late, common and rare, plain and strange, one of
each visual family. A complete table belongs in its own document (items.md, enemies.md) and is linked here.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | Sosaria (64x64), 10 townes, 2 castles, 7 dungeons of 8 levels, Ambrosia, the combat fields **(code)** | all places | ../playbook.md Game structure |
| Opponents | about 30 monster pictures; 13 kinds roam Sosaria **(code, ROM text)** | a spread | section 3 |
| Items | gold, food, gems, keys, powders, torches, 4 cards, 4 marks **(ROM text)** | all | section 4 |
| Equipment | 15 weapons + Exotic, 7 armours + Exotic **(ROM text)** | all, with prices | section 4 |
| Abilities / spells | 16 cleric spells, 15 named wizard spells **(ROM text)** | names | section 5 |
| Characters and people | 5 races, 11 classes; Lord British, the Time Lord, Radrion, named townsfolk **(ROM text)** | all | section 6 |
| Vehicles | horse, frigate **(code)** | both | - |
| Talk lines | about 70 lines in 11 places **(ROM text)** | a sample | section 7 |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Sosaria: grass, brush, forest, mountains, sea | the world map **(verified)** | the party icon, monsters and ships on the map | `start_party` |
| A towne (LCB) | (2E,13) **(verified)** | brick floor, counters with signs, guards, merchants | `towne_lcb` |
| Lord British's castle | (2D,12) **(verified)** | moat, the BRITISH sign over the throne, jesters | `castle_gate`, `castle_throne` |
| Yew's Circle of Light | (22,10) **(verified)** | a ring of clerics, where PRAY answers | `yew_pray` |
| Dawn | (25,35) in the Dark Forest **(verified)** | appears only at new moons; every shop | `dawn_towne` |
| Death Gulch, Devil Guard, Fawn, Grey, Moon, Montor East and West | Sosaria **(code)** | thieves' Grey, guarded Death Gulch ("<Bribe> me to enter"), stables of Devil Guard | `townes` |
| Dungeon corridors | 7 dungeons **(verified)** | wireframe-like walls, dark without a torch | `dungeon_torch` |
| The Time dungeon | (3A,1E), walled in by mountains **(verified)** | reached only by moongate; the Time Lord on level 8 | `moongate_through`, `timelord` |
| Ambrosia | through the whirlpool **(verified)** | mountains, four shrines, guardian monsters, the AMBROSIA sign | `ambrosia_shore`, `shrine_enter` |
| The Isle of Fire and Castle Exodus | (0A,35) behind the Silver Snake **(verified)** | lava rings, force fields, the DEATH sign, Exodus's slots | `isle_of_fire`, `exodus_*` |
| Combat fields | CNFLCT_A..S **(code)** | 11x11 terrain per place kind | `battle_*` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Orcs | Sosaria (grass) **(verified)** | humanoid | bands of several; 3 experience each **(verified)** | `battle_start` |
| Thieves, fighters, wizards, clerics | Sosaria, townes **(code)** | people | thieves steal (ROM text "Pilfered!") | `battle_*` |
| Skeletons, giants, daemons, pinchers | Sosaria, Ambrosia **(code)** | monsters | - | `battle_*`, `ambrosia_monsters` |
| Dragons, balrons | Sosaria, Ambrosia, Castle Exodus **(code)** | late monsters | - | `exodus_monsters` |
| Sea serpents, man-o-wars, pirates | the sea **(code)** | ships and serpents | pirates leave a frigate **(source: series knowledge, not checked)** | `battle_*` |
| The Silver Snake | the strait at (0A,39) **(verified)** | a fixed serpent | blocks the way to the Isle of Fire until EVOCARE | `serpent`, `evocare` |
| Floors | in front of Exodus **(verified)** | invisible: they look like the floor | attack when the party nears the slots | `exodus_floors` |
| Exodus | Castle Exodus **(verified)** | a machine of four slots | cannot be fought; ended by the four cards | `exodus_slots` |
| Dungeon monsters: Brigand, Cutpurse, Goblin, Troll, Ghoul, Zombie, Golem, Titan, Gargoyle, Mane, Snatch, Bradle, Griffon, Wyvern, Orcus, Devil **(ROM text)** | dungeons, by depth | - | - | `dungeon_fight` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Dagger 5, Mace 30, Sling 60, Axe 125, Bow 350, Sword 200, 2H Sword 250 | weapons (gold) | weapon shops **(ROM text)** | ready with R | `shop_weapons` |
| +2 Axe 400, +2 Bow 1050, +2 Sword 800, Gloves 1200, +4 Axe 2700, +4 Bow 6550, +4 Sword 4550 | magic weapons | weapon shops (Dawn) **(ROM text)** | - | `shop_weapons` |
| Exotic weapon | the best weapon | DIG at (21,03) **(code, verified)** | "Only with Exotic arms can you win" (LCB) | `dig_exotics` |
| Cloth 75, Leather 195, Chain 575, Plate 2500, +2 Chain 6130, +2 Plate 8250 | armour | armour shops **(ROM text)** | wear with W | `shop_armour` |
| Exotic armour | the best armour | DIG at (13,2C) **(code)** | - | `dig_exotics` |
| Torches, keys, powders, gems | tools | the Guild, chests **(ROM text)** | light dungeons, unlock doors, negate time, peer at the map | `shop_guild`, `peer_gem` |
| Cards of Love, Sol, Moons, Death | quest items | SEARCH on Ambrosia's shrines **(verified)** | inserted into Exodus | `card_found`, `ztats_cards` |
| Marks of Force, Fire, Snake, Kings | brands | rods in dungeons **(verified)** | fields, lava, EVOCARE, levels past five | `dungeon_mark` |
| Horses, frigates | vehicles | stables (horses), pirates (frigates) **(code)** | faster travel, the sea | `shop_horses`, `frigate` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Wizard spells Repond, Mittar, Lorum, Dor Acron, Sur Acron, Fulgar, Dag Acron, Mentar, Dag Lorum, Fal Divi, Noxum, Decorp, Altair, Dag Mentar, Necorp **(ROM text)** | wizards and other arcane classes | magic points (open) | open | `battle_spell` |
| Cleric spells Pontori, Appar Unem, Sanctu, Luminae, Rec Su, Rec Du, Lib Rec, Alcort, Sequitu, Sominae, Sanctu Mani, Vieda, Excuun, Surmandum, Zxkuqyb, Anju Sermani **(ROM text)** | clerics, paladins and others | magic points (open) | open | `battle_spell` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Races Human, Elf, Dwarf, Bobbit, Fuzzy; classes Fighter, Cleric, Wizard, Thief, Paladin, Lark, Barbarian, Druid, Illusionist, Alchemist, Ranger **(verified in the form)** | playable | creation | `menu_create_*` |
| ryz (Human Paladin), condi (Elf Wizard), ebo (Dwarf Fighter), cubi (Bobbit Cleric) | the party here | - | all |
| Lord British | king, raises levels | his castle's throne (20,0E) **(verified)** | `lb_*` |
| The Time Lord | gives the card order | Time dungeon level 8 **(verified)** | `timelord` |
| Radrion, Prophet of Life | oracle, a long rhyme for gold | oracle counters **(ROM text)** | `shop_oracle` |
| Dupre, Iolo, Gwino, Shamino, Sentri, Cookie, Chuckles, Jolly Joe, Baby Bob, the Wise Cleric, the Phantom Fighter | townsfolk with names **(ROM text)** | LCB, the castle, Montor East/West | `talk_*` |
| Guards, merchants, jesters | townsfolk **(verified)** | everywhere | `towne_lcb` |

## 7. Talk lines (sample, ROM text)
| Place | Lines |
|---|---|
| LCB | "Is it not lovely", "Quest ye unto Lost Ambrosia!", "Only with Exotic arms can you win", "Exodus lies beyond the Silver Snake!", "`Dawn' comes each new pair!", "Dupre laughs: Drink up!", "Round back!", "Ho! Ho!" |
| Lord British's castle | "West 8, South 35 and await Dawn!", "Cookie cries: Like the food?", "Iolo sings: Ho eyo he hum!", "Gwino sings: Muh eh oye oh!", "Phantom Fighter: The food stinks!", "The Wise Cleric: 4 cards, 4 slots", "Enter... If you dare!", "Chuckles: Welcome all!" |
| Moon | "Seek ye the Shrines of Truth", "<Bribe> guards! They will leave!", "I've been beyond the whirlpool!", "Dawn rises in the Dark Forest." |
| Yew | "Search and ye shall find!", "Welcome to the Circle of Light!", "Bonim Anima Teuri, Amen!", "Know ye well thy foes!!" |
| Montor East / West | "<Insert> cards into pannels!", "4 cards, 4 pannels", "`Cards' / `Marks' / `Exotics' are useful!"; "Seek the Jester in castle Fire!", "<Search> the Shrines!", "<Search> for cards!", "None shall pass!" |
| Grey | "Yo! ho! ho! and a bottle of rum!!!", "Ever seen Exotic arms?", "Exotic clues found at Dawn!", "Only Exotics will protect from Great Evil!" |
| Dawn | "<Dig> on isles", "<Dig> up Exotics", "Dawn lasts but a brief moment!", "Ambrosia awaits!" |
| Devil Guard | "`Marks' gained in dungeons!", "Hot metal leaves a `Mark'!", "The King favors a `Mark'!", "A `Mark' helps invoke the Snake", "4 `Marks', 4 uses!", "Seek ye the dungeon of fire!" |
| Fawn | "<Pray> for the invocation!", "<Pray> in the Circle of Light!", "`Invoke' the Silver Snake!", "To pass you need a Mark!", "Welcome to Fawn: City of the sea!" |
| Death Gulch | "Begone fool!", "<Bribe> me to enter", "Exodus is four as one!" |
| Castle Exodus | "All may enter, None shall leave", "Choose well your way!", "Save me Please!!!", "Death is here!", "Leave quickly!" |
| Dungeon level messages | e.g. Snake dungeon "<Insert> cards into Exodus!", "<Search> the Shrines!"; Time "Time awaits!", "Very near now!" |

## Open questions
- Which monster appears where in the dungeons (by depth), the combat fields by terrain, spell effects.
- Ambrosia's talk table repeats LCB's lines (the file holds a copy; Ambrosia has no talkers).
