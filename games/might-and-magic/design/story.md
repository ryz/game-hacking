# Might and Magic (NES) - story and ending

## Overview
The hero arrives in Sorpigal ("Welcome to our town Sorpigal.", "Be careful! This town is quite dangerous...")
**(verified: `sorpigal_welcome`)**. Rumours and messages hint at the plot: the King is in seclusion, the true King
Alamar is imprisoned "by a demonic alien being" who rules in his place and must be confronted with the Eye of
Goros; the Inner Sanctum is said to be a myth **(ROM text)**. The quest ends in the Astral Plane, where five gates
open and the Data Keeper of the Inner Sanctum offers "transfer to another World" **(verified: ending shots)**.

## 1. The Astral Plane
- Five squares announce "Loud voice: You've opened the First (... Fifth) gate!" **(verified, event scan of the
  Astral Plane)**.
- A door with "a small slot" and a square where the voice says "You are not yet worthy for transfer. Return after
  defeating the ..." guard the way **(verified, event scan)**.

## 2. The Inner Sanctum (ending)
"The metallic room is dimly lit by a pulsating white glow!" - "In a serene voice, the Data Keeper says: Welcome to
your Inner Sanctum. You are given the opportunity for transfer to another World. Return now to the Inn of Sorpigal
for rest and celebration, then continue on to your new assignment at the Gates to Another World... +500,000 exp
for your accomplishment!" - "A metallic panel slides open, revealing..." and the party stands in Sorpigal again
**(verified: `ending_metallic_room` ... `ending_panel`; reached by warping onto the square from `@vets`)**.
- The ending square itself checks nothing: it gives the text and 500,000 experience to whoever stands there
  **(ROM code + verified)**; the quest conditions sit on the way to it (the "not worthy" square, the slot door)
  **(inferred)**. See [findings.md](findings.md).

## Open questions
- What the "not worthy" square tests (the hero's quest bytes tested so far did not change it).
- The fight with the impostor king in Castle Alamar (not captured).
