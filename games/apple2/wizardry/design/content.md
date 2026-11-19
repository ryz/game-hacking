# Wizardry: Proving Grounds of the Mad Overlord - content (variety lens)

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
| Environments | the castle (text), ten maze floors of 20 x 20 **(disk data)** | planned: one view per floor, each special square type | [maps/floors.txt](maps/floors.txt) |
| Opponents | 101 monster records, 20 pictures **(disk data)** | planned: one per picture, early to late | `python3 ../tools/data.py monsters`; DOS [content](../../../dos/wizardry/design/content.md) |
| Items and equipment | 101 item records **(disk data)**; the same numbers as the DOS port, names worded differently (LONG SWORD + 2, BLADE CUSINART', MURASAMA BLADE) | planned: stock pages, sheets | `python3 ../tools/data.py items`; DOS [items](../../../dos/wizardry/design/items.md) |
| Abilities / spells | 21 mage and 29 priest spells in 7 levels **(verified: mage book; priest count from the DOS documents)** | planned: both books, six casts | DOS content |
| Characters and people | 5 races, 3 alignments, 8 classes; Trebor (the ruler, named in the ending), Werdna, Boltac, Gilgamesh, the Temple of Cant **(verified: screen texts)** | planned | - |

## 2. Environments
One row per distinct look or place type (tile or wall set, terrain, interior, special place), not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Castle | all menus | framed text header naming the place **(verified)** | `start` |
| Corridor and room wireframe | every floor | purple outlines, side openings, doors as inner frames **(verified)** | `maze1`, `gmaze` + `WARP` |
| Darkness | floor 1 band x 9-10 and others | the view stays empty **(verified)** | `@maze1,poke:7330=0900,poke:732E=0500,poke:732A=0000,a,w100,d,w100` |
| Elevators | floor 1 (10,8): A-D; floor 4 (10,0): A-F | button prompt **(verified)** | `@gmaze,WARP:04:0A:00` |
| Werdna's lair | floor 10 (17,4)/(17,3) | the sign and the fight **(verified)** | `werdna_sign`, `werdna` |

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Bubbly slime ("SLIME") | floor 1 (7,1) | green blob | 2, 3 and 3 hit points in the recorded fight **(RAM)**; three died in one round **(verified)** | `battle` |
| Orcs, Kobolds ("SMALL HUMANOID"), Rogues ("SCRUFFY MEN"), Undead kobolds ("SKELETONS") | floor 1 (7,1), other timings | humanoid with shield; blue-capped man; skeleton | seen as encounter starts only **(verified)** | playbook, DOS-route table |
| Vampire ("UNSEEN ENTITY") | Werdna's room | no picture of its own in the fight seen | a hit drained 4 levels **(verified)** | `werdna` variants |
| Vampire Lord | Werdna's room | - | 89 hit points in the recorded fight **(RAM)** | `gwerdna` |
| W E R D N A ("MAN IN ROBES") | floor 10 (17,3) | wizard in green, arms raised | 87 hit points **(RAM)**; his first spell killed four level 13 members **(verified)**; can be met friendly **(verified)** | `werdna` |

## 4. Items and equipment
A spread over types and tiers; the special ones (quest items, cursed, charged) marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Long sword, short sword, anointed mace, anointed flail, staff, dagger | weapons | trading post, first page: 25, 15, 30, 150, 10, 5 gold **(verified)** | - | `@vet,b,w300,1,w400,b,w500` |
| Long sword + 2, plate mail + 2, shield + 2, helm + 1 | fighter gear | poked for the veterans | armour class 10 -> -4 when equipped **(verified)** | `gcamp` |
| Dios potion | special | poked | listed in the pack **(verified)** | `gcamp` |
| Werdna's amulet | quest item (number 94) | Werdna's fight | appears unidentified in the finder's pack; ends the game at the castle **(verified)** | `werdna_won` |
| Blue ribbon, keys, statuettes | quest items 95-100 | maze events **(disk data)** | - | - |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| HALITO | mage level 1 | one level 1 point | killed a slime **(verified)** | `chest` route |
| TILTOWAIT | mage level 7 | one level 7 point | with Malikto and Lahalito ended Werdna's fight in one round **(verified)** | `werdna_won` route |
| MALIKTO | priest level 7 | - | damage to all groups **(verified in the same round; split of the damage not read)** | same |
| LAHALITO | mage level 4 | - | one group **(verified: asks for the group)** | same |
| DUMAPIC | mage level 1, camp | - | facing, squares east and north of the castle stairs, levels below **(verified)** | `@vmaze,c,w400,5,w400,s,w300,type:DUMAPIC\n,w400` |
| MALOR | mage level 7, camp | - | teleport by displacement **(verified)** | `malor_home` |

## 6. Characters and people
Playable classes or characters, and the people of the world (shopkeepers, quest givers, rulers).

| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ, CONDI, EBO, CUBI, DEDDO, MNZ | the party: two fighters, priest, thief, mage, bishop **(verified)** | everywhere | `start` |
| The inherited roster | 20 characters of an earlier player, levels 9-50, with samurai, lord and ninja **(verified)** | `castle` + Training Grounds roster | `@castle,TRAINING,type:*ROSTER\n,w400` |
| Trebor | "your benificent ruler" **(verified: ending text)** | ending | `ending` |
| Werdna | the evil wizard **(verified)** | floor 10 | `werdna` |

## Open questions
What exists but was not seen, and how it could be reached.
- All monsters past floor 1 except Werdna's company: `@gmaze,WARP` to a fight-room square of each floor and `wK` variants (playbook).
- The trading post's later stock pages, the Temple's services, the chest traps.
- The monster table's fields beyond the names are a reading of the record that was not checked in play.

