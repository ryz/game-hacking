# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of places, monsters and things; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/might-and-magic`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
Confidence tags are in the detail documents; a row without its own tag is **(verified)** by the shots it names.

## 1. Core loop
A party of up to six leaves the inn of a town, walks square by square through first-person maps of 16 by 16
squares and meets fixed and random groups of monsters. Fights are played in rounds from text menus and pay
experience; treasure is found by searching afterwards. Back in a town the party heals at the temple, buys food
and gear, pays for training once the experience is enough, and signs in at the inn, which is the only way to
save. Between loops the party grows in level, spells and equipment, and the player's own map and notes grow:
the game keeps no map and no quest log **(verified for the loop; the missing automap is from the manual)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move and turn | one step or a quarter turn per key; events fire by square and facing | arrow keys | maps 16 x 16 | [world.md](world.md) | `start_inn_door`, `sorpigal_inn_sign` | shown |
| Player verbs | Order | re-arrange the six by typing old positions in the new order | `O`, six digits | positions 1-2 fight first | [characters.md](characters.md) 3, 6 | `order_prompt`, `order_done` | shown |
| Player verbs | Protect | list the party spells in force | `P` | Protection from Fear +21% | [characters.md](characters.md) 6 | `protect_active`, `protect_three` | shown |
| Player verbs | Rest | restores the party, can be broken by an encounter | `R`, `Y` | 7 rests, no encounter | [characters.md](characters.md) 3 | `rest_prompt`, `rest_complete` | shown (interruption not seen) |
| Player verbs | Search | looks for treasure on the square, used after fights and at statues | `S` | - | [combat.md](combat.md) 3 | `search_nothing`, `env_forest_c1` | shown (a find after a fight not seen) |
| Player verbs | Bash | forces a locked door; sets off its trap | `B` | gas trap 1-2 points each | [combat.md](combat.md) 9 | `bash_trap`, `bash_after` | shown |
| Player verbs | Unlock | one character picks a lock; a failure sets off the trap | `U`, `1`-`6` | blades 2-4 points each | [combat.md](combat.md) 9 | `door_locked`, `unlock_who`, `unlock_success`, `unlock_trap`, `trap_damage` | shown |
| Player verbs | Quick reference | hit points, spell points, armor class, food, condition of all six | `Q` | - | [interface.md](interface.md) | `quickref` | shown |
| Player verbs | Share / Gather | split gems, gold or food evenly / collect them on one character | profile `S` / `G`, `1`-`3` | 1833 gold: 305 each, viewer 308 | [characters.md](characters.md) 6 | `share_prompt`, `share_done`, `gather_prompt`, `gather_done` | shown |
| Player verbs | Trade | hand an amount or an item to another character | profile `T`, member, kind, amount or letter | - | [characters.md](characters.md) 6 | `trade_with`, `trade_which`, `trade_how_much`, `trade_gold_done`, `trade_item_done`, `trade_food_done` | shown |
| Player verbs | Discard | destroys a backpack item, no confirmation | profile `D`, letter | - | [characters.md](characters.md) 6 | `discard_prompt`, `discard_done` | shown |
| Player verbs | Equip / Remove | move an item between backpack and the six equipped slots; class limits | profile `E` / `R` | armor class 3 to 1 without Leather Armor | [characters.md](characters.md) 6 | `equip_prompt`, `equip_wrong_class`, `remove_prompt`, `remove_done` | shown |
| Player verbs | Use | trigger an item's power, from either list | profile or combat `U` | Might Potion +5 Might; Magic Herbs +8 hit points; 3 charges | [characters.md](characters.md) 6 | `use_prompt`, `use_no_power`, `use_might_potion`, `use_herbs_target`, `use_herbs_done` | shown |
| Player verbs | Cast | spell by level and number, Enter, then a target if needed | profile or combat `C` | First Aid: 1 point, +8 hit points | [characters.md](characters.md) 5, 6 | `cast_prompt`, `cast_on_whom`, `cast_done`, `cast_healed`, `location_spell`, `detect_magic` | shown |
| Player verbs | Answer events | most squares ask Y/N; some offer numbered choices | `Y`/`N`, digits | - | [world.md](world.md) | `stairs_prompt`, `statue_prompt`, `alamar_prisoner`, `cave_portal`, `outdoors_statues`, `whitewolf_button` | shown |
| Characters and progression | Creation | seven statistics rolled 3-18 together; the roll decides the classes offered | `Enter` re-roll, digits | 6 classes, 5 races, 3 alignments | [characters.md](characters.md) 1 | `create_roll`, `create_race`, `create_alignment`, `create_name`, `create_save` | shown |
| Characters and progression | Roster and party | up to 18 characters kept, up to six travel | inn list, `Ctrl`+letter | 18 / 6 | [characters.md](characters.md) | `roster_view_all`, `profile_menu`, `rename_prompt`, `save_inn_list` | shown |
| Characters and progression | Profile | statistics, level, age, hit points, spell points, gems, gold, food, condition, 6 + 6 items | `1`-`6` | - | [characters.md](characters.md) 2 | `profile_ryz` | shown |
| Characters and progression | Levels by training | experience only qualifies; a town trainer raises the level for gold | trainer `A` | level 2 at 1500 experience, 25 gold; +11 hit points; level 3 at 3000, level 8 at 96000 (doubling) | [characters.md](characters.md) 4 | `train_level2`, `train_levelup`, `train_level3_need`, `train_level8_need`, `profile_level2`, `train_no_gold` | shown |
| Characters and progression | Ageing | training made the character a year older | - | 18 to 19 | [findings.md](findings.md) | `profile_level2` | shown |
| Characters and progression | Temporary statistic changes | a potion raises a statistic for a while | Use | Might 15 to 20 | [characters.md](characters.md) 6 | `use_might_potion` | shown (how long: open) |
| Resources and economy | Gold | carried per character; pays shops, temple, training, tavern | shop `G` gathers | start 0 (Knight of the stock party 200) | [sorpigal.md](sorpigal.md) | `shop_blacksmith_menu`, `gather_done` | shown |
| Resources and economy | Food | each character carries units; resting uses them; a market refills | market `Y` | 5 gold; 10 to 40 | [sorpigal.md](sorpigal.md) 6 | `market_food`, `market_bought`, `market_food_after`, `trade_food_done` | shown |
| Resources and economy | Gems | pay the leprechaun and stronger spells | - | 1 gem per trip; 200 in one chest | [sorpigal.md](sorpigal.md) | `leprechaun`, `leprechaun_algary`, `chest_opened` | shown |
| Resources and economy | Buying and selling | three lists of six per blacksmith; sell at half price | `A`-`F` | Dagger 5 ... Antidote Brew 500 | [sorpigal.md](sorpigal.md) 2, 6 | `shop_weapons`, `shop_armor`, `shop_misc`, `shop_sell`, `shop_cant_use`, `portsmith_weapons`, `portsmith_armor`, `portsmith_misc` | shown |
| Resources and economy | Temple services | restore health, uncurse, restore alignment, donation; priced by need | `A`-`D` | 25 wounded or poisoned (same screen), 200 dead, donation 100 | [sorpigal.md](sorpigal.md) 6 | `temple_services`, `temple_price`, `temple_cured`, `temple_cured_profile`, `temple_poisoned`, `temple_dead`, `temple_donation` | shown |
| Resources and economy | Tavern | drink, tip, rumors after tips | `A`-`C` | 1 gold each; rumor after 2 tips | [sorpigal.md](sorpigal.md) 6 | `tavern_menu`, `tavern_drink`, `tavern_rumor` | shown |
| Conflict | Encounter options | attack, bribe, retreat or surrender before combat, unless the group attacks at once | `A` `B` `R` `S` | bribe: all food | [combat.md](combat.md) 1, 6 | `encounter_poltergeists`, `encounter_bribe`, `encounter_bribe_demand`, `encounter_bribe_paid`, `encounter_bribe_food`, `encounter_surrender` | shown (Retreat prints nothing: [combat.md](combat.md) 6)  |
| Conflict | Rounds and turn order | everyone acts once a round; faster first | - | Speed 17, 15, 14 before the monsters | [combat.md](combat.md) 7 | `combat_round`, `combat_options` | shown |
| Conflict | Formation and reach | two characters fight hand to hand at first; `+` marks who can; Exchange swaps places | `E`, `1`-`6` | - | [combat.md](combat.md) 2, 7 | `combat_exchange_prompt`, `combat_exchange_done` | shown |
| Conflict | Attack, Fight, Shoot, Block | first monster, chosen monster, missile, defend | `A` `F` `S` `B`, `Ctrl-A` quick | Sling 7 points | [combat.md](combat.md) 2, 7 | `combat_fight_prompt`, `combat_shoot`, `combat_options` | shown |
| Conflict | Spells and items in combat | cast by level and number; use from the item lists | `C`, `U` | Flame Arrow 5 points | [combat.md](combat.md) 7 | `combat_cast`, `combat_spell_hit`, `combat_bless`, `combat_sleep_immune`, `combat_turn_undead`, `combat_use` | shown |
| Conflict | Handicap | a line names which side is favoured and by how much each round | - | "MONSTER +5" to "PARTY +5" seen | [combat.md](combat.md) 2 | `combat_round`, `boss_demon_drain` | shown (effect: open) |
| Conflict | Conditions | ten named states; some skip turns, some need a temple | - | see list | [characters.md](characters.md) 7 | `conditions_quickref`, `combat_conditions`, `combat_paralyzed`, `combat_stoned` | shown |
| Conflict | Going down and dying | 0 hit points is unconscious; another hit kills | - | - | [combat.md](combat.md) 4, 8 | `death_party_down`, `unconscious_quickref`, `combat_dragon_breath`, `combat_dies` | shown |
| Conflict | Victory and experience | every survivor gets the full amount | - | 25 per Poltergeist | [combat.md](combat.md) 3 | `combat_victory` | shown |
| Opponents | Groups | up to 14 in one list, mixed kinds, a picture of the first | - | 195 kinds | [content.md](content.md) 3 | `qvl_hydras`, `battle_centaurs`, `battle_giants`, `battle_lepers` | shown |
| Opponents | Random and fixed groups | a fight square rolls its group on entry; event squares hold fixed ones | - | 8 different groups in one room | [combat.md](combat.md) 1, [world.md](world.md) 8 | `encounter_goblins`, `encounter_guardsmen`, `outdoors_vines`, `cave_snakes`, `cave_fire_ants`, `cave_skeletons` | shown |
| Opponents | Special attacks | breath, gaze, spells, drains, instant death | - | breath 83/41 points | [combat.md](combat.md) 8 | `combat_dragon_breath`, `combat_stoned`, `boss_lich_eradicates`, `boss_demon_drains`, `combat_magicians`, `combat_lava_beast` | shown |
| Opponents | Undead | a class of monsters that Turn Undead destroys and Sleep does not touch | - | 2 of 4 Skeletons | [combat.md](combat.md) 7 | `combat_turn_undead`, `combat_sleep_immune`, `dusk_vampires`, `dusk_banshees`, `battle_mummies` | shown |
| Opponents | Named leaders | some groups have a unique leader and start without options | - | - | [world.md](world.md) 8 | `qvl_okrim`, `boss_demon_lord`, `boss_lich`, `boss_gray_minotaur`, `boss_evil_eyes`, `boss_scorpion`, `boss_dark_rider`, `battle_assassins` | shown |
| Items and equipment | Slots | six equipped, six carried per character | - | 6 + 6 | [characters.md](characters.md) 2 | `profile_ryz`, `equip_prompt` | shown |
| Items and equipment | Class limits | shops mark and Equip refuses what a class cannot use | - | - | [findings.md](findings.md) | `shop_cant_use`, `equip_wrong_class` | shown |
| Items and equipment | Charges and magic | items with a power hold charges; Detect Magic shows them | Cast 1-2 | 3 charges | [characters.md](characters.md) 6 | `detect_magic` | shown |
| Items and equipment | Treasure containers | chests and boxes: open, find/remove trap, detect | `1`-`3`, who | 200 gems, Undead Amulet | [combat.md](combat.md) 5, 9 | `dusk_chest`, `chest_who`, `chest_opened`, `chest_find_trap`, `chest_detect`, `demo_treasure` | shown |
| Abilities and magic | Spell lists | 47 Cleric and 47 Sorcerer spells in 7 levels, by number | level, number | 94 | [content.md](content.md) 5 | `cast_prompt`, `combat_cast` | shown |
| Abilities and magic | Spell points | each cast costs points; level 1 casters have 5 or fewer | - | 1 point for the level 1 spells seen | [characters.md](characters.md) 5 | `cast_healed`, `quickref` | shown |
| Abilities and magic | Spells of higher levels | damage to several monsters, information, food; some fail by place, some cost gems | level, number | Lightning Bolt 30 points each; Create Food 3 points + 1 gem, +6 food; Fire Ball 18 points to the party | [characters.md](characters.md) 8, [findings.md](findings.md) | `combat_lightning_bolt`, `combat_fire_ball`, `combat_identify_monster`, `combat_sleep_goblins`, `cast_create_food`, `cast_spell_failed`, `vet_profile` | shown |
| Abilities and magic | Party spells | some spells stay in force and are listed under Protect | - | - | [characters.md](characters.md) 6 | `protect_three` | shown |
| World and navigation | Areas | 55 maps: 5 towns, 9 caverns, 20 wilderness sectors, castles and dungeons, the Astral Plane | - | 55 | [world.md](world.md) 1 | `outdoors_first`, `dungeon_lit`, `env_doom` | shown |
| World and navigation | Light | caverns and dungeons show "DARKNESS" without a light | Light spell, torch | Light (1) | [world.md](world.md) 3 | `dungeon_darkness`, `dungeon_lit`, `trap_door_after` | shown |
| World and navigation | Doors, locks, traps | locked doors are picked or bashed; traps hurt the whole party | `U`, `B` | - | [combat.md](combat.md) 9 | `door_locked`, `bash_trap`, `unlock_trap` | shown |
| World and navigation | Trap doors, spinners, portals | squares that move or turn the party | - | - | [sorpigal.md](sorpigal.md) 7, [world.md](world.md) | `trap_door`, `trap_door_after`, `qvl_floor_spins`, `cave_portal`, `algary_portal`, `astral_projector` | shown |
| World and navigation | Travel between towns | a leprechaun moves the party to any town for a gem; exits and stairs link areas | `1`-`5` | 1 gem | [sorpigal.md](sorpigal.md) | `leprechaun`, `leprechaun_algary`, `stairs_prompt`, `outdoors_cave`, `a1_castle_doom`, `e1_dragadune` | shown |
| World and navigation | Finding one's place | the Location spell gives sector and coordinates; there is no map screen | Cast 1-7 | - | [world.md](world.md) 4 | `location_spell` | shown |
| World and navigation | Messages and lore on squares | walls, statues and plaques carry hints | Search | 8 statues in Sorpigal | [sorpigal.md](sorpigal.md) 7 | `cave_wall_message`, `a1_ice`, `statue_lore`, `statue_archer`, `statue_cleric`, `statue_knight`, `statue_minotaur`, `statue_wizard`, `statue_robber`, `statue_paladin` | shown |
| Goals and gating | Quests from lords and others | castle lords, a courier job, a king's errand | `Y`/`N` | - | [world.md](world.md) 5 | `whitewolf_ironfist`, `whitewolf_quest`, `alamar_king`, `cave_courier`, `portsmith_zam`, `a1_dark_rider`, `cave_arena` | shown |
| Goals and gating | Gates | guards, golden doors and a key-card door stop a party without the right item or mark | - | - | [world.md](world.md) 5, 6 | `alamar_guards`, `doom_golden_door`, `astral_door`, `doom_true_king` | shown |
| Goals and gating | Ending | the Inner Sanctum rates the party and sends it on | - | 500,000 experience each | [world.md](world.md) 6 | `ending_panel`, `ending_sanctum`, `astral_room` | shown |
| Chance | Rolls at creation | all seven statistics are random; re-roll freely | `Enter` | 3-18 | [characters.md](characters.md) 1 | `create_roll` | shown |
| Chance | Which monsters, who is hit | groups, hits and damage are random and follow the moment of input | - | Sling hits 2-9 | [combat.md](combat.md) 3 | `outdoors_vines`, `combat_shoot` | shown |
| Chance | Bribe, retreat, surrender | may be accepted or refused | - | retreat 2 of 2, bribe 1 of 5, surrender 0 of 4 | [combat.md](combat.md) 6 | `encounter_bribe`, `encounter_surrender` | shown; Retreat has no message and no shot ([combat.md](combat.md) 6) |
| Chance | Traps | a failed unlock or disarm sets the trap off | - | Robber 1 of 1 unlock, 0 of 1 disarm | [combat.md](combat.md) 9 | `unlock_success`, `chest_find_trap` | shown |
| Failure and recovery | Party wiped | all six down: back to the last inn with what was saved | `Enter` | - | [combat.md](combat.md) 4 | `gameover` | shown |
| Failure and recovery | Cure and raise | the temple restores hit points and conditions for gold, the dead for more | temple `A` | 25 / 200 | [sorpigal.md](sorpigal.md) 6 | `temple_price`, `temple_dead` | shown |
| Failure and recovery | Healing in the field | rest, First Aid, Magic Herbs | - | +8 hit points | [characters.md](characters.md) 6 | `cast_healed`, `use_herbs_done`, `rest_complete` | shown |
| Saving and sessions | Sign in at an inn | writes the whole roster; the only save | `Y` at the inn | 18 characters | [sorpigal.md](sorpigal.md) | `save_inn_prompt`, `save_inn_list`, `portsmith_inn`, `portsmith_signed_in` | shown |
| Saving and sessions | Start of a session | title, options, pick a town, form the party | `Esc`, `Enter`, `1`-`5` | 5 towns | [interface.md](interface.md) 3 | `title_screen`, `ready_prompt`, `menu_options` | shown |
| Pacing and difficulty | Early game | level 1 characters have 7-15 hit points; four Poltergeists are a fair fight | - | 1-4 points per monster turn | [combat.md](combat.md) 3 | `combat_round`, `combat_victory` | shown |
| Pacing and difficulty | Open world, no level gates | every area can be walked into; late groups kill a new party in one round | - | 83 points of breath against 15 hit points | [combat.md](combat.md) 8 | `battle_red_dragons`, `boss_lich_eradicates` | shown |
| Pacing and difficulty | Message speed | combat messages stay for a time the player sets | combat `D`, `0`-`9` | default 5 | [interface.md](interface.md) 1 | none: the Delay order was not pressed, its prompt was not shot | described |

## 3. How the systems feed each other
- Fights give experience and (after Search) gold, gems and items; gold buys training, training turns experience
  into levels and hit points, levels win harder fights.
- Gold also buys food (rest), temple cures (recovery) and gear (armor class, damage); gems buy travel between
  towns and stronger spells.
- Spell points buy healing and light; rest restores them and costs food; food is lost wholesale to a bribe.
- Statues, wall messages and rumors (which cost tips) are the quest log: they point at places in other sectors,
  which the player must map alone.
- The inn fixes everything gained; a wipe returns the party to it, so the distance from an inn is the stake of
  every trip.

## Open questions
- What the handicap number changes; how long a potion's bonus lasts; what a donation at the temple does.
- Whether rest can be interrupted in the areas tried, and where Search finds treasure after a fight.
- The surprise rule (a party that is surprised gets no options): no message for it was seen.
