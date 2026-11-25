# Wolfenstein 3D (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Bosses ignore a teleported player until shot
**Behavior:** with the player poked next to Otto Giftmacher, Hitler or Dr. Schabbs (debug teleport, `TP:`),
the boss stood still for 60+ frames in plain view; one burst of fire woke it (routes of `boss_otto`,
`boss_hitler`, `boss_schabbs`). Hans Grosse, reached by walking and opening his door, woke at once (`boss_hans`).
**Intended:** unclear; a normal player always arrives through a door, which connects the areas.
**Confidence:** (verified) the behaviour; (inferred) the cause: enemies only look for a player in an area
connected to theirs, and the connection is updated when doors open, not when the player is moved.
**Impact:** none in normal play; matters for debug set-ups.

## "You Win!" shows 00:00 total time after a debug warp
**Behavior:** E1 won after starting on floor 1 and warping (Tab+W) to floor 9: total time 00:00, all averages
0% (`victory_win`).
**Intended:** the totals add up the tallies of finished floors; a warp skips them.
**Confidence:** (inferred).
**Impact:** none in normal play.

## No game-over screen
**Behavior:** out of lives, the game goes straight from the red death dissolve to the High Scores
(`death_fizzle`, `highscore_entry`).
**Intended:** yes.
**Confidence:** (verified).
**Impact:** none.
