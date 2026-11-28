# Alien vs Predator - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The Alien loses energy with no attacker in view
**Behavior:** as the Alien, energy falls by about 200 in the first 10 seconds in its own ship and right after
arriving on sublevels 4 and 5, with purple damage flashes and no enemy on screen (`alien_hurt`; route
`@start_alien,WARP:04,w180`).
**Intended:** unclear: an unseen enemy behind the player, or a hazard of the level.
**Confidence:** (verified) for the loss, (inferred) for the cause.
**Impact:** the Alien, which cannot heal, starts every area weaker; turn around at once.

## Acid stays where an Alien died
**Behavior:** a killed Alien leaves a yellow splash on the floor (`marine_alien_dead`); walking through the
spot later still cost the Marine energy (start set, south door of the brig office: 470 -> 452).
**Intended:** yes (acid blood, as in the films).
**Confidence:** (verified) for the splash and the loss, (inferred) that the splash causes it.
**Impact:** walk around dead Aliens.

## High score entry returns to the title, not to the table
**Behavior:** after FIRE on a new name the screen goes black and then to the title; the table with the new
name is seen only through the main menu (`highscore_ryz`). Menu presses are ignored for several seconds after
this return.
**Intended:** unclear.
**Confidence:** (verified).
**Impact:** none beyond a missing confirmation.
