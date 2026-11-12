# Game settings: the Mode Settings screen

The **Mode Settings** screen holds nine switches that change sound, pictures and some rules for the whole save file.
Notation: [README.md](README.md#notation-and-style-binding-for-every-design-document). Everything here was traced in
the code and checked in play unless tagged.

## Overview

- The screen opens **once, at the first power-on** of a save file; B leaves it. After that it is only reachable in
  the maze: maze menu (Start) > **Settings**. There is no way to it from town.
- Four switches are **On / Off** (BGM, Sound, Effects, Pictures) and five are **Normal / Mania** (Map, Combat, Items,
  Inn, Save).
- They belong to the save file, not to a character. A new save starts with everything On / Normal **except Inn and
  Save, which start on Mania**.
- **Save is one-way:** once Save = Normal has been saved, the Save row can no longer be selected.
- Broadly, **Mania** gives the older, plainer Wizardry experience: a text location screen instead of the map, a
  plain Fight command, a plain Item command, the room inn, and no saving in the maze.

| Setting | Default | Off / Mania does |
|---|---|---|
| BGM | On | no music |
| Sound | On | no sound effects |
| Effects | On | no battle and spell animations |
| Pictures | On | the maze is drawn as a white wireframe instead of stone walls |
| Map | Normal | text location screen and coordinate Teleport instead of the auto-map |
| Combat | Normal | Fight is always a plain attack (no Aim to hit / Power hit) |
| Items | Normal | in battle, Item offers Use only (no Equip, no Throw) |
| Inn | **Mania** | the room inn (Stables to Royal Suite); Normal is a one-price full heal |
| Save | **Mania** | progress in the maze is only kept once the party is back in town |

---

## 1. Sound and pictures

- **BGM Off:** no song is started anywhere. Turning it on again in the maze restarts the floor's music.
- **Sound Off:** no sound effect is played (hits, wall bumps, doors, chests, temple results).
- **Effects Off:** battle and spell animations are skipped: the monster picture no longer shakes when the party hits,
  the screen no longer flashes when a monster hits, and spells show no animation. Messages and results are the
  same, so battles run faster.
- **Pictures Off:** the 3D maze view draws its walls as white lines on black instead of the floor's stone textures.
  Monster, town and shop pictures are unchanged.

Tech: [settings.md §2-§4](../tech/settings.md#2-bgm-and-sound)

## 2. Map

**Normal** is the graphic auto-map ([dungeon.md](dungeon.md#9-auto-map)). **Mania** replaces it with text:

- Compass and the Map Record Sheet print the party's floor, north and east position and facing.
- Teleport asks for a floor (1 to the deepest reached) and an offset of −15 to +15 north and east of the current
  square. A destination off the 16 × 16 grid puts the party in rock: everyone dies ("In rock"). The prompt cannot be
  cancelled ([findings](findings.md#39-a-teleport-to-an-unvisited-square-is-wasted-and-teleport-cannot-be-cancelled)).

Tech: [settings.md §5](../tech/settings.md#5-map), [dungeon.md §6](../tech/dungeon.md#6-auto-map)

## 3. Combat

With **Combat: Normal**, Fight opens a second choice:

| Choice | To-hit | Damage per hit |
|---|---|---|
| Normal | unchanged | unchanged |
| Aim to hit | `need` − 4 (+20% to hit) | ÷ 2 (at least 1) |
| Power hit | `need` + 4 (−20% to hit) | × 1.25 |

`need` is the number to roll on a d20 ([combat.md](combat.md#3-party-attacks-to-hit)). With **Combat: Mania** every Fight
is a Normal swing and the choice is not offered. The **Ambush** command gets the Aim-to-hit bonus and the Power-hit
damage in both modes.

The ± 4 is applied before `need` is clamped to 1-19. Hit chance = (20 − `need`) × 5%.

Example (computed): a Fighter who needs 11 (45%) and deals 8 per hit averages 3.6 per swing with Normal; Aim to hit
needs 7 (65%) for 4 per hit = 2.6; Power hit needs 15 (25%) for 10 = 2.5. On average Aim to hit only beats Normal
when Normal needs 17 or more (but not so much that both are stuck at the 5% minimum), and Power hit only when the
attacker is so accurate that `need` stays at 1 (95%) even with + 4.

Tech: [settings.md §6](../tech/settings.md#6-combat)

## 4. Items

With **Items: Normal**, the battle Item command offers **Use, Equip and Throw**, depending on what the character
carries. With **Items: Mania** it offers **Use** only, and the Item command is not shown at all when nothing the
character carries can be used. Outside battle nothing changes.

Tech: [settings.md §7](../tech/settings.md#7-items)

## 5. Inn

- **Inn: Mania** (the default) is the room inn described in [town.md](town.md#2-inn): Stables to Royal Suite,
  healing per night, prices per week.
- **Inn: Normal** has no rooms. A hurt character pays **10 × level** gold and is healed to full; at full HP the stay
  is free. Not enough gold: no stay. Either way the stay ages the character **7 days** and refills spells and
  checks for a level-up, like a room stay.

Example (verified): a level 5 character with 1 of 10 HP and 100 G pays 50 G and leaves with 10 HP, 7 days older.

Tech: [settings.md §8](../tech/settings.md#8-inn)

## 6. Save

The game keeps a working save and a backup; **every power-on restores the backup**.

- **Save: Normal:** the game is saved after every battle and with **End the quest** in the maze menu ("Make it
  safe to power off" / "Form another party"), and the backup follows each save. Turning the game off in the maze
  keeps everything up to the last battle.
- **Save: Mania** (the default): in the maze the backup is not updated and the maze menu has no End the quest. The
  backup is only written in town (entering or leaving the maze, the Training Grounds), at power-on and when the
  whole party dies. Turning the game off in the maze puts the party back where it was when it entered, with
  everything gained or lost since then undone (verified: a battle's EXP was lost and the party stood at the maze
  entrance).
- The switch only goes from Mania to Normal: once Normal is saved, the Save row is locked.

**Notes:** Mania therefore allows undoing a bad trip (a death or a lost item) by turning the game off, but a total
party wipe is saved at once (inferred for a single death: not tried). Normal makes every battle stick.

Tech: [settings.md §9](../tech/settings.md#9-save)

## Open questions

1. Which music track is which; what each battle and spell animation looks like.
2. Which items get Equip and Throw in battle (the item property behind them was not traced).
3. Undoing a single death by turning the game off with Save: Mania (expected from the save rule, not tried).

Tech: [settings.md §10](../tech/settings.md#10-open-questions)
