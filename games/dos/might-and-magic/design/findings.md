# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Training makes a character a year older
**Behavior:** RYZ, age 18, trained from level 1 to 2 and the profile then showed age 19 (`train_levelup`, `profile_level2`).
**Intended:** probably intended (training takes time); the manual was not checked for it.
**Confidence:** (verified)
**Impact:** levels cost lifetime as well as gold.

## A leprechaun without payment still moves the party
**Behavior:** asking the Sorpigal leprechaun for a town with no gems in the party ends with the party on another square of Sorpigal, (8,5), in front of the blacksmith's sign.
**Intended:** unclear; looks like a deliberate "nothing happens, off you go".
**Confidence:** (RAM) for the cause, (verified) for the result (scout run).
**Impact:** none beyond confusion.

## The same fight square holds different monsters
**Behavior:** stepping on a fight square a moment earlier or later changes the group: Snakes or Strangling Vines on one forest square of sector C-2, Poltergeists or Vampire Bats in the room at Sorpigal (3,6) (`outdoors_vines`, `encounter_poltergeists`).
**Intended:** yes, random groups from the area's list.
**Confidence:** (verified)
**Impact:** a party can re-enter for an easier group.

## The ending does not check where the party came from
**Behavior:** the Inner Sanctum square only looks at one mark on each character (impostor defeated). A level 1 party placed on the square with that mark set gets the full ending and 500,000 experience each (`ending_sanctum`).
**Intended:** the door with the Key Card slot is the real gate; the square itself trusts it.
**Confidence:** (verified) with a memory edit, (RAM) for the condition.
**Impact:** none in normal play.
