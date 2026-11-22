# Dragonflight - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The party starts without weapons
**Behavior:** every hero starts with gold 100, food 100 and a torch only; in a fight the attack icon answers
"Has no longrange weapon!" / "No weapon for close combat." (`inventory_items`, `battle_no_weapon`).
**Intended:** yes: the player is meant to buy weapons in Pegana first (inferred).
**Confidence:** (verified) for the inventory and the message; (inferred) for the intent.
**Impact:** a new player who leaves town at once cannot fight the first ambush.

## Command icons drawn one hero late in combat
**Behavior:** after an order the icon grid often still shows the previous hero's options (a sword appears
while the next hero is not next to an enemy, and the reverse) (live play, `battle_close`).
**Intended:** unclear; probably the grid should change with the hero whose order is due.
**Confidence:** (verified) in live play, several rounds.
**Impact:** clicks hit an icon the current hero does not have ("Has no longrange weapon!").

## English text slips
**Behavior:** "mortually wounded", "embaressed", "To far away to heal", "Dispell undead" in the game text
(RAM; "mortually" seen on screen in live play).
**Intended:** "mortally", "embarrassed", "Too far", "Dispel".
**Confidence:** (RAM).
**Impact:** none.

## A poked bow does not count as a longrange weapon
**Behavior:** with the Bow (item 0x0D) poked into Andariel's weapon word 3612 before the fight, the shooting
hand still answers "Has no longrange weapon!" (live play, 2026-11-22, capture round 2).
**Likely cause:** arrows or a second weapon slot are needed; not checked.
**Impact:** none in the shots; open question for a ranged attack shot.

## Opponent hit points not found
**Behavior:** a snake took 27, 24, 21 and more damage from Bladus's sword and stayed; no RAM value fell by the
damage dealt (chip and slow RAM searched across a hit). Victory was not reached (capture round 2).
