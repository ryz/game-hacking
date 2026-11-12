# Wizardry Empire (GBC, Rev 1): the dungeon, technical reference

Tracer, 2026-11-12. The source tags (code)/(data)/(emu)/(inferred) and the address style (`BB:AAAA`, bank in hex)
are the same as in [monsters.md](monsters.md). Every map number comes from the ROM maps (banks `$3E`-`$3F`).
`work/design/monsters/floor_events.py` lists every special square of every floor, with its parameters and the
first message of its event, in `work/design/monsters/floor_events.txt`. The per-floor tables below are taken from
that file. Earlier reachability notes: `docs/re/reach.md`.

---

## Overview (two-minute read)

- **30 maze levels** (`$CB82` = 0-29), each a **16 × 16 grid** that **wraps around** at the edges (`20:4740`:
  coordinates are `& $0F`). Floors 1-20 form the main dungeon, linked by stairs and chutes. Floor 20 is the Abyss
  Emperor's floor (final boss Demon Adish) and has no stairs. Floors 21-30 form a second, harder area (Dark/Ancient
  monsters, up to level 29; the encounter tables also hold weaker ones from level 3). Its top floor (21) has no up stairs, so it is entered some other way **(not traced)**.
- **Stairs keep your x,y.** A down-stair at (x,y) on floor n lands on the up-stair at (x,y) on floor n+1. Every
  floor change re-arms all guarded squares and one-shot events of the floor.
- **Square types** (byte 2 of a cell): rock (instant party death if you are teleported into it), stairs, guarded
  squares (one fixed fight + chest), hidden spots a thief can notice, floor traps (pit, chute, ceiling trap,
  rockfall, viper, spinner), event squares, and two zone flags (damage zone, magic-cancel zone).
- **Events** (bank 45): 16 summoning circles, 8 recruitable NPCs, button panels plus key-holes (elevator), wells,
  a levitation seller, two teleporting fairies, the maid, corpses that may rise, story encounters with the Demon King,
  the Succubus Queen, the Emperor's court, and the final battles on floors 20 and 30.
- **Encounters** are per square (the area id in byte 1); see monsters.md 2. Doors raise the fight chance from
  0.2 % to 5.1 % per action.

---

## 1. Map storage and cell format

Code: `20:58EA`, `20:5909`.

- Floor f (0-29) is 1024 bytes at bank `$3E + f/16`, address `$4000 + $400 × (f mod 16)`. It is copied to WRAM4
  `$D000` when you arrive. Slots 31-32 (bank `$3F` `$7800-$7FFF`) are empty, so there are 30 floors (data).
- Cell (x, y) = 4 bytes at `$D000 + (((y XOR 15) << 4) | x) × 4`. y = 15 is the top row of the data.

| Byte | Meaning |
|---|---|
| 0 Walls, 2 bits per facing (bits 2d, 2d+1; d = 0 north/y+1, 1 east/x+1, 2 south, 3 west). 0 open, 1 wall ("Ouch!"), 2 door (`20:46F4`, also raises the fight chance), 3 **secret or locked door** (`20:45EF`, section 2.1). **Each edge is stored on both squares and movement checks only the square being left**: an edge that is open/door on one side and wall/special on the other is a one-way door (emulator 2026-11-12, floor 1: (12,15) east -> (13,15) passes, (13,15) west bumps 'Ouch!' (`$C1BF` = 31:4596); (14,12) south passes, (14,11) north bumps). 53 door/wall edges on 16 floors; 222 open/wall edges on floor 20 alone (`tools/designtables/floormap.py`) |
| 1 | Encounter area id (0 = no random fights). On guarded squares it is the guard's area id |
| 2 | bits 0-5 square type (section 2); bits 6-7 zone: `01` damage zone (`20:4463`), `10` cancel zone (`20:5A8F`, below), `11` no effect found; bit 6 also changes the wall graphics set (`20:4393`) |
| 3 | Parameter (event number, trap kind, one-shot bit index) |

Position RAM: `$CB80` x, `$CB81` y, `$CB82` floor − 1, `$CB83` facing (reach.md).

**Zones.**
- **Damage zone** (`01`): after every action, each member with status < 5 loses `maxHP/4 + 1` HP (`20:4491`) and
  dies at 0 ("... has died", `49:4AA6`). This does not happen when `$CB84` bit 5 is set (a party protection,
  inferred levitation or a ward).
- **Cancel zone** (`10`): entering sets `$CB84` bit 2 and clears `$CB84` bits 4-7 (the party-wide spell effects).
  This is inferred to be the "Anti-magic space" named on a sign (`45:61F9`).

Zones with these flags: floor 5 (60 squares `11`), 6 (58 `10`), 8 (16 `01`), 11 (121 `01`), 12 (19 `11`), 15, 18,
22-26, 27 (15 `01`), 28 (126 `11`, 41 `10`), 30 (16 `01`). The `01` zones are also the squares with area ids 101-105,
so they have their own monster mix.

**Teleport curse.** If any member has record `+$6E` bit 7, each step has a 50 % chance to put the party on a random
square of the floor (`20:4754-477D`). Items.md lists an item property "teleport" (special 1) **(inferred link)**.

---

## 2. Square types

Code: handler table `20:6405` per floor; types 0-14 are the same on every floor.

| Type | Name | Effect (code) |
|---|---|---|
| 0 | floor | nothing |
| 5 | **lock square** | nothing when stepped on; p = the lock flag of its locked doors (section 2.1). 46 lock squares, each with at least one locked side; flags 30 and 33-58 |
| 1 | **rock** | `20:5AC7`: everyone's HP 0, status Dead, "In rock" (`49:4483`), party lost to town. Only reachable by teleport |
| 2 / 3 | **stairs up / down** | prompt Yes/No (`49:41FA` / `422B`). Floor ±1, same x,y (`20:5B74`, `5BB9`). Resets one-shot flags (`20:58DD`) |
| 4 | **hidden spot** | `20:5BFE`, one-shot by `$CB9B` bit p. Each member with status < 3 rolls to notice ("X noticed something", `49:44BC`). Skill (`20:5C20-5C93`, level L capped at 255): Thief LUK/2 + 5L; Ninja LUK/2 + max(0, 5L − 25); Kunoichi LUK/4 + max(0, 5L − 50); others max(0, L/4 − 10). From L 51 the level part is fixed (Thief 255, Ninja 230, Kunoichi 205); the total is capped at 255. Difficulty D = 5 × `20:7100[p]`. Margin m = skill − D (`20:5CA4-5CB4`): **m < 0: never; m = 0: only a roll of 0 (about 1 %); m = 1-4: 4m % (4, 8, 12, 16 %); m ≥ 5: 80 %** (roll `Random(99)`, success if the roll is 0 or below the chance, `20:5CB6-5CBF`). The jump from 16 % to 80 % at m = 5 is in the code (`cp $05` / `ld a,$50`). Corrected 2026-11-12: was "4 × (skill − difficulty) % if < 5 points over, else 80 % (+1 % on a roll of 0)". Noticing only shows the message: it does **not** set the flag (`20:5CC1-5CE1` loops on to the next member). The spot belongs to a secret door (section 2.1) |
| 6 | **guarded square** | `20:5CF0`: fixed fight with area byte 1, once per floor visit (`$C6DB` bit p). The victory gives a chest (`$C00B` bit 2, items.md 10) |
| 7 | button panel | event `$07` → `2D:640F` "A row of buttons. Which one will you press? A B C D E". p = 64-68. Next to a key-hole on most floors; the sign "Maze Elevator Control Room" exists, so these are inferred to be the elevator |
| 8 | **floor trap**, kind = p & `$E0` | `$00` Chute ("Chute"), `$20` Pit ("Pit"): both are skipped with "But you are floating" when levitating (`$CB84` check). `$40` Ceiling trap, `$60` Rockfall: damage, amounts not traced. `$80` Viper: each member saves with `rand(0..99)` < level/2 + LUK − (p & `$1F`) (rolls 0-4 always poison, 99 always saves), else poisoned (`20:5D4C`). `$A0` Spinner: random facing (`20:47FB`) |
| 9 | marker | `20:4795`: sets a bit per square in `$D967` (32 bytes per floor) and records the deepest floor in `$DD28` **(inferred: auto-map memory)** |
| A, B, C | event | `$FFB0` = type, `$FFB1` = p → bank 45 dispatcher `2D:63EB` |
| D | corpse | event `$0D` p |
| E | one-shot event | sub-handler p (0-16), once per floor visit (`$C6DD` bit p) |
| F, 10, 11, 12, 13 | floor-specific | a fixed event code per floor (`20:6058-60CE`); `20:600D` = alarm |

**After an event** (`20:60EB`): `$FFB0` = 0 means nothing. 2 means a fight with area `$FFB1` (monsters.md 2.2).
Anything else means the floor or position changed (teleport), and the map is reloaded.

---

### 2.1 Secret and locked doors (wall value 3)

Verified in the emulator 2026-11-12 (floor 1) and read from `20:45EF-4611`, `20:4F40-50F7`, `20:5188-51DB`.

- **Moving** through a side with value 3 (`20:45EF`, forward move, `e` bit 0 set) takes the cell's p (byte 3 of
  the square being **left**) as a flag number and tests `$CB9B` bit p (`0:2B8C`). Set: the side works as a door
  (`20:46F4`). Clear: on a hidden-spot square (type 4) it is a wall ("Ouch!", `20:46BC`); on any other square the
  locked-door picture is shown with "It is locked." (`49:43A0`, `20:4611-46B9`).
- **Secret door** = value-3 side on a hidden spot. The maze menu's **Search** (`20:512E`, menu item 0) facing such a
  side with the flag clear sets the flag (`0:2BA6`) and says "Found a secret door!" (`49:42E3`); no roll. Otherwise
  "Nothing was found." (`49:42F3`). Verified: (0,9) facing east on floor 1, Search -> flag 2 set; walking east then
  works.
- **Locked door** = value-3 side on any other square (in the data: lock squares, type 5). The maze menu's
  **Pick a lock** (`20:4EF0`, menu item 1) facing it with the flag clear asks "Who will pick the lock?"
  (`49:435D`), then "Picking the lock" (`49:436B`). Skill of the chosen member (`20:5011-5066`, level L from
  `0:2C72`):

  | Class | Skill |
  |---|---|
  | Thief (3) | 5L, 255 from L 51 |
  | Ninja (7) | 5L − 25 (at least 0), 230 from L 51 |
  | Kunoichi (12) | 5L − 50 (at least 0), 205 from L 51 |
  | others | L/2 − 10, at least 0 |

  Difficulty D = 5 × `20:7100[p]` (the hidden-spot table). m = skill − D (`20:5075-508B`): m < 0 fails;
  m = 0: success only on a roll of 0; m > 0: chance = min(95, 2m + AGI) % (AGI = `$C4E4`, the member's working
  copy `+55`). Roll `Random(99)` (`0:0DC0`), success if the roll is 0 or below the chance (`20:5099-50A3`). Success
  sets the flag: "The lock opened." (`49:437F`); else "Failed." (`49:4376`). No cost or penalty for a failure was
  seen in the code (retry at will, inferred).
- **The flags are global and saved:** `$CB9B-$CBA9` (15 bytes, 120 flags) are copied to SRAM `$AED3` with the save
  (`0:2D13`, `0:2D65`), so a found secret door or picked lock stays open for good (inferred from the save copy; no
  clearing code was found). Other readers: `20:5A04` (inferred: the 3D view, type 4) and `23:4345`.
- Data: 20 secret doors seen from both sides, 13 with a door on the far side and 1 with a wall; 18 locked doors
  seen from both sides and 11 with a door on the far side (`tools/designtables/floormap.py N --list`). One
  locked side is on a plain square with p = 0: floor 15 (1,2), which therefore shares flag 0 with floor 1's secret
  door at (11,15) (data oddity; untested).

## 3. Event catalogue

Code: bank 45, handler table `2D:4400`, index `$FFB0 − 7`.

| Code / p | Handler | What it is (first messages) |
|---|---|---|
| `$07` p64-68 | `640F` | Button panel A-E (elevator, inferred) |
| `$0A` p0-15 | `64CF` | Magic circle p: Summoner pact (monsters.md 8) |
| `$0B` p | `666E` | "Beside the door is a hole for slipping something in": key-hole door, p = key (item id, inferred) |
| `$0C` p0-7 | `6705` | Recruitable NPC p (`2D:66C5 + 8p`): Murphy, Lloyd, Louie, Siegfried, Laila, Kojiro, Badick, Warnard (message order). Joins if the roster has < 20 (2B:4037) |
| `$0D` p | `68E6` | "A monster's corpse lies here": nothing, or "The corpse began to move!" (fight) |
| E p0 | `6976` | Gold coins: pick up → gold, or they come alive (fight) |
| E p1 | `6A90` | A weird robed monster (fight; drops something) |
| E p2 | `6AEC` | A hermit in seiza (fight) |
| E p3 | `6B67` | The Demon King on his throne (fight; he withdraws) |
| E p4 | `6BE2` | A peerless beauty: the town of succubi, the Succubus Queen |
| E p5 | `6CB6` | Demons' court: "The Emperor awaits you" |
| E p6 | `6D31` | Space tears open (rift monster) |
| E p7 | `6D8D` | A giant bow appears |
| E p8 | `6DC4` | Something rises from the pond |
| E p9 | `6DFB` | A priest of the netherworld |
| E p10 | `6E32` | A huge creature asks for help ("HELP US") |
| E p11 | `6F08` | Town of Umber Hulks |
| E p12 | `6F64` | A man in jet black ("So Adish is dead") |
| E p13 | `6FD9` | The Ancient One from the rift |
| E p14 | `7035` | The Emperor of the Abyss: final battle with Demon Adish |
| E p15 | `713A` | The last, strongest monster: the true final battle |
| E p16 | `720C` | "A mighty demonic seal has been placed here" |
| `$0F-$18`, `$25`, `$26` | `79EC` | Sign texts (Torture Chamber, Prison, Maze Cemetery, Chapel, gentle slope, "Danger ahead!"...). The mapping from code to text was not traced |
| `$19` | `724E` | Giggling laughter ("A man?") |
| `$1A` / `$1B` | `728A` / `739E` | Fairy twins. They flee unless you carry item `$AD` (Fairy's Heart). With it, they teleport you to the other twin for 1 G (floors 1 ↔ 11) |
| `$1C` | `74B1` | Junk pile (random find or nothing) |
| `$1D` | `7571` | "You found what the monster dropped earlier" |
| `$1E` | `7645` | Well: drink → random: HP restored / poison / cured / heavy damage / paralysis |
| `$1F` | `776A` | Sorcerer: levitation for 500 G (lets you float over pits and chutes) |
| `$20` | `781D` | Maid ("If you...") service; she appears on floors 7, 20 and 30 |
| `$21` | `7881` | Small monster on the ceiling |
| `$22` | `78AE` | Handsome man in a cloak (vampire hint) |
| `$23` | `793C` | Queen of Darkness |
| `$24` | `79A4` | Alarm: "Suddenly an alarm blared" → fight with the square's area (`20:600D`) |
| `$27` | `7C08` | "Thanks for playing! You can now safely turn the power off" |
| `$28` | `7C2C` | "Use the map record sheet?" |

I did not trace the exact outcome rolls of the well, the junk pile and the corpses. The messages are in
`work/re/reach/scr/evtab.txt`.

---

## 4. Floors

The columns give counts. The coordinates are in `floor_events.txt`. "Areas" lists the random-encounter area ids
([../design/monsters_table.md](../design/monsters_table.md) has the monsters). The guarded column shows the count and the area ids.
Guarded squares: 0 (floor 20) to 21 (floor 4) per floor, 244 in all (data, `work/re/contradictions/floors.py`).

A few single squares carry another floor's area id (data, `work/re/contradictions/floors.txt`; given in brackets with
their (x,y)): floor 22 area 25 at (14,2) and 26 at (15,2); floor 23 area 27 at (7,7) and on the down stairs (7,8),
(8,7); floor 24 area 29 at (7,9) and the stairs (6,9); floor 27 area 31 on the marker (13,10); floor 28 area 32 on
the trap (8,8). The encounter check `20:443F-444F` reads byte 1 of the current square with no type test, so a
random fight on such a square uses that area (inferred; not seen). This is why
../design/monsters_table.md lists area 26 on floors 22 and 24, 27 on 23 and 25, 29 on 24 and 26-27: both tables are
right; the floor table below gives the main area. (Clarified 2026-11-12.)

| Floor | Stairs (x,y) | Areas | Guarded | Traps / hidden | Events |
|---|---|---|---|---|---|
| 1 | up (0,15) exit; down (15,0) | 1, 2, 3 | 8 (1-3) | 2 pits; 6 hidden | circle 0 (15,15); fairy (2,12); gold coins (5,4) |
| 2 | up (15,0); down (0,15) | 4 | 3 (4) | 4 rockfall, 3 pits; 2 hidden | NPC 0 Murphy (9,10) |
| 3 | up (0,15); down ×3 (14,15) (8,8) (14,1) | 5 | 14 (5, 6) | 2 hidden | circle 1 (4,0); button panel + key-hole (1,1)/(1,2) |
| 4 | up ×3; down (3,4) | 6 | 21 (6) | 3 spinners, 3 pits | weird robed monster (4,8); monster's drop (3,8); sign (7,9); buttons + key-hole |
| 5 | up (3,4); down (7,8) | 7 | 11 (7) | 2 chutes, 4 pits, spinner | NPC 1 Lloyd (1,11); circle 2 (15,9); ceiling monster (5,5); buttons + key-hole |
| 6 | up (7,8); no down | 8 | 5 (8) | chute (0,15) → floor 7 (inferred); 4 hidden | NPC 2 Louie (12,3); 3 alarm squares; buttons + key-hole |
| 7 | none up; down (15,0) | 9 | 6 (9) | 10 hidden; 4 markers | maid (1,14); 2 button panels + key-holes |
| 8 | up (15,0); down (4,14) (13,13) | 10, 101 (damage zone) | 14 (10, 101) | 4 hidden | hermit (2,14); pond (3,10); circle 3 (3,8); NPC 3 Siegfried (8,8); well (14,3); 3 signs |
| 9 | up ×2; down (0,15) | 11 | 8 (11, 12) | 4 pits; 4 hidden | circle 4 (11,5); NPCs 4 Laila (1,0) and 5 Kojiro (3,3); 2 signs |
| 10 | up (0,15); down (0,0) | 12 | 2 (12) | 2 hidden | 26 corpses (the "cemetery"); priest of the netherworld (1,1); 4 signs |
| 11 | up (0,0); down (15,15) | 13, 102 (damage zone, half the floor) | 10 (13, 102) | 3 vipers, 3 rockfall, 2 pits | fairy twin (11,12); NPC 6 Badick (6,6); levitation sorcerer (8,3); sign |
| 12 | up (15,15); down (0,0) | 14 | 7 (14) | 1 hidden | circle 5 (8,15); huge creature (3,6); NPC 7 Warnard (8,2) |
| 13 | up (0,0); down (0,15) | 15 | 5 (50: fixed formation) | 2 hidden | Umber Hulk town (8,7); circle 6 (9,3) |
| 14 | up (0,15); down (9,1) | 16 | 14 (16) | 2 ceiling traps | cloaked man (12,15); circle 7 (12,1) |
| 15 | up (9,1); down (15,15) | 17 | 11 (17) | 3 spinners, rockfall; 4 hidden | ceiling monster (9,3); circle 8 (0,2) |
| 16 | up (15,15); down (14,1) | 18 | 7 (18) | – | Queen of Darkness (14,4) |
| 17 | up (14,1); down (8,8) | 19 | 6 (19) | – | **Demon King** (7,7) |
| 18 | up (8,8); down (6,1) | 20 | 11 (20, 51) | 4 hidden | circle 9 (15,13); giggling (7,10); **succubus beauty** (5,6) |
| 19 | up (6,1); no down | 21 | 7 (21, 22) | 2 pits, spinner, chute (0,5) → floor 20 (inferred) | demons' court (7,8); junk pile (8,8) |
| 20 | none | 22 | 0 | – | **Emperor of the Abyss / Demon Adish** (8,7); maid (0,2); demonic seal (0,0); 3 signs |
| 21 | none up; down (12,2) | 23 | 6 (23, 24) | 27 floor traps; 3 hidden | circle 10 (0,3) |
| 22 | up (12,2); no down | 24 (+25, 26: one square each) | 8 (24) | 12 traps | – |
| 23 | none up; down ×5 | 25 (+27: three squares) | 8 (25, 26) | 12 traps; 4 hidden | circle 11 (13,3) |
| 24 | up ×5; down ×3 | 26 (+29: two squares) | 6 (26) | chute, 2 pits; 1 hidden | circle 12 (7,15) |
| 25 | up ×4; no down | 27, 103 | 11 (27, 103) | 20 traps (many spinners) | well (0,0) |
| 26 | none | 28, 29 | 5 (28, 30) | 11 traps (5 vipers, 4 pits, 2 rockfalls) | circle 13 (12,3) |
| 27 | none | 29, 104 (damage zone) (+31: one square) | 4 (31) | 8 traps | – |
| 28 | none | 30 (+32: one square) | 5 (32) | **122 trap squares** (spinner field) | – |
| 29 | none | 31, 33 | 17 (31, 33) | 13 traps, chute | circle 14 (11,1) |
| 30 | none | 32, 33, 105 | 4 (32, 33) | 18 traps | circle 15 (7,15); rift (1,8); giant bow (6,5); Ancient One rift (12,7); man in jet black (1,11); maid (15,11); well (12,10); **final battle** (15,14) |

Floor-change routes not explained by stairs: the chutes on floors 5, 6, 19, 24 and 29 (drop amount not traced), the
fairy teleports (1 ↔ 11), the button panels, and events that return a floor change.

---

## 5. Not found / open
- How floors 21-30 are entered (no up stairs on 21). Candidates: the button panels or an event after the ending
  (the second-clear flag `$C5C6` bit 7, docs/re/missing-text.md). Not traced.
- How many floors a chute drops, and the damage of pits, ceiling traps and rockfall (`20:5DD2-5F4B`).
- The button-panel destinations (`2D:640F`, p 64-68) and the key items for the holes (`2D:666E`, p).
- Zone value `11`. (Wall value 3: solved, section 2.1.)
- Encounter area ids 54-100 (not on any map).
