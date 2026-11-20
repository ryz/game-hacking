# Dungeon Master - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py amiga/dungeon-master`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
Shot ids are those of the set `main` (file names in `../shots/main/index.md`); the set `start` shows the
first hour again in play order.

## 1. Core loop
The party walks square by square through a level in real time, meets creatures and fights them with the
object in each champion's action hand or with spells, picks up and uses what lies around (keys in locks,
torches, food), opens doors with buttons and keys, eats, drinks and sleeps, and takes the stairs down
(verified: shots `gameplay_lock_key`, `system_key_used`, `system_door_opened`, `battle_hit`, `system_eat`,
`system_drink`, `gameplay_stairs_down`). Skills grow by use, so every blow and spell makes the champion
better (verified: `system_level_up`). Fourteen levels lead down to Lord Chaos; the quest ends when he is fused
with the Firestaff (verified: `boss_chaos_fused` .. `ending_champions`).

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move and turn | six moves: forward, back, step left/right without turning, turn left/right; one square per move (verified) | keypad 8/5/4/6/7/9 or the six arrows | about 30 frames per step with a light party (verified) | playbook Controls | `hall_start`, `env_l2_corridor` | shown |
| Player verbs | Take and put | the leader's hand takes an object from the floor or a wall and puts it into a slot, a lock or the world (verified) | click in the view / on a slot | - | [interface.md](interface.md) 4 | `system_torch_taken`, `system_key_taken`, `system_pick_up` | shown |
| Player verbs | Use wall devices | buttons open doors and gates, keyholes take the matching key (a gold key opens the gate at level 2 (0,3); a topaz key does not fit the lock at (2,12)) (verified) | click the button / the lock with the key | - | [maps.md](maps.md) level 2 | `system_door_opened`, `system_key_used`, `gameplay_lock_key`, `gameplay_l2_door_button` | shown |
| Player verbs | Throw | the THROW action sends the object in the action hand down the corridor (verified) | action button, THROW | - | - | `system_throw` | shown |
| Player verbs | Freeze | Esc stops the game until the next input; every control is hatched (verified) | Esc | - | playbook | `system_freeze` | shown |
| Characters and progression | Choosing champions | up to four of the champions in the hall's mirrors; RESURRECT keeps a champion as he is, REINCARNATE gives him a new name (verified) and turns his skills into statistics (source: manual) | click a mirror, then RESURRECT / REINCARNATE / CANCEL | 24 champions, 23 found (playbook Hall map) | playbook | `hall_mirror`, `system_champion_panel`, `system_reincarnate_name`, `system_reincarnated`, `system_resurrected`, `hall_champion_lizard`, `hall_champion_wizard`, `hall_champion_ninja`, `hall_champion_priestess`, `hall_champion_gothmog` | shown |
| Characters and progression | Party and leader | four champions in a 2 x 2 formation; the leader's hand does the clicking in the view; clicking a name makes that champion leader (verified) | click a name | - | - | `system_party_four`, `system_leader` | shown |
| Characters and progression | Formation | front row takes the melee blows and can strike, back row is safe from melee (verified: with the front row turned away from a monster the casters took the hits, RAM health) | drag the formation icons | - | [findings.md](findings.md) | `system_party_four` | shown |
| Characters and progression | Skills and levels | four classes (fighter, ninja, priest, wizard) with ranks from Neophyte to Archmaster; a rank comes at each doubling of experience (500, 1000, 2000 ... ) (inferred: 15995 -> one blow -> "JUST GAINED A FIGHTER LEVEL!", RAM); a new fighter rank also raised RYZ's maximum health from 90 to 121 (verified) | fight, cast | ranks on the final roll: Novice, Apprentice, Artisan, Adept (verified) | - | `system_level_up`, `ending_champions`, `inventory_tiggy_late` | shown |
| Characters and progression | Statistics | strength, dexterity, wisdom, vitality, anti-magic, anti-fire, plus health, stamina, mana; shown while the eye is held (verified) | hold the eye in the inventory | RYZ 55/43/34/51/38/50 at the start (verified) | - | `inventory_stats` | shown |
| Resources and economy | Food and water | two bars that fall over time; food is eaten at the mouth, water drunk from fountains or flasks (verified) | drop food on the mouth; click a fountain | one Screamer slice raised the bar visibly (verified) | - | `inventory_ryz`, `inventory_feed`, `system_eat`, `system_drink`, `gameplay_fountain` | shown |
| Resources and economy | Light | torches in hands and the magic torch spell light the view; without light the view shows only outlines (verified) | hold a torch, cast FUL | a taken torch reads 15 in what looks like its charge field (inferred, RAM) | - | `env_l2_dark`, `system_magic_light`, `system_torch_sconce`, `system_torch_taken`, `system_champion_dead` | shown |
| Resources and economy | Load | weight carried against a maximum that depends on the champion (verified: RYZ 6.7/54 kg, Tiggy 1.6/34 kg) | - | - | - | `inventory_ryz`, `inventory_tiggy` | shown |
| Resources and economy | Money | none: coins exist as objects (ROM text), there is no shop | - | - | - | none: the game has no economy | described |
| Conflict | Real-time melee | each champion attacks with the object in his action hand; the action list depends on the object (club: THROW, BASH; axe: SWING, CHOP; empty hand: PUNCH, KICK, WAR CRY; wand: CALM; Firestaff: INVOKE, FUSE, FLUXCAGE) (verified); damage appears in a starburst; the champion's action icon is hatched while he recovers (verified) | action button, then the action | RYZ's BASH: 17 and 21 damage seen (verified) | - | `system_action_menu`, `system_action_wuuf`, `battle_hit`, `battle_screamers` | shown |
| Conflict | Damage to the party | blows and spells show the damage on the hurt champion's bar; a champion at zero health dies, his bar shows a skull and his bones and belongings fall to the floor (verified) | - | a Trolin hit RYZ for 28; a fireball 71/86/74/63 (verified) | - | `battle_trolin`, `battle_fireball`, `system_pit_fall`, `system_champion_dead` | shown |
| Opponents | Creatures | 27 kinds; each level has its own mix (two on level 2, Demons and Lord Chaos on level 13) (RAM: [maps.md](maps.md)); some cast spells at the party (Vexirk and Demon fireballs, verified) | - | 27 kinds | [content.md](content.md) 3 | `battle_mummies`, `battle_demon`, `battle_fireball`, `battle_giggler` | shown |
| Opponents | Spoils | a killed Screamer leaves a slice of food (verified); a killed Mummy crumbles to dust (verified) | - | - | - | `system_pick_up` | shown |
| Items and equipment | Slots | hands (ready and action), head, neck, torso, legs, feet, pouch, quiver, backpack (verified on screen) | drag in the inventory | 30 slots per champion (RAM) | - | `inventory_ryz`, `inventory_tiggy`, `inventory_potion` | shown |
| Items and equipment | Examining | an object held over the eye shows its name and weight (verified) | hold the object on the eye | club 3.6 kg (verified) | - | `inventory_examine` | shown |
| Abilities and magic | Runes | a spell is spoken as up to four symbols: a power (LO .. MON), then element, form and alignment; each symbol costs mana; the caster's tab and the incantation line show the spell being built (verified) | spell panel | - | [content.md](content.md) 5 | `system_runes` | shown |
| Abilities and magic | Spells | ON FUL = magic torch (verified: dark view lit); ON FUL IR = fireball (verified, Tiggy at Adept rank); LO VI with an empty flask in hand = a healing potion (verified: flask turned into a potion, mana 30 -> 27) | cast line | - | - | `system_magic_light`, `system_potion`, `inventory_potion`, `system_spell_fireball`, `battle_spell_cast` | shown |
| World and navigation | Levels and stairs | stairs link the 14 levels; turning while standing on a staircase takes it (verified) | walk | 14 levels (RAM) | [maps.md](maps.md) | `gameplay_stairs_down`, `gameplay_stairs_up` | shown |
| World and navigation | Doors and gates | wooden doors and iron gates, opened by a button on the frame, a key in a wall lock, or (the hall gate) by having a champion (verified) | click | - | - | `gameplay_door_closed`, `system_door_opened`, `hall_gate_closed`, `hall_gate_open`, `gameplay_door_window` | shown |
| World and navigation | Pits | an open pit drops the party one level and hurts every champion (verified: 43/33/35/42) | walk in | - | - | `gameplay_pit`, `system_pit_fall` | shown |
| World and navigation | Teleporters | squares that move the party; on level 2 the ones checked are invisible (RAM: square type, verified: nothing drawn) | walk in | 9 on level 2 (RAM) | [maps.md](maps.md) | none: an invisible teleporter has nothing to show | described |
| Goals and gating | Quest | get the Firestaff and its gem, trap Lord Chaos and FUSE him; Lord Order and Chaos become the Grey Lord again (verified, ending reached) | FUSE action of the complete Firestaff | - | [findings.md](findings.md) | `boss_lord_chaos`, `boss_chaos_fused`, `ending_lord_order`, `ending_fusion`, `ending_grey_lord`, `ending_truth`, `ending_harmony`, `ending_names`, `ending_champions` | shown |
| Goals and gating | Keys and locks | doors and gates beyond the first rooms need keys found nearby (verified: gold key at level 2 (0,2) for the lock at (0,3)) | - | - | - | `gameplay_lock_key`, `system_key_used` | shown |
| Chance | Hits and misses | blows can miss (verified: many BASH attempts against Screamers without damage before the formation was right); damage varies (17, 21) (verified) | - | - | - | `battle_hit` | shown |
| Failure and recovery | Death and game over | dead champions show skulls; when all four are dead the screen fades to "The End" (verified); a dead champion can be revived at an altar (source: manual, not tried) | - | - | - | `gameover_party_dead`, `gameover_the_end` | shown |
| Failure and recovery | Rest | ZZZ puts the party to sleep (the view goes dark, WAKE UP); sleeping restores health, stamina and mana (source: manual; not measured) | ZZZ icon | - | - | `system_sleep` | shown |
| Saving and sessions | Save disk | save at any time from the inventory to a separate disk the game formats itself; RESUME at the entrance loads it (verified) | disk icon, FORMAT FLOPPY, SAVE; RESUME | DMGAME.DAT 48652 bytes (verified) | playbook | `save_menu`, `save_blank_prompt`, `save_formatting`, `save_saving`, `save_resume_prompt`, `save_loaded` | shown |
| Pacing and difficulty | Depth | creatures get stronger and more numerous level by level (Mummies and Screamers on level 2, Demons, Lord Chaos and the Red Dragon at the bottom) (RAM: [maps.md](maps.md)); the long floppy loads (80 s at start) set the pace of a session (verified) | - | - | - | `battle_mummies`, `boss_red_dragon`, `boot_logo` | shown |

## 3. How the systems feed each other
- Fighting and casting give experience -> ranks -> more health, stamina, mana and better hits (verified: level
  up raised maximum health 90 -> 121).
- Monsters drop food (Screamer slices) -> food keeps the party alive -> longer expeditions.
- Light (torches burn, the spell costs mana) -> without it the party sees nothing -> mana and torches are a
  resource like food.
- Keys and buttons gate the way down -> exploring each level for them -> more fights, more experience.
- Front and back rows: fighters in front absorb blows so casters can work; a wrong turn of the formation
  exposes the casters (verified, [findings.md](findings.md)).

## Open questions
- How long a torch lasts in minutes, and how fast food and water fall (bars seen falling, not timed).
- Sleep: how much each hour of rest restores.
- Altars of rebirth (manual) and Gando's mirror (playbook) were not reached.
