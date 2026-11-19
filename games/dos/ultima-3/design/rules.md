# Ultima III: Exodus (DOS) - rules in detail

The numbers behind the systems in [systems.md](systems.md): combat, magic, classes, shops, chests and traps,
dungeons, travel and the quest. Read from the program and checked in play during the 2026-11-19 capture.
Notation: [README.md](README.md). Shots are named by id (`id`); the file names are in `../shots/main/index.md`.

## Overview
Most of the game's chances use one random number (0-254). Monsters hit unless the target wears Exotic armour,
and their damage grows with the target's own maximum hit points, so fights stay dangerous at every level
**(code)**. Spells cost 5 magic points per letter of the alphabet (A free, P 75) **(code; verified for B, C,
N, O)**. A class decides which spell list a character casts from and which weapons and armour it may use
**(code; verified for the Wizard and the Fighter)**. Shops are chosen by the row of the counter **(code,
verified)**; a chest is trapped half the time **(code, verified)**; fountains, rods, gremlins and winds sit on
fixed squares of each dungeon level **(dungeon files, verified)**.

## 1. Combat
### 1.1 Fields
A fight moves to an 11x11 field chosen by where it starts **(code; verified for every row)**:
| Situation | Field | Shot |
|---|---|---|
| on grass (and most other land) | G: grass with tree borders | `battle_start`, `battle_giants` |
| on brush | B: brush | `battle_cutpurses`, `battle_daemons` |
| in a forest | F: trees | `battle_zombies` |
| in a dungeon, towne or castle | C: stone floor | `battle_dungeon_goblins`, `battle_lord_british` |
| a sea monster attacks the party on land | M: shore and sea | `battle_manowars` |
| pirates attack the party on land | A: their ship beside the shore | `battle_pirates_shore` |
| the party in a frigate, a sea monster | Q: the frigate's deck among waves | `battle_serpents` |
| the party in a frigate, a land monster | R: the deck below a coast | `battle_wyverns_ship` |
| the party in a frigate, pirates | S: two decks | `battle_pirates_board` |

### 1.2 Turns
Each living character acts in order ("----Player 1----"): move one square, Attack in a direction, Cast,
or pass; then every monster moves toward the party or strikes a neighbour **(verified)**. Ready is not a
combat command ("Not usable cmd!") **(verified)**: weapons are readied on the map. A ranged weapon (a bow)
hits the first monster in the chosen direction ("Bow Attack Dir-North Goblin Hit!", `battle_bow`)
**(verified)**. A monster killed gives experience at once ("Killed! Exp.+03" for an orc, +05 for a pirate, +10
for a pincher) **(verified)**; the last one gives "****Victory!****" and a chest where the monsters stood
**(verified: `battle_victory`, `system_chest_after_fight`)**.

### 1.3 Monster attacks
- **Hit or miss:** outside Castle Exodus a monster always hits a character in ordinary armour; against Exotic
  armour, and against everyone in the castle's fights, it hits when a random number from 0 to
  armour + 15 is below 8 (armour 0 skin ... 7 Exotic), i.e. 50% against skin, 35% against Exotic **(code)**.
  The late party (Exotic armour) was missed about half the time **(verified: `battle_thieves_pilfer` frames)**.
- **Damage:** 1 + a random number below (base + H) where H is the first two digits of the target's maximum
  hit points (2300 -> 23, read as the stored packed number, 35) and base is per monster: merchant and jester 4,
  orc 6, skeleton 10, cleric 12, thief 16, daemon and wizard 20, fighter and pincher 24, dragon and serpent 28,
  balron, guard, man-o-war, pirate and Lord British 30; fights that start in a dungeon, towne or castle add 16,
  32 or 48 **(code)**. An orc hit ryz (2300 maximum) for 29 **(verified, `battle_orc_hits`)**.
- **Specials:** pinchers, balrons and man-o-wars poison on a hit one time in four ("Plr 2 Poisoned!",
  `battle_snatches_poison`) **(code, verified for pinchers)**; thieves pilfer an unreadied weapon or armour
  ("Plr 1 Pilfered!", `battle_thieves_pilfer`) **(code, verified)**; pirate ships fire cannons at a frigate on
  the map (`battle_pirates_fire`) **(verified)**.
- **Death:** at 0 hit points "Killed!!!", status D, the body leaves the field (`battle_member_killed`); when
  no one can act, "All Players Out!" and the game stops (`gameover_all_out`) **(verified)**.

### 1.4 Names
The same picture can carry a second name: thieves fought as "Cutpurses", skeletons as "Zombies", dragons as
"Wyverns", pinchers as "Snatches", balrons as "Devils", orcs in a dungeon as "Goblins" **(verified)**; the
program holds 16 such names (Brigand, Cutpurse, Goblin, Troll, Ghoul, Zombie, Golem, Titan, Gargoyle, Mane,
Snatch, Bradle, Griffon, Wyvern, Orcus, Devil) **(ROM text)**. Which name a fight uses was not read **(open)**.

## 2. Magic
Cost = 5 x (letter - A) magic points: A costs nothing, P costs 75; the cost is taken before the effect, and
"M.P. too low!" refuses the cast (`system_cast_mp_low`) **(code, verified)**. Magic points come back by one or
two each turn **(verified on the panels)**. Who casts what **(code; verified for Paladin, Cleric, Wizard,
Fighter)**: Cleric, Paladin, Illusionist the cleric list; Wizard, Lark, Alchemist the wizard list; Druid and
Ranger choose ("Spell type W/C-"); Fighter, Thief, Barbarian "Not a mage!" (`system_cast_not_mage`).

| Letter | Wizard spell | Effect **(code)** | Cleric spell | Effect **(code)** |
|---|---|---|---|---|
| A (0) | Repond | combat: kills the orcs, one try per fight, half the time (`battle_spell_repond`) | Pontori | combat: kills the skeletons, same rule ("Failed!" on orcs, `battle_pontori_failed`) |
| B (5) | Mittar | combat: a bolt in one direction, up to 40 damage (`battle_spell_mittar`, `battle_spell_hit`) | Appar Unem | opens a chest without its trap three times in four |
| C (10) | Lorum | light for 10 dungeon moves (`system_spell_lorum`) | Sanctu | heals 10-29 hit points (`system_spell_sanctu`: 2213 -> 2233) |
| D (15) | Dor Acron | dungeon: one level down (`system_spell_dor_acron`) | Luminae | as Lorum |
| E (20) | Sur Acron | dungeon: one level up, out of level 1 to Sosaria (`system_spell_sur_acron`) | Rec Su | as Sur Acron |
| F (25) | Fulgar | combat: 75 damage to one monster | Rec Du | as Dor Acron |
| G (30) | Dag Acron | Sosaria: the party appears on a random open square (`system_spell_dag_acron`) | Lib Rec | dungeon: redraws the level (effect not settled) |
| H (35) | Mentar | combat: damage twice the caster's Intelligence | Alcort | cures poison (`system_spell_alcort`); cancelling refunds the points |
| I (40) | Dag Lorum | light for 250 moves | Sequitu | dungeon: straight out to Sosaria |
| J (45) | Fal Divi | casts any cleric spell (`system_spell_fal_divi`) | Sominae | as Dag Lorum |
| K (50) | Noxum | combat: 75 damage to every monster | Sanctu Mani | heals 20-99 hit points |
| L (55) | Decorp | combat: 255 damage to one monster | Vieda | out of combat: a view of the land or level (`system_spell_vieda`) |
| M (60) | Altair | stops time for 10 turns (as a powder) | Excuun | as Decorp |
| N (65) | Dag Mentar | combat: twice Intelligence to every monster | Surmandum | raises the dead three times in four, else ashes (`system_spell_surmandum`) |
| O (70) | Necorp | combat: every monster left with 5 hit points | Zxkuqyb | combat: 255 damage to every monster (`battle_spell_zxkuqyb`) |
| P (75) | (no name) | combat: 255 damage to every monster | Anju Sermani | raises ashes; the caster loses 5 Wisdom |

## 3. Classes, weapons and armour
Ready and Wear refuse with "Not allowed!" past the class's limit **(code, verified: `system_ready_refused`,
`system_wear_refused`)**:
| Class | Weapons (up to) | Armour (up to) | Spells |
|---|---|---|---|
| Fighter | all, Exotic too | all, Exotic too | none |
| Cleric | Mace | Chain | cleric |
| Wizard | Dagger | Cloth | wizard |
| Thief | Sword | Leather | none |
| Paladin | all | Plate | cleric |
| Barbarian | all | Leather | none |
| Lark | all | Cloth | wizard |
| Illusionist | Mace | Leather | cleric |
| Druid | Mace | Cloth | both |
| Alchemist | Dagger | Cloth | wizard |
| Ranger | +2 Sword | +2 Plate | both |
(code: one letter per class in the program's table; inferred that the letter is the first item refused)

## 4. Shops and townsfolk
- **Pub:** a drink costs 7; paying less: "Leave my shop! You scum!!"; paying more than the purse: "What? Can't
  pay! Out you scum!"; the tens digit of the payment picks the tip: 0x "Thank you, kindly!", 1x Ambrosia, 2x
  Dawn, 3x the conjunction of the moons, 4x nasty dark, 5x the pool, 6x the shrines, 7x fountains, 8x "EXODUS:
  Ultima III which is next?", 9x the Lord of Time **(code; verified 05, 08, 10, 35, 90)**.
- **Grocer:** 1 gold per ration, food capped at 9999 ("Too much to carry!") **(code; verified 50 rations)**.
- **Healer:** curing 100, healing 200 (to full: 2213 -> 2300), resurrection 500, recalling 900 gold; "Not
  injured!", "Not dead!", "Not ashes!" when there is nothing to do **(verified for the first three)**.
- **Weapons and armour:** a list in pages, then Buy or Sell by letter; LCB and Montor stock up to the 2H
  sword and plate, Dawn the magic arms (+2 and +4) **(verified)**.
- **Guild:** keys 50, torches 6, powders 90, gems 75, "How many?" **(verified)**.
- **Oracle (Radrion):** an offering of N hundred gold recites verse N of his rhyme (0 the opening lines) **(code;
  verified 1, 2, 6)**.
- **Stables:** "4 horses cost 800gp" (200 per member) **(verified)**.
- **Bribe:** 100 gold sends a guard away (`system_bribe`, gold 4352 -> 4252) **(code, RAM)**; anyone else: "No
  effect!".
- **Steal:** across a counter, from the chest behind it (only Grey has one): a roll below Dexterity (+64 for
  Barbarian, Illusionist, Ranger, +128 for a Thief) succeeds; a failure is "Failed!" three times in four, else
  "Watch out!" and every guard of the towne turns hostile **(code, verified all three)**.

## 5. Chests and traps
Half of all chests are trapped **(code)**: acid (the searcher loses up to 55), poison (the searcher), gas
(poisons everyone), bomb (everyone hurt) **(code, verified all four)**. The searcher evades with the same roll as
stealing ("Trap evaded!") **(code, verified)**. Every chest holds 30-99 gold, and one in four also a weapon
(Dagger to 2-H-Swd) or an armour (Cloth to Chain) **(code, verified)**. Shots `system_chest_*`, `system_trap_*`.

## 6. Dungeons
- 8 levels of 16x16 per dungeon, dark without a torch or Lorum; ladders up and down; Klimb on level 1's
  entrance leaves ("Exit to Sosaria!") **(verified)**.
- **Fountains** by the square's column (x mod 4): 0 poison ("Yuck! Horrible!"), 1 heal ("How wonderful!",
  2213 -> 2300), 2 hurt ("Argh! Blah! Yuk!", -25), 3 cure ("Ah! That's nice!") **(verified)**.
- **Strange wind** puts the torch out; **gremlins** eat 100 rations of one member; **traps** ("Argh!! A
  trap!!", evaded by the Dexterity roll); **misty writing** shows the level's message **(verified)**.
- **Rods** brand the toucher with a mark (by x mod 4: Force, Fire, Snake, Kings) for 50 hit points **(verified
  `system_rod_mark`)**.
- **Fights** start at random while walking ("Conflict!! ->Goblins" after a few steps) and leave a chest in the
  corridor **(verified)**.

## 7. Travel
- **Wind** changes every 25 turns: calm one time in nine, otherwise north, east, south or west **(code)**. A
  frigate cannot sail toward the side the wind is named after (east into an East Wind: "Invalid Move!",
  `system_wind`) and cannot move at all in a calm **(code; verified for the first)**.
- **Pirate ships** can be fired on ("Pirates Destroyed!", `battle_cannons`) or attacked; beating the crew on
  the two decks leaves their ship as an empty frigate (`system_frigate_taken`) **(verified)**.
- **Whirlpools:** the one on Sosaria drowns the frigate and washes the party onto Ambrosia; Ambrosia's own
  whirlpool takes the party back to Sosaria in a frigate ("All is Dark! You made it!",
  `cutscene_ambrosia_return`) **(verified)**.

## 8. The quest
Lord British: +100 maximum hit points per visit when the experience hundreds reach the maximum's hundreds;
"Seek ye, the Mark of Kings!" from 500 without that mark; "No more!" at 2500 **(code, verified all four
answers)**. Exotics are dug on two islets; EVOCARE needs the Mark of Snake; the cards go in Love, Sol, Moons,
Death; **a wrong card kills the inserter** (`system_insert_wrong`) **(code, verified)**.

## Open questions
- The party's hit chance and damage (weapon, Strength, Dexterity) were not read.
- Which of the two monster names a fight uses; Lib Rec's exact effect; the sale prices of arms.
- Starvation and the damage of poison per turn were not measured.
