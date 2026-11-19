# Ultima I: The First Age of Darkness (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
Shot ids are the planned ids of the playbook's Shot plan; status `described` until the capture run has taken them.

## 1. Core loop
The hero walks the overworld, enters towns to buy food, weapons, armour, spells and vehicles, and castles to
take a king's quest **(verified)**. Money and experience come from fighting monsters on the overworld and in
dungeons **(verified: fights; source: rewards)**; food runs down with every few moves and must be bought
**(verified)**. Quests raise strength or give gems; game time (moves) unlocks better goods in the shops **(code)**.
The late game leaves the fantasy loop for space combat, a princess rescue and the time machine **(verified)**.

## 2. Systems
| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move | one square per key; terrain and vehicle decide what is passable (water, mountains, woods for aircars) **(verified/ROM text)** | arrows | | playbook Controls | `start_overworld` | described |
| Player verbs | Pass | spend a turn **(verified)** | space | | | | described |
| Player verbs | Attack | melee or ranged with the readied weapon in a direction **(verified)** | a + direction | dagger 30 damage seen | | `battle_overworld`, `boss_hit_mondain` | described |
| Player verbs | Board / X-it | step on a vehicle, B boards, X leaves **(verified board)** | b, x | | | `gameplay_vehicles` | described |
| Player verbs | Cast | the readied spell; most work only in dungeons ("Failed, dungeon spell only!": ROM text) | c | | | `system_spell_cast` | described |
| Player verbs | Drop | pence, weapon or armour **(prompt verified)** | d | | | | described |
| Player verbs | Enter | town, castle, dungeon or landmark on the square **(verified)** | e | | | `gameplay_britian` | described |
| Player verbs | Fire | vehicle guns: cannons (frigate), lasers (aircar) **(ROM text)** | f | | | `system_frigate_fire` | described |
| Player verbs | Get | in Mondain's chamber, the gem **(verified)** | g | 2,196 damage to the player | | `boss_gem_destroyed` | described |
| Player verbs | HyperJump | in space, to the next sector, front view only **(verified)** | h | | | `system_hyperjump` | described |
| Player verbs | Inform and search | where am I; finds secret doors **(verified / ROM text)** | i | | | `gameplay_inform` | described |
| Player verbs | K-limb | ladders in dungeons **(prompt verified)** | k | | | | described |
| Player verbs | Noise | sound on/off **(verified)** | n | | | | described |
| Player verbs | Open | coffins and chests **(prompt verified)** | o | | | `gameplay_chest` | described |
| Player verbs | Quit | save (outdoors only) **(verified)** | q | | | `save_quit` | described |
| Player verbs | Ready | weapon, armour, spell **(verified)** | r | | | | described |
| Player verbs | Steal | from a shop counter; caught = guards **(ROM text)** | s | | | `system_steal` | described |
| Player verbs | Transact | shops (buy/sell), kings (pence or service), pub **(verified)** | t | | | `shop_*`, `dialogue_king_*` | described |
| Player verbs | Unlock | prison cells with the jester's key **(verified)** | u | | | `system_cell_open` | described |
| Player verbs | View | change view (vehicles, space) **(verified in space)** | v | | | `gameplay_space_front` | described |
| Player verbs | Ztats | inventory and statistics **(verified)** | z | | | `inventory_ztats` | described |
| Characters and progression | Creation | 30 points over Strength, Agility, Stamina, Charisma, Wisdom, Intelligence (all start at 10); race and class add bonuses (Human +5 Intelligence, Fighter +10 Strength and Agility) **(verified)** | arrows, letters | | playbook Boot | `gen_points`, `gen_race`, `gen_class` | described |
| Characters and progression | Level | experience / 1000 + 1 **(code)** | | level 8 = 7,000 | | `inventory_ztats_late` | described |
| Characters and progression | Statistics from quests and landmarks | landmark quests: 8 Strength from Lord British **(verified)**; landmarks give statistics ("Thou dost gain 2 Stamina") **(verified)** | e, t | | | `dialogue_quest_done`, `system_landmark_grave` | described |
| Characters and progression | Hit points | bought from kings for pence ("How much?") **(verified prompt)** | t, p | | | `dialogue_king_pence` | described |
| Resources and economy | Coin | copper pence, max 9,999; shown as copper, silver (10) and gold crowns (100) **(verified)** | | | | `inventory_ztats` | described |
| Resources and economy | Food | runs down with moves; 10 food for 5 pence in Britian **(verified)** | t | | | `shop_food` | described |
| Resources and economy | Shops | six kinds per town (transport, armour, weapons, magic, food, pub); each town sells a subset; goods improve with game time (3,000 moves: aircar, shuttle, vacuum and reflect suits) **(verified prices / code)** | t, b/s, letter | Britian prices in playbook | playbook Game structure | `shop_*` | described |
| Resources and economy | Game time | a move counter, saved with the character; gates shop goods **(code)** | | 3,000 | | `shop_transport_space` | described |
| Conflict | Melee and ranged attacks | hit or miss, damage numbers in the message log **(verified)** | a | | | `battle_*` | described |
| Conflict | Monsters' attacks | monsters on adjacent squares attack each turn; some steal (gremlin: food; thief) or reduce statistics (Mondain's mind blaster) **(verified / ROM text)** | | | | `battle_skeleton` | described |
| Conflict | Space combat | first-person front view, fire at enemy craft, shields and fuel **(ROM text)** | f, arrows | shield, fuel 1,000 | | `battle_space` | described |
| Opponents | Overworld monsters | wander the map as pieces and attack when adjacent; land and sea kinds **(verified)** | | 13 named | [content.md](content.md) | `battle_overworld` | described |
| Opponents | Dungeon monsters | 22 kinds by depth **(ROM text)**; quest monsters Gelatinous Cube, Carrion Creeper, Lich, Balron **(code)** | | | | `battle_dungeon_*` | described |
| Opponents | Town guards | attack after theft or violence ("Attacked by guard!": ROM text) | | | | | described |
| Opponents | Mondain | 1,000 hit points; bat form below 500; dies at 0 only if the gem is destroyed **(code, verified)** | a, g | 1,000 / 500 | playbook Game structure | `boss_*` | described |
| Items and equipment | Weapons | 16 from hands to blaster **(ROM text)**; readied one used | r, w | | | `inventory_ztats_late` | described |
| Items and equipment | Armour | skin, leather, chain, plate, vacuum suit, reflect suit **(verified)** | r, a | 45 / 90 / 135 | | `shop_armour` | described |
| Items and equipment | Gems | red, green, blue, white from the four gem kings; all four start the time machine **(verified)** | | | | `cutscene_time_machine` | described |
| Items and equipment | Vehicles | horse, cart, raft, frigate, aircar, shuttle, time machine **(verified prices)** | b, x, f | 36 ... 1,296 | | `gameplay_vehicles` | described |
| Abilities and magic | Spells | 11: Prayer (always), Open, Unlock, Magic Missile, Steal, Ladder Down, Ladder Up, Blink, Create, Destroy, Kill; bought singly in magic shops **(ROM text / verified prices)** | r, s, c | 5, 15, 25 | | `shop_magic`, `system_spell_cast` | described |
| World and navigation | Overworld | 168x156 squares, four continents (quarters), 84 places **(verified data)** | | | playbook Game structure | `gameplay_continents` | described |
| World and navigation | Towns and castles | one-screen maps; shops behind counters; castles with king, prison, jester **(verified)** | | | | `gameplay_britian`, `gameplay_castle` | described |
| World and navigation | Dungeons | first-person, levels, ladders, chests, coffins **(verified level 1)** | | | | `gameplay_dungeon` | described |
| World and navigation | Space | 49 sectors, sector scan, hyperjump, starbases, landing only by shuttle **(verified / ROM text)** | | | | `map_sector_scan` | described |
| Goals and gating | King quests | odd castles: find a landmark (strength); even: kill a monster (gem) **(verified / code)** | t, s | | playbook table | `dialogue_king_quest` | described |
| Goals and gating | Space Ace | 20 enemy vessels destroyed **(code, ROM text)** | | 20 | | `system_space_ace` | described |
| Goals and gating | Princess | key from the jester, open the right cell, lead her out; with Space Ace and level 8 she reveals the time machine **(verified)** | a, u, walk | 500 hit points, pence, experience | | `system_princess_reward` | described |
| Goals and gating | Time machine | needs all four gems **(verified)** | b | | | `cutscene_time_machine` | described |
| Goals and gating | Ending | destroy the gem, kill Mondain, ending text **(verified)** | g, a | | | `ending_victorious`, `ending_text` | described |
| Chance | Hits, damage, monster moves, which cell holds the princess, where the time machine appears **(code / verified)** | | | | | | described |
| Failure and recovery | Death | "thou art dead", "Attempting resurrection!" (resurrection at a cost: open) **(verified)** | | | | `gameover_dead` | described |
| Failure and recovery | Starvation, theft | food 0 kills (source: assumed, open); thieves steal **(ROM text)** | | | | | open |
| Saving and sessions | Save | Q outdoors writes the character file; four slots **(verified)** | q | | | `save_quit`, `menu_select` | described |
| Pacing and difficulty | Gates by time and progress | shop goods by move count; time travel by kills and level **(code)** | | 3,000 moves, 20 kills, level 8 | | | described |

## 3. How the systems feed each other
- Fights -> experience and coin -> hit points from kings, equipment, food -> deeper dungeons -> quest monsters ->
  gems **(verified/code)**.
- Landmark quests -> strength -> better hitting **(verified)**.
- Game time -> shuttle in the shop -> space -> 20 kills (Space Ace) **(code)**.
- Space Ace + level 8 + a rescued princess -> time machine; four gems -> the time machine works -> Mondain
  **(verified)**.

## Open questions
- Resurrection cost, starvation, the exact hit and damage formulas.
- Whether every landmark gives the same statistic and amount.
- Shop subsets per town and the weapon eras.
