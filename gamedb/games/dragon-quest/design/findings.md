# Dragon Quest (Famicom, English translation patch) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The password shortens the hero's name
**Behavior:** a hero named ryz who enters his own Return Spell comes back as "r56": the second and third
letters turn into digits. Route: `@password_entry` + `PW_LATE` without `NAME_FIX`.
**Intended:** the password keeps each name symbol only within the 64 symbols of the password grid; in the
Japanese game the same happens to name symbols outside that set. In the English patch the lower-case letters
r to z fall outside it. Probably an accepted side effect of the translation.
**Confidence:** (verified)
**Impact:** cosmetic; a player should pick a name from the symbols of the password grid (capitals, digits, a-q).

## Level and stats come from experience only when a password is entered
**Behavior:** raising experience from 0 to 34218 leaves the hero at level 1 with 15 HP; the king then quotes a
meaningless "next level after 31325". After entering the password he is level 21 with 149 HP.
**Intended:** experience only changes through battles, where the level-up check runs; the direct change is
outside normal play.
**Confidence:** (RAM)
**Impact:** none in normal play; matters for cataloguing.
