# World: Daedalus 8F and the town of Micom

## Overview
Play starts on 8F of the labyrinth Daedalus, which contains the town of Micom: townspeople, a sage who gives
passwords, a healer, a weapon/armour shop and the Heretic who fuses demons, all within a few squares of the
start. A guard south-east of the start warns before the stairs down to 7F. The floor is a 32 x 32 grid of
squares; the event map with coordinates is in `../playbook.md` ("Floor 8F event map").

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
- Tyrant Minotaur waits on 8F itself (square 31,10), not deeper down **(verified: `boss_minotaur`)**.

## 3. Battles and rewards
- A won battle: "Terran Gnome was defeated.", then "10 EXP gained. 53 Makka obtained." **(verified:
  `battle_rewards`)**; a Gnome hit for 4 points of damage **(verified: `battle_attack`)**.
- Nakajima's Stats page shows "EXP n Pts.", Yumiko's "Next Level: n Pts." (20 at level 1) **(verified:
  `status_nakajima`, `status_yumiko`)**.

## Open questions
- How levels are gained (EXP 2990 and a won battle did not raise Nakajima's level).
- The rooms behind "You couldn't enter!" doors, the elevator destinations, the town of Bien.
