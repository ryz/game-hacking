# Ultima II: The Revenge of the Enchantress (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima-2`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 5 Earth surfaces, 9 planet surfaces, about 20 town and castle maps, 9 dungeon and tower files of 16 levels | section 2 | `tools/u2map.py --list` |
| Opponents | 9 surface monster kinds, 7 dungeon creature pictures, 8 kinds of town people, Minax | section 3 | section 3 |
| Items | 16 special items | section 4 | playbook Game structure |
| Equipment | 9 weapons, 6 armours | section 4 | section 4 |
| Vehicles | horse, frigate, plane, rocket | section 4 | - |
| Abilities / spells | 9 spells (light and the ladders for both schools) | section 5 | section 5 |
| Characters and people | the hero (4 races, 4 types, 2 sexes); 4-5 named talkers in every town | sections 6 and 7 | section 7 |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Today's continents | 1423 B.C., 1990, 2112 surfaces | the same coasts, different places in each period (verified) | `gameplay_start`, `system_sign_1990`, `system_sign_2112` |
| Pangea | 9,000,000 B.C. | one supercontinent of grass, woods and hills (verified) | `gameplay_surface_pangea`, `system_sign_pangea` |
| Legends | Time of Legends | a round island; Shadow Guard in a ring of mountains with an army of monsters drawn into the map outside; a walled islet with the sign and the door squares (verified) | `gameplay_legends_islet`, `gameplay_legends_army` |
| Village | each period but Legends | four shops in the quarters, named houses (Le Jester, Port Bonifice, Pirates Harbour) (verified) | `gameplay_village_1423`, `gameplay_village_pangea`, `gameplay_port_bonifice`, `gameplay_pirates_harbour` |
| Towne | Linda (1423 B.C.), New San Antonio (1990) | brick floors, grey walls, the four towne shops, a jail (verified) | `gameplay_linda`, `gameplay_new_san_antonio` |
| Castle | Lord British (1423 and 1990), Shadow Guard, Ozys Place | throne hall with pillars; Shadow Guard's force-field gate and two chambers (verified) | `gameplay_castle_lb`, `gameplay_shadow_guard`, `gameplay_ozys_place` |
| Launch site and airfield | Pirates Harbour (2112) | "CCCP TEST LAUNCH", three rockets, a control house, twelve planes, a frigate dock (verified) | `gameplay_launch_site`, `system_board_plane`, `system_board_frigate` |
| Dungeon | 1423 B.C., Pangea, 1990, 2112, Mercury, Jupiter, Pluto | wireframe corridors going down 16 levels; level 16 has chests of tri-lithium (verified) | `gameplay_dungeon`, `gameplay_dungeon_door`, `gameplay_dungeon_level16` |
| Tower | 1423 B.C., 1990, Jupiter | the same wireframe, going up (verified) | `gameplay_tower` |
| Space | anywhere above Earth | star field, hyperwarp tunnel (verified) | `gameplay_space_earth`, `system_hyperwarp` |
| Mercury | 5-4-5 | a crater ring of hills on grey plains, a dungeon (verified) | `gameplay_mercury` |
| Venus | 3-3-4 | marsh and sea, nothing to enter (verified) | `gameplay_venus` |
| Mars | 6-2-3 | mountains; Towne Mary (verified) | `gameplay_mars`, `gameplay_towne_mary` |
| Jupiter | 1-3-4 | woods and lakes; village, tower, dungeon (verified) | `gameplay_jupiter` |
| Saturn | 2-8-5 | woods and water, nothing to enter (verified) | `gameplay_saturn` |
| Uranus | 9-4-6 | woods; the village New Jester (verified) | `gameplay_uranus`, `gameplay_new_jester` |
| Neptune | 4-0-5 | all grass; the village Computer Camp (verified) | `gameplay_neptune`, `gameplay_computer_camp` |
| Pluto | 0-1-4 | mountains and woods; Towne Marler, a village, a dungeon (verified) | `gameplay_pluto`, `gameplay_towne_marler` |
| Planet X | 9-9-9 | Ozys Place (Castle Barataria inside) and Towne Basro (verified) | `gameplay_planet_x`, `gameplay_towne_basro` |

## 3. Opponents
| Opponent | Where met | Picture | What it does | Shots |
|---|---|---|---|---|
| Devil | surface grass (kind 1 of the creation cycle, 16 H.P.) | horned beast | melee; 3 gold, 4 experience (verified); the start set's devil (met in play on the walk to Towne Linda) gave 11 gold, 2 experience and took 4 swings with bare hands at Agility 20 (start set `20`-`22`) | `battle_devil`, `battle_hit_kill`, `battle_land_monsters` |
| Thief | surface (kind 2, 32 H.P.), towns | cloaked figure | steals from ryz when adjacent (verified) | `battle_thief_stole`, `dialogue_thief` |
| Hooded man | surface (kind 3, 64 H.P.) | figure with a staff | paralyses legs from up to 3 squares (verified) | `battle_legs_boots` |
| Sea serpent | water (kind 4, 64 H.P.) | coiled serpent | melee from the water (code) | `battle_sea_monsters`, `battle_frigate_cannon` |
| Fighter | surface (kind 5, 128 H.P.), towns | armed man | melee (code) | `battle_land_monsters`, `dialogue_fighter` |
| Pirate frigate | water (kind 6, 160 H.P.) | ship | sails at ryz (code) | `battle_sea_monsters` |
| Robed figure | surface (kind 7, 192 H.P.) | hood and robe | paralyses arms (verified) | `battle_arms_cloak` |
| Wizard | surface (kind 8, 224 H.P.), towns | robed with a staff | magic missile, 114 H.P. in the verified hit (verified) | `battle_magic_missile`, `dialogue_wizard` |
| Winged daemon | surface (kind 9, 255 H.P.), Shadow Guard | winged figure | sleep spell; guards Minax (verified) | `battle_sleep_idol`, `boss_minax` |
| Dungeon creatures 1-7 | dungeons and towers, two per level | seven wireframe-shaded pictures from a horned insect (1) to a many-legged horror (7) | melee; 16 H.P. on level 1 to 248 on level 16; gold from a kill (verified) | `battle_dungeon_1`, `battle_dungeon_3`, `battle_dungeon_5`, `battle_dungeon_7`, `battle_dungeon_hit`, `battle_dungeon_kill` |
| Town guard | town gates | soldier | carries keys (code) | `dialogue_guard` |
| Minax | Shadow Guard, Chamber One / Two | robed enchantress | casts every turn, jumps between chambers (verified) | `boss_minax`, `boss_minax_gone`, `boss_chamber_two`, `dialogue_minax` |

## 4. Items, equipment and vehicles
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Dagger .. phaser | weapons 1-8 | weapons shops, chests, the Flopy Fighter (verified) | damage (n x 8 + Str) / 4 (code) | `shop_weapons`, `system_flopy_gift` |
| Light sword | weapon 7 | weapons shop, 356 gold (verified) | needs Agility 39+ on screen (code) | `shop_weapons_sold`, `system_agile_refused` |
| Enilno, the quicksword | weapon 9 | Santre, 500 gold (verified) | best weapon, 42 per hit at Str 62 (verified) | `system_enilno`, `system_ready_quicksword` |
| Cloth .. power armour | armour 1-6 | armour shops (verified) | reflect or power needed for space (verified) | `shop_armour`, `shop_armour_sold`, `system_strong_refused` |
| Ring | quest item | the old man, after the blessing (verified) | walk through force fields (verified) | `system_ring`, `system_field_ring` |
| Ankh | special | thieves (code) | board a rocket (verified) | `system_rocket_no_ankh` |
| Tri-lithium | special | dungeon level 16, thieves (verified) | rocket fuel, one per launch and jump (verified) | `system_trilithium`, `system_launch_no_fuel` |
| Blue tassle | special | thieves; sailors (pub tip) | board a frigate (verified) | `system_frigate_refused` |
| Skull key, brass button | special | thieves (code) | board a plane, launch it (verified) | `system_plane_refused`, `system_plane_no_button` |
| Helm | special | fighters (code) | View shows the whole map (verified) | `system_view_helm` |
| Strange coin | special | thieves (code) | negate time for 20 turns (code) | `system_negate_time` |
| Boots, cloak, green idol | special | thieves, fighters (code) | save from paralysis and sleep (verified) | `battle_legs_boots`, `battle_arms_cloak`, `battle_sleep_idol` |
| Wand | special | wizards (code) | needed to cast (verified) | `system_cast_none`, `system_cast_light` |
| Torch | supply | fighters (code) | light below ground for 150 turns (code) | `gameplay_dungeon` |
| Horse | vehicle | transport shoppe, 84 gold (verified) | rides on land (verified) | `shop_transport_buy`, `system_board_horse`, `gameplay_horse` |
| Frigate | vehicle | docks of Port Bonifice and Pirates Cove (verified) | water only, cannons (verified) | `gameplay_frigate`, `system_frigate_shore`, `battle_frigate_cannon` |
| Plane | vehicle | the airfield of Pirates Harbour (verified) | flies on its own, lands on grass (verified) | `gameplay_plane`, `system_plane_landed`, `system_plane_land_refused` |
| Rocket | vehicle | CCCP Test Launch (verified) | space (verified) | `gameplay_rocket`, `gameplay_vehicle_hall` |

## 5. Abilities and spells
| Spell | School | Cost (5 charges) at Cha 10 + Int 15 | What it does | Shots |
|---|---|---|---|---|
| Light | both | 20 (verified) | lights the dungeon like a torch (verified) | `system_cast_light`, `shop_cleric_buy` |
| Down ladder | both | - | down one level without a ladder (verified) | `system_cast_down_ladder` |
| Up ladder | both | - | up one level (failed in the one try) | none: failed when tried |
| Passwall | cleric | 356 at the wizards' counter (verified) | removes the wall ahead (verified) | `system_cast_passwall`, `shop_wizard_buy` |
| Surface | cleric | - | straight out to the surface (verified) | `system_cast_surface` |
| Prayer | cleric | - | a 1 in 2 chance to kill the creature ahead (code; a kill verified) | `system_cast_prayer` |
| Magic missile | wizard | - | damage to the creature ahead (verified kill) | `system_cast_magic_missile` |
| Blink | wizard | - | jump to a random square of the level (code; failed in the one try) | none: failed when tried |
| Kill | wizard | - | kills the creature ahead (verified, frame not kept: same picture as the magic missile) | none: same frame as `system_cast_magic_missile` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| ryz | the hero: male human fighter (also shown: a female elf wizard build) | everywhere | `inventory_ztats_new`, `inventory_ztats_late`, `menu_gen_other` |
| Lord British | king, sells hit points for tribute | castles of 1423 B.C. and 1990 (verified) | `dialogue_lord_british`, `system_king_1990` |
| Santre the Swashbuckler | jailed, sells Enilno | New San Antonio jail (verified) | `dialogue_santre`, `system_enilno` |
| The old man | under A TREE, sells the ring | New San Antonio (verified) | `dialogue_old_man`, `system_earn_ring`, `system_ring` |
| The Flopy Fighter, the hotel clerk | gifts for gold | New San Antonio (verified) | `dialogue_flopy_fighter`, `dialogue_hotel_clerk`, `system_alakazam` |
| Father Antos | blesses | Ozys Place, planet X (verified) | `dialogue_father_antos` |
| Brother Antos | his son, sends ryz to the stars | Lord British's castle (verified) | `dialogue_brother_antos`, `dialogue_brother_antos_1990` |
| Shopkeepers | weapons, armour, horses, pub, oracle, food, spells | towns (verified) | `shop_oracle`, `shop_pub` |
| Stock town people | guard, merchant, jester, fighter, cleric, wizard, thief: one line each | towns (verified) | `dialogue_guard`, `dialogue_merchant`, `dialogue_jester`, `dialogue_fighter`, `dialogue_cleric`, `dialogue_wizard`, `dialogue_thief` |
| Cameos | Robert Woodhead, John and Gerry Mayer, Richard Garriott, Marlin Perkins, Homer the Salesman ... | towns of Earth and the planets (verified, section 7) | `dialogue_woodhead`, `dialogue_john_mayer`, `dialogue_richard_garriott`, `dialogue_marlin_perkins`, `dialogue_homer` |

## 7. Talk lines
Every named person's line, in the order of the talk file (person types 81, 82, ... in the map's object list; `tools/u2town.py MAP` shows where they stand). Text as the game shows it (ROM text).

| Place | Lines |
|---|---|
| Shadow Guard (Legends castle) | The she-creature begs: Take me I'm yours! / Homer the Salesman asks: Ya want some life insurance? / David Alpert whimpers: I've done a bad thing... / Minax cries: A coward dies a thousand deaths, a hero only one. Either way, you lose!!! |
| village of Pangea | An astronaut claims: There is a planet 'X'! / An astronaut claims: Father Antos lives on 'X' / The druid: Anol nathrac uth das bessod dien doch dientes! / The Phylosopher theorizes: She's GOT to be at 9-9-9! |
| village of 1423 B.C. | Grendel the Bum says: Masters of riddle are masters indeed! / Andy Greenberg complains: What? No software?!? / Robert Woodhead exclaims: Copy protect! Copy protect! / The chaste nubile nymph asks: Visit the Hotel California? |
| Towne Linda (1423 B.C.) | Ithilian the Wench calls: Make me an offer sailor! / John Mayer orders: TAKE OUT THE TRASH!!! / Gerry Mayer proclaims: We know small computers! / Keith says: No thanks, trying to cut down. |
| Lord British's castle (1423 B.C.) | Brother Antos ordains: Search the stars for my kin! / Bishop Bob preaches: Confess to Brother Antos! / Andre the French chef burps: I drink therefore, I am! / Commander Decker screams: Is it soup yet?!! / The wandering bard asks: Do you know the way to San Jose? |
| village of 1990 A.D. | Lady Sherrie cries: Gag me with a spoon! / Ronall Mc Donall sings: Try our new Ride-Through! / The Sightless Sage says: Find the Father Earn the Ring! / Lady Mary Ellen pleads: Beat me kick me tell me lies! |
| New San Antonio (1990 A.D.) | Santre the Swashbuckler warns:Beware, I've a quick blade! / An old man mumbles: I'm an old man. / The Flopy Fighter brags: I own one of everything! / A clerk states: Welcome to the Hotel California! |
| castle of 1990 A.D. | Brother Antos inquires: Have you found my father? / Sister Sledge sings: We are family! / Andre the French chef says: Hic, wan som colduck, hic? / The merchant orders: Give the King a tribute! / The subdued balron whimpers: Lithium packs the 16th level! |
| village of 2112 A.D. | Waren Beatty asks: Have you seen Diane Keaton? / Chuckles the Bumble cries: Can I look yet, is it over? / The Village Idiot suggests: Offer the hotel clerc gold! / Red the Pirate boasts: I've a broken Ultima ]I[, want one? |
| towne of Mars | Marlin Perkins threatens: Go in and I'll zap you! / Owen K. Garriott asks: Have you seen my shuttle? / Hecate chants: Bubble bubble toil and trouble! / The Historian declares: George Washington slept here! |
| village of Jupiter | The Jocker laughs: You're half way there! / The Pirate chortles: I own 30 tassles! / Dupre the Swashbuckler asks: Wanna buy a duck? / Johnny Jones asks: Know where I can get a duck? / U bother me! |
| village of Uranus | The Swamp Jester laughs: You lose, cadet! / The Court Jester says: Isn't this a silly Place? / The French Jester begs: Manger moi! / The Stoned Jester complains: Rocks have spirits, too! |
| village of Neptune | Debbie the lifeguard yells: Get a big grip! / Richard Garriott promises: Tomorrow--for sure! / Howie the Pest hounds: Isn't Ultima ][ finished yet? / Johnathon Ben asks: This ever happen to you? |
| village of Pluto | Margot Tommervik exclaims: Talk softly to me! / Al Tommervik inquires: Do you read me? / Big Bob jaws: Give Bill 300 gold! / Bill Bruiser demands: Give Bob 600 gold! |
| towne of Pluto | The Seaworthy Pirate says: See the clerk in New San. / The Burly Pirate says: New San. is full of magic! / The Ugly Smelly Pirate says: Antos is the answer! / The Big Bouncer stalls: Where the hell is your I.D.? |
| towne of planet X | Ugly Irving states: No mages allowed! / Kieth Zabalaoui says: I've never done this before! / An experienced warrior says: Find Antos, earn the Ring! / A wimpy warrior squeals: Antos is on 'X'! |
| Ozys Place (planet X castle) | Father Antos chants: You have earned my blessing. Return and claim the Ring! / Sing Lee the cook yells: Kichen clost, com bac lato! / Justin the Jailer warns: I wouldn't go in there! / Queen Susan says: Father Antos awaits you! |


Shots of these lines (one or more per town): `dialogue_grendel`, `dialogue_nymph`, `dialogue_ithilian`,
`dialogue_keith`, `dialogue_bishop_bob`, `dialogue_bard`, `dialogue_astronaut`, `dialogue_astronaut_2`,
`dialogue_phylosopher`, `dialogue_sightless_sage`, `dialogue_balron`, `dialogue_merchant_tribute`,
`dialogue_village_idiot`, `dialogue_red_pirate`, `dialogue_queen_susan`, `dialogue_sing_lee`,
`dialogue_ugly_irving`, `dialogue_warrior_x`, `dialogue_jocker`, `dialogue_seaworthy_pirate`,
`dialogue_big_bouncer`, `dialogue_minax`. Pub tips and the oracle's verses: `shop_pub_tip`, `shop_pub_tip_9`,
`shop_oracle_0`, `shop_oracle_1`, `shop_oracle_3`, `shop_oracle_7`.

The oracle's poem, verse n for n x 100 gold (verified 0, 1, 3, 7; the order of the rest from the ROM text):
0 ASK ME NO QUESTIONS, I'LL TELL YOU NO LIES. / 1 THE QUEEN IS THE KING AND THE KING IS A SPY. / 2 THE EVIL MEN
DO IS A HORRIBLE THING. / 3 BUT DISPELLING MEANS THAT YOU MUST HAVE THE RING. / 4 JUST WHERE IT IS, I CANNOT SAY.
/ 5 BUT I'LL TELL YOU RIGHT NOW, THERE IS NO OTHER WAY. / 6 I HEAR IN A TOWN WHERE THE WATER RUNS FREE. / 7 THERE
IS AN OLD MAN LIVING UNDER A TREE. / 8 HE HAS NOT A NAME BUT HE DOES HAVE A CLUE / 9 MAYHAPS IF YOU FIND HIM,
HE'LL TELL IT TO YOU!

## Open questions
- The second Uranus village file (mapg61) has a talk file but no named person in its object list; the jesters'
  lines were not heard.
- Gems (gem, red gem, green gem): no use found.
