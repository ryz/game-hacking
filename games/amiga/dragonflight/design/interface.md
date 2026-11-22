# Dragonflight - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** the mouse does everything: left button on an icon, a portrait or an item picture; right button
  swaps the command icons for eight direction arrows and a rest icon, and back **(verified)**. The keyboard
  serves the Main Menu (letters N, O, B, S, C) and movement (numeric keypad) **(verified)**. Yes/No prompts are
  answered with the buttons themselves: "Left YES Right NO" **(verified)**. Clicking an item's name does nothing;
  the item's picture must be clicked **(verified)**. Clicks during a disk load are lost **(verified)**.
- **Layout:** title and menus are lores; the game screen is hires: a framed view at the top (map, scene,
  combat side view, text window, status or inventory page) and a fixed panel below: four portraits (2 x 2),
  the message scroll (five lines), the 3 x 3 command grid **(verified)**. In combat the overhead battle grid
  takes the view's top-left corner and the portraits show M (magic) and H (hit points) **(verified)**.
- **Text:** a single bold font; messages scroll up in the panel, each new one starting with a ">" mark
  **(verified)**. Long texts (intro, speech, encounter messages) get their own window; the encounter and combat
  result messages replace the whole panel **(verified)**. The game's English has German traces ("mortually
  wounded", "Housens", "embaressed") **(verified/RAM)**.
- **Feedback:** every command echoes in the scroll ("North", "Blocked", "Pass", "Status", "Inventory");
  irreversible actions ask Yes/No (leave a town, save, load) **(verified)**.
- **State visibility:** portraits only on the map; hit points and magic show on the portraits in combat and on
  the status pages **(verified)**. Position, time and gold need a page (status/inventory) **(verified)**.
- **Help and onboarding:** the sage's four intro pages; no in-game help beyond the Backup Menu's Help
  **(verified)**.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Crack intro | screen | power-on -> Thalion logo | cracker's intro (not the game) | vector letters | left button | - | `boot_crack` | - |
| Thalion logo | screen | crack -> dragon | publisher logo | logo over raining drops | left button | - | `boot_thalion` | - |
| Dragon scene | transition | logo -> title | attract animation | red dragon spreading its wings | - | - | `title_dragon` | - |
| Title | screen | attract cycle | game logo | DRAGONFLIGHT | - | - | `title_screen` | alternates with the menu by itself |
| Main Menu | menu | title -> new game, old game, backup, sequences, credits | start or load | five letter entries, "Configuration: 00000" | N O B S C | - | `menu_main` | **Observation:** keyboard letters, while the rest of the game is mouse-only |
| Backup Menu | menu | Main Menu (B) | format or copy Disk B | Format, Copy, Help, Exit | F C H E | - | `menu_backup` | - |
| Sequences prompt | prompt | Main Menu (S) | replay the story scenes | "Insert backupdisk B! (ESC to cancel)" | disk, ESC | - | `menu_sequences` | - |
| Credits | screen | Main Menu (C) | the three authors | portraits of Erik Simon, Udo Fischer, Jochen Hippel | - | - | `credits_team` | - |
| Intro pages | screen | New game -> Disk B prompt | the quest | the sage, five lines per page, arrow mark | left button per page | - | `cutscene_sage` | - |
| Disk prompts | message | new game, old game | swap floppies | "Insert disk B please", "Thank You!" | disk change | - | `menu_oldgame` | - |
| Town / land view | screen | the main view | walking | top-down map with the party | keypad, arrows, icons | "Blocked", "Pass" | `env_pegana_square`, `env_land_river`, `hud_land` | - |
| Command grid | hud element | always | commands of the place | 3 x 3 icons, different in town, land, combat, talk, inventory | left button | "Icon not available!" **(RAM)** | `hud_land`, `env_pegana_road` | **Observation:** icons only, no labels; the first click is guesswork |
| Arrow panel | hud element | right button | moving by mouse | 8 arrows + rest (Zz) | left button | - | `system_arrows`, `battle_arrows` | - |
| Message scroll | hud element | always | echoes and results | last five messages | - | - | `gameplay_door_nobody` | - |
| Leave prompt | prompt | town edge | confirm leaving | "Leave this place? Left YES Right NO" | left / right button | - | `18_leave_prompt` (start set) | - |
| Status page | screen | portrait | one hero's values | hit points, magic, experience, character, weapon, armour, weapon points, armour points, food, gold | icons: inventory (?), spells (pentagram), back | - | `inventory_status`, `inventory_status_dobranur`, `inventory_weapon` | - |
| Inventory page | list | status page | items | gold, food, item pictures with counts | Examine, Use, Prepare, drop; click an item's picture | "Examine which item?", "It is a Sword", "Can't use this item!" | `inventory_items`, `inventory_map_piece`, `inventory_examine`, `map_worldmap_added` | - |
| Spells page | list | status page | known spells | spell names with school, a check mark when prepared | Prepare icon (bottom left), then the spell's star | "Prepare which spell?" -> "Spell ready" | `inventory_spells`, `magic_spells_known`, `magic_prepared` | - |
| Read a scroll | prompt | Use on a scroll | who learns | "Who should read this scroll?", then a click on a portrait in the top-right 2 x 2 (the main panel portraits do not answer) | portrait | "learned this spell" | `inventory_scroll`, `magic_read_scroll`, `magic_learned` | **Observation:** two sets of portraits, only one answers this prompt |
| Cast result | message | magic icon -> hero | outcome | message scroll line | - | "Spell has failed!" | `magic_cast_failed` | - |
| Game over | screen | last hero falls | defeat | dark blue: "Is this THE END of all hope?" and the four faces | - | then "Insert disk A please" | `gameover` | - |
| Opponent views | screen | fight start | who you fight | one picture per kind on the side view, grid dots per opponent | - | - | `battle_orcs`, `battle_troll`, `battle_balron`, `battle_energyball` | - |
| Cast prompt | prompt | magic icon | choose the caster | "Who should cast ?" | portrait | "No spell prepared" or "You have no spell ready" | `system_cast_no_spell` | - |
| Speak window | screen | lips icon next to a person | conversation | a description of the person and what he says | up/down scroll, show, deliver | "Who should show something?" | `dialogue_redhair`, `dialogue_show` | - |
| Camp scene | screen | campfire icon | rest | the party at a campfire | - | "zzz..." | `system_camp` | - |
| Disk menu | menu | disk icon (land) | save, load, exit | two disk icons and an exit icon on a red grid | left button | "Gamesave?", "Gameload?", "Game saved" | `save_prompt`, `save_done`, `save_load_prompt` | - |
| Encounter message | message | random on the land -> combat | who attacks | "Your opponents' attack surprises you. They are Snakes!" | left button | - | `battle_encounter`, `battle_msg_orcs` | - |
| Combat screen | screen | encounter | orders | side view of the selected hero and the enemies, overhead grid, "Bladus 1. Move(1):" | arrows, icons (magic, attack or shoot, parry) | "Has no longrange weapon!" | `battle_start`, `battle_orders`, `battle_orders`, none (seen live: "Has no longrange weapon!"), `gameover` | **Observation:** the icon grid shows a hero's options one step late, so the sword appears after the order is due |
| Combat result | message | carrying out orders | blow by blow | full-width side view, message line | left button | "Bladus hit a Snake (27)!", "mortually wounded" | `battle_hit`, `battle_wounded`, `battle_statue` | - |
| Dungeon view | screen | Enter on a cave arch | first-person walking | stone corridor between two amulet medallions; black without light | keypad 8 2 4 6, icons | "Forward", "Turn left", "Blocked" | `dungeon_dark`, `env_dungeon_corridor`, `dungeon_forward`, `dungeon_turn`, `dungeon_blocked`, `dungeon_door` | the panel sits about 10 pixels higher than on the land |
| Dungeon icon grid | hud element | dungeon view | commands below ground | pentagram (cast), hand with item (take: "WHAT to take?"), ear (listen), hand at door (open), chest, eye, torch and key, disk | left button | "There is no door!", "There is no chest!", "It is a Door!", "I can hear nothing!", "The door is already open!" | `dungeon_look_door`, `dungeon_open`, `dungeon_listen`, `dungeon_key`, `dungeon_chest` | - |
| Great Map | screen | Examine on the Worldmap item | the world chart | the parts added so far on black, a compass rose (N E S W) | - | - | `map_great_map_one`, `map_great_map` | full screen, no panel |
| Mix potions | screen | Use on a potion | mixing | ten green ingredient cells, a cauldron, the flask, a T-shaped tray | item pointer | - | `potion_mix` | how a mixture is made is open |
| Give / drink prompt | prompt | click an item picture in the inventory | give an item; to oneself = eat or drink | "Give to whom?" | top-right 2 x 2 portraits | a full-width text of the potion's taste and effect | `potion_give`, `potion_heal`, `potion_poison` | - |
| Temple view | screen | Enter on a temple icon | revive and bless | a pillared hall with a blue basin, the temple's name | - | "The temple shows no effect!" | `temple_stormwind`, `temple_gemshine` | each temple has its own colours |

## 3. Screen flow
```
power-on -> crack intro -> Thalion logo -> dragon -> title <-> Main Menu
Main Menu: N -> intro pages x4 -> "Insert disk B" -> town (Pegana)
           O -> disk swaps -> land (saved place);  B -> Backup Menu;  S -> Sequences;  C -> Credits
town/land view -> portrait -> status -> inventory / spells -> back
town: lips -> speak window -> right button back;  hand -> door;  eye -> look;  edge -> "Leave this place?" -> land
land: enter -> town;  campfire -> camp;  disk -> disk menu (save / load / exit);  random -> encounter -> combat
combat: orders per hero -> results -> next round ... -> defeat: "Is this the end of all hope?" -> Insert disk A (victory not reached)
```

## 4. Elements in detail
- **Lower panel (all play screens):** portraits at the left (click = status page; in combat M and H values on
  each), the message scroll in the middle, the command grid at the right **(verified: `hud_land`)**.
- **Combat screen:** the top-left grid (12 x 8 squares) marks heroes and enemies and highlights the hero whose
  order is due; the side view shows that hero's surroundings; the scroll prints "<hero> 1. Move(1):" and each
  order given ("Forward", "Attack.", "Parry.") **(verified: `battle_start`, `battle_orders`)**.

## Open questions
- The disk menu's third icon and the land's sword icon; the talk window's "deliver" icon.
- Shop screens (the game text names the list header "List of:" and "Owner:").
