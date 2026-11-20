# Might and Magic II: Gates to Another World (Apple II) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/might-and-magic-2`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only; every screen prints its keys; single keystrokes (letters, digits, arrows), Return
  after names and numbers and to answer a disk prompt; Esc goes back; Ctrl+letter for party and roster actions
  (tick a member at the inn, rename, delete) **(verified)**. Return is also "forward" in the street
  **(verified)**. The Apple II keyboard holds one key: a key pressed while the game is busy replaces the one
  before **(verified)**. **Observation:** answering a disk prompt that did not come walks the party a square.
- **Layout:** 280x192 hi-res in colour (shots 560x384), purple double frames. Play screen: 3-D view top left,
  command list (OPTIONS) or Protection panel top right, a status line ('P' Protect, Day, Year, Face) and the
  party window at the bottom (names and hit points in two columns), which also carries messages and prompts
  **(verified: `env_middlegate_street`)**. Full-screen text pages (profile, quick ref, view all, inn list) keep
  the frame and end with "('ESC' to go back)" **(verified)**. In an encounter the monster names replace the
  command list in a yellow frame; in combat the portrait moves into a framed box top left and the list shows
  every monster with a tick for those in reach **(verified: `battle_encounter`, `battle_screen`)**.
- **Text:** one upper- and lower-case font in white on black; a selected line in inverse video (the acting
  monster in combat, a member who is down in the party window) **(verified: `battle_monster_hits`,
  `start 41_death_strikes`)**. Names keep their case (ryz) **(verified)**.
- **Feedback:** prompts end with "(y/n)?"; shops answer "Thank you - Please come again" or "Sorry - ..."
  **(verified)**. Combat messages are timed by the message delay (Controls 0-9), not by a key **(verified)**.
  Story pages wait for "('Space' to continue)" **(verified: `cutscene_corak`)**.
- **State visibility:** always on screen: party names and hit points, day, year, facing **(verified)**.
  Spell points, gold, food, conditions need the quick reference or a profile **(verified)**. Coordinates
  need M (not listed on the screen) **(verified)**.
  **Observation:** the party window is not redrawn after some changes (see playbook: hit points after a poke).
- **Help and onboarding:** the OPTIONS list names every exploration key; combat lists the member's options;
  creation lists the eligible classes **(verified)**. Spells, monsters and the map are only in the manual
  **(source)**.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Publisher logo | transition | power-on -> title | credit | "New World Computing Presents" with a globe | - | - | `boot_nwc`, `start 01_power_on` | |
| Title picture | screen | logo -> opening options | title | Might and Magic Book Two, a pegasus; a small creature animates | Space | - | `title_screen`, `start 02_title` | |
| Opening options | menu | title -> disk prompt, copy, about | start, copy, credits, drives | two turning globes, S C A N | `s` `c` `a` `n` | - | `menu_options`, `menu_copy`, `menu_about` | |
| Disk prompt | prompt | any load from another disk | ask for a disk | "Insert Disk X in Drive 1 and Press 'Return'" in a framed box over the screen | Return | - | `menu_disk_b`, `boss_sheltem_face`, `gameover_sheltem`, `start 33_insert_disk_c` | **Observation:** six disks and one drive: a prompt at most area changes |
| Main Options | menu | disk B -> create, view, transfer, towns | roster management | two books, C V T G | letters | - | `menu_main` | |
| Transfer | screen | Main Options | bring a Book One roster | instructions, insert MM1 character disk | Return, Esc | - | `menu_transfer` | |
| View All | list | Main Options | roster A-X | name, class/level | letter, Space (hirelings) | - | `menu_view_all`, `menu_hirelings`, `start 17_view_all_renamed` | |
| Profile | screen | View All, play `1`-`6`, combat V | one character | statistics, HP, SP, AC, SL, gold, gems, food, condition, equipped and backpack | letters, Ctrl-N, Ctrl-D | - | `inventory_premade`, `menu_rename`, `inventory_profile_ryz`, `inventory_profile_vet`, `inventory_profile_mnz`, `battle_view` | |
| Profile prompts | prompt | profile | equip, remove, drop, trade, cast | "Equip Which (A-F)?", "Remove Which (1-6)?", "Drop Which (A-F)?", "Trade: 1 Gold 2 Gems 3 Food 4 Item" | letter, digit | the lists redraw at once | `inventory_equip_prompt`, `inventory_remove_prompt`, `inventory_drop_prompt`, `system_trade_what`, `system_spell_prompt` | |
| Create New Characters | screen | Main Options | roll a character | a hand with dice, statistics A-G, eligible classes numbered | Return, letters, digits, name | the choice moves into the top right | `create_roll`, `create_exchange`, `create_race`, `create_alignment`, `create_sex`, `create_name` | |
| Inn list | list | Go to Towns, Death Strikes, signing in | form the party, save | town name, 24 roster slots with ticks, party and hireling counts, other towns 1-5 | Ctrl+letter, letters, 1-5, Z | ticks appear | `menu_inn_list`, `save_signed_in`, `save_atlantium`, `start 19_party_ticked` | |
| Play screen | screen | inn -> everything | explore | 3-D view, OPTIONS, status line, party window | arrows, letters | messages in the party window | `gameplay_inn_start`, `env_middlegate_street`, `gameplay_outdoors_c2` | |
| Status line | hud element | play screen | time and facing | 'P' Protect, Day, Year, Face | `p` | Year 800 after a century change | `system_year_800` | **Observation:** shows 900 again after an event in year 800 |
| Protection panel | hud element | `p` | light and protection | Light (n), Magic %, Forces % | `o` back | - | `system_protect`, `system_light`, `battle_protect` | |
| Controls | menu | `c`, combat D | options | sounds, walk beep, disposition, delay | `1`-`4` | inverse marks the choice | `options_controls`, `battle_delay` | |
| Quick reference | screen | `q`, combat Q | party overview | HP, SP, level, SL, AC, age, gems, food, condition per member | Esc | - | `inventory_quickref`, `hud_quickref_vet`, `hud_food_frenzy`, `battle_quickref` | |
| Location / automap | screen | `m` | coordinates, map | (x,y) at the top, the 16x16 area full screen (row 15 at the top), an arrow for the party; with a Cartographer in the party the squares walked are drawn: town = cyan floor, white walls, green door marks; outdoors = the terrain tiles (forest, water, mountains); cavern = green floor, white walls; without one only the arrow **(verified)** | Esc | unwalked squares black | `system_location`, `automap_partial`, `automap_middlegate`, `automap_c2`, `automap_cavern` | not on the command list |
| Exchange / dismiss prompts | prompt | `e`, `d` | marching order | "Exchange (1-8) With (1-8)", "Dismiss whom (1-6)?" | digits | the party window redraws | `system_exchange`, `system_exchange_done`, `system_dismiss`, `battle_exchange` | |
| Rest, search, bash messages | message | `r`, `s`, `b` | results | "Rest here? (Y/N)", "Rest complete, no encounters.", "Search... Nothing here!", "Solid!" | y/n | - | `system_rest_prompt`, `system_rest_done`, `system_search_nothing`, `system_bash` | |
| Event message | message | stepping or turning onto a square | story, offers, signs | text in the party window, picture in the view | y/n, Space | - | `cutscene_corak`, `dialogue_nordon`, `dialogue_nordon_quest`, `gameplay_fountain_clairvoyance`, `gameplay_stairs_cavern`, `gameplay_gates` | |
| Sign on a wall | message | the view | names a door or place | a sign over the door or on a post | - | - | `gameplay_middlegate_sign`, `gameplay_arena_entrance`, `gameplay_druid_sign`, `gameplay_fear_no_evil` | |
| Shop menu | menu | `y` at a shop | buy and sell | shop name, member and gold, Gather Gold, Other Char, items or services A-F with prices | letters, `g`, `#` | "Thank you - Please come again", "Sorry - ..." | `shop_blacksmith_menu`, `shop_blacksmith_weapons`, `shop_tavern_menu`, `shop_temple_menu`, `shop_sages_members_only`, `system_training_need` | |
| Encounter | screen | a fight square | decide | portrait, monster names (+N More), "Options: A-Attack B-Bribe H-Hide R-Run" | `a` `b` `h` `r` | "Encounter!", "The monsters surprised you!" | `battle_encounter`, `battle_bribe`, `battle_sl_wizards`, `start 36_orcs` | |
| Combat screen | screen | Attack | fight | framed portrait, monster list with ticks, the member's options, messages, party window | letters, D P Q | monster acting in inverse, damage lines | `battle_screen`, `battle_options_archer`, `battle_options_knight`, `battle_cast_target`, `battle_fight_hit`, `battle_spell_hit`, `battle_monster_hits` | |
| Victory | message | last monster down | reward | "Victory! The party has won its Nth battle. Each survivor receives N experience points" | - | - | `battle_victory` | |
| Death Strikes | message | party down | defeat | framed text, Return | Return | - | `gameover_death_strikes`, `start 41_death_strikes` | |
| Inn registry | prompt | inn desk | save | "Will you sign the registry (y/n)?" | y/n | inn list | `save_innkeeper`, `dialogue_atlantium_inn` | |

## 3. Screen flow
- Power-on -> logo -> title -> Space -> opening options -> S -> disk B -> Main Options
  - C create (roll -> class -> race -> alignment -> sex -> name -> Return saves, next roll) -> Esc
  - V view all -> letter: profile (Ctrl-N rename) -> Esc; Space: hirelings
  - T transfer -> insert Book One disk
  - G go to towns -> inn list -> Ctrl+letters -> Z -> play screen in the inn
- Play screen -> step/turn -> event message / encounter / area change (disk prompt) -> play screen
  - Encounter -> A -> combat -> victory or Death Strikes -> (disk B) -> inn list
  - `1`-`6` profile, `q` quick ref, `c` controls, `p` protection, `m` location, `e` `d` `r` `s` `b` `u`
  - Inn desk -> sign (y) -> inn list (saved)

## 4. Elements in detail
- **Play screen** (`env_middlegate_street`): view 3-D top left (walls with the area's texture, sky outdoors and
  in towns, black ceiling in caverns); OPTIONS top right lists Forward, Move Back, Turn Left/Right, Bash Door,
  Controls, Dismiss, Exchange, Quick Ref, Rest, Search, Unlock, View Char **(verified)**; status line; party
  window with "n) name /HP" for six members **(verified)**.
- **Combat screen** (`battle_screen`): portrait in a yellow frame; "D-Delay P-Prot Q-Quick" over a list of up
  to ten monsters with a tick for those in reach; "Options for: name" with the member's commands; message
  lines replace the options while the round plays **(verified)**.

## Open questions
- The Unlock prompt, Use, the hireling inn page with hirelings, the arena and Copy Disk's later screens were not
  seen.
