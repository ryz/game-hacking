# Characters and stats

## Overview
The player creates three characters in the opening dream: the hero, the Law hero and the Chaos hero. Each
starts with 5 in all six stats and receives 18 points to place freely **(verified: `@dream` onward)**. The hero
has no MP at all and the command menu answers "Nobody can use magic." while he is alone; the two companions
have MP **(verified)**. Characters carry a sword and a gun at the same time, with separate ammunition
**(verified: equipment slots on the status screen)**.

## 1. Creation
1. Name: up to 8 characters from upper- and lower-case letters, digits and a few symbols; an empty name is not
   accepted **(verified)**.
2. Stats: STR, INT, MAG, VIT, SPD, LUK start at 5; 18 points to divide; points can be taken back until the
   last one is placed, then a Yes/No confirmation appears **(verified)**.
3. The heroine is not created in the dream; a blank character with 5 in every stat is kept ready for her
   **(RAM)**.

## 2. What the stats do (as far as seen)
| Placed points | Effect seen on the creation screen | Tag |
|---|---|---|
| VIT | hero: 18 HP at VIT 5, 22 HP at VIT 10; Law hero: 18 HP at VIT 5, 20 HP at VIT 7; Chaos hero 22 HP at VIT 9 | **(verified)** |
| VIT | Defense 5 at VIT 5, 10 at VIT 10 (hero) | **(verified)** |
| SPD (with LUK) | Evade 7 at the start, 12 for the hero with SPD 9 and LUK 8 | **(verified)**; the split between the two stats is not known |
| MAG, INT | Law hero: MP 9 at the start, 14 with INT 10 and MAG 11; M.Power and M.Effect rise from 6 to 12 and 11 | **(verified)**; which stat feeds which value is not separated yet |
| STR | no change while no weapon is equipped (Power stays 0) | **(verified)** |

Level 1 needs 10 EXP for the next level; a level-23 hero is shown "Next 23000" **(RAM: level changed through
memory, see the playbook)**.

## 3. Status screen
LVL, HP, MP, EXP, Next, Stat (condition); equipment: Swd, Gun, Ammo, Head, Body, Arm, Leg; Power and Accur for
sword and gun, Defense, Evade, M.Power, M.Effect; six stat bars **(verified: `@apartment`, command menu, STATUS)**.

Equipping the Attack Knife on the level-1 hero (STR 11, SPD 9, LUK 8) changed sword Power from 0 to 17 and
sword Accur from 0 to 15; Defense 10, Evade 12, M.Power 6 and M.Effect 6 stayed as they were **(verified:
`../shots/main/status_hero.png` before, `../shots/main/equipment.png` after)**. The equipment slot shows the
name cut to eight letters ("Attack K").

## Open questions
- Exact formulas for HP, MP and the derived values (only single data points so far).
- Stat points per level-up and the stat cap (the bars have room for about 40).
- Whether the derived values are recalculated only at level-up or equipment changes (a stat changed through
  memory left them unchanged).
