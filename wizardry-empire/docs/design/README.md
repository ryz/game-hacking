# Game design reference (Wizardry Empire, GBC, 1999)

How the game works, for game designers: the rules, formulas and data behind characters, combat, items, the town
and the dungeon. No ROM addresses here; the same systems with addresses and evidence are in `../tech/`, which is
the source of truth for every number. Rules for these documents: `../README.md`.

## Notation and style (binding for every design document)

This section is the single definition; the other documents do not repeat it.

**Numbers and rolls**
- **Random numbers:** in prose "a random number from 0 to 19" (both ends included); in pseudocode `Rnd(0, 19)`.
  No other helper names, no "d20" for a 0-19 roll.
- **Dice:** `NdS+B` = the sum of N rolls of 1 to S, plus B (`3d6+2` = 5 to 20; `5d8` = 5 to 40). Every damage, HP
  and healing roll is written this way.
- **Rounding:** divisions round down unless a rule says otherwise. Percentages are rounded; the game's rolls are very
  slightly uneven (a 0-19 roll comes up 0 a little more often than 1 in 20), which these documents ignore.
- **Percent:** `5%` (no space).
- **To-hit**, the same shape for everyone: `need = clamp(attacker's to-hit − target AC − weapon Hit+, 1, 19)`; the
  attack hits if `Rnd(0, 19) ≥ need`. So the hit chance is always between 5% and 95%.
- **Pseudocode** (C#-style) only where a rule branches (caps, several cases); a single comparison is prose.

**Confidence tags** (plain text, after the number or sentence they cover)
- **(verified)** seen in the running game.
- untagged = **data**: read from the game's own tables or code, not observed in play. Do not write "(data)".
- **(inferred)** reasoned from code or data with a gap in the evidence.
- **(computed)** worked out in these documents from a stated rule or table (an average, a percentage).
- **(game text)** only known from an in-game description (e.g. the museum).
- **(v1.0)** true of the original release, not of Rev 1.

**Words**
- **Stats:** STR, IQ, PIE, VIT, AGI, LUK (Strength, I.Q., Piety, Vitality, Agility, Luck); AC armor class (lower is
  better); HP hit points; EXP experience. Use the abbreviations in rules.
- **Classes in tables:** Fig Mag Pri Thi Bis Sam Lor Nin Arc Val Ave Mus Kun Sum.
- **Gold:** `100 G`. **Coordinates:** (x, y), x east, y north. **Spelling:** American (armor, behavior, favor).
- **Names** follow the English translation (`../../glossary.md`). Tables quote the in-game names, which may be
  shortened (ShadowDragon, Gr. Demon); prose uses the full name (Shadow Dragon, Greater Demon). Data tables also
  give the Japanese name.
- **Elements:** Earth, Water, Fire, Wind, Spirit, the 6th element (name not read), Holy, None.
- **Monster terms:** swings (per round), special hits, chest rating (monster) -> chest value (rolled) -> tier.
- **No engineering words** in prose: not record, field, flag, bit, byte, routine, caller, handler, path, "code N",
  "school N". Say what it means in play; if unknown, "not traced".
- **No comments about the documentation** ("the tech notes say"): write "not traced" or "unconfirmed".

**Structure**
- Title "Topic: contents"; numbered sections (`## 1. ...`); an Overview a designer can read in two minutes first.
- One home per rule; other documents link to it. Quirks: stated as the game does it, with a link to
  [findings.md](findings.md). A findings entry is a `##` heading plus four labelled parts, in this order:
  `**Behavior:**`, `**Intended:**`, `**Confidence:**`, `**Impact:**`, then the Design/Tech links.
- Each section ends with a **Tech:** link to its implementation notes; each document ends with Open questions.

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
| [dungeon.md](dungeon.md) | Floors, special squares, zones, secret and locked doors, traps, chests, events, warps, the auto-map |
| [maps/](maps/README.md) | Floor maps: how to read them, and one page per floor |
| [settings.md](settings.md) | The Mode Settings screen: sound, pictures, and the Normal / Mania rule switches |
| [findings.md](findings.md) | Designer's notes: quirks and likely original bugs, with what the game does and what was probably intended |

Start with the Overview of each document; [findings.md](findings.md) collects everything that looks unintended.
