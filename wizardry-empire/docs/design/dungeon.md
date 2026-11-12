# Dungeon: floors, squares, traps, fights, chests, events

How Wizardry Empire's maze is built and what it does to the party: the floors and how they connect, what each kind
of square does, where fights come from, the chests that guarded squares give, the events, and a floor-by-floor
table. Notation and confidence tags: [README.md](README.md). Quirks: [findings.md](findings.md).

Related documents: monsters and encounter tables in [monsters.md](monsters.md) and
[monsters_table.md](monsters_table.md); items found in chests in [items.md](items.md) and
[items_table.md](items_table.md); Summoner pacts and the magic circles in [spells.md](spells.md#6-summoner-pacts).

---

## Overview

- **30 floors**, each a **16 × 16 grid whose edges wrap around**: walking off the east edge brings you in on the
  west edge.
- **Floors 1-20** are the main dungeon, linked by stairs plus two chutes. Floor 20 is the floor of the Emperor of the
  Abyss and the final battle with Demon Adish; it has no stairs. **Floors 21-30** are a second, harder area (the
  strongest monsters, up to level 29, mixed with weaker ones). No stairs lead there from floor 20; how the party gets there was not traced
  ([findings](findings.md#28-floors-21-30-are-not-reached-by-stairs)).
- **Warps** move the party at once to a fixed square, also to other floors (87, on floors 7, 15, 16 and 21-30).
- **Stairs keep your position:** a down stair at (x, y) on floor n puts you on the up stair at (x, y) on floor n+1.
- **Squares can hurt you:** pits, chutes, ceiling traps, rockfall, vipers (poison) and spinners; **damage zones**
  take a quarter of every member's max HP per action; **anti-magic zones** cancel the party's spell effects; **dark zones** blind the view;
  **rock** kills the whole party if a teleport puts it there.
- **Fights:** random fights are rare except right after a door (rates in [monsters.md](monsters.md#3-when-a-fight-starts)). **Guarded
  squares** (0-21 per floor, 244 in all) hold a fixed fight; they are the **only fights that give a chest**, and they
  **re-arm every time you change floors**, together with the floor's one-shot events.
- **Chests:** the strongest monster in the guard fight sets the chest's odds. The rolled chest value sets the tier
  (Leather bag up to Bewitching), the gold (10 × (4 + a random number from 0 to the value)), which item lists can
  drop, and the trap odds. Fire Bolt is the most common trap at every tier.
- **Events:** 16 magic circles (Summoner pacts), 8 recruitable adventurers, elevator button panels with key-holes,
  wells, a levitation seller, fairy twins that teleport between floors 1 and 11, a maid, corpses that may rise, signs,
  and the story encounters (Demon King, Succubus Queen, the court of the Emperor of the Abyss, the final battles on
  floors 20 and 30).

---

## 1. Map and coordinates

Each floor is a 16 × 16 grid of squares. Each square has four sides, an encounter area and a type, plus a detail
such as which event or trap.

- **Coordinates** are written (x, y), x from 0 to 15 going east, y from 0 to 15 going north. (0, 15) is the
  north-west corner. The maze entrance is the up stair at (0, 15) on floor 1.
- **Wrapping:** both coordinates wrap, so the grid is a torus.
- **Sides** (one per side of the square): open; wall (bumping says "Ouch!"); door (walking through it raises the
  random-fight chance, section 4); and a **secret or locked door** (section 3.6).
- **One-way doors:** each side is stored on both of its squares, and the game only looks at the side of the square
  the party is leaving. Where one side is open or a door and the other side is a wall, the party can pass in one
  direction only and bumps into a wall ("Ouch!") coming back (verified on floor 1, both a door/wall and a reverse
  case). There are 53 such edges with a door on one side, on 16 floors, and more where one side is simply open
  (computed from the maps); floor 20 is a spiral of rings joined only by one-way doors. The maps draw them as a
  door with an arrow ([maps/README.md](maps/README.md)).
- **Square types:** section 3.
- **Encounter area:** a number from 0 to 105 that says which monsters can appear on the square. 0 means no random
  fights there. Areas 1-33 are the normal areas of the floors, 101-105 cover the damage zones, and 34-53 are fixed
  fights started by events. Areas 54-100 are on no map ([findings](findings.md#21-encounter-areas-54-100-are-unused)).

**Notes:** the game remembers every square the party has stood on, per floor, and the deepest floor reached; the
in-game auto-map shows them (section 9). Drawn floor maps and how to read them: [maps/README.md](maps/README.md).

Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format)

---

## 2. How floors connect

The party moves between floors by stairs, chutes, warps, teleporting events, the Teleport spell (section 9) and
the elevator.

- **Stairs.** Stepping on a stair asks Yes/No. Yes moves you one floor up or down and keeps x and y, so every down
  stair sits directly above an up stair. Every floor change re-arms the guarded squares and one-shot events of the
  floor (section 4).
- **Chutes** are floor traps (section 3.2) on floors 5, 6, 19, 24 and 29. How many floors a chute drops was not
  traced. The chute at (0, 15) on floor 6 was inferred to lead to floor 7, but it has a wall on all four sides and cannot
  be walked onto (computed from the map), so the way from 6 to 7 is open; and the one at (0, 5) on floor 19 to
  floor 20, because those floors have no stairs between them (inferred).
- **Warps** (section 3.1): five warp squares change floor: floor 22 (12, 9) to 23, 25 (7, 8) to 26, 26 (3, 12) to
  27 (7, 10), 27 (15, 15) to 28, and 28 (6, 7) to 29 (0, 0) (verified for warps in general, B7).
- **Fairy twins** (Rei and Shia): with the Fairy's Heart in the party, one twin teleports the party to the other
  for 1 G, between floor 1 (2, 12) and floor 11 (11, 12).
- **Button panels and key-holes.** Floors 3 to 19 have panels with buttons A-E, most of them next to a door with a key-hole.
  A sign reading "Maze Elevator Control Room" exists, and the Key Card's special power is "elevator key" (game
  text), so the panels are inferred to be the **Maze Elevator** (inferred). Their destinations were not traced.
- **Events that teleport** (any event can move the party).

Stair links (from the floor table, section 8):

| Floors | Link |
|---|---|
| 1 ↔ 2 ↔ 3 ↔ 4 ↔ 5 ↔ 6 | stairs (floor 3 has three down stairs to floor 4) |
| 6 → 7 | no stairs; chute on floor 6 (inferred) |
| 7 ↔ 8 ↔ … ↔ 19 | stairs (floor 8 has two down stairs to floor 9) |
| 19 → 20 | no stairs; chute on floor 19 (inferred) |
| 20 → 21 | no stairs; not traced |
| 21 ↔ 22 | stairs |
| 22 → 23 | no stairs; not traced |
| 23 ↔ 24 ↔ 25 | stairs (five between 23 and 24; three down on 24, four up on 25) |
| 25 → 26 → … → 30 | no stairs on floors 26-30; not traced |

**Notes:** floors 7 and 20 have no up stairs, so the way back up from them is not known (elevator inferred).
Floors 21-30: [findings](findings.md#28-floors-21-30-are-not-reached-by-stairs).

Tech: [dungeon.md §4](../tech/dungeon.md#4-floors), [§5](../tech/dungeon.md#5-not-found--open)

---

## 3. Squares

What happens when the party steps on (or into) a square, and the two zone markings that can sit on top of a
square's type.

### 3.1 Square types

The same types exist on every floor; a few extra types are tied to one floor's events.

| Square | What it does to the party |
|---|---|
| Floor | Nothing. |
| **Rock** | Only reachable by teleport. Everyone's HP drops to 0 and everyone is Dead ("In rock"); the party is lost to town. |
| **Stairs up / down** | Yes/No prompt; one floor up or down, same x, y. |
| **Hidden spot** | Members may notice something (section 3.3); the square holds a secret door (section 3.6). |
| **Lock square** | Nothing on stepping; the square holds a locked door (section 3.6). |
| **Guarded square** | A fixed fight, once per floor visit; winning gives a chest (section 4). |
| **Button panel** | "A row of buttons. Which one will you press? A B C D E" (the elevator, inferred). |
| **Floor trap** | Chute, pit, ceiling trap, rockfall, viper or spinner (section 3.2). |
| **Warp** | Moves the party at once to a fixed square, on the same or another floor; no prompt, no cost (verified). 87 warps, on floors 7, 15, 16 and 21-30. A party that lands on a warp by Teleport is not moved on. |
| **Event** | Runs one of the events in section 7. |
| **Corpse** | "A monster's corpse lies here": nothing, or "The corpse began to move!" and a fight. |
| **One-shot event** | A story or special event that runs once per floor visit. |
| **Floor-specific** | A fixed event chosen per floor: signs, the fairy, the maid, the well, alarms. |

After an event the game does nothing, starts a fight with a given encounter area, or moves the party to the new
square.

Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types)

### 3.2 Floor traps

Trap squares on the floor (chest traps are in section 6). Floor 28 is almost all traps (122 trap squares, mostly
spinners).

| Trap | Effect |
|---|---|
| **Chute** | Drops the party to a lower floor (how far: not traced). Skipped when the party is floating ("But you are floating"). |
| **Pit** | Damage (amount not traced). Skipped when floating. |
| **Ceiling trap** | Damage (amount not traced). |
| **Rockfall** | Damage (amount not traced). |
| **Viper** | Each member may be poisoned (below). |
| **Spinner** | Turns the party to a random facing. |

**Viper:** each member has a save of `level/2 + LUK − trap strength`, where the trap strength is set per square.
The member avoids the poison if a random number from 0 to 99 is below the save. Two rolls are fixed: 0-4 always
poisons and 99 always avoids it, so the chance to be poisoned is never below 5% or above 99%. (This differs from the
saves against monster special hits, which have no fixed rolls; see [combat.md](combat.md#9-special-hits-and-saves).)

**Floating:** the levitation that the sorcerer on floor 11 sells for 500 G lets the party float over pits and
chutes.

**Notes:** floating is inferred to be the same protection that stops damage-zone damage (section 3.4).

Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types)

### 3.3 Hidden spots

Squares where a sharp-eyed member may notice something ("X noticed something"). All but three hidden spots sit at a
**secret door** (section 3.6); the exceptions are a pair on floor 18 and a single spot on floor 24 (data). Noticing is only a hint: it does not open anything, and **Search** finds the door without
it. Once the door is found, the spot stays silent.

Each member who is OK, Afraid or Asleep rolls once. Skill by class (level = character level; a negative level
part counts as 0):

| Class | Skill | From level 51 |
|---|---|---|
| Thief | LUK/2 + 5 × level | LUK/2 + 255 |
| Ninja | LUK/2 + (5 × level − 25) | LUK/2 + 230 |
| Kunoichi | LUK/4 + (5 × level − 50) | LUK/4 + 205 |
| Everyone else | level/4 − 10, at least 0 | |

The skill is at most 255. Each spot has a difficulty of 5 × a value set for that spot. With the margin
m = skill − difficulty, the chance to notice is:

| Margin m | Chance |
|---|---|
| below 0 | never |
| 0 | only on a roll of 0: about 1% |
| 1, 2, 3, 4 | 4%, 8%, 12%, 16% (4 × m) |
| 5 or more | 80% |

The roll is a random number from 0 to 99; a roll of 0 always succeeds. The jump from 16% to 80% is how the game is
written ([findings](findings.md#30-noticing-a-hidden-spot-jumps-from-16-to-80)).

Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types)

### 3.4 Zones: lake, magic seal, dark zone

Three zone kinds sit on top of a square's type. The auto-map names them "lake", "magic seal" and "dark zone"
(game text); the maps in this folder call the first two the damage zone and the anti-magic zone.

**Damage zone (lake).** After every action (step or turn) in the zone, each member who is not Dead, Ashes or Lost loses
`maxHP/4 + 1` HP and dies at 0 ("... has died"). A party-wide protection (not traced; inferred levitation or a
ward) prevents it. Without protection a full-HP character dies after at most 4 actions (computed: four hits of
`maxHP/4 + 1` always add up to more than max HP). Damage-zone squares have their own encounter areas (101-105).

**Anti-magic zone (magic seal).** Entering it cancels all party-wide spell effects. A sign names it "Anti-magic
space".

**Dark zone.** Entering it puts out the party's light and replaces the 3D view with "Pitch darkness!" (verified);
the party walks blind. The auto-map does not draw dark zones (it names them under the cursor).

| Floor | Zone squares |
|---|---|
| 5 | 60 dark |
| 6 | 58 anti-magic |
| 8 | 16 damage (area 101) |
| 11 | 121 damage (area 102, about half the floor) |
| 12 | 19 dark |
| 15 | 13 anti-magic, 46 dark |
| 18 | 10 anti-magic, 27 dark |
| 22 | 88 anti-magic |
| 23 | 49 dark |
| 24 | 32 anti-magic, 15 dark |
| 25 | 3 damage (area 103), 11 anti-magic, 42 dark |
| 26 | 73 dark |
| 27 | 15 damage (area 104) |
| 28 | 126 dark, 41 anti-magic |
| 30 | 16 damage (area 105) |

**Notes:** "not Dead, Ashes or Lost" includes Stoned members
([findings](findings.md#32-stoned-members-still-take-damage-zone-damage)). Dark-zone squares also use a different set of wall
pictures.

Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format)

### 3.5 Random teleport curse

If any party member carries a hidden condition (not traced), **each step has a 50% chance to put the party on a
random square of the current floor**. The condition is inferred to come from items with the "teleport" effect (the
Helm of Warping, [items.md](items.md#43-equipped-effects)) (inferred).

**Notes:** whether the random square can be rock (which kills the party) was not traced.

Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format)

### 3.6 Secret and locked doors

The fourth kind of side is a door that starts closed. Which kind it is depends on the square the party stands on
(verified in the game, floor 1):

- **Secret door** (on a hidden spot): looks and acts like a wall ("Ouch!") until found. Choosing **Search** in the
  maze menu while standing on the spot and facing the door always finds it: "Found a secret door!" (verified). There
  is no roll and noticing the spot first is not needed.
- **Locked door** (on a lock square): shows a locked double door, "It is locked." **Pick a lock** in the maze menu
  asks "Who will pick the lock?"; the chosen member rolls once per try. A failed try says "Failed." and costs nothing
  that was found, so it can be repeated (inferred).

Lock-picking skill by class (level = character level; a negative skill counts as 0):

| Class | Skill | From level 51 |
|---|---|---|
| Thief | 5 × level | 255 |
| Ninja | 5 × level − 25 | 230 |
| Kunoichi | 5 × level − 50 | 205 |
| Everyone else | level/2 − 10 | |

Each lock has a difficulty D = 5 × a value set for that lock (the same table as the hidden spots). With the margin
m = skill − D:

| Margin m | Chance to open |
|---|---|
| below 0 | never |
| 0 | only on a roll of 0: about 1% |
| 1 or more | 2 × m + AGI, at most 95% |

So a Thief's level and the picker's AGI decide it; LUK plays no part, unlike noticing a hidden spot.

**Both kinds stay open for good:** a found or picked door is remembered in the saved game, for every later visit
(inferred: the flags are saved and nothing was found that clears them). Doors with an ordinary door or open side on
the other face can always be passed from that side; the maps draw secret doors as a red dashed line and locked doors
as a red bar ([maps/README.md](maps/README.md)).

Example (computed): the floor 1 lock between (4, 7) and (4, 8) has difficulty 5. A level 1 Thief (skill 5) has
m = 0, about 1%; at level 2 (skill 10, m = 5) with AGI 12 the chance is 2 × 5 + 12 = 22%. A level 1 Fighter
(skill 0) cannot open it.

Tech: [dungeon.md §2.1](../tech/dungeon.md#21-secret-and-locked-doors-wall-value-3)

---

## 4. Fights in the maze

Random fights can start after any action, from the square's encounter area: 1 in 512 normally, 5.1% right after
walking through a door; squares with area 0 never have them. Rates, formations and the encounter tables:
[monsters.md](monsters.md#3-when-a-fight-starts) and [monsters_table.md](monsters_table.md).

**Guarded squares** are fixed spots where monsters wait; **one-shot events** are story and special encounters.

- A **guarded square** starts a fight with its own encounter area as soon as the party steps on it. It fights
  **once per floor visit**. Winning gives a **chest** (section 5), the only source of chests: random fights never
  give one (verified: 25 random battles, no chest).
- Guarded squares per floor: from 0 (floor 20) and 2 (floor 10) up to 21 (floor 4); 244 in all. Per floor: section 8.
- The nearest one to the entrance is floor 1 (6, 15), 22 steps from the stairs (verified).
- A **one-shot event** (gold coins, the Demon King, the final battles and the other story events) also runs
  once per floor visit.
- **Every floor change re-arms all guarded squares and one-shot events** of the floor. Going down the stairs and
  back up brings the guards (and their chests) back
  ([findings](findings.md#29-guards-and-one-shot-events-re-arm-on-every-floor-change)).

**Notes:** whether the story events also stay done for good, apart from this per-visit reset, was not traced.

Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types),
[monsters.md §2.1](../tech/monsters.md#21-when-a-fight-starts),
[§2.2](../tech/monsters.md#22-fixed-fights)

---

## 5. Chests

A chest appears **only after winning a guarded-square fight**. Random fights give gold only.

### 5.1 Chest rating, chest value, tier

Three numbers lead to the chest:

1. **Chest rating** (per monster): every monster has one (the "Chest" column of
   [monsters_table.md](monsters_table.md)). The fight's rating R is the highest rating among the monster groups
   present.
2. **Chest value** V (rolled): drawn from row R of a table. Row R holds values from 0 to R (from 1 to R for ratings 30-48), so a stronger monster
   allows a better chest but does not guarantee one.
3. **Tier** (from the value): the kind of chest, below.

Selected rows of the table (rows in between are not listed here):

| Rating R | Chest you get |
|---|---|
| 0-6 | always a Leather bag |
| 12 | 11% Leather bag, 89% Bronze |
| 24 | mostly Silver |
| 36 | 66% Platinum |
| 49-63 | almost flat: from 14-16% Leather bag up to 19% Bewitching (no monster has a rating this high, [findings](findings.md#34-chest-ratings-above-47-are-never-used)) |

**Tier** from the value V:

| V | Tier | Contents level cap |
|---|---|---|
| 0-6 | Leather bag | 6 |
| 7-12 | Bronze | 12 |
| 13-18 | Copper | one cap per tier, not listed |
| 19-24 | Silver | |
| 25-30 | Gold | |
| 31-35 | Platinum | |
| 36-40 | Paulownia | |
| 41-45 | Lacquered | |
| 46 | Jet-black | |
| 47 and up | Bewitching | |

Tech: [items.md §10.1](../tech/items.md#101-chest-value-and-type)

### 5.2 Gold

The chest adds `10 × (4 + a random number from 0 to V)` G to the fight's gold, which is split among the members who
are OK, Afraid or Asleep ([town.md](town.md#42-the-split)). A bag of value 3 gives 40-70 G; any Leather bag (V 0 to 6) gives
40-100 G (computed from the formula).

Tech: [items.md §9](../tech/items.md#9-gold-sources)

### 5.3 Items

The chest makes 1 to 4 attempts (equal odds):

1. Each attempt picks a random party member. The member must be OK, Afraid or Asleep.
2. The attempt succeeds if a random number from 0 to 99 is below `level/2 (at most 31) + 2 × LUK`.
3. The item comes from one of 47 item lists (0-46): the list is a random number from 0 to V − 1, then a random entry
   of that list. Lists hold 6-17 items, some repeated so that they come up more often: list 0 is starter gear and
   potions, lists 26-29 hold the class items (The Avenger, Valiant Shield...), list 46 holds the Revival Charm,
   Excalibur, Muramasa and Ura Muramasa.
4. The item goes into the member's first free inventory space, **unidentified**. With no free space it is lost.

Because the list is any number below V, a high-value chest can still roll a low list.

**Notes:** a few items may be handed out only once: the game can check whether an item already exists in the shop,
the party or the roster. Where that check is used was not traced (inferred: the chests).

Tech: [items.md §10.2](../tech/items.md#102-chest-contents), [§6](../tech/items.md#6-shop-lorelei)

### 5.4 Chest quality by floor

Computed: for each floor, the encounter areas of its guarded squares, their formations, and the highest chest
rating of the monsters in each formation, from [monsters_table.md](monsters_table.md). "Best possible" is the tier
of value R, the top of the row.

| Floors | Chest rating R of the guard fights | Best possible chest |
|---|---|---|
| 1-5 | 1-6 | Leather bag |
| 6 | 3-10 | Bronze |
| 7 | 6-9 | Bronze |
| 8 | 8-11; 15-25 in the damage zone | Gold (damage zone only) |
| 9-10 | 10-12 | Bronze |
| 11 | 12-13; 15-25 in the damage zone | Gold (damage zone only) |
| 12 | 14-23 | Silver |
| 13 | 39 (Umber Hulk guards) | Paulownia |
| 14-17 | 16-24 | Silver |
| 18 | 17-27 | Gold |
| 19 | 21-29 | Gold |
| 20 | no guarded squares | none |
| 21-24 | 25-34 | Platinum |
| 25 | 35-37; 15-25 in the damage zone | Paulownia |
| 26-27 | 37-44 | Lacquered |
| 28 | 43-46 | Jet-black |
| 29-30 | 42-47 | Bewitching |

**Notes:** the floor-13 Umber Hulk guards and the damage-zone guards on floors 8 and 11 give much better chests than
the rest of their floor; the damage-zone guards on floor 25 give worse ones.

Tech: [items.md §10.1](../tech/items.md#101-chest-value-and-type)

---

## 6. Chest traps

Every chest rolls one trap from a table for its tier (or no trap). Fire Bolt is the most common trap at every tier.

| Tier | No trap | Fire Bolt | Bomb | Poison Needle | Paralysis Needle | Others |
|---|---|---|---|---|---|---|
| Leather bag | 44% | 44% | 3% | 6% | 3% | none |
| Bronze | 25% | 38% | 12% | 12% | 6% | Magic Drain, Alarm, Hand of the Dead, Last Kiss 2% each |
| Copper | 25% | 34% | 12% | 12% | 6% | as Bronze, + Paralysis Gas |
| Silver | 19% | 34% | 12% | 12% | 6% | + Energy Drain, Medusa's Curse |
| Gold | 19% | 31% | 12% | 12% | 6% | + Teleporter |
| Platinum | 19% | 30% | 12% | 12% | 6% | + Level Teleporter |
| Paulownia | 12% | 30% | 12% | 12% | 12% | all 13 kinds |
| Lacquered | 12% | 28% | 12% | 12% | 12% | Hand of the Dead 5% |
| Jet-black | 6% | 28% | 12% | 12% | 12% | Magic Drain, Alarm, Hand of the Dead, Last Kiss 5-6% |
| Bewitching | 6% | 25% | 12% | 12% | 12% | as Jet-black, Paralysis Gas and Medusa's Curse 3% |

The 13 trap kinds: Fire Bolt, Bomb, Magic Drain, Energy Drain, Poison Needle, Alarm, Hand of the Dead, Paralysis
Needle, Paralysis Gas, Medusa's Curse, Last Kiss, Teleporter, Level Teleporter.

**Effects known** (N = the tier's contents level cap, section 5.1):
- **Fire Bolt** hits the member who opens the chest for `Nd8`: 6d8 (6-48) from a Leather bag, 12d8 (12-96) from a
  Bronze chest (computed), against a new character's 4-12 HP before the VIT bonus.
- **Bomb** hits every member for `Nd4` (6d4 = 6-24 from a Leather bag, computed); each member dodges if a random
  number from 0 to 99 is below their LUK (a LUK% chance).
- The other 11 trap effects are known only by their names.

**Notes:** the rules for inspecting and disarming chests were not traced. The Priest spell Inspect and the Kunoichi
art Trap Breaker are inferred from their names to check or disarm chest traps (see [spells.md](spells.md)).

Tech: [items.md §10.3](../tech/items.md#103-traps)

---

## 7. Events

What each kind of event does in play. Where an event appears is in the floor table (section 8). The exact odds of
the well, the junk pile and the corpses were not traced.

| Event | What happens |
|---|---|
| **Magic circle** (16) | "A strange pattern is drawn on the ground." With a Summoner who can act in the party: "Who will step inside?"; the circle's summon appears, and a Summoner of at least the circle's minimum level forms a pact. List of circles and rules: [spells.md](spells.md#6-summoner-pacts). |
| **Recruitable adventurer** (8) | Murphy, Lloyd, Louie, Siegfried, Laila, Kojiro, Badick, Warnard. Each offers to join ("Add Murphy?") if the roster has fewer than 20 characters; a per-adventurer condition (not traced) is also checked. |
| **Button panel** | Buttons A-E; the elevator (inferred), destinations not traced. |
| **Key-hole** | "Beside the door is a hole for slipping something in": a door that needs an item (inferred: a key; the Key Card is the "elevator key"). |
| **Corpse** | Nothing, or the corpse rises and attacks. |
| **Gold coins** (one-shot) | "Gold coins lie scattered. Pick them up?": gold (amount not traced), or the coins come alive (fight). |
| **Weird robed monster** (one-shot) | A fight; the monster drops something, found later on a nearby square ("You found what the monster dropped earlier"). |
| **Hermit in seiza** (one-shot) | A fight. |
| **Demon King on his throne** (one-shot) | A fight; he withdraws. |
| **Peerless beauty** (one-shot) | The town of succubi and the Succubus Queen. |
| **Demons' court** (one-shot) | The court of the Emperor of the Abyss: "The Emperor awaits you." |
| **Space tears open** (one-shot) | A rift monster appears. |
| **Giant bow** (one-shot) | A giant bow appears, its arrow aimed at the party. |
| **Something rises from the pond** (one-shot) | An encounter at a pond. |
| **Priest of the netherworld** (one-shot) | An encounter in the cemetery. |
| **Huge creature** (one-shot) | It asks for help ("HELP US"). |
| **Town of Umber Hulks** (one-shot) | An Umber Hulk settlement. |
| **Man in jet black** (one-shot) | A man in jet black: "So Adish is dead". |
| **Ancient One from the rift** (one-shot) | Something gigantic comes through a rift. |
| **Emperor of the Abyss** (one-shot) | The final battle with Demon Adish. |
| **The last, strongest monster** (one-shot) | The true final battle. |
| **Demonic seal** (one-shot) | "A mighty demonic seal has been placed here." |
| **Signs** | Texts such as Torture Chamber, Prison, Maze Cemetery, Chapel, a gentle slope, "Danger ahead!", "Anti-magic space", "Maze Elevator Control Room". Which sign stands where was not traced. |
| **Giggling** | Giggling laughter ("A man?"). |
| **Fairy twins** | They flee, unless the party carries the Fairy's Heart; then a twin offers to teleport the party to the other twin for 1 G (floors 1 and 11). |
| **Junk pile** | A random find, or nothing. |
| **Monster's drop** | "You found what the monster dropped earlier." |
| **Well** | "Drink from it?" One random outcome: HP restored, poison, cure, heavy damage or paralysis. |
| **Sorcerer** | Sells levitation for 500 G (float over pits and chutes). |
| **Maid** | "If you..." A service; what she offers was not traced. She appears on floors 7, 20 and 30. |
| **Small monster on the ceiling** | An encounter with a ceiling creature. |
| **Handsome man in a cloak** | A hint at a vampire. |
| **Queen of Darkness** | An encounter on floor 16. |
| **Alarm** | "Suddenly an alarm blared": a fight with the square's encounter area. |
| **Ending text** | "Thanks for playing! You can now safely turn the power off." |
| **Map Record Sheet** | Offers to use the Map Record Sheet item. |

Tech: [dungeon.md §3](../tech/dungeon.md#3-event-catalogue),
[monsters.md §8](../tech/monsters.md#8-summoner-pacts)

---

## 8. Floor by floor

Counts per floor; coordinates are (x, y). "Areas" are the random-encounter areas (monsters in the
[encounter tables](monsters_table.md)); "Guarded" gives the number of guarded squares and their areas. A magic
circle is named by its summon ([spells.md](spells.md#6-summoner-pacts)). Floor maps and their legend:
[maps/README.md](maps/README.md); floor 1 has its own map page, [maps/floor-01.md](maps/floor-01.md).

| Floor | Stairs (x, y) | Areas | Guarded | Traps / hidden spots | Events |
|---|---|---|---|---|---|
| [1](maps/floor-01.md) | up (0,15) = exit to town; down (15,0) | 1, 2, 3 | 8 (areas 1-3) | 2 pits; 6 hidden | Zombie circle (15,15); fairy twin (2,12); gold coins (5,4) |
| 2 | up (15,0); down (0,15) | 4 | 3 (area 4) | 4 rockfall, 3 pits; 2 hidden | Murphy (9,10) |
| 3 | up (0,15); down ×3 (14,15) (8,8) (14,1) | 5 | 14 (areas 5, 6) | 2 hidden | Ghoul circle (4,0); button panel + key-hole (1,1)/(1,2) |
| 4 | up ×3; down (3,4) | 6 | 21 (area 6) | 3 spinners, 3 pits | weird robed monster (4,8); its drop (3,8); sign (7,9); buttons + key-hole |
| 5 | up (3,4); down (7,8) | 7 | 11 (area 7) | 2 chutes, 4 pits, spinner | Lloyd (1,11); Lion of Hell circle (15,9); ceiling monster (5,5); buttons + key-hole |
| 6 | up (7,8); no down | 8 | 5 (area 8) | chute (0,15) → floor 7 (inferred); 4 hidden | Louie (12,3); 3 alarm squares; buttons + key-hole |
| 7 | no up; down (15,0) | 9 | 6 (area 9) | 10 hidden; 4 warps into the closed rooms | maid (1,14); 2 button panels + key-holes |
| 8 | up (15,0); down (4,14) (13,13) | 10, 101 (damage zone) | 14 (areas 10, 101) | 4 hidden | hermit (2,14); pond (3,10); Minotaur circle (3,8); Siegfried (8,8); well (14,3); 3 signs |
| 9 | up ×2; down (0,15) | 11 | 8 (areas 11, 12) | 4 pits; 4 hidden | Djinni circle (11,5); Laila (1,0); Kojiro (3,3); 2 signs |
| 10 | up (0,15); down (0,0) | 12 | 2 (area 12) | 2 hidden | 26 corpses (the cemetery); priest of the netherworld (1,1); 4 signs |
| 11 | up (0,0); down (15,15) | 13, 102 (damage zone, half the floor) | 10 (areas 13, 102) | 3 vipers, 3 rockfall, 2 pits | fairy twin (11,12); Badick (6,6); levitation sorcerer (8,3); sign |
| 12 | up (15,15); down (0,0) | 14 | 7 (area 14) | 1 hidden | Ifrit circle (8,15); huge creature (3,6); Warnard (8,2) |
| 13 | up (0,0); down (0,15) | 15 | 5 (area 50: a fixed Umber Hulk formation) | 2 hidden | Umber Hulk town (8,7); Dao circle (9,3) |
| 14 | up (0,15); down (9,1) | 16 | 14 (area 16) | 2 ceiling traps | cloaked man (12,15); Marid circle (12,1) |
| 15 | up (9,1); down (15,15) | 17 | 11 (area 17) | 3 spinners, rockfall; 4 hidden | ceiling monster (9,3); Titan circle (0,2) |
| 16 | up (15,15); down (14,1) | 18 | 7 (area 18) | none | Queen of Darkness (14,4) |
| 17 | up (14,1); down (8,8) | 19 | 6 (area 19) | none | **Demon King** (7,7) |
| 18 | up (8,8); down (6,1) | 20 | 11 (areas 20, 51) | 4 hidden | Greater Demon circle (15,13); giggling (7,10); **succubus beauty** (5,6) |
| 19 | up (6,1); no down | 21 | 7 (areas 21, 22) | 2 pits, spinner, chute (0,5) → floor 20 (inferred) | demons' court (7,8); junk pile (8,8) |
| 20 | none | 22 | 0 | none | **Emperor of the Abyss / Demon Adish** (8,7); maid (0,2); demonic seal (0,0); 3 signs |
| 21 | no up; down (12,2) | 23 | 6 (areas 23, 24) | 27 floor traps; 3 hidden | Vampire Lord circle (0,3) |
| 22 | up (12,2); no down | 24 (+25, 26: one square each) | 8 (area 24) | 12 traps | none |
| 23 | no up; down ×5 | 25 (+27: three squares) | 8 (areas 25, 26) | 12 traps; 4 hidden | Shadow Dragon circle (13,3) |
| 24 | up ×5; down ×3 | 26 (+29: two squares) | 6 (area 26) | chute, 2 pits; 1 hidden | Magic Gate circle (7,15) |
| 25 | up ×4; no down | 27, 103 (damage zone) | 11 (areas 27, 103) | 20 traps (many spinners) | well (0,0) |
| 26 | none | 28, 29 | 5 (areas 28, 30) | 11 traps (5 vipers, 4 pits, 2 rockfalls) | Ancient One circle (12,3) |
| 27 | none | 29, 104 (damage zone) (+31: one square) | 4 (area 31) | 8 traps | none |
| 28 | none | 30 (+32: one square) | 5 (area 32) | **122 trap squares** (mostly spinners) | none |
| 29 | none | 31, 33 | 17 (areas 31, 33) | 13 traps, chute | From Beyond circle (11,1) |
| 30 | none | 32, 33, 105 (damage zone) | 4 (areas 32, 33) | 18 traps | Unspeakable circle (7,15); space rift (1,8); giant bow (6,5); Ancient One rift (12,7); man in jet black (1,11); maid (15,11); well (12,10); **final battle** (15,14) |

**Single squares with another area.** A few squares carry another floor's encounter area: floor 22 area 25 at
(14,2) and 26 at (15,2); floor 23 area 27 at (7,7) and on the down stairs (7,8) and (8,7); floor 24 area 29 at (7,9)
and on the stairs (6,9); floor 27 area 31 on the warp (13,10); floor 28 area 32 on the trap (8,8). A random fight
on such a square would use that area (inferred; not seen). This is why the encounter tables list these areas on
more floors than the table above ([findings](findings.md#31-single-squares-carry-another-floors-encounter-area)).

Tech: [dungeon.md §4](../tech/dungeon.md#4-floors)

---

## 9. Auto-map

The in-game auto-map is a full-screen plan of one floor. It shows only the squares the party has **stood on**, with
their walls and doors and icons for a few kinds of squares. It is the only map the game gives the player (all
verified unless tagged).

**Opening it.** There is no map button. Three things open it:

| How | Notes |
|---|---|
| **Compass** (camp spell) | view only |
| **Map Record Sheet** (item): use it in camp, or press **Select** in the maze while anyone carries it ("Use the map record sheet?", cursor on No) | view only. Each use has a 30% chance to crumble the sheet silently; the map still opens that time. It does **not** complete the map ([findings](findings.md#37-the-map-record-sheet-does-not-complete-the-map)) |
| **Teleport** (spell) or the **Ring of Warping** (item, breaks 25%) | the map becomes a destination picker (below) |

Teleport cast in battle opens no map: it puts the party on a random square of the current floor (code only).

**What it shows.**
- Only visited squares: every square the party stands on is remembered, for good (saved with the game). The Map
  Record Sheet adds nothing.
- Walls and doors. Locked doors look like doors; a secret door looks like a wall until it is found.
- Icons: stairs up and down, chutes, the other floor traps (one icon for pit, ceiling trap, rockfall and viper),
  spinners, warps, events (one icon for every kind), and an "E" on elevator panels.
- No icon: hidden spots, lock squares, guarded squares, the adventurers' squares and rock.
- Lake squares are blue, magic-seal squares dotted red; dark zones are not drawn.
- The party arrow, on the party's own floor only.

**Controls.**

| Key | Map | Cursor |
|---|---|---|
| Up / Down | previous / next floor, from floor 1 to the deepest floor reached (wraps) | move the cursor |
| Left / Right | - | move the cursor |
| A | cursor mode (starts on the party) | Teleport: jump to the cursor square; otherwise nothing |
| B | close (not while teleporting) | back to the map |

In cursor mode the top line names the visited square under the cursor (wall, stairs, elevator, the trap kind, warp,
event, or the zone: lake, magic seal, dark zone). On a visited warp a side panel shows where it leads (floor, east,
north) and marks the destination when it is on the floor shown.

**Teleport through the map.** The destination is the cursor square on the floor being viewed, so any floor from 1 to
the deepest reached. It must be a **visited** square; otherwise "You were sent back." and the party stays, but the
spell or Ring is used up. The cast cannot be cancelled ([findings](findings.md#39-a-teleport-to-an-unvisited-square-is-wasted-and-teleport-cannot-be-cancelled)). Landing on a warp does not set it off.

**Floor numbers.** The map shows floors 1-20 as B1-B20, but floors 21-30 as B30, B31, B270, B271, B272, B358, B424,
B485, B570 and B666 (game data, deliberate: the text mode uses the same numbers) ([findings](findings.md#38-floors-21-30-are-numbered-b30-to-b666-on-the-map)).

**Mode Settings "Map: Mania".** This option replaces the map with the classic text screens: Compass and the sheet
print the party's floor, north, east and facing; Teleport asks for a floor and offsets north and east of here
(−15 to +15). In this mode a destination off the 16 × 16 grid puts the party in rock: everyone dies ("In rock").

Tech: [dungeon.md §6](../tech/dungeon.md#6-auto-map)

---

## Open questions

1. **How floor 21 is first entered** (floors 22-29 connect by warps, section 2). Candidates: the
   button panels (elevator) or an event after the ending (the game notes a second clear). Not traced.
2. **Elevator:** the destinations of buttons A-E and which item each key-hole needs.
3. **Chutes:** how many floors they drop. **Pits, ceiling traps, rockfall:** damage amounts.
4. **Floors 7 and 20:** how the party goes back up (no up stairs).
5. **Floor 25** has four up stairs but floor 24 only three down stairs; where the fourth leads was not checked.
6. **Hidden spots:** the difficulty value of each spot and how long a spot stays used.
7. **Random teleport curse:** whether the random square can be rock (instant party death), and which items cause it.
8. **Damage zone protection:** what gives it (inferred levitation or a ward), and whether the Levitate spell gives the
   same floating as the sorcerer's levitation.
9. **Dark zone:** whether any light spell or item works inside it.
10. **Event outcomes:** the odds of the well, the junk pile and the corpses; the gold-coins amount; what the maid
    offers; which sign text stands where; whether story events stay done for good.
11. **Single squares with another area** (floors 22-28): whether a random fight really starts there with that area
    (inferred, not seen).
12. **Chests:** the contents level cap of tiers above Bronze (used by the trap damage), what a chest of value 0
    gives (the list roll is from 0 to V − 1), and the trap inspect/disarm rules.

Tech: [dungeon.md §5](../tech/dungeon.md#5-not-found--open), [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried)
