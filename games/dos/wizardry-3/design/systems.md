# Wizardry III: Legacy of Llylgamyn (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry-3`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
As in Wizardry I and II: form a party in the Castle, climb into the maze, fight, map, come back to rest and shop
(verified: same menus). Wizardry III starts from the heroes of the earlier games reborn at level 1 without goods, so
the early loop is the classic one again (verified: `start`). The fork after floor 1 makes the player keep two parties
and alternate between the good half (floors 2 and 4) and the evil half (3 and 5); each half ends in a guardian whose
crystal opens the summit (verified: `guard_good`, `guard_evil`, `floor6`). No shots yet (set `main` not captured):
"Shots" below names the planned ids of the playbook's Shot plan.

## 2. Systems
Go through every group; write "none" where the game has nothing, do not drop the group.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Walk, turn, kick | W steps, A/D turn, K goes through a door; walls belong to the square you leave, so some doors are one-way (verified) | W A D K | 1 square per step | [maps](maps/floors.txt) | `gameplay_maze_f1_start`, `gameplay_wall`, `gameplay_door` | described |
| Player verbs | Search a square | "Will you search (Y/N)?" squares give, swap or guard an item, or start a fight (verified: desk, statue, Xeno) | Y/N | - | [messages](messages.md) | `dialogue_search` | described |
| Player verbs | Answer riddles | typed answer; right = stay, wrong = pushed back (verified: WHEEL) | text + Enter | 5 riddles, 1 password | [messages](messages.md) | `dialogue_riddle_*` | described |
| Player verbs | Pay a merchant | Abdul's taxi (2500 / 5000 gold) and crystal (25000) ask for gold (disk data, not tried) | - | prices | [messages](messages.md) | `dialogue_abdul_*` | open |
| Characters and progression | No creation; the legacy | characters come from Wizardry I/II through Utilities M)ove characters, then Training L)egate: name, race, class, honors kept, letter "D" added; level 1, 8 HP, age 20, 500 gold, no items, statistics rolled again near the old values, only level-1 spells; alignment chosen within the class rules; once only (verified) | M, letters, L, A/B/C | see playbook | playbook "What the legacy keeps" | `seq-legacy` (planned) | described |
| Characters and progression | Stock characters | six level-1 legacy characters on the disk (KLINDT LEIF ZETT VERPA SENA GITTER) (verified) | Tavern | - | playbook | `menu_roster` | described |
| Characters and progression | Classes, levels, ageing, spells | as Wizardry I (inferred: same records and screens) | - | - | Wizardry I design | - | described |
| Resources and economy | Gold, shop | Boltac's stock starts at the short sword (30) and runs to plate armour (verified first pages); Pool gold in the sheet (verified on screen) | B, P | prices in [items](items.md) | items.md | `shop_boltac` | described |
| Conflict | Combat | as Wizardry II: orders per member, groups, surprise rounds (verified: F/P/S options, "Press Enter to fight, or T)ake back orders") | F P S D U R T | - | Wizardry I design | `battle_*` | described |
| Conflict | Alignment barriers | floors 2/4: no evil member; 3/5: no good member; "You are forbidden to enter here! Begone!!" and back to the Castle (verified) | - | - | playbook "Game structure" | `gameplay_forbidden` | described |
| Opponents | Guardians | floor 4 (7,17): Living Legend (Delf unidentified) with Gaunt Figures, Delf's Minions; floor 5 (12,10): Soul Trappers (Hungry Monsters), Crusader Lords, Fighters; group sizes vary (verified) | - | - | [content](content.md) | `boss_guardian_*` | described |
| Items and equipment | Item list | 103 items (verified on the sheet) | - | 1001-1103 | [items](items.md) | `inventory_*` | described |
| Abilities and magic | Spells | Wizardry I's lists (inferred); casters arrive with level-1 spells only (verified) | S | - | Wizardry I design | `inventory_spellbook` | described |
| World and navigation | The volcano | six 20 x 20 floors climbed upward; fork 1 -> 2 -> 4 -> 6 and 1 -> 3 -> 5 -> 6; dark squares, pits, chutes, teleports, anti-magic, lake (disk data, warps verified) | - | 6 floors | [maps](maps/floors.txt) | `gameplay_f*` | described |
| Goals and gating | Two parties | the Tavern refuses good and evil together ("* Bad alignment *"), neutrals join both (verified) | Tavern | - | playbook | `menu_tavern_bad_alignment` | described |
| Goals and gating | Summit and orb | floor 6 needs a crystal (and a party not all neutral); Neutral Crystal + statue search square = Orb of Earithin; the orb in the Castle = the ending (verified) | - | - | playbook "The quest" | `seq-orb` (planned) | described |
| Goals and gating | Neutral Crystal | how it is made: not found (tried: statues, L'kbreth, every crystal combination) | - | - | playbook Open questions | - | open |
| Goals and gating | Ending | surrender the orb, the Queen gives the party the Star of Llylgamyn and the player awards six more stars ("*", +150,000 E.P. each) (verified) | Y, Enter, Y/N | 6 stars | playbook | `ending_*` | described |
| Chance | Encounters, drops | random fights and group sizes follow timing; the guardian drops were the same item every time (verified) | - | - | - | - | described |
| Failure and recovery | Death, temple | as Wizardry I (inferred); a level-1 party dies to the first guardian round (verified) | - | - | Wizardry I design | `gameover_party_dead` | described |
| Saving and sessions | Disk roster | the scenario disk holds the roster and is written as the game goes (verified); Leave game ends the program | L | 20 slots | playbook | - | described |
| Pacing and difficulty | Restart at level 1 | the heroes start over at level 1 with guardians that kill a level-1 party in one round (verified) | - | - | - | - | described |

## 3. How the systems feed each other
- Earlier games -> legacy -> a level-1 party with honors (verified).
- Fights -> experience and gold -> levels and gear -> the guardians (inferred, as Wizardry I).
- Alignment -> which half a party may enter -> which guardian -> which crystal; any crystal -> the summit (verified).
- Neutral Crystal -> statue search -> Orb -> Castle -> stars for six more characters (verified).

## Open questions
- Where the Neutral Crystal comes from (playbook Open questions); what the Staff of Earth, Amulet of Air, Holy
  Water, Rod of Fire, Ship in Bottle and Gold Medallion do.
