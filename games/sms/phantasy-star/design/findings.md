# Phantasy Star - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Message windows cover the status box
**Behavior:** while a message window is open in the field (SRCH, SAVE), it overlaps the right half of the
name/HP/MP box, so Alis's "HP 16" reads "HP 1" (routes in `../shots.txt`: `menu_search`, `save_slots`).
**Intended:** the layout shares the bottom of the screen; probably accepted, not a bug.
**Confidence:** (verified)
**Impact:** none in play; a reader of a screenshot may misread HP.

## Title cursor and early input
**Behavior:** inputs on the title are ignored until about four seconds after power-on; `up` then moves the cursor
from START to CONTINUE, while one `down` press did not (`work/scout/phantasy-star/t17`). CONTINUE without a valid
save starts a new game.
**Intended:** unclear.
**Confidence:** (verified) for `up`; `down` seen once.
**Impact:** none for players; automated routes use `up`.
