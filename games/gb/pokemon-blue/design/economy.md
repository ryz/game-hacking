# Economy - Pokémon Blue Version

## Overview
Money (shown with the ₽ sign) starts at 3000 **(verified: checkpoint `start`)**, is earned by beating
trainers and spent at Poké Marts on balls and medicine **(verified: mart_buy)**. Losing all Pokémon halves it
**(RAM)**. Healing at Pokémon Centers is free **(verified: pokecenter_heal)**.

## 1. Income
- Prize money = the trainer class's base value x the level of their last Pokémon **(source)**; observed: rival
  (first battle, L5) 175, Lorelei (last Pokémon L56) 5544 **(verified)**.

## 2. Losses
- Blackout: money halved, rounded down (48215 -> 24107) **(RAM: blackout route)**.

## 3. Shops
- A clerk offers BUY / SELL / QUIT with the money shown **(verified: mart_buy route)**.
- Indigo Plateau Mart: ULTRA BALL 1200, GREAT BALL 600, FULL RESTORE 3000, MAX POTION 2500, FULL HEAL 600
  **(verified: mart_buy)**, plus REVIVE and MAX REPEL **(source: pret marts)**.

## 4. Fees, prizes and coins
- Safari Zone entry 500 **(verified)**. Gym Leaders and the Champion pay 99 x level of their last Pokémon
  (Brock 1386, Champion 6435) **(verified, computed)**.
- Game Corner: slots need the COIN CASE **(source)**; bet 1-3 coins per spin ("Bet how many coins?" x3/x2/x1);
  three cherries on the bottom line paid 8 coins on a 3-coin bet **(verified: slots_bet, slots_spin, slots_win)**.
  Slot odds not measured.
- PC item storage: ryz's PC holds items separately from the bag (WITHDRAW / DEPOSIT / TOSS) **(verified:
  pc_items)**; a new game starts with one POTION stored **(RAM)**.

## Open questions
- Selling price (half the buying price per source) not checked; other towns' Marts not visited.
