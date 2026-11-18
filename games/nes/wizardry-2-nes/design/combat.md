# Wizardry: Knight of Diamonds (NES) - combat

## Overview
Fights are round based: every member gets an order (Fight, Parry, Spell, Dispell, Use Item, Run, Take back; the
list depends on class and position), then a last 'Fight / Take back' confirms the round and the messages play
**(verified: `battle_orders`)**. Up to four monster groups are listed at the top with their counts
**(verified: two groups in `battle_groups`)**. The rules follow the NES Wizardry I
(`../../wizardry-nes/design/combat.md`).

## 1. Orders
- Front row (members 1-3) may Fight; members 4-6 only Parry, Spell (casters), Use Item, Run **(verified:
  `guardian_kobold`, CUBI's and DEDDO's options)**.
- With several groups, 'Fight which group?' and 'Cast spell on group?' pick the target **(verified)**.
- Spell menu: 'Cast what spell?', one level at a time with the points left, e.g. 'Magic spell M7(2)'; Left goes up
  a level (Right x4 took EBO from C1 to C5 but did nothing for DEDDO on M1, see findings); only spells usable in battle are listed (Dumapic is missing on M1) **(verified:
  `battle_spell_mage`, `battle_spell_menu`)**.
- A Bishop (MNZ) opens the cleric levels first **(verified: `battle_spell_menu`)**.
- In some rooms the Spell order is missing for every caster (floor 4 (1,4), 2 Evil Eyes) **(verified; cause
  not checked: anti-magic area or the monsters)**.

## 2. Damage and messages
- Melee: 'EBO tries to stab Kobold King and hits 2 times for 17'; 'CONDI charges at Kobold King and hits 5 times
  for 29. Kobold King is dispatched.' **(verified: `battle_melee`, `battle_dispatched`)**.
- Monsters cast too: 'Woman in Robes casts a Melito': one message per member, 1-8 damage each
  **(verified: `battle_enemy_spell`)**.
- Badialma (cleric 5) kills one monster outright; Tiltowait (mage 7) kills the groups one by one
  **(verified: `battle_cast_cleric`, `battle_tiltowait`)**.
- Monsters flee ('Man at Arms flees.') **(verified)**.
- A member at 0 hit points is 'dispatched'; at the end of the round the dead move to the back of the list with
  status Dead **(verified: `party_dead`, `party_dead_list`)**. When all six die: six tombstones, then the castle
  with an empty party **(verified: `gameover`, `gameover_castle`)**.

## 3. Rewards
- 'Each survivor gets 476 E.P.' (Kobold King), 721 E.P. (7 Women in Robes and 2 Men at Arms) **(verified)**.
- Guardians (special type 0F) hand over their item: 'CUBI found BADGE' (the Gory badge, unidentified name)
  **(verified: `battle_found_badge`)**.
- Chests: Inspect, Calfo, Disarm, Open, Leave alone; Inspect names the trap ('Poison Needle'); opening it triggers
  it ('Oops! Poison Needle') and the opener is poisoned; loot 'RYZ found ARMOR' and 'Each survivor gets 33 G.P.'
  **(verified: `chest` to `chest_gold`, `poisoned`)**.

## 4. Status
- Status codes in the character record: 0 OK, 3 paralysed (P-lyze), 5 dead, 6 ashed **(RAM + `temple`)**.
- Poison shows as 'Poison' in the party list after the fight **(verified: `poisoned`)**.
- Armor class shows as 'LO' below -9 (RYZ in the full regalia) and hit points with '+' while regenerating
  **(verified, knight route)**.

## Open questions
- Hit chances, damage dice and the E.P. formula were not measured.
- Whether the missing Spell order comes from the room or the Evil Eyes.
