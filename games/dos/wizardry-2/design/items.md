# Wizardry II (DOS) - items

Overview: the scenario has 129 items (numbers 1-129; 0 is an empty pack entry and the item a confiscated
staff turns into, 130 and up show "**ERR**"). Names were read on screen by putting eight numbers at a time
into RYZ's pack (identified) and opening his sheet in the Tavern (`@start,poke:DDCC=0800,poke:DDCE=...,g,w120,1,w200`;
helper `work/scout/wizardry-2/itemcrop.py`, scratch), so every name is the game's own (verified, scout
2026-11-19). The font has single glyphs drawn here as "Potion of", "Scroll of" and "of" (as in the Wizardry I
table, `games/dos/wizardry/design/items.md`). (E)/(N) mark alignment-limited items (shown in the name). The
"#" column: the sheet marks the item as unusable for RYZ (a fighter). Several names repeat (114/122 Wand of
mages, 115/123 Coin of power, 120/121 Amulet of skill): different item records with the same name; what
tells them apart is not known yet. Boltac's stock and prices: section below (verified, capture 2026-11-19).

Quest items (verified in play, playbook "Game structure"): 125 Hrathnir and 126-129 KOD's helm, shield,
gauntlets, armor are the five pieces of the Knight of Diamonds' regalia (each carried by a guardian on floors
1-5, source: floor data + fights seen); 124 Staff of Gnilda is Gnilda's gift for the five.

| # | Name | # on RYZ's sheet (fighter cannot use) |
|---|---|---|
| 1 | Long sword |  |
| 2 | Short sword |  |
| 3 | Anointed mace |  |
| 4 | Anointed flail |  |
| 5 | Staff |  |
| 6 | Dagger |  |
| 7 | Small shield |  |
| 8 | Large shield |  |
| 9 | Robes |  |
| 10 | Leather armor |  |
| 11 | Chain mail |  |
| 12 | Breast plate |  |
| 13 | Plate mail |  |
| 14 | Helm |  |
| 15 | Potion of Dios |  |
| 16 | Potion of Latumofis |  |
| 17 | Long sword+1 |  |
| 18 | Short sword+1 |  |
| 19 | Mace+1 |  |
| 20 | Staff of Mogref | yes |
| 21 | Scroll of Katino |  |
| 22 | Leather+1 |  |
| 23 | Chain mail+1 |  |
| 24 | Plate mail+1 |  |
| 25 | Shield+1 |  |
| 26 | Breast plate+1 |  |
| 27 | Scroll of Badios |  |
| 28 | Scroll of Halito |  |
| 29 | Long sword-1 |  |
| 30 | Short sword-1 |  |
| 31 | Mace-1 |  |
| 32 | Staff+2 |  |
| 33 | Slayer of dragons |  |
| 34 | Helm+1 |  |
| 35 | Leather armor-1 |  |
| 36 | Chain mail-1 |  |
| 37 | Breast plate-1 |  |
| 38 | Shield-1 |  |
| 39 | Amulet of jewels |  |
| 40 | Scroll of Badios |  |
| 41 | Potion of Sopic |  |
| 42 | Long sword+2 |  |
| 43 | Short sword+2 |  |
| 44 | Mace+2 |  |
| 45 | Scroll of Lomilwa |  |
| 46 | Scroll of Dilto |  |
| 47 | Gloves of copper |  |
| 48 | Leather+2 |  |
| 49 | Chain mail+2 |  |
| 50 | Plate mail+2 |  |
| 51 | Shield+2 |  |
| 52 | Helm+2 (E) |  |
| 53 | Potion of Dial |  |
| 54 | Ring of Porfic |  |
| 55 | Were slayer |  |
| 56 | Mage masher |  |
| 57 | Mace of poison |  |
| 58 | Staff of Montino |  |
| 59 | Blade Cusinart' |  |
| 60 | Amulet of Manifo | yes |
| 61 | Rod of flame | yes |
| 62 | Chain+2 (E) |  |
| 63 | Plate+2 (N) |  |
| 64 | Shield+3 (E) |  |
| 65 | Amulet of Makanito |  |
| 66 | Helm of Malor |  |
| 67 | Scroll of Badial |  |
| 68 | Short sword-2 |  |
| 69 | Dagger+2 |  |
| 70 | Mace-2 |  |
| 71 | Staff-2 |  |
| 72 | Dagger of speed | yes |
| 73 | Robe of curses |  |
| 74 | Leather-2 |  |
| 75 | Chain-2 |  |
| 76 | Breast plate-2 |  |
| 77 | Shield-2 |  |
| 78 | Helm of curses |  |
| 79 | Breast plate+2 |  |
| 80 | Gloves of silver |  |
| 81 | Sword+3 (E) |  |
| 82 | S-sword+3 (E) |  |
| 83 | Dagger of thieves | yes |
| 84 | Breast plate+3 |  |
| 85 | Garb of lords | yes |
| 86 | Muramasa blade | yes |
| 87 | Shurikens | yes |
| 88 | Cold chain mail |  |
| 89 | Plate+3 (E) |  |
| 90 | Shield+3 |  |
| 91 | Ring of healing |  |
| 92 | Priests ring |  |
| 93 | Ring of death |  |
| 94 | Rod of raising | yes |
| 95 | Amulet of cover |  |
| 96 | Robe+3 | yes |
| 97 | Winter mittens |  |
| 98 | Magic charms | yes |
| 99 | Staff of light |  |
| 100 | Long sword+5 |  |
| 101 | Sword of swings |  |
| 102 | Priest puncher |  |
| 103 | Priest's mace | yes |
| 104 | S-sword of swings |  |
| 105 | Ring of fire | yes |
| 106 | Cursed plate+1 |  |
| 107 | Plate+5 |  |
| 108 | Staff of curing | yes |
| 109 | Ring of life | yes |
| 110 | Metamorph ring |  |
| 111 | Granite stone |  |
| 112 | Dreamer's stone |  |
| 113 | Damien stone |  |
| 114 | Wand of mages | yes |
| 115 | Coin of power |  |
| 116 | Stone of youth |  |
| 117 | Mind stone |  |
| 118 | Stone of piety |  |
| 119 | Blarney stone |  |
| 120 | Amulet of skill |  |
| 121 | Amulet of skill |  |
| 122 | Wand of mages |  |
| 123 | Coin of power |  |
| 124 | Staff of Gnilda |  |
| 125 | Hrathnir |  |
| 126 | KOD's helm |  |
| 127 | KOD's shield |  |
| 128 | KOD's gauntlets |  |
| 129 | KOD's armor |  |

## Boltac's Trading Post (verified, capture 2026-11-19: shots `shop_boltac_buy` ... `shop_boltac_rare`)
The stock is Wizardry I's starting stock, unchanged: 25 items on five pages of six (F)orward wraps round to
the start). Prices (gold): long sword 25, short sword 15, anointed mace 30, anointed flail 150, staff 10,
dagger 5, small shield 20, large shield 40, robes 15, leather armor 50, chain mail 90, breast plate 200, plate
mail 750, helm 100, potion of Dios 500, potion of Latumofis 300, scroll of Katino 500, leather+1 1500, chain
mail+1 1500, shield+1 1500, breast plate+1 1500, scroll of Badios 500, scroll of Halito 500, staff+2 2500,
gloves of copper 6000. Selling pays half (EBO's potion of Dios 250, plate mail 375, `shop_sell`). Identifying
KOD's shield costs 150,000 (`shop_identify`); uncursing the robe of curses 4,000 (`shop_uncurse`).
Usable by class (verified while equipping): priests cannot wear a helm; the bishop could not use the anointed
flail or chain mail (equipped staff, leather+1, small shield instead); a thief sees swords marked USELESS.

## The guardians' drops (verified, capture 2026-11-19, RAM item numbers in the finder's pack)
| Guardian | Floor | Found as | Item | Shot |
|---|---|---|---|---|
| Magic Armor | 1 | ARMOR | 129 KOD's armor | `boss_found_armor` |
| Magic Shield | 2 | SHIELD | 127 KOD's shield | `boss_found_shield` |
| Magic Sword | 3 | SWORD | 125 Hrathnir | `boss_found_sword` |
| Magic Helm | 4 | HELM | 126 KOD's helm | `boss_found_helm` |
| Magic Gauntlets | 5 | GAUNTLETS | 128 KOD's gauntlets | `boss_found_gauntlets` |
Worn together by RYZ (level 11 fighter): AC -18 and hit point regeneration (`inventory_kod_set`).
