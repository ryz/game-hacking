# Game design reference (Wizardry Empire, GBC, 1999)

How the game works, for game designers: the rules, formulas and data behind characters, combat, items, the town
and the dungeon. No ROM addresses here; the same systems with addresses and evidence are in `../tech/`, which is
the source of truth for every number. Rules for these documents: `../README.md`.

## How to read these documents
- **Dice:** `NdS+B` = the sum of N rolls of 1..S, plus B (`3d6+2` = 5 to 20). "A random number from 0 to 19" is
  written out where the game rolls from 0.
- **Stats:** STR Strength, IQ I.Q., PIE Piety, VIT Vitality, AGI Agility, LUK Luck; AC armour class (lower is
  better); HP hit points; EXP experience.
- **Confidence:** **(verified)** seen in the running game, **(data)** read from the game's own tables (the default
  when untagged), **(inferred)** reasoned from code or data but not observed.
- **Names** follow the English translation (`../../glossary.md`); data tables also give the Japanese name.
- Each section ends with a **Tech:** link to its implementation notes.

## Documents

| Document | Covers |
|---|---|
| [characters.md](characters.md) | Races, character creation and bonus points, classes and their requirements, special classes, class change, experience and leveling, aging, status ailments |
| [spells.md](spells.md) | Spell schools and levels, the spell list, how spells are learned, spell slots, Summoner pacts |
| [combat.md](combat.md) | Round structure, hitting and damage for the party and for monsters, special attacks and saves, spell resistance, escape, rewards |
| [items.md](items.md) | Equipment rules, using items, special powers, identification and curses |
| [items_table.md](items_table.md) | Every item with its stats (generated) |
| [town.md](town.md) | Shop, inn (healing, aging), temple (fees, resurrection), where gold comes from |
| [monsters.md](monsters.md) | The bestiary, encounters and group formation, how monsters choose actions |
| [monsters_table.md](monsters_table.md) | Every monster with its stats, plus the encounter tables (generated) |
| [dungeon.md](dungeon.md) | Floors, special squares, damage zones, traps, chests, events per floor |
| [findings.md](findings.md) | Designer's notes: quirks and likely original bugs, with what the game does and what was probably intended |

Start with the Overview of each document; [findings.md](findings.md) collects everything that looks unintended.
