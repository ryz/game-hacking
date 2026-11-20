# Dungeon Master - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The party walks square by square through a level, fights what comes in real time with weapons and spells, picks
up and uses objects, solves doors, levers and pressure plates, eats, drinks and rests, and takes the stairs down
(source: manual). Skills grow by use, so fighting and casting make the champions stronger; deeper levels bring
stronger creatures and the quest items (source: manual, Wikipedia). First steps verified: choosing four champions,
taking a torch, going down to level 2, saving and resuming (playbook checkpoints).

## 2. Systems
Go through every group; write "none" where the game has nothing, do not drop the group.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move and turn | six moves: forward, back, step left/right, turn left/right; one square per move | keypad 8/5/4/6/7/9 or the arrows | - | playbook Controls | (planned) hall_start | described (verified in play) |
| Player verbs | Take, put, throw, press | the leader's hand takes objects from the floor and walls, operates levers and buttons; an object held at eye level is thrown | click in the view | - | manual | (planned) system_torch_taken | verified (torch from a sconce) |
| Player verbs | Freeze | the game stops until a key/click | `esc` | - | playbook | (planned) system_freeze | verified |
| Characters and progression | Choosing champions | up to four of the champions in the hall's mirrors; resurrect keeps them, reincarnate renames them and turns skills into statistics | click a mirror, RESURRECT / REINCARNATE | 24 champions (23 found), stats per champion in the playbook | playbook Hall map | (planned) system_champion_panel | verified |
| Characters and progression | Skills and levels | fighter, ninja, priest, wizard; ranks Neophyte to Archmaster; gained by use | fight, cast | 15 rank names (ROM text) | manual | (planned) system_level_up | described |
| Characters and progression | Statistics | strength, dexterity, wisdom, vitality, anti-magic, anti-fire; health, stamina, mana | eye in the inventory | - | manual | (planned) inventory_stats | described |
| Resources and economy | Food and water | drop over time; eating and drinking at the mouth; starving kills | mouth in the inventory | - | manual | (planned) inventory_ryz | described (bars seen) |
| Resources and economy | Light | torches and light spells; level 2 is dark without them | torch in a hand, LO FUL | - | playbook | (planned) env_l2_dark, env_l2_corridor | verified (dark vs lit) |
| Resources and economy | Load | weight carried against a maximum; overload slows the party | - | e.g. 6.7/54 kg for ryz | manual | (planned) inventory_ryz | described |
| Conflict | Real-time combat | each champion attacks with the object in the action hand; actions depend on the object and skill; front row reaches with swung weapons | action button, action name | club: THROW, BASH | manual | (planned) system_action_menu, battle_* | described (menu verified) |
| Conflict | Formation | four positions, front and back; swap by dragging icons | formation icons | - | manual | (planned) system_formation | verified |
| Opponents | Creatures | 27 named creature kinds on the disk, from Giant Scorpion to Lord Chaos | - | 27 | content.md | (planned) battle_* | described |
| Items and equipment | Slots | hands (ready, action), head, neck, torso, legs, feet, pouch, quiver, 17 backpack slots | drag in the inventory | - | manual | (planned) inventory_ryz | described |
| Abilities and magic | Runes | spells are sequences of up to four symbols: power (LO weakest .. MON strongest), element, form, alignment; each symbol costs mana; cast or recant; magic torch = power + FUL | spell panel | LO FUL cast by Tiggy | manual | (planned) system_runes, system_cast | verified (cast, mana spent) |
| World and navigation | Levels and stairs | stairs link levels; turning on a staircase takes it | walk | 14 levels (source) | playbook | (planned) gameplay_stairs_down | verified |
| World and navigation | Doors, gates | doors with buttons; the hall gate opens once the party has a champion | click buttons | - | playbook | (planned) hall_gate_closed, hall_gate_open | verified (gate) |
| Goals and gating | Quest | recover the Firestaff (and the Power Gem), defeat Lord Chaos; a second ending for leaving with the staff | - | - | Wikipedia | - | described |
| Chance | (open) | - | - | - | - | - | open |
| Failure and recovery | Death | a champion at zero health dies (manual); what follows was not seen | - | - | manual | (planned) gameover_party_dead | open |
| Saving and sessions | Save disk | save at any time from the inventory to a separate disk the game formats; RESUME at the entrance | disk icon, FORMAT FLOPPY, SAVE; RESUME | DMGAME.DAT 48652 bytes | playbook | (planned) save_* | verified |
| Pacing and difficulty | (open) | - | - | - | - | - | open |

## 3. How the systems feed each other
The loops between systems (e.g. fights give experience and money, money buys training, training raises
statistics, statistics decide fights): a short list or a small diagram in text.

## Open questions
- Started by the scout (2026-11-20); shots are planned ids from `../shots.txt`, not captured yet. Tags: verified
  = seen in the emulator (playbook routes), described = manual or ROM text.
