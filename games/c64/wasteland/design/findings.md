# WASTELAND - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## An unconscious ranger acts again in the next round
**Behavior:** with all four rangers poked to CON 1 (`battle_radrat` route), Angela Deth shows UNC after the first
round, gets no order in the second, and is asked for orders again in the third ("Angela Deth, choose:") with CON 1,
while RYZ and Thrasher now show UNC.
**Intended:** unclear: the roster may show UNC only for rangers hit in the last round, or unconsciousness may
wear off.
**Confidence:** (verified) in one fight, with poked CON values.
**Impact:** none known for normal play; check with an unpoked party before relying on it.

## Declining a location puts the party back one square
**Behavior:** stepping onto the Ranger Center from the east and answering N puts the party back on the east
square. The two squares east of the Ranger Center are closed in by mountains, so a party there can only leave
by entering the Ranger Center and pressing Start, which puts it on the Ranger Center square, from where the
pass north is open (checkpoints `step1`, `start`, route of `highpool`).
**Intended:** probably (locations are not walked through).
**Confidence:** (verified).
**Impact:** a new player who steps east first (as the scout did) seems trapped: about 20 calls lost.
