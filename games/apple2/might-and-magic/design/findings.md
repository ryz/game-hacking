# Might and Magic Book One: The Secret of the Inner Sanctum - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Search after a fight finds a chest
**Behavior:** after the fixed fight at Sorpigal (3,6) was won, Search on that square showed an Iron Chest; opened by
the one member still standing it gave 3 gold a share and a Large Shield to RYZ, who was down **(verified: shots
`search_after_fight`, `chest_opened`)**.
**Intended:** yes, the manual's way to collect treasure **(source: DOS design reference, combat)**.
**Confidence:** verified here; the DOS run never found treasure by searching.
**Impact:** searching after every fight matters, also when most of the party is down.

## The Astral Plane sends the party home from one square
**Behavior:** arriving on square (10,10) of the Astral Plane, the game asks for disk D and at once for disk B and
puts the party in Sorpigal **(verified with the warp shortcut; RAM)**.
**Intended:** unknown; the square is not a normal way in.
**Confidence:** verified for the shortcut only.
**Impact:** none in normal play.

