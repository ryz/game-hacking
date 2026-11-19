# Might and Magic II: Gates to Another World (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/might-and-magic-2`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only; every screen prints its keys; single keystrokes (letters, digits, arrows), Enter only
  after names and numbers; Esc goes back; Ctrl+letter for destructive or party actions (add/remove a member,
  rename, delete) **(verified)**. Keys typed early stay in the buffer and act on the next screen **(verified)**.
  A key the screen does not use does nothing (no beep seen) **(verified)**.
- **Layout:** 320x200 in 16 colours, red double frames. Play screen: 3-D view top left, command list
  (OPTIONS) or Protection panel top right, a status line (Protect/Options toggle, Day, Year, Face), and the party
  window at the bottom with names and hit points in two columns; the party window doubles as the message area
  **(verified)**. Full-screen text pages (profile, quick ref, view all) keep the frame and end with "('ESC' to go
  back)" **(verified)**.
- **Text:** one bold 8x8 font in mixed case; prompts end with "(y/n)?"; abbreviations on the profile (Lvl, Mgt,
  Int, Per, End, Spd, Acy, Lck, HP, SP, AC, SL, Exp) **(verified)**.
- **Feedback:** results appear as one line in the party window ("Nothing Here!", "Not Locked!"); story messages
  wait for Space ("('Space' to continue)") **(verified)**. Signs appear as a yellow signboard over the view
  **(verified)**.
- **State visibility:** always visible: party names and hit points, day, year, facing; light, magic and element
  resistance on the Protect panel; coordinates and map only on the Location screen **(verified)**.
- **Help and onboarding:** none in the game beyond the key lists; the manual explains rules, spells and skills
  **(verified / source)**.

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`. All rows **(verified)** unless marked.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Logo | transition | power-on -> title | publisher logo | "New World Computing Presents..." | - | - | `boot_nwc_logo` | - |
| Title picture | screen | logo -> opening options | title | animated pegasus scene | any key | - | `title_screen` | - |
| Opening options | menu | title -> Main Options, About, Copy, drive | start the game | four options | `s` `a` `c` `d` | - | `menu_opening`, `menu_about`, `menu_copy` | - |
| Main Options | menu | -> create, view all, transfer, go to town | roster management | four options | `c` `v` `t` `g` | - | `menu_main` | - |
| View All | list | Main Options -> profile | the roster A-X, hirelings on a second page | name, class/level | letter, Space, Esc | - | `menu_view_all`, `menu_hirelings` | - |
| Profile (roster) | screen | View All -> rename/delete | one character | statistics, HP, SP, AC, SL, age, experience, gold, gems, food, thievery, skills, condition, 6 equipped, 6 backpack | Ctrl-N, Ctrl-D, Esc | name typed on the bottom line | `inventory_premade`, `menu_rename` | - |
| Create | screen | Main Options -> race, alignment, sex, name | roll a character | dice picture, seven statistics, eligible classes | Enter, letters, digits, name | the class list changes with each roll | `create_roll`, `create_exchange`, `create_race`, `create_alignment`, `create_sex`, `create_name` | **Observation:** the exchange option makes a wanted class reachable without many re-rolls |
| Transfer | prompt | Main Options | import Might and Magic 1 characters | path prompt with examples | text, Enter | - | `menu_transfer` | - |
| Inn list | list | go to town, sign-in, game over -> play | form the party, save | town name and number, characters, ticks, counts C/H | Ctrl-letter, `1`-`5`, Space, `z`, Esc | "'Z' to exit" with the first tick; "ESC to exit to DOS" after a sign-in | `menu_inn_list`, `save_signed_in`, `save_atlantium`, `gameover_inn_empty` | - |
| Play screen | screen | inn exit, every area | exploring | view, OPTIONS, status line, party window | arrows, command letters | one-line messages | `gameplay_inn_start`, `gameplay_outdoors_c2` | - |
| Event message | message | stepping or turning onto a square | story, offers | text in the party window, picture in the view | `y`/`n`, Space | "('Space' to continue)" for long texts | `dialogue_spirit_corak`, `dialogue_nordon_quest`, `cave_x_marks` | **Observation:** a turn also fires the event, so turning in place re-reads a message |
| Sign | message | square before a door or path | names a place | yellow signboard over the view, or the name above a door | - | - | `gameplay_middlegate_sign`, `env_signpost_b1`, `gameplay_monster_bowl` | - |
| Service offer | prompt | shop or trainer square | sell a skill, trip, key | text with the price, (y/n)? | `y`/`n`, then member `1`-`8` | "Not enough gold!" | `system_otto_mapper`, `system_locksmith`, `system_travel_booked` | **Observation:** most services show only a wall and a text; the shop owner's picture appears only in blacksmiths, taverns, temples, trainers and guilds |
| Shop window | menu | blacksmith, tavern, temple, training `y` | buy and sell | shop name, shopper, gold, Gather Gold, Other Char, list with prices | letters, `g`, `#` | "Thank you - please come again", "Sorry - that spell is unavailable" | `shop_blacksmith_menu`, `shop_blacksmith_weapons`, `shop_blacksmith_specials`, `shop_blacksmith_armor`, `shop_blacksmith_misc`, `shop_blacksmith_bought`, `shop_blacksmith_sell`, `shop_blacksmith_identify`, `shop_tavern_menu`, `shop_tavern_drinks`, `shop_tavern_specialties`, `shop_tavern_tip`, `shop_temple_menu`, `shop_temple_donation`, `shop_temple_spell_refused`, `shop_sages_members_only` | - |
| Training window | menu | training `y` | level up | next level, experience needed or cost, "Press 'T' to train" | `t`, `g`, `#` | "You gained 10 hit points" | `system_training_need`, `system_training_cost`, `system_training_levelup` | - |
| Protection panel | hud element | `p` on the play screen; P in combat | active effects | Light (n), Magic %, Forces % | `o` back to options | - | `system_protect`, `system_protect_elements`, `battle_protect` | - |
| Quick Reference | screen | `q` | the party at a glance | HP, SP, level, SL, AC, age, gems, food, condition | Esc | - | `inventory_quickref`, `hud_quickref_vet`, `hud_food_frenzy` | - |
| Controls | menu | `c`; D in combat | settings | sounds, walk beep, disposition, delay 0-9 | `1`-`4` | highlighted choice | `options_controls`, `battle_delay` | - |
| Location | screen | `m` | where am I | coordinates (map with a Cartographer) | Esc | - | `system_location` | - |
| Exchange box | prompt | `e` on the play screen or in combat | swap positions | "Exchange (1-6) with (1-6)" in a blue box | two digits | the party window redraws | `system_exchange`, `system_exchange_done`, `battle_exchange_prompt` | - |
| Rest / search / dismiss | prompt | `r`, `s`, `d` | - | one line in the party window | `y`/`n`, digit | "Rest complete, no encounters.", "Nothing Here!" | `system_rest_prompt`, `system_rest_done`, `system_search_nothing`, `system_dismiss` | - |
| Profile (play) | screen | `1`-`8` | manage one member | as above plus the command keys | Q C D E G R S T U | prompts on the bottom line ("Equip Which (A-F)?") | `inventory_profile_ryz`, `inventory_profile_vet`, `inventory_profile_mnz`, `inventory_skill_learned`, `inventory_equip_prompt`, `inventory_removed`, `inventory_dropped`, `system_trade_what`, `system_trade_done`, `system_share_done`, `system_gather_done`, `system_use_prompt` | **Observation:** results show only as changed numbers on the same sheet |
| Spell Book | prompt | profile `c`, combat `c` | cast | 9 levels x 7 spells with ticks, "Cast Spell Level", "Number", "'Return' to cast" or "On which" | digits, Enter, target letter | - | `system_cast_spellbook`, `system_spellbook_deddo`, `battle_cast_prompt` | - |
| Encounter | screen | a fight square or chance | choose to fight | monster picture, list of names (+n more), options line, surprise line | `a` `b` `h` `r` | "The monsters surprised you!", "You surprised the monsters!" | `battle_encounter`, `battle_bribe_prompt`, `battle_run_away`, `boss_sheltem_surprise` | - |
| Combat | screen | encounter `a` | fight round | framed picture, monster list with ticks (in reach) and "/Hurt", "Options for: name", party with ticks | per-character letters, D P Q, Ctrl-A | three-line result messages timed by the delay | `battle_options_knight`, `battle_options_caster`, `battle_options_fighter`, `battle_fight_prompt`, `battle_fight_hit`, `battle_spell_hit`, `battle_quick_shoot`, `battle_run`, `battle_waits_opening`, `battle_exchange_done` | **Observation:** ticks are the only sign of who can reach whom |
| Combat view | screen | combat `v` | own sheet in a fight | profile with "'V' View spell book" | `v`, Esc | - | `battle_view` | - |
| Victory | message | last monster down | reward | battles won so far, experience per survivor | - | - | `battle_victory`, `boss_sheltem_victory` | - |
| Death Strikes | screen | whole party down | game over | box over the view, "press ENTER" | Enter | back to the inn list | `gameover_death_strikes` | - |
| Innkeeper | prompt | inn square facing the desk | save | innkeeper picture, question | `y`/`n` | inn list after `y` | `save_innkeeper`, `dialogue_atlantium_inn` | - |
| Ending: control room | screen | after Sheltem | the last puzzle | Cron from space in a screen, text, input field | typed code, Enter | "Thank you. Recalculating trajectory now..." | `ending_control_room`, `ending_collision`, `ending_override_typed`, `ending_recalculating` | - |
| Ending: cryptogram | screen | after the override | test of worth | yellow-framed page, clock counting down from 15:00, cipher text, "Answer= Preamble Code=" | 8 typed letters, Enter | - | `ending_cryptogram`, `ending_answer_typed` | **Observation:** the only real-time element of the game |
| Ending: congratulations | screen | right answer | the end | picture of Cron with the ship, text, battles won/lost, score, address, bonus | key | back to the inn list | `ending_congratulations` | - |

## 3. Screen flow
Power-on -> logo -> title -> opening options -> Main Options -> (create / view all / transfer) -> go to town ->
inn list -> play screen. Play screen -> profile, quick ref, controls, protection, location, event messages,
shop windows, encounter -> combat -> victory -> play screen; a lost party -> Death Strikes -> inn list. Inn
square -> innkeeper -> inn list -> play screen or DOS. Square Lake gate -> Sheltem -> control room -> override
code -> cryptogram -> congratulations -> inn list **(verified)**.

## 4. The play screen, element by element
| Element | Where | Shows | Notes |
|---|---|---|---|
| 3-D view | top left, about 200x115 | three squares deep, walls, doors, torches, sky outdoors; monster or person picture during events | dark without light units **(verified)** |
| OPTIONS list | top right | the 13 exploration keys | replaced by the Protection panel with `p` **(verified)** |
| Status line | middle | 'P' Protect / 'O' Options toggle, Day, Year, Face | **(verified)** |
| Party window | bottom | number, name, hit points of up to 8 members in two columns; messages and prompts use the same box | current hit points are printed as "/14" **(verified)**; at the Square Lake gate it shows "Version 1.01" four times ([findings.md](findings.md)) |

## Open questions
- The automap of a Cartographer: Location showed only the coordinates in this capture.
