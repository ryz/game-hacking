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

## 6. Encounter options, more results (round 2)
- **Retreat** worked on both tries (four Poltergeists, four Mutant Larvae): the party stands in front of the inn
  door, no fight **(verified)**. Retreat prints no message: the first frame after `R` is already the map view at
  the inn door with its sign, pixel for pixel the picture `sorpigal_inn_sign`, so it has no shot of its own
  (fix-up round 2026-11-18: 15 frames sampled from the key press on; the shot `encounter_retreat` was dropped).
- **Bribe**: two Guardsmen with three Gnomes answered "GIVE UP ALL YOUR FOOD (Y/N)?"; after Y the fight was
  off, the party was back on the map and every character's food was 0 (`encounter_bribe_demand`,
  `encounter_bribe_paid`, `encounter_bribe_food`). Goblins, Guardsmen alone, Mutant Larvae and Poltergeists
  answered "NO RESPONSE" and attacked **(verified)**.
- **Surrender** was refused by all four groups tried ("THE MONSTERS DON'T TAKE PRISONERS!") **(verified)**.
- Some fixed groups skip the options and start combat at once: the Scorpion with its Giant Scorpions in sector
  D-1, the two Unicorns of the Arena (`boss_scorpion`, `cave_arena_fight`) **(verified)**. A message saying the
  party was surprised was not seen in 40 timed entries into the room in Sorpigal.

## 7. Combat orders at work (round 2)
Turn order in the fight against four Poltergeists, every round: MNZ (Speed 17), EBO (15), RYZ (14), CUBI, then
the monsters, then DEDDO and CONDI **(verified; that Speed decides is inferred)**.
- **Fight** asks "FIGHT WHICH 'A'-'C'?", only the monsters marked `+` (`combat_fight_prompt`).
- **Shoot** fires at once without asking for a target (`combat_shoot`).
- **Exchange** asks "EXCHANGE PLACES WITH (1-6)?" and swaps the two in the formation and in the party list: MNZ
  to position 1, RYZ to 6 (`combat_exchange_prompt`, `combat_exchange_done`).
- **Use** opens the character's item lists with "USE WHICH" (`combat_use`).
- **Block** and **Retreat** (as an order, round 1) printed nothing; the next character was asked **(verified)**.
- **Cast**: Bless (Cleric 1-2) "DONE" (`combat_bless`); Sleep (Sorcerer 1-8) asks a target, "POLTERGEIST IS NOT
  AFFECTED!" (`combat_sleep_immune`); Turn Undead (Cleric 1-8) "SOME MONSTERS WERE DESTROYED!", four Skeletons
  became two (`combat_turn_undead`) **(verified)**.

## 8. What strong monsters did to the party (round 2)
The party's hit points were raised to 44-71 for these fights; statistics stayed level 1 **(all verified)**.
| Monster | Where | Seen |
|---|---|---|
| Red Dragon (ten) | sector A-2 (10,4) | "BREATHES FIRE": 83 points to four characters and 41 to two, all "go down"; the next breath, 87 and 43, kills them: "RYZ DIES!" (`battle_red_dragons`, `combat_dragon_breath`, `combat_dies`) |
| Medusa (nine) | cavern 9 (15,4) | "MEDUSA GAZES: DEDDO IS TURNED TO STONE!" (`battle_medusas`, `combat_stoned`) |
| Lich with five Mummies | sector B-2 (2,1) | acts before anyone: "LICH CASTS DISINTEGRATION: EBO IS ERADICATED!" (`boss_lich`, `boss_lich_eradicates`) |
| Demon Lord, two Greater, three Lesser, seven Minor Demons | cavern 3 (8,7) | Demon Lord: 2 hits for 46 points, "CONDI IS ERADICATED"; Greater Demon: 6 hits of 7 for 29 points "AND DRAINS ABILITIES!" (`boss_demon_lord`, `boss_demon_drain`, `boss_demon_drains`) |
| Three Evil Eyes, two Lava Beasts, a Naga | below Dragadune, level 3 (1,14) | "NAGA CASTS PARALYZE": four paralyzed, two "NOT AFFECTED"; paralyzed characters are starred and skipped; Lava Beast 2 hits for 11 (`boss_evil_eyes`, `combat_paralyzed`, `combat_lava_beast`, `combat_conditions`) |
| Magician (thirteen) | PP level 1 (10,7) | "MAGICIAN CASTS LIGHTNING BOLT": 10 to 41 points per target (`battle_magicians`, `combat_magicians`) |
"GOES DOWN" (0 hit points, unconscious) and "DIES" are two steps: a hit on a downed character kills
**(verified: `combat_dragon_breath`, `combat_dies`, `unconscious_quickref`)**.

## 9. Traps
- A locked door can be trapped. Bash at the door of Sorpigal (3,7): "GAS!! ... NOXIOUS FUMES FILL THE AIR!",
  1 to 2 points to everyone, and the door gave way: the room's fight followed (`bash_trap`, `bash_after`).
  Unlock by the Robber: "SUCCESS!", no trap (`unlock_success`). Unlock by the Knight: "BLADES!! RAZOR SHARP
  BLADES SLICE THROUGH THE PARTY!", 2 to 4 points each (`unlock_trap`, `trap_damage`) **(verified)**.
- Bash against a plain wall prints nothing **(verified, no shot: the screen does not change)**.
- The gold chest in Dusk: Detect magic/trap by the Sorcerer says "MAGIC (Y) TRAP (Y)" (`chest_detect`);
  Find/remove trap by the Robber set the blades off (`chest_find_trap`) and the level 1 party died of it (the
  game-over text followed); Open by the Robber or the Knight just opened it (`chest_opened`) **(verified)**.

## Open questions
- What the handicap number does; the order of turns; what Exchange and Retreat do in combat.
- Whether a character who "goes down" is unconscious or dead, and how each is cured.
- Trap chances and what Find/remove trap and Detect do.
