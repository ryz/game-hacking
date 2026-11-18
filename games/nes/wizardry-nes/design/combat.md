# Wizardry (NES) - combat

## Overview
Fights are turn-based rounds: the player gives every member an order, confirms with "Fight", and then all
actions of the round are told one message at a time.

## 1. Encounters
- Monster groups (up to four lines) are shown with a count, unidentified at first ("5 Small humanoids", "Man in
  kimono", "Unseen entity"); a group can become identified during the fight ("Man in kimono" became "High
  Ninja") **(verified: `battle_fixed`, then round 2)**.
- Some encounters are "friendly" and offer Fight / Leave **(verified: `murphy_friendly`)**; either side may
  surprise the other ("The monsters surprised you": they act a round first) **(verified: Werdna)**.

## 2. Orders
- Fighters: Fight, Parry, Run, Take back; Clerics add Spell and Dispell; Mages and Wizards have no Fight
  **(verified: `battle_options`, `battle_cleric_options`, `battle_orders`)**. The front three can fight, the
  back three cannot (Thief and Mage offered only Parry/Spell) **(verified)**.
- Spells are chosen by level page; the page shows the casts left at that level ("Cleric Spell L5(3)") and only
  the spells usable in combat (Calfo is missing from L2) **(verified: `battle_spell_menu`)**.

## 3. Results seen
- Group spells hit each monster of a group with its own damage roll: Litokan 17 and 16, Mahalito 16 and 12
  **(verified: `battle_cast_cleric`, `battle_cast_mage`)**; Tiltowait hits every monster **(verified)**.
- Melee reports the number of hits ("hits 2 times for 11 damage") **(verified)**.
- Monster mages cast Dilto, which raised the whole party's AC from 10 to 12 **(verified)**.
- Vampires paralyze and drain levels ("CONDI is Drained 4 levels") **(verified: `werdna_drain`)**.
- After a win "Each survivor gets N E.P." (741 for Murphy's ghost, 1966 for the floor 4 guardians, 5972 for
  Werdna's group) and gold or a chest **(verified)**.

## 4. Chests
- "A chest! You may: Inspect, Calfo, Disarm, Open, Leave alone" **(verified: `chest`)**. Inspecting can set the
  trap off: a Fighter inspecting triggered a Teleporter trap **(verified: `chest_trap`, `chest_teleporter`)**;
  the loot is then shared out ("DEDDO found RING") **(verified: `chest_loot`)**.

## 5. Death
- A member at 0 hit points "is Killed" **(verified: `party_dead`)**. When all six die the screen shows six
  tombstones and the game returns to the Castle with an empty party **(verified: `gameover`)**.

## Open questions
- Hit chance, damage formulas, the Run success rate; what Calfo and Disarm do on a chest.
