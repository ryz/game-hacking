# Ultima II: The Revenge of the Enchantress (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only; one letter per command, no confirmation; directions with the arrow keys; numbers
  typed as digits (generation, offers, hyperwarp coordinates) (verified). A wrong key: "--ILLEGAL COMMAND!"
  (ROM text) or the command's own refusal ("BOARD WHAT?", "HYPER WHAT?") (verified).
- **Layout:** graphics screen 320x200: map view 20 x 10 squares above, the four-line command log bottom left,
  the status panel (H.P., FOOD, EXP., GOLD) bottom right (verified). Text screens (40 columns) for the menu,
  generation and Ztats (verified). Space: a star field with FUEL, XENO, YAKO, ZABO in the panel (verified).
- **Text:** capitals in the game's own messages; the talk lines from the TLK files are mixed case ("You have
  earned my blessing.") (verified). Place names are drawn into the town maps as letter tiles ("TOWNE LINDA",
  "NEW SAN ANTONIO", "LORD BRITISH", "CCCP TEST LAUNCH", "OZYS PLACE", "CHAMBER ONE") (verified).
- **Feedback:** every command echoes "CMD: NAME" and its result on the next line; results are short shouts
  ("HIT!!!", "SHE'S GONE!!!"); nothing asks for confirmation except generation's "SATISFACTORY (Y/N)" (verified).
- **State visibility:** the four numbers are always on screen; everything else (level, statistics, equipment,
  items) only on Ztats (verified). The period is shown only by signs ("ANOS: 1423 B.C.") (verified).
- **Help and onboarding:** the demonstration's captions; the rest is in the manual (not available here).

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Intro text | transition | power-on -> title | credits | "ORIGIN PROUDLY PRESENTS", "PART ][ ..." | none | timed | planned `boot_*` | |
| Title picture | screen | intro -> menu | name of the game | dragon head, "Ultima II Revenge of the Enchantress" | none | timed, about 1.5 s | `title_screen` | |
| Main menu | menu | title -> demo, generation, play | choose | D, P, C | `d` `p` `c` | | `menu_main` | |
| Demonstration | screen | menu `d` -> pictures -> title | advertise | six pictures with captions | none | timed | planned `cutscene_demo_*` | |
| Player generation | screen | menu `c` -> menu | make the hero | points left, six statistics, M/F, race, type, name, lists of races and types | digits, Enter, letters | form cleared on a value under 10 | `menu_generation` | **Observation:** the clearing has no message |
| Surface view | screen | play -> places, space | travel | map, hero, monsters, vehicles, doors | arrows and commands | "INVALID MOVE!" | planned `gameplay_start` | |
| Command log | hud element | always | history of the last three commands | "CMD: ..." lines | | scrolls up | planned `hud_status` | |
| Status panel | hud element | always | H.P., FOOD, EXP., GOLD | four numbers, four digits | | redrawn every turn | planned `hud_status` | |
| Town view | screen | `e` -> walk off the edge | trade and talk | walls, counters, people, the town's name in letters | arrows, `t`, `o`, `s`, `u` | | planned `gameplay_linda` | |
| Shop dialogue | prompt | `t` at a counter | buy | offer text, numbered list or price, Y/N | digits, Y/N | "YOU DONT HAVE THAT MUCH!", "THANKS FOR COMING BY..." | planned `shop_*` | |
| Talk line | message | `t` at a person | clues | "A GUARD SAYS: PAY YOUR TAXES!" or a TLK line | | | planned `dialogue_*` | |
| Offer prompt | prompt | `o` | give gold | "OFFER GOLD DIRECT-", "HOW MUCH (*100) ?" | direction, digit | "YOU DONT HAVE THAT MUCH!" | planned `system_enilno` | |
| Ztats | screen | `z` -> any key | character sheet | level, race, type, equipment, torches/keys/tools, statistics, owned lists | any key | | planned `inventory_ztats_*` | |
| Ready / Wear lists | prompt | `r`, `w` | equip | numbered abbreviations ("1-DA, 2-MA ...") | digit | "NOT OWNED!", "THOU ART NOT AGILE ENOUGH TO WIELD!" | planned `system_cmd_r` | |
| Dungeon view | screen | `e` on a dungeon or tower | explore | wireframe corridor, ladders | arrows, `k`, `d`, `i` | "IT'S DARK!", "-BLOCKED!" | planned `gameplay_dungeon_*` | |
| Space view | screen | `l` in a rocket | fly | star field, sight, FUEL/XENO/YAKO/ZABO | `h`, digits, `l` | "REQUEST DENIED!", "YOU HIT THE SUN!", "YOU HAVE EXPLODED!" | planned `gameplay_space_earth` | |
| Landing drift | screen | `l` in orbit -> planet surface | choose a landing square | planet map scrolling under the rocket, "(PRESS ANY KEY)" | any key | crash off grass (code) | planned `system_landing` | |
| Ending text | screen | Minax killed | the end | message over a scrolling world | none | endless | planned `ending_text` | |

## 3. Screen flow
- power-on -> intro text -> title picture -> main menu
  - `d` -> demonstration -> title picture -> menu
  - `c` -> player generation -> menu
  - `p` -> surface view (period saved in the character)
    - `e` -> village / towne / castle view -> walk off the edge -> surface
    - `e` -> dungeon / tower view -> ladder out -> surface
    - time door -> surface of another period
    - rocket `l` -> space view -> `h` hyperwarp -> `l` -> landing drift -> planet surface (or, on Earth, 2112)
    - `z` -> Ztats -> back; `q` -> save, play continues
    - Minax killed -> ending text (no way back)
(verified for every arrow except dungeon ladders out)

## 4. Elements in detail
- **Surface view** (verified): 20 x 10 squares of 16 x 16 pixels, the hero always in column 10, row 6; terrain
  water (magenta dots), grass (cyan dots), woods (cyan blobs), mountains (white zigzags); places, signs, doors
  and vehicles are single pictures. The view changes only on a turn.
- **Status panel** (verified): four lines "H.P.=0400", "FOOD=0399", "EXP.=0000", "GOLD=0400", four digits each.
- **Command log** (verified): the last commands and their results, scrolling one line per message.

## Open questions
- Shop screens for armour, weapons, food, spells and the oracle; the View command with a helm; the plane's
  flight screen; the death screen.
