# Might and Magic (NES) - combat

## Overview
Fights start when the party steps onto a fight square (most red squares in towns and caves) or meets a random
group; up to six monsters face the party of six **(verified: `battle_encounter`, cavern event scan)**. The party
first picks Attack, Bribe, Run or Giveup; on Attack each member in turn gets orders (Auto, Fight, Cast, Shoot,
Block, Row, Use, View, Prot, Run) and acts at once, interleaved with the monsters by speed **(verified:
`battle_orders`, message sequence of the cavern fight)**. Messages type out on the left; the monster list on the
right shows ▲ (front, reachable by weapons) and ▽ (back) **(verified: `battle_target`)**.

## 1. Orders
- Fight: pick a target from the list with its hit points ("Goblin 9") **(verified: `battle_target`)**.
- Cast: spell level 1-7, then the spell (Mage or Cleric list), then the target **(verified: `battle_cast_level`,
  `battle_mage_spells`, `battle_cleric_spells`)**. Knights and Robbers have no Cast (shown as dots); Archers get
  Shoot **(verified: order menus of RYZ, CUBI, MNZ)**.
- Level 1 Mage spells: Awaken, Detect, Voice, Flame, Armor, Light, Locate, Sleep. Level 1 Cleric spells: Awaken, Aim,
  Blind, Cure1, Light1, Cure3, P-Fear, Bless1 **(verified)**. Flame did 3 damage to a Savage Shrew
  **(verified: `battle_spell_flame`)**.
- Anti-magic squares answer "Magic doesn't work here." (Sorpigal) **(verified)**.

## 2. Results
- Attack messages: "<attacker> attacks <target> N times, hit M times, Damaged P Pts", "Monster goes down"
  **(verified: `battle_hit`, `battle_kill`: a level 9 Knight hit a Wolverine 2 of 3 times for 12)**.
- Monsters may run ("Savage Shrew runs away...") or wait ("Rabid Jackal waits for an opening!"); attacks can
  paralyse ("RYZ is paralyzed!") **(verified, cavern fight)**.
- A member at 0 hit points "goes down"; a paralysed member reduced further "dies!" **(verified: `battle_death`,
  `battle_dies`)**.
- Victory: "Each survivor receives N EXP" (300 for 2 Wolverines, 4 Savage Shrews, then 2 Orcs and Rabid Jackals) -
  experience is not split by party size in the message **(verified: `battle_victory`)**.
- When the whole party is down: "The Shadow of Death has fallen upon your Party!" and the game resets to the
  power-on screens (Continue loads the last inn save) **(verified: `gameover`)**.

## 3. Treasure
- After a won fight, Search may find a chest: Open, Untrap, Detect, Cancel **(verified: `chest_found`,
  `chest_menu`)**. Opening without untrapping: "Caught in a trap!" "BLADES!! Sharp blades slice through the
  party!", then the items: "RYZ gets an item" **(verified: `chest_blades`, `chest_loot`)**.

## Open questions
- Damage and hit formulas, turn order rule, encounter rates, Bribe and Giveup outcomes.
