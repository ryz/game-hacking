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

## ~~Cyberdemon and Spider Mastermind took no damage~~: the marine stood inside a pillar
**Behavior:** the earlier runs (rockets, BFG balls and bullets visibly "reaching" the E2M8 Cyberdemon and the
E3M8 Spider Mastermind, health in memory unchanged at 4000/3000) were not a game quirk. The no-clipping walk of
those routes ended at -969 72 on E2M8 (and -1000 100 in another try), inside a solid square column
(one-sided lines from -1216 to -960 x 64 to 320). Its walls face outward, so from inside the view looks open,
but every rocket exploded on the column's inner wall (rocket mobj stopped at -1191 288 with the Cyberdemon 290
units further on) and every bullet hit it. Checked 2026-11-25: the thinker list (walked from the player's
mobj) and the blockmap held exactly one live Cyberdemon, no ghosts; no memory word anywhere fell on impact.
Walked to a clear spot (`dplan.autospot`, no clipping off before firing), the same weapons killed both bosses
and the E4M8 Spider: Cyberdemon 4000 -> 3033 -> ... -> -76 with 9 BFG balls and 4 rockets, E3M8 Spider 3000
-> 2032 -> 643 -> 0 with 4 BFG balls (shots `boss_cyber_dies`, `boss_spider_dies`, `boss_spider_e4_dies`).
The coordinator's teleport-ghost hypothesis was not needed for this; the health poke to 40 "not killing" was
the same cause (nothing reached the boss). The muzzle bursts after `TP` (entry above) may well be the same
thing: a spot inside a solid structure.
**Intended:** the game is fine; a capture trap: with no clipping the marine can stop inside solid map
structures, and `wadmap.py --at` reports the surrounding sector, not the column.
**Confidence:** (RAM) for the rocket's stopping point, the lines and the health values; (verified) kills.
**Impact:** for capture: end a no-clipping walk on a spot checked for nearby one-sided lines (`dplan.autospot`)
and test one shot's health drop before a long fight.

## Boss deaths end E2 and E3 at once; E4M8 needs the exit
**Behavior:** when the Cyberdemon's (E2M8) or the Spider Mastermind's (E3M8) death animation ends, the episode
end text starts without a tally (verified, `ending_e2`, `ending_e3`). On E4M8 the Spider's death lowers the
column sector tagged 666 that walls in an octagon of W1 exit lines around -2368 32; walking in (with clipping:
crossing lines with no clipping on triggers nothing) ends the episode (verified, `ending_e4`). The end texts are
fully typed about 3000 frames after they start; a picture follows ~500 frames later.
**Intended:** yes (id's boss specials).
**Confidence:** (verified).
**Impact:** E4M8 cannot be finished by killing the Spider alone.

## Monsters kill each other in a crowd
**Behavior:** in a fist-only fight on E1M3 against a room of shotgun guys and zombiemen (no god mode) the kill
count reached 5 while the fist could have killed at most one or two (route `face_f6` in the capture plan).
**Intended:** yes: monsters hit by another monster's attack turn on it (source: id's released code).
**Confidence:** (inferred) from the kill count.
**Impact:** crowds of hitscan monsters thin themselves out.
