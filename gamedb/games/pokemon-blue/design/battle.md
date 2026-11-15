# Battle - Pokémon Blue Version

## Overview
Battles are turn-based, one Pokémon on each side. Each turn the player picks FIGHT (one of up to four moves),
PKMN (switch), ITEM or RUN from a 2x2 menu **(verified: battle_menu)**; moves show their type and remaining
PP while being chosen **(verified: battle_moves)**. Hits can be critical ("Critical hit!") and type matchups
are announced ("It's super effective!", "It's not very effective...") **(verified: battle_super_effective,
route of battle_levelup)**. Wild Pokémon can be caught with Poké Balls; trainers' Pokémon cannot **(source)**.
Winning gives EXP to the Pokémon that fought, and trainer wins pay prize money **(verified)**. When every
party Pokémon has fainted the player blacks out, loses half the money and wakes up at the last Pokémon Center
**(verified: blackout)**.

## 1. Battle start
- Wild battle: "Wild PIDGEY appeared!" with the player's back sprite and a row of party balls **(verified:
  battle_wild)**. Wild battles start on grass tiles with a per-step chance set by the area: Route 1 uses 25 out
  of 256 per step (about 10%) **(RAM: route1 grass rate, checkpoint `route1_pidgey_ball`)**.
- Trainer battle: "RED wants to fight!" with both sides' party balls (filled = healthy, empty slot = no
  Pokémon) **(verified: battle_rival_first, elite_four - Lorelei shows five of six slots filled)**.

## 2. Turn order and moves
- The faster Pokémon usually moves first: the rival's Bulbasaur (base speed 45) acted before the player's
  Squirtle (base 43) at level 5 **(verified: first rival battle)**; exact tie-breaks not measured.
- Moves have PP; one use costs 1 PP (TACKLE 35/35 -> 34/35 after one use) **(verified: rival battle frames)**.
- Measured damage: Raichu L45 THUNDERBOLT on Lorelei's Dewgong L54: 169 -> 43 HP (126 damage), "super
  effective" **(RAM: lorelei_tbolt)**; a critical TACKLE from a L5 Bulbasaur did 4 to a L5 Squirtle, normal
  TACKLEs 3 **(RAM: first rival battle)**.
- An enemy can use healing moves: Lorelei's Dewgong used REST and fell asleep (SLP shown next to its name)
  **(verified: blackout attempt from `lorelei_battle`)**.

## 3. Catching
- ITEM in a wild battle lists the balls; "ryz used POKé BALL!", the ball flies at the target, the Pokémon
  vanishes into it and the ball wobbles **(verified: battle_ball_throw)**.
- A failed catch: "Aww! It appeared to be caught!" and the Pokémon comes back out **(verified:
  battle_catch_fail)**. Success: "All right! PIDGEY was caught!" **(verified: battle_catch)**.
- The result is random: the same throw at a half-health Pidgey failed or succeeded depending on the frame of
  the press **(verified: waits 0-25 frames before the throw, `route1_pidgey_ball`)**.
- After a catch: "New POKéDEX data will be added for PIDGEY!", its Pokédex page, then the nickname question
  **(verified: pokedex_entry)**.

## 4. Winning
- EXP: the rival's L5 Bulbasaur gave 67 EXP **(verified)**; prize money 175 (= 35 per level of the last
  Pokémon) **(verified, computed)**. Lorelei paid 5544 (= 99 x level 56) **(verified, computed)**.
- Level up: "SQUIRTLE grew to level 6!" with a box of the new ATTACK / DEFENSE / SPEED / SPECIAL; HP max rose
  20 -> 22 **(verified: battle_levelup)**.
- EXP for the next level follows the species' growth group; medium-slow: 1.2 n^3 - 15 n^2 + 100 n - 140 for
  level n **(source; RAM-confirmed: Blastoise 134665 EXP shows 7012 to L53, summary_moves)**.
- After the first rival battle the game heals the party (Squirtle back to 22/22 on Route 1) **(verified)**.

## 5. Losing (blackout)
- "ryz is out of useable POKéMON!" then "ryz blacked out!" **(verified: blackout)**. Also happens in the field
  when the last Pokémon faints from poison (1 HP lost per few steps) **(verified)**.
- Money halves, rounded down: 48215 -> 24107 **(RAM)**; the player reappears at the last healing place
  (Indigo Plateau outside) **(RAM)**.

## 6. Battle style
- SHIFT (default) asks "Will ryz change POKéMON?" after each enemy faints; SET does not **(source;
  verified: options screen)**.

## Open questions
- Exact damage formula and random spread not measured beyond the samples above.
- Catch formula not measured (needs many throws per HP level).
- Enemy trainer AI: Lorelei's Cloyster/Dewgong spent many turns without damaging a 1-HP Blastoise
  (stat moves, misses, REST); not analysed.
