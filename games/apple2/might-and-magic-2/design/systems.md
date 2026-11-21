# Might and Magic II: Gates to Another World (Apple II) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/might-and-magic-2`.
The DOS port (`games/dos/might-and-magic-2/design/`) is the same game; its documents hold the details (world
table, event texts, the ending) that were not re-measured here. This file states what was seen on the Apple II.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
Shot ids are those of set `main` (`../shots/main/index.md` gives the file names); `start NN_...` are set `start`.

## 1. Core loop
Walk the party square by square through an area, meet fixed and random encounters, fight them in turn-based
menus, search for treasure, and return to a town to spend the gold on training, equipment, spells, skills and
healing; sign in at an inn to save **(verified: walking, fights, victory, training, shops, inn; set `start`
plays one loop from creation to the first defeat and the first save)**. Between loops the party grows in level,
buys secondary skills that open new terrain, and follows quest texts to new areas and to the 9th century
**(verified: skills offered, year 800 reached by memory, Castle Xabran and King Kalohn seen)**. The quest ends
at the gate under Square Lake with Sheltem's fight **(verified: the fight; not won here, see Open questions)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move and turn | one square forward or back, 90-degree turns; a turn fires the square's event like a step **(verified)** | arrows (Return = forward) | areas 16 x 16 | [README.md](README.md) | `gameplay_inn_start`, `env_middlegate_street`, `gameplay_outdoors_c2`, `start 24_street` | shown |
| Player verbs | Bash | B against a wall: "Solid!" **(verified)**; a locked door not tried | `b` | - | - | `system_bash` | shown |
| Player verbs | Search | looks for treasure on the square **(verified: "Search... Nothing here!")** | `s` | - | - | `system_search_nothing`, `cave_x_marks` | shown |
| Player verbs | Rest | restores hit and spell points; four rests make one day **(verified: Day 1 to 2 after four rests)**; out of one's own century a rest can send the party back to year 900 **(RAM: rest code)** | `r`, `y` | - | [findings.md](findings.md) | `system_rest_prompt`, `system_rest_done` | shown |
| Player verbs | Exchange | swaps two marching positions **(verified)** | `e`, two digits | - | - | `system_exchange`, `system_exchange_done`, `battle_exchange` | shown |
| Player verbs | Protect panel | light count, magic and forces protection in force (P; O turns the panel back to the command list) **(verified)** | `p`, `o` | Light (1) after one cast **(verified)** | - | `system_protect`, `system_light`, `battle_protect` | shown |
| Player verbs | Location / automap (Cartographer) | coordinates of the square and an arrow; with a Cartographer in the party every square stepped on is remembered per area (60 bitmaps of 32 bytes, aux RAM `10200 + 32*area`, kept across area changes) and `m` draws those squares with their walls, doors or terrain: 18 squares walked in Middlegate show as a corridor; a poke of all bits shows the whole 16x16 area **(verified, RAM)**. A party poked onto a square (`AT`, warp) marks nothing until it steps; a warp marks its landing square **(verified)** | `m` (not on the command list) | Otto Mapper teaches Cartographer for 10 gold | - | `system_location`, `automap_partial`, `automap_middlegate`, `automap_c2`, `automap_cavern` | shown |
| Player verbs | Controls | sounds, walk beep, party disposition (Inconspicuous to Thrill Seeker), message delay 0-9 **(verified)** | `c`, `1`-`4` | - | - | `options_controls`, `battle_delay` | shown |
| Player verbs | Dismiss | sends a member or hireling away **(verified: prompt "Dismiss whom (1-6)?")** | `d` | - | - | `system_dismiss` | shown |
| Player verbs | Unlock | opens locked doors with thievery **(source: command list)** | `u` | - | - | none: no locked door was met on the routes taken | described |
| Player verbs | Character sheet | quick ref, cast, drop, equip, gather, remove, share, trade, use **(verified: all but use)** | `1`-`6`, letters | backpack 6, equipped 6 **(verified)** | - | `inventory_profile_vet`, `inventory_equip_prompt`, `inventory_equipped`, `inventory_remove_prompt`, `inventory_removed`, `inventory_drop_prompt`, `inventory_dropped`, `system_trade_what`, `system_trade_done`, `system_share_done`, `system_gather_done` | shown |
| Characters and progression | Creation | seven statistics rolled, two may be exchanged, eligible classes numbered, then race, alignment, sex, name; Return saves and rolls the next **(verified)** | Return re-rolls, letters exchange | first roll after `MENU`: Might 16 ... Luck 14 **(verified)** | - | `create_roll`, `create_exchange`, `create_race`, `create_alignment`, `create_sex`, `create_name`, `start 13_create_next` | shown |
| Characters and progression | Roster | 24 characters kept at the inns, premade six, renaming and deleting **(verified)** | `v`, Ctrl-N, Ctrl-D | - | - | `menu_view_all`, `inventory_premade`, `menu_rename`, `menu_inn_list` | shown |
| Characters and progression | Classes | Knight, Paladin, Archer, Cleric, Sorcerer, Robber, Ninja, Barbarian; combat options depend on class **(verified)** | - | - | - | `create_roll`, `battle_options_knight`, `battle_screen`, `battle_options_archer` | shown |
| Characters and progression | Experience and training | experience is paid for at a training ground, one level at a time **(verified)** | `y` | level 2 needs 1,500; ryz at 601,337 needs 166,663 more for level 12 (768,000) **(verified)** | - | `system_training`, `system_training_need`, `start 31_training_need` | shown |
| Characters and progression | Spell levels | casters gain spell levels with level **(source; SL 5 at level 10-11 verified)** | - | - | - | `inventory_profile_mnz`, `system_spell_prompt` | shown |
| Characters and progression | Secondary skills | bought from trainers in towns and caverns; Brain Detoxification removes them **(verified: offers, Cartographer learned)** | `y`, member | Cartographer 10, Crusader 250, Athlete 500, Merchant 1000, Hero 1000, Pathfinder and Mountaineer 2000, river walking 50 gold **(verified)** | - | `system_otto_mapper`, `inventory_skill_learned`, `system_pathfinder`, `system_mountaineer`, `system_detox`, `system_athlete`, `system_hero_skill`, `system_crusader`, `system_merchant`, `system_river_walker` | shown |
| Characters and progression | Thievery | robbers' skill on the profile; thief trainers raise it **(verified: Thievery 0% at creation; Rinaldo Jr. 700 gold offer)** | - | - | - | `inventory_profile_ryz`, `system_thief_trainer` | shown |
| Characters and progression | Ageing | characters age; the profile shows the age **(verified: 18 at creation)** | - | - | - | `inventory_profile_ryz` | described |
| Characters and progression | Hirelings | freed prisoners become hirelings kept at the inn **(source: DOS texts)**; the hireling page is empty at the start **(verified)** | inn list Space | - | - | `menu_hirelings` | described (no hire played) |
| Resources and economy | Gold | shops take gold from the shopper; trade, share and gather move it **(verified)** | trade, share, gather | trade 500 to condi; share and gather change ryz's gold **(verified)** | - | `system_trade_done`, `system_share_done`, `system_gather_done`, `shop_blacksmith_bought` | shown |
| Resources and economy | Starting money | new and premade characters start with 0 gold, 0 gems, 10 food: nothing in Middlegate is affordable at first (Sir Felgar has 200) **(verified)** | - | - | - | `start 26_blacksmith_menu`, `start 29_temple_menu`, `inventory_premade` | shown |
| Resources and economy | Food | bought at taverns, 40 at most per member **(verified: feeding frenzy fills each to 40)** | tavern `a` | - | - | `hud_food_frenzy` | shown |
| Resources and economy | Gems | pay for bribes and higher spells **(source; bribe option verified)** | - | - | - | `battle_bribe` | shown |
| Resources and economy | Blacksmiths | weapons, specials (+1 items), armor, misc, sell, identify **(verified)** | letters | Dagger 8, Cudgel 15, Nunchakas 30; +1 Staff 80; Helm 30; a Cudgel sells for 4 **(verified)** | - | `shop_blacksmith_door`, `shop_blacksmith_menu`, `shop_blacksmith_weapons`, `shop_blacksmith_specials`, `shop_blacksmith_armor`, `shop_blacksmith_misc`, `shop_blacksmith_bought`, `shop_blacksmith_sell`, `shop_blacksmith_identify` | shown |
| Resources and economy | Taverns | food, drinks, specialties, tips, a rumor after a tip **(verified)** | letters | drinks 5-100, specialties 10-100, tip 1 gold **(verified)** | - | `dialogue_waitress`, `shop_tavern_menu`, `shop_tavern_drinks`, `shop_tavern_specialties`, `shop_tavern_tip`, `dialogue_tavern_rumor` | shown |
| Resources and economy | Temples | restore condition and alignment, donations, three cleric spells **(verified: menu)** | letters | donation 100 **(verified)** | - | `system_temple`, `shop_temple_menu`, `shop_temple_donation`, `shop_temple_spell_refused` | shown |
| Resources and economy | Mage guilds | membership 20 gold; members buy sorcerer spells **(verified: offer, refusal to non-members)** | `y` | illusionists' guild 10,000 **(verified: offer)** | - | `system_mage_guild`, `dialogue_sages`, `shop_sages_members_only`, `system_illusionist` | shown |
| Resources and economy | Other services | locksmith keys, Otto Mapper, travel agent, gemmaker (Enchant Item) **(verified: offers)** | `y` | key 500, Murray's Resort Isle 5,000 **(verified)** | - | `system_locksmith`, `system_travel_agent`, `system_travel_booked`, `system_gemmaker` | shown |
| Conflict | Encounter options | attack, bribe (food, gold, gems), hide, run **(verified)**; hide failed into combat, run left the fight **(verified)** | letters | - | - | `battle_encounter`, `battle_bribe`, `battle_hide`, `battle_run_away`, `start 36_orcs` | shown |
| Conflict | Surprise | either side can be surprised **(verified: "The monsters surprised you!")** | - | - | - | `battle_sl_wizards`, `battle_sl_enchantress` | shown |
| Conflict | Combat round | members act by speed (mnz the sorcerer first); options per class: attack, fight (pick a target), cast, use, block, run, exchange, view; D delay, P protection, Q quick reference **(verified)** | letters | - | - | `battle_screen`, `battle_options_archer`, `battle_options_knight`, `battle_cast_target`, `battle_view`, `battle_exchange`, `battle_quickref`, `battle_delay`, `battle_protect` | shown |
| Conflict | Hits and spells | a fighter strikes several times per round; a spell names its damage **(verified: ebo 3 hits for 13 points; Flame Arrow 5 points)** | - | - | - | `battle_fight_hit`, `battle_spell_hit`, `battle_monster_hits`, `start 39_orc_hurt` | shown |
| Conflict | Monster behaviour | strike, breathe (damage follows the monster's remaining hit points: 0 when they were set to 0), run away **(verified, RAM)** | - | Sheltem 500 hit points, Elementals 250 **(RAM)**; Sheltem hits 8 times for 208 **(verified)** | [findings.md](findings.md) | `boss_sheltem_fight`, `boss_sheltem_breath`, `battle_monster_hits` | shown |
| Conflict | Victory | survivors share the experience; the game counts battles won **(verified: 416 each, 1st battle)** | - | - | - | `battle_victory` | shown |
| Conflict | Defeat | when every member is down: Insert Disk B, "Death Strikes! ... resume adventuring at the inn in which you last stayed", Return: the inn list, party empty, everyone alive **(verified, set start)** | Return | ten Orcs beat the level-1 party **(verified)** | - | `gameover_death_strikes`, `gameover_sheltem`, `start 41_death_strikes`, `start 42_inn_after_death` | shown |
| Opponents | Fixed groups | squares hold fixed fights with picture, list and "+N More" **(verified)** | - | up to 13 shown (8 + 5 more Skeletons), 66 Devil Kings **(verified)** | [content.md](content.md) | `battle_skeletons`, `battle_blood_suckers`, `battle_brain_eaters`, `battle_vulcania_cavern`, `battle_square_lake_devils` | shown |
| Opponents | Bosses | Jouster, Queen Beetle, Mega Dragon, Sheltem with four Elementals **(verified)** | - | - | - | `boss_jouster`, `boss_queen_beetle`, `boss_mega_dragon`, `boss_sheltem_options` | shown |
| Items and equipment | Equipment | six equipped slots, six backpack slots; equipping raises armor class **(verified: AC 3 to 13 with Chain Mail, Large Shield, Helm)** | profile `e`, `r`, `d` | - | - | `inventory_equipped`, `inventory_removed` | shown |
| Items and equipment | Identification | the blacksmith identifies: class, equipable, use, charges, damage **(verified: Large Club damage 1-4)** | `f` | - | - | `shop_blacksmith_identify` | shown |
| Items and equipment | Quest items | Element Orb, four Talons, discs of Castle Xabran, Lava Grenade, Admit 8 Pass **(verified: texts)** | events | - | - | `dialogue_element_orb`, `dialogue_xabran_disc`, `gameplay_lava_grenade`, `dialogue_zombie_pass` | shown |
| Abilities and magic | Casting | level and number, then a target if the spell needs one; the spell book shows known spells **(verified)** | `c`, level, number | Light 1 SP; Flame Arrow 1-4 **(verified)** | - | `system_spell_prompt`, `system_light`, `battle_cast_target`, `battle_spell_hit` | shown |
| Abilities and magic | Spells for sale | temples sell cleric spells, mage guilds sorcerer spells; class checked **(verified: refusal)** | - | - | - | `shop_temple_spell_refused`, `shop_sages_members_only`, `dialogue_lloyd_beacon` | shown |
| World and navigation | Areas | 60 areas: five towns, 20 outdoor squares, caverns, dungeons, castles, four elemental planes **(verified: area warp)** | - | - | [content.md](content.md) | `gameplay_atlantium`, `env_mountains_c1`, `gameplay_cavern_lit`, `env_castle_hillstone`, `env_plane_air` | shown |
| World and navigation | Light | caverns and dungeons are "Darkness" without Light **(verified)** | cast Light | - | - | `battle_square_lake_devils`, `system_light` | shown |
| World and navigation | Travel services | Poorman's Portal, ferry, polar bear, dust devil, travel agent **(verified: offers)** | `y` | 10, 5, 50, 100, 5,000 gold **(verified)** | - | `system_poorman_portal`, `system_ferry`, `system_polar_bear`, `system_vulcania_export`, `system_travel_agent` | shown |
| World and navigation | Terrain skills | forest and mountain travel need Pathfinder and Mountaineer **(source; offers verified)** | - | - | - | `system_pathfinder`, `system_mountaineer` | described |
| World and navigation | Stairs and gates | stairs to the cavern, city gates "Exit (y/n)?" **(verified)** | `y` | - | - | `gameplay_stairs_cavern`, `gameplay_gates` | shown |
| World and navigation | Time | Day and Year on the status line; the century decides which version of an area loads **(verified: year 800, Castle Xabran stands in C2; ruins in 900)** | - | four rests per day **(verified)** | [findings.md](findings.md) | `system_year_800`, `gameplay_xabran_800`, `gameplay_ruins_900` | shown |
| Goals and gating | Main quest | Element Orb and four Talons to King Kalohn in year 800, then Luxus Palace Royale, then Sheltem at Square Lake **(verified: Kalohn texts)** | - | - | - | `dialogue_kalohn_asks`, `dialogue_kalohn_wins`, `boss_mega_dragon`, `boss_sheltem` | shown |
| Goals and gating | Restricted places | class, sex and quest checks: "Paladins Only!", "Males only", "Chosen Ones only" **(verified)** | - | - | - | `gameplay_paladins_only`, `gameplay_males_only`, `gameplay_chosen_only` | shown |
| Goals and gating | Final gate | the Square Lake gate let an unmarked party in (the DOS one demands the King's rescue) **(verified)** | - | - | [findings.md](findings.md) | `boss_sheltem_face`, `boss_sheltem` | shown |
| Chance | Rolls | creation statistics, encounters' surprise, hits and the "return to your century" check follow chance **(verified: creation follows timing)** | - | - | - | `create_roll`, `battle_sl_wizards` | shown |
| Failure and recovery | Death and resume | see Defeat; the temple restores conditions **(verified: menu)** | - | - | - | `gameover_death_strikes`, `shop_temple_menu` | shown |
| Saving | Inn registry | signing the registry writes the roster to disk B; each town's inn keeps its own list **(verified)** | `y` | - | - | `save_innkeeper`, `save_signed_in`, `dialogue_atlantium_inn`, `save_atlantium` | shown |
| Pacing | Disk changes | six disks; the game asks for a disk by letter when an area, a picture or the roster lives elsewhere **(verified: B, C, A)** | Return | - | [interface.md](interface.md) | `menu_disk_b`, `boss_sheltem_face`, `start 33_insert_disk_c` | shown |
| Pacing | Rumors and signs | rumors, signs and statues hint at quests **(verified)** | - | - | - | `dialogue_tavern_rumor`, `gameplay_fear_no_evil`, `extra_just_kidding`, `gameplay_unmarked_deadly` | shown |

## 3. Open questions
- Sheltem's fight was not won: with the monsters' hit points set to 0 they still acted and were not removed by
  the party's attacks, and the poked party could not hit them (tried for about 15 calls; playbook "Open").
  The ending (control room, override code, cryptogram) is therefore not shown here; the DOS set shows it.
- After an event message in year 800 the status line shows "Year= 900" again although the century stays 800
  (see [findings.md](findings.md)).
- Unlock, Use, hirelings, the arena and the spell list per level were not tried.
