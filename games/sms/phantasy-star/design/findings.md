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

## Talking to townspeople not found
**Behavior:** walking into a townsperson or a robotcop (from above and from the side) does nothing, and
either button beside one opens the field menu (capture run 2026-11-19, routes from checkpoint `camineet`).
The manual only says "stop and talk to them".
**Intended:** people surely talk; the trigger (a facing rule, a moving person's position, or a timing) is
not understood yet.
**Confidence:** (verified) that these attempts fail; the intended way is open.
**Impact:** none for players; a gap for the shot set (no townsperson dialogue yet).

## Purchases have no confirmation
**Behavior:** choosing an item in a shop list buys it at once; the next line is "Thank you. Anything else?"
(`shop_bought`: BURGER, 126 -> 86 meseta).
**Intended:** probably (fast shopping).
**Confidence:** (verified)
**Impact:** a stray press spends money; the second-hand shop buys back at half price (`shop_sell_offer`).

## Special squares that show nothing
**Behavior:** the Camineet passage's floor map marks four squares with the same code as the cave's chest
squares; standing on one (row 1, column 7) and using SRCH showed nothing (RAM map at `CB00`, playbook).
**Intended:** unclear: an emptied chest, or an object that needs a condition.
**Confidence:** (RAM) for the codes, (verified) for the empty result.
**Impact:** unknown.

## Talk needs a step first (capture part 2, 2026-11-19)
**Behavior:** a push into a person from standstill does nothing; one step toward them and a second push opens
the talk (`talk_townsperson`). The earlier "cannot talk" finding is resolved: it was the approach, not a bug.

## Forced Dark Falz dodges (capture part 2)
**Behavior:** Dark Falz brought into a battle with `FIGHT:49` dodges every attack ("Darkfalz dodges ..."), and his
picture is small (`battles:dark_falz`). The real fight is set up by his chamber (floors 3B/3C); not reached.

## Warped overworld counts as a town (capture part 2)
**Behavior:** after `WARP` to a planet surface the field-menu picture and the vehicle check behave as in a town
("Using LANDROVR will do no good"); from the real overworld (`@palma`) the Land Rover works (`landrover`).
