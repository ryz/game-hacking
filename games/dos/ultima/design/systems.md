# Ultima I: The First Age of Darkness (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: the row says why), `open` (not
understood). Shot ids are those of set `main` (`../shots/main/index.md` gives the file names).

## 1. Core loop
The hero walks the overworld, enters towns to buy food, weapons, armour, spells and vehicles, and castles to
take a king's quest **(verified)**. Money and experience come from fighting monsters on the overworld and in
dungeons; every kill pays a few copper and silver pieces and experience **(verified: `battle_orc_killed`,
`battle_spider_killed`)**; hit points earned in a dungeon are paid out when the hero climbs back to the surface
(`system_klimb_out`) **(verified)**. Food runs down with moves and must be bought **(verified)**. Quests raise
statistics or give gems; game time (moves) unlocks better goods in the shops **(verified)**. The late game
leaves the fantasy loop for space combat, a princess rescue and the time machine **(verified)**.

## 2. Systems
| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move | one square per key; terrain and vehicle decide what is passable **(verified)** | arrows | water, mountains block on foot; woods block the aircar | §3.1 | `start_overworld`, `hud_status`, `system_blocked_water`, `system_blocked_mountains`, `system_aircar_woods` | shown |
| Player verbs | Pass | spend a turn; monsters move and attack **(verified)** | space | | | `hud_status`, `battle_ness_creature` | shown |
| Player verbs | Attack | melee with the readied weapon in a direction outdoors, straight ahead in dungeons **(verified)** | a (+ direction) | dagger 17 damage, sword 105+ | §3.4 | `battle_orc_hit`, `battle_orc_killed`, `battle_spider_killed`, `system_jester_key`, `boss_hit_mondain` | shown |
| Player verbs | Board / Mount / X-it | step on a vehicle, B boards ("Mount Horse", "Board Frigate"), X leaves it standing **(verified)** | b, x | | §3.6 | `system_mount_horse`, `system_xit`, `gameplay_frigate`, `gameplay_cart`, `gameplay_raft`, `gameplay_aircar` | shown |
| Player verbs | Cast | the readied spell; Prayer outdoors has no effect, most spells work only in dungeons **(verified)** | c | | §3.7 | `system_cast_prayer`, `battle_magic_missile`, `system_spell_ladder_down` | shown |
| Player verbs | Drop | pence, weapon or armour; outdoors only "Drop?" **(verified)** | d, p/w/a, amount | | | `gameplay_drop_pence` | shown |
| Player verbs | Enter | town, castle, dungeon or landmark on the square **(verified)** | e | | | `gameplay_britian`, `gameplay_dungeon`, `system_landmark_pillars` | shown |
| Player verbs | Fire | the vehicle's guns: cannons on a frigate, lasers on an aircar, the ship's guns in space **(verified)** | f (+ direction) | one shot killed a pirate ship and an orc | §3.6, §3.9 | `system_frigate_fire`, `system_aircar_lasers`, `battle_space_hit` | shown |
| Player verbs | Get | in Mondain's chamber: take the gem (2,196 damage to the player); elsewhere "Get?" or "Get what?" **(verified)** | g | 2,196 | §3.11 | `boss_gem_destroyed`, `gameplay_refusals` | shown |
| Player verbs | HyperJump | in space, front view only, to another sector; outdoors "HyperJump?" **(verified)** | h | about 1,250 frames until "HyperJump completed." | §3.9 | `system_hyperjump`, `gameplay_space_enemy`, `gameplay_refusals` | shown |
| Player verbs | Inform and search | names the land, "You are in the woods", "You are at sea", the town; finds secret doors in towns **(verified; secret doors: ROM text)** | i | | | `gameplay_inform`, `gameplay_woods`, `gameplay_at_sea`, `gameplay_lands_lord_british` | shown |
| Player verbs | K-limb | climb a ladder in a dungeon; the hero must face north or south on the ladder square **(verified)** | k | | §3.8 | `system_klimb_down`, `system_klimb_out`, `system_klimb_facing` | shown |
| Player verbs | Noise | sound on/off **(verified)** | n | | | `system_noise` | shown |
| Player verbs | Open | coffins in dungeons (chests are opened with Unlock) **(verified)** | o | | §3.8 | `gameplay_coffin` | shown |
| Player verbs | Quit | save the game; only outdoors; play continues **(verified)** | q | | §3.12 | `save_quit`, `system_quit_indoors` | shown |
| Player verbs | Ready | choose weapon, armour or spell from what is owned **(verified)** | r, w/a/s, letter | | | `inventory_ready_weapon`, `inventory_ready_armour`, `inventory_ready_spell` | shown |
| Player verbs | Steal | behind a shop counter or in a castle storeroom; caught = guards **(verified)** | s | caught on 77 of 255 rolls, thieves 37 **(code)** | §3.5 | `system_steal`, `system_steal_caught`, `system_steal_storeroom` | shown |
| Player verbs | Transact | shops (buy/sell), pub (ale), kings (pence or service) **(verified)** | t | | §3.5 | `shop_transport`, `shop_pub`, `dialogue_king_offer` | shown |
| Player verbs | Unlock | prison cells with the jester's key; in dungeons opens chests **(verified)** | u | | §3.10, §3.8 | `system_cell_open`, `system_no_key`, `system_chest_trap`, `system_chest_gold` | shown |
| Player verbs | View | space: top view / front view; refused while enemies are in the sector **(verified)** | v | | §3.9 | `gameplay_space_front`, `system_space_view_refused` | shown |
| Player verbs | Ztats | inventory and statistics, paged with More **(verified)** | z | | | `inventory_ztats`, `inventory_ztats_mid`, `inventory_ztats_late` | shown |
| Player verbs | Unknown keys | "Huh?" **(verified)** | j l m p w y | | | `gameplay_refusals` | shown |
| Characters and progression | Creation | six statistics start at 10, 30 points to add; race and class add fixed bonuses; 150 hit points **(verified)** | arrows, letters | Human Int +5, Elf Agi +5, Dwarf Str +5, Bobbit Str -5 Wis +10; Fighter Str +10 Agi +10, Cleric Wis +10, Wizard Int +10, Thief Agi +10 | §3.2 | `gen_points`, `gen_stats_mid`, `gen_stats_done`, `gen_race`, `gen_sex`, `gen_class`, `gen_name`, `gen_save`, `gen_other_build` | shown |
| Characters and progression | Level | experience / 1000 + 1 **(code; verified on Ztats: 4213 exp = level 5, 7340 = level 8)** | | | | `inventory_ztats_mid`, `inventory_ztats_late` | shown |
| Characters and progression | Hit points | the life total; bought from kings at 3 for 2 pence, earned in dungeons, 500 from a princess **(verified)** | t, p | 50 pence = 75 hits | §3.3 | `dialogue_king_pence`, `system_klimb_out`, `system_princess_reward` | shown |
| Characters and progression | Statistics from landmarks | entering a landmark raises one statistic by (value + 8) / 10, to 99 at most **(code; verified 5 times)** | e | 28 Agility -> +3 | §3.3 | `system_landmark_pillars`, `system_landmark_tower`, `system_landmark_ozymandias`, `system_landmark_signpost`, `system_landmark_southern`, `system_landmark_grave_gain` | shown |
| Characters and progression | Quest rewards | landmark quests: Strength from the king; monster quests: a gem **(verified)** | t, s | Lord British: 8 Strength | §3.10 | `dialogue_quest_done`, `dialogue_gem_red`, `dialogue_gem_green`, `dialogue_gem_blue`, `dialogue_gem_white`, `system_quest_kill` | shown |
| Resources and economy | Coin | copper pence, max 9,999; Ztats splits it into copper, silver (10) and gold crowns (100); kills pay "2 copper! 1 silver!" **(verified)** | | | §3.5 | `inventory_ztats`, `battle_orc_killed` | shown |
| Resources and economy | Food | one unit per move or so; 0 = death; packs of 10 for 5 pence **(verified)** | t, amount | | §3.5 | `shop_food`, `shop_food_bought`, `gameover_starved` | shown |
| Resources and economy | Shops | six kinds; odd and even towns sell different weapons and spells; goods grow with game time; Charisma lowers prices **(verified)** | t, b/s, letter | | §3.5 | `shop_weapons`, `shop_weapons_even`, `shop_weapons_late`, `shop_armour`, `shop_armour_late`, `shop_magic`, `shop_magic_even`, `shop_transport`, `shop_transport_space` | shown |
| Resources and economy | Selling | weapons and armour sell for little; transport, magic and food shops buy nothing **(verified / ROM text)** | t, s | dagger 1 pence | §3.5 | `shop_weapons_sell`, `shop_no_used` | shown |
| Resources and economy | Pub | ale for 1 pence; a tavern keeper's tip after some drinks **(verified)** | t, b | tip on 75 of 255 rolls **(code)** | §3.5 | `shop_pub`, `dialogue_pub_space`, `dialogue_pub_princess`, `dialogue_pub_mondain`, `dialogue_pub_lakes` | shown |
| Resources and economy | Game time | the move counter, saved with the character; gates shop goods (1,500 and 3,000 moves) **(verified)** | | | §3.5 | `shop_weapons_late`, `shop_armour_late`, `shop_transport_space` | shown |
| Conflict | Melee and ranged attacks | hit or miss by the hero's numbers, damage shown in the log **(verified)** | a | | §3.4 | `battle_orc_hit`, `battle_spider_killed` | shown |
| Conflict | Monsters' attacks | adjacent monsters attack every turn; some steal or destroy (thief, gremlin, gelatinous cube, mind whipper) **(verified)** | | | §3.4 | `battle_thief`, `battle_gremlin`, `battle_gelatinous_cube`, `battle_ettin` | shown |
| Conflict | Vehicle guns | cannons and lasers reach several squares **(verified)** | f | | §3.6 | `system_frigate_fire`, `system_aircar_lasers` | shown |
| Conflict | Space combat | front view, gun sight, enemy fighters weave; a hit kills; aliens fire back **(verified)** | f, arrows | +100 experience per kill **(verified)** | §3.9 | `gameplay_space_enemy`, `battle_space_hit`, `battle_alien_fires` | shown |
| Conflict | Town guards | turn hostile after a theft is caught or a person is attacked **(verified)** | | 7 damage per hit seen | §3.10 | `battle_guard`, `system_steal_caught` | shown |
| Opponents | Overworld monsters | wander as map pieces and attack when adjacent; land and sea kinds; one kind is invisible **(verified)** | | 15 kinds | [content.md](content.md) §3 | `battle_orc_hit`, `battle_evil_trent`, `battle_hidden_archer`, `battle_ness_creature` | shown |
| Opponents | Dungeon monsters | 25 kinds; deeper levels hold stronger kinds; quest monsters Gelatinous Cube, Carrion Creeper, Lich, Balron **(verified)** | | | [content.md](content.md) §3 | `battle_skeleton`, `battle_balron`, `battle_lich`, `battle_carrion_creeper`, `battle_orc_corridor` | shown |
| Opponents | Mondain | 1,000 hit points; a bat below 500; dies at 0 only when the gem is destroyed **(code, verified)** | a, g | 1,000 / 500 | §3.11 | `boss_mondain`, `boss_hit_mondain`, `boss_mondain_bat`, `ending_victorious` | shown |
| Items and equipment | Weapons | 16 from hands to blaster; towns sell up to 5, the rest is stolen from castle storerooms **(verified)** | r, w | prices 5 to 94 | §3.5 | `inventory_ready_weapon`, `shop_weapons_late`, `system_steal_storeroom` | shown |
| Items and equipment | Armour | skin, leather, chain, plate, vacuum suit, reflect suit; a vacuum suit is needed to dock in space **(verified / code)** | r, a | 45 / 90 / 135; suits 172 / 215 (Charisma 19) | §3.5 | `shop_armour`, `shop_armour_late`, `inventory_ready_armour` | shown |
| Items and equipment | Gems | red, green, blue, white from the four gem kings; all four start the time machine **(verified)** | | | §3.10 | `dialogue_gem_red`, `cutscene_time_machine` | shown |
| Items and equipment | Vehicles | horse, cart, raft, frigate, aircar, shuttle, time machine **(verified)** | b, x, f | 36 to 1,296 pence | §3.6 | `shop_transport`, `shop_transport_space`, `gameplay_horse`, `gameplay_aircar`, `gameplay_shuttle` | shown |
| Abilities and magic | Spells | 11: Prayer (always known), Open, Unlock, Magic Missile, Steal, Ladder Down, Ladder Up, Blink, Create, Destroy, Kill; each cast uses one bought charge **(verified)** | r, s, c | 5 to 30 pence | §3.7 | `shop_magic`, `battle_magic_missile`, `system_spell_kill`, `system_spell_blink`, `system_spell_create`, `system_spell_destroy`, `system_spell_open`, `system_spell_unlock`, `system_spell_ladder_up` | shown |
| World and navigation | Overworld | 168x156 squares, four continents, 84 places **(verified data)** | | | §3.1 | `gameplay_lands_lord_british`, `gameplay_lands_feudal_lords`, `gameplay_lands_dark_unknown`, `gameplay_lands_danger_despair` | shown |
| World and navigation | Towns and castles | one-screen maps; 8 town plans and 2 castle plans, each used once per continent **(verified)** | | | §3.1 | `gameplay_britian`, `gameplay_town_montor`, `gameplay_castle`, `gameplay_castle_lost_king` | shown |
| World and navigation | Dungeons | first-person, 10 levels of 11x11 squares, doors, ladders, force fields, chests and coffins **(verified)** | | | §3.8 | `gameplay_dungeon`, `gameplay_dungeon_door`, `gameplay_dungeon_ladder`, `env_dungeon_doors`, `battle_balron_approach` | shown |
| World and navigation | Space | 7x7 sectors, sector scan, hyperjump, starbases, landing only by shuttle **(verified)** | | | §3.9 | `map_sector_scan`, `gameplay_space_top`, `system_landing` | shown |
| Goals and gating | King quests | odd castles: find a landmark (Strength); even: kill a monster (gem); one quest per king at a time **(verified)** | t, s | | §3.10 | `dialogue_king_quest`, `dialogue_king_kill_quest`, `dialogue_king_busy`, `dialogue_king_olympus`, `system_landmark_grave` | shown |
| Goals and gating | Space Ace | 20 enemy vessels destroyed **(verified)** | f | 20 | §3.9 | `system_space_ace`, `battle_space_hit` | shown |
| Goals and gating | Princess | key from the jester, open the cell, lead her out; with Space Ace and level 8 she reveals the time machine **(verified)** | a, u | 500 hit points, pence, experience | §3.10 | `system_jester_key`, `system_cell_open`, `system_cell_open_late`, `system_princess_reward` | shown |
| Goals and gating | Time machine | needs all four gems **(verified)** | b | | §3.11 | `gameplay_time_machine`, `cutscene_time_machine`, `system_time_machine_no_gems` | shown |
| Goals and gating | Ending | destroy the gem, kill Mondain, ending text **(verified)** | g, a | | §3.11 | `boss_gem_destroyed`, `ending_victorious`, `boss_or_is_he`, `ending_text` | shown |
| Chance | Rolls | hits, damage, steals, tips, traps, monster moves, the princess's cell, the time machine's place **(code / verified)** | | one random generator, advanced only when the game rolls | §3.4 | `system_chest_trap`, `dialogue_pub_lakes` | shown |
| Failure and recovery | Death and resurrection | at 0 hits or 0 food: "thou art dead", "Attempting resurrection!"; the hero returns with 99 hits and 99 food, no experience and no coin **(verified)** | | | §3.12 | `gameover_dead`, `gameover_starved`, `gameover_sun`, `system_resurrection` | shown |
| Failure and recovery | Traps and theft | chest traps cost hit points; thieves and gremlins steal; a gelatinous cube destroys armour **(verified)** | | | §3.8 | `system_chest_trap`, `battle_thief`, `battle_gremlin`, `battle_gelatinous_cube` | shown |
| Saving and sessions | Save | Q outdoors writes the character file; four character slots **(verified)** | q | | §3.12 | `save_quit`, `menu_select` | shown |
| Pacing and difficulty | Gates by time and progress | shop goods by move count; time travel by kills and level; monsters by dungeon depth **(verified)** | | 1,500 / 3,000 moves, 20 kills, level 8 | §3.5, §3.9 | `shop_weapons_late`, `battle_balron` | shown |

## 3. Details

### 3.1 World
- Four continents, one per quarter of the 168x156 map: the lands of Lord British (north-west), of the Feudal
  Lords (north-east), of the Dark Unknown (south-west), of Danger and Despair (south-east); each holds 8 towns, 2
  castles, 2 landmarks and 9 dungeons **(verified data, `gameplay_lands_*`)**.
- Terrain: water, grass, woods, mountains. On foot water and mountains block ("You can't walk on water!",
  "Mountains are impassable!"); an aircar cannot pass woods; frigates and rafts stay on water **(verified:
  `system_blocked_water`, `system_blocked_mountains`, `system_aircar_woods`)**.
- Towns use 8 plans, castles 2: town *n* and town *n*+8, +16, +24 share a plan (Britian, Arnold, Nassau and Gorlab
  look alike) **(verified, all 32 towns entered)**. Plans differ in which shops they hold: Britian's plan has all
  six, Montor's only food and weapons (`gameplay_town_montor`), Tune's sits in a moat (`gameplay_town_tune`).

### 3.2 Character creation
Six statistics start at 10; 30 points are spread with the arrows (`gen_points`, `gen_stats_mid`,
`gen_stats_done`); then race, sex, class and name (`gen_race`, `gen_sex`, `gen_class`, `gen_name`) and "Save this
character?" (`gen_save`) **(verified)**. Bonuses are added after the choice **(verified, all races and classes
tried)**:

| Choice | Bonus |
|---|---|
| Human | Intelligence +5 |
| Elf | Agility +5 |
| Dwarf | Strength +5 |
| Bobbit | Strength -5, Wisdom +10 |
| Fighter | Strength +10, Agility +10 |
| Cleric | Wisdom +10 |
| Wizard | Intelligence +10 |
| Thief | Agility +10 |

Sex changes nothing seen. Every new hero starts with 150 hit points, 200 food, 100 copper, leather armour and two
daggers **(verified, `inventory_ztats`)**. `gen_other_build` shows a female Bobbit wizard.

### 3.3 Hit points and statistics
- A king turns pence into hit points at 3 for 2: 50 pence gave 75 hits (`dialogue_king_pence`) **(verified;
  code: pence x 3 / 2)**.
- Kills inside a dungeon add up and are paid as hit points when the hero climbs out: "Thou dost gain 22 hit
  points" after one spider (`system_klimb_out`) **(verified)**.
- Landmarks raise one statistic each by (value + 8) / 10, never above 99 **(code)**: Pillars of Protection
  Agility (+3 from 28), Tower of Knowledge Intelligence (+2 from 17), Pillar of Ozymandias Wisdom (+1 from 10),
  The Sign Post and the Grave of the Lost Soul Stamina (+2 from 17), the Southern Sign Post Charisma (+2 from 13)
  **(verified)**. The Pillars of the Argonauts give a weapon instead ("You find a Mace!",
  `system_landmark_argonauts`); the Eastern Sign Post showed only its sign (`system_landmark_eastern`).

### 3.4 Combat
- Outdoors the hero attacks a direction; in dungeons straight ahead **(verified)**. Messages: "Attack with sword",
  "Hit! Spider killed!", "Thou dost find: 8 copper!" (`battle_spider_killed`); outdoors "Killed the Orc! 2
  copper! 1 silver!" (`battle_orc_killed`).
- Monster damage grows with the monster: a skeleton hits for 2, an ettin for 105, a mind whipper for 197, a
  wraith for 255 **(verified)**. Special attacks: the thief steals an item ("Thief stole a Dagger",
  `battle_thief`), the gremlin food (`battle_gremlin`), the gelatinous cube destroys armour
  (`battle_gelatinous_cube`), the mind whipper makes a "Mental attack!" (ROM text).
- One random number generator drives every roll and advances only when the game rolls, not with time **(code)**.

### 3.5 Shops and economy
- Six shop kinds: transport, armour, weapons, magic, food, pub **(verified)**. Each town names its own shops
  (Scooter's Super Duper Transport, The Tempered Steel, Mystic Melinda's ...) **(verified)**.
- Odd towns (Britian, Fawn, ...) sell Mace, Rope & Spikes, Great Sword, Amulet, Staff and the spells Open, Magic
  Missile, Ladder Down; even towns (Moon, Paws, ...) Dagger, Axe, Sword, Bow & Arrows, Wand and Unlock, Ladder Up
  **(verified in all 8 plans)**.
- Weapons grow with game time: 2 kinds under 1,500 moves, 3 from 1,500, 5 from 3,000 (`shop_weapons`,
  `shop_weapons_late`); vacuum and reflect suits, the aircar and the shuttle from 3,000 moves (`shop_armour_late`,
  `shop_transport_space`) **(verified at 1,000, 2,417, 3,100, 4,600, 6,100, 7,600, 9,100 moves)**. Pistol, light
  sword, phazor and blaster are never sold; they come from the castles' storerooms (`system_steal_storeroom`).
- Prices fall with Charisma: leather armour 45 at Charisma 13, 43 at 19; the shuttle 1,296 at Charisma 13, 1,116
  at 29 **(verified)**.
- Selling: weapons and armour only, cheaply (the dagger fetches 1 pence, `shop_weapons_sell`); "Sorry, we don't
  deal in used stuff" (transport), "we don't buy spells", "Used food? No thanks!" **(verified / ROM text)**.
- Food: packs of 10 food for 5 pence (`shop_food`, `shop_food_bought`) **(verified)**.
- Pub: ale costs 1 pence (`shop_pub`). After each ale a roll of 75 in 255 gives one of eight tips (space travel and
  the 20 vessels of an ace, the wench or lecher, the princess's reward and the gift for an 8th level ace, going back
  in time, destroying the evil gem, magic lakes and ponds, a great game, Mondain's history) **(code; four seen:
  `dialogue_pub_space`, `dialogue_pub_princess`, `dialogue_pub_mondain`, `dialogue_pub_lakes`)**. Drinking more
  ales in one visit than a quarter of Stamina can end in "Thou hast been seduced!": half the coin and 1 Wisdom
  lost **(code; not triggered here)**.
- Stealing works behind the armour, weapon and food counters and in castle storerooms; it yields a random item of
  that shop **(verified)**. Caught on a roll of 1-77 of 255 (thieves 1-37), or always once the alarm is raised;
  then "Oh no! Thou wert caught!" and the guards attack (`system_steal_caught`) **(code / verified)**.

### 3.6 Vehicles
Horse 36, cart 144, raft 324, frigate 576, aircar 900, shuttle 1,296 pence at Scooter's (Charisma 13)
(`shop_transport`, `shop_transport_space`) **(verified)**. Horse and cart are mounted ("Mount Horse",
`system_mount_horse`, `gameplay_cart`), the others boarded; X-it leaves the vehicle on its square (`system_xit`).
The frigate fires cannons ("Fire cannons: East", `system_frigate_fire`), the aircar lasers
(`system_aircar_lasers`); both reached a target 2-3 squares away and killed it in one shot **(verified)**. The
shuttle is the only way into space (`system_liftoff`).

### 3.7 Spells
Each spell is bought one charge at a time; Ready, then Cast **(verified)**. Effects seen in dungeons: Magic
Missile "VASTO!" kills an orc (`battle_magic_missile`); Kill "INTERFICIO!" destroys a lich (`system_spell_kill`);
Open "APERTUS!" opens a coffin and Unlock "PECUNIA!" a chest without the trap roll (`system_spell_open`,
`system_spell_unlock`); Ladder Down "INFERUS!" and Ladder Up "ASCENDO!" create ladders
(`system_spell_ladder_down`, `system_spell_ladder_up`); Blink "DUCIS-EDUCO!" teleports (`system_spell_blink`);
Create "STRUXI!" puts a force field across the corridor ahead, Destroy "DELIO!" removes it (`system_spell_create`,
`system_spell_destroy`) **(verified)**. Prayer "POTENTIS-LAUDIS!" does nothing outdoors (`system_cast_prayer`).
Create and Destroy fail ("Failed!") when the square ahead is not an open corridor **(verified)**.

### 3.8 Dungeons
- 10 levels of 11x11 squares per dungeon; the map is fixed per dungeon, monsters are placed at random
  **(verified: the same map on two entries)**. Squares: corridor, wall, door, secret door (looks like a wall),
  ladder down, ladder up, force field **(verified by placing each)**.
- Ladders: K-limb with the hero facing north or south on the ladder square; facing east or west gives "Thou must
  face the ladder!" (`system_klimb_facing`) **(verified)**. Climbing out of level 1 returns to the overworld (`system_klimb_out`).
- Chests (opened with Unlock): a roll of 1-75 above Agility sets off a trap that costs hit points equal to the
  level ("Thou hast set off a trap!", `system_chest_trap`); otherwise gold, up to level squared + 9
  (`system_chest_gold`) **(code / verified)**. Thieves never trigger traps **(code)**.
- Coffins (opened with Open, `gameplay_coffin`) may release a monster **(code)**.
- Monsters by depth: [content.md](content.md) §3.

### 3.9 Space
- Lift-off: a countdown 10..1 and "Thou hast lifted off!" (`system_liftoff`); a shuttle without fuel and shields
  is destroyed at once (`gameover_dead`) **(verified)**.
- Top view: planet, sun, starbase and ship (`gameplay_space_top`); flying into the planet with a shuttle lands
  ("Thou hast landed safely!", `system_landing`); other ships cannot land ("Only space shuttles are heat shielded
  for landings!", ROM text); flying into the sun destroys the ship and kills the hero ("Thy ship melts near the
  star!", `gameover_sun`) **(verified)**. HyperJump costs 100 fuel **(verified: 1000 -> 900)**.
- Sector Scan shows the 7x7 sectors; H marks sectors with enemy craft (`map_sector_scan`) **(verified: a jump
  into an H sector met a fighter)**.
- Front view: gun sight in the middle; HyperJump (front view only) streaks to the next sector
  (`system_hyperjump`); while enemies are present the view cannot be changed (`system_space_view_refused`).
- Combat: Fire costs fuel (10 per shot, verified 900 -> 890) and hits when the enemy is inside the sight's box;
  a hit destroys the fighter, +100 experience (`battle_space_hit`); enemies fire back ("Alien fires!",
  `battle_alien_fires`). The 20th kill gives "Thou hast achieved the rank of Space Ace!" (`system_space_ace`);
  later kills "Thou art still a Space ace!" **(verified)**.
- Docking at a starbase costs 500 pence and needs a vacuum or reflect suit ("The spacedoors open, exposing thee to
  a complete vacuum!"); then "Choose thy ship" **(code)**. Not reached here: see Open questions.

### 3.10 Castles, quests, princess
- Each castle has a king, guards, a jester, a prison with a princess and three storerooms (armour, food,
  weaponry) **(verified in Lord British's castle)**.
- T beside the king: "Dost thou offer pence or service" (`dialogue_king_offer`). Service gives a quest: odd
  castles send the hero to a landmark (`dialogue_king_quest`), even castles to kill a dungeon monster
  (`dialogue_king_kill_quest`); asking again: "Thou art on a quest for me already!" (`dialogue_king_busy`). The
  landmark with an open quest says "A quest has been completed!" (`system_landmark_grave_gain`), and so does the
  kill of the quest monster (`system_quest_kill`, a Gelatinous cube for the Lost King); back at the
  king: "For this I will give thee 8 points of strength" (`dialogue_quest_done`) or a gem with a hint
  (`dialogue_gem_red`, `dialogue_gem_green`, `dialogue_gem_blue`, `dialogue_gem_white`: the four hints are all
  four gems launch a time machine; the time machine must be used to win; the princess helps a space ace; take
  nine items from the storerooms) **(verified)**. The Castle of Olympus sends the hero to the Pillar of Ozymandias
  (`dialogue_king_olympus`).
- Killing the jester gives a key ("Thou hast found a key!", `system_jester_key`) that opens one of the two cells
  ("The door is open!", `system_cell_open`; without it "Thou hast not a key!", `system_no_key`); attacking people turns the guards hostile (`battle_guard`)
  **(verified)**.
- Leading the princess out: 500 hit points, pence and experience; with 20 kills and level 8 she reveals the time
  machine far to the north-west (`system_princess_reward`) **(verified)**.

### 3.11 The end
Board the time machine with all four gems (`gameplay_time_machine`, `cutscene_time_machine`; without them "Thou
canst not determine how to operate the craft at this time.", `system_time_machine_no_gems`), four pages of text
(`cutscene_launch`, `cutscene_pulled`, `cutscene_face_to_face`), then Mondain's chamber (`boss_mondain`). Get
(Gem) beside the gem costs 2,196 hit points and destroys it (`boss_gem_destroyed`); Mondain casts magic missile,
mind blaster and psionic shock (`boss_hit_mondain`), turns into a bat below 500 hit points (`boss_mondain_bat`)
and dies at 0 (`ending_victorious`); the ending text follows (`ending_text`) **(verified)**. Killed while his gem is
intact he only seems to die: "Mondain is dead!...or is he?" and the fight goes on (`boss_or_is_he`) **(verified)**.

### 3.12 Death, resurrection, saving
- 0 hit points or 0 food: "ryz, thou art dead", a skull, "Attempting resurrection!" (`gameover_dead`,
  `gameover_starved`) **(verified)**.
- Resurrection always succeeds here: the hero stands on the overworld with 99 hits and 99 food, 0 experience and
  0 coin; equipment stays (`system_resurrection`) **(verified)**.
- Q outdoors saves to the character's slot ("Quit - saving game...saved.", `save_quit`); inside towns,
  castles and dungeons "Quit - only allowed outdoors!" (`system_quit_indoors`) **(verified)**. Four slots in Character Selection (`menu_select`).

## Open questions
- Docking at a starbase: the docking ports are computed from tables (4 per starbase), but every attempt to sit on
  a port collided first ("Crunch!"); docking, "Choose thy ship" and the vacuum death are known only from code.
- The Eastern Sign Post's reward; whether coffins always release a monster; Prayer's effect in dungeons.
- The exact hit and damage formulas (outdoors and in dungeons).
- The seduction in the pub (code read, not triggered).
