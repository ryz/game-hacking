# Wizardry III: Legacy of Llylgamyn (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The orb leaves an invisible item behind
**Behavior:** surrendering the Orb of Earithin replaces it in its bearer's pack with item 1000, which has no name
and is not listed, but still counts as one of the eight pack entries (verified: `after_ending`, CUBI's pack count 1).
**Intended:** probably "remove the orb".
**Confidence:** (RAM)
**Impact:** one pack slot lost for the bearer after the ending.

## The party gets no star of its own
**Behavior:** the Queen says she gives "your party the Star of Llylgamyn", but only the six other characters chosen
afterwards get the "*" award and 150,000 E.P.; the party's records are unchanged on disk and in memory (verified:
`02_ending`).
**Intended:** unclear (the party may be meant to receive it too).
**Confidence:** (verified)
**Impact:** the bearers of the orb end without the award they were promised.

## Floor 6 refuses an all-neutral party even with a crystal
**Behavior:** a party of neutral characters carrying any crystal or the orb is sent back from floor 6 ("You are
forbidden to enter here!"), while good or evil parties with the same item enter (verified with poked parties).
**Intended:** fits L'kbreth's "neither good nor evil alone" only partly; unclear.
**Confidence:** (verified)
**Impact:** the all-neutral party that serves both halves cannot take the last step.
