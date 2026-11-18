# Might and Magic (NES) - towns and services

## Overview
Each of the five towns (Sorpigal, Portsmith, Algary, Dusk, Erliquin) is a 16x16 walled maze of streets with doors
into the services: inn, blacksmith, market (food), temple, training hall, guild, tavern, plus signs, stone
reliefs, a leprechaun who teleports between towns and a gate keeper **(verified in Sorpigal, every event square
stepped into: [maps.md](maps.md) section 5)**. A service starts with a prompt ("Would you like to sign in?",
"A man speaks: Can I help you?"), answered Yes/No with Up and A; the service menu then lists the party on the
right **(verified: `inn_signin`, `blacksmith_greet`, `blacksmith_menu`)**. Many other town squares start a fight;
Sorpigal is anti-magic at least where the first fight was tried ("Magic doesn't work here.") **(verified, route of
`battle_hit` + Cast)**.

## 1. Inn
- "Would you like to sign in?" - Yes saves the game ("Push A button and save your adventure.") and opens Member
  (Add, Remove, View, Quit), Rest, View, Cancel **(verified: `inn_save`, `inn_menu`)**.
- Fellows are hired with Member > Add from the roster of fifteen; a fellow living in another town shows "Another
  town" and cannot be added **(verified, scout)**.

## 2. Blacksmith ("B and B Blacksmiths" in Sorpigal)
- Menu Buy, Sell, View, Cancel; Buy asks for a category Misc, Weapon, Armor, then an item, then "It's N Gold OK?",
  then Who? **(verified: `blacksmith_menu`, `blacksmith_weapons`, `blacksmith_price`)**.
- Sorpigal stock: weapons Dagger, Hand Axe, Short Sword, Sling, Crossbow, Staff; armour Small Shield, Padded Armor,
  Leather Armor, Scale Armor, Ring Mail, Chain Mail **(verified: `blacksmith_weapons`, `blacksmith_armor`)**.
- Prices seen: Short Sword 20 gold, Scale Armor 50 gold **(verified: `blacksmith_price`; scale armour price from the
  route of `view_backpack`)**.
- Bought items go to the buyer's backpack; they are equipped from Camp (section 7) **(verified: `view_backpack`,
  `view_equipped`)**.

## 3. Market ("Eulard's Fine Foods")
- "Would you like to buy some Food?" -> Market: Buy, View, Cancel; "Food price is 5 Gold. Will you pay?"
  **(verified: `food_shop`, `food_price`)**. Each character starts with 20 food **(verified: `view_vitals`)**.

## 4. Temple ("House")
- "Do you seek our help?" -> Help, Donate, View, Cancel; Help offers Revive, Align and more per member
  **(verified: `temple_greet`, `temple`; prices not looked at)**.

## 5. Training ("Otto's Training" in Sorpigal)
- "Do you require training?" -> Who? -> either "RYZ, you need 1500 Exp for next Level" or "Service costs 40 Gold
  OK?" and "Welcome to Level 2!" **(verified: `training_need`, `training_levelup`; level 1 -> 2 for a Knight costs
  1500 experience and 40 gold)**.
- Level 1 -> 2 raised RYZ's hit points from 5 to 17 and his age from 17 to 18 **(RAM, record before/after training)**.

## 6. Guild and tavern
- Guild master: "Need help?" -> Change (class; "You must abandon all your experience..."), Rename, View
  **(verified: `guild`, `guild_change`)**. Rename is the game's own way to rename fellows **(inferred from the menu;
  not used: the capture renamed by pokes)**.
- Tavern: "Step up to the counter?" -> Drink, Tip, Rumors, View, Cancel; a rumour: "All Portals are connected."
  **(verified: `tavern`, `tavern_rumor`)**. Other rumours in the ROM: "The King is in seclusion.", "The Inner Sanctum
  is a myth.", "The canine has the Key.", "No rumors today." **(ROM text)**.

## 7. Camp, equipment and the character sheet
- Camp asks "Rest here?"; answering No opens the item menu Equip, Remove, Trade, Drop, Share **(verified:
  `camp_rest`, `camp_items`)**. Equip: Who? -> backpack item -> "WHERE?" (one of six equipment slots)
  **(verified, route of `view_equipped`)**.
- Use (exploration menu) uses the special power of an equipped or carried item ("No special power")
  **(verified)**.
- View pages through five screens: race/class/age/level/alignment/experience/condition; the seven statistics and
  armour class; HP, MP with spell level, gems, gold, food; equipped items; backpack (6 each) **(verified:
  `view_profile`, `view_stats`, `view_vitals`, `view_equipped`, `view_backpack`)**.
- A "+" before the class abbreviation in the party list marks a member in a bad condition (paralysed, poisoned...)
  **(verified: `chest_found`, RYZ paralysed in the fight before)**.

## 8. Leprechaun and gates
- The leprechaun: "Only 1 Gem you lose... I'll send you to the town you choose." Pay him? **(verified:
  `leprechaun`)**.
- Sorpigal's gate keeper: "You are too weak to use City gate!" **(verified, event scan)**.

## Open questions
- Prices of the other items, temple services, training costs at higher levels.
- Which town squares are fixed fights and which are random encounters.
