# Wizardry Empire (GBC, Rev 1): monsters, encounters and combat, technical reference

Tracer, 2026-11-12. All numbers come from the original Japanese Rev 1 ROM (`rom/wizardry_empire_j.gbc`). Addresses
are written `BB:AAAA` with the bank in hex (bank `$39` = 57 decimal). Source tags used below:
- **(code)**: read from the routine named next to it.
- **(data)**: read from a ROM table.
- **(emu)**: seen in the emulator.
- **(inferred)**: my reading, not confirmed in code.

Scratch scripts are in `work/design/monsters/`. The full bestiary (167 monsters, every field) and the encounter tables are
generated into **[../design/monsters_table.md](../design/monsters_table.md)** by `python3 tools/designtables`. The maze and its events are
in [dungeon.md](dungeon.md). Party-side weapon damage, slaying and chests are in [items.md](items.md) (sections 4, 9, 10).

---

## Overview (two-minute read)

- **Bestiary.** There are 167 monsters (ids 0-166), each one fixed 64-byte record (bank 57 `$4820`). Every monster has
  a level, HP dice, AC, a to-hit base, a number of swings per round, damage dice per swing, and a reach (melee, reach
  or ranged). It also has 8 elemental resistances, a type (undead, demon, dragon, spirit...), up to 6 spell schools
  with a top spell level, special hit effects (poison, fear, sleep, paralysis, stone, decapitation, level drain),
  breath, call-for-help and flee chances, EXP, gold, and a chest-quality row. Nothing is randomised per kill except HP.
- **Encounters.** Each map square carries an *encounter area id* (1-105). Ids 1-33 are the normal areas of floors
  1-30. Ids 34-53 are fixed fights used by events. Ids 101-105 cover the damage zones. Each id lists 4 formations,
  and one of the 4 is picked at random. A formation has up to 4 groups (monster + size code). A group holds 1-9
  monsters.
- **Encounter rate.** It is checked after every action in the maze (step, turn, turn-around). The normal chance is
  only **1/512 (0.2 %) per action**. Right after you walk through a door the chance becomes **13/256 (5.1 %) per
  action**, and it stays there until your next plain step or turn-around. So doors are where fights happen. **Guarded
  squares** (fixed spots, 0-21 per floor, 244 in all; dungeon.md 4) always fight once. They are the only fights that give a chest, and they
  re-arm whenever you change floors.
- **To-hit (monster on party).** Roll d20 (0-19). The monster hits if the roll is ≥ `T`, where
  `T = clamp(HitBase + mod − targetAC, 1, 19)`. That gives 5-95 %. The monster swings `Att` times per round. Each hit
  deals `min + N×(dS−1)` damage. Sleeping targets take ×2.
- **Monster AI per round.** Spellcasters cast with a 25 % chance. Otherwise the order of checks is: call for help
  (25 % or 65 %), flee (5 % × its flee value), breath (1/8 if it can breathe), then a melee/ranged attack. Afraid
  monsters only try to flee.
- **Special hits.** Every special has a saving roll on d100. The save is `LUK + level` (plus VIT for poison, IQ for
  fear), capped at 99 %. Level drain has its own save: `2×LUK + 60 + level/16`, capped at 95 %.
- **Spells vs monsters.** Each of the 8 resistance bytes is "percent that gets through". Success =
  `castPower − (100 − byte)`, clamped to 5-95 %. A byte of 0 means immune.
- **Escape.** `75 + party bonuses − (highest escape-block value among the monster groups)`, capped at 95 %.
- **Rewards.** Each kill adds the monster's EXP and gold to the pools. The pools are split evenly among the members
  who can still act (items.md 9). Identified kills are entered in the museum.
- **Summoner pacts.** 16 magic circles in the maze, at most one per floor (floors 1-30). A Summoner standing
  in a circle makes a pact with that circle's summon if the Summoner's level is at least the circle's minimum (3 to
  38). The ids 109-124 are **spell ids** (the 16 Summons, Zombie ... Unspeakable), not monster ids (section 8).

---

## 1. The monster record

Code: (bank 57 `$4820 + 64 × id`.

The game copies a record to `$C50F` with `0:2394` / `0:2397` (64 bytes). It also keeps one copy per monster group
at WRAM4 `$D4B8 + $40 × group` (`22:41DB`). So the `$C5xx` address of a field is `$C50F + offset`. "Readers" are
the sites that prove a meaning. I found them by a byte search for every `ld a,[$C5xx]` (`work/design/monsters/field_sites.txt`)
and by logging every read of the copies during a JP battle (`work/design/monsters/reads_bt.txt`, `battle_reads.py`).

| Off | RAM | Field | Values / encoding | Readers (proof) |
|---|---|---|---|---|
| `$00-$0C` | `$C50F` | Name | 12 chars + `$00`, `$FD` = line break | battle text `{B}`, museum |
| `$0D` | `$C51C` | Unidentified class | 0-15, index of the generic name shown while unidentified (`49:56FD`, museum `41:6730`) | `22:6B40`, `0:36D4`, museum `41:686F` |
| `$0E` | `$C51D` | Type bits | bit 0 undead, 1 demon, 2 dragon, 3 spirit (slaying, items.md 4.4). Bits 4 (golems, Wraith-likes) and 5 (ghosts) are not identified | `32:454A` (slaying), `24:4BAD` and 3 more in the spell bank, `22:6ECB` |
| `$0F` | `$C51E` | Picture id (inferred) | rises by family (Bowman/Shooter 8, Gunner 9...) | no direct reader |
| `$10` | `$C51F` | To-hit base H | lower = more accurate (Ancient One 1, Goblin 19) | `32:4DB7`, `32:5298` |
| `$11` | `$C520` | Swings per round | 1-14 (77 monsters 1, max: Musashi 14, Kamui 10, Kali, Scylla, Carrion Worm 8); used as the loop count, no cap (section 4.1). Corrected 2026-11-12: was "1-7" | `32:4DBF`, `32:52A0` |
| `$12-$14` | `$C521-23` | Damage per swing: N, S, min | damage = `min + Σ(N) rand(0..S−1)` = min .. min + N(S−1) | `32:4DE8-4DFB` |
| `$15-$17` | `$C524-26` | HP: N, S, min | HP = `min + Σ(N) rand(0..S−1)`, rolled per monster at battle start. min = 0 hangs the game (`22:558E` `jr z,$558E`), and no record has it | `22:558A-55A5`; museum shows "min~max" `41:68EB` |
| `$18-$1F` | `$C527-2E` | Resistance bytes, 8 elements | % that gets through: 100 = no resistance, 0 = immune. The museum shows `100 − byte` (`41:6AE8`). Order (museum labels): Earth, Water, Fire, Wind, Spirit, (6th glyph unread), Holy, None | spells `24:6C5E` (index = spell element `$C584`). Party weapon effects: stone uses `$18`, fear/sleep/paralysis use `$1C` (`32:472C-475F`) |
| `$20-$22` | `$C52F-31` | Spell schools | 6 nibbles (`$20` hi, `$20` lo, `$21` hi, ...) = top spell level 1-7 in schools 0-5 (0 = mage, 1 = priest, `work/re/spells.md`) | `0:3149-3198` (spell pick), `22:55B4-55ED` (spell slots) |
| `$23` | `$C532` | AC | signed, lower = better | `22:55AE` (copied to the instance), museum `41:688B` |
| `$24` | `$C533` | Escape block | subtracted from the party's escape chance (section 6) | `22:4839` |
| `$25` | `$C534` | Level | used against party status attacks (`32:46BF`), Hide (`22:6E3C`) and spells (`24:4BA6`, `32:4BFC`, `32:5649`) | as listed |
| `$26` | `$C535` | (unused) | 0 in all 167 records | `32:5652` |
| `$27` | `$C536` | Special attacks | bit 0 poison, 1 fear, 2 sleep, 3 paralysis, 4 stone, 5 decapitation (critical), 6 breath | `32:4FC7` (on hit), `22:6241` (breath AI), museum `41:6989` |
| `$28` | `$C537` | Level drain | number of levels drained per successful hit | `32:513D-51C8` |
| `$29` | `$C538` | Call / flee | high nibble ≠ 0: can call for help (bit 7 = strong caller); low nibble = flee value F | `22:6209`, `22:622B`, `22:6279` |
| `$2A` | `$C539` | Attack verb list | index into `32:5958` (verb lists, `docs/re/verbs.md`) | `32:4D64`, `32:5240` |
| `$2B` | `$C53A` | unknown | 0-14 | no reader found |
| `$2C` | `$C53B` | Reach (bits 0-1) | 0 melee, 1 reach, 2-3 ranged (section 4.2) | `22:62BA`, `22:62EA`, `32:4DC4` |
| `$2D` | `$C53C` | Chest row | chest-value row for guarded-square chests (items.md 10.1) | `25:40E0` (group copy) |
| `$2E-$2F` | `$C53D-3E` | Gold | 16-bit | `0:2F05`, museum `41:68D4` |
| `$30-$32` | `$C53F-41` | EXP | 24-bit | `0:2EF6`, museum `41:68BA` |
| `$33` | `$C542` | Breath element | 0 fire, 1 frost, 2 poison, 3 lightning, 4 acid, 5 stone (verbs 15-20) | `22:711A`, `22:71DE`, `22:7757` |
| `$34-$3D` | | (unused) | 0 in all records | none |
| `$3E` | `$C54D` | Runtime flags | bit 7 = unidentified ($80 in every ROM record; cleared when the group is identified, see the `bt.state` group 1 = $00); bit 3 = this monster cannot use special hits (`32:4FBF`) | 29 readers/writers in banks 0, 22, 24, 32 |
| `$3F` | `$C54E` | Museum index | = id | `0:2F19` (sets the "seen" bit `$C5AE`) |

Example (data): Goblin (id 52) = Lv 2, HP 1 + 1×rand(0..6) = 1-7, AC 6, H 19, 1 swing of 1-7, melee, escape block 10,
calls for help (25 %), flees (10 %), EXP 290, gold 30, chest row 1, met on floors 1-2 and 5.

**Per-monster instance (emulator).** At battle start `22:556B` writes one small record per monster (24 bytes, WRAM4
around `$D5B8`): HP (16-bit), AC copied from `+$23`, 7 + 7 spell charges (9 each per level if the monster has any
spells, `22:55CF-55ED`), and a to-hit modifier at instance `+$12` (0 in every attack I logged; spells presumably
change it).

---

## 2. Encounters

### 2.1 When a fight starts

Code: (code `20:4422-4460`, emu.
After every action in the maze, the main loop `20:43E4` returns to `20:4410`. Actions are a step, a turn, a
turn-around, and the "moved" handling. Then:
1. If `$CC06` ≠ 0 ("just went through a door"), the fight chance is `rand(0..19) == 0`. `0:0DC0` computes
   `(rand8 × 20) >> 8`, so the chance is 13/256 = **5.1 %**. `$CC06` is set by the door step `20:46F4`. It is cleared
   by a plain step `20:470D` and by turning around `20:457C`. Left/right turns keep it.
2. Otherwise the chance is `rand8 == 0` and then `rand8` even: **1/512**. Note that `0:0DA6` returns the high byte of
   a 16-bit LCG `x = 5x + $4123`. I checked this in the emulator by forcing the seed (`rng_check2.py`).
3. A fight only happens if the current square's map byte 1 (its encounter area id) is non-zero. The id goes to
   `$C48E`.

Emulator check (`enc_test.py`, JP state `work/shots/jp_tour/explore/mzbase.state`, walk seed 3): 357 random actions
gave 803 roll passes, 5 first-roll successes and 1 fight. This fits 1/512.

There is no step counter and no floor-depth modifier. The rate is the same on every floor. Squares with area id 0
(rock, some corridors on floors 2, 9, 13, 17, 19, 21, 22, 25) never have random fights.

### 2.2 Fixed fights
- **Guarded squares** (map type 6, `20:5CF0`). Area id = the square's byte 1. Each fights once (one-shot bit `$C6DB`
  by byte 3). All one-shot bits are cleared on every floor change (`20:58DD` clears `$C6DB-$C6E2`), so guards
  come back. Victory gives a chest (`$C00B` bit 2, items.md 10).
- **Events** start fights by returning `$FFB0` = 2 and `$FFB1` = area id from the bank-45 handler (`20:6109`). Ids 34-53
  have one fixed formation each (bosses and named monsters). Areas `$30`/`$31` (48/49) play the boss music (`22:4033`,
  `$C04A` = 4/3; the normal music is 2).

### 2.3 Group formation

Code: (code `22:40C7-41B5`, data `39:7A27`, `39:7573`.
1. Row = `39:7A27 + 4 × areaId`. Take `formation = row[rand & 3]` (4 equally likely formations; repeats in a row
   weight them).
2. Formation record = `39:7573 + 8 × formation` = 4 × [monster id][size code]. There are 150 formations.
3. Size code `$HL` → group size = `H + rand(0..L−1)` (L = 0: exactly H), capped at 9. Group 1 has at least 1 monster.
   Groups 2-4 with size 0 are dropped, and the empty slots are compacted (`22:4202-4283`). The game keeps up to 4
   groups (`$D928` = count).
4. The group sizes go to `$D91C-$D91F`. The monster ids go to `$D918-$D91B`. The records go to `$D4B8 + $40 × g`.

Area ids per floor (data, from the map bytes): floor 1 → 1/2/3 (3 zones), floor 2 → 4, floor 3 → 5 (6 on two guarded
squares), floor 4 → 6, ... floor 30 → 32/33. The full list, with every formation spelled out, is in
../design/monsters_table.md "Encounter tables". Ids 54-100 are not on any map and no event uses them (I did not find a
reader other than the formation code). They are sliding windows over the formation list, so they may be a cut
"random depth" table **(inferred)**.

### 2.4 Surprise / initiative
**Not found.** I traced no surprise roll and no initiative sort. What I checked: the battle entry `22:4000-42D7`
(formation, music, party copy) has no random call apart from formation and group size. A full initiative trace
needs a breakpoint on the action-queue builder (`22:7401` returns the next actor pointer `$DD53`). This is an open
question.

---

## 3. Monster turn

Code: (AI, code `22:61B2-6315`.

Per monster per round, the first rule that fires decides the action:

| Step | Condition | Action |
|---|---|---|
| 0 | the monster's status is Afraid (1) | flee if `F` (flee nibble) ≠ 0, with chance `(F+5)/20`; otherwise nothing (`22:6279`) |
| 0 | status ≥ 2 (asleep etc.) | nothing (`22:61C4` → `6313`) |
| 1 | has spells (`0:3131` picks one) and `rand & $14 == 0` (25 %) | **cast** (action 2) at a party target, or at the whole party (`$FE`) |
| 2 | call nibble ≠ 0 and `rand(0..19) < 5` (bit 7 set: `< 13`) | **call for help** (action 3): 25 % / 65 % |
| 3 | `F` ≠ 0 and `rand(0..19) < F` (and the monster is on the monster side) | **flee** (action 4): F × 5 % |
| 4 | breath bit and `rand & $70 == 0` (1/8) | **breath** (action 5) on the party |
| 5 | otherwise | **attack** (action 1), target by reach (4.2) |

**Spell choice** (`0:3131-321D`): the game collects the schools with a non-zero level nibble and picks one at random
(`0:2B7E`). The top level L selects how many spells of that school are allowed (cumulative counts per level at
`0:3C2B`..., pointer table `0:3C55`). Then it picks one spell uniformly from all spells up to L (`0:0DC0`) and maps it
to a spell id with `24:74B2`. A spell that cannot be cast in battle (`$C583` bit 0 clear) makes the monster do
nothing this turn.

---

## 4. Monster attacks on the party

Code: (code `32:4D55-4E29`.

### 4.1 Hit and damage
For each of the `Att` swings (`+$11`; the count is loaded into B and run down by `dec b / jp nz` at `32:4E25`, and
`32:52F3` in the second copy, with no cap, so Musashi really swings 14 times; hits are counted in the byte `$D962`):
1. `T = H + mod − AC`. H = `+$10`, mod = instance `+$12` (0 in all my logs). AC = target base AC (`$C4E7` = record
   `+$58`) + two modifiers (`$C505`, `$C506`), minus 2 if `$CB84` bit 4 (party-wide AC bonus, inferred: a protective
   spell) (`32:5662`). T is clamped to 1..19 (`32:569E`).
2. Roll `rand(0..19)`. **Hit if roll ≥ T** → hit chance = `(20 − T)/20` = 5 % to 95 %.
   - Ranged monsters (`+$2C`&3 = 2) when `$CB84` bit 1 is set: hit only on a roll of 0 (5 %) (`32:4DC4`) **(inferred:
     a missile-shield effect)**.
3. Damage per hit = `min + Σ(N) rand(0..S−1)` from `+$12..+$14`. ×2 if the target is Asleep (status 2) (`32:4E02`).
   The per-hit sum is kept in the 8-bit register C (`32:4DF6-4DFF`); only From Beyond (32 × 0..9 + 32, max 320) can
   exceed 255 and would wrap, which needs a roll about 5 standard deviations above its mean (inferred, not seen).
4. The hits are summed (`$D962` count, `$D963` damage) and subtracted from HP. HP ≤ 0 → dead (`32:51E3`).

Emulator check (`hitx.py`, `bt.state`, Crawling Claw H 19 vs AC 8): T = 11 logged for every swing, so a 45 % hit
chance.

### 4.2 Reach and targets

Code: (code `22:62B5-62E0`.
Monster groups 1-2 count as the front ranks and groups 3-4 as the back ranks. Party members 1-3 are the front row.

| Reach `+$2C`&3 | From group 1-2 | From group 3-4 |
|---|---|---|
| 0 melee | front row (members 1-3) | cannot attack |
| 1 reach | anyone | front row |
| 2-3 ranged | anyone | anyone |

### 4.3 Special hit effects, one roll per special after a hit

Code: (code `32:4FBF-51CD`.
The save S is capped at 99. Roll `rand(0..99)`: if roll < S the target resists. Lvl = the target's level
(`0:2C72`; 255 if level ≥ 256).

| Bit of `+$27` | Effect | Save S | Message |
|---|---|---|---|
| 0 | Poison (status bit 7) | LUK + VIT + Lvl | 49:47FB |
| 1 | Fear (Afraid) | LUK + IQ + Lvl | 49:46E9 |
| 2 | Sleep | LUK + Lvl | 49:4707 |
| 3 | Paralysis | LUK + Lvl | 49:4723 |
| 4 | Stone | LUK + Lvl | 49:4741 |
| 5 | Decapitation: status Dead, HP 0 | LUK + Lvl | 49:4761 |
| `+$28` ≠ 0 | Level drain of `+$28` levels | `2×LUK + 60 + Lvl/16`, cap 95 | 49:482B |

Notes:
- A status effect seems to apply only when the target's current status is milder (the code compares before writing, `32:503D`, `5078`, `50B4`, `50F0`) **(inferred)**.
- **Drain** (`32:5144-51CD`): items with drain protection (`$C4FC` bits 4-5) first give a 1-in-2 or 1-in-10 extra
  check (items.md: drain evade 50 % / 10 %). If the level falls to 0, the character dies (level set to 1, HP 0,
  status Dead, `32:51CE`). After a drain, the stats are lowered to the new level's maximums (`32:51BB`, inferred).
- Stats are party record offsets `+$51` STR, `+$52` IQ, `+$53` PIE, `+$54` VIT, `+$55` AGI, `+$56` LUK (read from a JP
  state; characters.md has the record).

### 4.4 Breath

Code: (`22:7121`, `32` side not traced.
The element is `+$33`. The verb is 15 + element ("breathed fire" ...). The damage formula was not traced **(not found:
I did not reach the breath damage routine; the breath verb path starts at `22:7119`)**.

---

## 5. Party attacks and spells on monsters

- **Weapons.** Hit, damage, swings, slaying: items.md section 4. Party weapon status effects on monsters
  (`32:46A0-4778`): chance = attacker value − monster level `+$25` (rolls of 0-4 always hit, 99 always fails).
  Stone also needs resistance byte `$18` ≠ 0. Sleep, paralysis and fear need byte `$1C` ≠ 0 (a byte of 0 =
  immune).
- **Spell resistance** (`24:6C5E-6C85`). Let R = resistance byte for the spell's element (`$C584`).
  - R = 0: no effect.
  - Otherwise h = `$DD57 − (100 − R)` (floor 0), with `$DD57` = the spell's power for this cast (set by the spell
    code, characters.md).
  - Roll d100: 0-4 always affects, 95-99 never, otherwise the spell affects if roll < h.
  - Some spells add a pre-roll before this check (`24:6C42-6C5D`: pass only if rand < 15, 50 or 40, by spell).
- **Hide** (`22:6E3C-6E80`): needs `rand(0..99)` ≥ clamp(`$DD29 − max over groups (level + living count)`, 5,
  `$DD2A`) (inferred reading; the field meanings of `$DD29/$DD2A` were not traced).

---

## 6. Escape

Code: (code `22:47C1-4858`.

Chance = `75 + A + B + 4 × (party size − $CB8C) − max over groups of +$24`. A and B are the party averages of the
combatant fields `+$49` and `+$4A` over members with status < 2. These are 0 for the standard party, and their meaning
was not traced. Roll `rand(0..99)`: success if roll < 95 and roll < chance (`22:4849-4855`). On success `$C00B` bit
4 is set and you return to the maze with no reward.

Examples (data, party bonus 0): vs Goblins (`+$24` 10) 65 %. vs Bowmen (12) 63 %. vs dragons (4) 71 %. vs the
"Ancient One" class (17-18) 57-58 %.

---

## 7. Rewards

Code: (code `0:2EEE-2F22`; split: items.md 9.

- Each monster killed adds `+$30` EXP and `+$2E` gold to the battle pools (`$DD2C` EXP, `$DD2F` gold). Monsters that
  flee or are left alive give nothing.
- If the kill was identified (`+$3E` bit 7 clear), the museum "seen" bit for `+$3F` is set (`$C5AE` bitfield). Unidentified
  kills are not recorded.
- The pools are split evenly among members with status < 3. Guarded-square victories add a chest (items.md 10).
- EXP range (data): 30 (Crawling Claw) to 150,000 (Abyss Lurker). Gold: 20 (Crawling Claw) to 250 (Abyss Lurker) per monster.

---

## 8. Summoner pacts

Code: (code `2D:64CF-6664`, data `2D:63BB`.

- **Where.** Magic-circle squares (event type `$0A`, parameter p = circle 0-15). Their floors are listed in dungeon.md.
  Message "A strange pattern is drawn on the ground" (`45:4490`).
- **Who.** If at least one party member is class `$0D` (Summoner) with status < 3, the text becomes "A magic circle
  is drawn... Who will step inside?" (`45:44A8`). Only a Summoner can be picked.
- **Check.** The table `2D:63BB + 3p` gives [**spell id**][minimum level][tier]. The event copies that id's **spell
  record** (`2D:657F` -> `0:24E8`, bank 24 `$6C95 + 16 × id` -> `$C577`) and shows its name: "From the pattern's
  center <summon> appeared! Will you form a pact?" (`2D:44CF`). If the Summoner's level is below the
  minimum: "Your level is too low. The summoning failed." Otherwise bit (id − 109) is tested in the Summoner's pact
  bitfield (record `+$39`, `$C4C8`). If the bit is already set: "A pact already exists." Otherwise the bit is set,
  the tier counter (record `+$4A + tier` = Summons slots of spell level tier + 1) is raised from 0 to 1 if it was 0,
  and "The pact is sealed."
- **Emulator** (JP, F1 (15,15), member 0 poked to class `$0D` level 40, `work/re/contradictions/circle.py`): the circle said
  "もようの ちゅうしんから ゾンビ があらわれた" (Zombie, spell 109), `$C577` held the Zombie spell record, and after
  "Yes" `+$39` bit 0 and the level-1 Summons slot were set to 1.

Corrected 2026-11-12: this table listed the ids as bestiary monsters (Undead Beholder ... Damned); they are the
Summons spells (characters.md §10.5 agrees).

| Circle p | Summon (spell id) | Min. level | Tier (slot level − 1) |
|---|---|---|---|
| 0 | Zombie (109) | 3 | 0 |
| 1 | Ghoul (110) | 4 | 0 |
| 2 | Lion of Hell (111) | 6 | 1 |
| 3 | Minotaur (112) | 10 | 1 |
| 4 | Djinni (113) | 14 | 2 |
| 5 | Ifrit (114) | 15 | 2 |
| 6 | Dao (115) | 16 | 3 |
| 7 | Marid (116) | 17 | 3 |
| 8 | Titan (117) | 20 | 4 |
| 9 | Greater Demon (118) | 23 | 4 |
| 10 | Vampire Lord (119) | 27 | 5 |
| 11 | Shadow Dragon (120) | 31 | 5 |
| 12 | Magic Gate (121) | 34 | 6 |
| 13 | Ancient One (122) | 36 | 6 |
| 14 | From Beyond (123) | 37 | 6 |
| 15 | Unspeakable (124) | 38 | 6 |

How a pact monster is summoned in battle (the Summoner's spell or command) belongs to the spell system and was not
traced here.

---

## 9. Not found / open
- Surprise (who strikes first) and initiative order: not traced (see 2.4).
- Breath damage formula (4.4).
- Meaning of `+$0E` bits 4-5, `+$2B`, the 6th element's name, and the combatant fields `+$49/+$4A` in the escape
  formula.
- How identification of a group is decided at battle start (clears `+$3E` bit 7). The 29 `$C54D` sites are listed
  in `field_sites.txt`.
- Ids 54-100 in the encounter table: no user found.
