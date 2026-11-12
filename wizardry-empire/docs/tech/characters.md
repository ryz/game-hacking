# Characters: races, classes, creation, leveling, aging, statuses, spells

Wizardry Empire (GBC, 1999), Japanese **Rev 1** ROM. Every number names its source: a ROM table (`bank:addr`,
bank in hex: e.g. `26:` = bank 38 decimal), a routine, or an emulator observation. Text marked **(guess)** is inferred from
the data pattern and was not traced in code. English names follow `glossary.md` / the patch script.

`Random(n)` below means the game's `0:2B7E` / `0:0DC0`: `floor(r × (n+1) / 256)` for a random byte `r`, i.e. a
uniform integer **0..n inclusive** (two RNG streams, same formula). "1dN" in the text = `Random(N-1)+1`.

Scratch, scripts and states: `work/design/characters/` (`rom.py` table dumper, `inn_exp*.py`, `inn_stay.py`,
`inn_age.py`, `exp.json`, `bonus_dist.txt`).

---

## 1. Overview (two-minute read)

- **Five races, fourteen classes.** Races give base stats (sum 47-50) and two have extra bonus points (Human +1,
  Hobbit +2). Classes: 9 can be created (Fighter, Mage, Priest, Thief, Bishop, Samurai, Lord, Ninja, Archer).
  5 "special" classes (Valiant, Avenger, Musashi, Kunoichi, Summoner) are reached **only by using one specific
  legendary item each**, never at the Training Grounds.
- **Creation** = race, gender, alignment, then a **bonus-point roll** (usually 4-13, mean 10.4, ~5.6% chance
  of 20+, cap 60) spread over six stats with **at most +10 on any one stat**. All points must be spent. Classes
  whose stat minimums, alignment and gender (Ninja male, Kunoichi female) are met are offered.
- **Stats** are capped at race base + 10 for life and never drop below race base (or the class minimum).
  Each level-up rolls every stat: young characters gain STR/VIT/AGI, old ones lose them but gain Piety.
- **HP**: start = small class roll + VIT bonus; each level adds 1 + up to three class dice.
- **EXP curve**: 16 hand-tuned steps per class, then linear (each level after 16 costs the last step again).
  Thief is cheapest, Ninja/Kunoichi/Valiant most expensive. Levels are bought only at the **Inn**, one per visit.
- **Aging** is real: each inn night is one day (360-day year). Characters start at 14-16. As coded, **any
  birthday at the inn that reaches 57 kills the character** (the survival roll's result is discarded; confirmed
  in the emulator). Resurrection and class change also add 1-3 years.
- **Spells**: 125 spells in 7 schools (Mage 28, Priest 28, Valiant 16, Avenger 12, Musashi 12, Kunoichi 13,
  Summoner 16), each with 7 spell levels. A caster learns **one guaranteed random spell** when a new spell level
  opens (class-specific level schedule) and has a stat-based chance (IQ, PIE, VIT or LUK, 5-60%) to pick up each
  missing spell of open levels at every level-up. Summoners learn summons only by forming **pacts** at maze
  events (level-gated).
- **Spell slots** per spell level = `min(9, max(spells known at that level, char level − unlock level + 1))`;
  other casters' spells kept after a class change give slots equal to the number known. Rest at the inn refills.
- **Death and recovery**: temple fee = level × 10/30/50/100/300 (minor/paralysis/stone/dead/ashes). Raising
  succeeds about 1-96% by age and VIT (§9); failure turns Dead into Ashes and Ashes into Lost. The Revival Charm
  restores Dead, Ashes and Lost members (§9).

---

## 2. Races

Race table `26:5B13` (8 bytes per race; a byte-identical copy at `27:56D9` is used by level-up). Read by
`26:5B40` when the race is chosen (stats into record `+$51..+$56`, byte 7 into the bonus pool `$D014`).

| Race (JP) | STR | IQ | PIE | VIT | AGI | LUK | Sum | Extra bonus points (byte 7) | Byte 6 |
|---|---|---|---|---|---|---|---|---|---|
| Human (にんげん) | 8 | 8 | 6 | 8 | 8 | 9 | 47 | **+1** | 6 |
| Elf (エルフ) | 7 | 10 | 10 | 6 | 10 | 6 | 49 | 0 | 6 |
| Dwarf (ドワーフ) | 12 | 6 | 10 | 10 | 5 | 6 | 49 | 0 | 7 |
| Gnome (ノーム) | 7 | 7 | 10 | 8 | 10 | 7 | 49 | 0 | 6 |
| Hobbit (ホビット) | 6 | 7 | 7 | 6 | 10 | 14 | 50 | **+2** | 5 |

- **Gender modifier**: female characters get **STR −1, VIT +1** on top of the race base (`26:5B79`; the same
  adjustment is applied to the race base when level-up checks stat limits, `27:577E`, and when class change
  resets stats, `26:5281`).
- **Stat limits for life** (`27:5763`): a stat can rise to **race base + 10** (female-adjusted), and cannot fall
  below race base. Examples: Human max 18 in STR, IQ, VIT, AGI, 16 in PIE, 19 in LUK (base + 10); Elf IQ/PIE/AGI 20; Dwarf STR 22; Hobbit
  LUK 24. A stat also cannot fall below the current class's minimum for it (`27:57C2`).
- Byte 6 (6/6/7/6/5) is loaded at `26:5B73` into a register that is then discarded: **unused** in Rev 1
  (guess: a leftover base-AC or size value).
- No race restricts a class (the class table has no race field), and no other racial trait (resistance,
  vision) was found in the creation or level-up code. Race also matters for resurrection: a raise can cost 1 VIT
  but never below race VIT (`27:69AF`, see §9).

---

## 3. Character creation (Training Grounds)

Code: bank 26.

Order of steps (bank 26 menus): name -> race -> gender -> alignment -> bonus points -> class -> confirm.

### 3.1 Starting age

Code: (`26:55E2`, at the gender step.
`r = Random(2)`; r = 0: 16; r = 1: 16 − Random(1); r = 2: 90% 16 − Random(1), 10% 16 − Random(2).
Result: **16 years ≈ 66%, 15 ≈ 33%, 14 ≈ 1%**. The day-of-year counter starts at a random 0-255
(`26:4802`), so the first birthday comes after 105-360 inn days.

### 3.2 Bonus points

Code: (`26:5F6F`.
1. Base roll: `r = Random(20)`. r < 5 (5/21): **8 + Random(2)** (8-10). 5 <= r < 10 (5/21): **4 + Random(3)**
   (4-7). Otherwise (11/21): **10 + Random(3)** (10-13).
2. Four independent "jackpot" rolls: each `Random(99) < 2` (2.3% each with the byte quantisation) adds **+10**.
3. Add the race extra (Human +1, Hobbit +2); cap at **60**.

Distribution without the race extra (exact, computed from the code: `work/design/characters/bonus_dist.txt`):
4-7: 5.4% each; 8: 7.3%; 9: 7.2%; **10: 19.1%**; 11-13: 11.9% each; 14-19: 3.5% total; 20-23: 5.3%;
24+: 0.3%. Mean **10.4**. P(>= 20) = **5.6%**. Whether the player can re-roll was not traced (guess: B
backs out to the alignment step and the roll is repeated on re-entry, since `5F6F` runs on entering the screen,
`26:5CC8`).

### 3.3 Spending points

Code: (`26:5F54`, `26:5D10-5DCC`.
- Up/down picks a stat, left/right moves a point. **Each stat takes at most +10 points** (`cp $0B`), never below
  the race value.
- **All points must be spent** before a class can be chosen: otherwise the message "Bonus points remain."
  (`26:7277`); if no class qualifies, "No class is available." (`26:7289`).
- Eligibility is recomputed live (`26:628B`) and the qualifying class names are shown.

### 3.4 Class eligibility

Code: (`26:628B`, table `26:6229`, 7 bytes per class.
A class qualifies when every stat >= its minimum (0 = no minimum), the gender nibble matches (`F` = any) and the
alignment bit is set (bit 0 Good, bit 1 Neutral, bit 2 Evil). Creation and the Change Class menu only cycle
indices **0-8** (`26:5D81 cp $09`, `26:4FE8`), so the special classes are never offered there although the table
has their requirements (they apply to the stat reset when the item changes the class, §5.5).

| Class (JP) | STR | IQ | PIE | VIT | AGI | LUK | Gender | Alignment |
|---|---|---|---|---|---|---|---|---|
| Fighter (せんし) | 11 | | | | | | any | any |
| Mage (まほうつかい) | | 11 | | | | | any | any |
| Priest (そうりょ) | | | 11 | | | | any | Good, Evil |
| Thief (とうぞく) | | | | | 11 | | any | Neutral, Evil |
| Bishop (ビショップ) | | 12 | 12 | | | | any | Good, Evil |
| Samurai (サムライ) | 15 | 11 | 10 | 14 | 10 | | any | Good, Neutral |
| Lord (ロード) | 15 | 12 | 12 | 15 | 14 | 15 | any | Good |
| Ninja (ニンジャ) | 16 | 16 | 16 | 16 | 15 | 16 | **male** | Evil |
| Archer (ゆみつかい) | 10 | 10 | | | 12 | | any | any |
| Valiant (ヴァリアント) | 15 | 16 | 17 | 15 | 16 | 15 | any | Good |
| Avenger (アベンジャー) | 16 | 16 | 14 | 12 | | | any | Evil |
| Musashi (ムサシ) | 18 | 13 | 13 | 18 | 17 | 13 | any | Good, Neutral |
| Kunoichi (くのいち) | 17 | 16 | 16 | 17 | 18 | 17 | **female** | Evil |
| Summoner (しょうかんし) | | 18 | 18 | | | 16 | any | Neutral |

Ninja at creation needs 16/16/16/16/15/16: with the +10 per-stat cap and a typical 10-point roll it is only
reachable with a jackpot roll (a Human needs 8+8+10+8+7+7 = 48 points).

### 3.5 What the new character gets

Code: (`26:47DA-4852`.
- Stats = race base (+ gender) + allocated points.
- **HP** (`26:6156`, table `26:6134`, classes 0-8 only): `Random(a) + 1 + b + VITbonus`.

  | Class | a, b | Starting HP before VIT bonus |
  |---|---|---|
  | Fighter | 2, 5 | 6-8 |
  | Mage | 1, 3 | 4-5 |
  | Priest | 1, 5 | 6-7 |
  | Thief | 1, 4 | 5-6 |
  | Bishop | 1, 4 | 5-6 |
  | Samurai | 2, 6 | 7-9 |
  | Lord | 4, 7 | 8-12 |
  | Ninja | 4, 5 | 6-10 |
  | Archer | 2, 4 | 5-7 |

  VIT bonus (`26:6146`, index VIT−6): VIT 6-7: 0; 8-10: +1; 11-14: +2; 15-18: +3; 19-20: +4; 21: +5.
- **Starting kit and AC** (`26:61D6`, table `26:61BB`, 3 bytes: item, item, AC); both items equipped
  (flag `$80`), gold 100 (template value, `+$59`).

  | Class | Items | AC |
  |---|---|---|
  | Fighter, Samurai, Lord | Sword + Leather Armor | 8 |
  | Thief | Short Sword + Leather Armor | 8 |
  | Archer | Dagger + Leather Armor | 8 |
  | Mage | Dagger + Robe | 9 |
  | Priest, Bishop | Quarterstaff + Robe | 9 |
  | Ninja | Short Sword + Robe | 9 |

- **Spells**: the level-up spell routine runs once (`26:4819` -> `2A:416D`), so a Mage/Priest/Bishop gets one
  guaranteed random level-1 spell plus the IQ/PIE chance for each other level-1 spell (§10.3).
- The record is stamped with "Wizardry EMPIRE1" at `+$70` (`26:6187`) and stored in the first free SRAM roster
  slot (`$A000 + $80×n`, `26:4822`).

### 3.6 Ready-made characters

Code: (`2E:4000`, 6 records = script/templates.json.

| Name | Race | Class | Align | Sex | STR IQ PIE VIT AGI LUK | HP | AC |
|---|---|---|---|---|---|---|---|
| Fighter (せんし) | Dwarf | Fighter | Good | M | 15 8 11 14 7 8 | 10 | 8 |
| Thief (とうぞく) | Human | Thief | Evil | M | 8 9 7 9 13 13 | 7 | 8 |
| Archer (ゆみつかい) | Hobbit | Archer | Neutral | M | 14 6 7 6 15 17 | 7 | 8 |
| Priest (そうりょ) | Gnome | Priest | Good | M | 9 10 14 9 12 9 | 8 | 9 |
| Mage (まほうつかい) | Elf | Mage | Evil | F | 8 15 12 8 12 8 | 5 | 9 |
| Bishop (ビショップ) | Elf | Bishop | Good | M | 8 13 13 8 12 8 | 7 | 9 |

All level 1, age 16, 100 gold, 0 EXP. Starting spells: Mage Call Fear; Priest Restore; Bishop Call Fear +
Flame Arrow.

---

## 4. Party record

Code: (`$80` bytes; party `$C880 + $80×n`, working copy `$C48F`, roster SRAM `$A001 + $80×n`.

Offsets from the record start. Confidence: **code** = read/written by a routine named here; **(guess)** = pattern only.

| Offset | Size | Field | Notes / source |
|---|---|---|---|
| `+00` | 8 | Name | `$00`-terminated, 7 characters max |
| `+08` | 1 | Race | 0 Human, 1 Elf, 2 Dwarf, 3 Gnome, 4 Hobbit (`26:5B4C`) |
| `+09` | 1 | Class | 0-13 in the order of §3.4 (`26:5E22`) |
| `+0A` | 1 | Alignment | 0 Good, 1 Neutral, 2 Evil (`26:62E6`) |
| `+0B` | 1 | Gender | 0 male, 1 female (`26:55DF`) |
| `+0C` | 1 | Status | low 6 bits: 0 OK, 1 Afraid, 2 Asleep, 3 Paralyzed, 4 Stoned, 5 Dead, 6 Ashes, 7 Lost; bit 6 Silenced, bit 7 Poisoned (`docs/re/text.md`) |
| `+0D` | 2 | Level | 16-bit, max 9999 (`27:53B3`) |
| `+0F` | 1 + bit 0 of `+10` | Day of year | 9-bit counter 0-359 (`27:5208`) |
| `+10` | bits 1-7 | Age in years | max 99; shown as `+10 >> 1` (`26:56FE`) |
| `+11` | 16 | Inventory | 8 × (item id, flags); id `$FF` = empty; flags bit 7 equipped, bit 5 cursed/locked, bit 4 set by off-hand equip (`26:5249`, `2A:615E`) |
| `+21` | 16 | (unused) | filled `00 FF`; v1.0 code read it as 8 more inventory pairs, Rev 1 does not (`docs/re/rev1.md`) |
| `+30` | 1 | ? | always 0 seen |
| `+31` | 7 | Spells known, Mage+Priest | bit n = spell id n (0-27 Mage, 28-55 Priest) (`2A:434A`, `2B8C` bit test) |
| `+38` | 1 | ? | (between the two bitmaps) |
| `+39` | 3 | Spells known, own special school | bit n = n-th spell of the class's school (`2A:440C`, `2D:65C7`) |
| `+3C` | 7 | Mage slots, levels 1-7 | remaining casts (`2A:45AF` display, `2A:4609` refill) |
| `+43` | 7 | Priest slots, levels 1-7 | |
| `+4A` | 7 | Special-school slots, levels 1-7 | cleared on class change |
| `+51` | 6 | STR, IQ, PIE, VIT, AGI, LUK | |
| `+57` | 1 | ? (guess: formation/row bits) | party copies hold slot×`$20`; set to `$15` when dying of old age (`27:5149`) |
| `+58` | 1 | AC | shown "Lo"/"Hi" when out of the printable range |
| `+59` | 4 | Gold | (`27:5245`) |
| `+5D` | 4 | EXP | (`27:5B8E`) |
| `+61` | 1 | ? | |
| `+62` | 2 | Max HP | cap 65535 (`27:5891`) |
| `+64` | 2 | Current HP | |
| `+66` | 2 | ? | |
| `+68` | 1 | Equipped weapon item id | `$FF` none (`2A:6154`) |
| `+69` | 1 | Equipped off-hand item id | (`2A:6162`) |
| `+6A` | 6 | ? | |
| `+70` | 16 | "Wizardry EMPIRE1" | signature (`26:6187`); the roster copy keeps 15 bytes |

Not stored in the record (recomputed): to-hit, swings per round, spell-slot maxima (see items.md §4 and §10.4).

---

## 5. Classes

### 5.1 Summary

| # | Class | Created? | Spell schools (start level of school) | HP die D per level (`27:57EF`) | Total EXP to reach L2 / L10 (§6.1) |
|---|---|---|---|---|---|
| 0 | Fighter | yes | - | 9 | 1,200 / 56,800 |
| 1 | Mage | yes | Mage (1) | 4 | 1,520 / 73,720 |
| 2 | Priest | yes | Priest (1) | 8 | 1,400 / 69,100 |
| 3 | Thief | yes | - | 5 | 1,080 / 45,320 |
| 4 | Bishop | yes | Mage (1), Priest (4) | 6 | 1,650 / 97,550 |
| 5 | Samurai | yes | Mage (4) | 8 | 1,800 / 106,070 |
| 6 | Lord | yes | Priest (4) | 8 | 1,920 / 111,320 |
| 7 | Ninja | yes (male) | - | 7 | 2,150 / 116,550 |
| 8 | Archer | yes | - | 6 | 1,520 / 71,370 |
| 9 | Valiant | item only | Valiant Prayers (5) | 8 | 2,100 / 121,400 |
| 10 | Avenger | item only | Avenger Arts (5) | 8 | 1,360 / 62,910 |
| 11 | Musashi | item only | Musashi Arts (5) | 8 | 1,980 / 116,150 |
| 12 | Kunoichi | item only (female) | Kunoichi Arts (5) | 6 | 2,150 / 116,550 |
| 13 | Summoner | item only | Summons (pacts, from level 3) | 5 | 1,420 / 77,170 |

D is used as `Random(D)` = 0..D, see §6.3.

Corrected 2026-11-12: the L10 column showed the level-9 totals of §6.1 (Fighter 35,800); it now shows the level-10
row (Fighter 56,800). The §6.1 rows were right (checked in the code and the emulator, §6.1).

Ninja and Kunoichi share one EXP table (identical values). Swings per round, to-hit and the class rules for
weapons (Musashi dual wield, Avenger immune to cursed items) are in `items.md` §2/§4.

### 5.2 Equipment groups
Each item's bytes 22-23 are a 14-bit class mask (bit = class number; items.md §1). Counting items per class and
item category (item byte 17) gives the equipment groups (`work/design/characters/items.json`):

Number of items usable, per item category (byte 17 generic name; "Staff/mace" = categories 5 and 10-12, which
also hold flails and maces). Column header = items in that category.

| Class | Sword (35) | Axe (6) | Spear (9) | Dagger (9) | Staff/mace (22) | Hammer (2) | Scythe (2) | Bow (7) | Arrow (4) | Armor (26) | Robe (6) | Shield (17) | Helm (16) | Gloves (14) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fighter | 26 | 6 | 9 | 7 | 21 | 2 | 2 | 3 | 4 | 20 | 3 | 16 | 13 | 13 |
| Mage | 0 | 0 | 0 | 6 | 8 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 2 | 0 |
| Priest | 0 | 0 | 0 | 0 | 17 | 2 | 0 | 0 | 0 | 17 | 5 | 13 | 12 | 12 |
| Thief | 5 | 0 | 0 | 8 | 0 | 0 | 1 | 2 | 4 | 4 | 4 | 3 | 2 | 1 |
| Bishop | 0 | 0 | 0 | 0 | 17 | 2 | 0 | 0 | 0 | 6 | 5 | 3 | 5 | 2 |
| Samurai | 32 | 6 | 9 | 7 | 21 | 2 | 2 | 3 | 4 | 21 | 4 | 0 | 12 | 12 |
| Lord | 26 | 6 | 9 | 7 | 21 | 2 | 2 | 3 | 4 | 18 | 4 | 16 | 13 | 13 |
| Ninja | 27 | 6 | 9 | 9 | 22 | 2 | 2 | 3 | 4 | 20 | 4 | 3 | 11 | 12 |
| Archer | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 7 | 4 | 3 | 4 | 0 | 2 | 1 |
| Valiant | 26 | 6 | 9 | 7 | 21 | 2 | 2 | 3 | 4 | 18 | 4 | 17 | 14 | 13 |
| Avenger | 6 | 2 | 2 | 1 | 4 | 0 | 1 | 0 | 0 | 7 | 4 | 6 | 4 | 4 |
| Musashi | 28 | 1 | 6 | 7 | 8 | 2 | 1 | 0 | 0 | 21 | 4 | 0 | 13 | 12 |
| Kunoichi | 27 | 6 | 9 | 9 | 22 | 2 | 2 | 3 | 4 | 20 | 4 | 11 | 11 | 13 |
| Summoner | 0 | 0 | 0 | 6 | 16 | 2 | 0 | 1 | 2 | 3 | 6 | 2 | 3 | 1 |

Reading: Fighter/Lord/Valiant/Ninja/Kunoichi take nearly all weapons; Samurai and Musashi own the katanas (32/28
swords) but no shields; Priests wear heavy armor and shields but no edged weapons; Mage, Archer and Summoner are
limited to robes and light armor; the Avenger has a short, special list.

Accessories (slot type 12, data `28:4000` bytes 22-23; `work/re/contradictions/notes.md` item 7):
- **Rings**: 9 of 10 can be equipped by every class; the Priest Ring only by Priest, Bishop, Lord and Valiant.
- **Other accessories** are mixed: Cloak, Shell Amulets, Rabbit's Foot, Synthesis and Youth Stone: every class;
  Hider Cloak: Thief; Clockwork Doll: Ninja, Kunoichi; Laila's Beads: Priest, Bishop, Valiant; Jewel of Magic: Mage,
  Priest, Bishop, Summoner; Fairy's Heart: all but Ninja, Avenger, Kunoichi.
- **Consumables** (all potions and scrolls, the Dreaming, Healing and Exorcist Stones, the Exorcism and Revival
  Charms, the Map Record Sheet) and the Key Card have **no class bit** ("none" in the items table): nobody can
  equip them, but **anyone can use them**. Item use does not test the class mask: camp use `2A:6C91-6CC0` checks only
  byte 33 bit 6; battle start sets "usable" from byte 33 bit 7 alone (`22:4356`). (emulator: a Fighter used a
  Healing Potion and a Revival Charm in camp, `work/re/contradictions/camp_potion.py`, `camp_charm.py`.)

Corrected 2026-11-12: was "Rings and odd objects are open to every class".
Exact per-item lists: [../design/items_table.md](../design/items_table.md).

### 5.3 Spell schedule per class (learning, §10.3)

| Class | School | Spell level 1..7 opens at character level | Extra-learn chance stat |
|---|---|---|---|
| Mage | Mage | 1, 3, 5, 7, 9, 11, 13 (`2A:40D1`) | IQ |
| Priest | Priest | 1, 3, 5, 7, 9, 11, 13 (`2A:40D8`) | PIE |
| Bishop | Mage | 1, 5, 9, 13, 17, 21, 25 (`2A:4118`) | IQ |
| Bishop | Priest | 4, 8, 12, 16, 20, 24, 28 (`2A:4127`) | PIE |
| Samurai | Mage | 4, 7, 10, 13, 16, 19, 22 (`2A:40DF`) | IQ |
| Lord | Priest | 4, 6, 8, 10, 12, 14, 16 (`2A:40E6`) | PIE |
| Valiant | Valiant Prayers | 5, 10, 15, 20, 25, 30, 35 (`2A:40ED`) | PIE |
| Avenger | Avenger Arts | 5, 10, ... 35 (`2A:40F4`) | VIT |
| Musashi | Musashi Arts | 5, 10, ... 35 (`2A:40FB`) | VIT |
| Kunoichi | Kunoichi Arts | 5, 10, ... 35 (`2A:4102`) | LUK |
| Summoner | Summons | slot schedule 3, 6, 14, 16, 20, 27, 34 (`2A:4109`); spells only by pacts (§10.5) | - |
| Fighter, Thief, Ninja, Archer | none | - | - |

### 5.4 Change Class

Code: (Training Grounds `26:5140` on the roster record; item version `26:521E` on the working copy.
Only classes 0-8 the character qualifies for (current stats, alignment, gender) and not the current class.
Effects:
- Level 1, **EXP 0**; age **+1..3 years** (`Random(2)+1`, cap 99).
- **Stats reset**: each stat = race base (gender-adjusted), then raised to the new class's minimum where it has one
  (`26:525E-52B1`). Everything earned above that is lost.
- Equipped items are unequipped unless cursed (flag bit 5) (`26:5249`).
- Mage and Priest spells known are **kept** (bitmap `+31` untouched); the special-school bitmap and slots are
  cleared (`26:52BB`).
- HP and gold are unchanged. At the Training Grounds the guaranteed level-1 spell of the new class is rolled
  (`26:5213` -> `2A:417F`; Mage/Priest/Bishop only) and slots are recomputed; the item version does not roll a
  spell (special schools open at level 5 anyway).

### 5.5 Special classes: legendary items

Code: (item byte 35, handler `2A:5EF6`.
"Use its special power" on these items: (items.md §3.3 covers the item side)

| Item (byte 35) | Effect |
|---|---|
| Rabbit's Foot (1) | LUK +1, up to race base + 10 (`26:52D5`) |
| Youth Stone (2) | age −1 year, not below 12 |
| Thieves' Dagger (3) | a **Thief** becomes a **Ninja** (male only) |
| Butterfly Knife (4) | becomes a **Ninja** (male only) |
| Guardian Shield (5) | becomes **Valiant** |
| The Avenger (6) | becomes **Avenger** |
| Warrior's Helm (7) | becomes **Musashi** |
| Charming Gloves (8) | becomes **Kunoichi** (female only) |
| Magic Robe (9) | becomes **Summoner** |

The handler checks only gender (Ninja male, Kunoichi female) and, for item 3, the Thief class; **no stat or
alignment check** was found (the item's own class/alignment equip bits are the only gate, guess). The change
itself is the Change Class routine `26:521E` (§5.4): level 1, EXP 0, +1-3 years, stats reset to race base raised
to the new class minimums (e.g. a Musashi starts with STR 18, VIT 18, AGI 17).

---

## 6. Experience and leveling

### 6.1 EXP needed

Code: (`27:5B70` / `27:5BEA`, per-class pointer table `27:5B54`, 16 × 3-byte steps per class.
Total EXP to reach level L = sum of the first L steps of the class table for L <= 16; from level 17 on each
level costs the 16th step again (Rev 1 multiplies it out with `0:0DFA`, see `docs/re/rev1.md`). Level 1 -> 2 thus
needs the first **two** steps. Confirmed in the emulator: a level-1 Fighter with 0 EXP is told "1200 more EXP"
at the Inn (`work/design/characters/inn1.png`). The v1.0 ROM said 500 at the same point
(`docs/shots/jp_tour/inn_stable.jp.png` was taken on v1.0), so the curve changed between revisions.

How to read the table: row N = the **total EXP a character needs to reach level N**; a character of level N−1
levels up at the Inn once his EXP is at least row N (`27:5B70` passes level+1 to `27:5BEA`, which adds the first
N steps). Emulator check (`work/re/contradictions/inn_spells_exp.py`, JP): a level-9 Thief with 29,820 EXP (row 9) is told
"15500 more" = row 10 (45,320) − 29,820. "EXP to L2" in §5.1 = row 2, "L10" = row 10.

Cumulative EXP to reach each level (raw steps in `work/design/characters/exp.json`):

| Level | Fig | Mag | Pri | Thi | Bis | Sam | Lor | Nin | Arc | Val | Ave | Mus | Kun | Sum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 1,200 | 1,520 | 1,400 | 1,080 | 1,650 | 1,800 | 1,920 | 2,150 | 1,520 | 2,100 | 1,360 | 1,980 | 2,150 | 1,420 |
| 3 | 2,200 | 2,820 | 2,600 | 1,920 | 3,150 | 3,550 | 3,820 | 4,150 | 2,770 | 4,200 | 2,460 | 3,930 | 4,150 | 2,670 |
| 4 | 3,700 | 4,820 | 4,400 | 3,220 | 5,450 | 6,250 | 6,820 | 7,450 | 4,670 | 7,600 | 4,110 | 7,030 | 7,450 | 4,570 |
| 5 | 6,000 | 8,020 | 7,200 | 5,270 | 9,150 | 10,450 | 11,420 | 12,350 | 7,670 | 12,800 | 6,610 | 11,830 | 12,350 | 7,570 |
| 6 | 9,500 | 13,020 | 11,800 | 8,370 | 15,250 | 16,870 | 18,320 | 19,650 | 12,470 | 20,600 | 10,610 | 19,150 | 19,650 | 12,370 |
| 7 | 14,800 | 20,620 | 19,100 | 13,020 | 25,050 | 26,870 | 28,820 | 30,850 | 19,870 | 32,600 | 16,910 | 30,650 | 30,850 | 19,920 |
| 8 | 22,800 | 31,920 | 30,100 | 19,820 | 40,450 | 42,870 | 45,320 | 48,350 | 30,970 | 50,800 | 26,410 | 48,350 | 48,350 | 31,620 |
| 9 | 35,800 | 48,720 | 46,100 | 29,820 | 63,450 | 67,870 | 71,320 | 75,450 | 47,370 | 78,800 | 40,910 | 75,350 | 75,450 | 49,620 |
| 10 | 56,800 | 73,720 | 69,100 | 45,320 | 97,550 | 106,070 | 111,320 | 116,550 | 71,370 | 121,400 | 62,910 | 116,150 | 116,550 | 77,170 |
| 11 | 90,300 | 110,720 | 104,100 | 70,820 | 147,750 | 164,070 | 171,320 | 178,350 | 107,370 | 184,400 | 97,110 | 177,150 | 178,350 | 118,970 |
| 12 | 144,600 | 165,720 | 158,100 | 111,820 | 220,750 | 249,070 | 259,320 | 268,350 | 161,870 | 276,400 | 151,210 | 266,150 | 268,350 | 182,470 |
| 13 | 229,700 | 251,720 | 239,500 | 176,820 | 326,150 | 370,270 | 384,320 | 398,350 | 245,570 | 408,400 | 234,410 | 394,350 | 398,350 | 277,470 |
| 14 | 355,700 | 378,720 | 366,000 | 276,820 | 476,150 | 541,070 | 558,320 | 582,350 | 372,270 | 594,400 | 360,410 | 577,150 | 582,350 | 415,470 |
| 15 | 533,700 | 564,720 | 546,000 | 426,820 | 693,150 | 779,070 | 799,320 | 838,350 | 555,270 | 854,400 | 539,410 | 834,150 | 838,350 | 612,470 |
| 16 | 763,700 | 814,720 | 786,000 | 644,820 | 1,003,150 | 1,105,070 | 1,129,320 | 1,188,350 | 800,270 | 1,204,400 | 774,410 | 1,180,150 | 1,188,350 | 882,470 |
| 17 | 993,700 | 1,064,720 | 1,026,000 | 862,820 | 1,313,150 | 1,431,070 | 1,459,320 | 1,538,350 | 1,045,270 | 1,554,400 | 1,009,410 | 1,526,150 | 1,538,350 | 1,152,470 |
| each level after 17 | +230,000 | +250,000 | +240,000 | +218,000 | +310,000 | +326,000 | +330,000 | +350,000 | +245,000 | +350,000 | +235,000 | +346,000 | +350,000 | +270,000 |

"each level after 17" = the cost of every further level (the 16th step repeated; level 17 itself already
used it once).

Order of cost at level 10: Thief < Fighter < Avenger < Priest < Archer < Mage < Summoner < Bishop < Samurai <
Lord < Musashi < Ninja = Kunoichi < Valiant.

### 6.2 When the level-up happens
Only at the **Inn**: choosing a room for a character first checks the EXP (`27:4DCE`); if enough, that stay
grants **one** level (`27:4F2B` -> `27:5451`), otherwise the Inn shows "Next level in N more EXP". Level cap
9999 (`27:53B3`).

Level-up (`27:5451`), in this order: level +1; each of the six stats is rolled (§6.4); HP gain (§6.3); spells
(`27:54B5` -> `2A:416D`, §10).

### 6.3 HP gained per level

Code: (`27:57FD`.
1. A special case: `Random(99) == LUK + Random(LUK)` (about 1%) -> gain only **1 HP**. (The age bracket computed
   just before is overwritten here and has no effect.)
2. Otherwise, with D = class die (§5.1 table, `27:57EF`):
   - gain = 1 + `Random(D)`;
   - if `Random(99) >= VIT + LUK`, add `Random(D−1)`; and if a second `Random(99)` is >= the margin of the first
     roll (`first − (VIT+LUK)`), add `Random(D−2)` as well.
   As coded, **low VIT+LUK gives more extra dice**; with VIT+LUK >= 100 there is never an extra die. (This looks
   inverted against the usual design intent; reported as the code reads.)
3. The gain is added to both max and current HP, capped at 65535.

Example, Fighter (D = 9), VIT+LUK = 30: base 1-10 (avg 5.5); 70% chance of +0-8; then usually another +0-7.

### 6.4 Stat changes per level

Code: (`27:566F`, table `27:7451`, 6 stats × 10 age brackets × 2 bytes.
Age bracket by years: <20, 20-24, 25-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80-89, 90+. Roll
`r = Random(100)`: **r < gain → +1**; gain <= r < keep → no change; **r >= keep → −1**. Limits from §2 apply
(a blocked change is simply no change). Messages "STR rose." / "STR fell." etc. (`27:7787...`).

Percent chances (gain% / loss%), exact for the byte-quantised `Random(100)`:

| Age | STR | IQ | PIE | VIT | AGI | LUK |
|---|---|---|---|---|---|---|
| <20 | 75 / 11 | 50 / 6 | 40 / 21 | 89 / 6 | 79 / 6 | 46 / 16 |
| 20-24 | 70 / 11 | 55 / 6 | 45 / 16 | 84 / 6 | 79 / 6 | 46 / 17 |
| 25-29 | 60 / 21 | 55 / 11 | 50 / 16 | 75 / 11 | 75 / 11 | 41 / 21 |
| 30-39 | 45 / 30 | 60 / 11 | 55 / 16 | 64 / 21 | 70 / 11 | 38 / 25 |
| 40-49 | 30 / 40 | 60 / 21 | 60 / 11 | 50 / 30 | 55 / 30 | 25 / 25 |
| 50-59 | 20 / 50 | 55 / 25 | 64 / 11 | 40 / 40 | 30 / 60 | 20 / 25 |
| 60-69 | 10 / 65 | 45 / 40 | 70 / 11 | 30 / 55 | 20 / 75 | 20 / 25 |
| 70-79 | 5 / 75 | 30 / 55 | 79 / 11 | 15 / 70 | 5 / 90 | 19 / 25 |
| 80-89 | 0 / 90 | 20 / 70 | 89 / 6 | 10 / 80 | 5 / 90 | 19 / 30 |
| 90+ | 0 / 95 | 5 / 85 | 89 / 6 | 5 / 90 | 5 / 90 | 19 / 30 |

Raw thresholds (gain, keep) as stored, e.g. STR <20 = (75, 90), are in `27:7451`.

---

## 7. Aging

- **Clock**: a 9-bit day counter (`+0F` and `+10` bit 0) and the age in years (`+10` bits 1-7). Each counted day
  adds 1; at 360 the counter wraps and the age goes up (`27:5208`), cap 99.
- **What advances it**: each inn night outside the Stables, **at any HP** (§8; a full stay = 7 nights: day counter
  +7 after Cots both from HP 1/200 and at full HP, none after the Stables; `work/re/contradictions/inn_days.py`, emulator; the
  loop `27:50F8-5131` calls `27:5208` every night unless the room is the Stables). Class change and item class change: +1-3 years. Temple raise: +1-3 years at 89%;
  spell raise: +1 year (§9). Youth Stone: −1 year. No time-in-maze aging was found.
- **Effects**: the age bracket drives the level-up stat rolls (§6.4) and resurrection odds (§9).
- **Death of old age** (`27:532B`, at a birthday during an inn stay): if the new age is **57 or more**, the
  character dies (status Dead, HP 0, "died of old age.", `27:7866`). The code rolls
  `Random(99 + VIT/2 + LUK/2)` and compares it with `age − 56`, but no branch uses the result (`cp b` followed by
  an unconditional store, identical in v1.0), so **every** such birthday is fatal. Intended rule (guess): death if
  the roll < age − 56. **Confirmed in the emulator**: age 56, day 359, Cots -> Dead at 57 (six RNG seeds, VIT = LUK = 18;
  a breakpoint at `27:537C` read rolls 89, 89, 59, 50, 8, 11 against B = age − 56 = 1: under the intended rule all
  six would have survived, all six died; `work/re/contradictions/inn_oldage.py`); age 55 ->
  56 survives ("Happy birthday!", `27:7857`). Script `inn_age.py`, start state `jp_inn_rooms.state`
  (tokens from power-on, JP ROM: `boot,right*3,a,w60,a,w40,a,w30,a,w30,a,w30,a,w30,a,w30,a,w30,b,w40,b,w40,b,w60,right*4,a,w60,a,w60`; the
  state is the room menu for the party's Fighter).
  Practical lifespan from 16: about 41 game years = ~14,800 inn nights.

---

## 8. Inn rest

Code: (Aries Inn, `27:5046-5B53`.

| Room | Price (per night charged) | Nights | HP per night (`27:5A96`) | Ages? |
|---|---|---|---|---|
| Stables | free | 1 | none | no |
| Cots | 10 | up to 7 | 3d6+2 | yes |
| Economy | 50 | up to 7 | 10d6 | yes |
| Suite | 200 | up to 7 | 8d10+20 | yes |
| Royal Suite | 500 | up to 7 | 10d20+20 | yes |

The menu says "/week", but the price is charged for **each night the character is still hurt** (observed: HP
1/200 at Cots cost 70 G for 7 nights and healed 104; HP 1/10 cost 10 G). All 7 nights age the character
regardless of HP (emulator: Cots at full HP, age 50 day 300 -> day 307, 0 G paid; `work/re/contradictions/inn_days.py`).
Every night, including the Stables, ends in the heal routine `27:5AAA`, which always finishes with the slot refill
`27:5B4B` -> `2A:45F3` (recount + class slots `2A:4737`, §10.4); the only night without it is a hurt night the
character cannot pay for (`27:598F` skips `5AAA`). Emulator: Stables at full HP and Cots from HP 1 both raised
Mage slots 0 -> 4 for four known level-1 spells (`work/re/contradictions/inn_spells_exp.py`). The Inn is also where
level-ups happen (§6.2).

---

## 9. Status ailments and recovery

| Status (code) | Temple rate × level (`27:6A20`) | Notes |
|---|---|---|
| Afraid (1), Asleep (2), Poisoned (bit 7), Silenced (bit 6) | 10 | (status < 3) |
| Paralyzed (3) | 30 | |
| Stoned (4) | 50 | |
| Dead (5) | 100 | raise roll |
| Ashes (6) | 300 | raise roll |
| Lost (7) | - | temple: not offered; Revival Charm cures it (below) |

**Revival Charm** (item 172, use effect 20 = `2E:5209`): on a member with status Dead, Ashes **or Lost**
(`& $3F >= 5`) it sets status OK and HP = max; on anyone else "nothing happens". Emulator (JP, camp): a member
poked to Lost (`$C90C` = 7) was restored to OK at full HP (`work/re/contradictions/camp_charm.py`). A Lost character only
stays in the party when the spell raise fails on Ashes (below); a failed temple raise deletes him at once.
Corrected 2026-11-12: was "Lost: character removed; no cure found".

**Temple raise** (`27:683A`): success if `Random(100) < base(age) + VITbonus + 1`, i.e. about
(base + bonus + 1)/101 (exactly `ceil(256c/101)/256` for c = base + bonus + 1, because `Random` scales one random
byte). Range: 1.2% (age 70+, VIT < 7) to 95.3% (age < 20, VIT 20-21); the VIT 22+ bonus 6 (96.1%) needs a VIT no
race can reach (race base + 10 is at most 21, §2).

| Age | base | | VIT | bonus |
|---|---|---|---|---|
| <20 | 90 | | <7 | 0 |
| 20-29 | 80 | | 7 | 1 |
| 30-39 | 65 | | 8-9 | 2 |
| 40-49 | 40 | | 10-14 | 3 |
| 50-69 | 10 | | 15-19 | 4 |
| 70+ | 0 | | 20-21 | 5 |
| | | | 22+ | 6 |

Success: status cleared, HP at least 1; then 61%: VIT −1 (not below race VIT, `27:69B4`); then 89%: age +1..3
years. Failure: Dead -> Ashes, Ashes -> Lost (Lost characters are deleted from the roster, `27:6903`).

**Spell raise** (`0:3920`, called from the spell-effect bank `24`): success if `Random(99) <` base(age) (same as
the temple but 50+ = 10) + VIT bonus + caster's PIE bonus (PIE <7: 0, 7-10: 1, 11-14: 2, 15-17: 3, 18-19: 4,
20+: 5). Success: status OK, age +1 year. Failure: status +1 (Dead -> Ashes -> Lost).

Not traced: how Afraid/Asleep/Paralysis wear off in battle, poison damage per step, Silence duration (battle
code, banks 22/32; see `monsters.md` if written).

---

## 10. Spells

### 10.1 The spell record

Code: (`24:6C95`, 16 bytes × 125, id order.
| Byte | Meaning | Confidence |
|---|---|---|
| 0-10 | Name (11 bytes; the patch keeps a short fallback name here) | code (`0:24E8`) |
| 11 | `$00` terminator | |
| 12 | Use flags: bit 5 battle, bit 6 camp, bit 4 at a chest; bit 7 and bit 0 unknown | camp bit matches the "×" marks on the camp spell screen (`docs/shots/jp_tour/camp_spells_mage.jp.png`); rest (guess) |
| 13 | Element / resist type 0-7 (fire spells = 2, cold 1, lightning 3, mind 4, earth 0, healing 6, none 7) | (guess) |
| 14 | 0-`$1E`, low 3 bits look like a level, bits 3-4 an index | unknown (not the spell level; the level comes from the school tables) |
| 15 | Low nibble = school (0 Mage, 1 Priest, 2 Valiant, 3 Avenger, 4 Musashi, 5 Kunoichi, 6 Summoner); high nibble = target type | school: matches every id range; target: (guess) from names: 1 one enemy, 6 one group, 7 all enemies, 8 caster, 9 one ally, A party, C chest |

Spell level = position inside the school's per-level count table (`2A:408A` Mage 4-3-4-3-4-6-4; `2A:4092` Priest
4-5-5-3-4-4-3; specials `2A:40AA...`). Ids: Mage 0-27, Priest 28-55, Valiant 56-71, Avenger 72-83, Musashi
84-95, Kunoichi 96-108, Summoner 109-124. Cost of a cast: one slot of that spell level (`2A:4D16`, `32:51AA`
decrement; guess on the exact site).

### 10.2 Spell lists

Columns: Where = byte 12 use flags; Target and Element = bytes 15/13 with the (guessed) meanings of §10.1; raw =
record bytes 11-15.

#### Mage spells (まほうつかいの じゅもん)

| Lv | # | Spell (EN) | JP | Where (flags) | Target code | Element code | raw +11..+15 |
|---|---|---|---|---|---|---|---|
| 1 | 0 | Call Fear | コールフィアー | battle | 6 (enemy group) | 4 (mind) | `00 21 04 00 60` |
| 1 | 1 | Shield | シールド | battle | 8 (caster) | 5 (arcane) | `00 21 05 08 80` |
| 1 | 2 | Flame Arrow | フレイムアロー | battle | 1 (1 enemy) | 2 (fire) | `00 21 02 10 10` |
| 1 | 3 | Compass | コンパス | camp | 0 (none/field) | 7 (none) | `00 40 07 18 00` |
| 2 | 4 | Sleep | スリープ | battle | 6 (enemy group) | 4 (mind) | `00 21 04 01 60` |
| 2 | 5 | Lightning Bolt | ライトニングボルト | battle | 6 (enemy group) | 3 (air/lightning) | `00 21 03 09 60` |
| 2 | 6 | Darkness | ダークネス | battle | 6 (enemy group) | 7 (none) | `00 21 07 11 60` |
| 3 | 7 | Fireball | ファイアボール | battle | 6 (enemy group) | 2 (fire) | `00 21 02 02 60` |
| 3 | 8 | Missile Shield | ミサイルシールド | battle | A (party) | 3 (air/lightning) | `00 21 03 0a a0` |
| 3 | 9 | Striking | ストライキング | battle | 9 (1 ally) | 7 (none) | `00 20 07 12 90` |
| 3 | 10 | Hold Ray | ホールドレイ | battle | 6 (enemy group) | 4 (mind) | `00 21 04 1a 60` |
| 4 | 11 | Ice Storm | アイスストーム | battle | 6 (enemy group) | 1 (water/cold) | `00 21 01 03 60` |
| 4 | 12 | Explosion | エクスプロージョン | battle | 7 (all enemies) | 2 (fire) | `00 21 02 0b 70` |
| 4 | 13 | Levitate | レビテート | camp | A (party) | 5 (arcane) | `00 40 05 13 a0` |
| 5 | 14 | Thunderbolt | サンダーボルト | battle | 7 (all enemies) | 3 (air/lightning) | `00 21 03 04 70` |
| 5 | 15 | Stone Ray | ストーンレイ | battle | 6 (enemy group) | 0 (earth) | `00 21 00 0c 60` |
| 5 | 16 | Dispel Magic | ディスペルマジック | battle+camp | B (?) | 5 (arcane) | `00 61 05 14 b0` |
| 5 | 17 | Magic Screen | マジックスクリーン | battle | A (party) | 5 (arcane) | `00 21 05 1c a0` |
| 6 | 18 | Frost Blizzard | フロストブリザード | battle | 6 (enemy group) | 1 (water/cold) | `00 21 01 05 60` |
| 6 | 19 | Earthquake | アースクウェイク | battle | 7 (all enemies) | 0 (earth) | `00 20 00 0d 70` |
| 6 | 20 | Rainbow Ray | レインボーレイ | battle | 6 (enemy group) | 5 (arcane) | `00 20 05 15 60` |
| 6 | 21 | Sun Ray | サンレイ | battle | 6 (enemy group) | 6 (holy/life) | `00 20 06 1d 60` |
| 6 | 22 | Astral Gate | アストラルゲート | battle | 6 (enemy group) | 6 (holy/life) | `00 20 06 05 60` |
| 6 | 23 | Dissolve | ディゾルヴ | battle | 1 (1 enemy) | 5 (arcane) | `00 21 05 0d 10` |
| 7 | 24 | Nuclear Blast | ニュークリアブラスト | battle | 7 (all enemies) | 2 (fire) | `00 21 02 06 70` |
| 7 | 25 | Teleport | テレポート | battle+camp | A (party) | 5 (arcane) | `00 60 05 0e a0` |
| 7 | 26 | Anti-Magic Shell | アンチマジックシェル | battle | A (party) | 5 (arcane) | `00 21 05 16 a0` |
| 7 | 27 | Wish | ウィッシュ | battle | 0 (none/field) | 5 (arcane) | `00 20 05 1e 00` |

#### Priest spells (そうりょの じゅもん)

| Lv | # | Spell (EN) | JP | Where (flags) | Target code | Element code | raw +11..+15 |
|---|---|---|---|---|---|---|---|
| 1 | 28 | Restore | レストア | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 00 91` |
| 1 | 29 | Light | ライト | camp | 0 (none/field) | 7 (none) | `00 40 07 08 01` |
| 1 | 30 | Remove Fear | リムーブフィアー | battle+camp | 9 (1 ally) | 4 (mind) | `00 e0 04 10 91` |
| 1 | 31 | Iron Body | アイアンボディ | battle | 9 (1 ally) | 5 (arcane) | `00 21 05 18 91` |
| 2 | 32 | Healing | ヒーリング | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 01 91` |
| 2 | 33 | Silence | サイレンス | battle | 6 (enemy group) | 3 (air/lightning) | `00 21 03 09 61` |
| 2 | 34 | Yell | エール | battle | A (party) | 4 (mind) | `00 21 04 11 a1` |
| 2 | 35 | Wake Up | ウェイクアップ | battle | 9 (1 ally) | 4 (mind) | `00 20 04 19 91` |
| 2 | 36 | Search Person | サーチパーソン | camp | 0 (none/field) | 7 (none) | `00 40 07 01 01` |
| 3 | 37 | Cure Paralysis | キュアパラライズ | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 02 91` |
| 3 | 38 | Encyclopedia | エンサイクロペディア | battle+camp | A (party) | 7 (none) | `00 60 07 0a a1` |
| 3 | 39 | Continual Light | コンティニュアルライト | camp | 0 (none/field) | 7 (none) | `00 40 07 12 01` |
| 3 | 40 | Inspect | インスペクト | chest | C (chest) | 7 (none) | `00 10 07 1a c1` |
| 3 | 41 | Protection | プロテクション | battle | A (party) | 5 (arcane) | `00 21 05 02 a1` |
| 4 | 42 | Cure Poison | キュアポイズン | battle+camp | 9 (1 ally) | 1 (water/cold) | `00 60 01 03 91` |
| 4 | 43 | Force Field | フォースフィールド | battle+camp | A (party) | 6 (holy/life) | `00 60 06 0b a1` |
| 4 | 44 | War Cry | ウォークライ | battle | A (party) | 4 (mind) | `00 21 04 13 a1` |
| 5 | 45 | Recovery | リカバリー | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 04 91` |
| 5 | 46 | Revive | リバイブ | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 0c 91` |
| 5 | 47 | Stone to Flesh | フレッシュストーン | battle+camp | 9 (1 ally) | 0 (earth) | `00 e0 00 14 91` |
| 5 | 48 | Death Spell | デススペル | battle | 1 (1 enemy) | 5 (arcane) | `00 21 05 1c 11` |
| 6 | 49 | Magic Armor | マジックアーマー | battle | A (party) | 5 (arcane) | `00 21 05 05 a1` |
| 6 | 50 | Cure All | キュアオール | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 0d 91` |
| 6 | 51 | Bless | ブレス | battle | A (party) | 7 (none) | `00 21 07 15 a1` |
| 6 | 52 | Recall Word | リコールワード | camp | A (party) | 7 (none) | `00 40 07 1d a1` |
| 7 | 53 | Elixir Light | エリクサーライト | battle+camp | A (party) | 6 (holy/life) | `00 e0 06 06 a1` |
| 7 | 54 | Holy Word | ホーリーワード | battle | 7 (all enemies) | 6 (holy/life) | `00 21 06 0e 71` |
| 7 | 55 | Resurrection | リザレクション | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 16 91` |

#### Valiant Prayers (ヴァリアントの じゅもん)

| Lv | # | Spell (EN) | JP | Where (flags) | Target code | Element code | raw +11..+15 |
|---|---|---|---|---|---|---|---|
| 1 | 56 | Healing to Thee | なんじにいやしを | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 00 92` |
| 1 | 57 | Be Thou Whole | なんじすこやかなれ | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 08 92` |
| 2 | 58 | Be Thou Healed | なんじいやされよ | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 01 92` |
| 2 | 59 | Vigor to Thee | なんじにかつりょくを | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 09 92` |
| 3 | 60 | Grace to Thee | なんじにかごあれ | battle | 9 (1 ally) | 5 (arcane) | `00 21 05 02 92` |
| 3 | 61 | Be Thou Guarded | なんじまもりたもう | battle | 9 (1 ally) | 5 (arcane) | `00 21 05 0a 92` |
| 4 | 62 | Be Ye All Whole | みなすこやかなれ | battle+camp | A (party) | 6 (holy/life) | `00 e0 06 03 a2` |
| 4 | 63 | Might to Thee | なんじにちからを | battle | 9 (1 ally) | 6 (holy/life) | `00 21 06 0b 92` |
| 5 | 64 | Be Ye All Healed | みないやされよ | battle+camp | A (party) | 6 (holy/life) | `00 e0 06 04 a2` |
| 5 | 65 | Be Ye All Guarded | みなをまもりたもう | battle | A (party) | 5 (arcane) | `00 21 05 0c a2` |
| 6 | 66 | Might to Ye All | みなにちからを | battle | A (party) | 6 (holy/life) | `00 21 06 05 a2` |
| 6 | 67 | Grace to Ye All | みなにかごあれ | battle | A (party) | 5 (arcane) | `00 21 05 0d a2` |
| 7 | 68 | A Miracle for Thee | なんじきせきあれ | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 06 92` |
| 7 | 69 | O God | かみよ | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 0e 92` |
| 7 | 70 | Heaven, Smite Them | てんばつくだされよ | battle | 6 (enemy group) | 6 (holy/life) | `00 21 06 16 62` |
| 7 | 71 | Begone, Evil | あしきちからされ | camp | D (?) | 6 (holy/life) | `00 c0 06 1e d2` |

#### Avenger Arts (アベンジャーの じゅもん)

| Lv | # | Spell (EN) | JP | Where (flags) | Target code | Element code | raw +11..+15 |
|---|---|---|---|---|---|---|---|
| 1 | 72 | Grudge Aura | うらみのオーラ | battle | 8 (caster) | 5 (arcane) | `00 21 05 00 83` |
| 1 | 73 | Blade of Fear | きょうふのけん | battle | 1 (1 enemy) | 4 (mind) | `00 21 04 08 13` |
| 2 | 74 | Nightmare Blade | あくむのけん | battle | 1 (1 enemy) | 4 (mind) | `00 21 04 01 13` |
| 2 | 75 | Binding Blade | そくばくのけん | battle | 1 (1 enemy) | 4 (mind) | `00 21 04 09 13` |
| 3 | 76 | Blade of Enmity | おんしゅうのけん | battle | 1 (1 enemy) | 7 (none) | `00 21 07 02 13` |
| 3 | 77 | Blade of Madness | きょうきのけん | battle | 6 (enemy group) | 4 (mind) | `00 21 04 0a 63` |
| 4 | 78 | Hatred Aura | にくしみのオーラ | battle | 8 (caster) | 5 (arcane) | `00 21 05 03 83` |
| 4 | 79 | Cursed Blade | のろいのけん | battle | 1 (1 enemy) | 0 (earth) | `00 21 00 0b 13` |
| 5 | 80 | Wrath Aura | いかりのオーラ | battle | 8 (caster) | 5 (arcane) | `00 21 05 04 83` |
| 5 | 81 | Life Stealer | いのちうばいしもの | battle | 1 (1 enemy) | 5 (arcane) | `00 21 05 0c 13` |
| 6 | 82 | Vengeance Blade | ふくしゅうのけん | battle | 1 (1 enemy) | 7 (none) | `00 21 07 05 13` |
| 7 | 83 | Hellish Wail | あびきょうかん | battle | 6 (enemy group) | 7 (none) | `00 21 07 06 63` |

#### Musashi Arts (ムサシの じゅもん)

| Lv | # | Spell (EN) | JP | Where (flags) | Target code | Element code | raw +11..+15 |
|---|---|---|---|---|---|---|---|
| 1 | 84 | Blunt Strike | みねうち | battle | 1 (1 enemy) | 4 (mind) | `00 21 04 00 14` |
| 1 | 85 | Counter Cut | かえすがたな | battle | 2 (?) | 7 (none) | `00 21 07 08 24` |
| 2 | 86 | Meditation | めいそう | battle+camp | 8 (caster) | 6 (holy/life) | `00 e0 06 01 84` |
| 2 | 87 | Triple Slash | さんれんぎり | battle | 3 (?) | 7 (none) | `00 21 07 09 34` |
| 3 | 88 | Fighting Spirit | きこん | battle | 6 (enemy group) | 4 (mind) | `00 21 04 02 64` |
| 3 | 89 | Four Lights Cut | よんこうざん | battle | 4 (?) | 7 (none) | `00 21 07 0a 44` |
| 4 | 90 | Blade Lock | つばぜりあい | battle | 8 (caster) | 5 (arcane) | `00 21 05 03 84` |
| 4 | 91 | Rainfall Slash | さみだれぎり | battle | 5 (?) | 7 (none) | `00 21 07 0b 54` |
| 5 | 92 | Whirl Slash | たてまわり | battle | 6 (enemy group) | 7 (none) | `00 21 07 04 64` |
| 6 | 93 | Read the Blade | みきり | battle | 8 (caster) | 5 (arcane) | `00 21 05 05 84` |
| 6 | 94 | Mind's Eye Blade | しんがんのけん | battle | 1 (1 enemy) | 7 (none) | `00 21 07 0d 14` |
| 7 | 95 | Wild Dance Blade | らんぶのけん | battle | 7 (all enemies) | 7 (none) | `00 21 07 06 74` |

#### Kunoichi Arts (くのいちの じゅもん)

| Lv | # | Spell (EN) | JP | Where (flags) | Target code | Element code | raw +11..+15 |
|---|---|---|---|---|---|---|---|
| 1 | 96 | Trap Breaker | からくりやぶり | chest | C (chest) | 7 (none) | `00 10 07 00 c5` |
| 1 | 97 | Illusion | げんかく | battle | 1 (1 enemy) | 4 (mind) | `00 21 04 08 15` |
| 2 | 98 | Substitution | かわりみ | battle | 9 (1 ally) | 5 (arcane) | `00 21 05 01 95` |
| 2 | 99 | Hunger Pill | きかつがん | battle+camp | 9 (1 ally) | 6 (holy/life) | `00 e0 06 09 95` |
| 3 | 100 | Smokescreen | えんまく | battle | 7 (all enemies) | 7 (none) | `00 20 07 02 75` |
| 3 | 101 | Sleep Powder | ねむりごな | battle | 6 (enemy group) | 4 (mind) | `00 21 04 0a 65` |
| 4 | 102 | Fire Art | かとん | battle | 6 (enemy group) | 2 (fire) | `00 21 02 03 65` |
| 4 | 103 | Shadow Dance | かげまい | battle | 1 (1 enemy) | 7 (none) | `00 21 07 0b 15` |
| 5 | 104 | Numbing Drug | しびれぐすり | battle | 6 (enemy group) | 4 (mind) | `00 21 04 04 65` |
| 5 | 105 | Shadow Double | かげぼうし | battle | 9 (1 ally) | 5 (arcane) | `00 21 05 0c 95` |
| 6 | 106 | Mist Slash | かすみぎり | battle | 2 (?) | 7 (none) | `00 21 07 05 25` |
| 6 | 107 | Izuna Drop | いずなおとし | battle | 1 (1 enemy) | 7 (none) | `00 21 07 0d 15` |
| 7 | 108 | Thunder | いかづち | battle | 7 (all enemies) | 3 (air/lightning) | `00 21 03 06 75` |

#### Summons (しょうかんしの じゅもん)

| Lv | # | Spell (EN) | JP | Where (flags) | Target code | Element code | raw +11..+15 |
|---|---|---|---|---|---|---|---|
| 1 | 109 | Zombie | ゾンビ | battle+camp | 0 (none/field) | 5 (arcane) | `00 60 05 00 06` |
| 1 | 110 | Ghoul | グール | battle+camp | 0 (none/field) | 5 (arcane) | `00 60 05 08 06` |
| 2 | 111 | Lion of Hell | ライオン オブ ヘル | battle+camp | 0 (none/field) | 5 (arcane) | `00 60 05 01 06` |
| 2 | 112 | Minotaur | ミノタウロス | battle+camp | 0 (none/field) | 5 (arcane) | `00 60 05 09 06` |
| 3 | 113 | Djinni | ジィニー | battle+camp | 0 (none/field) | 3 (air/lightning) | `00 60 03 02 06` |
| 3 | 114 | Ifrit | イフリート | battle+camp | 0 (none/field) | 2 (fire) | `00 60 02 0a 06` |
| 4 | 115 | Dao | ダオ | battle+camp | 0 (none/field) | 0 (earth) | `00 60 00 03 06` |
| 4 | 116 | Marid | マリッド | battle+camp | 0 (none/field) | 1 (water/cold) | `00 60 01 0b 06` |
| 5 | 117 | Titan | タイタン | battle+camp | 0 (none/field) | 7 (none) | `00 60 07 04 06` |
| 5 | 118 | Greater Demon | グレーターデーモン | battle+camp | 0 (none/field) | 5 (arcane) | `00 60 05 0c 06` |
| 6 | 119 | Vampire Lord | ヴァンパイアロード | battle+camp | 0 (none/field) | 5 (arcane) | `00 60 05 05 06` |
| 6 | 120 | Shadow Dragon | シャドウドラゴン | battle+camp | 0 (none/field) | 6 (holy/life) | `00 60 06 0d 06` |
| 7 | 121 | Magic Gate | まどうゲート | battle+camp | 0 (none/field) | 7 (none) | `00 60 07 06 06` |
| 7 | 122 | Ancient One | いにしえからのもの | battle+camp | 0 (none/field) | 7 (none) | `00 60 07 0e 06` |
| 7 | 123 | From Beyond | かなたよりのもの | battle+camp | 0 (none/field) | 7 (none) | `00 60 07 16 06` |
| 7 | 124 | Unspeakable | けいようしがたきもの | battle+camp | 0 (none/field) | 7 (none) | `00 60 07 06 06` |

### 10.3 Learning

Code: (`2A:416D` at creation and level-up; `2A:417F` after a class change.
1. **Guaranteed spell** (`2A:418B`): when the new character level equals the opening level of a spell level
   (§5.3) - exactly that level, not later - the character learns **one random spell of that spell level**
   (`Random(count−1)`; re-rolling a spell already known gives nothing). Minimum character level per school
   (first byte of each table): Mage/Priest 1, Bishop's Priest 4, Samurai 4, Lord 4, special schools 5.
   Special rule: if the guaranteed Priest level-6 spell is Recall Word, the character also learns one of Magic
   Armor, Cure All or Bless (`2A:42F0`).
2. **Extra spells** (`2A:4311` Mage with IQ, `2A:4363` Priest with PIE, `2A:43BA` special schools 9-12): for every
   spell not yet known in each spell level where the character already knows at least one spell, roll
   `Random(99) < chance`:

   | Stat | <=11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|
   | Mage (IQ) / Priest (PIE) `2A:412E` | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
   | Valiant (PIE) `2A:413A` | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 10 | 15 | 20 | 25 | 25 |
   | Avenger (VIT) `2A:4146` | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 10 | 15 | 15 | 20 | 25 |
   | Musashi (VIT) `2A:4152` | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 7 | 12 | 12 | 15 | 20 |
   | Kunoichi (LUK) `2A:415E` | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 7 | 7 | 7 | 12 |

   Values above 22 run past each 12-entry table into the next one (e.g. IQ 23 reads the Valiant table: 5%). Only an
   Elf can reach IQ 20, so the Mage table's top entries are rarely used; a Hobbit Kunoichi with LUK 23-24 reads
   past the end (guess: low values).
3. **No stat drives the guaranteed spell** (for any class): the routine looks up a chance from a stat
   (`2A:428B-429F`, table `2A:412E`) but never uses it. For a Bishop that unused lookup reads IQ in both passes
   (Mage `2A:41F9`, Priest `2A:4214`), which is where the old wording came from. **Extra spells**: Mage spells with
   IQ (`2A:432C`), Priest spells with PIE (`2A:437B`), for Bishops as for everyone. Corrected 2026-11-12: was "Bishops
   use IQ for the guaranteed roll of both schools".
4. Spells of other schools learned in a previous class stay known and castable (§10.4).

### 10.4 Spell slots

Code: (`2A:45F3` + `2A:4737`, run at every inn stay, level-up and class change.
For each school and spell level i:
- known_i = number of spells known at that level; slots = known_i (`2A:45F3`, applies to Mage and Priest for every
  class, so ex-casters keep "one cast per known spell").
- If the current class uses the school and the character level L >= opening level t_i: slots =
  `min(9, max(known_i, L − t_i + 1))`. No known spell at a level = 0 slots.

Example, Mage: level-1 slots = L at levels 1-8, then 9; level-7 slots open at character level 13 with 1.
Example, Samurai: Mage level-1 slots appear at character level 4 (1 slot), reach 9 at level 12.
The camp/sheet shows the current remaining slots per level as "n/n/n/n/n/n/n" (`2A:4B7B`).

### 10.5 Summoner pacts

Code: (maze events, `2D:6560`, table `2D:63BB`.
Summons are never learned at level-up (`2A:41D5` returns for class 13). A maze event shows a monster in a magic
circle: "From the pattern's center X appeared! Will you form a pact?" (`2D:44CF`). A Summoner of at least the
listed level learns the summon (bit in `+39`); if that slot level had 0 slots it gets 1 ("The pact is sealed.").
X is the **summon spell's name**: the event copies the spell record (`2D:657F` -> `0:24E8`, bank 24 `$6C95`, id
109-124), not a monster record. Emulator (JP, F1 (15,15), member 0 poked to Summoner level 40): "もようの ちゅうしんから
ゾンビが あらわれた" (Zombie), then the pact bit 0 of `+$39` and Summons slot level 1 = 1 (`work/re/contradictions/circle.py`).
monsters.md §8 had read the same ids as bestiary monsters (corrected there).

| Summon (JP) | Min. level | Slot level | | Summon (JP) | Min. level | Slot level |
|---|---|---|---|---|---|---|
| Zombie (ゾンビ) | 3 | 1 | | Dao (ダオ) | 16 | 4 |
| Ghoul (グール) | 4 | 1 | | Marid (マリッド) | 17 | 4 |
| Lion of Hell (ライオン オブ ヘル) | 6 | 2 | | Titan (タイタン) | 20 | 5 |
| Minotaur (ミノタウロス) | 10 | 2 | | Greater Demon (グレーターデーモン) | 23 | 5 |
| Djinni (ジィニー) | 14 | 3 | | Vampire Lord (ヴァンパイアロード) | 27 | 6 |
| Ifrit (イフリート) | 15 | 3 | | Shadow Dragon (シャドウドラゴン) | 31 | 6 |
| | | | | Magic Gate (まどうゲート) | 34 | 7 |
| | | | | Ancient One (いにしえからのもの) | 36 | 7 |
| | | | | From Beyond (かなたよりのもの) | 37 | 7 |
| | | | | Unspeakable (けいようしがたきもの) | 38 | 7 |

Which floor holds which circle: see `dungeon.md` (not traced here).

---

## 11. Open questions / not found

- **Spell effects** (damage dice, durations, success rolls) live in the battle/spell banks (24, 32) and were not
  traced; byte 13 (element) and the target nibble are pattern guesses.
- **Bonus re-roll**: whether backing out re-rolls the bonus (likely) was not tested.
- **Record fields** `+30`, `+38`, `+57`, `+61`, `+66-67`, `+6A-6F`: meaning unknown.
- **Race byte 6** (6/6/7/6/5): unused in the code read.
- **Status wear-off in battle**, poison per-step damage, silence duration: not traced.
- **Inn alternate mode** (`27:4D9B`: when `$CB9A` bit 7 is set the Inn uses another path that charges 10 × level
  for one full-heal night, `27:4E05`): what sets the flag was not traced.
- **Item class change requirements**: only gender checks were found in `2A:5EF6`; equip/alignment bits of the five
  items may be the real gate (items.md).
- Swings per round and to-hit by class: items.md §4 (class mapping not finished there either).
