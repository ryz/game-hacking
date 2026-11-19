# Might and Magic II: Gates to Another World (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
Walk the party square by square through an area, meet fixed and random encounters, fight them in turn-based
menus, search the square for treasure, and return to a town to spend the gold on training, equipment, spells,
skills and healing; sign in at an inn to save **(source: manual; verified: walking, encounters, inn)**. Between
loops the party grows in level and spell level, buys secondary skills that open new terrain (mountains,
forests, water), and follows quest texts to new areas and other centuries **(source: manual, area texts)**.

## 2. Systems
Shot ids are the planned ids of `../shots.txt` (scout 2026-11-19); "planned" = not captured yet.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move and turn | one square forward or back, 90-degree turns; walls answer with a message **(verified)** | arrows | - | [world.md](world.md) | gameplay_inn_start, gameplay_outdoors_c2 | described |
| Player verbs | Exploration commands | bash, controls, dismiss, exchange, quick ref, rest, search, unlock, protect, location, view character **(verified: every prompt)** | letters | - | [../playbook.md](../playbook.md) Controls | options_controls, system_protect, system_rest_prompt, system_search_nothing, system_location, system_exchange, system_dismiss, inventory_quickref | described |
| Player verbs | Character sheet actions | cast, drop, equip, gather, remove, share, trade, use **(verified: prompts)** | letters | backpack 6, equipped 6 **(source)** | - | inventory_profile_ryz | described |
| Characters and progression | Creation | seven statistics rolled 3-21, two can be exchanged, eligible classes listed, then race, alignment, sex, name **(verified)** | Enter re-rolls, letters exchange | race modifiers e.g. Gnome +2 Luck -1 Speed -1 Accuracy **(source)** | - | create_roll, create_exchange, create_race, create_alignment, create_sex, create_name | described |
| Characters and progression | Classes | Knight, Paladin, Archer, Cleric, Sorcerer, Robber, Ninja, Barbarian; prime statistic 13 or 15 **(source; eight listed on screen: verified)** | - | hit points per level 1-6 (Sorcerer) to 1-12 (Knight, Barbarian) **(source)** | - | create_roll | described |
| Characters and progression | Levels and training | experience is paid for at a training ground; about 2,000 for level 2, doubling **(source)** | `y` at the trainer | - | - | system_training | described |
| Characters and progression | Secondary skills | two per character, bought from trainers (Cartographer 10 gold, Pathfinder and Mountaineering 2,000 gold in Middlegate), removed by Brain Detoxification for 100 gold **(verified: offers)** | `y` | 15 skills **(source)** | - | system_otto_mapper, system_detox | described |
| Characters and progression | Ageing | characters age; old characters can die while resting after about 80 **(source)** | - | start age 18 **(verified)** | - | inventory_profile_ryz | described |
| Characters and progression | Hirelings | premade characters hired at inns after quests, paid daily, up to 7, 8 members in all **(source)** | inn list, `d` dismiss | - | - | menu_hirelings, system_dismiss | described |
| Resources and economy | Gold, gems, food | gold buys services; gems pay for higher spells; one food per character per rest, 40 at most **(source)** | trade, share, gather | prices seen: guild 20, Otto Mapper 10, portal 10, locksmith key 500, trainers 2,000, resort trip 5,000 gold **(verified)** | - | system_mage_guild, system_poorman_portal | described |
| Resources and economy | Light | light units are spent one per dark square; Light spell gives one **(source; Light cast verified)** | cast | - | - | system_protect, system_cast_spellbook | described |
| Conflict | Encounters | options attack, bribe, hide, run; surprise skips them **(source; options verified)** | letters | - | - | battle_encounter | described |
| Conflict | Combat | turn order by speed; per character attack, fight, shoot, cast, use, block, run, exchange; Ctrl-A quick fight **(source; option lists verified)** | letters | - | - | battle_options_caster, battle_options_fighter | described |
| Conflict | Party disposition | Inconspicuous, Average, Aggressive, Thrill Seeker change the encounters **(source; menu verified)** | `c`, 3 | - | - | options_controls | described |
| Opponents | Monster groups | over 250 kinds; groups up to dozens ("+56 more Devil Kings") **(verified: lists)** | - | - | [content.md](content.md) | battle_encounter, battle_square_lake_devils | described |
| Items and equipment | Equipment | class and alignment restrictions; one armour, one hand weapon, one missile weapon **(source)** | equip, remove | - | - | inventory_premade | described |
| Abilities and magic | Spells | 48 cleric and 48 sorcerer spells in 9 levels; spell level every second character level; cost in spell points and gems; some spells must be bought in guilds or found **(source)** | `c`, level, number, Enter | Light 1 SP **(verified)** | - | system_cast_spellbook, system_mage_guild | described |
| World and navigation | Areas | 60 areas of 16x16: 5 towns, 20 outdoor areas in a 5x4 grid that wraps, 16 caverns, 5 castles, 10 dungeons and towers, 4 elemental planes **(verified)** | - | - | [world.md](world.md) | gameplay_outdoors_c2, gameplay_cavern_lit | described |
| World and navigation | Travel services | portals, ferries (5 gold), travel agent, Guardian Pegasus once a year **(verified: offers)** | `y` | - | - | system_poorman_portal, gameplay_pegasus | described |
| World and navigation | Time | day and year on the status line; areas differ by century; the quest needs the 9th century **(verified: Castle Xabran in year 800)** | (how the party travels in time: not seen) | start year 900 | [world.md](world.md) | gameplay_xabran_800 | open |
| World and navigation | Auto-map | needs a Cartographer; Location shows the coordinates and the visited squares **(source; coordinates verified)** | `m` | - | - | system_location | described |
| Goals and gating | Main quest | class quests for the Jurors, Triple Crown, Discs and Talons, Element Orb, King Kalohn, Square Lake **(source: area texts, cluebook)** | - | - | [world.md](world.md) | battle_square_lake_devils | open |
| Goals and gating | Gates by class, sex, alignment, item | doors and people refuse ("Sorcerers ONLY!", "Archers Only", "Lord Slayer will only bestow a quest unto a Crusader") **(source: area texts)** | - | - | - | planned | described |
| Chance | Rolls | statistics at creation, encounter groups, combat order follow chance **(verified: rolls change with timing)** | re-roll | - | - | create_roll | described |
| Failure and recovery | Death | 0 hit points = unconscious, below = dead; temples cure; a dead party loses everything since the last sign-in **(source)** | - | - | - | planned | described |
| Saving and sessions | Inn | sign in at an inn of any town to save the whole roster; the party starts from that town next time **(verified)** | `y` | - | - | save_innkeeper, save_signed_in | described |
| Pacing and difficulty | Fixed fights in town | Middlegate holds fixed fights from 10 cats and rodents to 13 skeletons beside its shops **(verified)** | - | - | - | battle_encounter | described |

## 3. How the systems feed each other
Fights give experience and treasure; gold pays for training (levels, spell levels), equipment, spells, skills
and travel; skills open terrain and auto-map; quests (often class-specific) give large experience rewards
(250,000 for a house's quest, bishops' 50,000-200,000 for Triple Crown winners: area texts) and open later
areas; time travel opens the past, where the final gate is decided **(source: area texts; not played)**.

## Open questions
- How the party travels between centuries in play (an item, a spell, a place) and how long a stay lasts.
- What ends the game; what the Square Lake gate checks.
- Exact experience table, training prices, hit point gains.
