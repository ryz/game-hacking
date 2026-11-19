# Ultima II: The Revenge of the Enchantress (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima-2`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only; one letter per command, no confirmation; directions with the arrow keys; numbers
  typed as digits, two per statistic in generation, one (hundreds) for gold offers, one per hyperwarp
  coordinate (verified). A command with nothing to act on answers with its own refusal ("BOARD WHAT?", "HYPER
  WHAT?") (verified: `gameplay_refusals`, `gameplay_refusals_2`, `gameplay_refusals_3`).
- **Layout:** CGA 320 x 200, four colours: the map view (20 x 10 squares of 16 x 16 pixels, ryz in the middle)
  above, the four-line command log bottom left, the status panel (H.P., FOOD, EXP., GOLD) bottom right
  (verified: `hud_status`). Text screens of 40 columns for the menu, generation and Ztats (verified:
  `menu_main`, `menu_generation`, `inventory_ztats_late`). In space the panel shows FUEL, XENO, YAKO, ZABO
  (verified: `gameplay_space_earth`).
- **Text:** capitals in the game's own messages; the talk lines from the TLK files are mixed case ("You have
  earned my blessing.") (verified: `dialogue_father_antos`). Place names are drawn into the town maps as large
  letter tiles ("TOWNE LINDA", "NEW SAN ANTONIO", "CCCP TEST LAUNCH", "CHAMBER ONE") (verified).
- **Feedback:** every command echoes "CMD: NAME" and its result on the next line; results are short shouts
  ("HIT!!!", "SHE'S GONE!!!"). Only generation asks "SATISFACTORY (Y/N)"; shops ask "HOW 'BOUT IT?" (verified).
  A strong spell inverts the screen colours for a moment (seen once in Legends).
- **State visibility:** the four numbers are always on screen; level, statistics, equipment and items only on
  Ztats; the period only on signs ("ANOS: 1423 B.C.") (verified).
- **Help and onboarding:** the demonstration's captions; the rest is in the manual (not available here).
  **Observation:** the period is never shown on the main screen, and the 1423 B.C., 1990 and 2112 maps share
  their coasts (compare `system_sign_1990` and `system_sign_2112`), so a player who just stepped through a time
  door has to find a sign or a town to know where (when) he is.

## 2. Screen inventory
| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Intro text | transition | power-on -> title | credits | "ORIGIN PROUDLY PRESENTS", "PART ][ ..." | none | timed | `boot_origin`, `boot_part2` | |
| Title picture | screen | intro -> menu | name of the game | dragon head, "Ultima II Revenge of the Enchantress" | none | timed, about 1.5 s | `title_screen` | |
| Main menu | menu | title -> demo, generation, play | choose | D, P, C | `d` `p` `c` | | `menu_main` | |
| Demonstration | screen | menu `d` -> pictures -> intro | advertise | five pictures with captions (the castle picture of the kings caption is missing from this release) | none | timed, about 150 frames each | `cutscene_demo_creatures`, `cutscene_demo_pub`, `cutscene_demo_dungeons`, `cutscene_demo_space`, `cutscene_demo_minax` | |
| Player generation | screen | menu `c` -> menu | make the hero | points left, six statistics, M/F, race, type, name, lists of races and types | digits in pairs, letters | form cleared silently on a value under 10 | `menu_generation`, `menu_gen_stats`, `menu_gen_male`, `menu_gen_human`, `menu_gen_done`, `menu_gen_other` | **Observation:** the bonuses appear in the numbers as each choice is made, a clear way to show them |
| Surface view | screen | play -> places, space | travel | map, ryz, monsters, vehicles, doors | arrows and commands | "INVALID MOVE!" | `gameplay_start`, `gameplay_blocked`, `gameplay_surface_pangea` | |
| Command log | hud element | always | the last four lines of commands and answers | "CMD: ..." lines | | scrolls up; a long answer pushes the command line out | `hud_status`, `system_cast_none` | **Observation:** with two-line answers the command itself scrolls away (`system_cast_none` shows only the answers) |
| Status panel | hud element | always | H.P., FOOD, EXP., GOLD | four numbers, four digits; magenta zeros at death | | redrawn every turn | `hud_status`, `gameover_dead` | |
| Sign | message | `e` on a sign | name the period | "THE SIGN READS: ANOS: ..." | | | `system_sign_1423`, `system_sign_legends` | |
| Town view | screen | `e` -> walk off the edge | trade and talk | walls, counters, people, the town's name in letters | arrows, `t`, `o`, `s`, `u` | | `gameplay_linda`, `gameplay_village_1423`, `gameplay_castle_lb`, `gameplay_towne_mary` | |
| Shop dialogue | prompt | `t` across a counter | buy | offer text, numbered list or price, Y/N | digits, Y/N | "YOU DONT HAVE THAT MUCH!", "THANKS FOR COMING BY..." | `shop_weapons`, `shop_weapons_price`, `shop_armour`, `shop_pub`, `shop_food`, `shop_food_buy`, `shop_transport`, `shop_oracle` | **Observation:** the prices only appear after choosing an item, never as a list |
| Talk line | message | `t` at a person | clues, jokes | "A GUARD SAYS: PAY YOUR TAXES!" or a named person's line | | "FUNNY, NO RESPONSE!" | `dialogue_guard`, `dialogue_santre`, `system_unlock_transact` | |
| Offer prompt | prompt | `o` | give gold | "OFFER GOLD DIRECT-", "HOW MUCH (*100) ?" | direction, digit | "OFFER TO WHOM?", "THANK YOU VERY MUCH!" | `system_offer_steal`, `system_offer_thanks`, `system_enilno` | |
| Ready / Wear lists | prompt | `r`, `w` | equip | numbered abbreviations ("1-DA, 2-MA ...") | digit | "NOT OWNED!", "THOU ART NOT AGILE ENOUGH TO WIELD!", "...STRONG ENOUGH TO WEAR!", "SWORD READY." | `system_ready_list`, `system_wear_list`, `system_agile_refused`, `system_strong_refused`, `system_ready_weapon`, `system_wear_armour` | |
| Magic ready | prompt | `m` | choose the spell for C | "MAGIC SPELL READY #", "SPELL READY => LIGHT" | digit | | `system_magic_ready` | |
| Ztats | screen | `z` -> any key | character sheet | level, sex, race, type, readied weapon / armour / spell, torches, keys, tools, statistics, owned lists | any key | | `inventory_ztats_new`, `inventory_ztats_late` | |
| Helm view | screen | `v` with a helm | the whole map | the 64 x 64 Earth map as dots | any key | "VIEW WHAT?" without a helm | `system_view_helm`, `gameplay_refusals_3` | |
| Dungeon view | screen | `e` on a dungeon or tower | explore | wireframe corridor, doors, ladders, chests, creatures | arrows, `k`, `d`, `i`, `a`, `g`, `c` | "IT'S DARK!" (nothing drawn), "-BLOCKED!" | `gameplay_dungeon_dark`, `gameplay_dungeon`, `gameplay_dungeon_turn`, `gameplay_dungeon_door`, `gameplay_tower` | |
| Vehicle views | screen | `b` -> `x` | travel | ryz drawn as a horse, frigate, plane or rocket | arrows, `f`, `l` | "LAND--NOT HERE!!!!!" | `gameplay_horse`, `gameplay_frigate`, `gameplay_plane` | |
| Space view | screen | `l` in a rocket | fly | star field and sight, FUEL/XENO/YAKO/ZABO | `h`, digits, `l`, arrows | "REQUEST DENIED!", "YOU HIT THE SUN!", "YOU HAVE EXPLODED!" | `gameplay_space_earth`, `system_hyperwarp_prompt`, `system_deep_space` | |
| Hyperwarp tunnel | transition | launch or `h` -> orbit | travel | white rays from the centre | none | "HYPERWARP ENGAGED!" | `cutscene_launch`, `system_hyperwarp` | |
| Landing drift | screen | `l` in orbit -> planet surface | choose a landing square | planet map scrolling under the rocket, "(PRESS ANY KEY)" | any key | crash off grass (code) | `system_landing` | **Observation:** the landing square is chosen by timing a key press over a moving map |
| Death | message | H.P. 0 -> nothing | end | "RYZ IS DEAD!" alone, panel zeros in magenta | none | the program stops | `gameover_dead` | **Observation:** no prompt, no menu: the player must restart the computer |
| Ending text | screen | Minax killed | the end | message over a scrolling world | none | endless | `ending_text` | |

## 3. Screen flow
- power-on -> intro text -> title picture -> main menu
  - `d` -> demonstration -> intro text -> title -> menu
  - `c` -> player generation -> menu
  - `p` -> surface view (period saved in the character)
    - `e` -> village / towne / castle view -> walk off the edge -> surface
    - `e` -> dungeon / tower view -> ladder out (or Surface spell) -> surface
    - time door -> surface of another period
    - `b` on a vehicle -> the vehicle on the same map; plane: `l` flies, `l` lands
    - rocket `l` -> space view -> `h` hyperwarp -> `l` -> landing drift -> planet surface (or, on Earth, 2112)
    - `z` -> Ztats -> back; `v` (helm) -> world map -> back; `q` -> save, play continues
    - death -> "RYZ IS DEAD!" (stop); Minax killed -> ending text (no way back)
(verified for every arrow)

## 4. Elements in detail
- **Surface view** (verified): 20 x 10 squares of 16 x 16 pixels, ryz always in column 10, row 6; terrain water
  (magenta dots), grass (sparse cyan dots on black), woods (cyan blobs), mountains (white zigzags); places,
  signs, doors and vehicles are single pictures. The view changes only on a turn.
- **Status panel** (verified): four lines "H.P.=0400", "FOOD=0399", "EXP.=0000", "GOLD=0400", four digits each.
- **Command log** (verified): the last four lines, scrolling one line per message.

## Open questions
- The text of the "PLEAD WITH MEDIEVAL KINGS" demonstration picture never shows (its picture file is missing).
