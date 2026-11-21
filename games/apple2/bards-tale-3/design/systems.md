# The Bard's Tale III: Thief of Fate - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. The same shots
also appear in [interface.md](interface.md) (the screens) and [content.md](content.md) (the variety of what
fills the game); overlap is intended. Shot ids are those of the `main` set (`shots/main/index.md`) unless marked
`start` (`shots/start/index.md`). Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/bards-tale-3`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The party walks a grid of squares in first person (wilderness, city ruins, dungeons), meets random and fixed
encounters, fights them round by round with per-member orders (melee, spells by four-letter code, bard songs,
items), and earns experience and gold. Experience buys levels at the Review Board, gold buys spell levels and
healing; lit by Mage Flame, the party maps dungeon levels (automap) and solves their riddles to collect the
pieces that open the next dimension, until Tarjan himself is fought in his own realm. Between loops the world
changes (Skara Brae -> Arboria -> Gelidia -> Lucencia -> Kinestia -> Tenebrosia -> Tarmitia -> Malefia) and the
foes grow from single Pumas to groups of thirty demons **(verified for the start and the end; the order source)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Walk and turn | `i` one square forward, `j`/`l` turn; trees, rocks and walls block; `k` (or Return) enters a building or gate square, `i` does not **(verified: Skara Brae gate)** | i j l k | 1 square per key | playbook Controls | `walk_wild` (start), `skara_gate` (start), `skara_inside` (start) | shown |
| Player verbs | Where am I | `?` outdoors and in cities: square counted from a landmark and the time of day; in a dungeon it opens the automap | ? | "4 paces south and 13 paces west of the refugee camp", "It's now dusk" | interface | `system_whereami`, `city_where`, `restored` (start) | shown |
| Player verbs | Party commands outside combat | `p` per-member defend / party attack / use; `n` new marching order; `u` use an item; `b` bard plays; `c` cast; `1`-`7` view a member; ESC pause; `s` save | p n u b c 1-7 esc s | | interface | `party_menu`, `order`, `use_item`, `bard_walk`, `cast_walk`, `pause`, `inventory_view_char` | shown |
| Player verbs | Buildings | Each building has its own menu: storage (pick up), Review Board, temple (speak), tavern (order, talk), shrine (heal, pool gold), credits house | menu letters | | interface | `inventory_storage`, `menu_review_board`, `dialogue_temple`, `gameplay_tavern`, `gameplay_shrine`, `extra_interplay` | shown |
| Characters and progression | Creation | Sex, race (7), rolled St IQ Dx Cn Lk and HP (ESC rerolls), class (8 open at creation: Warrior Conjurer Magician Rogue Bard Paladin Hunter Monk), name | m/f, 1-7, 0-9, text | RYZ Human: St 11 IQ 10 Dx 11 Cn 11 Lk 9 HP 26 **(verified)** | playbook Naming | `menu_create_race`, `menu_create_class`, `menu_create_name`, `create_sex` (start) | shown |
| Characters and progression | Starting gear | A new character comes equipped by class (RYZ: Broadsword, Scale Armor, Buckler, Helm, Leather Gloves) | none | | content | `inventory_ryz` (start), `inv_ironpants` | shown |
| Characters and progression | Advancement | The Review Board elder raises one level when experience reaches the next threshold; each level adds hit points and one point to a statistic | a, member | Level 2 -> 3 needs 4000 total (2000 more at 2000); RYZ level 1 needs 2000; Ironpants HP 33 -> 48 and +1 IQ **(verified, exp poked to 6233)** | | `adv_no`, `adv_yes`, `advancement` (start) | shown |
| Characters and progression | Class change | Magic users may change class at the Review Board after knowing 3 spell levels of their art | c, member | 3 spell levels **(verified message)** | | `class_change`, `class_change2` | shown |
| Characters and progression | Character record | Level, sex, race, class, five statistics, spell points, experience, gold; Pool gold / Trade gold from the view | 1-7 | records 0400+0x80n (RAM) | playbook RAM map | `inventory_view_char`, `view_morganna`, `view_ryz` (start) | shown |
| Resources and economy | Gold | Per character; pooled at the shrine or from the character view; spent on spell levels, healing, tavern drinks and tips | p, t | new party 0 gold **(verified)** | | `shrine_pool`, `tavern_tip`, `shrine_sorry` (start) | shown |
| Resources and economy | Spell levels for gold | Spell Acquiring at the Review Board sells the next spell level of a caster's art | s, member | Conjurer level 2: 1000 gold; "Thou cannot acquire new spells yet" below the level **(verified)** | | `spell_acq`, `spell_acq_yes` | shown |
| Resources and economy | Healing | Shrine heals for gold; a dead character costs 900 gold (EBO, level 1) **(verified)** | h, member, payer | 900 for raising a level-1 character | | `gameplay_shrine`, `shrine_price` (start), `shrine_sorry` (start) | shown |
| Resources and economy | Spell points | Casting costs spell points; they come back while walking (DEDDO 1 -> 15 SP on the walk from the catacombs to the shrine) and the Review Board elder re-energizes all magic users on the first visit | | MAFL 2 SP, ARFI 3 SP **(verified on screen)** | | `elder_5` (start), `fled` (start), `shrine` (start) | shown |
| Conflict | Encounter | "You see N <monster> (distance)"; Fight bravely / Advance ahead (when the foe is far) / Run away | f a r | distance 10' to 90' | | `battle_puma`, `encounter` (start), `battle_dragon`, `battle_palace` | shown |
| Conflict | Round orders | Each member in turn picks an order (attack a group A-D, defend, party attack, cast, use an item, bard song); "Use these commands?" confirms | a d p c u b, y/n | ranks 1-3 attack in melee, deeper ranks get no Attack **(verified: KNIGHT rank 5)** | | `battle_options`, `options_bard` (start), `tarjan_target`, `confirm` (start), `battle_magic_eaters` | shown |
| Conflict | Round resolution | The round text scrolls by itself: hits, misses, damage, spells burning, monsters advancing; then "You still face ..." | none | Nefastmaster hits for 16 **(verified)** | | `battle_round`, `round` (start), `battle_dragon_round`, `tarjan_round` | shown |
| Conflict | Death and the party order | A dead member drops to the end of the party list and shows "Dead" | | | | `ebo_dead` (start), `tarjan_round` | shown |
| Conflict | Running away | Run away can fail (the round is fought) or succeed (the party leaves, the light can be lost) | r | failed once, succeeded once in the Nefastmaster fight | | `fled` (start) | shown |
| Conflict | Winning a fight | none: no fight was won within the budget (the Puma and the Black Dragon outlasted two rounds; the endgame fight has 63 foes); rewards text not captured | | | findings | none: not reached in budget | open |
| Opponents | Groups | Up to four groups (A-D) of up to 30+ each, with distances; the picture shows the first group | | Tarjan's summons: 2 High Priestesses, 30 Black Slayers, 30 Rock Demons, 1 Lorini | content | `tarjan_fight`, `battle_palace`, `battle_cougars` | shown |
| Opponents | Breath and special attacks | Dragons breathe at the whole party; some characters repel attacks | | Black Dragon breath fries for 100+ | | `battle_dragon_round` | shown |
| Items and equipment | Inventory | Up to 12 items per character (list with scroll), equipped items marked; picking an item offers equip/unequip, trade, drop | 1-7, space, Return | | | `inv_ironpants`, `inv_item_menu` | shown |
| Items and equipment | Storage building | Free starting gear in the ruins: Plate Armor, Halbard, Long Bows, Arrows, Wineskin, Lamps | 1-6, Return | | | `inventory_storage`, `storage_list` (start), `storage_pickup` (start) | shown |
| Abilities and magic | Spells | Typed as four-letter codes (MAFL Mage Flame, ARFI Arc Fire); a target prompt for attack spells | c, member, code, target | | | `system_cast_light`, `cast_walk`, `spell_prompt` (start), `spell_target` (start) | shown |
| Abilities and magic | Light | Dungeons are dark until a Mage Flame (or a lamp) burns; an icon row shows active effects (light, compass, shield ...) | | | | `system_cast_light`, `env_catacombs_lit`, `catacombs_dark` (start) | shown |
| Abilities and magic | Bard songs | A bard with an instrument plays one of six tunes in and out of combat (Sir Robin's Tune, Safety Song, Sanctuary Score, Bringaround Ballad, Rhyme of Duotime, Watchwood Melody) | b, song 1-6 | | | `bard_walk`, `bard_songs` (start) | shown |
| World and navigation | Wilderness and cities | 20x20 wilderness around the camp; 9 city maps (Skara Brae 17x17 ... Nowhere 11x11) | walk | 10 maps on disk 2 | playbook Game structure | `env_wild_camp`, `gameplay_skara_gates`, `arboria_env`, `celaria`, `env_gelidia` | shown |
| World and navigation | Dungeons | 61 levels on two disk sides, 5x5 to 22x22, stairs, passageways, portals and teleports | walk, y/n at stairs | | [maps/README.md](maps/README.md) | `gameplay_catacombs`, `env_lv34`, `env_lv16`, `env_lv21`, `env_lv2a` | shown |
| World and navigation | Automap | `?` in a dungeon draws a window of the level around the party; only visited squares are drawn | ? | square byte 4 bit 0 (RAM) | maps/README.md | `map_catacombs`, `unter_walk`, `map_unter4_walk`, `map_unter4_full` | shown |
| World and navigation | Disk changes | The game asks for the character disk (cities, saves) or a dungeon side; the wrong side is asked again | disk swap + key | | | `menu_chardisk`, `insert_side_a` (start) | shown |
| World and navigation | Dimension travel | Chronomancer spells travel between dimensions | | | | none: no Chronomancer in the parties used; cities reached by RAM warp | described |
| Goals and gating | Quest start | Review Board elder: destroy Brilhasti ap Tarj under Skara Brae, enter by saying TARJAN in the Mad God's temple | | | | `dialogue_review_hint`, `elder_3` (start), `tarjan` (start) | shown |
| Goals and gating | Final confrontation | Tarjan at square 3,2 of his realm: speech, conjures his friends, a fight against four groups | walk | | | `tarjan_meet`, `tarjan_2`, `tarjan_3`, `tarjan_4`, `tarjan_fight`, `gameplay_tarjan_end` | shown |
| Goals and gating | Ending | Not reached: the endgame fight was not won in the budget | | | | none: not reached | open |
| Chance | Encounters and rolls | Random encounters, hits and damage follow the frame timing (emulator RNG); no encounter switch found | | | | `encounter` (start) | shown |
| Failure and recovery | Death | Dead members stay in the party; the shrine raises them for gold; a full wipe ends the game (not captured) | | | | `ebo_dead` (start), `shrine_price` (start) | shown |
| Saving and sessions | Save anywhere | `s` saves the whole game to the character disk without a message; at power-on "restore your last saved game?" | s, y/n | | | `save_prompt`, `menu_restore`, `saved` (start), `restored` (start) | shown |
| Saving and sessions | Camp roster | Characters live on the character disk; the camp adds, removes, creates, deletes, saves a party under a name | a r c d s l e | 15 roster slots used by the dump | | `menu_roster`, `camp_remove`, `camp_delete`, `camp_save_party`, `camp_leave` | shown |
| Pacing and difficulty | First steps | A fresh level-1 party meets a Nefastmaster in the first catacombs corridor that hits for 16 of 26 HP: running and the shrine are the way out | | | | `fight_or_run` (start), `ebo_dead` (start) | shown |

## 3. How the systems feed each other
- Fights -> experience and gold -> Review Board levels (HP, statistics) and spell levels for gold -> stronger
  fights.
- Spell points -> light (MAFL) -> seeing and mapping a dungeon (automap) -> its riddles and exits.
- Death -> gold at the shrine -> back to full strength; no gold -> run, or play on without the member.

## Open questions
- Encounter switch and the rewards screen of a won fight; the ending after Tarjan.
- Meaning of square flag bytes 2-3 (maps) and the event list.
