# Digital Devil Monogatari: Megami Tensei II (Famicom, English translation patch) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Presses during typing text are ignored
**Behavior:** while a text page (the "Caution for Devil Busters" pages, battle messages) is still typing, a button
press is dropped instead of finishing the page or being queued; the next press after the page is complete works.
**Intended:** unclear (many games of the time finish the page instead).
**Confidence:** (verified) with the route of checkpoint `naming`.
**Impact:** none for a player who reads; it only matters for automated input.

## A story-point list left in the cartridge
**Behavior:** the cartridge holds a list of 50 romanised story points ("Elder in Micon" to "The Y.H.V.H"), in the
original Japanese release as well as the translation; it looks like a developer's scenario jump menu.
**Intended:** a debugging aid removed from normal play (inferred).
**Confidence:** (inferred) from the text; no way to open it has been found.
**Impact:** none in normal play.
