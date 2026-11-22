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

## Inventory clicks below the first item line are not taken
**Behavior:** in the inventory, a click on the item picture of the first slot (record +F4, line 3, pointer y
004B) works for Use, Examine, Prepare and Give; clicks on line 4 (pointer y 59, 5B, 5D, 63, 69, 6F tried, from
cached and live states) never answered (capture round 3, 2026-11-22).
**Likely cause:** unknown (hit test per line, or the emulator's pointer poke); not traced.
**Confidence:** (verified) for the symptom.
**Impact:** routes poke the item they need into the first slot.

## Healing never finds its target
**Behavior:** Healing (w), prepared by Rinakles, asks "Cast spell on whom?" and then says "Spell has failed!"
(5 magic points spent) whatever portrait is clicked; eight wait and Character variants gave the same result.
**Likely cause:** the target picker (code C6A0) waits for an input event (975E) and maps the pointer to a zone
(5E48, minus 10 = hero); the poked pointer and click are evidently not seen as a portrait zone. Not traced.
**Confidence:** (verified) symptom, (RAM) code path.
**Impact:** no successful Healing shot; Light (no target) succeeds.

## A Levelmap item with suffix 00,00 draws garbage
**Behavior:** Examine on a poked Levelmap (item 52, shown "Levelmap 00,00") in the dungeon fills the screen
with striped grey, beige and red garbage (round 3).
**Likely cause:** the suffix names a level whose map is not loaded.
**Confidence:** (verified) symptom.
**Impact:** none; a real Levelmap (found in a dungeon) is open.
