# WASTELAND - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only; cursor keys and joystick do nothing on the map **(verified)**. Commands are the first
  letter of the word in the command bar (the letter is highlighted); lists are chosen by number (`1>` ... `9>`);
  yes/no prompts take Y or N; the C64 left-arrow key is Esc (cancel, close a window) **(verified)**. Keys
  pressed while the disk loads or a screen draws are lost **(verified: routes need 200-300 frame waits)**.
- **Layout:** one fixed frame: a large window top left (map, or a portrait on encounter, shop and doctor
  screens), a text window top right that covers the map when open, the clock in the top border, the roster of
  up to seven rangers below, two message lines and the command bar at the bottom **(verified, `world_start`,
  `hp_shop`)**.
- **Text:** upper-case-looking C64 font with lower case; names typed in upper case only **(verified)**; the
  command bar is shown inverted, the active command letter in normal video **(verified, `field_use`)**.
- **Feedback:** each square stepped on may print a line in the message area; messages scroll upward; long
  messages and round reports wait for RETURN (`[RETURN]`) **(verified, `battle_appears`, `hp_creek_wade`)**.
  Irreversible steps ask first: delete a ranger, keep a character, save, enter a location, use the round's
  orders **(verified)**.
- **State visibility:** the roster always shows AC, AMM (rounds loaded), MAX and CON per ranger and the weapon
  in hand; UNC replaces CON for an unconscious ranger **(verified, `battle_radrat`)**. Money, attributes and
  skills need the character sheet (digit key) **(verified, `char_stats`)**. Position is never shown as numbers.
- **Help and onboarding:** none in the game; the manual and the paragraph book carry the story (source).

## 2. Screen inventory
| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Loading globe | transition | power-on -> title | credits while side 1 loads | Earth globe, EA and Interplay credits, logo | nothing | | `boot_globe` | |
| Title | screen | loading -> Start / Utils | choose to play or to copy disks | Place EARTH, Year 1998, Status DEFCON 1 typed over the globe | S, U | | `title_screen` | **Observation:** the lines keep typing, so the title never stands still |
| Utils | menu | title -> Copy, Restart, Start | make play copies of the four sides | menu bar only, empty window | C, R, S | | `title_utils` | |
| Use last saved game | prompt | Start -> insert side | continue or start over | one line under the title | Y, N | | `menu_continue` | |
| Insert side | prompt | continue -> world map | ask for a play disk | "Insert side 1. [RETURN]"; the same line under the map when a location on another side is entered, and twice during a save in a town (side 1, then the town's side) | RETURN | a master disk is refused and asked again **(verified)** | `menu_insert_side`, `menu_insert_side2`, `menu_insert_side3`, `menu_insert_side4`, `save_town` | |
| Ranger Center | screen | entering the Ranger Center -> Create, Delete, Start | manage the party | building picture, roster, empty text window | C, D, S | Create with four rangers asks to delete first **(verified)** | `rc_roster`, `rc_party` | |
| Create a character | screen | Create -> name | roll the attributes | seven attributes, skill points, rank, MAXCON, money | SPACE, RETURN | | `rc_roll`, `rc_reroll` | |
| Name, sex, nationality | prompt | roll -> skills | identity | "Enter name", "Enter sex (M/F)", list of five nationalities | text, M/F, 1-5 | | `rc_nation` | |
| Skill purchase | list | nationality -> keep | spend skill points | points left; per skill minimum IQ, cost, level | digit, RETURN | | `rc_skills` | **Observation:** the columns are unlabelled except by a header line that is hard to read |
| World map | screen | Start, leaving a location -> everything | travel | 18 by 7 squares around the party, roster (SPACE toggles), clock | I J K L, command letters, digits | blocked moves print a line | `world_start`, `world_full`, `env_world_valley` | |
| Character sheet | screen | digit -> RETURN pages | ranger details | page 1 attributes, CON, rank, money, sex, nationality; page 2 items; page 3 skills | RETURN, Esc | | `char_stats`, `char_items`, `char_skills` | |
| Use prompts | prompt | U -> ranger -> Item/Skill/Attribute -> list -> direction | use something on a square | "Which player?", "Use: Item Skill Attribute?", skill list, "Which way?" with I J K L around SPACE | digits, letters, direction | "You see nothing special." | `field_use`, `field_use_kind`, `field_use_skill`, `field_which_way`, `field_perception` | **Observation:** the direction prompt draws the keys as a compass, a neat reminder |
| Enc prompt | prompt | E | start a battle round when not attacked | explanation and (Y/N) | Y, N | | `field_enc` | |
| Disband, Radio, Save | prompt | D, R, S | leave a ranger, radio the Ranger Center, save | one question each | digit or Y/N | | `field_disband`, `field_radio`, `field_save` | |
| Map messages | message | stepping | blocked moves, edges, terrain | one or more lines above the command bar | | | `map_mountain`, `map_edge`, `world_river_current` | |
| Enter new location | prompt | stepping on an icon -> location | confirm entry | "Entering <name>." plus (Y/N) window | Y, N | N steps back | `loc_agcenter` | |
| Square description | message | stepping in a location | describe the place | two or three lines | | | `hp_dorm`, `hp_store_entry`, `hp_workshop_parts`, `hp_workshop_pump`, `hp_creek_wade` | |
| Shop | screen | shop square -> Buy/Sell | trade | storekeeper portrait, "Who wants to enter?", then Buy or Sell, then the list with Pool Money | digit, B, S, digit | the pool money changes at once | `hp_shop`, `hp_shop_buysell`, `hp_shop_buy`, `hp_shop_bought`, `hp_shop_sell` | |
| Infirmary | screen | infirmary square -> treatment | heal | doctor portrait, "Who wants treatment?", then the recommendation with prices | digit | | `hp_infirmary`, `hp_infirmary_exam` | |
| Encounter | message | random -> combat | announce the enemy | group size and distance in feet, [RETURN] | RETURN | | `battle_appears` | |
| Combat orders | menu | encounter -> confirm | one order per ranger | enemy portrait and name, "<ranger>, choose:" with seven orders | R U H E A W L | | `battle_menu`, `battle_weapon`, `battle_use`, `battle_hire` | |
| Use these options | prompt | orders -> round | confirm the round | (Y/N) | Y, N | | `battle_confirm` | |
| Round report | message | confirm -> next round or result | play out the round | scrolling lines: attacks, hits, damage, kills, experience | RETURN at the end | | `battle_round`, `battle_xp`, `battle_radrat` | **Observation:** older lines scroll out of the window before the [RETURN] stop, so a long round cannot be read back |
| Clock | hud element | always | game time | hours:minutes in the top border | | | `world_start` | |
| Roster | hud element | always (map: SPACE toggles) | party state | number, name, AC, AMM, MAX, CON, weapon | digit | UNC for unconscious | `world_start`, `battle_radrat` | |
| Town map | screen | entering a town -> streets, buildings | walk a town | the same window as the world map, 16-pixel squares: houses as purple and blue blocks, walls as white lines | I J K L, command letters | "Ouch!" for a wall | `qz_arrival`, `env_qz_houses`, `env_qz_park`, `vg_arrival`, `env_vg_streets`, `env_vg_golf`, `dw_arrival`, `env_dw_village`, `nd_arrival`, `env_nd_walls`, `env_nd_railway` | |
| Interior map | screen | walk-in building | rooms | brick walls, doors, tables, ovens, people as figures | I J K L | | `ct_arrival`, `env_ct_hall`, `sl_arrival`, `env_sl_halls`, `cb_arrival` | |
| Street sign | message | street corner | orientation | "N-S <street> / E-W <street>" | | | `qz_street_sign` | **Observation:** the only orientation aid in towns; there is no automap |
| Building prompt | prompt | door square -> sub-location | confirm entry with a line of flavour | "Entering the Vegas Hospital where the rich get well, and the poor die young." + (Y/N) | Y, N | | `vg_hospital`, `vg_casino_door`, `dw_black_market`, `dw_library`, `dw_jekyll`, `nd_waste_pit` | |
| Description on stepping (later towns) | message | stepping | flavour, hints | two to four lines; some end in [RETURN] | RETURN | | `qz_manhole`, `qz_shop_closed`, `qz_stagecoach`, `qz_scotts_bar`, `vg_golf_pond`, `ct_grand_hallway`, `ct_wall_writing`, `ct_ovens`, `dw_lab`, `dw_delicious`, `sl_debris`, `sl_shining`, `sl_door_slot` | |
| Text entry | prompt | talking to a guard | type a word | the speaker's line and a ">" cursor | typed text, RETURN | | `dw_password` | |
| Store (trader) | screen | store door -> Buy/Sell | trade | trader portrait with the shop's name, "Who wants to enter?" | digit | | `dw_store` | |
| Fixed encounter | message | event square -> combat | announce a set fight | flavour line, then each named member or group with distance in feet, [RETURN] | RETURN | | `qz_ghouls`, `vg_warroids`, `vg_scorpitron`, `vg_cyborgs`, `vg_freddy`, `vg_glowing`, `vg_death_machines`, `ct_brother_austin`, `ct_guardians`, `ct_chef`, `ct_museum`, `ct_sisters`, `sl_wolves`, `cb_weapon_pod`, `cb_plasma`, `cb_robots`, `cb_gate_robots` | |
| World map hazards | screen | world map | show danger | yellow radiation symbols round Darwin | | | `env_world_radiation` | |

## 3. Screen flow
```
power-on -> loading globe -> title -(U)-> Utils
                               -(S)-> Use last saved game? -> Insert side 1 -> world map
world map -(step on icon, Y)-> location map (town) -(step on building)-> interior / shop / infirmary
world map -(Ranger Center, Y)-> Ranger Center -(C)-> create -> name -> sex -> nationality -> skills -> keep?
                                              -(S)-> world map
world map -(random)-> encounter -> orders per ranger -> Use these options? -> round report -> ... -> map
world map -(digit)-> character sheet: stats -> items -> skills -> map
world map -(S, Y)-> saved, map
world map -(icon on another side, Y)-> Insert side N -> RETURN -> location map
location -(S, Y)-> Insert side 1 -> Insert side N (the location's) -> map
```

## 4. Elements in detail
- **World map window** (`world_start`): the party is a single figure in the centre; location icons are drawn
  pictures (Highpool's figure and pool, the Agricultural Center's sign); mountains are white-capped ridges,
  lakes blue, the area beyond the map edge red **(verified)**.
- **Roster** (`world_start`): `1>` to `4>` (up to seven); the leader's number is highlighted when a ranger is
  asked to choose **(verified, `battle_menu`)**.
- **Combat window** (`battle_menu`): the portrait replaces the map and names the group (Animals, Wild Canine,
  Radioactive); the orders list uses the first letter as the key **(verified)**.
- **Shop list** (`hp_shop_buy`): Pool Money at the top, then `$$$` and ITEM columns, nine lines, a `MORE:`
  prompt at the bottom **(verified)**.

## Open questions
- What MORE: in the shop list accepts (RETURN did not page).
- Utils Copy and Restart screens; View's purpose.
