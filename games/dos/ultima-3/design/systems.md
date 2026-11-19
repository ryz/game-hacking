# Ultima III: Exodus (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima-3`. Numbers: [rules.md](rules.md).

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
Walk the party over Sosaria, enter townes and castles to talk, trade and heal, and fight the monsters that walk
up to the party; experience turns into hit points at Lord British's throne **(verified: `gameplay_start`,
`gameplay_towne_lcb`, `battle_start`, `dialogue_lb_greater`)**. Between loops the party goes deeper: dungeons
for marks and gold, a frigate for the sea, the whirlpool to Ambrosia for statistics and cards, the moongates for
the Time dungeon, until the four cards end the game in the Castle of Fire **(verified: `system_rod_mark`,
`cutscene_whirlpool`, `system_card_sol`, `cutscene_timelord`, `ending_text`)**.

## 2. Systems
| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Movement and refusals | arrows move the party a square; water, mountains and walls answer "Invalid Move!"; a command with nothing to act on answers "<-What?" or "Not Here!" **(verified)** | arrows, letters | - | interface.md | `gameplay_invalid_move`, `gameplay_refusals`, `gameplay_refusals_2` | shown |
| Player verbs | Look | names the terrain or thing in a direction **(verified)** | L + direction | - | - | `system_look` | shown |
| Player verbs | Real-time pass | five seconds without a key pass a turn ("Pass"); idle turns count as moves **(code, verified)** | none | 5 s | findings.md | `gameplay_start`, `save_quit` | shown |
| Player verbs | Other command | a typed word: INSERT, DIG, SEARCH, BRIBE, PRAY; anything else "No effect!" **(verified)** | O, player, word | - | rules.md 4, 8 | `system_no_effect`, `system_other_no_effect`, `system_dig_weapon`, `system_card_sol`, `system_bribe`, `system_pray`, `system_insert_prompt` | shown |
| Player verbs | Yell | a word to the world; only EVOCARE at the Silver Snake does anything **(verified)** | Y, player, word | - | - | `system_no_effect`, `system_evocare_no_mark`, `system_evocare` | shown |
| Player verbs | Volume, Modify order | V toggles sound; M swaps two members' places **(verified)** | V; M, two numbers | - | - | `system_ignite_volume`, `system_modify` | shown |
| Characters and progression | Creation | name, sex, race (5), type (11), 50 points over four statistics; a value past the points is refused **(verified)** | letters + Enter, digits | 50 points; new: 150 H.P., food, gold; dagger, cloth | ../playbook.md Boot | `menu_create_name`, `menu_create_race`, `menu_create_type`, `menu_create_str`, `menu_create_ok`, `menu_create_fuzzy`, `menu_create_overspent` | shown |
| Characters and progression | Roster and party | 20 register entries, a party of 1-4 formed, dispersed, terminated **(verified)** | Organize menu | 20, 4 | interface.md | `menu_register`, `menu_form`, `menu_form_inuse`, `menu_disperse`, `menu_terminate`, `menu_create_notempty` | shown |
| Characters and progression | Race limits | the highest each statistic can reach: Human 75/75/75/75, Elf 75/99/75/50, Dwarf 99/75/50/75, Bobbit 75/50/75/99, Fuzzy 25/99/99/75 **(ROM text)** | - | table | - | none: a table in the program, never shown | described |
| Characters and progression | Levels and hit points | level = experience / 100 + 1; Lord British adds 100 maximum H.P. per visit while experience allows, the Mark of Kings past 500, never past 2500 **(code, verified)** | T at the king | +100, 500, 2500 | rules.md 8 | `dialogue_lb_experience`, `dialogue_lb_greater`, `dialogue_lb_mark`, `dialogue_lb_nomore` | shown |
| Characters and progression | Classes | the class decides the spell list and the best weapon and armour allowed ("Not allowed!") **(code, verified)** | R, W | table | rules.md 3 | `system_ready`, `system_ready_refused`, `system_wear`, `system_wear_refused`, `system_cast_not_mage` | shown |
| Characters and progression | Shrines of Ambrosia | an offering of N hundred gold raises one statistic by N up to the race limit **(code, verified)** | E on a shrine, player, number | 100 gold a point | ../playbook.md | `system_shrine`, `system_shrine_shazam`, `system_shrine_cheat`, `system_shrine_off` | shown |
| Resources and economy | Per-character goods | gold, food, gems, keys, powders, torches belong to each member; Hand moves them, Join pools gold up to 9999 **(verified)** | H, J | 9999 cap | - | `inventory_ztats_2`, `system_hand_gold`, `system_hand_food`, `system_join_refused` | shown |
| Resources and economy | Food | each member eats as the party moves; gremlins steal 100 **(verified)** | buy at the grocer | 1 gold a ration | rules.md 4, 6 | `shop_grocer_buy`, `system_dungeon_gremlins` | shown (starvation: open) |
| Resources and economy | Shops | eight kinds chosen by the counter's row: pub, grocer, healer, weapons, armour, Guild, oracle, stables **(code, verified all)** | T over a counter | prices in rules.md 4 | rules.md 4 | `shop_pub`, `shop_grocer`, `shop_healer`, `shop_weapons`, `shop_armour`, `shop_guild`, `shop_oracle`, `shop_horses` | shown |
| Resources and economy | Buying and selling arms | Buy or Sell by letter; refused without the gold or the item **(verified)** | B/S, letter | - | rules.md 4 | `shop_weapons_buy`, `shop_weapons_poor`, `shop_weapons_sell`, `shop_armour_buy`, `shop_armour_sell`, `shop_weapons_dawn`, `shop_armour_dawn` | shown |
| Resources and economy | Tips and the oracle | the pub's tip follows the tens digit paid; the oracle recites the verse of the hundreds offered **(code, verified)** | numbers | 7 gold a drink | rules.md 4 | `shop_pub_scum`, `shop_pub_kindly`, `shop_pub_tip_ambrosia`, `shop_pub_tip_moons`, `shop_pub_tip_time`, `shop_pub_bye`, `shop_oracle_1`, `shop_oracle_2`, `shop_oracle_6` | shown |
| Resources and economy | Healing for gold | curing 100, healing 200, resurrection 500, recalling 900 **(verified)** | T at the healer | - | rules.md 4 | `shop_healer_cure`, `shop_healer_heal`, `shop_healer_resurrect`, `shop_healer_bye` | shown |
| Resources and economy | Stealing and bribing | steal a chest across Grey's counter on a Dexterity roll, else "Failed!" or "Watch out!"; 100 gold sends a guard away **(code, verified)** | S; O + BRIBE | 100 gold | rules.md 4 | `system_steal`, `system_steal_failed`, `system_steal_caught`, `system_bribe` | shown |
| Conflict | Combat screen | a separate 11x11 field chosen by place and terrain; each member acts in turn, then the monsters **(verified)** | arrows, A, C, space | 9 fields | rules.md 1 | `battle_start`, `battle_cutpurses`, `battle_zombies`, `battle_serpents`, `battle_pirates_board`, `battle_dungeon_goblins` | shown |
| Conflict | Attacks | melee into a neighbouring square, ranged weapons along a line; Hit!, Missed!, Killed! Exp.+N, Victory! **(verified)** | A + direction | exp. 3-10 per kill seen | rules.md 1.2 | `battle_victory`, `battle_bow`, `battle_kill` | shown (party's formula open) |
| Conflict | Monster attacks | hits always except against Exotic armour or in Castle Exodus; damage grows with the target's maximum H.P.; poison and pilfering **(code, verified)** | - | rules.md 1.3 | rules.md 1.3 | `battle_orc_hits`, `battle_snatches_poison`, `battle_thieves_pilfer`, `battle_pirates_fire` | shown |
| Conflict | Monsters on the map | monsters walk toward the party on land and sea; touching or attacking starts a fight; a chest is left after it **(verified)** | move, A | - | content.md | `gameplay_monster_map`, `gameplay_serpent_sea`, `system_chest_after_fight` | shown |
| Conflict | Attacking people | attacking a guard or Lord British starts a fight with them **(verified)** | A in a towne | - | - | `battle_guards`, `battle_lord_british` | shown |
| Conflict | Death and game over | at 0 H.P. "Killed!!!", status D; all out: "All Players Out!" and the game stops **(verified)** | - | - | rules.md 1.3 | `battle_member_killed`, `gameover_all_out` | shown |
| Opponents | Kinds and names | 13 kinds roam Sosaria (land and sea), more in dungeons and castles; one picture can carry two names **(verified)** | - | 16 alternate names | content.md 3 | `battle_giants`, `battle_daemons`, `battle_devils`, `battle_wizards`, `battle_wyverns_ship`, `battle_manowars`, `battle_pirates_shore` | shown |
| Items and equipment | Chests | half are trapped (acid, poison, gas, bomb, evaded by Dexterity); 30-99 gold, one in four an arm or armour **(code, verified)** | G, player | rules.md 5 | rules.md 5 | `system_chest_gold`, `system_chest_weapon`, `system_chest_armour`, `system_trap_acid`, `system_trap_poison`, `system_trap_gas`, `system_trap_bomb`, `system_trap_evaded` | shown |
| Items and equipment | Exotics | DIG on the islet (21,03) gives an Exotic weapon, on (13,2C) Exotic armour **(code, verified)** | O + DIG | one per dig | findings.md | `system_dig_weapon`, `system_dig_armour` | shown |
| Items and equipment | Cards and marks | four cards from Ambrosia's shrines (SEARCH); four marks from red-hot rods in the dungeons **(verified)** | O + SEARCH; touch | rod 50 H.P. | rules.md 6 | `system_card_sol`, `system_card_death`, `system_rod`, `system_rod_mark`, `inventory_ztats_marks` | shown |
| Items and equipment | Tools | gems (Peer), keys (Unlock), powders (Negate time), torches (Ignite) **(verified)** | P, U, N, I | Guild prices | rules.md 4 | `system_peer_gem`, `system_unlock`, `system_negate`, `gameplay_dungeon_torch`, `system_none_left` | shown |
| Abilities and magic | Spells | 16 cleric and 16 wizard spells by letter, 5 M.P. per letter; casters by class **(code, verified for 12)** | C, player, letter | 0-75 M.P. | rules.md 2 | `battle_spell_mittar`, `battle_spell_hit`, `battle_spell_repond`, `battle_pontori_failed`, `battle_spell_zxkuqyb`, `system_spell_sanctu`, `system_spell_alcort`, `system_spell_surmandum`, `system_spell_vieda`, `system_spell_dag_acron`, `system_spell_fal_divi`, `system_spell_lorum`, `system_spell_dor_acron`, `system_spell_sur_acron`, `system_cast_mp_low` | shown |
| World and navigation | Sosaria and its places | 64x64, wraps; 10 townes, 2 castles, 7 dungeons **(code)** | arrows, E | coordinates in the playbook | content.md 2 | `gameplay_start`, `gameplay_moon`, `gameplay_castle`, `gameplay_dark_forest` | shown |
| World and navigation | Horses | bought at the stables, ridden, left standing with X-it, boarded again **(verified)** | B, X | 800 gold for 4 | - | `shop_horses_buy`, `gameplay_horse`, `system_horse_xit`, `system_horse_board` | shown |
| World and navigation | Frigates and wind | taken from pirates; sail with the wind, never into it or in a calm; cannons **(code, verified)** | B, X, F | wind every 25 turns | rules.md 7 | `system_board_frigate`, `gameplay_frigate`, `system_wind`, `battle_cannons`, `system_frigate_taken` | shown |
| World and navigation | Moongates | the first moon picks the gate's square, the second where it leads **(code, verified)** | walk in | 8 phases | ../playbook.md | `system_moongate`, `system_moongate_through` | shown |
| World and navigation | Whirlpools and Ambrosia | Sosaria's whirlpool sinks the frigate and strands the party in Ambrosia; Ambrosia's brings it back in a frigate **(verified)** | sail | - | rules.md 7 | `cutscene_whirlpool`, `cutscene_ambrosia_shore`, `cutscene_ambrosia_return`, `gameplay_ambrosia_sign` | shown |
| World and navigation | Dungeons | first person, 8 levels of 16x16, dark without light; ladders, doors, chests, fountains, winds, traps, gremlins, writing, random fights **(verified)** | arrows, K, D, I | - | rules.md 6 | `gameplay_dungeon_dark`, `gameplay_dungeon_ladder`, `system_dungeon_descend`, `system_dungeon_klimb_out`, `system_fountain`, `system_fountain_heal`, `system_fountain_poison`, `system_fountain_hurt`, `system_dungeon_wind`, `system_dungeon_trap`, `system_dungeon_writing`, `system_dungeon_not_cmd`, `system_dungeon_get_chest`, `system_dungeon_chest` | shown |
| World and navigation | Maps | a gem or Vieda shows the whole land in miniature **(verified)** | P, C | 75 gold a gem | - | `system_peer_gem`, `system_spell_vieda` | shown |
| Goals and gating | The quest chain | marks for every member (force fields, lava, the snake, the king), EVOCARE, the four cards, their order from the Time Lord, Castle Exodus **(verified)** | - | - | rules.md 8 | `system_evocare`, `system_exodus_field`, `system_exodus_lava`, `cutscene_timelord`, `system_insert_love`, `system_insert_sol`, `system_insert_moons`, `ending_flash` | shown |
| Goals and gating | Wrong card | a card in the wrong slot kills the inserter **(code, verified)** | O + INSERT | - | rules.md 8 | `system_insert_wrong` | shown |
| Goals and gating | Dawn | the city of Dawn stands in the Dark Forest only while both moons are new **(code, verified)** | wait | - | ../playbook.md | `system_dawn_appears`, `gameplay_dawn` | shown |
| Goals and gating | Hints | townsfolk lines, pub tips and the oracle's rhyme carry every clue **(ROM text, verified)** | T | ~70 lines | content.md 7 | `dialogue_lcb_9`, `dialogue_devil_1`, `dialogue_fawn_1`, `dialogue_british_19` | shown |
| Chance | Random rolls | one generator for encounters, traps, steals, spell successes, damage **(code)** | - | rules.md | ../playbook.md Capture notes | none: hidden rolls (forced by poke for `system_trap_*`, `system_steal_*`) | described |
| Failure and recovery | Healing and raising | fountains, healers, cleric spells (Sanctu, Alcort, Surmandum) **(verified)** | - | - | rules.md 2, 4, 6 | `system_fountain_cure`, `shop_healer_resurrect`, `system_spell_surmandum` | shown |
| Saving and sessions | Quit & Save | only on Sosaria; play goes on; entering a place also saves **(verified)** | Q | moves counted | - | `save_quit` | shown |
| Pacing and difficulty | Knowledge gates | almost nothing is locked by level; the gates are marks, cards, a word, a moon phase and a whirlpool **(inferred from the code)** | - | - | - | none: a property of the design, no screen | described |

## 3. How the systems feed each other
- Fights give experience and gold; Lord British turns experience into hit points; gold buys arms, horses,
  healing and (in Ambrosia) statistics **(verified)**.
- Monster damage grows with the target's maximum hit points, so Exotic armour (dug, not bought) is what lets a
  late party shrug off hits **(code)**.
- Dungeons give gold, chests and the marks; the marks open the Castle of Fire and Lord British's levels past
  five **(verified)**.
- The sea (frigate, whirlpool) opens Ambrosia: statistics and the cards; the moons open Dawn (magic arms) and
  the Time dungeon (the card order) **(verified)**.

## Open questions
- The party's hit and damage formulas; which alternate monster name a fight uses.
- Starvation and poison damage per turn (food 0 showed nothing within 300 frames, scout).
