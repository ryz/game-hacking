# Phantasy Star - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact. Coverage: the early game (set `main`, 53 shots).

## 1. Conventions
- **Input:** one control pad with two buttons. On the map either button opens the field menu; in menus button 2
  confirms and button 1 cancels; in text either button turns the page **(verified)**. Lists are chosen with a
  cursor (a small triangle) that blinks **(verified: `item_commands`, `shop_sell`)**. The field menu ignores
  input for about two seconds after it opens **(verified)**. Wrong keys do nothing.
- **Layout:** 256x192. The field menu sits top left, the name/HP/MP box bottom left, lists on the right, the
  message box along the bottom **(verified: `hud_menu`, `menu_items`)**. Battles use the same corners: commands
  top left, monster name and HP top centre/right **(verified: `battle_sworm`)**.
- **Text:** white upper-case letters in black boxes with white borders; messages type out letter by letter and
  wait for a button; abbreviations of four to eight letters (STAS, MAGC, SRCH, SHT. SWD, LTH. ARMR) **(verified)**.
- **Feedback:** a struck monster flashes white, a hit on the party flashes the whole screen **(verified:
  `battle_attack`, `battle_hit`)**; purchases are confirmed with "Thank you. Anything else?" **(verified:
  `shop_bought`)**. **Observation:** buying has no "are you sure" step, so one press spends the money.
- **State visibility:** HP and MP of the party are on screen in the field menu and in battle; meseta only in
  ITEM, STAS and shops **(verified)**. **Observation:** a message window covers the right half of the HP box
  (findings.md).
- **Help and onboarding:** none in the game; controls are in the manual **(source)**.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title | screen | power-on -> intro / CONTINUE | start | logo, Alis, START / CONTINUE | up/down, button | input ignored for ~4 s | `title_screen` | |
| Intro scenes | transition | START -> Camineet | story | planet, caption, framed pictures with text | button per page | | `intro_planet`, `intro_camineet`, `intro_nero_beaten`, `intro_nero_dying`, `intro_alis_vow` | the caption fades in and out by itself |
| Continue prompt | prompt | title CONTINUE -> slot list | continue or delete | YES / NO | cursor, button 2 | | `continue_prompt` | "DELETE GAME- NO" doubles as the delete choice |
| Slot list | list | continue / SAVE | pick a save | 1-5 | cursor | | `continue_slots`, `save_slots` | |
| Town map | screen | game -> buildings, gate | walk | top-down town, people | D-pad, button | blocked moves do nothing | `camineet_start`, `camineet_shops`, `camineet_gate` | |
| Surface map | screen | town EXIT -> caves, towns | travel | top-down terrain | D-pad, button | | `palma_camineet`, `palma_forest`, `palma_cave` | |
| Field menu | menu | button on a map | commands | STAS MAGC ITEM SRCH SAVE over a picture of the place | cursor, buttons | | `hud_menu`, `menu_forest` | picture changes with terrain (town, forest) |
| Name/HP/MP box | hud element | field menu, battle | party state | name, HP, MP | none | | `hud_menu`, `battle_sworm` | |
| STAS window | screen | field menu | character sheet | equipment list, LV, EP, ATTACK, DEFENSE, MAX HP, MAX MP, MST | button | | `menu_status`, `status_shield` | |
| ITEM list | list | field menu | inventory | MST and items | cursor | | `menu_items` | |
| Item command box | menu | ITEM list | act on an item | USE EQP DRP | cursor | | `item_commands` | |
| Item message | message | USE / EQP | result | "Alis equips ...", "Burger. Alis is healed." | button | | `item_equip`, `item_use_burger` | |
| SRCH message | message | field menu | search | "There doesn't seem to be anything" | button | | `menu_search` | |
| House scene | screen | door | flavour | room picture, one message | button | | `alis_home` | |
| Shop scene | screen | shop door -> list | buy/sell | shopkeeper, counter, BUY / SELL (second-hand) or YES / NO | cursor | | `shop_secondhand`, `shop_food`, `shop_armory` | each shop has its own room and keeper |
| Price list | list | shop | choose an item | names, prices, MST window | cursor, button 2 | | `shop_list`, `shop_food`, `shop_armory`, `shop_bought` | |
| Sell list and offer | list, prompt | second-hand SELL | sell | items carried, offered price, YES / NO | cursor | | `shop_sell`, `shop_sell_offer` | |
| Church scene | screen, prompt | church door | resurrection | priest, altar, YES / NO | cursor | "Alis is alive." | `camineet_church`, `church_alive` | |
| First-person view | screen | cave or passage door | explore | 3D corridor, no HUD | D-pad, button | dark: "Cannot go forward, it's pitch black." | `dungeon_corridor`, `camineet_passage`, `dungeon_step`, `dungeon_turn`, `cave_dark` | animated steps and turns |
| Chest prompt | prompt | chest square, beaten monster | open | chest picture, YES / NO | cursor | contents message | `dungeon_chest`, `battle_chest`, `battle_chest_meseta` | |
| Battle screen | screen | encounter | fight | backdrop of the place, monster, name/HP, commands | cursor | flashes | `battle_sworm`, `battle_scorpion`, `battle_wing_eye`, `battle_attack`, `battle_hit` | |
| Battle messages | message | battle | results | kill, EXP, level, TALK, death | button / time | | `battle_killed`, `battle_exp`, `battle_levelup`, `battle_talk`, `battle_died` | some pass by themselves |
| Game over | message | party dead -> title | end | "... The adventure is over." | button | | `gameover` | no continue prompt, back to the title |


### 2b. Screens added in part 2 (2026-11-19)
| Screen / element | Purpose | Shows | Accepts | Answers / leads to | Shots |
|---|---|---|---|---|---|
| Person scene | talk with a townsperson | the person in front of a picture of the town, a two-line text box below | button 1/2 per page | YES / NO window or the map | `talk_townsperson`, `nekise`, `npc_question`, `parolit_medusa`, `cola_beggar`, `bortevo_junk`, `governor`, `myau_merchant`, `myau_trade`, `myau_traded` |
| Person in a dungeon | a person met on an event square | the person over the corridor view, text box | button, YES / NO | | `cat_thief`, `dungeon_robotcop`, `talking_spider`, `mansion_guard`, `boss_shadow` |
| Portrait scene | story moments | a framed portrait (Alis, Myau) on black, text under it | button per page | | `myau_meet_alis`, `myau_meet` |
| Hospital | heal for a fee | nurse at a counter, red cross, YES / NO | YES / NO | fee page | `hospital`, `hospital_fee` |
| Dungeon shop | buy from a merchant inside a dungeon | the merchant in the corridor | | | `dungeon_shop` |
| Spaceport counter | board the liner | the guard on the landing field with ships, YES / NO | YES / NO | the flight scene | `spaceport_guard`, `spaceship_board` |
| Flight scene | travel between planets | the ship on a star field | none | the arrival spaceport | `spaceship_flight` |
| Luveno destination list | pick a destination | Hapsby, a list GOTHIC UZO SKURE, "Where are we going?" | up/down, button | | `luveno_ship` |
| Name grid | name a new save | letters A-Z and signs, ADV RUB END | D-pad, button | | `save_name` |
| Member chooser | pick who acts (MAGC, STAS) | a list of the party under the field menu | up/down, button | the member's list | `magic_who` |
| Item USE for vehicles | change to a vehicle | ITEM list with USE / EQP / DRP | | the vehicle, or "will do no good" | `landrover_menu`, `vehicle_no_good` |
| Party HUD | permanent | one box per member with HP / MP, up to four | | | `boss_titan`, `battles:sorcerers` |
| Battle HP box | monster HP | the name, and one HP line per monster of the group | | | `battles:marman_group`, `battles:fishman_group` |
| Battle messages | results | deaths, "You are all dead.", TALK answers, status ("turned to stone") | button | | `battles:wipe_myau`, `battles:wipe_all`, `battles:talk_dezorian`, `battles:talk_barbarian`, `battles:medusa_attack` |
| Map: towns | top-down towns, each family with its own tiles | | D-pad | | `parolit`, `gothic`, `scion`, `drasgow`, `paseo`, `motavia_village`, `motavia_village2`, `skure`, `dezorian_town`, `lassic_castle` |

## 3. Screen flow
- Power-on -> title -> START -> planet -> caption -> Nero scenes -> Camineet (control).
- Title -> CONTINUE -> continue/delete -> slot list -> the saved place.
- Map -> button -> field menu -> STAS / MAGC / ITEM (-> USE / EQP / DRP) / SRCH / SAVE (-> slots).
- Map -> door -> house, shop (BUY / SELL -> list -> thanks), church (YES / NO), first-person passage.
- Town EXIT -> surface -> cave -> first-person view (dark: message) -> chest squares.
- Surface or cave -> encounter -> battle (ATTK / MAGC / ITEM / TALK / RUN) -> messages -> chest -> map; or
  death -> game over -> title.

## 4. Elements in detail
- **Battle screen** (`battle_sworm`): commands top left with the acting member's name below; monster name top
  centre with its HP to the right; the party box bottom left; the backdrop is the place of the fight: forest
  on the surface, the corridor in caves (`battle_wing_eye`).
- **First-person view** (`dungeon_corridor`): the full screen, no HUD; a step scrolls the floor lines
  (`dungeon_step`), a turn rotates the walls (`dungeon_turn`); a chest stands on the floor in front of the
  player (`dungeon_chest`). Wall colour depends on the place: blue in the cave, green in the Camineet passage
  (`camineet_passage`).

## Open questions
- How a talk with a townsperson is started and what it looks like (portrait window per the scout's notes).
- DRP and its confirmation; the save confirmation message.
