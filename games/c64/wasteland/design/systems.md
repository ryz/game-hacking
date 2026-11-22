# WASTELAND - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The party walks the world map one square per key, meets random encounters while time passes, and steps onto
location icons to enter towns and buildings **(verified, `env_world_valley`, `loc_agcenter`)**. Inside, squares
describe themselves as the party steps on them, and shops, doctors and people are entered like small locations
**(verified, `hp_store_entry`, `hp_shop`, `hp_infirmary`)**. Fights give experience to the survivors and cost
CON that a doctor restores for money **(verified, `battle_xp`, `hp_infirmary_exam`)**. Skills are used on the
map through Use (Perception on a square) as well as in fights **(verified, `field_which_way`)**.

## 2. Systems
Go through every group; "none" where the game has nothing.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Field commands | one key each: U Use, E Enc, O Order, D Disband, V View, S Save, R Radio; digits open a ranger's sheet; SPACE shows or hides the roster **(verified)** | keyboard | | interface.md | `field_use`, `field_enc`, `field_disband`, `field_radio`, `field_save`, `world_full` | shown |
| Player verbs | Use a skill on the map | Use, ranger, Skill, skill number, then a direction (I J K L) or SPACE for the party's own square **(verified)** | U, digit, S, digit, direction | Perception on an empty square: "You see nothing special." | | `field_use_kind`, `field_use_skill`, `field_which_way`, `field_perception` | shown |
| Player verbs | Order | rearranges the marching order: pick the rangers one by one, the last is placed automatically **(verified)** | O, Y, digits | | | start set `21_order`, `22_order_pick`, `23_world_ordered` | shown |
| Characters and progression | Ranger creation | Create rolls seven attributes and MAXCON; SPACE rerolls the whole set, RETURN keeps it; then name (upper case), sex, nationality, skills **(verified)** | C, SPACE, RETURN, text, M/F, 1-5, digits | skill points equal IQ (IQ 9 -> 9, IQ 11 -> 11) **(verified, `rc_roll`, `rc_reroll`)**; four rangers at most, delete one first **(verified)** | | `rc_roll`, `rc_reroll`, `rc_nation`, `rc_skills`, `rc_party`, `rc_roster` | shown |
| Characters and progression | Skills | each skill costs 1 point at level 1; a skill already owned costs 2 for its next level; each has a minimum IQ (3 for most, 6 for Knife throw and Perception) **(verified, `rc_skills`, start set `17_rc_skills_taken`)** | digit per skill, RETURN ends | 9 skills offered at creation | | `rc_skills`, `char_skills` | shown |
| Characters and progression | Experience | each surviving ranger who acted gains experience after a won fight: 5 each against 3 Animals; 42 and 14 against 4 wild canines (the share differs per ranger) **(verified)** | | | | `battle_xp`, start set `35_battle_won` | shown |
| Resources and economy | Money pool | every ranger carries cash; shops and doctors work with the pooled money of the party ("Pool Money") **(verified, `hp_shop_buy`, `hp_infirmary_exam`)** | | new rangers have $0 **(verified)** | | `char_stats`, `hp_shop_buy` | shown |
| Resources and economy | Shop | Buy or Sell; Buy shows nine items with prices: Book 10, Canteen 10, Crowbar 15, Gas mask 150, Geiger counter 300, Hand mirror 10, Jug 1, Map 50, Match 10 (Highpool); buying takes the price from the pool at once **(verified, `hp_shop_bought`: 1287 -> 1272 for a Crowbar)** | B/S, digit | the Sell list offers 80% of the buying price (Canteen 8, Crowbar 12, Hand mirror 8, Match 8) **(computed from `hp_shop_sell` and `hp_shop_buy`)** | | `hp_shop`, `hp_shop_buysell`, `hp_shop_buy`, `hp_shop_bought`, `hp_shop_sell` | shown |
| Resources and economy | Doctor | the infirmary offers what the chosen ranger needs: Exam $25 for a healthy ranger; Exam $25 and Healing for a wounded one **(verified, `hp_infirmary_exam`, start set `47_infirmary_price`)** | digit | | | `hp_infirmary`, `hp_infirmary_exam` | shown |
| Resources and economy | Ammunition | pistols use clips carried in the pack; AMM on the roster counts the loaded rounds **(verified, roster: AMM 18 for Angela Deth's VP91Z, 7 for Thrasher's M1911A1)** | W, L | RYZ starts with eight .45 clips **(verified, `char_items`)** | | `char_items`, `battle_weapon` | shown |
| Conflict | Combat rounds | the encounter names the group, its size and distance in feet; each conscious ranger gets an order (Run, Use, Hire, Evade, Attack, Weapon, Load/Unjam), then "Use these options (Y/N)?" plays the round as scrolling text **(verified)** | R U H E A W L, Y | | | `battle_appears`, `battle_menu`, `battle_confirm`, `battle_round` | shown |
| Conflict | Weapon change | Weapon picks a gun from the pack; it takes that ranger's action for the round ("RYZ swaps equipment") **(verified, start set `33_battle_round` route)** | W, digit | | | `battle_weapon`, start set `31_battle_weapon` | shown |
| Conflict | Evade | an evading ranger is hit less: with all four at CON 1 against Radioactive Vermin, two Evade rounds cost one ranger, the Attack round after them two more **(verified, `battle_radrat` route; one fight only, inferred as a rule)** | E | | | `battle_radrat` | shown |
| Conflict | Hire | asks "Which group?" with each group's size and distance: opponents can be asked to join **(verified prompt; joining source)** | H, digit | | | `battle_hire` | shown |
| Conflict | Unconscious | a ranger brought to 0 shows UNC in the CON column and gets no orders **(verified, start set `34_battle_hurt`, `battle_radrat`)** | | | | `battle_radrat` | shown |
| Opponents | Random groups | Animals (vermin, wild canines) on the world map near the Ranger Center; group of 3-4; wild canines hit for 5 to 13 per bite **(verified)** | | | content.md | `battle_appears`, `battle_round` | shown |
| Items and equipment | Pack and hand | a ranger holds one weapon (roster WEAPON) and carries items in a numbered list paged with RETURN **(verified, `char_items`)** | digit, RETURN | | | `char_items` | shown |
| Abilities and magic | none | no magic; skills (above) take their place **(verified: no spell command anywhere)** | | | | no shot: nothing to show | described |
| World and navigation | World map | one 64 by 64 square map; one square per key (I J K L); mountains block ("This mountain is in your way"), the south and east edges give "miles and miles of endless wasteland" **(verified, RAM for the size)** | I J K L | the Ranger Center is at x55 y62, Highpool at x47 y59 **(RAM)** | playbook RAM map | `map_mountain`, `map_edge`, `env_world_valley` | shown |
| World and navigation | Terrain hazards | river squares carry the party along and hurt each ranger for 1 CON ("You are caught by the river's current") **(verified, `world_river_current`)** | | 1 damage per ranger | | `world_river_current` | shown |
| World and navigation | Locations | stepping on a location icon asks "Enter new location (Y/N)?"; N puts the party back on the square it came from **(verified at the Ranger Center)**; buildings inside a town are separate small locations (shop, infirmary) or walk-in interiors (store, workshop) **(verified)** | Y/N | entry loads about 1600 frames (30 s) from disk **(verified)** | | `loc_agcenter`, start set `37_highpool_prompt`, `hp_store_entry`, `hp_workshop` | shown |
| World and navigation | Square descriptions | many squares print a description when stepped on (dorm, store entry, machinery, pump, creek) **(verified)** | | | | `hp_dorm`, `hp_workshop_parts`, `hp_workshop_pump`, `hp_creek_wade` | shown |
| Goals and gating | Town events | the Highpool creek's slippery rocks dunk the party and call a laughing kid; a note in the store lists the town's problems (cave, outlaws, Jackie, Bobby's dog) **(verified)**; the cave, Jackie and the Red Ryder follow **(source)** | | | | `hp_creek_slip`, `hp_creek_kid`, start set `45_wall_note` | shown |
| Chance | Rolls | attributes at creation, encounters, hits and damage are random; the frame timing of the keys decides them in the emulator **(verified)** | SPACE rerolls | | | `rc_reroll` | shown |
| Chance | Encounter rate | random encounters come while walking or waiting: one after 1000 idle frames in one run, after 10000 in another **(verified)** | | | | `battle_appears` | shown |
| Failure and recovery | Unconscious and death | rangers fall unconscious at 0 CON; a doctor heals for money; the whole party lost was not reached (game over open) **(verified for UNC)** | | | | `battle_radrat`, `hp_infirmary_exam` | described |
| Saving and sessions | Disk saves | Save asks "Save game (Y/N)?" and writes the party to play side 1 (about 3000 frames); Continue = Y at "Use last saved game" puts the party back where it saved **(verified, `field_save`, `save_load`)** | S, Y | | | `field_save`, `menu_continue`, `menu_insert_side`, `save_load` | shown |
| Saving and sessions | Play disks | the game refuses its master disks as play disks; Utils makes copies **(verified)** | U, C | | playbook | `title_utils` | shown |
| Pacing and difficulty | Clock | a clock in the frame's top right advances about 4 minutes per step or per 20 s of waiting **(verified: 1:52 -> 2:36 over 11 waits of 1000 frames)** | | | | `world_start` | shown |
| Pacing and difficulty | First hours | the first fight outside the Ranger Center can knock a ranger unconscious; the party starts with no money for the doctor **(verified, start set)** | | | | start set `34_battle_hurt`, `47_infirmary_price` | shown |

## 3. How the systems feed each other
- Fights -> experience (and loot, source) -> ranks and skill points (source) -> better fights.
- Fights -> lost CON -> the doctor -> money; money also buys shop items (tools such as the Crowbar or Rope open
  doors and caves, source).
- Skills -> map actions (Perception finds hidden things, Climb passes rubble, source) -> town events -> items.
- Time -> random encounters.

## Open questions
- Game over (whole party down) not reached: four CON 1 rangers against 3 Animals stayed alive through four rounds.
- Rank and level-up rules, loot after fights, the Hire success rule.
- What View does beyond redrawing the map; Radio's use.
