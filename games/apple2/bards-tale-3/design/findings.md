# The Bard's Tale III: Thief of Fate - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Buildings and gates need K, not the forward key
**Behavior:** `i` (forward) bumps against a gate or building square and nothing happens; `k` or Return enters
(Skara Brae gate from the wilderness, storage building, Review Board, temple, shrine; start set
`skara_gate`, `skara_inside`). Verified 2026-11-21.
**Intended:** probably the BT1 "kick" key kept for doors.
**Confidence:** (verified).
**Impact:** a new player stands in front of the city gate without a hint.

## A level-1 party meets a Nefastmaster in the first catacombs corridor
**Behavior:** the honest RYZ party walking east then north from the catacombs arrival met 1 Nefastmaster at
square 6,1 (a door; byte 4 of the square has bit 3 set there and on its neighbours): it hit RYZ for 16 of 26 HP
and killed EBO in four rounds; running away worked on the second try (start set `encounter` .. `fled`).
**Intended:** unclear (random or fixed at the door).
**Confidence:** (verified) for the fight, (inferred) for the square flag.
**Impact:** the first dungeon is deadly for a fresh party; the shrine asks 900 gold to raise a level-1 member.

## Saving gives no confirmation
**Behavior:** `s`, Yes: the drive runs and the view returns with no message (start `save_prompt`, `saved`);
restoring at power-on proves the save (`restored`).
**Confidence:** (verified).

## The previous owner's endgame save is edited
**Behavior:** the character disk's saved game has a Vampire Lord with 9999/9999 HP and AC -42 in slot 1 next to
level 30-60 characters (`tarjan_2`): edited with a character editor, not grown in play.
**Confidence:** (inferred from the round 9999). **Impact:** the endgame shots show this party.
