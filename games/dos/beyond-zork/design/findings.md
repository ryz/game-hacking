# Beyond Zork: The Coconut of Quendor (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Scroll words change from game to game
**Behavior:** the crinkly scroll in the Wine Cellar reads "The word Watkin is inscribed across the top" in one
route and "Blarn" in another (`inventory_scroll_blarn`; the scout-built route with `examine scroll` first gave
Watkin). The hint ("something to do with refreshment") stays the same.
**Intended:** yes: the names of magic items are randomised per game, so the player must learn them by use.
**Confidence:** (verified) two routes, two words.
**Impact:** walkthroughs cannot name scrolls; identification is part of play.

## Combat monitor bar stays after the fight
**Behavior:** after a monster is beaten or flees, the Endurance bar stays in the room window in the next
rooms (`gameplay_eyes`, `gameplay_gasses`) and its percentage is not updated after the attributes change
(it showed 23% while STATUS showed 47%, after a RAM change of the attributes).
**Intended:** probably the bar is redrawn only during a fight.
**Confidence:** (verified) for the bar staying; (RAM) for the stale number, which needed a poke to see.
**Impact:** cosmetic.

## UNDO only for deaths outside combat
**Behavior:** a death by the rat-ant offers RESTORE, RESTART or QUIT (`gameover_ratant`); a death in the
dark offers UNDO as well (`gameover_grue`).
**Intended:** yes, the manual says UNDO is not available in combat.
**Confidence:** (verified).
**Impact:** a lost fight costs the progress since the last SAVE.

## Movement in darkness is a gamble
**Behavior:** the Darkness beyond the Wine Cellar kills on some moves ("You stumble blindly ahead, straight
into the jaws of a deadly presence") and lets you "inch forward one step at a time" on others, depending on
the route (`gameover_grue`).
**Intended:** yes (the classic grue).
**Confidence:** (verified) both outcomes seen.
**Impact:** without a light the cellar is deadly; the door locks behind you (`system_cellar_locked`).
