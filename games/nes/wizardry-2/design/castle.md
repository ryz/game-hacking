# Wizardry: Knight of Diamonds (NES) - the castle of Llylgamyn

## Overview
The castle is a set of menus: Gilgamesh's Tavern (form the party), the Adventurer's Inn (rest, heal, level up),
Boltac's Trading Post (buy, sell, uncurse, identify), the Temple of Cant (cure the dead, paralysed and ashed) and
the Edge of Town (Training Grounds, the maze, restart an OUT party, Leave Game = save) **(verified: `castle_menu`,
`edge_of_town`)**. Everything works like the NES Wizardry I (`../../wizardry/design/castle.md`), with the
differences below.

## 1. Training Grounds
- Create: name (up to 8 letters, keyboard of 4 rows) -> 'Create this character?' -> race (Human, Elf, Dwarf, Gnome,
  Hobbit) -> alignment (Good, Neutral, Evil) -> bonus points on the six scores -> class from the eligible list ->
  'Keep this character?' **(verified: `training_name` to `training_class`)**.
- Human base scores 8 8 5 8 8 9 with 7 bonus points in the shown roll **(verified: `training_bonus`)**.
- Class list: all eight classes are listed in fixed rows, only the eligible ones are written: a Human with
  Strength 15, I.Q. 11, Piety 10, Vitality 14, Agility 10 sees Fighter, Mage and Samurai **(verified:
  `training_class`)**.
- There is no import of Wizardry I characters; six level 1 characters (FIGHTER1, FIGHTER2, CLERIC1, THIEF1,
  MAGE1, MAGE2) come with a fresh battery **(verified: `tavern_roster`)**.

## 2. Adventurer's Inn
- Rooms: Stables free, Cot 10, Economy 50, Merchant suites 200, Royal suite 500 G.P. per week **(verified:
  `inn_rooms`)**.
- Resting in a room checks the level: with enough E.P. the character 'made the next level' and each score may go
  up or down (seen: Piety, Agility, Luck up, Vitality down, 1 hit point) **(verified: `inn_levelup`; the changes
  differ between runs, so they are random)**. Without enough E.P.: 'You need 288548 more E.P. to make the next
  level.' **(verified)**.
- A level 12 fighter with 401,236 E.P. made level 13 (Wizardry's fighter table: 400,075 for level 13)
  **(verified + source table)**. A cot stay of RYZ (110/112 hit points) cost 20 G.P. **(RAM: 3412 -> 3392)**.

## 3. Boltac's Trading Post
- Menu: Buy, Sell, Uncurse, Identify, Pool Gold, Leave **(verified)**.
- Stock in shop order: Long sword 25, Short sword 15, Anointed mace 30, Anointed flail 150, Staff 10, Dagger 5,
  Buckler 20, Shield 40, Robes 15, Leather armor 50, Chain mail 90, Breast plate 200, Plate mail 750, Helm 100,
  Potion of curing 500, Potion of neutralizing 300, Blade of biting 15000, Rod of iron 3000 (#), Scroll of sleep
  500, Padded leather, Shiny chain, Sturdy plate, Iron shield, Body armor 1500 each, Scroll of pain 500, Scroll of
  fire 500, Studly staff 2500, Potion of glass 1500, Gloves of copper 6000 **(verified: `shop_buy`, `shop_stock`)**.
- A purchase answers '* Just what you needed *' (the NES Wizardry I spelled it 'Just want you needed')
  **(verified: `shop_bought`)**.

## 4. Temple of Cant
- The temple lists only characters who need help; with none it returns to the castle at once **(verified)**.
- Prices for level 1 characters: Dead 250, P-lyze (paralysed) 100, Ashes 500 G.P. **(verified: `temple`)**;
  'MURMUR - CHANT - WISH - INVOKE', then 'FIGHTER2 is cured' **(verified: `temple_cured`)**.

## 5. Leave Game
- Edge of Town > Leave Game saves the roster and shows '* CAUTION * Turn Power switch off while pressing
  Reset-switch' and '[A] to more Wizardry' **(verified: `save_leave`; saves 02-04 reload)**.
- Only characters the game writes back keep their changes over a power cycle (each record carries a check
  value; see findings) **(RAM)**.

## Open questions
- Inn prices per week versus hit points healed (one cot stay measured).
- Uncurse and Identify prices not looked at.
