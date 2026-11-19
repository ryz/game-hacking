# Wizardry: Proving Grounds of the Mad Overlord (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry main`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
Create characters, form a party, enter the maze, walk square by square and fight what comes, take the loot,
go back up to rest, level and shop, and go a little deeper each time (verified: the set follows this loop from
`menu_training` to `ending_final_party`). Between loops the party grows in level and equipment, the floors get
harder and the player's own paper maps grow, since the game shows no map (DUMAPIC only reports the position:
`system_dumapic`). The run ends when Werdna's amulet is carried up to the Castle (`ending_congratulations`).

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Walk and turn | W steps forward, A turns left, D turns right; walls stop you | W A D | 1 square per step | [maps](maps/floors.txt) | `gameplay_maze_f1_start`, `gameplay_wall` | shown |
| Player verbs | Kick a door | K moves through the door in front (Werdna's door) | K | - | - | `gameplay_door`, `boss_werdna` | shown |
| Player verbs | Camp | C opens camp: inspect (spells and items are used from the character sheet), reorder, equip, leave | C, 1-6, R, E, Enter | - | - | `gameplay_camp`, `camp_reorder`, `inventory_camp_inspect` | shown |
| Player verbs | Equip | E)quip in camp walks through every member and asks per slot (weapon, armour, shield, helm ...), listing only items that fit | digit, Enter for none | - | - | `camp_equip` | shown |
| Player verbs | View toggles | S)tatus hides the party window and draws the view full height; O)ff hides command line and party window | S, O | - | - | `gameplay_status_off`, `gameplay_full_view` | shown |
| Player verbs | Inspect the square | I)nspect searches the square for bodies of other parties ("Found: * no one *") | I | - | - | `gameplay_inspect_none` | shown |
| Player verbs | Search at statues | some message squares then ask "Will you search (Y/N)?"; searching gives the square's item (bear statuette on floor 2) | Y, N | - | [findings](findings.md) | `system_search`, `system_search_found` | shown |
| Characters and progression | Creation | name, password, race (5), alignment (3), random bonus points spread over six statistics, then a class the statistics allow, keep Y/N | text, letters, Up/Down, Enter, Esc | elf base 7/10/10/6/9/6, bonus 9 here; new characters 8 HP, 100-199 gold | §4 | `create_name` ... `create_keep`, `training_inspect_new` | shown |
| Characters and progression | Classes and class change | 8 classes; the list offers only those the statistics and alignment allow; Training > C)hange class switches to another allowed class at level 1 | class letter | fighter STR 11, mage IQ 11, thief AGI 11 (verified on the elf) | content §6 | `create_bonus_spent`, `create_class`, `training_change_class`, `training_class_changed` | shown |
| Characters and progression | Character records | delete (Y/N), alter password, inspect from the Training Grounds | D, A, I | - | - | `training_char_menu`, `training_delete`, `training_password`, `training_pick` | shown |
| Characters and progression | Levels | experience from fights; a level is made only when resting at the inn: "You made the next level!", random changes to each statistic and new hit points | rest at the inn | fighter level 2 at 1000 E.P. (verified) | §5 | `inn_stables`, `inn_levelup` | shown |
| Characters and progression | Level drain | vampires (and the "unseen entities" with Werdna) take levels per touch: RYZ 13 -> 11, CONDI 13 -> 11 | - | 2 levels per touch here; 4 in the scout's run | §6 | `boss_level_drain`, `boss_drained_after`, `ending_chevron` | shown |
| Characters and progression | Age | kept in weeks, shown in years; rest at the inn costs weeks | - | new characters 14-16 | - | `inventory_inspect_l1`, `inventory_sheet_vet` | shown |
| Resources and economy | Gold | each character carries gold; the tavern divides it (D)ivvy), the sheet pools it into one purse (P)ool); trade moves gold and items between members | D, P, T | - | - | `inventory_pool`, `inventory_trade`, `inventory_trade_gold` | shown |
| Resources and economy | Boltac's | buys at list price, pays half, identifies and uncurses for gold; warns before a class buys something it cannot use | B S U I P, F/B to page | prices in [items](items.md) | [items](items.md) | `shop_boltac` ... `shop_uncursed` | shown |
| Resources and economy | Inn | stables free (no healing), cot 10, economy 50, merchant 200, royal suite 500 gold per week; hit points come back week by week while gold counts down | room letter | cot: about 1 HP per week here | §5 | `menu_inn`, `inn_recuperating` | shown |
| Resources and economy | Temple of Cant | revives and cures for a donation by level: paralysis 100, death 250, ashes 500 gold per level; the ritual can fail | letter, payer | 1100 (L11 paralyzed), 3250 (L13 dead), 6500 (L13 ashes) | §5 | `temple_dead` ... `temple_lost_party`, `ending_temple_paralysis` | shown |
| Conflict | Rounds | each round every member gets an order, then everyone acts in an order the game decides; messages tell each blow | F P S D U R T, group number | messages stay about 160 frames (2.7 s) each | §6 | `battle_orders`, `battle_kill`, `battle_multi_hit` | shown |
| Conflict | Front and back rank | the first three members can fight; members 4-6 parry, cast or use items | - | 3 front | - | `battle_orders` | shown |
| Conflict | Surprise | "You surprised the monsters!" / "The monsters surprised you!": a first round without spells for the surprised side | - | - | [findings](findings.md) | `battle_options`, `battle_f3_wolves` | shown |
| Conflict | Targets | Fight and group spells ask "Fight which group (#)?" when there is more than one group | 1-4 | up to 4 groups | - | `battle_group_select`, `boss_werdna_orders` | shown |
| Conflict | Identification of monsters | groups start as generic names ("Unseen entity", "Man in robes") and get their real names as the fight goes on | - | - | - | `battle_identified`, `boss_vampires_identified` | shown |
| Conflict | Friendly groups | some groups are friendly: F)ight or L)eave | F, L | - | - | `battle_friendly`, `battle_f1_undead_kobolds`, `battle_f2_gas_clouds`, `battle_f7_friendly_wyverns` | shown |
| Conflict | Dispell | priests (and the elite classes) turn undead: "EBO dispells one monster"; dispelled monsters give no E.P. | D | 0 E.P. (verified for the Lifestealer) | - | `battle_dispell` | shown |
| Conflict | Use item | U)se in battle or camp casts the item's spell (potion of Dios heals) | U, item number, target | - | - | `battle_use_item`, `camp_use_item` | shown |
| Conflict | Run | R)un tries to flee; on success "One moment" and the party is back in the maze, on a failed try the monsters act | R | 3 of 4 timings fled from six giant rodents | - | `battle_run` | shown |
| Conflict | Status conditions | asleep (Katino), poisoned (`gameplay_poisoned`), paralyzed, dead, ashes, lost; sleeping and paralyzed members move to the back of the party | - | - | - | `battle_enemy_katino`, `battle_party_asleep`, `boss_paralyzed`, `boss_four_dead`, `temple_lost_party` | shown |
| Conflict | Spell resistance | monsters can resist a spell ("an unseen entity resists the spell") | - | - | - | `boss_spell_resisted` | shown |
| Opponents | Groups | up to four named groups with counts; a group's picture shows in the view | - | - | content §3 | `battle_f4_fixed`, `boss_werdna` | shown |
| Opponents | Monster spells | monster casters use the party's spell list: Katino, Lahalito, Badialma, Dilto, Molito, Tiltowait | - | - | content §3 | `battle_enemy_katino`, `battle_enemy_lahalito`, `battle_badialma`, `boss_enemy_dilto`, `boss_werdna_tiltowait` | shown |
| Opponents | Fixed fights | squares that always start a fight (floor 3, 4, 7 and Werdna on 10) | - | - | [maps](maps/floors.txt) | `battle_f4_fixed`, `battle_f7_dragons`, `boss_werdna` | shown |
| Opponents | Random encounters | fight zones ("rooms") start fights when entered or turned in; the group comes from the floor's encounter table | - | floor 1: monsters 0-5, floor 10: 70-86 (disk data) | [maps](maps/floors.txt) | `battle_f1_kobolds`, `battle_f2_priests`, `battle_f2_humanoids`, `battle_f2_gas_clouds_hostile`, `battle_f9_lifestealer`, `battle_f10_thieves` | shown |
| Items and equipment | Equipment | weapons, armour, shields, helms, gauntlets, misc; equipped items marked "*"; armour class drops from 10 | E)quip | AC -4 with plate+2, shield+2, helm+1 | [items](items.md) | `inventory_sheet_vet`, `menu_castle_vets` | shown |
| Items and equipment | Chests and traps | a won fight may leave a chest: open, Calfo (a priest names the trap), leave, inspect, disarm; a trap goes off on opening (exploding box: a member slain; poison needle: POISON); disarm needs the trap's name typed | O C L I D | - | §6 | `battle_chest`, `chest_calfo_who`, `chest_calfo`, `chest_poison_needle`, `chest_exploding`, `chest_disarmed` | shown |
| Items and equipment | Identification and curses | found items are unknown ("?SWORD"); a bishop identifies (I on the sheet) or Boltac for gold; a cursed item ("-") stays equipped until Boltac uncurses (removes) it | I, U | - | [items](items.md) | `shop_identify`, `shop_identified`, `inventory_bishop_identify`, `inventory_identified`, `shop_uncurse` | shown |
| Abilities and magic | Spells | typed by name ("Spell name ?") in battle and camp; 21 mage and 29 priest spells in 7 levels, points per level | S, name, Enter, target | points per level | content §5 | `battle_spell_prompt`, `inventory_mage_book`, `inventory_priest_book`, `camp_cast_whom` | shown |
| Abilities and magic | Utility spells | DUMAPIC reports the position; MALOR teleports by offsets (E/W/N/S/U/D); healing with DIOS | camp | - | content §5 | `system_dumapic`, `camp_malor` | shown |
| World and navigation | Maze | ten floors of 20 x 20 squares, walls, doors, hidden doors, rooms, stairs, elevators (floors 1-4 and 4-9) | - | 10 floors | [maps](maps/floors.txt) | `gameplay_maze_f1_start`, `gameplay_stairs`, `gameplay_elevator`, `gameplay_elevator_f4` | shown |
| World and navigation | Traps of the maze | pits ("A pit!"), spinners (turn the party silently), teleporters, a chute (floor 9 to 10), darkness, anti-magic ("* Fizzle! *"), rock (death) | - | positions in maps | [maps](maps/floors.txt) | `gameplay_pit`, `gameplay_chute`, `gameplay_dark`, `system_fizzle` | shown |
| World and navigation | Signs and scenes | message squares: signs, statues, placards, smoke and fog that push the party out | Enter | about 40 squares | content §2 | `dialogue_*` | shown |
| Goals and gating | Main goal | Werdna's amulet on floor 10 (17,3), taken up to the castle | - | - | §6 | `boss_amulet_found`, `ending_congratulations` | shown |
| Goals and gating | Gates | rooms that need an item: bronze smoke (bronze key), silver fog (silver key), a door only the bear/frog statuette opens, the floor 4 elevator room that puts the party to sleep without the blue ribbon | - | - | content §2 | `dialogue_f2_bronze_smoke`, `dialogue_f2_silver_fog`, `dialogue_f2_door`, `dialogue_f4_asleep`, `dialogue_f4_bear_wall` | shown |
| Chance | Random rolls | encounters, monster groups, hits, damage, bonus points, level-up changes, temple rituals; with a fixed route they repeat | - | - | - | `inn_levelup`, `temple_buried` | shown |
| Failure and recovery | Death and the cemetery | a party killed: "Your entire party has been slaughtered" and the cemetery; dead members stay in the maze for a rescue party; the temple revives for gold, ashes can be buried (lost) | Enter | - | §5 | `gameover_cemetery`, `chest_slain`, `gameplay_member_dead`, `temple_buried` | shown |
| Saving and sessions | Scenario disk | the roster is written to the scenario disk while playing and when leaving the game; leaving in the maze leaves the party "out" (Utilities: restart an "out" party) | L)eave game | - | playbook Saves | `menu_utilities`, `util_restart_none` | shown |
| Saving and sessions | Moving characters | Utilities M)ove characters asks for the source scenario disk (the way characters go to Wizardry II and III) | M | - | - | `util_move` | shown |
| Pacing and difficulty | Ramp | floor 1 slimes and kobolds for 8-HP characters; a level 1 party on floor 4 dies in one round of Lahalito; Werdna's own Tiltowait killed four level 13 members in one timing | - | - | §6 | `battle_options`, `battle_enemy_lahalito`, `boss_four_dead` | shown |

## 3. How the systems feed each other
- Fights give experience, gold and chests; experience becomes levels only at the inn; levels give hit points
  and spell points; gold buys equipment at Boltac's and pays the inn and the temple (verified screens).
- Spell points are spent in the maze and come back by resting; deeper floors need more of them.
- Death costs gold at the temple (or the character, when ashes are buried); level drain undoes levels, as
  the two drained fighters at the end show (`ending_chevron`).

## 4. Character creation (verified, `create_*`)
1. Name (shown in capitals; "Name already in use" for a taken one), password (may be empty).
2. Race: human, elf, dwarf, gnome, hobbit. The elf's base statistics: STR 7, IQ 10, PIE 10, VIT 6, AGI 9, LUC 6.
3. Alignment: good, neutral, evil.
4. Bonus points (9 in the shot; 6-7 seen in other rolls): Enter moves the pointer, the cursor keys add or
   take back points, Esc finishes and is refused while points are left. The class list on the right updates
   with each point: STR 11 opens fighter, IQ 11 mage, AGI 11 thief (priests need good or evil alignment).
5. Class letter, then "Keep this character (Y/N)?". The new character has 8 hit points and 100-199 gold
   ([findings](findings.md)); a new mage shows 0 spell points until the maze recomputes them (verified:
   `training_inspect_new`).

## 5. Castle services (verified)
- **Inn** (`menu_inn`): who stays, then a room. Stables are free but heal nothing; they still run the level
  check ("You need 1000 more E.P. to make the next level", `inn_stables`). In a paid room the sheet counts
  weeks: hit points rise and gold drops (cot, 10 gold per week: 3 -> 5 HP and 102 -> 82 gold in two weeks,
  `inn_recuperating`). When the E.P. are enough the level is made at the end of the stay with a list of
  statistic changes and hit points gained (`inn_levelup`: IQ, agility, luck up, vitality down, +3 HP).
- **Temple** (`temple_*`): "Who shall we help?" lists characters who are not OK; the donation is by level
  (paralysis 100, death 250, ashes 500 gold per level); a member pays. Ritual "Murmur - chant - pray -
  invoke!", then "* NAME has been healed *" or, for ashes, "* NAME will be buried *" (lost for good,
  `temple_lost_party`). A dead character's revival can fail into ashes (source, series; not seen here).
- **Boltac's** (`shop_*`, [items](items.md)): one member enters; buy (pages of six, F/B to scroll),
  sell (half price), uncurse (the cursed item is removed), identify, pool gold.
- **Training Grounds and Utilities**: §4 above; change name, move characters, restart an "out" party.

## 6. Combat (verified)
- First round: a side that is surprised gets no spells (the party's options lack S)pell, `battle_options`).
- Each blow is one message: "RYZ charges at a slime and hits once for 4 damage / The slime is killed!";
  fighters at level 13 hit 2-3 times per round (`battle_multi_hit`).
- After a fight: "Each survivor gets N E.P." (36 for four slimes, 433 for six giant rodents, 5472 for Werdna and
  his guards), then gold or a chest. Undead turned by dispell give 0 E.P.
- Werdna's fight here (`boss_*`): Werdna (71 hit points, RAM) with a group of one and a group of two "unseen
  entities" (named after round 2 as a Vampire lord and 2 Vampires). Round 1 was a surprise round with no spells;
  in round 2 Deddo's TILTOWAIT killed Werdna, the guards drained RYZ 2 levels and paralyzed him; round 3
  another TILTOWAIT finished the Vampire lord and the vampires. After the fight "CONDI was drained!", "RYZ was
  drained!" (both 13 -> 11), then "CONDI found: AMULET". In another timing (`boss_werdna_tiltowait`) Werdna
  cast TILTOWAIT first and killed four members. The scout's fight met him as "Man in robes" with a Vampire
  lord and 4 Vampires: the guards are rolled.
- Ending (`ending_*`): reaching the Castle with the amulet gives "50,000 G.P. and E.P." and the Chevron of
  Rank (">") to every member, the paralyzed one too; the amulet leaves the pack; a member who is not OK is
  taken out of the party at the Castle.

## Open questions
- Run: the chance to flee and what decides it (3 of 4 timings fled from the rodents).
- The searchable statues on floor 1 (chicken, hooded man, boar) asked nothing in any approach tried (see
  findings); Murphy's ghost was not met.
- Criticals and stoning were not seen.
