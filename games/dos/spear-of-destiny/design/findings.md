# Spear of Destiny (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## You Win! averages divide by 14, not by the 20 floor records
**Behavior:** the victory screen sums the kill, secret and treasure percentages of all 20 per-floor records
(RAM 45796, 10 bytes each) and divides by 14; the total time sums all 20. With 20 records filled at about
70% each the screen read KILL 99%; with only the 14 regular floors filled (bosses and secret floors zero) it
read the true averages 67/39/60% (`victory_win`, macro `SODRATIOS`).
**Intended:** the 14 regular floors are the ones with a tally; the boss and secret floors are meant to stay
zero, so dividing by 14 gives the average over the floors a player always plays.
**Confidence:** (RAM) poked records, screen read.
**Impact:** none in normal play; a tool that fills the records must leave floors 5, 10, 16, 18, 19, 20 at zero.

## The Angel of Death takes few hits from a chain gun hold
**Behavior:** 240 frames of chain-gun fire at about 6 tiles took the Angel from 1594 to 1158 hit points
(RAM 477EA); many bullets miss while it moves or throws fireballs. Its full 1650 needs well over 1000 frames of
fire, more than 120 short presses gave.
**Intended:** yes, the last boss is a long fight.
**Confidence:** (RAM).
**Impact:** the capture pokes its hit points to 64 and finishes it with real fire (`angel_hit`).

## Lives counter unchanged after a death in the Trans Grosse fight
**Behavior:** in `TGFIGHT,TF*N` (started with `tedlevel 4`, MLI used) B.J. dies at cycle 19 and the floor
restarts at cycle 28 with pistol, 8 ammo and 100% health, but LIVES still reads 3 (RAM 45462 and status bar,
`face_28`).
**Intended:** unclear; Wolfenstein's code takes a life on every death. Possibly the debug/tedlevel start.
**Confidence:** (RAM), cause (inferred) not checked.
**Impact:** none for a player starting normally (not checked there).

## Floor 21 shows "18" on the status bar
**Behavior:** the Angel of Death's floor displays FLOOR 18 (`env_f21`, `spectre`, `angel_of_death`).
**Intended:** the designers hide the floor count of the finale (or reuse the Death Knight's number).
**Confidence:** (verified).
**Impact:** the bar cannot be used to tell floor 18 from 21.
