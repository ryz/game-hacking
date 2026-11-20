# Might and Magic II: Gates to Another World (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/might-and-magic-2`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
Shot ids are those of set `main` (`../shots/main/index.md` gives the file names).

## 1. Core loop
Walk the party square by square through an area, meet fixed and random encounters, fight them in turn-based
menus, search for treasure, and return to a town to spend the gold on training, equipment, spells, skills and
healing; sign in at an inn to save **(verified: walking, fights, victory, training, shops, inn)**. Between loops
the party grows in level and spell level, buys secondary skills that open new terrain, and follows quest texts
to new areas and to another century **(verified: skills offered, year 800 reached; source: manual)**. The quest
ends at the gate of the cavern under Square Lake: Sheltem's fight, an override code and a cryptogram
**(verified: played to the Congratulations screen, see section 3)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move and turn | one square forward or back, 90-degree turns; a turn fires the square's event like a step **(verified)** | arrows | areas 16 x 16 | [world.md](world.md) | `gameplay_inn_start`, `gameplay_outdoors_c2`, `gameplay_middlegate_sign` | shown |
| Player verbs | Bash | the inn door: B walks the party through it into the street **(verified)**; a locked door elsewhere not found | `b` | - | [findings.md](findings.md) | none: bashing the inn door looks like stepping out, no locked door found | described |
| Player verbs | Search | looks for treasure on the square **(verified: "Nothing Here!", also after a fight)** | `s` | - | - | `system_search_nothing`, `cave_x_marks` | shown |
| Player verbs | Rest | restores the party; an encounter can break it **(verified: "Rest complete, no encounters")** | `r`, `y` | one food per member **(source)** | - | `system_rest_prompt`, `system_rest_done` | shown |
| Player verbs | Exchange | swaps two marching positions; positions 1-2 fight hand to hand **(verified)** | `e`, two digits | - | - | `system_exchange`, `system_exchange_done` | shown |
| Player verbs | Protect panel | light units and protection spells in force **(verified)** | `p` | Protection from Elements: Forces 30% at caster level 10 **(verified)** | - | `system_protect`, `system_protect_elements` | shown |
| Player verbs | Location | coordinates of the square; the map needs the Cartographer skill **(verified: coordinates; source: map)** | `m` | - | - | `system_location` | shown (map with a Cartographer not seen) |
| Player verbs | Controls | sounds, walk beep, party disposition, message delay 0-9 **(verified)** | `c`, `1`-`4` | - | - | `options_controls`, `battle_delay` | shown |
| Player verbs | Dismiss | sends a hireling away **(verified: prompt)** | `d` | - | - | `system_dismiss` | shown |
| Player verbs | Character sheet | quick ref, cast, drop, equip, gather, remove, share, trade, use **(verified: every command)** | `1`-`8`, letters | backpack 6, equipped 6 **(verified)** | - | `inventory_profile_vet`, `inventory_equip_prompt`, `inventory_removed`, `inventory_dropped`, `system_trade_what`, `system_trade_done`, `system_share_done`, `system_gather_done`, `system_use_prompt` | shown |
| Characters and progression | Creation | seven statistics rolled, two may be exchanged, eligible classes listed, then race, alignment, sex, name **(verified)** | Enter re-rolls, letters exchange | statistics 3-21 **(source)** | - | `create_roll`, `create_exchange`, `create_race`, `create_alignment`, `create_sex`, `create_name` | shown |
| Characters and progression | Roster | 24 characters kept at the inns, premade six, renaming and deleting **(verified)** | `v`, Ctrl-N, Ctrl-D | - | - | `menu_view_all`, `inventory_premade`, `menu_rename`, `menu_inn_list` | shown |
| Characters and progression | Classes | Knight, Paladin, Archer, Cleric, Sorcerer, Robber, Ninja, Barbarian; front-rank options depend on class and position **(verified)** | - | hit points per level d12 Knight .. d6 Sorcerer **(source)** | - | `create_roll`, `battle_options_knight`, `battle_options_caster` | shown |
| Characters and progression | Experience and training | experience is paid for at a training ground, one level at a time **(verified)** | `y`, `t` | level 2 1,500; Knight level 12 768,000; level 33 30,144,000; level 12 costs 600 gold and gave 10 hit points **(verified)** | [playbook](../playbook.md) RAM map | `system_training`, `system_training_need`, `system_training_cost`, `system_training_levelup` | shown |
| Characters and progression | Spell levels | casters gain a spell level every second level up to 9; Paladins and Archers later **(source; SL 5 at level 10 verified)** | - | - | - | `inventory_profile_mnz`, `system_spellbook_deddo` | shown |
| Characters and progression | Secondary skills | two per character, bought from trainers in towns; Brain Detoxification removes them **(verified: offers, Cartographer learned)** | `y`, member | Cartographer 10, Athlete 500, Linguist 500, Crusader 250, Merchant 1000, Hero 1000, Pathfinder and Mountaineer 2000 gold **(verified)** | - | `system_otto_mapper`, `inventory_skill_learned`, `system_pathfinder`, `system_mountaineer`, `system_athlete`, `system_hero_skill`, `system_crusader`, `system_merchant`, `system_detox` | shown |
| Characters and progression | Thievery | robbers' skill shown on the profile, grows with level; thief trainers raise it **(verified: 45% at level 11, 55% at 31)** | - | Rinaldo Jr. 700 gold **(verified: offer)** | - | `battle_view`, `system_thief_trainer` | shown |
| Characters and progression | Ageing | characters age; the profile shows the age **(verified: 18 at creation)** | - | - | - | `inventory_profile_ryz` | described |
| Characters and progression | Hirelings | freed prisoners become hirelings at an inn; up to 8 in the party **(source: area texts, e.g. Drog and Sir Hyron)** | inn list, `d` | - | - | `menu_hirelings`, `cave_torture_chamber` | described (no hire played) |
| Resources and economy | Gold | shops take gold from the shopper; services sold by an event pool the whole party's gold, take the price and share the rest evenly **(verified, RAM)** | trade, share, gather | Otto Mapper with 5,000 on ryz: 4,990 left, 831 each, 835 for ryz **(verified)** | [findings.md](findings.md) | `system_gather_done`, `system_share_done`, `shop_blacksmith_bought` | shown |
| Resources and economy | Starting money | new and premade characters start with 0 gold and 0 gems, 10 food: nothing in Middlegate's shops, temple or training is affordable at first **(verified, RAM +0x66 of all six records)** | - | - | - | start `26_blacksmith_menu`, `30_temple_menu` | shown |
| Resources and economy | Food | bought at taverns, 40 at most per member **(verified: feeding frenzy fills each to 40)** | tavern `a` | - | - | `hud_food_frenzy` | shown |
| Resources and economy | Gems | pay for higher spells and bribes **(source; bribe option verified)** | - | - | - | `battle_bribe_prompt` | shown |
| Resources and economy | Blacksmiths | weapons, specials (+1 items), armor, misc, sell, identify **(verified)** | letters | Dagger 8, Cudgel 15, Nunchakas 30; Ring Mail 200; a 15-gold Cudgel sells for 3 **(verified)** | - | `shop_blacksmith_menu`, `shop_blacksmith_weapons`, `shop_blacksmith_specials`, `shop_blacksmith_armor`, `shop_blacksmith_misc`, `shop_blacksmith_bought`, `shop_blacksmith_sell`, `shop_blacksmith_identify` | shown |
| Resources and economy | Taverns | food, drinks, specialties, tips, rumors after a tip **(verified)** | letters | drinks 5-100, specialties 10-100, tip 1 gold **(verified)** | - | `shop_tavern_menu`, `shop_tavern_drinks`, `shop_tavern_specialties`, `shop_tavern_tip`, `dialogue_tavern_rumor` | shown |
| Resources and economy | Temples | restore condition and alignment, donations, three cleric spells for sale **(verified: menu)** | letters | donation 100 **(verified)** | - | `shop_temple_menu`, `shop_temple_donation`, `shop_temple_spell_refused` | shown |
| Resources and economy | Mage guilds | membership 20 gold; members buy sorcerer spells from the sages **(verified: offer, refusal to non-members)** | `y` | - | - | `system_mage_guild`, `dialogue_sages`, `shop_sages_members_only`, `system_illusionist` | shown |
| Resources and economy | Locksmiths | sell keys **(verified: offer 500 gold)** | `y` | - | - | `system_locksmith` | shown |
| Conflict | Encounter options | attack, bribe (food, gold, gems), hide, run **(verified)**; hide failed into combat once, run left the fight | letters | - | - | `battle_encounter`, `battle_bribe_prompt`, `battle_run_away` | shown |
| Conflict | Surprise | either side can be surprised: the party then loses or gains the first round **(verified both)** | - | - | - | `boss_sheltem_surprise`, `battle_sl_guardians` | shown |
| Conflict | Combat round | members act by speed; options depend on class and rank: attack, fight (pick a target in reach), shoot, cast, use, block, run, exchange, view **(verified)** | letters | front two members and the first five monsters are in reach (ticks) **(verified)** | - | `battle_options_knight`, `battle_options_caster`, `battle_options_fighter`, `battle_fight_prompt`, `battle_fight_hit`, `battle_cast_prompt`, `battle_spell_hit`, `battle_view`, `battle_exchange_prompt`, `battle_exchange_done`, `battle_run`, `battle_protect` | shown |
| Conflict | Quick fight | Ctrl-A lets the member do the default action **(verified)** | Ctrl-A | - | - | `battle_quick_shoot` | shown |
| Conflict | Monster behaviour | strike, breathe (damage = a part of the monster's hit points), wait for an opening when out of reach, run away **(verified)** | - | Sheltem 500 hit points, Elementals 250 **(RAM)** | - | `battle_waits_opening`, `battle_exchange_done`, `battle_party_falls`, `boss_sheltem_slashes` | shown |
| Conflict | Victory | survivors share the experience; the game counts battles won **(verified: 416 each, 488th battle)** | - | Sheltem's group: 208,000 each **(verified)** | - | `battle_victory`, `boss_sheltem_victory` | shown |
| Conflict | Defeat | when every member is down: "Death Strikes! ... resume adventuring at the inn in which you last stayed", Enter: the inn list with the roster as last written to disk, everyone alive, party empty; unsaved changes (an equipped sword) are undone **(verified, set start)** | Enter | ten Orcs beat the level-1 party in 20 quick-fight steps **(verified)** | [findings.md](findings.md) | start `48_death_strikes`, `49_inn_after_death` | shown |
| Opponents | Monster groups | fixed groups on event squares and random ones; up to dozens ("+56 more Devil Kings") **(verified)** | - | - | [content.md](content.md) 3 | `battle_skeletons`, `battle_square_lake_devils`, `battle_vulcania_cavern` | shown |
| Opponents | Bosses | named enemies guard quest steps: Jouster, Queen Beetle, Lich Lord, Mega Dragon, Sheltem **(verified)** | - | - | [content.md](content.md) 3 | `boss_jouster`, `boss_queen_beetle`, `boss_lich_lord`, `boss_mega_dragon`, `boss_sheltem_fight` | shown |
| Items and equipment | Equipment | class restrictions (a Sorcerer cannot use a Sling); armour class from what is worn **(verified)** | equip, remove | Large Shield 2 AC **(verified: 11 to 9)** | - | `inventory_removed`, `inventory_profile_vet` | shown |
| Items and equipment | Quest items | Discs, Talons, Element Orb, tickets, keys, J-26 Fluxer and three more **(RAM: item table)** | - | 256 item records **(RAM)** | [content.md](content.md) 4 | `dialogue_xabran_disc`, `dialogue_element_orb`, `gameplay_lava_grenade` | shown |
| Abilities and magic | Spells | 48 cleric + 48 sorcerer spells in 9 levels; cast by level and number, some cost gems **(source; casting verified)** | `c`, level, number, Enter | Flame Arrow 8 points to a cat **(verified)** | - | `system_cast_spellbook`, `battle_cast_prompt`, `battle_spell_hit`, `system_protect_elements` | shown |
| World and navigation | Areas | 60 areas: 5 towns, 20 outdoors in a wrapping 5 x 4 grid, 16 caverns, 5 castles, 8 dungeon levels, 2 towers, 4 elemental planes **(verified)** | - | - | [world.md](world.md) | `env_tundra_a1`, `env_sea_a3`, `gameplay_cavern_lit`, `env_castle_hillstone`, `env_plane_fire` | shown |
| World and navigation | Terrain and hazards | outdoor hazards strike by square: whirlpool, oasis, dragon dung, sewage, cave-ins **(verified)** | - | - | - | `env_sea_a3`, `gameplay_dragon_dung`, `gameplay_sandsobar_sewage` | shown |
| World and navigation | Darkness | caverns and dungeons are dark without light units **(verified)** | Light spell | - | - | `gameplay_cavern_lit` | shown |
| World and navigation | Travel services | portals, ferries, river walking, transport companies, travel agent, polar bear **(verified: offers)** | `y` | portal 10, ferry 5, river walker 50, polar bear 50, export 100, Murray's trip 5,000 gold **(verified)** | - | `system_poorman_portal`, `system_ferry`, `system_river_walker`, `system_polar_bear`, `system_vulcania_export`, `system_travel_agent`, `system_travel_booked` | shown |
| World and navigation | Time | Day and Year on the status line; areas change with the century **(verified: Castle Xabran and King Kalohn in year 800)** | (how the party travels in time in play: not seen) | start year 900 | [world.md](world.md) | `gameplay_xabran_800`, `dialogue_kalohn_asks` | shown (the travel itself open) |
| Goals and gating | Gates by class, sex, sign | "Paladins Only!", "Males only", "Archers Only", "Chosen Ones only" **(verified)** | - | - | - | `gameplay_paladins_only`, `gameplay_chosen_only`, `battle_ice_cavern` | shown |
| Goals and gating | Main quest | Discs open the elemental shrines, the Talons and the Element Orb go to King Kalohn in year 800, the Square Lake gate opens for the marked party **(verified: Kalohn's event and the gate; RAM: marks)** | `y` | quest marks in the character record **(RAM)** | section 3 | `dialogue_kalohn_asks`, `dialogue_kalohn_wins`, `gameplay_square_lake_gate`, `dialogue_devil_kings_bow` | shown |
| Goals and gating | Ending | Sheltem and four Elementals, the override code WAFE, then the cryptogram answered in its own cipher before the clock runs out **(verified)** | typing | 15-minute clock; bonus 50,000,000 experience **(verified)** | section 3 | `boss_sheltem_appears`, `ending_collision`, `ending_override_typed`, `ending_recalculating`, `ending_cryptogram`, `ending_answer_typed`, `ending_congratulations` | shown |
| Chance | Rolls | creation rolls, hits ("3 times and hit 2"), encounters follow chance **(verified)** | re-roll | - | - | `create_roll`, `battle_fight_hit` | shown |
| Failure and recovery | Death | 0 hit points = down, below = dead; a lost party sees Death Strikes and resumes at the last inn **(verified)** | Enter | - | - | `battle_party_falls`, `gameover_death_strikes`, `gameover_inn_empty` | shown |
| Saving and sessions | Inn | sign in at any town's inn to save the roster; play resumes there **(verified: Middlegate, Atlantium)** | `y` | - | - | `save_innkeeper`, `save_signed_in`, `save_atlantium` | shown |
| Pacing and difficulty | Fixed fights | fixed groups guard places, from cats in Middlegate to Square Lake's twelve groups **(verified)** | - | - | - | `battle_encounter`, `battle_sl_phantasms`, `battle_sl_alien_probes` | shown |

## 3. The end of the game (verified 2026-11-19)
1. King Kalohn (year 800, area C4 (14,5)) asks for the Element Orb and the four Talons; giving them marks every
   party member "Kalohn saved" and he defeats the Mega Dragon (`dialogue_kalohn_asks`, `dialogue_kalohn_wins`).
   Without them he dies and the Mega Dragon attacks (`boss_mega_dragon`).
2. The gate of the cavern under Square Lake (area 17 (0,15), facing east) refuses parties without a second
   mark ("You shouldn't be here until you save the King in the 9th century") (`gameplay_square_lake_gate`).
   What sets that mark in play was not found in any area script **(RAM: only Kalohn writes a mark; the gate
   tests another bit)**; the capture sets it by memory. The cave in C2 for "Chosen Ones only" and the 66 Devil
   Kings bowing to the Chosen One test a third mark.
3. With the marks, Sheltem's face appears and he attacks with the Water, Air, Fire and Earth Elementals
   (`boss_sheltem_appears`, `boss_sheltem_surprise`, `boss_sheltem_fight`, `boss_sheltem_victory`).
4. After the fight a vacuum tube takes the party to the control room: "CRON is off course and headed directly
   towards the sun! ... Enter override code to abort". The code is **WAFE** (from the game's code; a wrong code
   puts the party back at the cavern's entrance) (`ending_control_room`, `ending_collision`,
   `ending_override_typed`, `ending_recalculating`).
5. "Error, Error! Computer malfunction" and Sheltem's recorded message follow, then the cryptogram: the
   preamble "We, the people of Terra ..." enciphered with a substitution key drawn at random, a 15-minute clock
   at the top, and "Answer= Preamble Code=". The player must type the word Preamble in the same cipher (8
   letters, case kept) (`ending_cryptogram`, `ending_answer_typed`). Time out fails.
6. Success: every member gets 50,000,000 experience and a "Cron saved" mark; the screen congratulates the party
   ("This ship, created by the Ancients ... Prepare to beam down in Might+Magic III"), gives battles won and lost
   and a final score, then returns to the inn (`ending_congratulations`) **(verified)**.

## 4. How the systems feed each other
Fights give experience and treasure; gold pays for training, equipment, spells, skills and travel; skills open
terrain and services; quests give large experience rewards (the Bishop of Black Battle: 10,000 and 200,000 for
Triple Crown winners: area text) and open later areas; time travel opens the past, where the final gate is
decided **(verified in part: see rows)**.

## Open questions
- How the party travels between centuries in play (an item such as the Hourglass, a place or a spell).
- What sets the gate's mark and the Chosen One mark in play.
- The full experience table and hit point gains per class.
- Hirelings: hiring was not played.
