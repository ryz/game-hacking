# Wizardry II: The Knight of Diamonds - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/wizardry-2`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
Form the party in the Tavern, rest at the Inn, equip in the camp, go down, fight groups of monsters for
experience and chests, beat a floor's guardian for its piece of armor and the way down, come back up, rest and
identify, go deeper **(verified: `start`, `rested`, `gcamp`, `battle`, `chest`, `guard1`-`guard5`; the order of
the loop is the DOS port's, source)**. Between loops the party gains pieces of the armor rather than levels: the
characters arrive at level 13 and the scout's party gained none **(verified)**.

## 2. Systems
Go through every group; write "none" where the game has nothing, do not drop the group.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Castle, Tavern, Inn, Edge of Town | one letter per place; members join by typed name, leave by number; the stables are free and restore spell points | `A G B C E`; `A` + name, `R` + number; room letter | stables free, cots 10, economy 50, merchant 200, royal 500 gold a week | [Wizardry I systems](../../wizardry/design/systems.md) | `start`, `rested`, `edge` | described (seen as text, no shot yet) |
| Player verbs | Walk, turn, kick, camp | forward, left, right; doors are kicked; the camp inspects, reorders, equips, disbands | `F L R K C` | - | [maps](maps/floors.txt) | `maze1`, `camp`, `gcamp` | described |
| Player verbs | Transfer characters | the boot menu's Utilities move one living character at a time from another scenario disk; the source loses the character | `U`, `T`, Return, disk changes, slot letter, password | 20 roster places | playbook, Boot sequence | `start` | described |
| Characters and progression | No creation | "YOU CANNOT CREATE CHARACTERS IN LLYLGAMN BECAUSE THEY WOULD NOT SURVIVE": characters come at about level 13 from the first scenario **(verified)** | - | 13th level "or so" | - | route in playbook | described |
| Characters and progression | What the move keeps | level, hit points, experience, gold, age, scores, spells, the chevron; spell points as spent **(verified)** | - | - | playbook | `start` | described |
| Characters and progression | Marks of rank | `>` chevron from Wizardry I, `G` for the bearer of the staff, `K` for a knight, shown after the name **(verified)** | - | bearer +300,000 experience | §Goals | `knights`, `final` | described |
| Resources and economy | Gold | carried per member; the Wizardry I ending left 4,817 to 9,342 each; Boltac's prices are Wizardry I's **(disk data)** | - | long sword 25, plate mail 750, shield + 1 1,500 | [DOS items](../../../dos/wizardry-2/design/items.md) | `gcastle` | described |
| Conflict | Rounds | orders for all six, then the round; fight asks for a group when there are several; a surprised side loses its first round **(verified)** | `F S P R U`, Return, `B` | - | [DOS systems](../../../dos/wizardry-2/design/systems.md) | `battle`, `guard3_won` | described |
| Opponents | Random groups | rooms hold groups of up to four kinds, names unknown until identified ("MEN IN ARMOR") **(verified)** | - | 78 monster kinds **(disk data)** | content §3 | `battle` | described |
| Opponents | Guardians | one animated piece of armor on the square before each stairs down; it is not there while its piece is owned by anyone in the roster **(verified, also piece by piece)** | - | armor 305 hit points, AC -10; shield AC -10; gauntlets come as two | [findings](findings.md) | `guard1`-`guard5` | described |
| Items and equipment | The five pieces and the staff | Hrathnir, KOD's helmet, shield, gauntlets, armor drop unidentified; worn together: armor class "LO", hit points regenerate (`112+`) **(verified)** | equip in camp | items 125-129, staff 124 | [DOS items](../../../dos/wizardry-2/design/items.md) | `guard1_won`-`guard5_won`, `gnilda_test` | described |
| Abilities and magic | Spells | Wizardry I's mage and priest lists, typed by name; Tiltowait, Malikto, Lahalito cast here **(verified)** | `S` + name | 7 levels each | [Wizardry I](../../wizardry/design/systems.md) | `guard3_won` | described |
| World and navigation | Six floors | 20 by 20 squares each, stairs, pits, chutes, teleports, darkness, rock, spinners, message squares **(disk data)** | - | 6 floors | [maps](maps/floors.txt) | `maze1`, `sphinx` | described |
| Goals and gating | The quest | five guardians, five pieces on one character, the sphinx's riddle, Gnilda's test for one alone, the staff, the stairs home **(verified)** | answer typed | answer "THE KNIGHT OF DIAMONDS" | playbook, Game structure | `sphinx`, `sphinx_answer`, `sphinx_right`, `one_alone`, `temple_door`, `gnilda_test`, `gnilda_answer`, `staff_gift`, `staff`, `ending` | described |
| Goals and gating | Awards | the bearer may make five roster characters knights **(verified)** | `Y N` | 5 knighthoods | - | `knights` | described |
| Chance | Encounters and rounds | which group waits in a room is decided when the floor is loaded; hits, damage and spell results are rolled **(inferred from routes)** | - | - | playbook, Emulation notes | - | described |
| Failure and recovery | Death | members die in fights (four of six in one round against the helmet or the gauntlets) **(verified)**; temple and cemetery as Wizardry I **(source)** | - | - | [Wizardry I](../../wizardry/design/systems.md) | route in playbook | described |
| Saving and sessions | Roster on disk | written when characters are moved, deleted, added, and on leaving the game **(verified)** | `L` at the Edge of Town | 20 places | - | saves 01, 02 | described |
| Pacing and difficulty | Start at the top | the first floor already fields level 7-8 casters and groups of five and six **(verified)** | - | - | - | `battle` | described |

## 3. How the systems feed each other
- Guardian beaten -> its piece -> stronger bearer (armor class, regeneration) -> next guardian **(verified for
  the drops; the bearer's gain seen with all five)**.
- All five worn by one character -> Gnilda's test -> the staff, and the five are taken back **(verified)**.
- The roster is the gate: a piece owned by any roster character keeps its guardian away **(verified)**.

## Open questions
- Everything in the playbook's Open questions; levels and treasure were not played.
