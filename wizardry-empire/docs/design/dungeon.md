# The dungeon (the maze)

How Wizardry Empire's maze is built and what it does to the party: floors and how they connect, square types,
traps, damage zones, guarded squares, events per floor, chests and chest traps. Notation, dice and confidence tags:
[README.md](README.md). Quirks are explained in [findings.md](findings.md). Untagged numbers are **(data)**: read
from the game's tables or code, not observed in play.

Related documents: monsters and encounter formations in [monsters.md](monsters.md) and
[monsters_table.md](monsters_table.md); items found in chests in [items.md](items.md) and
[items_table.md](items_table.md); Summoner pacts in [spells.md](spells.md).

---

## Overview (two-minute read)

- **30 floors**, each a **16 × 16 grid whose edges wrap around**: walking off the east edge brings you in on the
  west edge. **(data)**
- **Floors 1-20** are the main dungeon, linked by stairs plus two chutes. Floor 20 is the floor of the Emperor of
  the Abyss and the final battle with Demon Adish; it has no stairs. **Floors 21-30** are a second, harder area
  (monsters of level 20-30). No stairs lead there from floor 20, and how the party gets there has not been traced
  ([findings](findings.md#floors-21-30-are-not-reached-by-stairs)).
- **Stairs keep your position:** a down stair at (x, y) on floor n puts you on the up stair at (x, y) on floor n+1.
- **Random fights are rare** except right after a door: the chance per action is 1 in 512 (0.2 %), and 13 in 256
  (5.1 %) after stepping through a door ([findings](findings.md#random-encounters-almost-only-happen-after-doors)).
- **Guarded squares** (0-21 per floor) hold a fixed fight. They are the **only fights that give a chest**, and
  they **re-arm every time you change floors**, together with the floor's one-shot events.
- **Squares can hurt you:** pits, chutes, ceiling traps, rockfall, vipers (poison) and spinners; **damage zones**
  take a quarter of every member's max HP per action; **anti-magic zones** cancel the party's spell effects;
  **rock** kills the whole party if a teleport puts it there.
- **Events:** 16 magic circles (Summoner pacts), 8 recruitable adventurers, elevator button panels with key-holes,
  wells, a levitation seller, fairy twins that teleport between floors 1 and 11, a maid, corpses that may rise, signs,
  and the story encounters (Demon King, Succubus Queen, the Emperor's court, the final battles on floors 20 and 30).
- **Chests:** the chest's value comes from the strongest monster group in the guard fight. Value sets the chest tier
  (Leather bag up to Bewitching), the gold (10 × (a random number from 0 to the value, + 4)), which item lists can
  drop, and the trap odds. Fire Bolt is the most common trap at every tier.

---

## Map layout and coordinates

Each floor is a 16 × 16 grid of squares. A square stores its four walls, an encounter area (which monsters can
appear there), a square type and one parameter (an event number, trap kind and so on).

- **Coordinates** are written (x, y), x from 0 to 15 going east, y from 0 to 15 going north. (0, 15) is the
  north-west corner. The maze entrance is the up stair at (0, 15) on floor 1.
- **Wrapping:** both coordinates wrap, so the grid is a torus. **(data)**
- **Walls** (one per side of the square): open; wall (bumping says "Ouch!"); door (walking through it raises the
  random-fight chance, see [Random encounters](#random-encounters)); and a fourth "special" value whose behaviour
  was not traced.
- **Square types:** see [Square types](#square-types).
- **Encounter area:** a number from 0 to 105. 0 means no random fights on that square. Areas 1-33 are the normal
  areas of the floors, 101-105 cover the damage zones. Areas 34-53 are fixed fights started by events.

**Notes:** the game keeps a visited-square memory per floor and the deepest floor reached (marker squares,
below); this is inferred to feed the auto-map.

Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format-code-2058ea-205909)

---

## How floors connect

The party moves between floors by stairs, chutes, teleporting events and (inferred) an elevator.

- **Stairs.** Stepping on a stair asks Yes/No. Yes moves you one floor up or down and keeps x and y, so every down
  stair sits directly above an up stair. Every floor change re-arms the guarded squares and one-shot events of the
  floor you arrive on.
- **Chutes** are floor traps (see [Floor traps](#floor-traps)) on floors 5, 6, 19, 24 and 29. How many floors a
  chute drops was not traced. The chute at (0, 15) on floor 6 is inferred to lead to floor 7, and the one at
  (0, 5) on floor 19 to floor 20, because those floors have no stairs between them. **(inferred)**
- **Fairy twins** (Rei and Shia): with the Fairy's Heart in the party, one twin teleports the party to the other
  for 1 G, between floor 1 (2, 12) and floor 11 (11, 12).
- **Button panels and key-holes.** Floors 3 to 7 have a panel with buttons A-E next to a door with a key-hole.
  A sign reading "Maze Elevator Control Room" exists, and one item's special text is "elevator key" (Key Card),
  so the panels are inferred to be the **Maze Elevator**. **(inferred)** Their destinations were not traced.
- **Events that teleport** (any event can return a floor or position change).

Stair links (from the floor table below):

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
Floors 21-30: [findings](findings.md#floors-21-30-are-not-reached-by-stairs).

Tech: [dungeon.md §4](../tech/dungeon.md#4-floors), [§5](../tech/dungeon.md#5-not-found--open)

---

## Square types

What happens when the party steps on (or into) a square. The same types exist on every floor; a few extra types
are tied to one floor's events.

| Square | What it does to the party |
|---|---|
| Floor | Nothing. |
| **Rock** | Only reachable by teleport. Everyone's HP drops to 0, everyone is Dead ("In rock"), and the party is lost. |
| **Stairs up / down** | Yes/No prompt; one floor up or down, same x, y. |
| **Hidden spot** | Members may notice something (see [Hidden spots](#hidden-spots)). |
| **Guarded square** | A fixed fight, once per floor visit; winning gives a chest (see [Guarded squares](#guarded-squares-and-one-shot-events)). |
| **Button panel** | "A row of buttons. Which one will you press? A B C D E" (the elevator, inferred). |
| **Floor trap** | Chute, pit, ceiling trap, rockfall, viper or spinner (see [Floor traps](#floor-traps)). |
| **Marker** | Nothing visible; records the square as visited and the deepest floor reached (inferred: auto-map memory). |
| **Event** | Runs one of the events in the [catalogue](#events). |
| **Corpse** | "A monster's corpse lies here": nothing, or "The corpse began to move!" and a fight. |
| **One-shot event** | A story or special event that runs once per floor visit. |
| **Floor-specific** | A fixed event chosen per floor: signs, the fairy, the maid, the well, alarms. |

After an event, the game either does nothing, starts a fight with a given encounter area, or (if the event moved
the party) reloads the map.

Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types-handler-table-206405-per-floor-types-0-14-are-the-same-on-every-floor)

---

## Floor traps

Trap squares on the floor (not chest traps). Floor 28 is almost all traps (122 trap squares, mostly spinners).

| Trap | Effect |
|---|---|
| **Chute** | Drops the party to a lower floor (how far: not traced). Skipped when the party is floating ("But you are floating"). |
| **Pit** | Damage (amount not traced). Skipped when floating. |
| **Ceiling trap** | Damage (amount not traced). |
| **Rockfall** | Damage (amount not traced). |
| **Viper** | Each member rolls to avoid poison (below). |
| **Spinner** | Turns the party to a random facing. |

**Viper:** each member is safe if a random number from 0 to 99 is below `level/2 + LUK − trap strength`, where the
trap strength is set per square. A roll of 0-4 always poisons and a roll of 99 always saves, so the poison chance
is never below 5 % or above 99 %.

**Floating:** the levitation the sorcerer on floor 11 sells for 500 G lets the party float over pits and chutes.

**Notes:** the same party flag that marks floating is inferred to protect against damage zones too (below).

Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types-handler-table-206405-per-floor-types-0-14-are-the-same-on-every-floor)

---

## Hidden spots

Squares where a sharp-eyed member may notice something ("X noticed something"). They come in pairs on both sides of
a wall, so they are inferred to be **hidden doors**. **(inferred)**

Each member who is OK, Afraid or Asleep rolls once. Skill by class (level = character level):

| Class | Skill |
|---|---|
| Thief | LUK/2 + 5 × level |
| Ninja | LUK/2 + 5 × level − 25 |
| Kunoichi | LUK/4 + 5 × level − 50 |
| Everyone else | level/4 − 10 |

Difficulty = 5 × a value set for each spot. The tech note gives the chance as 4 % per point of skill above the
difficulty while the margin is under 5 points, and 80 % otherwise, plus 1 % on a roll of 0 (see Open questions:
the wording leaves the exact cap unclear).

**Notes:** a spot is one-shot; how long it stays used was not traced.

Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types-handler-table-206405-per-floor-types-0-14-are-the-same-on-every-floor)

---

## Damage zones and anti-magic zones

Two zone markings sit on top of a square's type.

**Damage zone.** After every action (step or turn) in the zone, each member who is not Dead, Ashes or Lost loses
`maxHP/4 + 1` HP and dies at 0 ("... has died"). A party-wide protection flag prevents it; this is inferred to be
levitation or a ward. **(inferred)** Without protection a full-HP character dies after at most 4 actions (four hits
of `maxHP/4 + 1` always add up to more than max HP). Damage-zone squares have their own encounter areas (101-105).

**Anti-magic zone.** Entering it cancels all party-wide spell effects. It is inferred to be the "Anti-magic space"
named on a sign. **(inferred)**

| Floor | Zone squares |
|---|---|
| 5 | 60 with the fourth zone value (no effect found) |
| 6 | 58 anti-magic |
| 8 | 16 damage (area 101) |
| 11 | 121 damage (area 102, about half the floor) |
| 12 | 19 with the fourth zone value |
| 15, 18, 22-24, 26 | zone squares present (kind not listed in the tech notes) |
| 25 | damage zone (area 103) |
| 27 | 15 damage (area 104) |
| 28 | 126 with the fourth zone value, 41 anti-magic |
| 30 | 16 damage (area 105) |

**Notes:** "not Dead, Ashes or Lost" includes Stoned members
([findings](findings.md#stoned-members-still-take-damage-zone-damage)). The fourth zone value has no known effect
([findings](findings.md#map-values-with-no-known-effect)).

Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format-code-2058ea-205909)

---

## Random teleport curse

If any party member carries a certain status flag, **each step has a 50 % chance to put the party on a random
square of the current floor**. The flag is inferred to come from items with the special property "teleport"
(see [items.md](items.md)). **(inferred link)**

**Notes:** whether the random square can be rock (which kills the party) was not traced; see Open questions.

Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format-code-2058ea-205909)

---

## Random encounters

Which monsters a square can produce and how often. Formations and group sizes are in [monsters.md](monsters.md)
and the [encounter tables](monsters_table.md).

- The chance is checked after **every action** in the maze (step, turn, turn-around).
- **Normal chance: 1 in 512 (0.2 %) per action.** (verified: 357 random actions in the emulator gave 1 fight)
- **After walking through a door: 13 in 256 (5.1 %) per action**, until the next plain step or turn-around.
  Turning left or right keeps the higher chance.
- No step counter and no depth bonus: the rate is the same on every floor.
- A fight needs a non-zero encounter area on the current square. Some corridors on floors 2, 9, 13, 17, 19, 21,
  22 and 25 have area 0 and never have random fights.
- Each area lists 4 formations (one is picked at random); a formation has up to 4 groups of 1-9 monsters.
- Areas 48 and 49 (the Demon Adish and Abyss Lurker formations) play the boss music.

**Notes:** the very low base rate makes doors the place where fights happen, and turning on the spot after a door
keeps the 5.1 % chance ([findings](findings.md#random-encounters-almost-only-happen-after-doors)). Random fights
never give a chest (verified: 25 random battles, no chest). Areas 54-100 are on no map
([findings](findings.md#encounter-areas-54-100-are-unused)).

Tech: [monsters.md §2.1](../tech/monsters.md#21-when-a-fight-starts-code-204422-4460-emu),
[§2.3](../tech/monsters.md#23-group-formation-code-2240c7-41b5-data-397a27-397573)

---

## Guarded squares and one-shot events

Guarded squares are fixed spots where monsters wait; one-shot events are story and special encounters.

- A **guarded square** starts a fight with its own encounter area as soon as the party steps on it. It fights
  **once per floor visit**. Winning gives a **chest** (the only source of chests).
- Guarded squares per floor: from 0 (floor 20) and 2 (floor 10) up to 21 (floor 4); see the floor table.
- The nearest one to the entrance is floor 1 (6, 15), 22 steps from the stairs. **(verified)**
- A **one-shot event** (gold coins, the Demon King, the final battles and the other story events) also runs
  once per floor visit.
- **Every floor change re-arms all guarded squares and one-shot events** of the floor. Going down the stairs and
  back up brings the guards (and their chests) back
  ([findings](findings.md#guards-and-one-shot-events-re-arm-on-every-floor-change)).

**Notes:** whether the story events also keep a permanent "done" flag of their own was not traced.

Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types-handler-table-206405-per-floor-types-0-14-are-the-same-on-every-floor),
[monsters.md §2.2](../tech/monsters.md#22-fixed-fights)

---

## Events

What each kind of event does in play. Where an event appears is in the [floor table](#floor-by-floor). The exact
odds of the well, the junk pile and the corpses were not traced.

| Event | What happens |
|---|---|
| **Magic circle** (16, circles 0-15) | "A strange pattern is drawn on the ground." With a Summoner who can act in the party: "Who will step inside?"; a Summoner of at least the circle's level forms a pact (table below, rules in [spells.md](spells.md)). |
| **Recruitable adventurer** (8) | Murphy, Lloyd, Louie, Siegfried, Laila, Kojiro, Badick, Warnard. Each offers to join ("Add Murphy?") if the roster has fewer than 20 characters; a per-character join flag is also checked. |
| **Button panel** | Buttons A-E; the elevator (inferred), destinations not traced. |
| **Key-hole** | "Beside the door is a hole for slipping something in": a door that needs an item (inferred: a key; the Key Card is the "elevator key"). |
| **Corpse** | Nothing, or the corpse rises and attacks. |
| **Gold coins** (one-shot) | "Gold coins lie scattered. Pick them up?": gold (amount not traced), or the coins come alive (fight). |
| **Weird robed monster** (one-shot) | A fight; the monster drops something, found later on a nearby square ("You found what the monster dropped earlier"). |
| **Hermit in seiza** (one-shot) | A fight. |
| **Demon King on his throne** (one-shot) | A fight; he withdraws. |
| **Peerless beauty** (one-shot) | The town of succubi and the Succubus Queen. |
| **Demons' court** (one-shot) | "The Emperor awaits you." |
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
| **Maid** | "If you..." A service (not described in the tech notes); she appears on floors 7, 20 and 30. |
| **Small monster on the ceiling** | An encounter with a ceiling creature. |
| **Handsome man in a cloak** | A hint at a vampire. |
| **Queen of Darkness** | An encounter on floor 16. |
| **Alarm** | "Suddenly an alarm blared": a fight with the square's encounter area. |
| **Ending text** | "Thanks for playing! You can now safely turn the power off." |
| **Map record sheet** | "Use the map record sheet?" |

**Magic circles** (floor from the floor table; level = minimum Summoner level; summon learned per the spell
tables, see Open questions):

| Circle | Floor | Level | Summon |
|---|---|---|---|
| 0 | 1 | 3 | Zombie |
| 1 | 3 | 4 | Ghoul |
| 2 | 5 | 6 | Lion of Hell |
| 3 | 8 | 10 | Minotaur |
| 4 | 9 | 14 | Djinni |
| 5 | 12 | 15 | Ifrit |
| 6 | 13 | 16 | Dao |
| 7 | 14 | 17 | Marid |
| 8 | 15 | 20 | Titan |
| 9 | 18 | 23 | Greater Demon |
| 10 | 21 | 27 | Vampire Lord |
| 11 | 23 | 31 | Shadow Dragon |
| 12 | 24 | 34 | Magic Gate |
| 13 | 26 | 36 | Ancient One |
| 14 | 29 | 37 | From Beyond |
| 15 | 30 | 38 | Unspeakable |

Tech: [dungeon.md §3](../tech/dungeon.md#3-event-catalogue-bank-45-handler-table-2d4400-index-ffb0--7),
[monsters.md §8](../tech/monsters.md#8-summoner-pacts-code-2d64cf-6664-data-2d63bb)

---

## Floor by floor

Counts per floor; coordinates are (x, y). "Areas" are the random-encounter areas (monsters in the
[encounter tables](monsters_table.md)); "Guarded" gives the number of guarded squares and their areas.

| Floor | Stairs (x, y) | Areas | Guarded | Traps / hidden spots | Events |
|---|---|---|---|---|---|
| 1 | up (0,15) = exit to town; down (15,0) | 1, 2, 3 | 8 (1-3) | 2 pits; 6 hidden | circle 0 (15,15); fairy twin (2,12); gold coins (5,4) |
| 2 | up (15,0); down (0,15) | 4 | 3 (4) | 4 rockfall, 3 pits; 2 hidden | Murphy (9,10) |
| 3 | up (0,15); down ×3 (14,15) (8,8) (14,1) | 5 | 14 (5, 6) | 2 hidden | circle 1 (4,0); button panel + key-hole (1,1)/(1,2) |
| 4 | up ×3; down (3,4) | 6 | 21 (6) | 3 spinners, 3 pits | weird robed monster (4,8); its drop (3,8); sign (7,9); buttons + key-hole |
| 5 | up (3,4); down (7,8) | 7 | 11 (7) | 2 chutes, 4 pits, spinner | Lloyd (1,11); circle 2 (15,9); ceiling monster (5,5); buttons + key-hole |
| 6 | up (7,8); no down | 8 | 5 (8) | chute (0,15) → floor 7 (inferred); 4 hidden | Louie (12,3); 3 alarm squares; buttons + key-hole |
| 7 | no up; down (15,0) | 9 | 6 (9) | 10 hidden; 4 markers | maid (1,14); 2 button panels + key-holes |
| 8 | up (15,0); down (4,14) (13,13) | 10, 101 (damage zone) | 14 (10, 101) | 4 hidden | hermit (2,14); pond (3,10); circle 3 (3,8); Siegfried (8,8); well (14,3); 3 signs |
| 9 | up ×2; down (0,15) | 11 | 8 (11, 12) | 4 pits; 4 hidden | circle 4 (11,5); Laila (1,0); Kojiro (3,3); 2 signs |
| 10 | up (0,15); down (0,0) | 12 | 2 (12) | 2 hidden | 26 corpses (the cemetery); priest of the netherworld (1,1); 4 signs |
| 11 | up (0,0); down (15,15) | 13, 102 (damage zone, half the floor) | 10 (13, 102) | 3 vipers, 3 rockfall, 2 pits | fairy twin (11,12); Badick (6,6); levitation sorcerer (8,3); sign |
| 12 | up (15,15); down (0,0) | 14 | 7 (14) | 1 hidden | circle 5 (8,15); huge creature (3,6); Warnard (8,2) |
| 13 | up (0,0); down (0,15) | 15 | 5 (50: fixed Umber Hulk formation) | 2 hidden | Umber Hulk town (8,7); circle 6 (9,3) |
| 14 | up (0,15); down (9,1) | 16 | 14 (16) | 2 ceiling traps | cloaked man (12,15); circle 7 (12,1) |
| 15 | up (9,1); down (15,15) | 17 | 11 (17) | 3 spinners, rockfall; 4 hidden | ceiling monster (9,3); circle 8 (0,2) |
| 16 | up (15,15); down (14,1) | 18 | 7 (18) | none | Queen of Darkness (14,4) |
| 17 | up (14,1); down (8,8) | 19 | 6 (19) | none | **Demon King** (7,7) |
| 18 | up (8,8); down (6,1) | 20 | 11 (20, 51) | 4 hidden | circle 9 (15,13); giggling (7,10); **succubus beauty** (5,6) |
| 19 | up (6,1); no down | 21 | 7 (21, 22) | 2 pits, spinner, chute (0,5) → floor 20 (inferred) | demons' court (7,8); junk pile (8,8) |
| 20 | none | 22 | 0 | none | **Emperor of the Abyss / Demon Adish** (8,7); maid (0,2); demonic seal (0,0); 3 signs |
| 21 | no up; down (12,2) | 23 | 6 (23, 24) | 27 floor traps; 3 hidden | circle 10 (0,3) |
| 22 | up (12,2); no down | 24 | 8 (24) | 12 traps | none |
| 23 | no up; down ×5 | 25 | 8 (25, 26) | 12 traps; 4 hidden | circle 11 (13,3) |
| 24 | up ×5; down ×3 | 26 | 6 (26) | chute, 2 pits | circle 12 (7,15) |
| 25 | up ×4; no down | 27, 103 (damage zone) | 11 (27, 103) | 20 traps (many spinners) | well (0,0) |
| 26 | none | 28, 29 | 5 (28, 30) | 11 traps (6 vipers) | circle 13 (12,3) |
| 27 | none | 29, 104 (damage zone) | 4 (31) | 8 traps | none |
| 28 | none | 30 | 5 (32) | **122 trap squares** (spinner field) | none |
| 29 | none | 31, 33 | 17 (31, 33) | 13 traps, chute | circle 14 (11,1) |
| 30 | none | 32, 33, 105 (damage zone) | 4 (32, 33) | 18 traps | circle 15 (7,15); space rift (1,8); giant bow (6,5); Ancient One rift (12,7); man in jet black (1,11); maid (15,11); well (12,10); **final battle** (15,14) |

**Notes:** the generated encounter table lists a few extra random areas that the tech floor table does not
(area 26 on floor 22, 27 on 23, 29 on 24); see Open questions.

Tech: [dungeon.md §4](../tech/dungeon.md#4-floors)

---

## Chests

A chest appears **only after winning a guarded-square fight**. Random fights give gold only.

**Chest value.** Every monster has a chest row (the "Chest" column of [monsters_table.md](monsters_table.md)).
The fight's row R is the highest row among the monster groups present. The chest value V is then drawn from row R
of a table; row R holds values from 0 to R, so a stronger monster allows a better chest but does not guarantee one.

| Row | Chest you get |
|---|---|
| 0-6 | always a Leather bag |
| 12 | 11 % Leather bag, 89 % Bronze |
| 24 | mostly Silver |
| 36 | 66 % Platinum |
| 49-63 | almost flat: from 14-16 % Leather bag up to 19 % Bewitching (no monster has a row this high, [findings](findings.md#chest-rows-above-47-are-never-used)) |

**Chest tier** from the value V:

| V | Tier | Contents level cap |
|---|---|---|
| 0-6 | Leather bag | 6 |
| 7-12 | Bronze | 12 |
| 13-18 | Copper | (one cap per tier, not listed) |
| 19-24 | Silver | |
| 25-30 | Gold | |
| 31-35 | Platinum | |
| 36-40 | Paulownia | |
| 41-45 | Lacquered | |
| 46 | Jet-black | |
| 47 and up | Bewitching | |

**Gold.** The chest adds `10 × (a random number from 0 to V, + 4)` gold to the fight's gold pool, which is split
among the members who can still act. A bag of value 3 gives 40-70 G.

**Items.** The chest makes 1-4 attempts (equal odds):

1. Each attempt picks a random party member. The member must be OK, Afraid or Asleep.
2. The attempt succeeds if a random number from 0 to 99 is below `level/2 (at most 31) + 2 × LUK`.
3. The item comes from one of 47 item lists (0-46), picked as a random number from 0 to V − 1, then a random entry
   of that list. Lists hold 6-17 items, some repeated as weights: list 0 is starter gear and potions, lists 26-29
   hold the class items (The Avenger, Valiant Shield...), list 46 holds the Revival Charm, Excalibur, Muramasa and
   Ura Muramasa.
4. The item goes into the member's first empty slot, **unidentified**. With no empty slot it is lost.

Because the list is any number below V, a high-value chest can still roll a low list.

**Chest quality by floor** (computed: for each floor, the guarded-square areas, their formations, and the highest
chest row of the monsters in each formation, from [monsters_table.md](monsters_table.md); "best possible" is the
tier of value R, the top of the row):

| Floors | Chest row R of the guard fights | Best possible chest |
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

**Notes:** a few items may be handed out only once (the game checks whether an item already exists in the shop,
the party or the roster; who uses that check was not traced, inferred to be the chests). The floor-13 Umber Hulk
guards and the damage-zone guards on floors 8 and 11 give much better chests than the rest of their floor; the
damage-zone guards on floor 25 give worse ones.

Tech: [items.md §10.1](../tech/items.md#101-chest-value-and-type-2540d8-416b),
[§10.2](../tech/items.md#102-chest-contents-255185-521a), [§9](../tech/items.md#9-gold-sources),
[§6](../tech/items.md#6-shop-bank-41-lorelei)

---

## Chest traps

Every chest rolls one trap from a table for its tier (or no trap). Fire Bolt is the most common trap at every tier.

| Tier | No trap | Fire Bolt | Bomb | Poison Needle | Paralysis Needle | Others |
|---|---|---|---|---|---|---|
| Leather bag | 44 % | 44 % | 3 % | 6 % | 3 % | none |
| Bronze | 25 % | 38 % | 12 % | 12 % | 6 % | Magic Drain, Alarm, Hand of the Dead, Last Kiss 2 % each |
| Copper | 25 % | 34 % | 12 % | 12 % | 6 % | as Bronze, + Paralysis Gas |
| Silver | 19 % | 34 % | 12 % | 12 % | 6 % | + Energy Drain, Medusa's Curse |
| Gold | 19 % | 31 % | 12 % | 12 % | 6 % | + Teleporter |
| Platinum | 19 % | 30 % | 12 % | 12 % | 6 % | + Level Teleporter |
| Paulownia | 12 % | 30 % | 12 % | 12 % | 12 % | all 13 kinds |
| Lacquered | 12 % | 28 % | 12 % | 12 % | 12 % | Hand of the Dead 5 % |
| Jet-black | 6 % | 28 % | 12 % | 12 % | 12 % | Magic Drain, Alarm, Hand of the Dead, Last Kiss 5-6 % |
| Bewitching | 6 % | 25 % | 12 % | 12 % | 12 % | as Jet-black, Paralysis Gas and Medusa's Curse 3 % |

The 13 trap kinds: Fire Bolt, Bomb, Magic Drain, Energy Drain, Poison Needle, Alarm, Hand of the Dead, Paralysis
Needle, Paralysis Gas, Medusa's Curse, Last Kiss, Teleporter, Level Teleporter.

**Effects known:**
- **Fire Bolt** hits the member who opens the chest for `L d8`, where L is the chest tier's contents level cap
  (6 for a Leather bag, 12 for Bronze). A Leather bag's Fire Bolt therefore deals 6d8 = 6-48 (computed), against a
  new character's 4-12 HP before the VIT bonus.
- **Bomb** hits every member for `L d4`; each member dodges if a random number from 0 to 99 is below their LUK
  (a LUK % chance).
- The other 11 trap effects are known only by their names.

**Notes:** the rules for inspecting and disarming chests were not traced. The Priest spell Inspect and the Kunoichi
art Trap Breaker work on chests (their effects were not traced either; see [spells.md](spells.md)).

Tech: [items.md §10.3](../tech/items.md#103-traps-2547ac-table-25551c--tier256-handlers-2550f1)

---

## Open questions

What is not known yet (from the tech notes) and what a designer may want traced next.

1. **How floors 21-30 are entered**, and how floors 22 → 23 and 25 → 30 connect (no stairs). Candidates: the
   button panels (elevator) or an event after the ending (a second-clear flag exists). Not traced.
2. **Elevator:** the destinations of buttons A-E and which item each key-hole needs.
3. **Chutes:** how many floors they drop. **Pits, ceiling traps, rockfall:** damage amounts.
4. **Floors 7 and 20:** how the party goes back up (no up stairs).
5. **Floor 25** has four up stairs but floor 24 only three down stairs; where the fourth leads was not checked.
6. **Hidden spots:** the difficulty value of each spot, how long a spot stays used, and the exact chance rule (the
   tech note reads "4 × (skill − difficulty) % if that is < 5 points over, else 80 %", which jumps from 16 % to
   80 %; worth confirming).
7. **Random teleport curse:** whether the random square can be rock (instant party death), and which items set it.
8. **Damage zone protection:** what sets the protecting flag (inferred levitation or a ward). Whether the
   Levitate spell gives the same floating state as the sorcerer's levitation.
9. **The fourth wall value and the fourth zone value** (floors 5, 12, 28): no effect found.
10. **Event outcomes:** the odds of the well, the junk pile and the corpses; the gold-coins amount; what the maid
    offers; which sign text stands where; whether story events keep their own permanent "done" flag.
11. **Magic circles:** the tech notes name different creatures for the circles (Undead Beholder, Berserker ...
    Damned in the monster notes; Zombie, Ghoul ... Unspeakable as the summons learned). The table above uses the
    summon names; the creature shown in the circle may be the other one.
12. **Encounter areas:** the tech floor table and the generated encounter table disagree for floors 22-24 (extra
    areas 26, 27, 29 in the generated table).
13. **Chests:** the contents level cap of tiers above Bronze (used by the trap damage), what a chest of value 0
    gives (the list roll is from 0 to V − 1), and the trap inspect/disarm rules.

Tech: [dungeon.md §5](../tech/dungeon.md#5-not-found--open), [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried)
