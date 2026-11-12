# Monsters and encounters

What a monster is, which monsters exist, when and how a fight starts, and how a monster chooses what to do each
round. The full stat list of all 167 monsters and every encounter table is in
**[monsters_table.md](monsters_table.md)** (generated from the game data). How the actual hits, damage, saves,
spells, escape and rewards are resolved is in [combat.md](combat.md).

Notation: see [README.md](README.md). Untagged numbers are **(data)**, read from the game's own tables. Numbers
marked "computed" were worked out here from the stated rule or table.

---

## Overview

- **167 monsters**, each one fixed record. Nothing about a monster is random except its HP, which is rolled per
  monster when the battle starts. There are no elite or scaled variants: a Goblin is always level 2 with AC 6.
- **Levels 1 to 30.** About half the bestiary is level 1-10 and only 5 monsters are above level 25 (computed from
  monsters_table.md).
- **A monster is a short list of numbers:** level, HP dice, AC, a to-hit base, swings per round and damage per
  swing, a reach (melee, reach or ranged), 8 elemental resistances, a type (undead, demon, dragon, spirit), up to six
  spell schools, special hits (poison, fear, sleep, paralysis, stone, decapitation, level drain), breath, how likely
  it is to call for help or flee, and its EXP, gold and chest quality.
- **Random fights are rare in corridors and common at doors.** After every action in the maze (a step or a turn) the
  game rolls for a fight. The normal chance is **1/512 per action (verified)**. Right after the party walks through
  a door it is **13/256, about 5.1 %, per action**, until the next plain step or turn-around. The same rates apply on
  every floor. See [findings.md](findings.md).
- **Guarded squares** are fixed fights (up to 21 per floor; none on floor 20). Each fights once per floor visit and
  comes back when you change floors. They are the only fights that give a chest.
- **A fight** is one of 4 formations listed for the square's encounter area, picked at random. A formation has up
  to 4 groups of 1-9 monsters each.
- **Monster AI** is a fixed priority list: a spellcaster casts 25 % of the time; otherwise the monster may call for
  help, flee, or breathe, and attacks if none of these fires.

---

## What a monster is

Every monster has the fields below. The column names are those of [monsters_table.md](monsters_table.md).

| Field (table column) | What it means in play |
|---|---|
| **Level** (Lv) | Used against the party's save rolls for the monster's special hits, against the party's weapon status effects, against Hide, and in some spell checks ([combat.md](combat.md)). 1 to 30. |
| **HP** | A dice roll made for each monster when the battle starts: `minimum + the sum of N rolls of 0..(S−1)`. The table shows the range, e.g. Goblin 1-7. Every monster has a minimum of at least 1. |
| **AC** | Armour class, lower is better. From 10 (Mudman) down to −30 (Abyss Lurker) (computed from monsters_table.md). The party's to-hit roll is made against it. |
| **To-hit base** (Hit) | How hard it is for this monster to hit; **lower is more accurate**. From 1 (Ancient One and other top monsters) to 19 (Goblin, Orc). Works like a THAC0: see [combat.md](combat.md#monster-attacks-to-hit-and-damage). |
| **Swings per round** (Att) | How many attacks the monster makes when it attacks. Most monsters have 1-3; the data goes up to 14 (Musashi). See Open questions. |
| **Damage per swing** (Dmg) | Same dice form as HP: `minimum + N rolls of 0..(S−1)`, rolled per hit. |
| **Reach** | 0 melee, 1 reach, 2 or 3 ranged: decides which party members it can attack and from which rank ([combat.md](combat.md#monster-reach-and-targets)). |
| **Resistances** (Resist %) | 8 values, one per element, in the museum's order: Earth, Water, Fire, Wind, Spirit, a 6th element whose name was not read, Holy, None. Shown as a resistance %: 0 = no resistance, 100 = immune. Spells subtract it from their power ([combat.md](combat.md#spells-against-monsters)); Earth and Spirit at 100 % also block the party's weapon status effects. |
| **Type** | Undead, demon, dragon, spirit (used by slaying weapons, [combat.md](combat.md#slaying-weapons)). Two more type flags exist, one on golem-like monsters and one on ghost-like monsters; their effect was not traced. |
| **Spell schools** (Spells) | Up to 6 schools, each with the highest spell level (1-7) the monster can cast. School 0 is Mage, school 1 is Priest. A spellcaster gets 9 casts at each spell level for the battle. |
| **Special hits** (Specials) | Poison, fear, sleep, paralysis, stone, decapitation, each tried after a successful hit; level drain (how many levels per hit). The target gets a save ([combat.md](combat.md#special-hits-and-saving-throws)). |
| **Breath** | Whether it can breathe, and the element: fire, frost, poison, lightning, acid or stone. |
| **Call for help** | Whether it can call for help, and how strongly: 25 % or 65 % per turn (see Monster AI). |
| **Flee value** F | 0 = never flees. Otherwise the monster flees with F × 5 % per turn (10 % for F = 2, the value of 19 of the 26 monsters that flee; computed from monsters_table.md). |
| **Escape block** (Esc) | Subtracted from the party's chance to run away; the highest value among the groups counts. 2 to 18 (computed from monsters_table.md). See [combat.md](combat.md#escape). |
| **EXP, Gold** | Paid per monster killed: EXP 30 (Crawling Claw) to 150,000 (Abyss Lurker), gold 20 to 250. |
| **Chest row** (Chest) | The chest quality a guarded-square victory rolls from; the highest row among the groups counts ([dungeon.md](dungeon.md#chests)). |
| **Unidentified name** | While a group is unidentified the battle shows one of 16 generic names instead of the real one. |
| **Attack verb** | Which set of attack words the battle text uses. No game effect. |

Example (data): the Goblin row of [monsters_table.md](monsters_table.md).

| id | EN | JP | Lv | HP | AC | Hit | Att | Dmg | Reach | Esc | Type | Spells | Specials | Resist % | EXP | Gold | Chest | Floors | G | Enc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 52 | Goblin | ゴブリン | 2 | 1-7 | 6 | 19 | 1 | 1-7 | 0 | 10 | - | - | call 25%, flee 10% | - | 290 | 30 | 1 | 1-2,5 | 1-2,5 | 3-4,7,54,56 |

Read: a level-2 melee monster with 1-7 HP and AC 6 and the least accurate to-hit base (19), one swing of 1-7 damage,
calls for help 25 % of its turns and flees 10 %, worth 290 EXP and 30 gold, found on floors 1-2 and 5.

**Notes:** a battle flag can switch off a monster's special hits; what sets it was not traced. The "Spells" column
names schools 2-5 only by number (see Open questions).

Tech: [monsters.md §1](../tech/monsters.md#1-the-monster-record-bank-57-4820--64--id)

---

## The bestiary

The 167 monsters span levels 1 to 30. Counts below are computed from [monsters_table.md](monsters_table.md).

| Levels | 1-5 | 6-10 | 11-15 | 16-20 | 21-25 | 26-30 |
|---|---|---|---|---|---|---|
| Monsters | 34 | 43 | 41 | 26 | 18 | 5 |

**Families by type flag** (computed):

| Type | Count | Members |
|---|---|---|
| Undead | 26 | skeletons, zombies, ghouls, mummies, vampires, Lich, Dullahan, ghosts (Banshee, Ghost, Gas Cloud, Specter)... |
| Demon | 10 | Lesser Demon up to Demon King, Demon Queen and the final boss Demon Adish |
| Dragon | 3 | ShadowDragon, Deep Dragon, Mist Dragon (level 21-22, floors 18-19) |
| Spirit | 11 | the elementals, Djinni, Dao, Marid, Ifrit, Dryad, Treant, Rakshasa |
| Golem-like flag (effect not traced) | 7 | the golems, Gargoyle, Juggernaut, Kugutsu |
| Ghost-like flag (effect not traced) | 13 | the four ghosts, Air and Fire Elementals, Djinni, Phoenix, both Beholders, Couatl, Eye Wing, Gargoyle |
| No type | 106 | humans and humanoids, beasts, giants, the "ancient" monsters |

A monster can carry more than one flag (a Ghost is undead and ghost-like).

**What monsters do besides hitting** (computed): 68 cast spells, 20 breathe, 31 call for help (only the Creeping
Coin at 65 %), 26 can flee. Special hits: paralysis 14, level drain 15, poison 11, fear 11, decapitation 9,
stone 8, sleep 3. Reach: 102 melee, 45 reach, 20 ranged.

**Notable monsters:**

| id | EN | JP | Lv | HP | AC | Hit | Att | Dmg | Reach | Esc | Type | Spells | Specials | Resist % | EXP | Gold | Chest | Floors | G | Enc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 130 | CrawlingClaw | クラウリングクロウ | 1 | 1-6 | 8 | 19 | 1 | 1-4 | 0 | 10 | - | - | - | 0/0/0/0/100/0/0/0 | 30 | 20 | 1 | 1,6 | 1,6 | 1,8,56,58 |
| 115 | CreepingCoin | クリーピングコイン | 1 | 1-1 | 7 | 19 | 1 | 1-2 | 0 | 14 | U | - | breath(lightning), call 65% | 95/100/95/95/100/95/80/95 | 260 | 20 | 1 | 1 | 1 | 2,34 |
| 8 | Bowman | ボウマン | 5 | 5-30 | 7 | 15 | 2 | 3-27 | 2 | 12 | - | - | call 25%, flee 10% | - | 550 | 60 | 6 | 7,12 | 7,12 | 9,14,59-60,67 |
| 24 | Vampire | ヴァンパイア | 10 | 15-85 | 1 | 12 | 1 | 6-18 | 0 | 15 | U | - | paralyze, drain 1 | 20/60/20/60/100/50/5/20 | 1000 | 80 | 12 | 10,29 | 9-10,27,29 | 12,31,63,66,92-93,97 |
| 152 | Musashi | ムサシ | 20 | 36-288 | -10 | 2 | 14 | 16-30 | 0 | 12 | - | s4:L7 | - | - | 44050 | 180 | 42 | 26,28-30 | 26,28-30 | 28,30,32-33,87,90,93-100 |
| 7 | Abyss Lurker | しんえんよりのもの | 30 | 255-2295 | -30 | 1 | 2 | 34-226 | 3 | 18 | - | s0:L7 s1:L7 | fear, sleep, paralyze | 100/100/100/100/100/100/100/100 | 150000 | 250 | 43 |  |  | 49 |

- **Crawling Claw** is the weakest monster (30 EXP). **Creeping Coin** has a single HP but breathes lightning,
  calls for help 65 % of its turns, resists most elements, and has its own event fight (area 34).
- **Bowman, Shooter, Gunner, Sagittarius** (ids 8-11) are the archer line: ranged, so they hit any party member from
  any rank.
- **Vampire** is the first level drainer met on the main route (floors 9-10, also 27 and 29).
- **Musashi, Kamui, Kali, Scylla, Carrion Worm** have the most swings (8 to 14 per attack round).
- **Abyss Lurker** is the strongest: level 30, up to 2295 HP, AC −30, 100 % resistance in every element, so no spell
  that checks resistance affects it ([combat.md](combat.md#spells-against-monsters)).
- **Event-only monsters** (no floor in the table, they appear only in event fights): Ancient One, Fair Fiend,
  Godslayer, Rift Walker, Abyss Lurker, Demon King, Demon Queen, Demon Adish, Kamui, Alien.
- **The second area** (floors 21-30) is where most level 20-30 monsters live: the "ancient" ones (From Beyond,
  Unspeakable, Star Seizer), the high demons and vampires, and the special-class fighters (Valiant, Avenger,
  Musashi, Kunoichi).

**Notes:** the type flags are what slaying weapons check ([combat.md](combat.md#slaying-weapons)). Some monster names
repeat a spell name (Ifrit, Lion of Hell, Ancient One...): those are the same creatures the Summoner's pacts call
([spells.md](spells.md#6-summoner-pacts)).

Tech: [monsters.md overview](../tech/monsters.md#overview-two-minute-read), [monsters.md §1](../tech/monsters.md#1-the-monster-record-bank-57-4820--64--id)

---

## When a fight starts

The player sees fights mostly on stepping through a door; a long corridor walk rarely triggers one.

After **every action** in the maze (a step, a left or right turn, a turn-around) the game rolls for a random fight:

| Situation | Chance per action | Average actions until a fight (computed: 1 / chance) |
|---|---|---|
| Normal | 1/512, about 0.2 % (verified) | 512 |
| Right after walking through a door | 13/256, about 5.1 % | about 20 |

- The "after a door" state starts with the door step and lasts until the next **plain step** or **turn-around**.
  Left and right turns do not end it, so turning in place after a door keeps rolling at 5.1 %.
- There is no step counter and no depth modifier: the rate is the same on floor 1 and floor 30.
- A fight only happens on a square that has an **encounter area**. Squares with no area (rock, and some corridors on
  floors 2, 9, 13, 17, 19, 21, 22 and 25) never have random fights.

The 1/512 rate was checked in the emulator (a 357-action walk gave one fight, which fits 1/512; a small sample). The
door rate comes from the game's code and was not measured separately.

**Notes:** the corridor rate is very low and doors raise it 26-fold (computed: 13/256 against 1/512); whether
that is intended is discussed in [findings.md](findings.md). Doors, squares and damage zones are described in
[dungeon.md](dungeon.md#damage-zones-and-anti-magic-zones).

Tech: [monsters.md §2.1](../tech/monsters.md#21-when-a-fight-starts-code-204422-4460-emu)

---

## Fixed fights: guarded squares and events

Besides random fights there are two kinds of fixed fight.

- **Guarded squares**: fixed spots, from none (floor 20) to 21 (floor 4) per floor. Stepping on one always starts a
  fight from that square's encounter area. Each guard fights **once per floor visit**: all guards come back whenever the party changes floors.
  A guarded-square victory is **the only way to get a chest**; random fights give gold only.
- **Event fights**: story events (bosses, named monsters) start a fight from areas 34-53, each with one fixed
  formation. Areas 48 and 49 play the boss music.

Example (generated table): event area 49, the Abyss Lurker fight.

| enc id | random on floors | guarded squares on floors | formation (one of 4 picked at random; monster ×size) |
|---|---|---|---|
| 49 |  |  | F133: Mist Dragon ×2 + ShadowDragon ×1-2 + Deep Dragon ×0-2 + Abyss Lurker ×1 |

**Notes:** on most floors guards use the same areas as random fights, so a guarded square is a guaranteed,
re-arming fight with the floor's normal monsters plus a chest. The chest itself (value, items, traps) is in
[dungeon.md](dungeon.md#chests).

Tech: [monsters.md §2.2](../tech/monsters.md#22-fixed-fights), [dungeon.md §4](../tech/dungeon.md#4-floors)

---

## Encounter areas and group formation

Every map square carries an **encounter area** number, and each area lists **4 formations**. The fight uses one of
the 4, each with chance 1/4; an area that lists the same formation twice makes it twice as likely.

| Area numbers | Used for |
|---|---|
| 1-33 | random fights and guarded squares of floors 1-30 (floor 1 has three zones: areas 1, 2, 3; floor 2 is area 4; floor 3 is area 5 with area 6 on two guarded squares; ... floor 30 uses 32 and 33) |
| 34-53 | event fights, one fixed formation each; the guarded squares of floor 13 use area 50 and some of floor 18 use area 51 |
| 101-105 | the damage-zone squares of floors 8, 11, 25, 27 and 30, which have their own monster mix |
| 54-100 | on no map and used by no event (see Notes) |

**Formation.** A formation has up to 4 **groups**, each a monster and a size rule. The size is
`H + a random number from 0 to L−1` (exactly H when L is 0), at most 9. Group 1 always has at least one monster;
groups 2-4 that roll 0 are dropped. So a fight has 1 to 4 groups of 1 to 9 monsters. Groups 1-2 fight from the front
ranks and groups 3-4 from the back ([combat.md](combat.md#monster-reach-and-targets)).

Examples from [monsters_table.md](monsters_table.md):

| enc id | random on floors | guarded squares on floors | formation (one of 4 picked at random; monster ×size) |
|---|---|---|---|
| 1 | 1 | 1 | F0: CrawlingClaw ×1-4 / F1: Eye Wing ×1-4 / F2: Gas Cloud ×1-4 / F3: Banshee ×1 |
| 7 | 5 | 5 | F24: Dryad ×3-4 + Treant ×2-4 / F25: Ogre ×3-4 + Ogre Lord ×2-4 / F26: Skeleton ×4 + Wight ×3 + Zombie ×1-4 + Ghoul ×0-3 / F27: Goblin ×5-7 + Goblin King ×0-4 + Dark Elf ×3-4 |
| 33 | 29-30 | 29-30 | F128: Avenger ×3 + Valiant ×4 + Kunoichi ×3 + Musashi ×1 / F129: Treant ×8 + Rakshasa ×6 + Phoenix ×4 + From Beyond ×1 / F130: Demon Lord ×2 + Succubus Qn. ×3 + Arch Demon ×2 + Hell Master ×3 / F131: Beholder ×4 + Nightcrawler ×4 + Night Rider ×4 + Unspeakable ×1 |

Floor 1 starts with single groups of 1-4 weak monsters; by floor 5 fights have 2-4 groups; two of the four
formations of the last floors put a level 27-29 "ancient" monster behind three large groups.

**Notes:** areas 54-100 are overlapping slices of the formation list that no map or event uses; they may be a cut
"random depth" table **(inferred)**, see [findings.md](findings.md). There are 150 formations.

Tech: [monsters.md §2.3](../tech/monsters.md#23-group-formation-code-2240c7-41b5-data-397a27-397573)

---

## Monster AI: how a monster picks its action

Each round every monster picks one action by walking a fixed priority list; the first check that succeeds decides.
The checks use only the monster's own data and status.

| Order | Condition | Action |
|---|---|---|
| 0 | the monster is Afraid | flee with chance (F + 5) / 20 if its flee value F is not 0; otherwise do nothing |
| 0 | the monster is Asleep or worse | do nothing |
| 1 | it has spells, 25 % | cast a spell |
| 2 | it can call for help, 25 % (strong callers 65 %) | call for help |
| 3 | flee value F is not 0, F × 5 % | flee (only monsters on the enemy side) |
| 4 | it can breathe, 1/8 (12.5 %) | breathe on the party |
| 5 | otherwise | attack (its swings against a target its reach allows) |

```csharp
MonsterAction ChooseAction(Monster m)
{
    if (m.Status == Status.Afraid)
        return (m.Flee > 0 && Random(0, 19) < m.Flee + 5) ? Flee : Nothing;
    if (m.Status >= Status.Asleep) return Nothing;
    if (m.HasSpells && Chance(25)) return CastSpell(PickSpell(m));
    if (m.CanCallForHelp && Random(0, 19) < (m.StrongCaller ? 13 : 5)) return CallForHelp;
    if (m.Flee > 0 && m.IsEnemy && Random(0, 19) < m.Flee) return Flee;
    if (m.CanBreathe && Chance(1, 8)) return Breath;
    return Attack;   // target chosen by reach, see combat.md
}
```

**The percentages are per step, not overall**: each check only runs if the ones above it failed. For a Goblin (calls
25 %, flee value 2): calls for help 25 %, flees 75 % × 10 % = 7.5 %, attacks the remaining 67.5 % (computed).

**Spell choice.** The monster picks one of its schools at random, then one spell uniformly from **all** spells of
that school up to its top level, so a top-level-7 Mage monster casts a level-1 spell as often as any other single
spell. If the picked spell cannot be cast in battle, the monster does nothing that turn.

**Fleeing** removes the monster from the fight; fled monsters give no EXP or gold ([combat.md](combat.md#rewards)).
An Afraid monster is more likely to flee than a calm one ((F + 5) / 20 against F / 20), and a monster with flee
value 0 that is Afraid just stands there.

**Notes:** what "call for help" does (how many monsters arrive, into which group) was not traced. Breath damage was
not traced either ([combat.md](combat.md#breath)).

Tech: [monsters.md §3](../tech/monsters.md#3-monster-turn-ai-code-2261b2-6315)

---

## Open questions

- **Swings per round.** The tech notes give 1-7 swings, but the generated table has five monsters above 7 (Kali 8,
  Scylla 8, Carrion Worm 8, Kamui 10, Musashi 14). Which is right needs a check of the field or an emulator fight.
- **Spell schools 2-5** are not named in the tech notes. Their numbering matches the special-class schools (2
  Valiant, 3 Avenger, 4 Musashi, 5 Kunoichi), and the monsters Valiant, Avenger, Musashi and Kunoichi carry schools
  2, 3, 4 and 5 respectively, so this is likely **(inferred)** but not confirmed.
- **Two type flags** (golem-like, ghost-like) and one more record field have no known effect. The 6th element's name
  was not read.
- **Call for help**: what it adds to the battle.
- **Target choice**: which party member a monster attacks among those its reach allows was not traced.
- **Areas 104 and 105** (damage zones of floors 27 and 30): the generated table shows them pointing at formations
  150 and 151, past the 150-formation list, marked "(none)". What a fight there produces was not checked.
- **Identification**: how the game decides at battle start whether a group shows its real name was not traced.
- **Surprise and initiative**: see [combat.md](combat.md#round-structure-and-initiative).
- **Encounter areas 54-100**: no user found.

Tech: [monsters.md §9](../tech/monsters.md#9-not-found--open)
