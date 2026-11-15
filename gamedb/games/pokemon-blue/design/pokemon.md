# Pokémon - Pokémon Blue Version

## Overview
Each Pokémon has a species (Pokédex number, category, height, weight, description), a level, HP, four stats
(ATTACK, DEFENSE, SPEED, SPECIAL), one or two types, up to four moves with PP, EXP, an original trainer (OT)
and ID number **(verified: summary_stats, summary_moves, starter_preview)**. The party holds six
**(verified: party_screen)**.

## 1. Summary screen
- Page 1: picture, No., name, level, HP, STATUS (OK/PSN/SLP/FNT...), four stats, TYPE1/TYPE2, IDNo, OT
  **(verified: summary_stats)**.
- Page 2: EXP POINTS, "LEVEL UP <n> to :L<next>", the four moves with PP **(verified: summary_moves)**.

## 2. Growth
- Stats rise on level up and are shown in a box (Squirtle L5 -> L6: ATTACK 11, DEFENSE 13, SPEED 10,
  SPECIAL 12; HP 20 -> 22) **(verified: battle_levelup)**.
- EXP needed follows the species' growth group: medium fast n^3, medium slow 1.2n^3 - 15n^2 + 100n - 140,
  fast 0.8n^3, slow 1.25n^3 **(source; medium slow RAM-confirmed on Blastoise L52, summary_moves)**.
- Raichu L46 -> L47 after Lorelei: HP max 133 -> 136 **(verified)**.

## 3. Field moves
- The party sub-menu lists a Pokémon's field moves (SURF, STRENGTH for Blastoise) above STATS / SWITCH /
  CANCEL **(verified: party_submenu)**.

## 4. Status in the field
- Poison costs HP while walking; a Pokémon can faint from it ("BLASTOISE fainted!") **(verified: blackout
  route)**.

## 5. Pokédex
- CONTENTS list by number with a ball mark for owned species; SEEN / OWN totals; DATA / CRY / AREA / QUIT
  **(verified: pokedex_list)**. AREA shows the species' nests on the Kanto map (PIKACHU's NEST)
  **(verified: pokedex_area)**. Starters: Squirtle No.007 TINYTURTLE 1'08" 20.0 lb; Pidgey No.016 TINY BIRD
  1'00" 4.0 lb **(verified)**.

## 6. Learning moves and evolution
See [battle.md section 4a](battle.md) for the dialogs. Level-up stat rise measured on Butterfree L15 -> L16:
ATTACK 23 -> 24, DEFENSE 23 -> 24, SPEED 30 -> 31, SPECIAL 34 -> 36, HP 46 -> 49 **(verified: Brock route)**;
Squirtle L15 -> L16: HP 40 -> 42 **(verified)**. Evolution levels used: Squirtle 16, Butterfree learns STUN
SPORE at 16 **(source: pret learnsets; verified on screen)**.

## 7. Field moves (HMs) in use
| Move | Effect seen | Shot |
|---|---|---|
| CUT | facing a small tree: "VICTREEBEL hacked away with CUT!", the tree disappears | cut_tree (verified) |
| SURF | facing water: "ryz got on BLASTOISE!", the player sprite becomes a sea creature and moves on water | surfing (verified) |
| FLY | outdoors only: a Kanto map titled "To <TOWN>", Up/Down cycles through visited towns, A flies there | fly_map (verified) |
| FLASH | lights dark caves; usable outside battle after the BOULDERBADGE | badge text (verified), effect source |
The party sub-menu shows only the field moves the Pokémon knows (FLY for Pidgeot, SURF/STRENGTH for
Blastoise, CUT for Victreebel) **(verified)**.

## Open questions
- ~~Evolution and move learning not captured~~ captured 2026-11-15 (learn_move, evolution). Stone evolution not tested.
