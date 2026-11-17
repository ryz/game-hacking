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

## YES/NO box covers the Pokémon's name when learning a move
**Behavior:** at "Delete an older move to make room for STUN SPORE?" the YES/NO box is drawn over the battle HUD
and cuts BUTTERFREE's name to "BUTT" and the HP numbers to "49" **(verified: Brock route, frame before
learn_move_forget)**.
**Intended:** probably accepted: the box reuses a fixed position.
**Confidence:** verified (cosmetic).
**Impact:** none on play.

## Evolution waits for the end of the battle
**Behavior:** a Pokémon that reaches its evolution level mid-battle keeps fighting in its old form; the
evolution runs after all post-battle text (here after the Gym Leader's badge speech) **(verified: evolution_start)**.
**Intended:** yes (design).
**Confidence:** verified.
**Impact:** the evolved form's stats only apply from the next battle.

## "SOMEONE's PC" until Bill is met
**Behavior:** the Pokémon Center PC menu says "SOMEONE's PC" until the event of meeting Bill; then "BILL's PC"
**(RAM: met-Bill event set by poke -> BILL's PC, pc_menu)**.
**Intended:** yes (story).
**Confidence:** verified through memory.
**Impact:** none.

## Halving money on a blackout rounds down
**Behavior:** 48215 -> 24107 after a field blackout (blackout shot route).
**Intended:** yes (half the money).
**Confidence:** (RAM).
**Impact:** none beyond the loss.
