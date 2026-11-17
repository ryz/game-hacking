# Controls and commands

## Overview
Outside battle the A button opens a window of eight commands; nothing in the world reacts to walking into it
except map exits. **(verified)** `@start` In battle a window of four commands appears each turn. **(verified)**
`@late_battle`

## 1. Field commands
| Command | What it does | Confidence |
|---|---|---|
| Talk | asks for a direction (N, W, E, S), then speaks to the person on that side | **(verified)** `@start`, king to the north |
| Spell | lists the spells known; ten at level 21: Hoimi, Gira, Laliho, Remira, Mahot.., Riremi.., Lulra, Toher.., Behoi.., Begira.. | **(verified)** `@late` |
| Stats | Lvl, Power, Speed, Max HP, Max MP, AtkPwr, DefPwr, weapon, armour, shield | **(verified)** `@late`: 21, 95, 82, 149, 122, 135, 91 |
| Items | Herb and Key with counts, then up to eight single items | **(verified)** `@late` |
| Stairs | uses the staircase under the hero | **(verified)** throne room to the castle |
| Check | searches the ground under the hero | **(source)** |
| Door | opens a door beside the hero (no direction asked, no message, the door tile disappears); "No doors here!" otherwise | **(verified)** `@start_door`; that it spends the Key **(source)** |
| Take | takes what is in the chest under the hero: the first throne-room chest holds 120 Gold | **(verified)** `@start` |

## 2. Battle commands
Fight, Spell, Flee, Items. **(verified)** A level 21 hero kills a Slimess with one Fight and gets 1 experience
and 2 Gold. **(verified)** `@late_battle`

## 3. The status window
Standing still for about a second shows name, LVL, HP, MP, G and E; it also stays up while a command window is
open. **(verified)** `@start`

## Open questions
- What Check finds and where. Not tried.
- Stairs on a tile without stairs: "No entry here." **(verified)**
- Start and Select: no effect seen in the command window; not tried while walking.
