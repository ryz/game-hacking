# Pokémon Blue Version - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Tile-by-tile tapping avoids wild encounters (emulator observation)
**Behavior:** On Route 1 grass, 18 single-tile steps (`up:16` / `down:16`, released at the end of each step)
gave no wild battle even with the encounter rate poked to the maximum; holding the direction across several
tiles (`down:64`) started a battle at once. Seen from `lab_after_rival` + walk north (route1_grass, battle_wild).
**Intended:** encounters on every step in grass.
**Confidence:** (verified) for the observation; the cause (the check apparently runs only while the direction
is still held when a step ends) is (inferred).
**Impact:** a player tapping the D-pad step by step may meet fewer wild Pokémon; for routes here, walk with
long holds to get encounters and tap to avoid them.

## Halving money on a blackout rounds down
**Behavior:** 48215 -> 24107 after a field blackout (blackout shot route).
**Intended:** yes (half the money).
**Confidence:** (RAM).
**Impact:** none beyond the loss.
