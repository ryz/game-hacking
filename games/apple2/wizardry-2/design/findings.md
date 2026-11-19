# Wizardry II: The Knight of Diamonds - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## A guardian stays away while its piece is in the roster
**Behavior:** on this copy the scenario disk came with four characters of an earlier player who hold four of the
five pieces. With them in the roster every guardian square gave an ordinary random group; after deleting them
in the Training Grounds the same routes met the five guardians (checkpoints `guard1` to `guard5`).
**Intended:** the pieces are unique: a second copy cannot be won while one exists.
**Confidence:** (verified) for the set of four; (inferred) that each guardian looks only for its own piece (the
gauntlets' guardian was not tried with only THUG present).
**Impact:** a used scenario disk can make the quest look broken; the fix is to delete or strip the holders.

## The Training Grounds disband the party
**Behavior:** entering the Training Grounds and coming back leaves the Castle's party list empty.
**Intended:** unclear (the training grounds work on the roster).
**Confidence:** (verified) once, `@edge,t`, roster, leave.
**Impact:** the party must be formed again in the Tavern.

## Space does not leave the title
**Behavior:** Return goes on to the copyright menu, space does not (tried at frames 1200 and 1900 after power-on, and once by hand).
**Intended:** unclear; Wizardry I takes any key.
**Confidence:** (verified).
**Impact:** none beyond a moment of doubt.
