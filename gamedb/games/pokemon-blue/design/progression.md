# Progression - Pokémon Blue Version

## Overview
A new game puts the player in his bedroom with no Pokémon **(verified: start_room)**. Stepping into the Route 1
grass makes Professor Oak stop him ("Hey! Wait! Don't go out!") and lead him to the lab **(verified:
oak_wait)**, where he picks one of three Poké Balls (Charmander, Squirtle, Bulbasaur) **(verified:
oak_lab_choose)**; the rival takes the one strong against it (Bulbasaur after Squirtle) and challenges him
on the way out **(verified: battle_rival_first)**. Eight badges, then the Elite Four and Champion
**(source; Elite Four room verified: elite_four_room)**.

## 1. Opening sequence (verified)
1. Title -> NEW GAME -> Oak's speech (Nidorino shown as the example Pokémon) -> player name (BLUE/GARY/JOHN or
   own) -> rival name (RED/ASH/JACK or own) -> bedroom **(verified: oak_intro .. naming_rival)**.
2. Route 1 edge: Oak appears, walks the player to the lab **(verified)**.
3. Lab: examining a ball shows that Pokémon's Pokédex page, then "So! You want the water POKéMON,
   SQUIRTLE?" YES/NO, "ryz received a SQUIRTLE!", nickname question **(verified: starter_preview,
   starter_received)**.
4. Leaving: the rival battle (L5 vs L5) triggers on the row south of the bookshelves; win or lose, the story
   continues and the party is healed **(verified; losing path from source)**.

## 2. Elite Four
- Lorelei, first of the Elite Four, ice-floored room, party of five (Dewgong L54, Cloyster L53, Slowbro,
  Jynx, Lapras L56) **(verified: elite_four, battle frames)**.

## 3. Gyms (Brock verified)
- Pewter Gym: one trainer on the way, Brock at the top (Geodude L12, Onix L14). Winning gives the
  BOULDERBADGE, 1386 money and TM34 **(verified: pewter_gym, gym_brock, badge_received)**.

## 4. Champion and ending (verified)
1. The Champion's room: walking in, the player is moved up to the rival, who speaks, then battles
   (Pidgeot L61 ... Rhydon L61 ... Venusaur L65 with a Bulbasaur rival) **(verified: champion)**.
2. Defeat line "NO! That can't be! You beat my best!", then Prof. Oak enters ("So, you won! Congratulations!")
   and scolds the rival, and leads the player to the Hall of Fame **(verified: champion_defeated, oak_congrats)**.
3. Hall of Fame: Oak's speech, each party Pokémon shown in turn (name, level, types, "HALL OF FAME" label), then
   the player's record: PLAY TIME, money, Pokédex Seen/Owned, and Oak's Pokédex rating by owned count
   ("Go fish for some marine POKéMON!" at 71 owned) **(verified: hall_of_fame, hall_of_fame_trainer,
   dex_rating)**.
4. The game saves itself; credits (DIRECTOR, PROGRAMMERS, MUSIC, PRODUCERS ... "THE END"); CONTINUE afterwards
   starts in Pallet Town in front of the player's house **(verified: credits, the_end, save 06_hall_of_fame)**.

## Open questions
- Badge effects (obedience levels, stat boosts, HM use outside battle) not tested.
- ~~Champion and Hall of Fame not reached~~ reached 2026-11-15 by warp + script poke (see playbook).
- Badge effects on obedience and stats not measured.
