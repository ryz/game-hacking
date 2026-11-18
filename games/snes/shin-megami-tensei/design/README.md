# Shin Megami Tensei (Super Famicom, English translation patch) - design reference

How the game works, for game designers: rules, formulas, progression, data tables, and quirks, built up while
the game is researched and played. No RAM/ROM addresses here (those live in `../playbook.md`). Screenshots are
the evidence: link them (`../shots/main/<file>.png`; the file name of a shot is in the set's `index.md`).

## Notation and style (binding for every document in this folder)
- **Confidence tags** after the claim they cover:
  **(verified)** seen in play here (name the shot id or the route/checkpoint);
  **(source)** from the manual/FAQ/wiki, link in Sources below;
  **(RAM)** read from or tested through memory while playing (e.g. the HP formula from before/after values);
  **(inferred)** reasoned from observations with a gap;
  **(computed)** worked out here from a stated rule or table.
  A claim with no tag is not allowed.
- **Numbers:** decimal; random ranges in prose "a random number from 1 to 8"; dice `NdS+B`; percentages `5%`.
- **Names:** the game's own on-screen names (English release; give the original name in tables if the game is
  Japanese-only). Prose uses full names.
- **No engineering words** in prose (byte, flag, routine): say what it means in play.
- **Structure:** each document starts with an Overview a designer reads in two minutes, then numbered sections
  (`## 1. ...`); one home per rule (other documents link to it); each document ends with **Open questions**
  (what is not known, what was tried). Never fill a gap with a guess presented as fact.
- **Quirks and likely bugs** go in [findings.md](findings.md): a `##` heading, then `**Behavior:**`,
  `**Intended:**`, `**Confidence:**`, `**Impact:**`.

## Overview
Shin Megami Tensei is a first-person dungeon role-playing game set in Tokyo, first in "199X" and later in its
ruins **(source: Wikipedia)**. The player walks grid-based 3D corridors and a 2D overhead town map, fights
turn-based battles, and builds a party out of the demons he meets: demons can be talked to, recruited, summoned
through a computer program and fused into stronger ones **(source: Wikipedia)**. Summoned demons cost
Magnetite while walking, and the hero's choices move him between Law, Neutral and Chaos, which changes the
demons that will join, the areas that open and the ending (three endings) **(source: Wikipedia)**. The game
opens with a dream in which the player names the hero and two future companions and divides 18 points among
six stats for each **(verified: checkpoints `dream` to `start`)**. Progress is kept in two battery save files,
first written from the hero's room **(verified: save `01_start`)**. This is the Japanese Super Famicom
release with the Aeon Genesis English translation; the on-screen names used here are that translation's.

## Documents
| Document | Covers |
|---|---|
| [characters.md](characters.md) | character creation, the six stats, what the status screen shows |
| [world.md](world.md) | view modes, the opening sequence, places seen so far, moon phase |
| [economy.md](economy.md) | yen, the arcade shops, price lists |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [combat.md](combat.md) | battle commands, first damage and EXP numbers, level-up, death, demon negotiation (started run 2) |

Planned, to be started by the capture agent when the systems are seen: `demons.md` (summoning, Magnetite,
fusion; negotiation is in `combat.md` for now), `alignment.md`, `items.md`.

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Shin_Megami_Tensei_(video_game) | genre, systems, structure, endings |
| The game (checkpoints `dream`, `start`, `apartment`, `kichijoji`, `lv23`, `bldg_red`, `arcade`, `knifeshop`, `armed`, `coffee`) | `../checkpoints.txt` | everything tagged verified or RAM |
