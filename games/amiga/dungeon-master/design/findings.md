# Dungeon Master - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Formation cells are fixed to the compass, not to the party
**Behavior:** each champion stands on one of four cells named by compass corner (north-west .. south-west); a
turn of the party rotates every champion's cell. When the party's facing was changed in memory without a turn,
the champions kept their cells: facing west, the two casters stood in front, took every blow of a Screamer
group, and the fighters' attacks never landed (RAM: champion cells and health; checkpoint `saved` with the warp
`WARP` vs `GO`, 2026-11-20).
**Intended:** yes; the game always turns the cells with the party.
**Confidence:** (RAM) for the cell layout; (verified) for the effect.
**Impact:** none in normal play; for tools: change the facing only with the game's own turns (macro `GO`).

## Lord Chaos escapes a FUSE unless every neighbouring square is closed, the party's own included
**Behavior:** the Firestaff's FUSE on Lord Chaos made him vanish (he moved away) with walls on three sides
of his square and the party on the fourth; it succeeded and started the ending once the party's own square
was a wall as well (verified, level 13, macro `FUSE`, shots `boss_chaos_fused` .. `ending_champions`). He also
moves while boxed in: from (15,0) to (15,2) past the party in about 100 frames (RAM).
**Intended:** the manual's way is to trap him in fluxcages before fusing; a square holding a fluxcage counts
as closed (inferred). That the party's square counts as a way out is probably how the code treats any open
square next to him (inferred).
**Confidence:** (verified) for what happened; (inferred) for the rule.
**Impact:** the player must cage all sides, including the one he stands on or faces from, before fusing.

## One blow can kill the first Mummy
**Behavior:** in the start set RYZ's first BASH did 21 damage and the Mummy behind the east gate of level 2
crumbled at once (verified: start set `30_bash_hit`).
**Intended:** probably; early creatures are weak against a barbarian.
**Confidence:** (verified)
**Impact:** the first fight is easy with Halk reincarnated in front.
