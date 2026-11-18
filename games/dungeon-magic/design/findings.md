# Dungeon Magic: Sword of the Elements (NES, USA) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Floor 92 guardian ignores normal blows
**Behavior:** the guardian standing on the arrival square of floor 92 (lower world) has 182 HP and hits for
about 62 per blow; with its HP poked to 1, a sword blow from a level-11 hero left it at 1 (route: checkpoint
`boss92`, `poke:00DB=01,a`).
**Intended:** it presumably needs an elemental sword or a spell to be harmed (story gate).
**Confidence:** (RAM) - the poke shows the blow did nothing; the condition that makes it vulnerable is unknown.
**Impact:** arriving at floor 92 too early is death within a few seconds.

## Monsters strike from out of view
**Behavior:** a monster on a side square can hit the hero (floor 81: 58 to 51 HP) while nothing is shown in the
view and Fight is selected automatically.
**Intended:** probably intended (real-time combat), but the player cannot see the attacker without turning.
**Confidence:** (verified) (capture route to `battle_monster`).
**Impact:** turn toward the attacker; standing still in a corridor junction is dangerous.
