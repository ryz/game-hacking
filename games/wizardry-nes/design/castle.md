# Wizardry (NES) - the castle: characters, inn, shop, temple

## Overview
Everything outside the maze happens in menus: the Training Grounds make characters, Gilgamesh's Tavern forms
the party, the Adventurer's Inn heals and raises levels, Boltac's Trading Post buys and sells, the Temple of
Cant cures characters left dead or helpless, and Edge of Town leads to the maze or saves (Leave Game).

## 1. Making a character (Training Grounds)
- Order: name (on-screen keyboard), "Create this Character?", race (Human, Elf, Dwarf, Gnome, Hobbit),
  alignment (Good, Neutral, Evil), bonus points, class, "Keep this Character?" **(verified: shots
  `training_confirm` .. `training_class`)**.
- Each race starts from fixed scores; a Human starts at Strength 8, I.Q. 8, Piety 5, Vitality 8, Agility 8,
  Luck 9 **(verified: `training_bonus`)**. A random number of bonus points (7 in that shot) is spread with
  Left/Right; the game only accepts the character once every point is used **(verified)**.
- The class list beside the scores shows the classes the current scores allow and updates as points are spent
  **(verified: `training_stats`)**; an Elf with I.Q. 15 and Piety 14 may become Mage, Cleric or Wizard
  **(verified: `training_class`)**. The US release calls the Priest "Cleric" and the Bishop "Wizard"
  **(verified)**.
- New characters start at level 1 with some gold (119 to 166 seen) and age 14-16 **(verified: Inspect)**.

## 2. Adventurer's Inn
- Rooms: The Stables (free), A Cot 10, Economy rooms 50, Merchant suites 200, The Royal suite 500 gold per week
  **(verified: `inn_rooms`)**.
- Levels are gained only here: a character with enough experience who rests is told "You made the next
  Level!", each score may rise or fall by one and hit points rise **(verified: `inn_levelup`; a Fighter with
  1083 E.P. reached level 2, gained 1 hit point and lost a point of Piety)**.
- A character with full hit points rested in a Cot and kept all his gold **(verified)**.

## 3. Boltac's Trading Post
- Menu: Buy, Sell, Uncurse, Identify, Pool Gold, Leave **(verified: `shop_boltac`)**.
- Opening stock and prices: Long sword 25, Short sword 15, Anointed mace 30, Anointed flail 150, Staff 10,
  Dagger 5, Small shield 20, Large shield 40, Robes 15, Leather armor 50, Chain mail 90, Breast plate 200,
  Plate mail 750, Helm 100, potion of Curing 500 (the list scrolls on) **(verified: `shop_buy`, `shop_armor`)**.
- Selling pays half the price (Long sword 12, Large shield 20) **(verified: `shop_sell`)**.

## 4. Temple of Cant
- Lists the roster characters outside the party who are dead, paralyzed or ashed, with the donation: at level 1,
  250 for the dead, 100 for paralysis, 500 for ashes **(verified: `temple_cant`)**. The donation is paid by a
  party member ("Who will tithe?"); then "MURMUR - CHANT - PRAY - INVOKE" and the result **(verified:
  `temple_cured`)**. With nobody to help the Temple does not open **(verified)**.

## 5. Spell books
- Mage spells, 21 in 7 levels: Halito Mogref Katino Dumapic / Dilto Sopic / Mahalito Molito / Morlis Dalto
  Lahalito / Mamorlis Makanito Madalto / Lakanito Zilwan Masopic Haman / Malor Mahaman Tiltowait **(verified:
  `spellbook_mage`)**.
- Cleric spells, 29 in 7 levels: Kalki Dios Badios Milwa Porfic / Matu Calfo Manifo Montino / Lomilwa Dialko
  Latumapic Bamatu / Dial Badial Latumofis Maporfic / Dialma Badialma Litokan Kandi Di Badi / Lorto Madi Mabadi
  Loktofeit / Malikto Kadorto **(verified: `spellbook_cleric`)**.
- Spell points are counted per spell level (shown as 9/8/6/4/3/2/1) **(verified: `inspect_mage`)**.
- A new Mage knows Halito and Katino, a new Cleric Kalki and Dios **(RAM)**.

## 6. Saving
- Edge of Town > Leave Game writes the roster to the cartridge and asks the player to switch off while holding
  Reset **(verified: `save_leave`)**.

## Open questions
- Identify and Uncurse prices (no unidentified item was found in time).
- Inn healing per week and prices of hit point recovery; ageing per stay.
