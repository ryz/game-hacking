# Wizardry Empire (GBC, Rev 1): items and economy, design reference

Tracer, 2026-11-12. Every number comes from the original Japanese Rev 1 ROM (`rom/wizardry_empire_j.gbc`). Addresses
are written `BB:AAAA` with the bank in hex (bank `$28` = 40 decimal). A formula marked **(code)** was read from the
routine named next to it. **(data)** means it was read from a ROM table. **(display)** means it comes from the museum's
own description text. **(inferred)** is my reading and has not been confirmed in code. Nothing here was checked in the
emulator, except that the party record layout was read from a JP battle savestate. Scratch scripts and disassembly
dumps are in `work/design/items/`.

The full 224-item table is generated into **`docs/design/items_table.md`** (`work/design/items/gen_table.py`).

---

## Overview (two-minute read)

- **Items.** There are 224 item types. Each has one fixed 40-byte record (bank 40 `$4000`). Items do not vary: there are
  no random enchantments or durability. An inventory slot holds only an item id and 4 state bits: equipped, cursed
  (stuck), unidentified, and off-hand. Each character carries 8 slots.
- **Weapons.** Damage per swing is `NdS + B`. The number of swings per round is the class/level count plus the weapon's
  bonus (daggers +2 to +6, Swift Sword +7). To-hit works on a d20: chance = (20 - miss)/20, with the miss value clamped
  so the hit chance always stays between 5% and 95%. Some weapons get ×1.5 or ×2 damage against a monster family.
  There are launchers (bow, crossbow, sling) with matching ammo, two-handed weapons, a parry dagger, and dual wielding
  for the Musashi class only.
- **Armour.** Each equipped piece adds a signed AC value; negative is better. The slots are main hand, off hand
  (shield, parry dagger or ammo), body, helm, gloves and one "other" accessory.
- **Curses and alignment.** Equipping a cursed item, or an item your alignment may not use, locks it in place. An
  uncurse at the shop destroys the item and costs half its price. The Avenger class is immune to both locks and to
  the HP drain of cursed gear.
- **Unidentified items** show a generic name (Sword, Ring...). Identifying costs half the price at the shop. In camp,
  the chance is `(6 + level - item level)/20`; a failed attempt can make the identifier Afraid.
- **Shop.** Buy at full price, sell at ceil(price/2). A new game starts with 65 items in stock, 39 of them unlimited.
  Items you sell are added to the stock, so the shop is the long-term store for rare finds.
- **Inn.** A stay is 7 days. Each day the room heals a dice amount: Cots 3d6+2, Economy 10d6, Suite 8d10+20, Royal
  10d20+20. The room price is charged for each day on which the character was still hurt. Spells are restored in every
  room. Every day except in the Stables adds one day of age (a year is 360 days). As written, the code kills a
  character at the birthday that reaches age 57.
- **Temple.** Fee = rate × level. The rate is 10 for Afraid/Asleep, 30 Paralyzed, 50 Stoned, 100 Dead, 300 Ashes. Dead
  and Ashes need a roll: about 10-97% success depending on age and vitality. On failure Dead becomes Ashes and Ashes
  becomes Lost. A success costs vitality (61%) and ages the character 1-3 years (89%).
- **Gold.** Each monster carries a fixed gold value; the sum is split evenly among the conscious survivors. Only
  guarded squares (fixed fights) give a chest. A chest adds `10 × (rand(0..V) + 4)` gold, where V is the chest value,
  and tries to give 1-4 items from 47 item pools. The trap is picked by chest tier from 14 kinds, Fire Bolt being the
  most common.

---

## 1. The item record (bank 40 `$4000 + 40 × id`)

The game copies a record to `$C54F` with `0:24FF` (40 bytes, `0:0C97`) before every use, so the `$C5xx` address of a
field is `$C54F + offset`. The column "who reads it" lists the routines that prove the meaning.

| Off | RAM | Field | Values / encoding | Who reads it (proof) |
|---|---|---|---|---|
| 0-16 | `$C54F` | Name | 16 chars + `$00` | everywhere |
| 17 | `$C560` | Unidentified class | 0-24, index into the generic-name list `49:567D` (Axe, Arrow, Stone, Scythe, Odd object, Staff, Sword, Dagger, Hammer, Cord, Long staff ×2, Staff, Spear, Bow, Armor, Robe, Shield, Helm, Gloves, Odd object, Scroll, Potion, Cloth, Ring). It also picks the attack verb. | `0:3748`, museum `41:64CE`, battle verb `32:4342` |
| 18 | `$C561` | Slot type | 0 one-handed weapon, 1 arrows, 2 quarrels, 3 sling stones, 4 parry dagger (Main Gauche), 5 bow, 6 crossbow, 7 sling, 8 body armour (robes too), 9 shield, 10 helm, 11 gloves, 12 other (accessories, consumables), 13 two-handed weapon | equip filter `2A:629A`, `2A:6037`, `32:4329` |
| 19-21 | `$C562-64` | Price | 23-bit little-endian gold (byte 21 bit 7 masked off) | shop `29:4670`, museum `41:6555` |
| 21 bit 7 | `$C564` | "Cannot be sold" | no item has it set | shop sell check `29:55A3` -> "That item can't be sold." |
| 22 | `$C565` | Classes, part 1 | bit 0 Fighter, 1 Mage, 2 Priest, 3 Thief, 4 Bishop, 5 Samurai, 6 Lord, 7 Ninja | `0:2B8C` bit test with class id (`22:434B`, `2A:6234`, shop `29:4A19`) |
| 23 | `$C566` | Classes, part 2 | bit 0 Archer (class 8), 1 Valiant (9), 2 Avenger (10), 3 Musashi (11), 4 Kunoichi (12), 5 Summoner (13) | same bit test (class id 8-13 reaches into this byte); museum `41:65BE` |
| 24 | `$C567` | Alignment / curse | bit 0 Good, 1 Neutral, 2 Evil may equip it without it sticking; **bit 7 = cursed** | `2A:6124` (equip), `22:6FE5`, `32:41A8`, museum `41:6680` |
| 25 | `$C568` | Damage dice count N | 0 = no damage (non-weapon) | `32:447D` |
| 26 | `$C569` | Dice sides S | per die: `rand(0..S-1)` | `32:448B` |
| 27 | `$C56A` | Damage base | damage = Σ N × rand(0..S-1) + base, so min = base, max = base + N(S-1), the same as `NdS + (base - N)` | `32:44A0`; museum shows `base ~ base+N(S-1)` (`41:64E6`) |
| 28 | `$C56B` | AC modifier | signed; added to the wearer's AC (sum over equipped items, `2A:63FE` -> `$C4E7`); negative = better | `2A:63FE`, museum `41:651D` |
| 29 | `$C56C` | To-hit bonus | unsigned; subtracted from the miss threshold (see 4.2). Values 0-8, plus 47-50 on 20 cheap or heavy weapons (see Open questions) | `32:443B`, `32:48C7` |
| 30 | `$C56D` | Extra swings | added to the attacker's swings per round | `32:444A`, `32:48D6` |
| 31 | `$C56E` | Range / throw | bits 2-3 = range 0 S, 1 M, 2 L, 3 "-" (table `41:6374` "SML-"); **bit 7 = can be thrown**; bits 0-1 meaning unknown | museum `41:653E`, equip `2A:5FD9`, battle flags `22:4362` |
| 32 | `$C56F` | Kept after a throw | % chance a thrown item comes back (else it is lost) | throw `22:706D` (`rand(0..99) < v` keeps it) |
| 33 | `$C570` | Use spell | bits 0-5 = spell effect (museum text = use table entry `v+10`); **bit 7 = usable in battle, bit 6 = usable in camp** | `22:4356`, camp use `2A:6CB2`, museum `41:6638` |
| 34 | `$C571` | Break on use | % chance the item is used up after a use (100 = always consumed) | `2E:4D01` (`rand(0..99) < v` -> remove via `2E:638B`) |
| 35 | `$C572` | Special power | 1 Luck +1, 2 Age -1, 3 Thief becomes Ninja, 4 becomes Ninja, 5-9 become Valiant / Avenger / Musashi / Kunoichi / Summoner (see 5.3) | `2A:5E68`, `2A:5EF6` |
| 36 | `$C573` | Special power: vanish chance | 0 = item changes form; >= 100 = always used up; else % chance it is used up instead of changing | `2A:5E77` |
| 37 | `$C574` | HP per step | signed; HP regained per step while equipped (negative = drain, used by cursed gear). The equipped total goes to `$C4F9` | `2A:5F99` |
| 38 | `$C575` | Special property | index into the museum "special" texts (0-31). Codes 15-20 are slaying, applied in combat (4.4) | `32:455A`, `2A:6404`, museum `41:665E` |
| 39 | `$C576` | Level / use mode | low nibble = **item level** (1-15, identification difficulty); high nibble = use mode of usable items: 0 none, 6 enemy group(s), 7 all enemies, 9 one ally, A party / self **(inferred from which items have it)** | identify `2A:6B47`, battle use `22:516F`, camp use `2A:6CA8` |

Example, Hand Axe (id 0): `00 00 3C 00 00 E1 1A 07 01 06 02 00 00 00 80 46 ...`, read from byte 17 on.
- Byte 17: class Axe. Byte 18: one-handed. Bytes 19-21: price 60.
- Classes: Fighter, Samurai, Lord, Ninja, Valiant, Musashi, Kunoichi. Any alignment.
- Damage 2-7 (1d6+1). Range S. Throwable, kept 70% of the time.

### Inventory slot (party record, WRAM `$C880 + $80 × member`)
- Items are 8 pairs `[id][flags]` at record `+$11..+$20`; id `$FF` = empty. Read from a JP battle savestate and from
  `22:4330`.
- Flag bits: **7 = equipped**, 6 = unidentified, 5 = cursed/stuck (cannot be unequipped), 4 = worn in the off hand.
- Battle start computes bits 0-2: bit 2 = class may equip it, bit 1 = usable in battle, bit 0 = throwable and not
  equipped (`22:4343-436D`).
- Items found in chests arrive with flags `$40` (unidentified, `25:51E9`).
- Other fields of the record, for reference:
  - age: `+$10` = age × 2, plus bit 0. `+$0F` = days into the year.
  - status: `+$0C`.
  - level: `+$0D/+$0E`.
  - stats: `+$51..+$56` = STR, IQ, PIE, VIT, AGI, LUK.
  - gold: `+$59` (4 bytes).
  - HP: max at `+$62`, current at `+$64`.

---

## 2. Equipment rules

The equip screen walks six steps (`$D00C` = 0-5). Slot names are from `49:5703`: Weapon, Off-hand, Armor, Helm,
Gloves, Other. Filter `2A:629A`:

| Step | Accepts slot types | Extra rules (code `2A:62AE-637F`) |
|---|---|---|
| 0 Weapon | 0, 4, 5, 6, 7, 13 | must be allowed for the class (bytes 22-23) |
| 1 Off-hand | 4 (parry dagger), 9 (shield) | Two-handed main weapon: nothing. Bow: arrows only (1). Crossbow: quarrels (2). Sling: stones (3). **Musashi (class 11) may also put a one-handed weapon (0) here** (dual wield). |
| 2 Armor | 8 | |
| 3 Helm | 10 | |
| 4 Gloves | 11 | |
| 5 Other | 12 | one accessory |

- **Class check.** An item whose class bit is clear cannot be equipped. The shop marks such items for the selected
  character (`29:4A19`); items with "camp use" (byte 33 bit 6) are never marked.
- **Curse and alignment lock** (`2A:6116-6135`). On equipping, the item gets flag 5 (stuck) if the record is cursed
  (byte 24 bit 7) or the character's alignment bit is clear. Exception: the **Avenger** (class 10) never gets stuck.
  `32:4199` repeats the alignment check on equipped items (it runs from a bank-50 routine, trigger not traced) and
  shows message `49:5594`.
- **Avenger and HP drain.** For an Avenger, negative HP-per-step values (byte 37 >= `$80`) are ignored (`2A:5F8A`).
- **Launchers without ammo** (`32:4358-43A7`). A bow, crossbow or sling without matching ammo in the off hand sets
  `$C4FA` bit 6. Each die then rolls `rand(0..S/4)` instead of `rand(0..S-1)` (`32:4491`). With ammo, the slaying
  property comes from the ammo record (`$DD7F`, `32:4555`), not from the launcher.
- **Clockwork Doll** (id 185, accessory). While equipped it sets `$C4FC` bit 6, and every hit does double damage
  (`2A:63EA`, `32:4521`).

---

## 3. Using items (battle and camp)

### 3.1 Spell items (byte 33)
- The spell effect is `v & $3F`. Bit 7 means usable in battle, bit 6 usable in camp.
- After each use, the item breaks with probability byte 34 % (`2E:4D01`).
- Examples:
  - Healing Potion: Healing, battle, 100% consumed.
  - Staff of Healing: Healing, battle+camp, breaks 25%.
  - Ring of Warping: Teleport, camp, breaks 25%.
  - Map Record Sheet: shows the map, camp, breaks 30%.
  - Revival Charm: cures death, ashes and lost, battle+camp, 100% consumed, price 1,000,000.
- The high nibble of byte 39 is the use mode (inferred, see section 1). Spell names are the museum texts; the spell
  power behind each effect was not traced.

### 3.2 Throwing (command "Throw")
- Only items with byte 31 bit 7 can be thrown, and only when not equipped. That covers hand axes, daggers, flails,
  spears, the Gladius, maces, shuriken, Gungnir, Longinus, healing potions and stones, the Exorcism Charm and the
  Potion of Poison.
- After the throw, the item is kept with probability byte 32 %. Otherwise it is removed (`22:706D`).
- Holy items have thrown-at-undead texts (museum specials 22-25: 32-48, 16-24, 4-8 damage, "can destroy undead"). Those
  damage numbers are display text; the throw damage code was not traced.

### 3.3 Special powers (byte 35; prompt "Use its special power?")
Code `2A:5E53-5F5C`:
1. The item is unequipped.
2. The effect runs:
   - 1 = Luck +1 (`26:52D5`).
   - 2 = age -1 year, not below 12 (`$C49F`).
   - 3 = becomes Ninja, only if the user is a Thief.
   - 4 = becomes Ninja.
   - 5-9 = class becomes 9-13 (Valiant, Avenger, Musashi, Kunoichi, Summoner).
   - Ninja needs record `+$0B` = 0 and Kunoichi needs it non-zero. This is probably gender, 0 = male (inferred).
3. Byte 36 decides what happens to the item:
   - 100: the item is used up (Rabbit's Foot, Youth Stone, Thieves' Dagger, Butterfly Knife). By code order, the
     Thieves' Dagger is also used up when a non-Thief uses it (inferred).
   - 30 (the five class items): 30% chance the item vanishes. Otherwise it changes into its class version (table
     below).
4. A successful change also sets bit 0-4 of `$C5C6` (class unlocked; the museum uses it to show the hidden class
   letters).

| Item | Becomes | Class |
|---|---|---|
| Guardian Shield (218) | Valiant Shield (217) | Valiant |
| The Avenger (213) | Avenger Sword (212) | Avenger |
| Warrior's Helm (220) | Musashi's Helm (219) | Musashi |
| Charming Gloves (222) | Kunoichi Gloves (221) | Kunoichi |
| Magic Robe (216) | Summoner's Robe (215) | Summoner |

---

## 4. Weapons in combat (bank 50, `32:42F1-4628`; the second copy `32:48xx` is the same formula)

### 4.1 Swings per round
- swings = `$C508` + 1 + weapon byte 30.
- `$C508` = (level - 1) / k per class, capped (`22:4B53-4CB5`). Examples: one class uses k=5, cap 9; another k=10,
  cap 3. Mapping each routine to its class was not traced.
- Only the main-hand weapon's record is used (`$C4F7`).

### 4.2 To-hit (per swing)
1. `miss = clamp((attacker_hit - weapon byte 29) - target_AC, 1, 19)` (`32:4441`, `32:569E`).
   - attacker_hit = `$C502 + $C503`. Per class, `$C502` = `max(0, K - level) - M`. For example the first class uses
     K 33, M 15, so 18 - level, down to -15 (`22:4B53`). Lower is better, like a THAC0.
   - target_AC = target record `+5 + +6`.
   - Some attacker states (`$C4FF` = `$0D`) lower the threshold by 4; others (`$0E`, or `&$7F` = 2) raise it by 4.
2. Roll `rand(0..19)` (a d20). **Hit if the roll >= miss**, so the hit chance is between 5% and 95%.
3. Long-range weapons (main range L) against targets with `$C54D` bit 1 hit only on a natural 0 (5%, `32:4450`).
   The meaning of the target flag was not traced.

### 4.3 Damage per hit (`32:4474-4537`)
1. `Σ N × rand(0..S-1) + base`, from bytes 25-27. Without ammo a launcher uses `rand(0..S/4)` per die.
2. `+ rand(0..STRtab[STR])`. STRtab (`32:592A`, STR capped at 22): 0 up to STR 12; 13-15: 1; 16-17: 2; 18: 3; 19: 4;
   20: 6; 21: 8; 22: 10.
3. Unarmed: `rand(0..T2[STR]) + 1`. T2 is at `32:5941` (0, 1 from STR 7 ... 12 at STR 22). Ninjas add level/4 to that
   range.
4. Attacker state `$0D`: ÷2 (minimum 1). State `$0E` or `&$7F` = 2: ×1.25.
5. Sleeping target (status 2): ×2. Clockwork Doll: ×2.
6. Slaying (4.4).

### 4.4 Slaying (byte 38; target type bits = monster record byte `$0E`, `$C51D`; code `32:454E`)
| Code | Museum text | Target bits | Multiplier | Items |
|---|---|---|---|---|
| 15 | vs Demons, Undead | `&3` | ×1.5 | Sword of Flash |
| 16 | vs Demons, Spirits, Dragons | `&$0E` | ×1.5 | Odin Sword |
| 17 | vs Demons | `&2` | ×1.5 | Silver Quarrel, Kris, Holy Flail, Faust Halberd |
| 18 | vs Undead "damage up 2" | `&1` | ×1.5 | none |
| 19 | vs Undead | `&1` | **×2** | Exorcist Arrow, Holy Cross Sword, Purified Mace |
| 20 | vs Dragons | `&4` | ×1.5 | Dragonslayer |

So monster type bit 0 = undead, bit 1 = demon, bit 2 = dragon, bit 3 = spirit (inferred from the texts). The texts for
18 and 19 swap "up" and "up 2" compared with the code; 18 is used by no item.

Other special codes are passive and are set up at `2A:6420` when equipment changes. Their effects come from the museum
texts; I did not trace the code that applies them:
- 1 teleport, 2 critical +10%, 3 critical +5%, 4/10 water damage ½, 11 fire damage ½.
- 5 Hide +10%.
- 6 / 7 drain evade 50% / 10%.
- 8 healing and cure success +50%.
- 12-14 magic evade 30 / 50 / 85%.
- 27 "no critical bonus".
- 28 elevator key (Key Card), 29 meet the fairy twins (Fairy's Heart).
- 30 / 31 "+5 / -5 HP per step". The real amount is byte 37.

---

## 5. Identification and curses

- **Shop Identify**: fee = ceil(price / 2). Always succeeds and clears flag 6 (`29:5498-54F8`).
- **Camp Identify** ("Identify what?", bank 42 `2A:6B1F`; the class gate was not traced, probably Bishop):
  - L = identifier level (255 if level > 255, `0:2C72`); I = item level (byte 39 & 15).
  - L - I >= 14: always succeeds.
  - Otherwise: succeeds if `rand(0..19) < 6 + L - I`, i.e. chance (6 + L - I)/20, 0 if I >= L + 6.
  - On a failure, LUK decides the chance of turning **Afraid** (`2A:6C43`): LUK <7: 20%, 7-8: 19%, 9-10: 18%, 11-13:
    17%, 14-17: 15%, 18-20: 12%, 21-22: 10%, 23: 7%, 24+: 5%. The fail message is "Oops!" (`26:7689`).
- **Cursed items.**
  - Byte 24 bit 7 marks 36 items. Cursed gear also has negative HP-per-step (e.g. Blood Axe -3, Demon Armor -4,
    Demon Gloves -5).
  - Once equipped, a cursed item is stuck (flag 5). Unequip skips it (`2A:6179`). The shop refuses to buy it.
  - **Shop Uncurse**: fee = ceil(price / 2), and **the item is destroyed** (`29:53F0-545A`, removal `2E:638B`).

---

## 6. Shop (bank 41, "Lorelei")

| Action | Price | Source |
|---|---|---|
| Buy | full price; stock -1 unless the stock is 255 (unlimited) | `29:4670`, stock `29:53B5` |
| Sell | ceil(price / 2); stock +1 (capped at 254); refused for unidentified, cursed or "unsellable" items. An equipped item asks for confirmation | `29:5326`, `29:5394`, checks `29:5576` |
| Uncurse | ceil(price / 2); the item is lost | `29:53F0` |
| Identify | ceil(price / 2) | `29:5498` |
| Pool gold | gathers the party's gold on one member | menu `29:6C21` |

- **Stock** is one byte per item id: WRAM `$CC07`, saved in SRAM `$ADC0`.
- A new game copies the table at bank 46 `$4300` (224 bytes, `2E:5552`). The same pass marks those items as seen in the
  museum, which is why a fresh museum shows 65 items.
- Opening stock: 65 items, 39 unlimited (Hand Axe ... Healing Potion, plus the Revival Charm at 1,000,000 G). The
  limited ones: Great Axe 1, Claws 2, Staff of Healing 1, Gladius 1, Falchion 1, Katana 1, Silver Dagger 3, Kris 3,
  Main Gauche 1, Morning Star 5, Nunchaku 5, Vermilion Spear 1, Lance 1, Long Bow 2, Scale Mail 5, Chain Mail 5, Kite
  Shield 5, Spiked Shield 1, Plate Helm 4, Chain Gloves 3, Shell Amulet 1, Dreaming Stone 1, Scroll of Sleep 5, High
  Heal Potion 15, Elixir 3, Cloak 5. The "Shop" column of items_table.md has every value.
- **Unique items.** `25:5487` checks whether an item already exists in the shop stock, in the party or in the 20-slot
  roster (SRAM `$A000`). The caller and the item list were not traced (inferred: chests do not hand out a second
  copy of some items).

---

## 7. Inn (bank 39, "Aries Inn")

Menu `27:7890`: Stables free, Cots 10, Economy 50, Suite 200, Royal Suite 500 per week. Code `27:5046-5B53`:

| Room | Days | Price per day charged | HP healed per day (table `27:5A96`) | Spells | Ages |
|---|---|---|---|---|---|
| Stables | 1 | 0 | none | restored | no |
| Cots | 7 | 10 | 3d6+2 | restored | yes |
| Economy | 7 | 50 | 10d6 | restored | yes |
| Suite | 7 | 200 | 8d10+20 | restored | yes |
| Royal Suite | 7 | 500 | 10d20+20 | restored | yes |

- **Payment.** At check-in the game tests whether the character can afford one day ("Not enough gold." otherwise).
  Then, for each of the 7 days on which the character is still below max HP, it pays the room price and heals the dice
  amount, capped at max (`27:598F`, `27:5245` with c = 1 = pay).
  - At full HP the remaining days are free.
  - So the menu's "/week" is really a per-day price for each day of healing.
  - A Royal Suite stay from 1 HP can cost up to 3,500 G.
- **Spells.** The far call `2A:45F3` restores spell points every day in every room (inferred from its position; not
  traced).
- **Room index 0** (no menu entry) sets HP to max outright (`27:5B35`). It may be used by another caller; not traced.
- **Ageing** (`27:5208`).
  - Every day outside the Stables adds 1 to a 9-bit day counter (`+$0F`, plus bit 0 of `+$10`).
  - At 360 days the counter wraps and age goes up by 1 (cap 99): a "birthday". Age is kept as age × 2 in `+$10`.
- **Birthday** (`27:532B`): under 57: "Happy birthday!". At **57 or older: "died of old age"**.
  - The character gets status Dead, HP 0, record `+$57` = `$15`, and leaves the party (`27:513D`).
  - The code does roll `rand(0..99 + VIT/2 + LUK/2)` and compares it with `age - 56`. The comparison's result is never
    used (`27:5379-537D`: `call 2B7E / cp b / ld a,$FF`, no branch).
  - So as written every inn birthday at 57+ is fatal. The intended rule was probably "dies if roll < age - 56".
  - **Emulator check (2026-11-12, coordinator):** Fighter (VIT 14, LUK 8) poked to age 56, day 359 (`+$0F`=$67,
    `+$10`=$71), one stay at Cots: "Fighter is asleep." / "...died of old age." and the Fighter left the party; same on
    the Japanese ROM. One sample, so it confirms the death happens, not that the roll is ignored (a single roll at
    VIT/LUK this low could also fail). Control at age 50 / day 359: no birthday at all, and `+$0F`/`+$10` were
    unchanged after the stay (the character was at full HP) - the per-day aging rule above needs a second look.
- **Level-up** checks also run at the inn (`27:53B3`, `27:5958` "more max HP"). Out of scope here.

---

## 8. Temple (bank 39, "Samsara Temple")

**Fee** (`27:6A20`) = rate × the patient's level (16-bit, from the SRAM roster record), paid by a chosen party member
(`27:660A-6645`). "Not enough gold." if short.

| Status (record `+$0C & $3F`) | Rate per level | Outcome |
|---|---|---|
| 1 Afraid, 2 Asleep (anything below 3) | 10 | always cured |
| 3 Paralyzed | 30 | always cured |
| 4 Stoned | 50 | always cured |
| 5 Dead | 100 | roll (below) |
| 6 Ashes, 7 Lost | 300 | roll; Lost is not offered (the temple text lists fear, stone, paralysis, death and ashes) |

**Resurrection roll** (`27:683A-6929`): success if `rand(0..100) < base(age) + bonus(VIT) + 1`, i.e. (base+bonus+1)/101.

| Age | base | | VIT | bonus |
|---|---|---|---|---|
| < 20 | 90 | | < 7 | 0 |
| 20-29 | 80 | | 7 | 1 |
| 30-39 | 65 | | 8-9 | 2 |
| 40-49 | 40 | | 10-14 | 3 |
| 50-69 | 10 | | 15-19 | 4 |
| 70+ | 0 | | 20-21 | 5 |
| | | | 22+ | 6 |

Example: a 25-year-old with VIT 12 has 84/101 = 83%.

- **Failure.** Dead becomes Ashes, Ashes becomes **Lost**. A Lost character is removed from the party list (`27:6903`).
- **Success.** Status cleared, `+$57` = 0, HP set to 1 if it was 0. Then:
  - 61% chance (`rand(0..100) < 61`): VIT -1. The floor is the race minimum (Human 8, Elf 6, Dwarf 10, Gnome 8,
    Hobbit 6, table `27:69AF`), +1 when record `+$0B` is non-zero.
  - 89% chance (`rand(0..99) < 89`): age +1 to +3 years (cap 99).
  - Non-death cures have no side effects (`27:696A`).

---

## 9. Gold sources

- **Monsters.** Each monster record (bank 57) has gold at `+$2E` (16-bit) and EXP at `+$30` (24-bit). These are the
  "Gold:" and EXP values on the museum page (`41:68BA`, `41:68D4`). Every kill adds both to the battle pools (`0:2EF3`:
  EXP `$DD2C`, gold `$DD2F`).
- **Chest bonus.** If the victory has a chest, the gold pool gets `10 × (rand(0..V) + 4)` (`25:5147`), where V is the
  chest value (10.1). A bag of V 3 gives 40-70 G.
- **Split.** EXP and gold are each divided evenly (integer division) among members with status < 3 (OK, Afraid,
  Asleep) (`25:4724`, `25:521D`, divide `0:163F`). Dead, paralysed and stoned members get nothing.
- **Selling** (6), **events** (e.g. the floor-1 "gold coins" square, `docs/re/reach.md`; amount not traced),
  **Pool gold / Divide gold** (moves gold between members).

---

## 10. Chests and traps (bank 37 `$25`)

Only fixed fights on **guarded squares** give a chest (`$C00B` bit 2, set only by `20:5D0B`; `docs/re/reach.md`).
Random encounters give gold only.

### 10.1 Chest value and type (`25:40D8-416B`)
- **Row.** R = the highest monster byte `+$2D` among the groups present.
- **Value.** V = a random byte of row R in the table at bank 55 (`$37`) `$4000 + R×256`. Row R holds values 0..R.
- **Tier.** V gives the chest tier:

| V | Tier | Contents level cap (`$C636`) |
|---|---|---|
| 0-6 | Leather bag | 6 |
| 7-12 | Bronze | 12 |
| 13-18 | Copper | ... (one cap per tier, `25:4198-4646`) |
| 19-24 | Silver | |
| 25-30 | Gold | |
| 31-35 | Platinum | |
| 36-40 | Paulownia | |
| 41-45 | Lacquered | |
| 46 | Jet-black | |
| 47+ | Bewitching | |

- **Row distributions** (full list: `work/design/items/chest_rows.txt`).
  - Rows 0-6: always a bag.
  - Row 12: 11% bag, 89% bronze.
  - Row 24: mostly silver.
  - Row 36: 66% platinum.
  - Rows 49-63: flat, 14-16% bag up to 19% bewitching.

### 10.2 Chest contents (`25:5185-521A`)
1. 1-4 attempts (`rand & 3` + 1). Each picks a random party member.
2. The member must have status < 3. Success if `rand(0..99) < level/2 (max 31) + 2×LUK`.
3. The item comes from list `25:6A02[rand(0..V-1)]`, a random entry. It goes into the first empty slot, unidentified;
   with no empty slot it is lost.
4. There are 47 lists (0-46). Each holds 6-17 ids, with some ids repeated as weights. The full dump is in
   `work/design/items/chest_items.txt`:
   - List 0: starter gear and potions.
   - Around 26-29: the class items (The Avenger, Valiant Shield...).
   - List 46: Revival Charm, Excalibur, Muramasa, **Ura Muramasa**.
5. V >= 48 (some bewitching chests) can index past list 46, into the list data (not checked).
6. Note that `rand(0..V-1)` lets a high chest also roll the low lists.

### 10.3 Traps (`25:47AC`, table `25:551C + tier×256`; handlers `25:50F1`)
The trap is picked per chest tier. Fire Bolt hits the opener for L×d8 (`L + Σ L × rand(0..7)`, L = `$C636`,
`25:4D26`). Bomb hits every member for L×d4; each member dodges with `rand(0..99) < LUK` (`25:4D6E`). The other 11
effects are known only by name (handler addresses: `25:50F1` table).

| Tier | No trap | Fire Bolt | Bomb | Poison Needle | Paralysis Needle | others |
|---|---|---|---|---|---|---|
| Leather bag | 44% | 44% | 3% | 6% | 3% | none |
| Bronze | 25% | 38% | 12% | 12% | 6% | Magic Drain, Alarm, Hand of the Dead, Last Kiss 2% each |
| Copper | 25% | 34% | 12% | 12% | 6% | + Paralysis Gas |
| Silver | 19% | 34% | 12% | 12% | 6% | + Energy Drain, Medusa's Curse |
| Gold | 19% | 31% | 12% | 12% | 6% | + Teleporter |
| Platinum | 19% | 30% | 12% | 12% | 6% | + Level Teleporter |
| Paulownia | 12% | 30% | 12% | 12% | 12% | all 13 kinds |
| Lacquered | 12% | 28% | 12% | 12% | 12% | Hand of the Dead 5% |
| Jet-black | 6% | 28% | 12% | 12% | 12% | Magic Drain, Alarm, Hand of the Dead, Last Kiss 5-6% |
| Bewitching | 6% | 25% | 12% | 12% | 12% | as Jet-black, Paralysis Gas / Medusa 3% |

Exact percentages: `work/design/items/traps.txt`. Trap names: `49:5661` (No trap, Fire Bolt, Bomb, Magic Drain, Energy
Drain, Poison Needle, Alarm, Hand of the Dead, Paralysis Needle, Paralysis Gas, Medusa's Curse, Last Kiss, Teleporter,
Level Teleporter). Disarm/inspect chances were not traced.

---

## 11. Open questions / not found (what was tried)

1. **To-hit values 47-50** (byte 29) on 20 items: Battle Axe, Great Axe, Chain Sickle, Quarterstaff, the staves and
   rods, Shamshir, the whips, Nunchaku, Cursed Flail, Unholy Mace, Lance, Halberd, Sickle Spear, Windmill Glaive and
   Spiked Shield.
   - The code subtracts the whole byte, so these weapons always get the 95% maximum hit chance. That may be intended
     ("easy to hit") or a data quirk. The values are ASCII `/ 0 1 2`.
   - To check: an emulator breakpoint at `32:4444` (D = miss threshold) with a Battle Axe.
2. **Inn old-age death** at 57+ regardless of the roll (section 7). Death confirmed in the emulator (one sample, see
   section 7); "roll ignored" still needs several samples or a breakpoint at `27:5379`. Aging per day: a full-HP
   stay at age 50 did not change the day counter.
3. **Range S/M/L.** Stored in `$C4FA` bits 0-3 (`2A:5FD9`). Which enemy groups each range can reach was not traced.
   Byte 31 bits 0-1 have unknown meaning (1 on most two-handed and heavy weapons, 2 on daggers and claws, 3 on the
   Spiked Shield).
4. **Byte 39 high nibble** (use mode): the reading is inferred. `22:5183` branches on 0 / <7 / 7 / 9.
5. Class-by-class swings (`$C508`) and base to-hit (`$C502`) tables (`22:4B53-4CB5`): one routine per class; which
   routine belongs to which class was not traced.
6. Passive specials (criticals, magic evade, elemental halving, hide, drain evade): the effect values are the museum's
   own texts. The applying code (`2A:6420` sets flags; battle readers) was not traced.
7. Trap effects other than Fire Bolt and Bomb; the disarm, inspect and Calfo-style rules; the gold coins event amount.
8. Chest value V >= 48 and the item-list index (possible over-read). The callers of the unique-item check `25:5487`.
