# Ultima I: The First Age of Darkness (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact. Shot ids are the playbook's planned ids.

## 1. Conventions
- **Input:** keyboard only; one letter per command, the command's initial (A)ttack, (B)oard, (C)ast ... (Z)tats;
  arrows move; space passes or continues; menus are lettered `a)`-`f)` and chosen by letter; numbers choose the
  character slot; Enter ends the name **(verified)**. Unknown keys answer "Huh?" **(verified)**.
- **Layout:** 320x200 EGA. Play screen: map window (19x9 squares outdoors, the whole town or castle in one
  window, a first-person view in dungeons) inside a blue frame; message log bottom left (four lines, newest at
  the bottom, prompt `>`); status panel bottom right (Hits, Food, Exp., Coin; in space Shld, Fuel) **(verified)**.
  Dungeon frame: "Level N" on top, facing on the bottom edge **(verified)**.
- **Text:** one capital-and-small-letter bitmap font, cyan on black for messages and menus, white for titles
  and the ending text; red for readied items in Ztats and for low values in the status panel **(verified)**.
  Archaic English ("Thou hast", "Dost thou") throughout **(verified)**.
- **Feedback:** every key echoes its command name in the log ("North", "Pass", "Ztats"); results follow on the
  next line ("Missed!", "Hit! 2 damage!"); larger texts open a framed box over the map with "Press Space to
  continue" **(verified)**.
- **State visibility:** hits, food, experience and coin always shown; everything else in Ztats; place name only
  on entry and with Inform **(verified)**.
- **Help and onboarding:** none in the game beyond the creation screen's instructions and the pub tips; commands
  are in the manual **(verified / source)**.

## 2. Screen inventory
| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Text title | screen | power-on -> Origin logo | name and copyright | "Ultima I / The First Age of Darkness" | any key -> credits | | `boot_title_text` | |
| Origin logo | transition | title -> castle | publisher | animated logo, captions | any key | | `boot_origin` | |
| Castle picture | title | -> loop | title art | "Ultima I" over a castle | any key | | `title_castle` | |
| Credits card | screen | any key -> main menu | trademarks, conversion credit | | | | `boot_credits` | |
| Main menu | menu | -> GEN / selection | start | a) Generate new character b) Continue previous game | a, b | | `menu_main` | |
| Character Generation: points | menu | a -> race | spend 30 points | six statistics with cursor arrows, points left, instructions | up/down/left/right, space, esc | values stop at 0 points left | `gen_points`, `gen_stats_done` | **Observation:** the only screen with on-screen instructions |
| Race / sex / class | menu | -> name | choices | lettered lists, chosen values listed above | a-d | | `gen_race`, `gen_class` | |
| Name, save | prompt | -> main menu | name, confirm | "Enter thy name:", "Save this character? (Y-N)" | letters, enter, y/n | | `gen_save` | |
| Character Selection | list | b -> overworld | pick slot | 1)-4) names | 1-4, esc | | `menu_select` | |
| Overworld view | screen | | play | map, player, monsters, vehicles | all commands | | `start_overworld` | |
| Message log | hud element | always | history and prompts | four lines | | | `hud_status` | |
| Status panel | hud element | always | vital numbers | Hits, Food, Exp., Coin | | values change colour when low (red) | `hud_status` | **Observation:** not redrawn after outside changes (seen with pokes) |
| Ztats | screen | z -> back | inventory | player line, statistics, coins, armour, weapons, spells, vehicles, gems, enemy vessels | space | | `inventory_ztats`, `inventory_ztats_late` | |
| Town / castle view | screen | e on the overworld -> walk off the edge | town play | whole map, signs ARMOUR, WEAP, FOOD, MAGIC, PUB, TRANSPORT, PRISON | commands | | `gameplay_britian`, `gameplay_castle` | |
| Shop box | menu | t at a counter | buy/sell | shop name, lettered goods with prices | b/s, letters | "Sold!", "Thou canst not afford it!", "Thou art not by a counter!" | `shop_*` | |
| King box | dialogue | t beside the king | quests, hit points | "Dost thou offer pence or service:", quest text | p/s, amounts | "Thou art on a quest for me already!" | `dialogue_king_*` | |
| Landmark box | message | e on a landmark | text and reward | inscription | space | | `system_landmark_grave` | |
| Dungeon view | screen | e on a dungeon | first-person | wireframe corridor, chest, monster, Level, facing | arrows, commands | | `gameplay_dungeon`, `battle_skeleton` | |
| Lift-off countdown | message | b on a shuttle | | "10..9..8..", "Thou hast lifted off!" | | | `system_liftoff` | |
| Space top view | screen | | flight | sector with planet, sun, starbase, ship; Shld, Fuel | arrows, commands | | `gameplay_space_top` | |
| Sector Scan | map | i in space | the 7x7 sectors | symbols per sector | | | `map_sector_scan` | |
| Space front view | screen | v | combat view | stars, enemies | | | `gameplay_space_front`, `battle_space` | |
| Death | screen | 0 hits | | skull, "thou art dead", "Attempting resurrection!" | | | `gameover_dead` | |
| Time machine boxes | cutscene | b on the time machine | story | four pages, gem holes R G B W | space | | `cutscene_*` | |
| Mondain's chamber | screen | | final fight | time machine, player, gem, Mondain | arrows, a, g | | `boss_*` | |
| Victory box | message | Mondain at 0 | | "THOU ART VICTORIOUS!" | space | | `ending_victorious` | |
| Ending text | screen | | epilogue | three paragraphs, "Press CONTROL-ALT-DEL to Restart" | none | | `ending_text` | |

## 3. Screen flow
- power-on -> text title -> Origin logo -> castle picture -> (loop) ; any key -> credits -> main menu
  - a -> Character Generation (points -> race -> sex -> class -> name -> save) -> main menu
  - b -> Character Selection -> overworld
- overworld <-> towns / castles (e; leave by the edge) <-> shops, king boxes
- overworld <-> dungeons (e; ladders up out) ; overworld <-> landmarks (e, box)
- overworld -> shuttle (b) -> space (top/front view, sector scan, starbases) -> landing -> overworld
- overworld -> time machine (b, four gems) -> four boxes -> Mondain's chamber -> victory -> ending text
**(verified except dungeon exits and starbases)**

## 4. Elements in detail
- **Play screen:** blue frame; map window 304x144 pixels (19x9 squares of 16 pixels outdoors; 8-pixel squares
  in towns so the whole town fits); log 4 lines at the bottom left; panel at the bottom right **(verified)**.
- **Status panel:** Hits, Food, Exp., Coin right-aligned four-digit numbers; in space Shld and Fuel replace Hits
  and Food **(verified)**.

## Open questions
- Starbase screens, ship choice, the pub's wench/lecher boxes, dungeon ladder messages.
