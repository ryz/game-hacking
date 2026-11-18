# Might and Magic (NES) - story and ending

## Overview
The hero arrives in Sorpigal ("Welcome to our town Sorpigal.", "Be careful! This town is quite dangerous...")
**(verified: `sorpigal_welcome`)**. Rumours and messages hint at the plot: the King is in seclusion, the true King
Alamar is imprisoned "by a demonic alien being" who rules in his place and must be confronted with the Eye of
Goros; the Inner Sanctum is said to be a myth **(ROM text)**. The quest ends in the Astral Plane, where five gates
open and the Data Keeper of the Inner Sanctum offers "transfer to another World" **(verified: ending shots)**.
The impostor is beaten not in a fight but by naming him in the Soul Maze **(verified: `boss_voided`)**.

## 1. The impostor king and the Soul Maze
- In the throne room of Castle Alamar "The omnipotent King Alamar speaks: Varnlings, I quest thee to find the Crypt
  of Carmenca. Away with you..." **(verified: `king_alamar`, `king_alamar_quest`)**.
- Carrying the Eye of Goros (the true king's message: "Confront him with this Eye of Goros and you shall see his
  true self") changes the scene: "You've discovered my true identity! Into the soul maze you go..." and the party
  stands in the Soul Maze **(verified: `boss_unmasked`; the item was placed in RYZ's backpack by the capture)**.
- There "A strange alien being in a shimmering silver jumpsuit" says the party must find "your captor's name hidden
  within these walls" and asks "Answer!" on the letter keyboard **(verified: `soul_maze_alien`,
  `soul_maze_riddle`)**. The answer SHELTEM gives "Imposter xx21a7-3 voided!", "You are now Rank 1 and eligible for
  transfer. Find Inner Sanctum for new assignment.", "The walls begin to fade..." and the party is back at the inn
  door of Sorpigal **(verified: `soul_maze_answer`, `boss_voided`, `rank1`)**. There is no fight: the "boss" is
  beaten by naming him **(verified)**.
- The win is kept in the save: after signing in and reloading (`saves/03_impostor_voided`), the Astral Plane square
  that said "You are not yet worthy for transfer" says "Message: My dream leads me, your dream leads you."
  **(verified: `astral_dream`)**.

## 2. The Astral Plane
- Five squares announce "Loud voice: You've opened the First (... Fifth) gate!" **(verified, event scan of the
  Astral Plane)**.
- A door with "a small slot" and a square where the voice says "You are not yet worthy for transfer. Return after
  defeating the ..." guard the way **(verified, event scan)**.

## 3. The Inner Sanctum (ending)
"The metallic room is dimly lit by a pulsating white glow!" - "In a serene voice, the Data Keeper says: Welcome to
your Inner Sanctum. You are given the opportunity for transfer to another World. Return now to the Inn of Sorpigal
for rest and celebration, then continue on to your new assignment at the Gates to Another World... +500,000 exp
for your accomplishment!" - "A metallic panel slides open, revealing..." and the party stands in Sorpigal again
**(verified: `ending_metallic_room` ... `ending_panel`; reached by warping onto the square from `@vets`)**.
- The ending square itself checks nothing: it gives the text and 500,000 experience to whoever stands there
  **(ROM code + verified)**; the quest conditions sit on the way to it (the "not worthy" square, the slot door)
  **(inferred)**. See [findings.md](findings.md).

## Open questions
- Where the "impostor voided" state is stored (not in the hero's record bytes +$61..+$64 tested).
- The legitimate way from the "worthy" square to the Inner Sanctum (the capture warped there).
