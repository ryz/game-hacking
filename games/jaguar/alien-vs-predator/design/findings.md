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
**Intended:** settled 2026-11-28 (round 2): a Marine stands half a cell west of the Alien's start cell
(actor table, kind 2 at 23.9,19.5; player at 24.5,19.3 facing south) and shoots it in the back; on sublevel 4
two Marines stand next to the arrival cell. Turning west shows him (`alien_marine_enemy`, `alien_marine_fires`).
**Confidence:** (verified) for the loss and the Marine, (RAM) for the positions.
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

## Bite and tail are invisible
**Behavior:** the Alien's claw (A) is drawn as a swipe; bite (B) and tail (C) show nothing in the frames after the
press (preview every 2 frames), though the claw-tail-claw combo lowers a Marine's energy by 29 of 50.
**Intended:** probably (the jaw and tail have no first-person sprite).
**Confidence:** (verified) frames, (RAM) energy.
**Impact:** the player cannot see whether a tail strike landed.

## The Predator's health reserve is empty at the start
**Behavior:** keypad 5 at the Predator start with energy poked to 1024 gave no energy back (energy kept falling
under Marine fire).
**Intended:** yes if the reserve fills only from medkits and food (source).
**Confidence:** (RAM).

## A blade kill of a Marine earns no honor
**Behavior:** a Marine killed with the wrist blade while the Predator was visible left the honor points at 0
(`predator_marine_killed`); an Alien killed with the shoulder cannon gives 5000.
**Intended:** unclear (the manual's honor table is unreadable in the scan).
**Confidence:** (RAM).
