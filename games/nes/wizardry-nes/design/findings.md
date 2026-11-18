# Wizardry: Proving Grounds of the Mad Overlord (NES, USA) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Boltac's purchase message typo
**Behavior:** every purchase prints "* Just want you needed *" (shot `shop_bought`).
**Intended:** "Just what you needed".
**Confidence:** (verified)
**Impact:** none; text only.

## Temple "cures" the dead
**Behavior:** raising a dead character ends with "FIGHTER2 has been cured" (shot `temple_cured`).
**Intended:** probably a single shared message for every condition.
**Confidence:** (verified)
**Impact:** none.

## Anti-magic lasts until the next stairs or teleport
**Behavior:** stepping on an anti-magic square switches party spells off; only stairs, teleports and elevators
switch them back on, so the effect follows the party after it leaves the area.
**Intended:** probably an area effect.
**Confidence:** (inferred from the program)
**Impact:** casters stay silenced after crossing such an area until the floor is changed.

## Fixed fights are set up only on arrival
**Behavior:** guardians and Werdna are placed when the party arrives on a floor by stairs, elevator, chute or
teleport; a party put on a floor by other means (MALOR is a candidate, not tested) found the floor 4 guardian
room empty.
**Intended:** unclear.
**Confidence:** (verified for a direct position change; MALOR not tested)
**Impact:** possible way past guardians if a spell moves the party within a floor without the set-up.
