# Wizardry I (DOS) - items

Overview: the scenario has 100 items (numbers 1-100; 0 is an empty pack entry, 101 and up show "**ERR**").
Names were read on screen by putting each number into a pack in turn and opening the character sheet
(RAM; route in `../playbook.md`, "Item numbers"), so every name below is the game's own (verified on the
sheet). Names use two special letters on screen, drawn here as "Potion of" and "Scroll of" (the font has a
single glyph for each "of" form). (E)/(N) mark items limited to an alignment (verified: shown in the name).
A "#" in front of a name on the sheet marks an item the character's class cannot use (RAM: on RYZ, a
fighter, the survey showed it for the staff of Mogref, amulet of Manifo, rod of flame, dagger of speed,
dagger of thieves, garb of lords, Muramasa blade, shurikens, the statuettes, keys and the blue ribbon).
"-" before a name marks a cursed item (verified: `shop_uncurse`), "*" an equipped one (verified:
`inventory_sheet_vet`), "?" an unidentified one with its generic name (verified: `shop_identify`, "?SWORD").

## 1. Prices
Boltac's buys at the listed price and pays half when he buys from the party (verified: long sword 25 in the
stock; sale price of a potion of Dios 250 against 500 in the stock: `shop_boltac_potions`, `shop_sell`).
Boltac's stock seen (verified, `shop_boltac_buy` ... `shop_boltac_rare`): the 14 basic weapons and armours,
potions of Dios and Latumofis, scrolls of Katino, Badios and Halito, the +1 armours and shield, staff+2 and
gloves of copper; magic items beyond that are found in chests (inferred: the series rule).

## 2. Table
| # | Name | Boltac's price | Boltac pays (seen) |
|---|---|---|---|
| 1 | Long sword | 25 | - |
| 2 | Short sword | 15 | - |
| 3 | Anointed mace | 30 | - |
| 4 | Anointed flail | 150 | - |
| 5 | Staff | 10 | - |
| 6 | Dagger | 5 | - |
| 7 | Small shield | 20 | - |
| 8 | Large shield | 40 | - |
| 9 | Robes | 15 | - |
| 10 | Leather armor | 50 | - |
| 11 | Chain mail | 90 | - |
| 12 | Breast plate | 200 | - |
| 13 | Plate mail | 750 | - |
| 14 | Helm | 100 | - |
| 15 | Potion of Dios | 500 | 250 |
| 16 | Potion of Latumofis | 300 | - |
| 17 | Long sword+1 | - | - |
| 18 | Short sword+1 | - | - |
| 19 | Mace+1 | - | - |
| 20 | Staff of Mogref | - | - |
| 21 | Scroll of Katino | 500 | - |
| 22 | Leather+1 | 1500 | - |
| 23 | Chain mail+1 | 1500 | - |
| 24 | Plate mail+1 | - | - |
| 25 | Shield+1 | 1500 | - |
| 26 | Breast plate+1 | 1500 | - |
| 27 | Scroll of Badios | 500 | - |
| 28 | Scroll of Halito | 500 | - |
| 29 | Long sword-1 | - | - |
| 30 | Short sword-1 | - | - |
| 31 | Mace-1 | - | - |
| 32 | Staff+2 | 2500 | - |
| 33 | Slayer of dragons | - | 5000 |
| 34 | Helm+1 | - | 1500 |
| 35 | Leather-1 | - | - |
| 36 | Chain-1 | - | - |
| 37 | Breast plate-1 | - | - |
| 38 | Shield-1 | - | - |
| 39 | Amulet of jewels | - | - |
| 40 | Scroll of Badios | - | - |
| 41 | Potion of Sopic | - | - |
| 42 | Long sword+2 | - | 2000 |
| 43 | Short sword+2 | - | - |
| 44 | Mace+2 | - | - |
| 45 | Scroll of Lomilwa | - | - |
| 46 | Scroll of Dilto | - | - |
| 47 | Gloves of copper | 6000 | - |
| 48 | Leather+2 | - | - |
| 49 | Chain+2 | - | - |
| 50 | Plate mail+2 | - | 3000 |
| 51 | Shield+2 | - | 3500 |
| 52 | Helm+2 (E) | - | - |
| 53 | Potion of Dial | - | - |
| 54 | Ring of Porfic | - | - |
| 55 | Were slayer | - | - |
| 56 | Mage masher | - | - |
| 57 | Mace of poison | - | - |
| 58 | Staff of Montino | - | - |
| 59 | Blade Cusinart' | - | - |
| 60 | Amulet of Manifo | - | - |
| 61 | Rod of flame | - | - |
| 62 | Chain+2 (E) | - | - |
| 63 | Plate+2 (N) | - | - |
| 64 | Shield+3 (E) | - | - |
| 65 | Amulet of Makanito | - | - |
| 66 | Helm of Malor | - | - |
| 67 | Scroll of Badial | - | - |
| 68 | Short sword-2 | - | - |
| 69 | Dagger+2 | - | - |
| 70 | Mace-2 | - | - |
| 71 | Staff-2 | - | - |
| 72 | Dagger of speed | - | - |
| 73 | Robe of curses | - | 4000 |
| 74 | Leather-2 | - | - |
| 75 | Chain-2 | - | - |
| 76 | Breast plate-2 | - | - |
| 77 | Shield-2 | - | - |
| 78 | Helm of curses | - | - |
| 79 | Breast plate+2 | - | - |
| 80 | Gloves of silver | - | - |
| 81 | Sword+3 (E) | - | - |
| 82 | S-sword+3 (E) | - | - |
| 83 | Dagger of thieves | - | - |
| 84 | Breast plate+3 | - | - |
| 85 | Garb of lords | - | - |
| 86 | Muramasa blade! | - | - |
| 87 | Shurikens | - | - |
| 88 | Cold chain mail | - | - |
| 89 | Plate+3 (E) | - | - |
| 90 | Shield+3 | - | - |
| 91 | Ring of healing | - | - |
| 92 | Priests ring | - | - |
| 93 | Ring of death! | - | - |
| 94 | Amulet of Werdna | - | - |
| 95 | Statue of bear | - | - |
| 96 | Statue of frog | - | - |
| 97 | Key of bronze | - | - |
| 98 | Key of silver | - | - |
| 99 | Key of gold | - | - |
| 100 | Blue ribbon | - | - |

## Open questions
- What each magic item does in use (the spell of a potion or scroll is its name; rings, rods and amulets
  untested).
- The full list of what Boltac stocks after the party sells him items (stock counts are not shown).
