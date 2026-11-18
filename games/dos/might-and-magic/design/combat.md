# Combat and encounters

Shots are in `../shots/main/`; a shot id `x` in category `c` is the file `might-and-magic_dos_na_c_x.png`.

## Overview
Fights start on fixed squares and at random while walking. The party either gets an encounter screen with four
choices or is thrown straight into combat. Combat is a text screen played in rounds; every character and monster
acts once per round in speed order, and each character is asked for an order when its turn comes
**(verified: `encounter_poltergeists`, `combat_round`, `combat_options`)**.

## 1. The encounter screen
The monster's picture, the list of monsters (letters A onward, up to at least 14 seen in one group) and the
options Attack, Bribe, Retreat, Surrender **(verified: `encounter_poltergeists`, `cave_snakes`,
`dusk_vampires`)**.
- Attack starts round 1 **(verified: `combat_round`)**.
- Bribe against four Poltergeists: "NO RESPONSE", and combat starts **(verified: `encounter_bribe`)**.
- Surrender against the same group: "THE MONSTERS DON'T TAKE PRISONERS!", and combat starts **(verified:
  `encounter_surrender`)**.
- Retreat from the room at Sorpigal (3,6) put the party in front of the inn door without a fight **(verified:
  route `@combat,r`)**.
- Which monsters appear on a fight square depends on the moment the party steps in: the same forest square
  gave six Snakes with one wait and nine Strangling Vines with another; the room in Sorpigal gave Poltergeists
  or Vampire Bats **(verified: `outdoors_vines`, playbook)**. Some squares hold a fixed group: the wizard Okrim
  with three Wizards and a Brontasaurus in the Quivering Forest **(verified: `qvl_okrim`; fixed is inferred from
  the named leader)**.

## 2. The combat screen
Round number; the party as a 2 by 3 formation where `+` marks who can fight hand to hand (two at the start, more
after monsters "infiltrate the ranks"); the monster list, where `+` marks the monsters in reach and "(WOUNDED)"
appears after a hit; a handicap line ("MONSTER +2", "PARTY +3", "EVEN") that changed from round to round
**(verified: `combat_round`, `combat_spell_hit`, `death_party_down`)**. What the handicap changes is not
measured.

Orders, as offered **(verified: `combat_options`, `combat_cast`, `combat_shoot`)**:
| Key | Order | Offered to |
|---|---|---|
| A | Attack the first monster in reach | characters marked `+` |
| F | Fight: choose the monster | characters marked `+` |
| S | Shoot | characters with a missile weapon (the Archer and the Robber with their Slings) |
| C | Cast: spell level, spell number, then the target letter | Cleric, Sorcerer |
| E, R, U, B | Exchange places, Retreat, Use an item, Block | everyone |
Ctrl-A is a quick order: attack, shoot or block, whichever applies **(verified)**.

## 3. Numbers seen (level 1 party against four Poltergeists)
- Poltergeists attack twice per turn and did 1 to 4 points per attack turn **(verified: `combat_round`,
  `death_party_down`)**.
- Flame Arrow (Sorcerer level 1, number 4) did 5 points **(verified: `combat_spell_hit`)**.
- EBO's Sling hit a Poltergeist for 7 points and it went down **(verified: `combat_shoot`)**. Other hits in the
  same fight were between 2 and 9 points (read from small frames during the run, not in the set).
- Victory: "FOR DEFEATING THE MONSTERS EACH SURVIVOR RECEIVES 100 EXPERIENCE POINTS" for four Poltergeists; three
  were worth 75, so 25 each, shared by nobody: every survivor gets the full amount **(verified:
  `combat_victory`; the per-monster value is computed)**.
- Searching the room afterwards found nothing **(verified: `search_nothing`)**.

## 4. Going down and the end of the party
A character reduced to 0 hit points "GOES DOWN!!!" and is marked with `*` in the party list; the others fight
on. When the sixth went down the game showed "THE SHADOW OF DEATH HAS FALLEN UPON YOUR PARTY! FORTUNATELY, YOU
MAY RENEW YOUR QUEST FROM THE LAST INN IN WHICH YOU STAYED BY PRESSING 'ENTER'" **(verified:
`death_party_down`, `gameover`; the party was set to 1 hit point each for these shots)**. Nothing is lost that
was signed in at an inn **(inferred from the text)**.

## 5. Treasure
A chest (gold chest, gold box, iron box, cloth sack seen) offers Open it, Find/remove trap, Detect magic/trap;
each asks which character tries. Opened by the Robber, the gold chest in Dusk gave "EACH SHARE IS WORTH 0 GOLD",
200 gems to the opener and an Undead Amulet to the first character **(verified: `dusk_chest`, `chest_who`,
`chest_opened`)**.

## Open questions
- What the handicap number does; the order of turns; what Exchange and Retreat do in combat.
- Whether a character who "goes down" is unconscious or dead, and how each is cured.
- Trap chances and what Find/remove trap and Detect do.
