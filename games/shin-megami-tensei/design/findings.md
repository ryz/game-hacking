# Shin Megami Tensei (Super Famicom, English translation patch) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Two-row cursor jumps in vertical lists
**Behavior:** in the stat allocation list and the room menu, holding Up or Down for 8 frames (about 0.13 s)
moves the cursor two rows; a 4-frame tap moves one (`@dream` stat screens, `@start`).
**Intended:** fast key repeat for long lists; unclear whether the original cartridge on a console feels the same.
**Confidence:** (verified) in this emulator only.
**Impact:** none for a human; automated routes must tap for 4 frames.

## Cosmetic slips of the English translation
**Behavior:** the facing word in the 3D window sometimes keeps a trailing underscore ("EAST_", "SOUTH_") after
a step or turn; the Chaos hero's prompt reads "Divide 18 points among his paramenters." (`@dream` onward,
`@apartment`).
**Intended:** "EAST", "parameters".
**Confidence:** (verified); belongs to the translation patch, the frames replay identically.
**Impact:** visible in screenshots of the 3D view; pick a frame without the underscore where it matters.

## Derived values are not refreshed when a stat changes outside a level-up
**Behavior:** after raising the hero's stats and level through memory, Defense, Evade, M.Power and M.Effect on
the status screen keep their old numbers while "Next" follows the new level (`@lv23`).
**Intended:** the game stores these values and recalculates them only at set moments.
**Confidence:** (RAM).
**Impact:** none in normal play; matters for cheated status screens.

## Long item names collide with the user symbols on shop lists
**Behavior:** on the knife shop's buy list the male/female symbols and the alignment letter are drawn at a
fixed column on top of the item name, so names longer than about nine letters are cut: "Attack Kn..eA",
"Replica S..rA", "Unnamed K.taA" (`../shots/main/shop_buy.png`). The equip list and the status screen cut the
same weapon to "Attack K" (`../shots/main/equipment.png`).
**Intended:** the Japanese names fit their fields; the English names are longer than the space the list gives.
**Confidence:** (verified); belongs to the translation patch, the frames replay identically.
**Impact:** two of five weapon names cannot be read in full in the shop; the purchase prompt shows the full
name ("Attack Knife will cost 5000 yen").

## Steps after a door are sometimes not taken
**Behavior:** in the arcade a forward press given 60 frames after the previous step is ignored on some squares
(seen leaving squares 5,5 and 5,2 and after a room pushes the hero back out); an extra second of waiting
before the next press makes it register (checkpoint `armed`, then the walk to the cafe).
**Intended:** the game is still finishing the door or scene transition and does not buffer input.
**Confidence:** (verified) in this emulator, by position read from memory after each press.
**Impact:** none for a human; automated routes need a pause after doors and room scenes.

## The second dream can stay locked after the coffee errand
After the cafe errand and the mother's evening talk, "Go to sleep" only says "ryz went to sleep..." and the
next morning repeats the first morning's lines (police sirens) without the second dream **(verified:
checkpoint `home_room`, then `morning2`)**. The dream needs a day-1 story event that the run here never
triggered (cafe, park police and roadblock were all seen); setting it by hand plays the dream normally
**(RAM: checkpoint `dream2`)**. Either an event was missed (likely: one of the arcade's people not talked to)
or the event can be skipped by the order of visits, which would be a progression trap.
