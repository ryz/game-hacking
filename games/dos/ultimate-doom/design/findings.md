# The Ultimate Doom (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Teleported player: missiles burst at the muzzle
**Behavior:** after the player's position is written straight into memory (the `TP` macro), rockets and BFG
balls fired at the E2M8 Cyberdemon burst right in front of the launcher, as if something invisible stood
there (preview of `LEVEL:2:8,ARMS,5,TP:...` with `ctrl:8`; the old `boss_cyber_rocket` shot showed it and was
dropped). Walking the same spot with no clipping instead of teleporting, the rockets fly on and burst at the
Cyberdemon.
**Intended:** not a game behaviour: the poke skips the game's own unlinking of the player from its old map
block, which leaves a stale entry behind (consistent with the teleport caveat in the playbook).
**Confidence:** (inferred) from the frames; the game's code was not traced.
**Impact:** none for players; for capture, fire only after walking, never right after a `TP`.

## Cyberdemon and Spider Mastermind took no damage in the routes tried
**Behavior:** on E2M8 and E3M8 (Hurt me plenty, `ARMS`, walked into place with no clipping) 40 chaingun
bullets, three rockets and seven BFG balls visibly reached the Cyberdemon and the Spider Mastermind, but their
health in memory stayed 4000 and 3000 and neither reacted; a written lower health (40) did not let them die
either. On E1M8 the same tools killed the Barons of Hell.
**Intended:** unclear; the bosses can certainly be killed in the game (source), so this is most likely a
capture-side problem (a state left by the no-clipping walk, or the monster reader of `dnav.py` finding a copy
rather than the live monster).
**Confidence:** (RAM) for the unchanged values; cause open.
**Impact:** the E2 and E3 end texts were not reached this run.

## Monsters kill each other in a crowd
**Behavior:** in a fist-only fight on E1M3 against a room of shotgun guys and zombiemen (no god mode) the kill
count reached 5 while the fist could have killed at most one or two (route `face_f6` in the capture plan).
**Intended:** yes: monsters hit by another monster's attack turn on it (source: id's released code).
**Confidence:** (inferred) from the kill count.
**Impact:** crowds of hitscan monsters thin themselves out.
