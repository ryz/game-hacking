# Wizardry III: Legacy of Llylgamyn (DOS) - items

The 103 items, by the game's item number (1000 + record), as the character sheet names them (**verified**: put
into a pack eight at a time and read on the Tavern sheet). "#" before a name on the sheet marks an item the
character cannot use (RYZ, a fighter, was the reader). Prices are those of the item records (disk data) where the
shop shows them (verified for the first page of Boltac's).

## Overview
Weapons and armour from short sword (30 gold) to +2 and named blades, a few charged magic items, potions and
scrolls, and the quest items 1001-1011. Item 1000 has no name: the game puts it where the orb was taken.

## 1. Item list
| No. | Name | No. | Name | No. | Name | No. | Name |
|---|---|---|---|---|---|---|---|
| 1001 | Orb of Earithin | 1027 | Plate armor | 1053 | Bag of gems | 1079 | Breastplate+2 |
| 1002 | Neutral Crystal | 1028 | Sallet | 1054 | Wizard's staff | 1080 | Plate armor+2 |
| 1003 | Crystal of Evil | 1029 | Potion of Dios | 1055 | Flametongue | 1081 | Armet |
| 1004 | Crystal of Good | 1030 | Potion of Latumofis | 1056 | Round shield-1 | 1082 | Wargan robes |
| 1005 | Ship in Bottle | 1031 | Short sword+1 | 1057 | Cuirass-1 | 1083 | Giant's club |
| 1006 | Staff of Earth | 1032 | Broadsword+1 | 1058 | Hauberk-1 | 1084 | Blade Cusinart' |
| 1007 | Amulet of Air | 1033 | Mace+1 | 1059 | Breastplate-1 | 1085 | Shepherd crook |
| 1008 | Holy Water | 1034 | Battle axe+1 | 1060 | Plate armor-1 | 1086 | Unholy axe |
| 1009 | Rod of Fire | 1035 | Nunchaka | 1061 | Sallet-1 | 1087 | Rod of Death |
| 1010 | Gold Medallion | 1036 | Dagger+1 | 1062 | Potion of Sopic | 1088 | Gem of Exorcism |
| 1011 | Orb of Mhuuzfes (cursed) | 1037 | Scroll of Katino | 1063 | Gold ring | 1089 | Bag of emeralds |
| 1012 | Butterfly knife | 1038 | Cuirass+1 | 1064 | Salamander ring | 1090 | Bag of garnets |
| 1013 | Short sword (30) | 1039 | Hauberk+1 | 1065 | Serpent's tooth | 1091 | Blue pearl |
| 1014 | Broadsword (50) | 1040 | Breastplate+1 | 1066 | Short sword+2 | 1092 | Ruby slippers |
| 1015 | Mace (60) | 1041 | Plate armor+1 | 1067 | Broadsword+2 | 1093 | Necrology rod |
| 1016 | Staff (20) | 1042 | Heater+1 | 1068 | Battle axe+2 | 1094 | Book of Life |
| 1017 | Hand axe (30) | 1043 | Bascinet | 1069 | Ivory blade (G) | 1095 | Book of Death |
| 1018 | Battle axe (140) | 1044 | Gloves of iron | 1070 | Ebony blade (E) | 1096 | Dragon's tooth |
| 1019 | Dagger (10) | 1045 | Scroll of Badios | 1071 | Amber blade (N) | 1097 | Trollkin ring |
| 1020 | Flail (300) | 1046 | Potion of Halito | 1072 | Mace+2 | 1098 | Rabbit's foot |
| 1021 | Round shield (40) | 1047 | Short sword-1 | 1073 | Gloves of mithril | 1099 | Thief's pick |
| 1022 | Heater shield (80) | 1048 | Broadsword-1 | 1074 | Amulet of Dialko | 1100 | Book of Demons |
| 1023 | Mage's robes (30) | 1049 | Mace-1 | 1075 | Cuirass+2 | 1101 | Butterfly knife |
| 1024 | Cuirass | 1050 | Dagger-1 | 1076 | Heater+2 | 1102 | Gold tiara |
| 1025 | Hauberk | 1051 | Battle axe-1 | 1077 | Displacer robes | 1103 | Mantis gloves |
| 1026 | Breastplate | 1052 | Margaux's flail | 1078 | Hauberk+2 | | |
On screen "OF" is one ligature glyph ("ORB♡EARITHIN"), potions start with "&", scrolls with a scroll sign.

## 2. Quest items
| Item | Got from | Used for |
|---|---|---|
| Crystal of Evil | the floor 4 guardian (good party) (verified) | entry to floor 6 (verified) |
| Crystal of Good | the floor 5 guardian (neutral party) (verified) | entry to floor 6 (verified) |
| Neutral Crystal | both crystals invoked by one good or evil bearer (E)quip, own alignment's crystal) (verified 2026-11-19) | entry to floor 6; becomes the Orb at the statue search square (17,17) (verified) |
| Orb of Earithin | the statue (17,17) search with the Neutral Crystal (verified) | the ending, when brought to the Castle (verified) |
| Orb of Mhuuzfes | the statue (13,2) search with the Neutral Crystal (verified) | a cursed decoy (record: cursed, AC -10) (disk data) |
| Staff of Earth | the floor 2 desk (7,1) search (verified) | not known |
| Amulet of Air, Holy Water, Rod of Fire | records cast spells (disk data); Gold Medallion and Holy Water from the floor 3 swaps (verified) | not known |

## 3. Records, special powers and curses (disk data, 2026-11-19)
Item records on WIZ3.DSK are Wizardry I's without the two names: 23 words (OBJTYPE, ALIGN, CURSED, SPECIAL,
CHANGETO, CHGCHANC, PRICE x3, BOLTACXX, SPELLPWR, CLASSUSE, HEALPTS, ...) at SCENARIO.DATA block 48 (0x23A00),
22 records per 1,024 bytes.
- Special powers: Crystal of Good SPECIAL 28, Crystal of Evil 29, Orb of Earithin 30 (type 5, special item);
  the Neutral Crystal and the Ship in Bottle have none. E)quip offers to invoke them (verified, findings).
  Staff of Earth, Amulet of Air, Holy Water and Rod of Fire are type 6 with a spell power (29, 10, 35, 7), price
  25000 and a change chance of 5 after use (disk data).
- Cursed (CURSED -1): the Butterfly knife 1012 (150000), all "-1" items 1047-1052 and 1056-1061 (1000/2000),
  Wargan robes 1082, Giant's club 1083, Gem of Exorcism 1088 (armour, 12000), Bag of emeralds 1089, Butterfly
  knife 1101 (500000); the Orb of Mhuuzfes 1011 has SPECIAL 9 and AC -10.
- Boltac identifies and uncurses for half the price: Gem of Exorcism 6000 (`shop_identify_fee`), Sallet-1 1000
  (`shop_uncursed`) (verified).
- Unidentified items show a family name: JEWELRY (the gem), ROD, WEAPON, SPHERE (the orbs), "&" for a potion
  (the Holy Water) (verified: `chest_found_rod`, `inventory_crystal_sphere`, `inventory_decoy_sphere`,
  `inventory_holy_water`).
- Swaps: the monk (floor 3 (7,7)) takes the Broadsword 1014 for the Gold Medallion 1010, the pool (10,19) the
  medallion for the Holy Water 1008 (verified in RAM, 2026-11-19).

## Open questions
- What the Ship in Bottle, Staff of Earth, Amulet of Air, Holy Water, Rod of Fire, Gold Medallion and Blue Pearl
  open.
