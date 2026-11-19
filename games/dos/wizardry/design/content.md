# Wizardry: Proving Grounds of the Mad Overlord (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Which kinds exist depends on the game, its genre and structure: keep the kinds this game has, drop the rest,
add its own (vehicles, tracks, puzzles, levels, minigames ...). For each kind say how many there are in total
if known, then show a sample that spans the range: early and late, common and rare, plain and strange, one of
each visual family. A complete table belongs in its own document (items.md, enemies.md) and is linked here.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | castle menus, 10 maze floors (dark areas, rock, anti-magic) | 5 | [maps](maps/floors.txt) |
| Opponents | about 100 monster kinds (source) | 4 | not decoded (encoded text on the disk) |
| Items | about 100 (item 94 = Werdna's amulet, verified) | 7 | not decoded |
| Abilities / spells | 21 mage + 29 priest (source; the spell-known bits verified) | 4 | §5 |
| Characters and people | 8 classes, 5 races; Boltac, Gilgamesh, Werdna, Trebor | §6 | - |

## 2. Environments
One row per distinct look or place type (tile or wall set, terrain, interior, special place), not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Castle and town menus | above ground | framed menus, no pictures | `menu_castle`, `menu_edge` |
| Lit corridor | floor 1 onward | white wireframe walls and doors | `gameplay_maze_f1_start` |
| Darkness | floor 1 (9-10, 0-19) and others | hatched view | `gameplay_dark` |
| Rock | floor 10 around the paths, floor 8 east | instant death | `gameover_rock` |
| Werdna's lair | floor 10 (17-19, 1-4) | sign and door, fixed fight | `dialogue_werdna_sign`, `boss_werdna` |

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Slime / Bubbly slime | floor 1 rooms | cyan blob | weak, comes in fours | `battle_options` |
| Vampire | floor 10, with Werdna | ghost-like picture | drains levels | `boss_werdna` |
| Vampire Lord | floor 10, with Werdna | same family | drains 4 levels in one hit (verified), casts sleep (inferred: party fell asleep) | `boss_werdna` |
| Werdna ("Man in robes" before identified) | floor 10 (17,3) | robed wizard with a staff | boss; a round of his killed four members (verified) | `boss_werdna` |

## 4. Items and equipment
A spread over types and tiers; the special ones (quest items, cursed, charged) marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Long sword (25), short sword (15), dagger (5), staff (10) | weapons | Boltac's | - | `shop_boltac_buy` |
| Anointed mace (30), anointed flail (150) | priest weapons | Boltac's | - | `shop_boltac_buy` |
| Chest | container | after fights | trapped loot | `battle_chest` |
| Werdna's amulet (item 94) | quest item | Werdna | ends the game when brought to the castle | `ending_congratulations` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| HALITO | mage, level 1 | 1 point of level 1 | fire at one group (source); cast on the Slimes (verified) | (planned `battle_messages`) |
| DUMAPIC | mage, level 1 | 1 point | tells the position (verified) | `system_dumapic` |
| TILTOWAIT | mage, level 7 | 1 point of level 7 | hits every group (verified: cleared Werdna's escort over two rounds) | (planned `boss_werdna_fight`) |
| CALFO | priest, level 2 | 1 point | names a chest's trap (source) | `battle_chest` |

## 6. Characters and people
Playable classes or characters, and the people of the world (shopkeepers, quest givers, rulers).

| Who | Role | Where | Shots |
|---|---|---|---|
| Fighter, Priest, Thief, Mage, Bishop (the party: ryz, condi, ebo, cubi, deddo, mnz) | playable classes | Training Grounds | `inventory_roster` |
| Samurai, Lord, Ninja | elite classes, high statistics | Training Grounds | (planned `create_class`) |
| Pre-made characters Tarkin, Shreev, Curtis, Kimbal, Tivis, Mewo | ready-made level 1 party on the scenario disk | Tavern | `inventory_roster` |
| Gilgamesh, Boltac | tavern keeper, merchant (names only) | Castle | `menu_tavern`, `shop_boltac` |
| Werdna | the evil wizard | floor 10 | `boss_werdna` |
| Trebor, the Mad Overlord | quest giver (in the ending text) | castle | `ending_congratulations` |

## Open questions
What exists but was not seen, and how it could be reached.
- Monster and item names are stored encoded on the disk; decode them (the text appears in memory when shown)
  for full tables.
- Murphy's ghost (floor 1 (13,5)), the floor 4 monster allocation centre and the floor 7 fixed fight: reach
  them with WARP next to the square (maps.py).
