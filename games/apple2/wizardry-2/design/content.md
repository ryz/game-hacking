# Wizardry II: The Knight of Diamonds - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/wizardry-2`.

Which kinds exist depends on the game, its genre and structure: keep the kinds this game has, drop the rest,
add its own (vehicles, tracks, puzzles, levels, minigames ...). For each kind say how many there are in total
if known, then show a sample that spans the range: early and late, common and rare, plain and strange, one of
each visual family. A complete table belongs in its own document (items.md, enemies.md) and is linked here.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 6 maze floors and the castle **(disk data, verified)** | floors 1 and 6, castle | [maps](maps/floors.txt) |
| Opponents | 78 kinds, pictures numbered 0-29 **(disk data)** | 5 guardians, 4 random groups | `../tools/data.py monsters` |
| Items and equipment | 130 **(disk data)**: Wizardry I's 0-93 range plus new ones up to the five pieces and the staff | 6 quest items, the scout's gear | `../tools/data.py items`, [DOS items](../../../dos/wizardry-2/design/items.md) |
| Abilities / spells | Wizardry I's lists **(source)** | 3 cast | [Wizardry I](../../wizardry/design/content.md) |
| Characters and people | the party of six, four characters found on the disk, Gnilda, the sphinx, Queen Margda | all named below | - |

## 2. Environments
One row per distinct look or place type (tile or wall set, terrain, interior, special place), not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Castle of Llylgamyn (written LLYLGAMN) | town menus | text screens **(verified)** | `start` |
| Wireframe corridors | all floors | purple and white lines, doors as inner frames **(verified)** | `maze1`, `sphinx` |
| Dark squares | floors 1, 2, 5, 6 **(disk data)** | no view | not seen |
| Rock, pits, chutes, spinners, teleports | floors 3-6 **(disk data)** | special squares | not seen |
| Gnilda's temple | floor 1 (9,10) | message pages and the test **(verified)** | `gnilda_test` |

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Magic Armor (boss) | floor 1 (15,2) | animated object | 305 hit points, AC -10; three spells did nothing **(verified)** | `guard1` |
| Magic Shield (boss) | floor 2 (2,6) | animated object, first unnamed | AC -10 **(disk data)** | `guard2` |
| Magic Sword (boss) | floor 3 (14,13) | animated object | fell in one round **(verified)** | `guard3`, `guard3_won` |
| Magic Helmet (boss) | floor 4 (10,4) | animated object | left four of six dead in a round **(verified)** | `guard4` |
| Magic Gauntlets (boss, two) | floor 5 (10,9) | animated object | the same **(verified)** | `guard5` |
| Lesser demons with a level 8 ninja | floor 1 | demonic figure | group of five and one **(verified)** | `battle` |
| Trolls, ogres, weretigers, were amoebae, major daimyos, priests, swarms, giant bats, will o' wisps, vampire | floors 1-5 | several pictures | met on warp arrivals **(verified, names as shown)** | scout sheets only |
| A little old man (monster 0, Dink, in the table) | floor 1 | little old man | met once, unidentified **(verified)** | scout sheet only |

## 4. Items and equipment
A spread over types and tiers; the special ones (quest items, cursed, charged) marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| KOD's armor, shield, helmet, gauntlets, Hrathnir | quest armor and sword | the five guardians, unidentified **(verified)** | worn together: AC "LO", regeneration **(verified)** | `guard1_won`-`guard5_won`, `gnilda_test` |
| Staff of Gnilda | quest item | Gnilda **(verified)** | ends the quest at the castle | `staff` |
| Long sword, plate mail, shield + 1, helm and the rest of the scout's gear | weapons and armor | Boltac's prices **(disk data)**, given by poke | AC 0 to 9 **(verified)** | `gcamp` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Tiltowait, Lahalito | mage, bishop | a level 7 / level 4 mage spell point | damage to a group **(verified cast; the Magic Sword died that round)** | `guard3_won` |
| Malikto | priest | a level 7 priest point | damage to all monsters **(source for the effect)** | `guard3_won` |

## 6. Characters and people
Playable classes or characters, and the people of the world (shopkeepers, quest givers, rulers).

| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ, CONDI, EBO, CUBI, DEDDO, MNZ | the party: two fighters, priest, thief, mage, bishop, level 13 | from Wizardry I **(verified)** | `start` |
| THUG, HALIG, KELRACH, FURY | characters of an earlier player on this copy's disk (levels 28-38, holding four of the pieces) **(disk data, verified in the roster)** | Training Grounds roster | route in playbook |
| Gnilda's apparition, the fiery face | quest giver | floor 1 (9,10) **(verified)** | `gnilda_test`, `staff_gift` |
| The sphinx | riddle | floor 6 (1,2) **(verified first page)** | `sphinx` |
| Queen Margda | ruler, speaks the ending **(verified)** | ending | `ending` |

## Open questions
Floors 2-6 as views, most monsters and items, the shops: reach with `WARP` and the DOS survey's squares.
