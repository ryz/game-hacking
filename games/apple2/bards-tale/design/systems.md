# The Bard's Tale: Tales of the Unknown - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. The same shots
also appear in [interface.md](interface.md) (the screens) and [content.md](content.md) (the variety of what
fills the game); overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/bards-tale`.
Shot ids in backticks are from the `main` set (`../shots/main/index.md`); the `start` set retells the first hour.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The party of up to six leaves the Guild of Adventurers into the snow-bound city of Skara Brae, fights the
monster groups that meet it in the streets, and comes back to spend its gold: healing at temples, spell points
at Roscoe's, arms at Garth's, levels and spell levels at the Review Board. Stronger, it enters the dungeons in
a fixed order (Wine cellar and Sewers, Catacombs, Harkyn's Castle, Kylearan's Amber Tower, Mangar's Tower),
mapping them by hand, answering riddles and collecting the objects that open the next place, until it defeats
Mangar the Dark in his tower and Kylearan ends the eternal winter **(verified: shots below; order of the
middle dungeons source: Wikipedia)**. What changes between loops: the monster level of the dungeon
(0 in the cellar to 7 at the top of Mangar's Tower) and the party's levels, spell levels and equipment.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Movement | step forward, turn left or right; kick through doors and into buildings | I, J, L (arrows), K | 22 by 22 dungeon levels that wrap, 30 by 30 city | [maps/README.md](maps/README.md) | `env_city_street`, `env_city_houses`, `env_cellar_corridor` | shown |
| Player verbs | Where am I | the street name and the time of day | ? | "early morning" at the start | - | `gameplay_where` | shown |
| Player verbs | Cast | a member casts a spell by typing its four-letter code | C, member, code | - | Abilities below | `spell_cast_prompt`, `system_mafl` | shown |
| Player verbs | Bard song | the Bard plays one of six tunes; he needs an instrument equipped | B, member, 1-6 | 6 tunes | Abilities below | `song_no_instrument`, `song_prompt` | shown |
| Player verbs | Use item | a member uses an item from his list | U, member, item | - | - | `system_use` | shown |
| Player verbs | Party attack | outside a fight a member may attack his own party | P | - | [findings.md](findings.md) | `system_party_attack` | shown |
| Player verbs | New order | the six places are reordered (only places 1-3 can strike in melee) | N, five picks | - | - | `menu_new_order` | shown |
| Player verbs | View member | statistics page, then items and spell levels: equip, trade, drop, pool gold | 1-6, then E T D P | 8 item slots | - | `inventory_stats`, `inventory_items`, `inventory_bard_items` | shown |
| Characters and progression | Creation | race (7), rolled attributes St IQ Dx Cn Lk and hit points, then a class open to that race, then a name; no re-roll | Disk options, Create | Human: 8 classes offered; Dwarf: 6 (start set `13_dwarf`) | - | `system_race`, `system_class` | shown |
| Characters and progression | Classes | Warrior, Paladin, Rogue, Bard, Hunter, Monk fight; Conjurer and Magician cast; Sorcerer and Wizard come by class change | - | - | - | `system_class`, `system_class_change` | shown |
| Characters and progression | Advancement | the Review Board raises a level when the experience is enough | Review Board, A, member | level 1 Warrior needs 2000 experience; level 9 RYZ still needs 18260 | - | `system_review`, `system_review_xp`, `system_advance` | shown |
| Characters and progression | Spell levels | mages buy each spell level at the Review Board | Review Board, S | Conjurer level 2: 1000 gold **(verified)** | - | `system_spell_buy`, `inventory_hero_spells` | shown |
| Characters and progression | Class change | a mage changes to another mage class after learning at least three spell levels | Review Board, C | 3 spell levels | - | `system_class_change` | shown |
| Resources and economy | Gold | each character carries his own gold; Pool gold gives it all to one | View or shop, P | new characters about 100-200 gold (RYZ 176) | - | `shop_pool`, `inventory_hero_stats` | shown |
| Resources and economy | Garth's Equipment Shoppe | buy, sell, identify; the list pages forward and back | B S I P E | Torch 5, Lamp 15, Broadsword 80, Short Sword 30, Dagger 20, War Axe 70, Halbard 200, Mace 60, Staff 20; sells at half (Mace 30) **(verified)** | - | `shop_garth`, `shop_menu`, `shop_buy`, `shop_buy2`, `shop_sell`, `shop_identify` | shown |
| Resources and economy | Temples | heal wounds and raise the dead for gold | member, payer | wounds 10 gold per hit point (RYZ 9 points: 90); raising a level-1 Paladin 900 **(verified: start set)** | - | `system_temple` | shown |
| Resources and economy | Roscoe's Energy Emporium | spell points restored for gold | member, payer | 600 gold for 38 points of a level-8 Conjurer **(RAM: points poked)** | - | `system_roscoe`, `system_roscoe_price` | shown |
| Resources and economy | Taverns | drinks; the barkeep talks only for a tip; Wine at the Scarlet Bard opens the cellar | O, T, amount | tip of 100 gold gave a rumour | - | `dialogue_tavern`, `dialogue_drinks`, `dialogue_barkeep`, `dialogue_barkeep_tip`, `dialogue_rumour` | shown |
| Resources and economy | Spell points | casting spends them; they come back at Roscoe's (and with time, source) | - | MAFL costs 2 (scout) | - | `inventory_hero_stats` | shown |
| Conflict | Encounter | a group or several groups (up to four) meet the party; Fight or Run | F / R | random: a roll on every step, about 1 in 64 **(RAM: code)**; forced-fight squares in dungeons | - | `battle_encounter`, `battle_golem` | shown |
| Conflict | Round orders | each member gets an order: Attack a group (places 1-3), Party attack, Defend, Use, Cast, play (Bard); then confirm | A P D U C B, group, Y-N | - | - | `battle_target`, `battle_round` | shown |
| Conflict | Round report | blows and spells are told line by line, the text scrolls by itself; the dead move to the back | - | a Skeleton hits a level-1 character for 7-12 | - | `battle_round`, `boss_mangar_spell` | shown |
| Conflict | Running | Run can get the party away; the fight ends at once | R | worked against 4 Skeletons (start set `32_fled`) | - | none: in the `start` set (`32_fled`) | shown |
| Conflict | Victory | each character gets experience and gold; items may be found | - | "CUBI found a Misc. Item" | - | `ending_treasure` | shown |
| Opponents | Monster groups | up to four groups, each with its own count and portrait; magic users summon and cast | - | monster level per dungeon level 0-7 | [content.md](content.md) | `battle_humans`, `battle_stone_giants`, `boss_mangar_group` | shown |
| Opponents | Guardian statues | statues in the city bar the way to castle and towers and come to life when attacked | A / L | Stone Golem, Stone giant, Grey Dragon | - | `gameplay_guardian`, `battle_golem` | shown |
| Items and equipment | Item list | eight slots; a mark shows equipped and unusable items | View, E | status: carried, equipped, unusable **(RAM)** | - | `inventory_items`, `inventory_bard_items` | shown |
| Items and equipment | Identification | unknown items can be identified at Garth's | I | - | - | `shop_identify` | shown |
| Abilities and magic | Spells | four-letter codes per class and level; some act at once (light, compass, location), some ask a target | C, code | Conjurer and Magician levels 1-7 (source) | - | `system_mafl`, `spell_scsi`, `spell_maco`, `spell_lere`, `spell_levi`, `spell_aren`, `spell_wohl` | shown |
| Abilities and magic | Bard songs | six tunes with lasting effects; need an equipped instrument | B | - | - | `song_prompt` | shown |
| World and navigation | City | 30 by 30 streets; buildings are entered by kicking; most are empty houses | K | 7 taverns, 15 temple squares, 1 shop, Roscoe's, Review Board | playbook City map | `hud_city`, `gameplay_where`, `extra_credits` | shown |
| World and navigation | Gates | the city gate is snowed in; iron gates and a magic mouth close Kylearan's and Mangar's towers | - | - | - | `gameplay_gate`, `gameplay_iron_gate`, `gameplay_magic_mouth` | shown |
| World and navigation | Dungeon entrances | wine at the Scarlet Bard, the sewer portal, the Mad God's priest (name), the castle and tower entry chambers | O, Y, S, T | - | - | `dialogue_madgod`, `gameplay_sewer_portal`, `gameplay_castle_entry`, `gameplay_tower_entry` | shown |
| World and navigation | Light | dungeons are dark without a light spell or torch; darkness squares put the light out | MAFL, LERE | - | [maps/README.md](maps/README.md) | `system_mafl`, `gameplay_darkness` | shown |
| World and navigation | Stairs and portals | stairs ask Y-N when stepped on; portals in floors and ceilings (code) | Y / N, D / E | 16 levels in 6 dungeons | [maps/README.md](maps/README.md) | `gameplay_stairs` | shown |
| World and navigation | Special squares | inscriptions, voices, magic mouths with riddles, traps, smoke | type an answer | - | [maps/README.md](maps/README.md) | `gameplay_sewers_inscription`, `gameplay_ky_riddle`, `gameplay_trap`, `gameplay_smoke` | shown |
| World and navigation | Maps | no automap; SCSI tells levels and squares from the entry stairs | - | - | [maps/](maps/README.md) | `spell_scsi` | shown |
| Goals and gating | Quest objects and riddles | objects and names open the way (the name TARJAN for the Catacombs, a silver triangle, the riddle answers) | type, find | three shapes etched in Mangar's tower: square, circle, triangle | - | `gameplay_silver_triangle`, `gameplay_m5_shapes`, `gameplay_m5_bind` | shown |
| Goals and gating | Final goal | defeat Mangar in his antechamber at the top of his tower | - | Mangar with 2 Greater demons and 3 Vampire lords | - | `boss_mangar`, `boss_mangar_friends`, `boss_mangar_group` | shown |
| Goals and gating | Ending | Kylearan appears, the winter will end, a bonus of 300,000 gold and experience | key | 300,000 | - | `ending_kylearan`, `ending_winter`, `ending_bonus`, `ending_vanishes` | shown |
| Chance | Rolls | attributes at creation, encounters, monster groups, hits and damage, running | - | - | - | none: rolls show only through their results (`system_class`, `battle_round`) | described |
| Failure and recovery | Death | a member at 0 hit points is Dead; the temple raises him for gold; the whole party dead ends the game | - | - | - | `gameover_party_dead` | shown |
| Saving and sessions | Saving | characters are written to the character disk when made and when the party is saved in the Guild; a party is saved under a name (`*NAME`) | Disk options, S | - | - | `menu_roster`, `menu_disk_options` | shown |
| Pacing and difficulty | Difficulty | a level-1 party loses members in its first street fight; monster level rises with each dungeon level | - | level-1 Paladin killed by one 8-point blow | - | `battle_round` | shown |

## 3. How the systems feed each other
- Fights -> experience and gold -> Review Board (levels, spell levels) and Garth's (arms) -> stronger fights.
- Fights -> wounds and spent spell points -> temples and Roscoe's (gold) -> back into the streets.
- Dungeon specials (riddles, inscriptions, rumours bought in taverns) -> names and objects -> the next dungeon.
- Light (spell points) -> seeing walls and doors -> mapping by hand (no automap) -> finding stairs and specials.

## Open questions
- Spell list beyond the codes tried (MAFL ARFI SCSI MACO LERE LEVI AREN WOHL); the manual was not reachable.
- What the six bard tunes do (no visible effect outside a fight).
- Exact experience table and hit point gains per level.
