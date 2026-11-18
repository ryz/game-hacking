# Might and Magic: Secret of the Inner Sanctum (NES, USA) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The Inner Sanctum square has no condition of its own
**Behavior:** stepping onto Astral Plane (6,7) facing west always plays the Inner Sanctum ending and adds 500,000
experience; warping there with any party (e.g. the level 9 party of `@vets`) works (`ending_*` shots, checkpoint
`sanctum`). The neighbouring "not worthy" square refuses for the same party.
**Intended:** the gate squares and the "not worthy" square are meant to be the only way in, so the ending square
needs no test.
**Confidence:** (verified) for the ending; the reason is (inferred).
**Impact:** any way of reaching the square (a teleport spell, a map bug) finishes the game; whether the 500,000 experience
can be collected again was not tested.

## The party starts with no gold
**Behavior:** the hero and all fifteen fellows have 0 gold at the start, 20 food each (`view_vitals` before the
capture's pokes; RAM at checkpoint `party`). Nothing can be bought until the first fights pay.
**Intended:** probably (the NES version replaces the original's rolled characters).
**Confidence:** (RAM).
**Impact:** the first visit to the blacksmith is window shopping.

## Training ages the character
**Behavior:** training RYZ from level 1 to 2 raised his age from 17 to 18 (record before/after, `training_levelup`).
**Intended:** unclear (the original ages characters with time and rest).
**Confidence:** (RAM).
**Impact:** none soon; age matters for the "natural death" message ("died a natural death", ROM text).
