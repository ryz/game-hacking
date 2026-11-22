# Ultima II: The Revenge of the Enchantress (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima-2`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
"Code" means read from the program (ULTIMAII.EXE) and tested with pokes where marked; the playbook has the
addresses.

## 1. Core loop
Walk the surface of a period, enter places, talk and trade, fight what comes near, and collect money, hit points
and items (verified: `gameplay_start`, `gameplay_village_1423`, `battle_hit_kill`). The world clock runs: waiting
passes turns, and monsters, spells and thieves act on every turn (verified: the `PASS` lines in `gameplay_start`).
Between loops the player changes period through a time door or flies a rocket to a planet, and gathers the few
things the ending needs: the quicksword, the blessing, the ring, then Shadow Guard and Minax (verified, the
whole chain is in the set from `system_enilno` to `ending_text`; Minax was killed in play, no poke).

## 2. Systems
| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | 26 one-key commands | A attack, B board, C cast, D descend, E enter, F fire, G get, H hyperwarp, I ignite, J jump, K klimb, L launch, M magic, N negate time, O offer, Q quit/save, R ready, S steal, T transact, U unlock, V view, W wear, X x-it, Y yell, Z ztats, space pass; every one tried (verified) | letter + direction or digit | - | playbook Controls | `gameplay_refusals`, `gameplay_refusals_2`, `gameplay_refusals_3`, `system_jump_ignite`, `system_yell`, `system_magic_ready`, `system_cast_none`, `system_unlock_transact`, `system_offer_steal` | shown |
| Player verbs | Real-time pass | no key for about a second and the game passes a turn ("CMD: PASS") (verified) | none | about 1 turn per second at 500 cycles | playbook | `gameplay_start`, `hud_status` | shown |
| Player verbs | Jump, Yell | Jump only prints "JUMP...WHEE..."; Yell echoes a typed word, nothing answers (code: the word is read and thrown away) | `j`; `y` + word + Enter | - | - | `system_jump_ignite`, `system_yell` | shown |
| Player verbs | Offer gold | gold in hundreds to a person; most say "THANK YOU VERY MUCH!" and keep it; Santre, the old man, the Flopy Fighter and the hotel clerk answer (verified) | `o`, direction, digit | 500 for Enilno and the ring | section 3 | `system_offer_thanks`, `system_enilno`, `system_flopy_gift`, `system_alakazam` | shown |
| Characters and progression | Generation | 90 points over six statistics, each typed as two digits; a value under 10 clears the whole form; sex, race and type add fixed bonuses (male Str +5, female Cha +10, human Int +5, elf Agi +5, fighter Str +15, wizard Int +10) (verified) | digits, M/F, 1-4, name | 90 points | [findings.md](findings.md) | `menu_generation`, `menu_gen_stats`, `menu_gen_male`, `menu_gen_human`, `menu_gen_done`, `menu_gen_other` | shown |
| Characters and progression | Level | the level is the hundreds of experience ("A LEVEL 20" at 2083) (verified) | - | dungeon kills give 0-6, surface kills 4 | - | `inventory_ztats_new`, `inventory_ztats_late` | shown |
| Characters and progression | Lord British | 50 gold buys +300 H.P. while H.P. is under 5000, +200 under 7500, +100 under 9900, nothing above (code: the test reads the two high digits of H.P.; verified +300 at 400 and at 3184) | Transact at the throne | 50 gold | [findings.md](findings.md) | `dialogue_lord_british`, `system_king_1990` | shown |
| Characters and progression | Requirements | weapon n needs Agility above 8n, armour n needs Strength above 8n, compared on the stored decimal digits read as a number (Strength 45 counts as 69) (code; verified: sword and light sword refused at Agility 20, axe readied at Agility 20 (start set `34_system_ready_refused`, `37_system_ready_axe`), power armour refused at Strength 25, worn at 45) | Ready, Wear | quicksword 9 -> Agility 49+ on screen | [findings.md](findings.md) | `system_agile_refused`, `system_strong_refused`, `system_ready_weapon`, `system_wear_armour`, `system_ready_quicksword` | shown |
| Characters and progression | Hotel clerk | 100s of gold offered: 6 times in 256 one of the six statistics rises by 4 per 100 ("ALAKAZAM!"), otherwise the gold is simply gone (code; forced roll verified: Agility 71 -> 79 for 200) | Offer | 4 per 100 gold | section 3 | `system_alakazam`, `dialogue_hotel_clerk` | shown |
| Resources and economy | Gold, food, H.P., experience | four numbers always on the panel; food falls slowly as turns pass (verified: 2463 -> 2457 over the endgame route) | - | start 400 H.P., 399 food, 400 gold | - | `hud_status`, `gameplay_start` | shown |
| Resources and economy | Shop kinds | the quarter of a towne decides the shop: north-west weapons, north-east armour, south-east transport, south-west pub; in a village: oracle, food, cleric spells, wizard spells (code; all eight verified) | Transact over a counter with the merchant two squares away | - | section 3 | `shop_weapons`, `shop_armour`, `shop_transport`, `shop_pub`, `shop_oracle`, `shop_food`, `shop_cleric`, `shop_wizard` | shown |
| Resources and economy | Prices | a weapon or armour price is a Fibonacci-like series that starts lower the higher Charisma + Intelligence are (code); at Cha 10 + Int 15: dagger 20, mace 32, axe 52, sword 136, light sword 356, leather 84, chain 220 (start set `28`, `31`, `36`, shots 2026-11-22); food 52 per 100; five lights 20, five passwalls 356; horse 84 (verified) | Y/N | see Details | section 3 | `shop_weapons_price`, `shop_weapons_sold`, `shop_armour_sold`, `shop_food`, `shop_food_buy`, `shop_cleric_buy`, `shop_wizard_buy`, `shop_transport` | shown |
| Resources and economy | Refusals | not enough gold: "YOU DONT HAVE THAT MUCH!"; spells only for clerics / wizards; N declines ("OH, WELL.") (verified) | - | - | - | `shop_weapons_poor`, `shop_weapons_no`, `shop_oracle_poor`, `system_cleric_refused`, `system_wizard_refused` | shown |
| Resources and economy | Selling | none: no shop buys anything back (ROM text has no selling messages) | - | - | - | none: the game has no selling | described |
| Resources and economy | Pub | 1-Buy costs 5 gold ("HERE, HAVE A STRONG ONE!") and a random barkeep line; 2-Tip n gold picks line (random + n), lines 3-9 are the hints (code; verified) | digits | 10 lines | section 3 | `shop_pub_buy`, `shop_pub_tip`, `shop_pub_tip_9` | shown |
| Resources and economy | Oracle | pay n x 100 gold, hear verse n of a ten-verse poem that ends with the old man under a tree (verified 0, 1, 3, 7) | digit | 100 per verse number | content.md section 7 | `shop_oracle_0`, `shop_oracle_1`, `shop_oracle_3`, `shop_oracle_7` | shown |
| Resources and economy | Steal | across a counter (merchant two squares away): two coin flips (one for a thief), then food (village north-east), armour (towne north-east) or a weapon (towne north-west); a failure that rolls 0 calls the guards (code; forced success verified) | `s` + direction | 1 in 4 (fighter), 1 in 2 (thief) | - | `system_steal`, `system_offer_steal` | shown |
| Conflict | Melee | a hit if random/2 is below Agility; damage = (weapon x 8 + Strength) / 4; the monster strikes back on its turn (code; verified 42 per quicksword hit at Str 62) | `a` + direction | quicksword 42, bare hands 17 | playbook | `battle_hit_kill`, `battle_miss`, `battle_dungeon_hit`, `battle_dungeon_kill` | shown |
| Conflict | Ranged specials | within 3 squares, 1 turn in 8: the hooded man paralyses legs (boots save 3 in 4), the robed figure arms (cloak saves), wizards cast magic missile, daemons sleep (green idol saves); 0-15 turns (code; verified) | - | 1 in 8 per turn | - | `battle_legs_boots`, `battle_arms_cloak`, `battle_magic_missile`, `battle_sleep_idol` | shown |
| Conflict | Thieves | a thief next to ryz takes something ("A THIEF STOLE SOMETHING!") (verified) | - | - | - | `battle_thief_stole` | shown |
| Conflict | Fleeing | a monster with under 15 H.P. walks away instead of closing in (code) | - | 15 | - | none: not caught on a frame (a hit usually kills outright) | described |
| Conflict | Vehicle guns | Fire from a frigate shoots in a direction; a miss or a kill like melee (verified) | `f` + direction | - | - | `battle_frigate_cannon` | shown |
| Opponents | Surface monsters | every turn the game tries to create one monster on a random square of the map; nine kinds in a fixed cycle, each needing grass or water there (code; one devil after about 20,000 idle frames, RAM) | - | H.P. 16 to 255 by kind | content.md section 3 | `battle_land_monsters`, `battle_sea_monsters`, `battle_devil` | shown |
| Opponents | Dungeon creatures | prepared per dungeon: two per level, seven pictures by depth, hit points rising with depth (RAM) | - | 16 at level 1 to 248 at level 16 | content.md section 3 | `battle_dungeon_1`, `battle_dungeon_3`, `battle_dungeon_5`, `battle_dungeon_7` | shown |
| Opponents | Minax | 255 H.P.; every hit that does not kill sends her to the mirrored chamber ("SHE'S GONE!!!"); she casts every turn (100-450 H.P. lost per turn in the verified fight: 3084 -> 600 over 8 swings, 7 hits) | - | 255 H.P. | playbook | `boss_minax`, `boss_minax_gone`, `boss_chamber_two`, `ending_minax_dead` | shown |
| Items and equipment | Weapons and armour | 9 weapons (dagger .. quicksword), 6 armours (cloth .. power); one readied / worn at a time (verified) | Ready, Wear | - | content.md section 4 | `system_ready_list`, `system_wear_list`, `inventory_ztats_late` | shown |
| Items and equipment | Special items | 16 kinds, each opening something: ring (fields), ankh (rocket), tri-lithium (fuel), blue tassle (frigates), skull key (planes), brass button (plane launch), wand or staff (casting), boots, cloak, green idol (spell saves), helm (View), strange coin (negate time) (verified for all but the gems) | - | - | content.md section 4 | `system_rocket_no_ankh`, `system_frigate_refused`, `system_plane_refused`, `system_plane_no_button`, `system_view_helm`, `system_negate_time`, `system_field_ring` | shown |
| Items and equipment | Chests | a dungeon chest gives gold (3 in 4) or else a weapon (odd levels) / armour (even levels); on level 16 always tri-lithium (code; gold and tri-lithium verified; one level-1 chest said "A  WEAPON" with no name) | `g` on the chest square | - | [findings.md](findings.md) | `gameplay_dungeon_chest`, `system_chest_gold`, `system_trilithium` | shown |
| Items and equipment | Quest gifts | Santre: Enilno for 500; the old man: the ring for 500 after the blessing; the Flopy Fighter: a random weapon for any offer (verified) | Offer | 500 | section 3 | `system_enilno`, `system_ring`, `system_earn_ring`, `system_flopy_gift` | shown |
| Abilities and magic | Spells | bought by fives in villages (clerics: light, down ladder, up ladder, passwall, surface, prayer; wizards: light, down ladder, up ladder, magic missile, blink, kill), readied with M, cast with C; casting needs a wand or staff and works only in dungeons and towers (verified) | `m` digit, `c` | one charge per cast | content.md section 5 | `system_cast_light`, `system_cast_passwall`, `system_cast_magic_missile`, `system_cast_prayer`, `system_cast_down_ladder`, `system_cast_surface`, `system_magic_ready`, `system_cast_none` | shown |
| World and navigation | Five periods | Legends, Pangea, 1423 B.C., 1990, 2112 (Aftermath), each a 64 x 64 Earth map with at most one place of each kind; the sign names the period (verified) | walk, Enter a sign | 5 maps | playbook Game structure | `system_sign_1423`, `system_sign_legends`, `system_sign_pangea`, `system_sign_1990`, `system_sign_2112`, `gameplay_surface_pangea` | shown |
| World and navigation | Time doors | a door appears after 256 turns on one of four squares per period and moves every 8 turns; stepping in leads to a fixed other period (code; verified) | walk onto it | 4 squares per period | playbook | `system_time_door`, `gameplay_legends_islet` | shown |
| World and navigation | Places | villages, townes, castles, towers, dungeons; leave a town by walking off the edge (verified) | `e` | - | content.md section 2 | `gameplay_linda`, `gameplay_castle_lb`, `gameplay_port_bonifice`, `gameplay_new_san_antonio` | shown |
| World and navigation | Dungeons and towers | first-person, 16 levels of 16 x 16; dark without a torch (150 turns per torch); dungeons go down, towers up; ladders, doors, chests (verified) | arrows, `k`, `d`, `i` | 16 levels | content.md section 2 | `gameplay_dungeon_dark`, `gameplay_dungeon`, `gameplay_dungeon_turn`, `gameplay_dungeon_retreat`, `gameplay_dungeon_door`, `system_descend`, `system_klimb_out`, `gameplay_tower`, `system_tower_klimb`, `gameplay_dungeon_level16` | shown |
| World and navigation | Traps | each step below ground springs a trap with chance level/256: the torch goes out, a tool saves ("ESCAPED! BY USE OF TOOLS!"), without tools ryz dies (code; both verified with a forced roll) | - | level in 256 | [findings.md](findings.md) | `system_trap`, `gameplay_dungeon_retreat` | shown |
| World and navigation | Vehicles | horse (bought, rides on land), frigate (needs a blue tassle, water only, cannons), plane (skull key to board, brass button to launch, flies on by itself, steered with arrows, lands only on grass), rocket (ankh) (verified) | `b`, `x`, `l`, `f`, arrows | horse 84 gold | content.md section 4 | `system_board_horse`, `gameplay_horse`, `system_board_frigate`, `gameplay_frigate`, `system_frigate_shore`, `system_board_plane`, `gameplay_plane`, `system_plane_land_refused`, `system_plane_landed`, `shop_transport_buy` | shown |
| World and navigation | Space | launch needs tri-lithium and reflect or power armour; hyperwarp by three digits costs one tri-lithium; ten destinations, the sun, deep space; landing only on grass; landing on Earth always arrives in 2112 (verified) | `l`, `h`, digits, any key | 9 planets + Earth | playbook | `gameplay_rocket`, `cutscene_launch`, `gameplay_space_earth`, `system_space_climb`, `system_hyperwarp_prompt`, `system_hyperwarp`, `gameplay_orbit_x`, `system_landing`, `gameplay_earth_2112` | shown |
| World and navigation | Space failures | no fuel ("SHIP INCAPABLE OF LAUNCH!", "NO FUEL!"), no space armour ("YOU HAVE EXPLODED!"), 4-4-4 ("YOU HIT THE SUN!"), a coordinate without a planet ("YOU ARE IN DEEP SPACE.", "REQUEST DENIED!"), fuel left with both low bits set ("SHIP OFF COURSE!") (verified) | - | - | [findings.md](findings.md) | `system_launch_no_fuel`, `system_no_fuel`, `system_exploded`, `system_sun`, `system_deep_space`, `system_off_course` | shown |
| World and navigation | View | with a magical helm, V shows the whole map of the current Earth (verified) | `v` | - | - | `system_view_helm` | shown |
| World and navigation | Doors and fields | a locked door (only east or west of ryz) opens with a key; force fields do 1,000 damage unless the ring is owned (verified) | `u`, walk | 1,000 | - | `system_unlock`, `system_unlock_nokeys`, `system_field_ring`, `system_field_damage` | shown |
| Goals and gating | Main quest | Enilno -> blessing on planet X -> ring -> Shadow Guard -> Minax; the quicksword is not checked by the code (verified) | - | - | playbook | `system_enilno`, `dialogue_father_antos`, `system_ring`, `gameplay_shadow_guard`, `boss_minax` | shown |
| Goals and gating | Clues | talk lines, pub tips and the oracle point at every step (planet X, 9-9-9, Father Antos, the old man, lithium on level 16, the clerk) (verified) | Transact, Offer | - | content.md section 7 | `dialogue_phylosopher`, `dialogue_astronaut`, `dialogue_sightless_sage`, `dialogue_balron`, `dialogue_village_idiot`, `dialogue_seaworthy_pirate`, `dialogue_warrior_x` | shown |
| Chance | Random numbers | one lagged generator for every roll; poking its state right before a key chooses the outcome (RAM) | - | - | playbook RAM map | none: a tool for capturing, not visible | described |
| Failure and recovery | Death | H.P. at 0 (or a trap without tools, launching unprotected, the sun): "RYZ IS DEAD!", the four numbers set to 0, and the program stops in an endless loop; only a restart and the last Q save remain (code; verified 2,000 frames later unchanged) | - | - | [findings.md](findings.md) | `gameover_dead` | shown |
| Saving and sessions | Q | saves on the surface of Earth only; play continues (verified; saves 01-03 made this way) | `q` | - | playbook | `save_quit` | shown |
| Pacing and difficulty | Real time | turns pass on their own, so standing still is never safe; Minax drains several hundred H.P. a turn (verified) | - | - | - | `boss_chamber_two` | shown |
| Ending | Minax dead | "MINAX IS DEAD!! ALL HER WORKS SHALL DIE!", Shadow Guard breaks apart, then the closing text over the scrolling 1990 map, no return (verified) | - | about 1,500 frames | - | `ending_minax_dead`, `ending_crumble`, `ending_text` | shown |

## 3. Details: shops and offers (verified unless marked)
| Shop / person | Where | Offer | Answers |
|---|---|---|---|
| Weapons Shoppe | towne, north-west | 1-DA 2-MA 3-AX 4-BO 5-SW 6-GR 7-LI 8-PH, price per item | "AH! YES! A SWORD FOR YOU ONLY 0136 HOW 'BOUT IT?", "SOLD!", "OH, WELL.", 0/9: "THANKS FOR COMING BY..." |
| Armour Shoppe | towne, north-east | 1-CLOTH .. 6-POWER | chain 220 at Cha 10 + Int 15 |
| Transport Shoppe | towne, south-east | a horse, 84 gold | "RIDE SWIFTLY!" (the horse waits in the stable), "O.K. BYE THEN..." |
| Pub | towne, south-west | 1-Buy (5 gold), 2-Tip (n gold) | "HERE, HAVE A STRONG ONE!", "THE BARKEEP SAYS: ..." |
| Oracle | village, north-west | n x 100 gold | verse n of the poem |
| Food | village, north-east | 100 food | "THE FOOD HERE COSTS 0052 PER 100", "NO ONIONS AND TO GO PLEASE!" (`shop_food_buy`) |
| Holy Spells | village, south-east | five of a spell, clerics only | "WELCOME BROTHER RYZ", "I WILL TAKE 5!" |
| Wizardry | village, south-west | five of a spell, wizards only, in Turkish ("MUSERREF OLDUM!", "LUTFEN EVET?", "GULE GULE!") | |
| Santre | New San Antonio jail | 500 gold | "ENILNO IS YOURS!" |
| The old man | New San Antonio, A TREE | 500 gold | "EARN THE RING!" (gold kept) or, after the blessing, "THE RING IS YOURS!" |
| Flopy Fighter | New San Antonio, At Own Risk | any amount | "HERE TAKE THIS!" and a random weapon (a phaser for 100) |
| Hotel clerk | New San Antonio, The Hotel | n x 100 | 6 in 256 "ALAKAZAM!" (+4n to one statistic), else "THANK YOU VERY MUCH!" (code) |

## 4. How the systems feed each other
- Fights give gold and experience; slain thieves, fighters, wizards and guards give the special items and keys
  (code) -> items open vehicles, magic, space and doors.
- Gold buys hit points from Lord British, food, horses, spells, statistics (clerk), and the two quest purchases.
- Statistics gate weapons and armour; armour 5+ gates space; space gates the blessing; the blessing gates the
  ring; the ring gates Shadow Guard (verified chain).
- Time doors connect the periods: the rocket is in 2112, the quest people in 1990, Minax in Legends (verified).

## Open questions
- Monster loot on a natural kill (code read, not seen: the poked monsters gave gold only); fleeing not caught.
- Blink and up ladder failed in their only tries (random or position rules not read).
- The gems (gem, red gem, green gem) have no use found in the code paths read.
