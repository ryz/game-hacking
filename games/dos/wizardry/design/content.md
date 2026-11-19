# Wizardry: Proving Grounds of the Mad Overlord (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. The rules behind the content are in [systems.md](systems.md), the screens it appears on in
[interface.md](interface.md); the same shots appear there, overlap is intended. Notation: [README.md](README.md).
Check: `python3 tools/lenses.py dos/wizardry main`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | castle menus, 10 maze floors of one wireframe look; special places by message squares | 30 | [maps](maps/floors.txt) |
| Opponents | about 100 monster kinds (source); 101 monster numbers in the encounter tables (disk data) | 30 | not decoded (names are encoded on the disk) |
| Items | 100 (verified, every name read on screen) | 30 | [items.md](items.md) |
| Abilities / spells | 21 mage + 29 priest (verified: the spell books) | 14 | §5 |
| Characters and people | 8 classes, 5 races; Boltac, Gilgamesh, Werdna, Trebor | §6 | - |

## 2. Environments
The maze has a single look (white wireframe on black, the same on all ten floors), so variety comes from the
special squares and their texts.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Castle and town menus | above ground | framed menus, no pictures | `menu_castle`, `menu_edge` |
| Lit corridor | every floor | white wireframe walls and doors | `gameplay_maze_f1_start`, `gameplay_door` |
| Darkness | floor 1 (9-10, 0-19) and others | grey view | `gameplay_dark` |
| Anti-magic | floor 5 centre, floor 7 (5,7) | spells fizzle | `system_fizzle` |
| Rock | floor 10 around the paths, floor 8 east | instant death | `gameover_rock` |
| Pits, chute | floors 2, 3, 6, 7; chute floor 9 | damage; drop to floor 10 | `gameplay_pit`, `gameplay_chute` |
| Stairs and elevators | every floor; elevators 1-4 (A-D) and 4-9 (A-F) | Y/N or button prompts | `gameplay_stairs`, `gameplay_elevator`, `gameplay_elevator_f4` |
| Floor 1 statues and signs | (9,12) out of bounds, (9,19) the robed man, (13,3) chicken-cat, (13,5) hooded man and altar, (13,18) boar | the first floor's mysteries | `dialogue_sign_f1`, `dialogue_f1_mapiro`, `dialogue_f1_chicken`, `dialogue_f1_altar`, `dialogue_f1_boar` |
| Floor 2 gates and statues | bronze smoke (8,7), silver fog (8,12), placards before the pit (13-15,11), bear (9,18), frog (12,4), locked door (4,11-12) | keys and statuettes open the way | `dialogue_f2_bronze_smoke`, `dialogue_f2_silver_fog`, `dialogue_f2_placard`, `dialogue_f2_bear`, `dialogue_f2_frog`, `dialogue_f2_door` |
| Floor 3 mosaics | (0,15) and others: "Turn left." | directions in the floor | `dialogue_f3_mosaic` |
| Floor 4 testing grounds | control center, alarm, treasure repository, monster allocation center, the desk room, the private elevator, the bear wall | Trebor's facility | `dialogue_f4_control`, `dialogue_f4_alarm`, `dialogue_f4_treasure`, `dialogue_f4_allocation`, `dialogue_f4_desk`, `dialogue_f4_private`, `dialogue_f4_asleep`, `dialogue_f4_bear_wall` |
| Floor 10 Werdna's domain | gold plaque (0,0), guardians' warning (3,14), the lair (17,3-4) | the last floor | `dialogue_f10_plaque`, `dialogue_f10_guardians`, `dialogue_werdna_sign` |

## 3. Opponents
Unidentified names as shown first; the real name where the fight revealed it.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Slime / Bubbly slime | floor 1 rooms | cyan blob | weak, comes in fours | `battle_options`, `battle_identified` |
| Kobolds, Small humanoids | floor 1 | small armed humanoids | two groups at once | `battle_f1_kobolds` |
| Skeletons | floor 1 | skeleton | undead | `battle_f1_skeletons` |
| Orcs, Undead kobolds | floor 1 | friendly groups | let the party leave | `battle_friendly`, `battle_f1_undead_kobolds` |
| Gas clouds | floor 2 | cloud; friendly or hostile | - | `battle_f2_gas_clouds`, `battle_f2_gas_clouds_hostile` |
| Lvl 1 priests | floor 2 | robed human | - | `battle_f2_priests` |
| Weird humanoids, Slimes | floor 2 | two groups | strike first | `battle_f2_humanoids` |
| Dragons (unidentified) | floor 3 | small dragon | - | `battle_f3_dragons` |
| Lvl 3 priests | floor 3 | robed human | casters | `battle_f3_priests` |
| Rotting corpses | floor 3 | zombie | undead | `battle_f3_corpses` |
| Giant rodents | floor 3 | rat | six at a time, some run away | `battle_f3_rodents`, `battle_cast_badios`, `battle_multi_hit`, `battle_mahalito`, `battle_victory_vets`, `battle_run` |
| Killer wolves | floor 3 | wolf | strike first | `battle_f3_wolves` |
| Spirits | floor 3 | ghost | - | `battle_f3_spirits` |
| Men in armor, Lvl 7 mages, High priests, Man in kimono | floor 4 guard room (fixed) | four groups of humans | Lahalito and Badialma kill a level 1 party in one round | `battle_f4_fixed`, `battle_enemy_lahalito`, `battle_badialma`, `gameover_cemetery` |
| Fire dragon | floor 7 (2,9), fixed | dragon | - | `battle_f7_dragons` |
| Wyverns | floor 7 | winged reptile, friendly | - | `battle_f7_friendly_wyverns` |
| Man in robes, Champ samurai | floor 7 | humans | - | `battle_f7_samurai` |
| Chimeras | floor 8 | three-headed beast | bite several times | `battle_f8_chimeras`, `battle_monster_bite`, `battle_use_item` |
| Arch mages | floor 8 | robed mage | cast Katino: party members fall asleep | `battle_f8_arch_mages`, `battle_enemy_katino`, `battle_party_asleep` |
| Men in armor | floor 8 | armoured fighter | - | `battle_f8_men_in_armor` |
| High priests | floor 8 | priest | - | `battle_f8_high_priests` |
| Thieves | floor 10 | thief with a blade | - | `battle_f10_thieves` |
| Lifestealer | floor 9 | ghost | undead, casts Katino; dispelled | `battle_f9_lifestealer`, `battle_dispell` |
| Vampire lord, Vampires ("unseen entities") | floor 10, Werdna's guards | ghost-like picture | drain 2 levels per touch, paralyze, cast Dilto and Molito; resist spells | `boss_level_drain`, `boss_paralyzed`, `boss_enemy_dilto`, `boss_spell_resisted`, `boss_vampires_identified`, `boss_vampire_lord_killed`, `boss_drained_after` |
| Werdna ("**W*E*R*D*N*A**", or "Man in robes" unidentified) | floor 10 (17,3) | robed wizard with a staff | boss; casts Tiltowait; 71 hit points in this fight (RAM) | `boss_werdna`, `boss_werdna_orders`, `boss_werdna_hit`, `boss_werdna_killed`, `boss_tiltowait_damage`, `boss_werdna_tiltowait`, `boss_member_killed`, `boss_four_dead`, `boss_werdna_ep` |

## 4. Items and equipment
A spread over types and tiers; the full table with numbers and prices is [items.md](items.md).

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Long sword (25), short sword, maces, staff, dagger | basic weapons | Boltac's | - | `shop_boltac_buy` |
| Shields, robes, leather, chain, breast plate, plate mail (750), helm | armour | Boltac's | lower AC | `shop_boltac_armor`, `shop_boltac_potions` |
| Potions of Dios / Latumofis, scrolls of Katino, Badios, Halito | consumables | Boltac's | cast their spell | `shop_boltac_potions`, `shop_bought`, `camp_use_item` |
| Leather+1 ... breast plate+1 (1500), staff+2, gloves of copper (6000) | magic gear | Boltac's | better AC and hits | `shop_boltac_magic`, `shop_boltac_rare` |
| Long sword+2, plate mail+2, shield+2, helm+1 | the veterans' gear | (poked, see playbook) | RYZ's AC -4 | `inventory_sheet_vet`, `camp_equip`, `shop_sell` |
| Slayer of dragons ("?SWORD") | rare weapon | found | identified by Boltac | `shop_identify`, `shop_identified` |
| Ring of Porfic | ring | found | identified by the bishop | `inventory_bishop_identify`, `inventory_identified` |
| Robe of curses ("-") | cursed armour | found | removed by Boltac's uncurse | `shop_uncurse`, `shop_uncursed` |
| Statue of bear | quest item | floor 2 statue | opens the floor 2 door (source) | `system_search_found` |
| Chest | container | after fights | trapped loot | `battle_chest`, `chest_inspect_who`, `chest_inspected`, `chest_open_who`, `chest_disarm_prompt`, `chest_disarmed`, `chest_gold`, `chest_exploding`, `chest_slain`, `chest_calfo_who`, `chest_poison_needle`, `gameplay_poisoned` |
| Werdna's amulet (item 94) | quest item | Werdna | ends the game when brought to the castle | `boss_amulet_found`, `ending_congratulations` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| HALITO | mage 1 | 1 point of level 1 | fire at one monster | `battle_spell_prompt`, `battle_cast` |
| KATINO | mage 1 | - | puts a group to sleep; monsters cast it at the party | `battle_enemy_katino` |
| DUMAPIC | mage 1 | - | tells the position | `system_dumapic` |
| MAHALITO, LAHALITO | mage 3, 4 | - | fire at a group | `battle_mahalito`, `boss_spell_resisted`, `battle_enemy_lahalito` |
| DILTO | mage 2 | - | darkness on a group (cast by the vampires) | `boss_enemy_dilto` |
| MALOR | mage 7 | - | teleport by offsets (in camp) | `camp_malor` |
| TILTOWAIT | mage 7 | - | huge damage to every monster (or every member, when Werdna casts it) | `boss_werdna_killed`, `boss_tiltowait_damage`, `boss_werdna_tiltowait` |
| CALFO | priest 2 | - | names a chest's trap | `chest_calfo` |
| DIOS | priest 1 | - | heals one member | `camp_cast_whom` |
| BADIOS | priest 1 | - | wounds one monster | `battle_cast_badios` |
| LITOKAN | priest 5 | - | flames on a group | `boss_werdna_orders` |
| BADIALMA | priest 5 | - | wounds; cast by high priests | `battle_badialma` |
| Dispell | priest, bishop, lord | none | destroys undead | `battle_dispell` |
| All 21 mage and 29 priest spells | books | - | - | `inventory_mage_book`, `inventory_priest_book` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Fighter, Priest, Thief, Mage, Bishop (the party: ryz, condi, ebo, cubi, deddo, mnz) | playable classes | Training Grounds | `inventory_roster`, `menu_castle` |
| Elf mage ZED, changed to fighter | a throwaway character | Training Grounds | `training_inspect_new`, `training_class_changed` |
| Samurai, Lord, Ninja | elite classes, high statistics | Training Grounds | - (no character qualified; described) |
| Pre-made characters Tarkin, Shreev, Curtis, Kimbal, Tivis, Mewo | ready-made level 1 party on the scenario disk | Tavern | `menu_tavern_add` |
| Gilgamesh, Boltac | tavern keeper, merchant (names only) | Castle | `menu_tavern`, `shop_boltac` |
| A small man in a long robe | chants "Mapiro mahama diromat" and sends the party away | floor 1 (9,19) | `dialogue_f1_mapiro` |
| Werdna | the evil wizard | floor 10 | `boss_werdna` |
| Trebor, the Mad Overlord | quest giver (in the ending text) | castle | `ending_congratulations` |

## Open questions
- Monster names are stored encoded on the disk; a full monster table needs the decoder (the encounter tables
  give monster numbers per floor, `../tools/maps.py` disk offsets).
- Murphy's ghost (floor 1 (13,5)) was not met: see findings.
