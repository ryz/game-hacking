# Wizardry II: The Knight of Diamonds (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
As in Wizardry I: form a party in the Castle, descend, fight, map the floors on paper, come back to rest and
shop (verified: same menus). Wizardry II starts where Wizardry I ended: the party arrives as veterans of levels
11-13 without equipment (the import keeps everything but the items), so the first loop is shopping at Boltac's
with the gold carried over (inferred). Then each floor ends at a guardian before the stairs down that drops a
piece of the regalia (verified: floor 1); the run ends with one character alone carrying the Staff of Gnilda
to the Castle (verified: `ending_congratulations`).

## 2. Systems
Rules shared with Wizardry I are listed once with a link; the Wizardry I reference has their details.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Walk, turn, kick, camp, status, inspect, off | as Wizardry I: W A D, K through doors, C camp, S/O views, I search for bodies (verified: command line and moves) | W A D K C S I O | 1 square per step | [Wizardry I systems](../../wizardry/design/systems.md) | `gameplay_maze_f1_start` (planned: door, camp, views) | shown |
| Player verbs | Answer a riddle | some squares ask for a typed answer; a wrong one sends the party back a square (verified: the sphinx) | text + Enter | sphinx: "the knight of diamonds" | playbook, Game structure | `dialogue_sphinx`, `dialogue_gnilda_test` | shown |
| Characters and progression | Import (Move characters) | Utilities M)ove reads a Wizardry I scenario disk, the player marks characters by letter, Enter moves them; they keep level, HP, E.P., gold, age, statistics, spells and the chevron, lose all items; on the source disk they become lost (verified) | letters, Enter, Esc | up to the free slots (20 in the roster) | playbook, Game structure | planned `system_move_list`, `system_move_marked`, `system_move_moved` | shown |
| Characters and progression | No creation | the Training Grounds only inspect and list characters; six ready veterans (levels 12-13) come on the disk (verified) | I, R | 6 stock characters | - | planned `menu_training`, `menu_tavern_stock` | shown |
| Characters and progression | Levels, classes, ageing, statistics | as Wizardry I (inferred: same engine and record) | Inn | - | [Wizardry I](../../wizardry/design/systems.md) | planned `menu_inn_rooms` | described |
| Characters and progression | Awards | marks after the name: ">" Wizardry I's Chevron of Rank kept, "G" Mark of Gnilda for the staff's bearer, "K" Knight of the City for companions chosen at the ending (verified) | Y/N per character | bearer +300,000 E.P., knights none | playbook | `ending_congratulations`, planned `ending_sheet_ryz`, `ending_sheet_condi` | shown |
| Resources and economy | Gold, Boltac's, Inn, Temple | as Wizardry I; imported characters bring their gold (55,077-74,817 here) (verified: sheets) | menus | prices not surveyed | [Wizardry I](../../wizardry/design/systems.md) | planned `shop_boltac*`, `menu_inn*`, `menu_temple` | described |
| Conflict | Combat | as Wizardry I: orders per member, members 4-6 cannot fight hand to hand, no spells in a surprise first round, group targeting (verified: guardian fights) | F P S D U R T, digits | - | [Wizardry I](../../wizardry/design/systems.md) | `battle_f1_kobold_kings`, the five `boss_*` | shown |
| Conflict | Fight zones | squares marked as rooms always meet a group when the party arrives there (verified: every warp onto one) | - | - | [maps](maps/floors.txt) | `battle_f1_kobold_kings` | shown |
| Opponents | Guardians | a fixed group on the square before each stairs down, floors 1-5: Magic Armor, Magic Shield, Magic Sword, Magic Helm, two Magic Gauntlets; they fight every time the square is entered (verified) | - | Magic Armor hits for 5, dodged unarmed blows | playbook | `boss_magic_armor` ... `boss_magic_gauntlets` | shown |
| Opponents | Random groups | per floor encounter tables; friendly groups can be left (verified: "A friendly group of Lvl 7 Priests. F)ight or L)eave") | F, L | - | - | planned `battle_friendly`, `battle_f2`... | shown |
| Items and equipment | Items | 129 items: Wizardry I's 100-odd and new ones (stones, KOD pieces, the staff) (verified: sheet survey) | camp E)quip, T)rade, U)se, I)dentify | 129 | [items.md](items.md) | planned `camp_equip`, `inventory_kod_set` | shown |
| Items and equipment | The regalia | Hrathnir, KOD's helm, shield, gauntlets, armor: each dropped by its guardian, unidentified ("ARMOR") (verified: floor 1); worn they regenerate hit points ("+") and give a very low armour class shown as "LO" (verified with the pieces poked) | E)quip, T)rade | - | playbook | planned `boss_found_armor`, `inventory_kod_set` | shown |
| Abilities and magic | Spells | as Wizardry I; imported casters keep spells and points (verified: sheets) | S, typed names | - | [Wizardry I](../../wizardry/design/systems.md) | planned `inventory_sheet_deddo`, `battle_spell` | described |
| World and navigation | Six floors | 20 x 20 each, linked by one staircase per floor, with dark areas, pits, chutes (floor 5 to 6), teleports, spinners, rock and ouch squares (verified: disk data) | - | 6 floors | [maps](maps/floors.txt) | planned `gameplay_f1`...`gameplay_f6`, `system_*` traps | described |
| World and navigation | Gnilda's temple | floor 1 (9,10), reached from floor 6 (1,4) by teleport (verified) | - | - | playbook | planned `dialogue_gnilda` | shown |
| Goals and gating | The chain | guardians -> five pieces -> one bearer wears all five -> sphinx's riddle (floor 6) -> Gnilda's test (alone) -> the staff -> Castle alone -> ending (verified, fights shortcut) | - | - | playbook, Game structure | `dialogue_sphinx`, `dialogue_gnilda_test`, `dialogue_staff_gift`, `ending_congratulations` | shown |
| Goals and gating | "One alone" | Gnilda's test and the ending only answer a party of one (verified: six with the staff get nothing, the staff is taken) | Tavern remove | 1 | [findings](findings.md) | `dialogue_gnilda_test` | shown |
| Chance | Encounters and combat rolls | as Wizardry I: random groups, hits, surprise (verified: surprise both ways seen) | - | - | - | planned `battle_surprised`, `battle_surprise` | described |
| Failure and recovery | Death, Temple, cemetery | as Wizardry I (inferred) | Temple | - | [Wizardry I](../../wizardry/design/systems.md) | planned `gameover_cemetery`, `menu_temple_dead` | described |
| Saving and sessions | The scenario disk | the roster on the disk is the save; Leave game ends the session; the Wizardry I disk is read only for the import (verified) | Edge of Town L | 20 slots | playbook, Saves | planned `save_leave_game` | described |
| Pacing and difficulty | Veterans only | the game assumes a high-level party: the first group met on floor 1 was 5 Kobold Kings, guardians from floor 1 (verified); without gear the party barely hurts them (verified) | - | - | - | `battle_f1_kobold_kings`, `boss_magic_armor` | shown |

## 3. How the systems feed each other
- Wizardry I's end state (levels, gold, spells, chevron) is Wizardry II's start; the items stay behind, so gold
  buys the first gear (inferred).
- Guardians gate the stairs and drop the pieces; the pieces gate the staff; the staff gates the ending; the
  ending's marks carry on (Wizardry III imports from both disks: owner's queue).

## Open questions
- Boltac's stock and prices; the Inn and Temple tables (shared with Wizardry I? not checked).
- Whether guardians 2-5 drop their pieces exactly like the Magic Armor (inferred).
- The exact "one alone" rule (party of one, or the bearer only?).
- Floor 6 fixed fights (group 47) and the floor 2 riddle (3,6).
