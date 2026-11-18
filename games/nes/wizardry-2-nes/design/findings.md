# Wizardry II: Knight of Diamonds - The Second Scenario (NES, USA) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## A wiped party loses half its gold and part of its pack
**Behavior:** after the whole party died in a fight (`gameover`), RYZ's record held 1706 gold instead of 3412 and
fewer items; the status byte was 5 (dead).
**Intended:** unclear (Wizardry I keeps a lost party's belongings for a rescue).
**Confidence:** (RAM) one observation.
**Impact:** a total party kill costs gold even when the party is recovered.

## Records the game does not save again are wiped at power-on
**Behavior:** each character record carries a check value; edited records that the game itself never wrote back
(characters not in the party when Leave Game saved) were missing from the roster after loading the save.
**Intended:** protection against corrupted battery memory.
**Confidence:** (verified) with the first 04_ending export (four characters missing), fixed by starting from a save.
**Impact:** none for players; save editors must fix the check value (`../tools/roster.py`).

## The spell level keys behave unevenly
**Behavior:** in the battle spell menu Left went up one mage level per press (M1 -> M2 -> M7 after six), Right did
nothing for DEDDO on M1, while Right x4 took EBO from cleric level 1 to level 5.
**Intended:** unclear.
**Confidence:** (verified) robes fight.
**Impact:** small usability quirk.
