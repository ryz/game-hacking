# Phantasie - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. The same shots
also appear in [interface.md](interface.md) (the screens) and [content.md](content.md) (the variety of what
fills the game); overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py phantasie`.
Shot ids are those of the `main` set (`../shots/main/index.md`); the `start` set replays the opening honestly.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The player builds a party of up to six in a town Guild, walks it square by square through the wilderness and
into dungeons, fights the groups it meets, and returns to a town, where the gold and experience won are divided
into shares, experience is turned into levels by paid training and gold into equipment and spells **(verified:
start set, `town_shares_return`, `guild_training_cost`, `char_sheet_level2`)**. Each loop the party reaches
farther: stronger groups, more ranks of monsters, other towns and dungeons **(source: manual)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Town buildings | Six places on one screen: Guild, Armory, Bank, Inn, gate (leave), Mystic; letters C, U, G, P for cast, use, save, print **(verified)** | cursor + return, letters | - | [interface.md](interface.md) | `env_town_pelnor`, `town_pelnor_party`, `town_cast`, `use_items`, `printout` | shown |
| Player verbs | Wilderness commands | Return opens Inspect (status report), Use potion, Health, Cast spell, Move **(verified)** | cursor + return | - | interface.md | `world_cmd_menu`, `world_health`, `world_status` | shown |
| Player verbs | Dungeon commands | Cast, Inspect, Use, Health, Look, Move **(verified)** | cursor + return, then direction keys | - | interface.md | `dungeon_menu` | shown |
| Characters and progression | Creation | Race (human, dwarf, elf, halfling, gnome, random creature), class (thief, monk, ranger, fighter, priest, wizard), rolled attributes with keep/reroll, name **(verified)** | menus, Y/N, text | 6 attributes rolled; rolls depend only on how many rolls were made (RAM: route of `guild_created`) | [README.md](README.md) | `guild_new_race`, `guild_new_class`, `guild_roll`, `guild_name`, `char_sheet_ryz` | shown |
| Characters and progression | Roster and party | Up to 21 characters in the Guild roster (source); the party of up to six is added from it; drop, rename, purge **(verified prompts)** | menus | party 6 | - | `guild_roster`, `guild_party`, `guild_drop`, `guild_rename` | shown |
| Characters and progression | Experience and training | Experience only becomes a level by training at the Guild; it costs gold carried **(verified: 401 more XP needed after the first fight; level 1 to 2 costs 6 gp)**; a level raised ryz's attack skill from 64 to 101 and max HP from 11 to 12 **(verified: `char_sheet_ryz`, `char_sheet_level2`)** | Guild > training | level 2 at 472 XP for a human fighter (computed: 71 + 401) | - | `guild_training_cost`, `char_sheet_level2` | shown |
| Characters and progression | Skills | Attack, parry, swim, listen, spot trap, disarm, find item, pick lock on the sheet, rising with level **(verified)** | none | see sheets | - | `char_sheet_ryz`, `guild_inspect_cubi` | shown |
| Resources and economy | Gold | 256 gold per new character in the bank **(verified)**; carried gold is shared by the party, pooled from withdrawals; entering a town or saving divides gold and experience into shares, 0 to 3 per member, back into the bank **(verified: 273 gold per share after the first fight)** | Bank withdraw/deposit, shares | max 65000 in the bank (source) | - | `bank_menu`, `bank_withdraw`, `bank_deposit`, `town_shares_return` | shown |
| Resources and economy | Armory | Stock depends on what adventurers sold; Pelnor's first stock: small shield 2 gp, scroll 8 for 121 gp **(verified)**; bought items leave the stock ("sold") | buy, another shopper, exit | prices per item | - | `armory`, `armory_buy` | shown |
| Resources and economy | Inns | Town inns are free (source); an independent inn in the wilderness rests the party for 256 gold **(RAM: carried gold 1536 -> 1280)** | yes/no | 256 gp | - | `inn`, `world_inn_prompt`, `world_inn_rest`, `world_red_pony` | shown |
| Conflict | Party options | Each fight starts with beg mercy, threaten, greetings, fight, flee **(verified)**; beg mercy: the monsters take the party's gold (-256 GP each) **(verified)**; threaten and greetings: "monsters don't respond" against giant ants (verified); flee succeeded against ants and bees (verified) | cursor + return | - | - | `battle_party_options`, `battle_beg_mercy`, `battle_beg_result`, `battle_threaten`, `battle_flee` | shown |
| Conflict | Individual options | Per member thrust, attack, slash, lunge, spell, parry, kept from round to round **(verified)**; thieves pick a rank to hit **(verified: `battle_thief_rank`)**; unarmed-style choices that a member cannot use fall back to thrust **(inferred: attack and slash chosen for ryz became thrust)** | member list, option list, number selector | - | - | `battle_individual`, `battle_thief_rank`, `battle_spell_select` | shown |
| Conflict | Rounds and damage | Every member and monster acts in turn, one message each (hits, misses, takes N damage, dies) **(verified)** | none | hits of 3-6 damage by level-1 members (verified) | - | `battle_hit`, `battle_member_hurt`, `battle_ant_dies`, `battle_bee_hits`, `battle_round2_options` | shown |
| Conflict | Victory reward | "Each survivor gets N XP and N GP" **(verified: 73 XP + 17 GP for 3 bantirs; 166 XP + 0 GP for 11 ants and bees)** | none | - | - | `battle_killed`, `battle_reward`, `battle_ants_reward` | shown |
| Opponents | Groups in ranks | Monsters stand in up to three ranks; rank 1 is closest, most attacks reach only rank 1 (source), the screen lists each rank with count and name **(verified)** | - | up to 11 monsters seen | [content.md](content.md) | `battle_bantirs`, `battle_ants`, `battle_ants_options` | shown |
| Opponents | Encounters | Random while walking the wilderness (first after 28 steps east of Pelnor) and in dungeons (after about 100 steps) **(verified)** | walking | - | - | `world_encounter` | shown |
| Items and equipment | Equipment | One weapon, armour, shield each; new characters start with a club, robes and small shield **(verified: sheets)**; point values (":4") show strength **(verified)** | Armory | - | - | `char_sheet_ryz`, `armory` | shown |
| Items and equipment | Scrolls | 20 scrolls tell the story (source); scroll 8 is sold in Pelnor **(verified)** | Use items | - | - | `armory_buy`, `use_items` | shown |
| Abilities and magic | Spells | Spells by number; wizard cubi starts knowing spell 5, a fire attack that hit one monster for 5 damage **(verified)**; casting costs magic points (cubi 7 -> 6, RAM) | spell number selector or digit | - | - | `battle_cast`, `battle_spell_damage`, `battle_fire_rank3`, `battle_spell_select` | shown |
| Abilities and magic | Learning spells | At the Guild: the character may learn N more spells, 10 gold per try, possible spell numbers listed; the try can fail (source) **(verified: cubi learned spell 9)** | spell number | 10 gp per try | - | `guild_spells`, `guild_spell_learned`, `guild_inspect_cubi` | shown |
| World and navigation | Wilderness | Island map of 16 sections, one screen each, the party moves one square per key; terrain messages and descriptions of nearby places **(verified)** | direction keys | Pelnor at square 14,15 of its section (RAM) | - | `env_world_pelnor`, `env_world_west`, `world_path_message`, `world_hillside_door` | shown |
| World and navigation | Towns | 11 towns (source); stepping on one asks "A town. Enter?" **(verified)** | yes/no | - | - | `world_town_prompt`, `town_pineville_old` | shown |
| World and navigation | Dungeons | Entered from a door square ("A dungeon. Enter?"), then the dungeon disk is asked for; the first square is the exit; the map is drawn as the party explores it, each room type named **(verified)** | yes/no, disk swap, directions | - | - | `world_dungeon_prompt`, `dungeon_disk`, `dungeon_exit_prompt`, `env_dungeon_passage`, `env_dungeon_guardroom`, `env_dungeon_hall`, `env_dungeon_hallway` | shown |
| Goals and gating | Story | Defeat the Black Knights and Nikademus; scrolls tell the story (source) | - | - | - | none: not reached in this run | described |
| Chance | Rolls | Attribute rolls, hits, damage, encounters, spell learning are random **(verified for rolls and hits)**; rolls at creation do not depend on timing (RAM) | - | - | - | `guild_roll` | shown |
| Failure and recovery | Death | Characters can die ("dead" status, robert in the roster) **(verified)**; a dead party ends the game (source) | - | - | - | `guild_roster` | shown |
| Saving and sessions | Game save | Only in towns: G divides gold and experience into shares and writes the party to the boot disk; "Continue saved game" loads the party into its town **(verified)** | G | - | - | `save_saving`, `menu_start`, `town_pineville_old` | shown |
| Pacing and difficulty | Party score | The Mystic reports the party's score (2: novice adventurers) **(verified)** | - | - | - | `mystic` | shown |

## 3. How the systems feed each other
Fights give experience and gold -> entering town divides them into shares in the bank -> gold pays training
(levels, skills, hit points) and spell lessons, and buys equipment from what others sold -> a stronger party
reaches farther dungeons and stronger groups. Inns turn gold into hit points and magic outside towns.

## Open questions
- Game over screen (whole party dead) not captured: no fight in this run came close.
- What spell 5 and spell 9 are called (the C64 version shows numbers only); full spell list from the manual.
- Encounter rate formula; whether greetings or threaten ever work (only giant ants tried).
