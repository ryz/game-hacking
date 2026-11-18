# Characters, levels and magic

Shots are in `../shots/main/`; a shot id `x` in category `c` is the file `might-and-magic_dos_na_c_x.png`.

## Overview
A roster holds up to 18 characters; up to six form the party at an inn. A character has seven statistics, a
class, a race, an alignment and a sex, and carries six equipped items and six backpack items **(verified:
`roster_view_all`, `profile_ryz`)**.

## 1. Creation
Seven statistics are rolled together, each 3 to 18: Intellect, Might, Personality, Endurance, Speed, Accuracy,
Luck. Enter re-rolls all seven; the classes the roll qualifies for are listed (`create_roll`). Then race
(`create_race`), alignment (`create_alignment`), sex, name of up to 15 letters (`create_name`) and "SAVE
CHARACTER (Y/N)?" (`create_save`) **(verified)**. Class requirements and race changes: see `../playbook.md`
(inferred from about 25 rolls).

## 2. The profile and what can be done from it
Name, sex, alignment, race, class; the seven statistics; level, age, experience; spell points and spell level;
gems; hit points now and maximum; gold; armor class; food; condition; equipped items 1-6 and backpack A-F
**(verified: `profile_ryz`)**. Commands: Cast, Discard, Equip (`equip_prompt`), Gather (all gems, gold or
food onto this character), Remove, Share (gems, gold or food split among the party, `share_prompt`), Trade,
Use, quick reference (`quickref`) **(verified)**. From the roster a profile offers re-name and delete instead
(`profile_menu`, `rename_prompt`) **(verified)**.

## 3. Party commands while exploring
Order re-arranges the six (`order_prompt`); Protect lists the active party spells (`protect_active`: Leather
Skin after the Sorcerer cast it); Rest asks "REST HERE (Y/N)?" and, undisturbed, ends with "REST COMPLETE: NO
ENCOUNTERS!" (`rest_prompt`, `rest_complete`); Search; Bash; Unlock asks who tries (`unlock_who`)
**(verified)**.

## 4. Levels
Experience alone does not raise a level; training in a town does, for gold. A Knight with 1685 experience was
offered level 2 for 25 gold; training printed "CONGRATULATIONS! YOU ARE NOW LEVEL 2, YOU GAINED 11 HIT POINTS!"
(15 to 26), and the character's age went from 18 to 19; level 3 then needed 1315 more experience, so 3000 in
all **(verified: `train_level2`, `train_levelup`, `profile_level2`, `train_level3_need`)**.

## 5. Magic
A spell is cast by its level and number, then Enter; outside combat from the caster's profile (`cast_prompt`).
Seen: Leather Skin (Sorcerer 1-5, shows under Protect), Light (Sorcerer 1-6, makes a dark area visible:
`dungeon_darkness` against `dungeon_lit`), Location (Sorcerer 1-7, `location_spell`), Flame Arrow (Sorcerer
1-4, 5 points in combat, `combat_spell_hit`); each cost 1 spell point **(verified)**. The full list of 94
spells is in the manual **(source)**.

## 6. Profile commands at work (round 2)
All from a character's profile while exploring; each prints its own prompt **(verified, shot ids in brackets)**.
- **Share** asks gems, gold or food and splits the party's total evenly; the character viewed keeps the
  remainder: 1833 gold became 305 each and 308 for RYZ (`share_done`).
- **Gather** asks gems, gold or food and moves everybody's onto the character viewed: CONDI then held all 1833
  gold (`gather_prompt`, `gather_done`).
- **Trade** asks "TRADE WITH 1-6", then gems, gold, food or item, then "HOW MUCH" (typed, Enter) or the item's
  letter: 250 gold, a Club and 4 food changed hands (`trade_with`, `trade_which`, `trade_how_much`,
  `trade_gold_done`, `trade_item_done`, `trade_food_done`).
- **Discard** asks for a backpack letter and removes the item at once, without a second question
  (`discard_prompt`, `discard_done`).
- **Use** asks for an item, equipped (1-6) or carried (A-F). An ordinary weapon answers "NO SPECIAL POWER"
  (`use_prompt`, `use_no_power`). A Might Potion raised Might from 15 to 20 (`use_might_potion`); Magic Herbs
  ask "CAST ON 1-6" and healed 8 hit points, 6 to 14 (`use_herbs_target`, `use_herbs_done`). Both show 3
  charges under Detect Magic and stay in the backpack after one use (`detect_magic`).
- **Remove** asks for an equipped slot and moves the item to the backpack; without the Leather Armor RYZ's armor
  class fell from 3 to 1 (`remove_prompt`, `remove_done`).
- **Equip** refuses an item the class may not use with "WRONG CLASS": a Sorcerer and Chain Mail
  (`equip_wrong_class`; the mail was put into the backpack by a memory edit).
- **Cast** outside combat: level, number, Enter, then "CAST ON 1-6" for spells with a target. First Aid
  (Cleric 1-4) cost 1 spell point and healed 8 hit points, 6 to 14 (`cast_on_whom`, `cast_done`,
  `cast_healed`). Detect Magic (Sorcerer 1-2) lists the caster's backpack: magic yes or no and charges
  (`detect_magic`). Protection from Fear (Cleric 1-7) shows under Protect as "+ 21%" next to Light (1) and
  Leather Skin (`protect_three`).
- **Order** takes the six old positions in the new order and redraws the party list (`order_done`).

## 7. Conditions
The condition line of the profile and the quick reference names: asleep, blinded, silenced, diseased,
poisoned, paralyzed, unconscious, dead, stone, eradicated; several can show at once ("BLINDED,ASLEEP")
**(RAM: each set in memory and read off the quick reference; `conditions_quickref` shows six of them)**. Seen
arising in play: unconscious at 0 hit points after a fight (`unconscious_quickref`), paralyzed by a Naga's spell
(`combat_paralyzed`, `combat_conditions`), stone by a Medusa (`combat_stoned`), dead by a second dragon breath
(`combat_dies`), eradicated by a Lich (`boss_lich_eradicates`) **(verified)**. Cures at a temple: see
[sorpigal.md](sorpigal.md) section 6.

## Open questions
- Exact class requirements; what each race changes; experience needed beyond level 3; hit points gained per
  level by class; why training aged the character a year.
