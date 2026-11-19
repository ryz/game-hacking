# Wizardry II: The Knight of Diamonds (DOS) - content (variety lens)

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
| Environments | 6 floors of 20 x 20 plus the Castle menus (verified: disk data) | wireframe corridors, dark areas, rock, the temple | [maps](maps/floors.txt) |
| Opponents | groups from a per-floor table; 5 guardians (verified) | Kobold Kings, Magic Armor ... | not decoded (names are packed on the disk) |
| Items | 129 (verified) | sample below | [items.md](items.md) |
| Equipment | weapons, armour, shields, helms, gauntlets in the same list | sample below | [items.md](items.md) |
| Abilities / spells | Wizardry I's mage and priest lists (inferred) | DUMAPIC, Mahalito (enemy), Katino (enemy) | [Wizardry I](../../wizardry/design/content.md) |
| Characters and people | 6 stock veterans, the imported party, the sphinx, Gnilda's apparition, the Castle (verified) | below | - |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| The Castle "Llylgamyn" | town | menus only | `menu_castle` |
| Floor 1 | under the temple | 98 dark squares, Gnilda's temple at (9,10), teleports (verified: maps) | `gameplay_maze_f1_start` |
| Floor 4 / 6 | deep | large areas of rock (177 / many squares) between corridors (verified: maps) | planned `gameplay_f4`, `gameplay_f6` |
| Floor 5 | deep | chutes down to floor 6 (verified: maps) | planned `system_chute` |
| Gnilda's temple | floor 1 (9,10) | the apparition, the test | `dialogue_gnilda_test` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Kobold King | floor 1 (verified) | kobold, armed | groups of 4-5 | `battle_f1_kobold_kings` |
| Magic Armor (guardian) | floor 1 (15,2) | animated armour | hits for 5, hard to hit, drops KOD's armor (verified) | `boss_magic_armor` |
| Magic Shield / Sword / Helm / Gauntlets | floors 2-5 (verified) | animated pieces | guard the stairs | `boss_magic_shield`, `boss_magic_sword`, `boss_magic_helm`, `boss_magic_gauntlets` |
| Lvl 7 Mages, Lvl 7 Priests (friendly), Warriors, Ogres, Men in Leather/Armor, Major Daimyos (friendly) | floor 1 (verified) | humans, giants | Mahalito, Katino | planned |
| Corrosive Slimes + No-See-Um Swarm, Strange Animal + Master Ninjas, Skulls + Doomtoads, Hatamotos + Lvl 10 Mages, Priests + Orc Lords | floors 3-6 (verified: seen once each on arrival) | mixed groups | - | planned `battle_f2`... |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Long sword, plate mail ... | basic weapons and armour | Boltac's (inferred) | - | planned `shop_boltac_buy` |
| Hrathnir, KOD's helm, shield, gauntlets, armor | the regalia | the guardians (verified: armor) | worn: regeneration "+", AC "LO" | planned `inventory_kod_set` |
| Staff of Gnilda | quest item | Gnilda, for the five | ends the game; U)se: "* Powerless *" (verified) | `dialogue_staff_gift`, planned `inventory_staff` |
| Damien stone, Stone of youth, Mind stone, Blarney stone ... | stones (new) | not seen | probably invoked ("Will you invoke the special power of your ...": disk text) | - |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Mage and priest spells | DEDDO, EBO, MNZ (imported with their points) | spell points per level | as Wizardry I | planned `inventory_sheet_deddo` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ CONDI EBO CUBI DEDDO MNZ | the party, from Wizardry I | roster C-F, K, L | `menu_castle` |
| CALEB, BOREE, ODDLER, NAUTUS, ZIL, GUYDOMAN | ready veterans (L12-13) | roster | planned `menu_tavern_stock` |
| The sphinx | riddle keeper | floor 6 (1,2) | `dialogue_sphinx` |
| Gnilda's apparition | quest giver | floor 1 (9,10) | `dialogue_gnilda_test`, `dialogue_staff_gift` |

## Open questions
- Monster names are packed on the disk; only those met are known. Boltac's stock not surveyed.
- What the stones do (Damien, youth, mind, piety, Blarney, granite, dreamer's).
