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
