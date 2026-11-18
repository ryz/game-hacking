# Sorpigal - the first town

## Overview
Every new and pre-made character starts at the Inn of Sorpigal **(verified; manual)**. The town is one map of 16
by 16 squares of white-brick corridors and doors; its services are rooms that speak when the party steps in
facing the right way, each announced by a sign over its door **(verified: checkpoints `start`, `blacksmith`;
`tools/scan.py 0`)**. Shots: `../shots/main/` (`start_inn_door`, `sorpigal_inn_sign`, `shop_*`, `temple_services`, `market_food`, `tavern_menu`, `train_*`, `leprechaun`, `statue_lore`).

## 1. Services
| Place | Where (x east, y north) | What it offers |
|---|---|---|
| The Inn of Sorpigal | (8,3) | sign in: saves the party and returns to the character list **(verified)** |
| B and B Blacksmiths | (6,5) | buy weapons, armor, miscellaneous items; sell an item **(verified)** |
| Eulards Fine Foods | (10,5) | "all you can eat" for 5 gold each **(verified: prompt)** |
| Temple Moonshadow | (4,1) | restore health, uncurse items, restore alignment, make a donation of 100 gold **(verified: menu; the first three showed no price for a healthy character)** |
| Otto's Training | (13,11) | training for the next level: 25 gold for level 2 **(verified)** |
| Ye Olde Hogge Tavern | (11,14) | have a drink, tip the bartender, listen for rumors **(verified: menu)** |
| Leprechaun | (11,3) | sends the party to a town of its choice for 1 gem **(verified: text)** |
| Stairs down | (14,0) | a dark level below the town **(verified)** |
| Passage outside | (12,0) | the wilderness **(verified)** |
| Statues | eight squares | a line of lore each when searched **(verified: one read)** |
| Jail | door at (6,10) | sign "JAIL, KEEP OUT!" **(verified)** |

## 2. Blacksmith prices (gold)
Weapons: Dagger 5, Hand Axe 10, Short Sword 20, Sling 10, Crossbow 50, Staff 30. Armor: Small Shield 10, Padded
Armor 10, Leather Armor 20, Scale Armor 50, Ring Mail 100, Chain Mail 200. Miscellaneous: Torch 2, Rope & Hooks
10, Garlic 5, Magic Herbs 50, Might Potion 200, Scroll of Fire 300 **(verified: `shop_weapons`, `shop_armor`,
`shop_misc` routes; items the shopper cannot use are marked with "-")**. Short Sword and Leather Armor raised a
Knight's armor class from 1 to 3 **(verified)**.

## 3. What a party starts with
A created character: level 1, age 18, no gold, 10 food, a Club in the backpack **(verified: RYZ)**. The six
pre-made characters: 60 experience, 18 food, a Club equipped (the Archer and the Robber also a Sling, the Knight a
Small Shield and 200 gold) **(verified on their profiles)**.

## 4. A first fight
The room at (3,6), behind a locked door that a Robber can pick, holds a fight: four Poltergeists or four Vampire
Bats in two visits (three Poltergeists in another). Three Poltergeists were worth 75 experience per survivor,
four Vampire Bats 83; neither left anything to find **(verified)**.

## 5. Seen in the capture run
A drink at the tavern costs 1 gold **(verified: gold 1833 to 1832)**. The market answers a paid meal with
"THANK YOU, COME AGAIN!" **(verified)**. A leprechaun asked for a town by a party without gems puts it at (8,5)
inside Sorpigal instead **(RAM: read from the town's program; the scout saw the result)**. The town has two more
event squares than the scout listed, (5,8) and (5,15); they were not visited.

## Open questions
- Prices of temple services for a wounded or cursed character; what a drink, a tip and rumors do.
- What the statues say (only one was read) and whether they matter.
- ~~The two event squares at (1,0) and (8,1)~~: they do not exist (a reading error in the survey tool, fixed).
- What is at (5,8) and (5,15).
