# Ultima I: The First Age of Darkness (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact. Shot ids are those of set `main`.

## 1. Conventions
- **Input:** keyboard only; one letter per command, the command's initial: (A)ttack, (B)oard, (C)ast, (D)rop,
  (E)nter, (F)ire, (G)et, (H)yperJump, (I)nform, (K)-limb, (N)oise, (O)pen, (Q)uit, (R)eady, (S)teal,
  (T)ransact, (U)nlock, (V)iew, (X)-it, (Z)tats; arrows move (in dungeons forward and turn; in space thrust,
  retro and rotate); space passes or continues; lettered lists are chosen by letter; amounts are typed and ended
  with Enter **(verified)**. Unknown keys answer "Huh?" and commands without a target echo their name with a
  question mark ("HyperJump?", "Steal?") (`gameplay_refusals`) **(verified)**.
- **Layout:** 320x200 EGA. Play screen: a map or view window inside a blue frame (grey riveted frame in space);
  message log bottom left, four lines, newest at the bottom with the prompt `>`; status panel bottom right
  (`hud_status`) **(verified)**.
- **Text:** one bitmap font; cyan for messages and menus, white for names and titles, red for readied items in
  Ztats and for dangerously low numbers in the status panel (`gameover_dead`) **(verified)**. Archaic English
  ("Thou hast", "Dost thou") throughout.
- **Feedback:** every key echoes its command name in the log ("North", "Pass", "Ztats"); the result follows on the
  next lines ("Missed!", "Hit! 2 damage!"); longer texts open a framed box over the map that stays until a key
  ("Press Space to continue") **(verified)**.
- **State visibility:** hits, food, experience and coin always shown (in space shield and fuel replace hits and
  food); everything else in Ztats; place names on entry and with Inform **(verified)**.
- **Help and onboarding:** on-screen instructions only in character generation; pub tips are the in-game hints
  **(verified)**.

## 2. Screen inventory
| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Text title | screen | power-on -> Origin logo | name and copyright | "Ultima I / The First Age of Darkness", Copyright 1987 | any key -> credits | | `boot_title_text` | |
| Origin logo | transition | title -> castle | publisher | logo drawn line by line, three captions | any key | | `boot_origin`, `boot_presents`, `boot_new_release`, `boot_masterpiece` | |
| Castle picture | title | -> loop | title art | "Ultima I" over a castle | any key | | `title_castle` | |
| Credits card | screen | any key -> main menu | trademarks, conversion credit | | | | `boot_credits` | |
| Main menu | menu | -> GEN / selection | start | a) Generate new character b) Continue previous game | a, b | | `menu_main` | |
| Character Generation: points | menu | a -> race | spend 30 points | six statistics, cursor arrows, points left, instructions | up/down/left/right, space, esc | values stop at 0 points left | `gen_points`, `gen_stats_mid`, `gen_stats_done` | **Observation:** the only screen with on-screen instructions |
| Race / sex / class | menu | -> name | choices | lettered lists, choices so far listed above with the bonus already added | a-d | | `gen_race`, `gen_sex`, `gen_class`, `gen_other_build` | **Observation:** bonuses appear only after the choice; the lists do not say what a race or class gives |
| Name, save | prompt | -> main menu | name, confirm | "Enter thy name:", "Save this character? (Y-N)" | letters, enter, y/n | | `gen_name`, `gen_save` | |
| Character Selection | list | b -> overworld | pick slot | 1)-4) names | 1-4, esc | | `menu_select` | |
| Overworld view | screen | | play | 19x9 squares around the hero, monsters, vehicles, places | all commands | blocked moves answered in the log | `start_overworld`, `gameplay_lands_feudal_lords` | |
| Message log | hud element | always | history and prompts | four lines | | | `hud_status`, `battle_orc_hit` | |
| Status panel | hud element | always | vital numbers | Hits, Food, Exp., Coin; Shld, Fuel in space | | red when low | `hud_status`, `gameplay_space_top` | **Observation:** numbers jump to four digits ("Hits:1487") and lose their space |
| Ztats | screen | z -> back | inventory | player line, statistics, coins by kind, armour, weapons, spells, vehicles, gems, enemy vessels; readied items red; More when two pages | space | | `inventory_ztats`, `inventory_ztats_mid`, `inventory_ztats_late` | |
| Ready lists | menu | r, w/a/s | choose readied item | owned items lettered by their fixed list letter | letter | | `inventory_ready_weapon`, `inventory_ready_armour`, `inventory_ready_spell` | **Observation:** letters skip missing items (no e) for an unbought Steal) so a letter always means the same spell |
| Inform | message | i | location | land, woods, sea, town name | | | `gameplay_inform`, `gameplay_woods`, `gameplay_at_sea` | |
| Refusals | message | any | | "Huh?", "HyperJump?", "Steal?", "Get?", "Quit - only allowed outdoors!", "Thou hast not a key!", "Thou must face the ladder!" | | | `gameplay_refusals`, `system_quit_indoors`, `system_no_key`, `system_klimb_facing` | **Observation:** refusals use the same log line as results, no sound or colour change |
| Town / castle view | screen | e -> walk off the edge | town play | whole map at 8x8 pixels per square, signs over the shops, people | commands | | `gameplay_britian`, `gameplay_town_moon`, `gameplay_town_fawn`, `gameplay_town_paws`, `gameplay_town_yew`, `gameplay_town_tune`, `gameplay_town_grey`, `gameplay_castle` | |
| Shop box | menu | t at a counter | buy/sell | shop name, lettered goods with prices | b/s, letters, amounts | "Sold!", "Thou canst not afford it!", "Sorry, we don't deal in used stuff." | `shop_transport`, `shop_sold`, `shop_cannot_afford`, `shop_no_used`, `shop_weapons_sell`, `shop_food` | **Observation:** goods keep their list letter (c, e, g ...) so letters are not consecutive |
| Pub box | dialogue | t, b in a pub | ale and tips | "The tavern keeper sayeth:", tip text | b, space | | `shop_pub`, `dialogue_pub_space`, `dialogue_pub_princess`, `dialogue_pub_mondain`, `dialogue_pub_lakes` | |
| King box | dialogue | t beside the king | quests, hit points | "Dost thou offer pence or service:", "How much?", quest text | p/s, amounts | "Thou art on a quest for me already!", "He is not here!" | `dialogue_king_offer`, `dialogue_king_pence`, `dialogue_king_quest`, `dialogue_king_busy`, `dialogue_king_kill_quest`, `dialogue_king_olympus`, `dialogue_gem_red`, `dialogue_gem_white`, `dialogue_quest_done` | |
| Landmark box | message | e on a landmark | inscription and reward | text; reward in the log after space | space | | `system_landmark_pillars`, `system_landmark_tower`, `system_landmark_argonauts`, `system_landmark_ozymandias`, `system_landmark_signpost`, `system_landmark_southern`, `system_landmark_eastern`, `system_landmark_grave` | |
| Dungeon view | screen | e on a dungeon | first-person | wireframe corridor, doors, ladders, chest, coffin, monster; "Level N" on top, facing below | arrows, commands | "Forward - path blocked!" | `gameplay_dungeon`, `gameplay_dungeon_door`, `gameplay_dungeon_ladder`, `gameplay_coffin`, `battle_balron` | |
| Lift-off countdown | message | b on a shuttle | | "10..9..8..", "Thou hast lifted off!" | | | `system_liftoff` | |
| Space top view | screen | | flight | sector with planet, sun, starbase, ship | arrows, commands | | `gameplay_space_top` | |
| Sector Scan | map | i in space | the 7x7 sectors | one symbol per sector, H for enemies | | | `map_sector_scan` | **Observation:** no legend on screen |
| Space front view | screen | v | combat view | stars, gun sight, enemy fighters, laser beams | f, h, arrows | "Thou must eliminate all enemy craft first!" | `gameplay_space_front`, `gameplay_space_enemy`, `system_space_view_refused`, `battle_alien_fires` | |
| Hyperspace | transition | h | | streaking stars | | | `system_hyperjump` | |
| Achievement box | message | 20th kill | | "Thou hast achieved the rank of Space Ace!" | | | `system_space_ace` | |
| Death | screen | 0 hits or food | | skull, "thou art dead", "Attempting resurrection!" | | | `gameover_dead`, `gameover_starved`, `gameover_sun` | |
| Time machine boxes | cutscene | b on the time machine | story | four pages, gem holes R G B W; without the gems a one-line refusal | space | | `system_time_machine_no_gems`, `cutscene_time_machine`, `cutscene_launch`, `cutscene_pulled`, `cutscene_face_to_face` | |
| Mondain's chamber | screen | | final fight | time machine, hero, gem, Mondain | arrows, a, g | | `boss_mondain`, `boss_gem_destroyed` | |
| Victory box | message | Mondain at 0 | | "THOU ART VICTORIOUS!"; with the gem intact only "...or is he?" in the log | space | | `ending_victorious`, `boss_or_is_he` | |
| Ending text | screen | | epilogue | three paragraphs, "Press CONTROL-ALT-DEL to Restart" | none | | `ending_text` | **Observation:** the game ends by asking for a reboot |
| Save message | message | q outdoors | | "Quit - saving game...saved." | | "only allowed outdoors!" | `save_quit` | |

## 3. Screen flow
- power-on -> text title -> Origin logo -> castle picture -> (loop); any key -> credits -> main menu
  - a -> Character Generation (points -> race -> sex -> class -> name -> save) -> main menu
  - b -> Character Selection -> overworld
- overworld <-> towns / castles (e; leave by the edge) <-> shop, pub and king boxes
- overworld <-> dungeons (e; K-limb up from level 1 out) ; overworld <-> landmarks (e, box)
- overworld -> shuttle (b) -> space (top/front view, sector scan, hyperjump) -> landing -> overworld
- overworld -> time machine (b, four gems) -> four boxes -> Mondain's chamber -> victory -> ending text
- any death -> skull -> resurrection on the overworld
**(verified except starbase docking)**

## 4. Elements in detail
- **Play screen:** blue frame; map window 304x144 pixels (19x9 squares of 16 pixels outdoors; 8-pixel squares
  in towns so the whole town fits); log 4 lines at the bottom left; panel at the bottom right **(verified)**.
- **Status panel:** "Hits:", "Food:", "Exp.:", "Coin:" with right-aligned numbers; in space "Shld:", "Fuel:"
  **(verified)**. The panel is redrawn only when a value changes in play.
- **Dungeon frame:** "Level N" centred on the top edge, the facing (North, South, East, West) on the bottom edge
  **(verified)**.
- **Message log examples:** "Attack with dagger: East", "Hit the Orc! 17 damage", "Killed the Orc! 2 copper! 1
  silver!" (`battle_orc_hit`, `battle_orc_killed`); "Mount Horse" (`system_mount_horse`); "X-it"
  (`system_xit`); "Noise off" (`system_noise`); "Drop pence:10 OK!" (`gameplay_drop_pence`).

## Open questions
- Starbase screens ("Docked! Welcome to base!", "Choose thy ship:") not reached.
