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
| Arrow panel | hud element | right button | moving by mouse | 8 arrows + rest (Zz) | left button | - | `system_arrows`, battle_arrows (live play only, not in the set: fights do not reproduce, see playbook) | - |
| Message scroll | hud element | always | echoes and results | last five messages | - | - | `gameplay_door_nobody` | - |
| Leave prompt | prompt | town edge | confirm leaving | "Leave this place? Left YES Right NO" | left / right button | - | `18_leave_prompt` (start set) | - |
| Status page | screen | portrait | one hero's values | hit points, magic, experience, character, weapon, armour, weapon points, armour points, food, gold | icons: inventory (?), spells (pentagram), back | - | `inventory_status`, `inventory_status_dobranur`, `inventory_weapon` | - |
| Inventory page | list | status page | items | gold, food, item pictures with counts | Examine, Use, Prepare, drop; click an item's picture | "Examine which item?", "It is a Sword", "Can't use this item!" | `inventory_items`, `inventory_map_piece`, `inventory_examine`, `map_worldmap_added` | - |
| Spells page | list | status page | known spells | empty at the start | - | - | `inventory_spells` | - |
| Cast prompt | prompt | magic icon | choose the caster | "Who should cast ?" | portrait | "No spell prepared" or "You have no spell ready" | `system_cast_no_spell` | - |
| Speak window | screen | lips icon next to a person | conversation | a description of the person and what he says | up/down scroll, show, deliver | "Who should show something?" | `dialogue_redhair`, `dialogue_show` | - |
| Camp scene | screen | campfire icon | rest | the party at a campfire | - | "zzz..." | `system_camp` | - |
| Disk menu | menu | disk icon (land) | save, load, exit | two disk icons and an exit icon on a red grid | left button | "Gamesave?", "Gameload?", "Game saved" | `save_prompt`, `save_done`, `save_load_prompt` | - |
| Encounter message | message | random on the land -> combat | who attacks | "Your opponents' attack surprises you. They are Snakes!" | left button | - | battle_encounter (live play only, not in the set: fights do not reproduce, see playbook) | - |
| Combat screen | screen | encounter | orders | side view of the selected hero and the enemies, overhead grid, "Bladus 1. Move(1):" | arrows, icons (magic, attack or shoot, parry) | "Has no longrange weapon!" | battle_start (live play only, not in the set: fights do not reproduce, see playbook), battle_close (live play only, not in the set: fights do not reproduce, see playbook), battle_attack_order (live play only, not in the set: fights do not reproduce, see playbook), battle_no_weapon (live play only, not in the set: fights do not reproduce, see playbook), battle_round2 (live play only, not in the set: fights do not reproduce, see playbook) | **Observation:** the icon grid shows a hero's options one step late, so the sword appears after the order is due |
| Combat result | message | carrying out orders | blow by blow | full-width side view, message line | left button | "Bladus hit a Snake (27)!", "mortually wounded" | battle_hit (live play only, not in the set: fights do not reproduce, see playbook), battle_wounded (live play only, not in the set: fights do not reproduce, see playbook) | - |

## 3. Screen flow
```
power-on -> crack intro -> Thalion logo -> dragon -> title <-> Main Menu
Main Menu: N -> intro pages x4 -> "Insert disk B" -> town (Pegana)
           O -> disk swaps -> land (saved place);  B -> Backup Menu;  S -> Sequences;  C -> Credits
town/land view -> portrait -> status -> inventory / spells -> back
town: lips -> speak window -> right button back;  hand -> door;  eye -> look;  edge -> "Leave this place?" -> land
land: enter -> town;  campfire -> camp;  disk -> disk menu (save / load / exit);  random -> encounter -> combat
combat: orders per hero -> results -> next round ... (victory / defeat not reached)
```

## 4. Elements in detail
- **Lower panel (all play screens):** portraits at the left (click = status page; in combat M and H values on
  each), the message scroll in the middle, the command grid at the right **(verified: `hud_land`)**.
- **Combat screen:** the top-left grid (12 x 8 squares) marks heroes and enemies and highlights the hero whose
  order is due; the side view shows that hero's surroundings; the scroll prints "<hero> 1. Move(1):" and each
  order given ("Forward", "Attack.", "Parry.") **(verified: battle_start (live play only, not in the set: fights do not reproduce, see playbook), battle_attack_order (live play only, not in the set: fights do not reproduce, see playbook))**.

## Open questions
- The disk menu's third icon and the land's sword icon; the talk window's "deliver" icon.
- Shop screens (the game text names the list header "List of:" and "Owner:").
