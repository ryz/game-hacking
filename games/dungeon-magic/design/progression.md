# Dungeon Magic - progression and combat

## Overview
Experience points come from defeating monsters, but levels do not rise by themselves: the hero must visit his
wizard (the "wise man"), who trades experience for a level **(verified)** (`wise_man_level`, `level_up`). Fights
happen in real time on the map; the hero swings with A while the Fight icon is active **(verified)**
(`battle_monster`, `battle_win`).

## 1. Levels
- At level 0 with 412 EXP the wizard granted level 1, took 15 EXP (412 to 397) and raised maximum HP from 12 to
  15 **(verified)** (`level_up`). Without enough experience he answers "You are not wise enough! You need
  additional experience" **(source)** (ROM text next to the level-up lines).
- A new game starts at level 0 with 12 HP, no gold, no food or water **(verified)** (checkpoint `start`).

## 2. Combat
- Monsters roam dungeons, forests and the field and attack on their own; when one engages, the command switches
  to Fight automatically **(verified)** (`battle_monster`, `battle_skeleton`, floor 81 and 86 fights).
- The monster's HP is shown on the right scroll, the hero's on the left **(verified)**.
- A monster can hit from a square the hero is not facing: on floor 81 the hero lost 7 HP with no monster in view
  **(verified)** (capture route to `battle_monster`).
- A level-6 hero (no weapon bought) hit for 23 (29 to 6), then finished the monster; it vanished and gave 3 EXP, no
  gold **(verified)** (`battle_win`).
- The guardian on the arrival square of floor 92 has 182 HP, hits for about 62 and took no damage from a normal
  blow even when poked down to 1 HP **(verified)** (`boss_guardian`, checkpoint `boss92`); see
  [findings.md](findings.md).
- At 0 HP the game ends: "Your life is over" over the hero's sword planted in a hillside **(verified)**
  (`gameover`).

## Open questions
- Experience needed per level; HP gain per level beyond level 1.
- Weapon and armour effects on damage; monster stats.
