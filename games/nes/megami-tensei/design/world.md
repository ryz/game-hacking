# World: Daedalus 8F and the town of Micom

## Overview
Play starts on 8F of the labyrinth Daedalus, which contains the town of Micom: townspeople, a sage who gives
passwords, a healer, a weapon/armour shop and the Heretic who fuses demons, all within a few squares of the
start. A guard south-east of the start warns before the stairs down to 7F. 8F is a block of 8 x 8 squares of
the labyrinth's one 128 x 64 grid; all floors are drawn in [maps.md](maps.md) **(computed from the ROM)**.

## 1. Micom services
- Sage: "I am known as the sage here in Micom Town. Let me tell you the password." then shows a password of
  32 characters in four groups of five plus two (characters 0-9 and A-Y without I and O) **(verified: `sage`,
  `sage_password`)**.
- Password screen: 40 slots; Right moves the character cursor, A writes the character; Start submits. The
  sage's password restored Makka, MAG, Jewel and the demon in the Comp, and restarted at the 8F start square
  after the pyramid scene; EXP showed 0 afterwards **(verified: `password_filled`, checkpoint
  `password_loaded`)**.
- Shop: "Welcome! What do you seek?" Weapons / Armor; weapons Jack Knife 80, Nunchuks 130, Dagger 195,
  Scorpion Whip 280 Makka; "Who'll take it?" picks the hero; buying equips at once ("Nakajima equipped the
  Dagger."); buying a new weapon offers to sell the old one for half its price (Dagger 97) **(verified:
  `shop`, `shop_weapons`, `status_nakajima`)**.
- Healer: "Who needs treatment?" with a fee per party member, N/A at full health **(verified: `healer`)**.

## 2. Bosses
- ~~Tyrant Minotaur waits on 8F itself~~: his square (31,10) is on 1F of the first tower; round 1 reached it by a
  position poke **(computed; verified by warp, `minotaur_down`)**. All six tyrants, what they need and what they
  drop: [maps.md](maps.md) section 2 **(verified)**.

## 3. Battles and rewards
- A won battle: "Terran Gnome was defeated.", then "10 EXP gained. 53 Makka obtained." **(verified:
  `battle_rewards`)**; a Gnome hit for 4 points of damage **(verified: `battle_attack`)**.
- Nakajima's Stats page shows "EXP n Pts.", Yumiko's "Next Level: n Pts." (20 at level 1) **(verified:
  `status_nakajima`, `status_yumiko`)**.

## 4. Levels and magic
- Both heroes share one "Next Level" counter; each won battle lowers it by the EXP gained; when it runs out
  both gain a level together **(RAM; verified: `levelup`)**. Each level gives one stat point per hero, chosen
  on a stat screen ("Determine Nakajima's stats.", A raises the highlighted stat, "Is this okay?" Yes/No)
  **(verified: `levelup_stat`)**, raises maximum HP (level 25: Nakajima 325, Yumiko 192) **(verified)** and can
  teach Yumiko a spell ("New spell learned!") **(verified: `levelup_spell`)**.
- EXP to the next level grows from 20 (level 1) by 30, 50, 80, 120 ... (level 24 -> 25 needs 2780, 25 -> 26
  3020); total EXP for level 10 is 1380, level 20 11780, level 30 41180 **(computed from the game's table)**.
- Yumiko's battle spells (Medi 2 MP, Patch 4, Bottra 5, Etna 6, Marinka 10, Clink 7, Hacke 10 at level 24)
  **(verified: `magic_list`)**; Bottra hit a Ghost for 35 points and finished it the second time
  **(verified: `magic_damage`)**. Field-only spells include Mappa, Swadona, Medical, Staruto **(verified on
  the Stats page)**.
- A summoned demon takes orders like a hero ("Nekomata's action?") and attacks on its own turn
  **(verified: `battle_orders`, `demon_attacks`)**.
- After a battle a chest may hold MAG or a Jewel ("Something's there! 5 MAG was found!") **(verified:
  `battle_mag`, `calm_gem` route)**.

## 5. The ending
Lucifer beaten: "The Dark Lord Lucifer has perished...", the two heroes on a hill as the pyramid sinks,
Izanami and Izanagi thank them and leave, then a recap of scenes from the whole journey, "PRESENTED BY namcot"
and END **(verified: `lucifer_perished` ... `the_end`)**.

## Open questions
- ~~How levels are gained~~: section 4.
- The rooms behind "You couldn't enter!" doors, the elevator destinations, the town of Bien.
