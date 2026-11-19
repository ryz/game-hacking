# Wizardry III: Legacy of Llylgamyn (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry-3`.

Which kinds exist depends on the game, its genre and structure: keep the kinds this game has, drop the rest,
add its own (vehicles, tracks, puzzles, levels, minigames ...). For each kind say how many there are in total
if known, then show a sample that spans the range: early and late, common and rare, plain and strange, one of
each visual family. A complete table belongs in its own document (items.md, enemies.md) and is linked here.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 6 floors + the Castle (disk data) | wireframe corridors, dark areas, the lake, the Grand Wizard's house, the summit | [maps/floors.txt](maps/floors.txt) |
| Opponents | 78 monster records (disk data) | the two guardians and random groups seen | - |
| Items | 103 (verified) | quest items, magic items | [items.md](items.md) |
| Equipment | weapons and armour in -1/+0/+1/+2 tiers and named blades (verified names) | Boltac's stock | [items.md](items.md) |
| Abilities / spells | Wizardry I's lists (inferred) | - | Wizardry I design |
| Characters and people | 6 stock characters + imports; NPCs by message: L'kbreth, Abdul, the monk, the whip woman, the Queen | - | [messages.md](messages.md) |

## 2. Environments
One row per distinct look or place type (tile or wall set, terrain, interior, special place), not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Floor 1 lake and beach | floor 1 (1-7, 0-7) | water's edge drowning warning, an island (verified text) | planned |
| The Grand Wizard's house | floor 2 | dining room, wine cellar, desk, "the wizard is *out*" (verified text) | planned |
| Graveyard and monk | floor 3 | warnings, the monk's chest, the murky pool (verified text) | planned |
| Dark floors | floors 4-6 | grey view (verified on floor 5) | planned |
| The summit | floor 6 | statues, L'kbreth's lair, riddles (verified) | planned |

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Giant Serpents | floor 1 | snake | attack first (verified) | `battle_f1_serpents` |
| Unseen Entities | floors 1, 4, 6 | ghost / skull | (verified) | planned |
| Men in Robes, Burglars | floor 6 | priest, fighter | (verified) | planned |
| Gnome Priests, Men in Leather, Dwarf Fighters | floor 6 | people | (verified) | planned |
| Living Legend (Delf) + Gaunt Figures, Delf's Minions | floor 4 guardian | bearded sage, skeletons | kills a level-1 fighter in one blow; drops the Crystal of Evil (verified) | `boss_guardian_good` |
| Soul Trappers (Hungry Monsters), Crusader Lords, Fighters | floor 5 guardian | spider, knights | drop the Crystal of Good (verified) | `boss_guardian_evil` |
| Xeno | floor 6 (4,4) search | - | (verified) | planned |

## 4. Items and equipment
A spread over types and tiers; the special ones (quest items, cursed, charged) marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Orb of Earithin | quest | statue search with the Neutral Crystal | ends the game in the Castle (verified) | planned |
| Crystal of Evil / Good | quest | the guardians of floors 4 / 5 | open floor 6 (verified) | planned |
| Staff of Earth | quest | floor 2 desk | not known | planned |
| Orb of Mhuuzfes | cursed | statue search (13,2) | AC -10, cursed (disk data) | planned |
| Broadsword | weapon | Boltac's, 50 | 1-8 damage (disk data) | `shop_boltac` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|

## 6. Characters and people
Playable classes or characters, and the people of the world (shopkeepers, quest givers, rulers).

| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ CONDI EBO CUBI DEDDO MNZ | our party, descendants of the Wizardry I/II heroes | Castle | `menu_castle_start` |
| KLINDT LEIF ZETT VERPA SENA GITTER | stock legacy characters | roster | `menu_roster` |
| L'kbreth | the dragon who took the orb | floor 1 warning, floor 6 farewell | planned |
| Abdul | merchant: password, taxi, crystal | floors 4, 3, 5 | planned |
| Queen Beyki | gives the stars | ending | planned |

## Open questions
What exists but was not seen, and how it could be reached.
