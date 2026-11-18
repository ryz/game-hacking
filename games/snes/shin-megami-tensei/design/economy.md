# Economy: yen, shops and what they sell

## Overview
The hero starts with nothing and receives 10000 yen from his mother before leaving home **(verified:
`../shots/main/shin-megami-tensei_snes_jp_dialogue_home_mother.png`)**. In the opening hours of 199X the only places to spend it are the shops of
the Kichijoji arcade. Shops are rooms entered from the arcade corridor: stepping through the door opens the
shopkeeper's greeting, then a menu; leaving puts the hero back in the corridor facing away from the door
**(verified: checkpoint `knifeshop`)**. Yen and Magnetite are shown in the corner window while a shop or the
command menu is open **(verified: `../shots/main/shin-megami-tensei_snes_jp_shop_shop_menu.png`)**.

## 1. Shop menus
| Shop | Menu | Tag |
|---|---|---|
| Knife shop (arcade) | Buy, Sell, Equip, Status, Sort your items, Leave the shop | **(verified: `../shots/main/shin-megami-tensei_snes_jp_shop_shop_menu.png`)** |
| Antique shop (arcade) | Purchase Items, Sell, Leave the store | **(verified: checkpoint `armed`, then the door north of square 6,2)** |

Buying asks "<item> will cost <price>. Do you want to buy it?" with Yes preselected, takes the yen at once and
then asks "Is there something else I can get for you?" **(verified: bought one Attack Knife, 10000 -> 5000
yen)**. A bought weapon goes to the item list unequipped; it is equipped from the shop's Equip entry or from
ITEM, Equip in the command menu **(verified: checkpoint `armed`)**.

## 2. Price lists
Knife shop, Kichijoji arcade **(verified: `../shots/main/shin-megami-tensei_snes_jp_shop_shop_buy.png`)**. The symbols after each name on the
buy list say who can use the item (male, female) and an alignment letter; all five show "A".

| Item (as far as the list shows the name) | Price (yen) | Users shown |
|---|---|---|
| Attack Knife | 5000 | male, female |
| Machete | 6500 | male, female |
| Tonfa | 7000 | male |
| Replica S... (name cut off by the symbols) | 9000 | male, female |
| Unnamed K...ta (name cut off) | 12000 | male |

Antique shop, Kichijoji arcade **(verified: `../shots/main/shin-megami-tensei_snes_jp_shop_shop_antique.png`)**:

| Item | Price (yen) |
|---|---|
| Hanging Scroll | 10000 |
| Ink Painting | 12800 |
| Stone Lantern | 25000 |
| Golden Buddha | 43000 |

With 10000 yen the hero can afford one of the three cheaper knives, or the Hanging Scroll, not both
**(computed)**.

## 3. Things that cost nothing
The cafe Master puts the coffee for the hero's mother on a tab: "I'll bring it to your house and you can pay me
then" **(verified: `../shots/main/shin-megami-tensei_snes_jp_dialogue_cafe_master.png` and the two pages after it)**. The clinic doctor only talks
at this point of the story; no healing menu was offered **(verified: `../shots/main/shin-megami-tensei_snes_jp_dialogue_clinic_doctor.png`)**.

## Open questions
- What the antiques are for (sold on for profit, gifts for demons, a later trade?): none was bought.
- Sell prices; whether the knife shop's stock changes later; where guns, armour and healing are sold.
- The full names of the fourth and fifth knife-shop items.
