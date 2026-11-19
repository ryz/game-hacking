# Wizardry: Proving Grounds of the Mad Overlord - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
No shot set exists yet (scout stage): `planned` = the shot plan in `../playbook.md` covers it; the Shots column
names the checkpoint that reaches the screen.

## 1. Core loop
Form a party in the Tavern, buy and equip in the trading post and the camp, enter the maze, fight groups of
monsters for experience and chests, come back up the stairs before the party is spent, rest at the Inn (which
heals and grants the levels earned), cure the fallen at the Temple, and go deeper **(verified: each step's
screen; the loop itself is the DOS port's, source)**. Between loops the characters gain levels, spells and
gear; the maze does not change.

## 2. Systems
Go through every group; write "none" where the game has nothing, do not drop the group.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Castle menus | one letter per place: Inn, Tavern, Trading post, Temple, Edge of Town **(verified)** | `a g b c e` | - | playbook Controls | `start` | planned |
| Player verbs | Tavern: add, remove, see | members are added by typing their name and password; six at most **(verified)** | `a` + name, `r`, digit | 6 members | playbook | `start` route | planned |
| Player verbs | Maze movement | forward, turn left, turn right, kick through a door; walking into a wall prints OUCH! in the view **(verified)** | `f l r k` or `w a d` | 20 x 20 squares | playbook | `maze1` | planned |
| Player verbs | Camp | inspect, reorder, equip everyone, disband (leave the party in the maze), leave **(verified: e, digits, l; r and d prompts)** | `c`, then digit `r e d l` | - | playbook | `camp`, `gcamp` | planned |
| Player verbs | Maze utilities | status, quick plot, message delay 1-5000, inspect for bodies **(verified: t and i; s and q accepted)** | `s q t i` | delay 1-5000 | playbook | - | open (s, q) |
| Player verbs | Battle orders | fight, spell (typed name), parry, run, use, dispell (priests); confirm the round or go back **(verified: f s p)** | `f s p r u d`, Return, `b` | up to 4 groups | DOS systems | `battle`, `werdna` | planned |
| Player verbs | Chest | open, Calfo, leave, inspect, disarm (typed trap name) **(verified: menu; program text for the rest)** | `o c l i d` | 10 trap names | DOS systems | `chest` | planned |
| Characters and progression | Creation | name, optional password, race (5), alignment (3), bonus points onto six scores, class from those the scores allow, keep or discard **(verified)** | typed name, letters, `+ -` Return Esc | bonus 7 seen; scores 5-9 for a human before points | playbook Naming | `start` route | planned |
| Characters and progression | Classes | fighter, mage, priest, thief, bishop, samurai, lord, ninja **(verified: the first five created; the last three on the inherited roster)** | - | 8 | DOS systems | - | planned |
| Characters and progression | Levels | experience from fights; the Inn tells what is missing and grants levels **(verified: "YOU NEED 257878 MORE EXPERIENCE POINTS TO MAKE LEVEL" for a level 13 fighter)** | Inn stay | - | DOS systems | - | planned |
| Characters and progression | Training Grounds edits | inspect, delete, reroll, change class, set password **(verified: inspect, delete, change-class prompt)** | name, then `i d r c s` | - | playbook | - | planned |
| Characters and progression | Age | shown in years on the sheet; "YOU HAVE DIED OF OLD AGE" exists **(verified: sheet; program text)** | - | - | DOS systems | - | described |
| Resources and economy | Gold | rolled at creation (117-186 seen), from chests, spent at the Inn, Temple and trading post **(verified: sheet, shop)** | - | cots 10, economy 50, merchant 200, royal 500 per week; long sword 25, dagger 5 | DOS systems | - | planned |
| Resources and economy | Spell points | per spell level 1-7, for mage and priest lists separately, shown as 9/8/7/6/5/4/2 **(verified)** | - | - | DOS systems | - | planned |
| Conflict | Rounds | all orders first, then the round plays as timed messages **(verified)** | - | message delay adjustable | DOS systems | `werdna_won` route | planned |
| Conflict | Surprise | either side can surprise the other; a surprised party loses its first round **(verified both ways at Werdna's door)** | - | - | DOS systems | - | planned |
| Conflict | Friendly groups | monsters may hail the party; fight or leave in peace **(verified: Werdna himself)** | `f l` | - | findings | - | planned |
| Conflict | Level drain, stoning, death | a vampire's hit drained 4 levels; RYZ was stoned or killed in most Werdna tries **(verified)** | - | - | DOS systems | - | planned |
| Opponents | Unidentified names | groups appear as "UNSEEN ENTITY", "MAN IN ROBES", "SLIMES" until known **(verified)** | - | 101 monster records, 20 pictures (disk data) | content | `battle`, `werdna` | planned |
| Items and equipment | Slots | weapon, armor, shield, helmet, gauntlets, misc; marks * equipped, - cursed, ? unknown, # unusable **(verified: four slots equipped; legend on the sheet)** | camp `e` | 8 pack places | DOS items | `gcamp` | planned |
| Items and equipment | Identify, uncurse | at the trading post for a fee, or by a bishop **(program text; sheet entry seen)** | `i u` | - | DOS systems | - | planned |
| Abilities and magic | Spells by typed name | 21 mage and 29 priest spells in seven levels; cast in camp or in battle **(verified: Halito, Malikto, Tiltowait, Lahalito, Dumapic, Malor; DEDDO's book lists all 21)** | `s` + name | - | DOS content | - | planned |
| World and navigation | Floors and special squares | stairs, elevators with buttons, chutes, pits, darkness, teleports, messages, fixed fights **(verified: stairs, both elevators, chute, darkness, messages; disk data for the rest)** | - | 10 floors | maps/floors.txt | - | planned |
| World and navigation | Malor | teleport by a typed displacement east/north/down; wrong targets kill or lose the party **(verified: the trip home; program text for the failures)** | `n s e w u d`, Return | - | playbook | `malor_home` | planned |
| Goals and gating | The amulet | beat Werdna on floor 10 (17,3), carry the amulet to the castle **(verified)** | - | reward 250,000 experience points each | playbook | `werdna_won`, `ending` | planned |
| Goals and gating | The price of the ending | all equipment and all gold above the last four digits are taken; the chevron stays **(verified)** | - | 24,817 -> 4,817 gold | findings | `after_ending` | planned |
| Chance | Encounters, rolls | hit points and gold at creation, encounters, surprise and round results differ with timing **(verified)** | - | - | - | - | described: no screen of its own |
| Failure and recovery | Death and the cemetery | dead members stay in the roster; the Temple raises for a donation; a wiped party is left in the maze **(program text; DOS systems)** | - | - | DOS systems | - | planned |
| Saving and sessions | The roster disk | characters are written when made, when the party changes, and on Leave game; a party can be left in the maze (OUT) **(verified: saves 01 and 02 read back; OUT is program text)** | Edge of Town `l` | 20 slots | playbook Saves | - | planned |
| Saving and sessions | Utilities | backup, recover, transfer between scenario disks, make a scenario disk, update, change names **(verified: menu only)** | boot menu `u` | - | playbook | - | planned |
| Pacing and difficulty | Werdna | an unequipped level 13 party loses four members to his first spell when surprised, and wins in one round with three spells when it acts first **(verified)** | - | Werdna 87 hit points in that fight | playbook Strategy | - | planned |

## 3. How the systems feed each other
- Fights give experience and chests; chests give gold and unidentified items **(verified: 27 experience points
  each for three slimes, then a chest)**.
- Gold buys gear (armour class), Inn weeks (healing, levels) and Temple cures **(verified: price lists)**.
- Levels give hit points, spell points and new spells, which decide the deeper fights **(source: DOS documents)**.
- The ending resets wealth (no items, little gold) but leaves levels and adds experience: the characters are
  meant to go on to the next scenario **(verified: `after_ending`; inferred: the purpose)**.

## Open questions
- What Status and Quick plot change in the maze.
- Every rule taken from the DOS documents and not re-checked here (level tables, hit and damage rules, trap effects).
- Whether the price lists and Temple donations equal the DOS port's beyond the first stock page.
