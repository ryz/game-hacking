# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md); overlap is
intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/might-and-magic`.

Facts carry a confidence tag as everywhere in this folder; a table row without its own tag is **(verified)** by
the shots it names. A judgement (clear, slow, easy to miss) is written as **Observation:** with the reason,
never as a fact.

## 1. Conventions
- **Input:** keyboard only. Every command is one key: a letter printed on the screen in quotes or before a
  parenthesis, a digit for a party member or a numbered choice, arrow keys to move. Enter is needed only after
  typed text and numbers (names, amounts, the two spell numbers). ESC goes back one step everywhere and is
  printed as "'ESC' TO GO BACK". Ctrl with a letter is used for rare or dangerous actions (add to party,
  re-name, delete, quick fight). Keys typed early are kept and used by the next screen. A key that means
  nothing on a screen is ignored without a sound or message **(verified)**.
- **Layout:** 320 x 200, four colours on most machines' settings here (black, white, green, and the picture
  colours). Exploration: the view fills the top left (about 240 x 136), the command list the top right, the
  party in two columns under a green line, two message lines at the bottom. Text screens (profile, quick
  reference, combat) use the whole screen. Services keep the view and replace the lower third by their menu,
  with the service's name printed on the view's lower edge ("--TEMPLE--") **(verified: `start_inn_door`,
  `temple_services`)**.
- **Text:** one fixed-width font, capitals only, white on black; no colour coding of text. Prompts end in
  "(Y/N)?" or name the keys ("'A'-'F'", "1-6"). Errors and confirmations are framed by three stars ("*** WRONG
  CLASS ***", "*** DONE ***"). Trap and event shouts end in exclamation marks ("BLADES!!", "TRAP DOOR!")
  **(verified)**.
- **Feedback:** results are printed in the message lines and vanish after about one and a half seconds, or
  stay until the next key (statue plaques, quest texts). Nothing irreversible is confirmed except deleting a
  character ("ARE YOU SURE": manual) and saving a new character; Discard and trap attempts act at once.
  In combat the message time is a setting (Delay 0-9) **(verified; delete from the manual)**.
- **State visibility:** always visible while exploring: the six names and their order. Hit points, spell
  points, armor class, food and condition need the quick reference (`Q`); gold, gems, items and statistics need
  a profile. In combat the formation, who can strike (`+`), who is hurt (`*` before the number) and the
  monster list are always on screen; monster hit points are never shown, only "(WOUNDED)". The place is never
  named; the Location spell prints coordinates **(verified)**.
- **Help and onboarding:** the command list on the exploration screen and the options line in combat are the
  only help; the title's demo scenes show sample screens. Spell names, numbers and effects, item powers and the
  map exist only in the manual and the player's notes **(verified; manual)**.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title pictures | screen | power-on -> ready prompt, demo | brand and start | two animated pictures, "ESC TO START GAME / SPACE FOR SCENES" | `Esc`, `Space` | - | `title_screen`, `title_book_one` | **Observation:** the key prompt appears only after about ten seconds |
| Demo scenes | screen | title -> title | show what play looks like | still pictures of sample screens | `Space` | - | `demo_stronghold`, `demo_treasure` | **Observation:** they look like live play but are pictures |
| Ready prompt | prompt | title -> options | a pause before the menu | "ARE YOU READY? THEN PRESS ENTER!" | `Enter` | - | `ready_prompt` | |
| Options menu | menu | ready prompt, inn list -> creation, roster, inn list | start of every session | three entries | `C`, `V`, `1`-`5` | - | `menu_options` | **Observation:** "go to town" lists no town names |
| Creation: roll | screen | options -> race | roll statistics, pick class | seven statistics, eligible classes | `Enter`, `1`-`6`, `Esc` | - | `create_roll` | **Observation:** classes the roll misses are simply not listed, with no reason given |
| Creation: race, alignment, sex | menu | roll -> name | choices | numbered lists | digits | - | `create_race`, `create_alignment` | |
| Creation: name and save | prompt | sex -> roll or options | name, confirm | "NAME:", "SAVE CHARACTER (Y/N)?" | letters, `Enter`, `Y`/`N` | - | `create_name`, `create_save` | |
| Roster list | list | options -> profile | see all characters | letter, name, town, level, class | `A`-`R`, `Esc` | - | `roster_view_all` | |
| Profile (from the roster) | screen | roster -> rename, delete | inspect, manage | full character sheet, Ctrl-N, Ctrl-D | `Ctrl-N`, `Ctrl-D`, `Esc` | - | `profile_menu`, `rename_prompt` | |
| Inn list | list | options, sign-in -> town | form the party | characters lodged here, `@` marks members | `Ctrl`+letter, `X`, `Esc` | - | `save_inn_list`, `portsmith_signed_in` | **Observation:** leaving with `Esc` instead of `X` disbands the party without warning |
| Exploration screen | screen | inn list -> everything | the main view | 3-D view, command list, party, messages | arrows, command letters, `1`-`6` | "LOCKED!", "SEARCH: NOTHING" | `start_inn_door`, `outdoors_first`, `dungeon_lit`, `env_doom` | **Observation:** the command list cuts its last entries at the screen edge ("QUIKREF", "VIEW CH") |
| Command list | hud element | exploration | remind the keys | ten commands with their letters | - | - | `sorpigal_inn_sign` | |
| Party list | hud element | exploration, encounter, combat | who is in the party, in order | number and name, two columns | - | redrawn after Order | `order_done` | **Observation:** shows no health at all while walking |
| Darkness | message | dark areas | no light | "DARKNESS" in place of the view | - | - | `dungeon_darkness` | the same frame wherever it is dark (after the trap door too) |
| Sign over a door | message | facing a service door | name the place | "A SIGN ABOVE THE DOOR READS:" | - | - | `sorpigal_inn_sign`, `portsmith_inn_sign` | also what a retreat from the room at (3,6) ends on |
| Event text with Y/N | prompt | stepping on a square | offer something | one to five lines of text, "(Y/N)?" | `Y`, `N` | the text of the result | `save_inn_prompt`, `stairs_prompt`, `statue_prompt`, `shop_blacksmith_prompt`, `market_food`, `leprechaun`, `cave_portal`, `cave_arena`, `outdoors_forest`, `outdoors_fountain`, `outdoors_statues`, `outdoors_cave`, `a1_castle_doom`, `e1_dragadune`, `algary_portal`, `whitewolf_button`, `whitewolf_ironfist`, `a1_dark_rider`, `env_forest_c1` | **Observation:** the same prompt form serves shops, stairs and story choices, so nothing marks a choice as important |
| Event text without a choice | message | stepping on a square | lore, refusals, effects | lines of text, sometimes filling the lower third | any key or time | - | `statue_lore`, `statue_archer`, `statue_cleric`, `statue_knight`, `statue_minotaur`, `statue_wizard`, `statue_robber`, `statue_paladin`, `cave_wall_message`, `cave_courier`, `a1_ice`, `portsmith_zam`, `portsmith_secret`, `portsmith_blacksmith`, `portsmith_inn`, `algary_inn`, `algary_mystic`, `dusk_inn`, `dusk_training`, `erliquin_agar`, `erliquin_inn`, `erliquin_training`, `alamar_guards`, `alamar_king`, `doom_golden_door`, `doom_true_king`, `whitewolf_quest`, `qvl_floor_spins`, `astral_door`, `astral_projector`, `astral_room`, `outdoors_gypsy`, `trap_door` | |
| Numbered event choice | menu | some event squares | more than yes or no | numbered options | digits | - | `alamar_prisoner` | |
| Order prompt | prompt | exploration `O` -> exploration | re-order | "NEW ORDER", the typed digits | six digits, `Esc` | list redrawn | `order_prompt`, `order_done` | |
| Protect list | screen | exploration or combat `P` | active spells | one line per spell, value where it has one | `Esc` | - | `protect_active`, `protect_three` | |
| Rest prompt and result | prompt | exploration `R` | rest | "REST HERE (Y/N)?", "REST COMPLETE: NO ENCOUNTERS!" | `Y`, `N` | - | `rest_prompt`, `rest_complete` | |
| Search result | message | exploration `S` | search | "SEARCH: NOTHING" or a find | - | - | `search_nothing` | |
| Who will try | prompt | Unlock, chest options | pick the character | "WHO WILL TRY '1'-'6'?" | `1`-`6`, `Esc` | "SUCCESS!" or a trap message | `unlock_who`, `chest_who`, `unlock_success` | |
| Trap message | message | failed Unlock, Bash, chest | announce damage | "BLADES!! ...", "GAS!! ..." | - | no numbers: damage shows only in the quick reference | `unlock_trap`, `bash_trap`, `chest_find_trap`, `trap_damage` | **Observation:** the player is not told how much each character lost |
| Quick reference | screen | exploration, profile, combat `Q` -> profile | party status at a glance | hit points now/maximum, spell points, armor class; food and condition in a second block | `1`-`6`, `Esc` | - | `quickref`, `trap_damage`, `unconscious_quickref`, `conditions_quickref`, `combat_conditions`, `encounter_bribe_food`, `market_food_after` | **Observation:** two blocks with repeated numbers instead of one row per character make the eye jump |
| Profile (in play) | screen | `1`-`6` -> its commands | everything about one character | header, statistics, level, age, experience, spell points, gems, hit points, gold, armor class, food, condition, equipped 1-6, backpack A-F, command keys | command letters, digits for another member, `Esc` | prompts replace the command block | `profile_ryz`, `profile_level2`, `vet_profile`, `temple_cured_profile`, `cast_healed`, `use_might_potion`, `use_herbs_done` | **Observation:** statistics show only the current value, so a potion's bonus cannot be told from the base |
| Item prompt | prompt | profile `E`, `R`, `D`, `U` | choose an item | "EQUIP WHICH ITEM: 'A'-'F'?" and the like | letter or digit, `Esc` | "*** WRONG CLASS ***", "*** NO SPECIAL POWER ***" | `equip_prompt`, `remove_prompt`, `discard_prompt`, `use_prompt`, `equip_wrong_class`, `use_no_power`, `remove_done`, `discard_done` | **Observation:** Discard has no confirmation |
| Kind prompt | menu | profile `S`, `G`, `T` | choose gems, gold, food (or item) | numbered list beside the prompt | `1`-`4` | the profile's numbers change | `share_prompt`, `gather_prompt`, `trade_which`, `share_done`, `gather_done` | |
| Member prompt | prompt | Trade, Use and Cast with a target | choose a character | the party list and "TRADE WITH: '1'-'6'?" / "CAST ON: '1'-'6'?" | `1`-`6` | - | `trade_with`, `cast_on_whom`, `use_herbs_target` | |
| Amount prompt | prompt | Trade | type a number | "HOW MUCH:" with a cursor | digits, `Enter` | - | `trade_how_much`, `trade_gold_done`, `trade_item_done`, `trade_food_done` | |
| Spell prompt | prompt | profile or combat `C` | choose a spell | "CAST SPELL: LEVEL= NUMBER=", "'ENTER' TO CAST" | two digits, `Enter`, `Esc` | "*** DONE ***", a result text, or "NOT ENOUGH SPELL POINTS" | `cast_prompt`, `cast_done`, `cast_spell_failed`, `cast_create_food`, `combat_cast`, `location_spell`, `detect_magic` | **Observation:** spells have no names on screen; the player needs the manual's numbers |
| Shop menu | menu | blacksmith event -> lists | choose a list | shopper, gold, four entries, gather and other-character keys | `A`-`D`, `G`, `1`-`6`, `Esc` | - | `shop_blacksmith_menu` | |
| Shop list | list | shop menu | buy or sell | six items with prices; "-" marks what the shopper cannot use | `A`-`F`, `Esc` | "THANK YOU!" | `shop_weapons`, `shop_armor`, `shop_misc`, `shop_sell`, `shop_cant_use`, `portsmith_weapons`, `portsmith_armor`, `portsmith_misc` | **Observation:** items show no statistics, only a price |
| Temple menu | menu | temple event | services with prices | four services, "----" where not needed | `A`-`D`, `G`, digits | price turns to "----" | `temple_services`, `temple_price`, `temple_cured`, `temple_poisoned`, `temple_dead`, `temple_donation` | **Observation:** one entry "restore health" covers wounds, poison and death; only the price tells them apart, and not wounds from poison: the menu for a poisoned character is the same picture as `temple_price`; `temple_poisoned` is the clerics' prompt with the star that marks him in the party list |
| Tavern menu | menu | tavern event | drink, tip, rumors | three entries | `A`-`C` | a line of text, or nothing | `tavern_menu`, `tavern_drink`, `tavern_rumor` | **Observation:** "listen for rumors" answers with silence until tipped, which reads as a dead option |
| Market message | message | market event | sell food | "THANK YOU, COME AGAIN!" | - | - | `market_bought` | |
| Training screen | menu | trainer event | level up | level offered, experience missing or cost | `A`, `G`, digits | "CONGRATULATIONS! ...", "*** NOT ENOUGH GOLD ***" | `train_level2`, `train_levelup`, `train_level3_need`, `train_level8_need`, `train_no_gold` | |
| Encounter screen | screen | fight square -> combat or map | meet the monsters | the first monster's picture in the view, the list A.., four options | `A`, `B`, `R`, `S` | "NO RESPONSE", "THE MONSTERS DON'T TAKE PRISONERS!", a demand | `encounter_poltergeists`, `encounter_bribe`, `encounter_surrender`, `encounter_bribe_demand`, `encounter_bribe_paid`, `encounter_goblins`, `encounter_guardsmen`, `bash_after`, `battle_caryatids`, `battle_medusas`, `boss_dark_rider` | **Observation:** only the first kind in a mixed group gets a picture |
| Combat screen | screen | encounter -> map, game over | play the rounds | round, formation, monster list, keys, handicap, party, options or message | order letters | messages in the bottom lines | `combat_round`, `combat_options`, `cave_arena_fight`, `boss_scorpion` | |
| Combat options line | menu | combat, per character | what this character may do | only the orders available to it | letters | - | `combat_options`, `combat_exchange_done` | **Observation:** the available orders change place from character to character |
| Combat prompts | prompt | Fight, Exchange, Cast, Use | choose target, partner, spell, item | "FIGHT WHICH 'A'-'C'?", "EXCHANGE PLACES WITH (1-6)?" | letters, digits, `Esc` | - | `combat_fight_prompt`, `combat_exchange_prompt`, `combat_use`, `combat_cast` | |
| Combat message | message | every action | say what happened | who, what, hits, points, result | waits the Delay time | - | `combat_spell_hit`, `combat_lightning_bolt`, `combat_fire_ball`, `combat_sleep_goblins`, `combat_shoot`, `combat_bless`, `combat_sleep_immune`, `combat_turn_undead`, `combat_dragon_breath`, `combat_dies`, `combat_stoned`, `combat_paralyzed`, `combat_lava_beast`, `combat_magicians`, `boss_lich_eradicates`, `boss_demon_drain`, `boss_demon_drains`, `death_party_down` | **Observation:** the message replaces the options line, so a slow reader loses it when the next prompt appears |
| Monster information | message | Identify Monster in combat | show a monster's numbers | name, hit points, armor class, speed, attacks, maximum damage, three Y/N traits | waits the Delay time | - | `combat_identify_monster` | **Observation:** the only place the game shows a monster's statistics |
| Victory message | message | last monster down -> map | pay out | experience per survivor | any key | - | `combat_victory` | |
| Treasure container | menu | Search or an event square | open safely or not | the container's picture and name, three options | `1`-`3`, `Esc` | "IT OPENS!", shares, finds; "MAGIC (Y) TRAP (Y)" | `dusk_chest`, `chest_opened`, `chest_detect` | |
| Game over | screen | party wiped -> options | restart from the inn | boxed text | `Enter` | - | `gameover` | |
| Ending text | screen | Inner Sanctum | close the story | panel text, performance total | any key | - | `ending_panel`, `ending_sanctum` | |

## 3. Screen flow
```
power-on -> title pictures --Space--> demo scenes
                |Esc
            ready prompt --Enter--> OPTIONS MENU
              C -> creation (roll, class, race, alignment, sex, name, save) -> options
              V -> roster list -> profile (re-name, delete)
              1-5 -> inn list of that town --X--> EXPLORATION
EXPLORATION (view, commands, party, messages)
  arrows -> next square -> event text (Y/N, choices) -> shop / temple / tavern / training menus -> exploration
                        -> inn prompt --Y--> inn list (saved) --Esc--> options menu
                        -> encounter screen --A / refused B, S--> COMBAT -> victory message -> exploration
                                            --R, accepted B--> exploration
                                                               COMBAT -> all down -> game over -> options menu
  O order, P protect, R rest, S search, B bash, U unlock (who will try) -> exploration
  Q quick reference <-> 1-6 profile -> C cast, D discard, E equip, G gather, R remove, S share, T trade, U use
  Search or event -> treasure container (open, find/remove trap, detect) -> exploration
```

## 4. Elements in detail
**Exploration screen** (`start_inn_door`): the view is drawn in perspective three squares deep, with doors,
torches, portcullises and outdoor terrain as flat pictures; a green frame line separates it from the party
list. The right column "COMMANDS" never changes. The two bottom lines are empty until something speaks; signs,
"LOCKED!" and search results use them. Service menus take over everything under the view and print the
service's name on the view's lower edge **(verified)**.

**Profile** (`profile_ryz`): line 1 number, name, sex, alignment, race, class; a block of seven statistics on
the left with level, age, experience, spell points now/maximum and spell level in brackets, gems, hit points
now/maximum, gold, armor class and food to the right; "COND=" below; then two columns, EQUIPPED 1-6 and BACKPACK
A-F; the bottom three lines list the command keys and are replaced by a prompt while a command runs
**(verified)**.

**Combat screen** (`combat_round`, `combat_options`): top left "COMBAT ROUND #n"; under it the formation as
two columns of numbers, `+` before those who can fight hand to hand, the acting character's number in inverse,
`*` before a character who is down or disabled (`combat_conditions`, `combat_lava_beast`); top right the
monster list with letters, `+` for monsters in reach, "(WOUNDED)" after dots; mid left the keys that do not
use a turn (Delay, Protect, Quickref, View Ch) and the handicap line; a dashed line; the party list; the bottom
three lines alternate between "OPTIONS FOR: name" with that character's orders and the message of the last
action **(verified)**.

**Shop list** (`shop_weapons`, `shop_cant_use`): shopper's name and gold on the left with the fixed keys, the
list title and six lettered items in the middle, prices right-aligned; a "-" between letter and name marks an
item the shopper's class cannot use; the legend "(- = CANT USE)" is printed under the keys **(verified)**.

**Encounter screen** (`encounter_poltergeists`, `boss_dark_rider`): the monster's picture is pasted into the
middle of the current view, so the walls or the landscape frame it; the list of up to fourteen names covers the
right part of the view; the options line sits under the party list **(verified)**.

## Open questions
- The Delay prompt, the "NOT ENOUGH SPELL POINTS" message, the delete confirmation and the bribe refusal after
  a demand were not shot.
- Whether any screen shows the date or time of day (none seen).
