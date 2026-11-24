# Quake (DOS, shareware 1.06) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
One paragraph or table each; "not applicable" where the game has none.
- **Input:** devices; confirm and cancel; how lists are chosen (cursor, letter, number); shortcuts; key repeat
  and buffering; what happens on a wrong key.
- **Layout:** screen size and regions (view, lists, message area), what stays in the same place across screens.
- **Text:** fonts, case, colours and what each colour means, wording of prompts, abbreviations.
- **Feedback:** how the game confirms an action, reports an error, asks before something irreversible; waits and
  pacing of messages (press a key, timed).
- **State visibility:** what the player can always see (party, health, money, place, time) and what needs a
  screen to look up.
- **Help and onboarding:** in-game instructions, reference screens, what is only in the manual.

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| DOS command line and start-up console | screen | power-on -> attract demo | memory, hardware, configs, demo loop | Quake v1.06, video card, "3 demo(s) in loop" | nothing | none | [01](../shots/start/quake_dos_na_01_boot_command_line.start.png) [02](../shots/start/quake_dos_na_02_boot_console.start.png) | |
| Attract demo | screen | console -> demo loop; Esc -> main menu | shows play | recorded play with pickup messages | Esc | none | [03](../shots/start/quake_dos_na_03_title_demo_start.start.png) [04](../shots/start/quake_dos_na_04_title_demo_play.start.png) | |
| Main menu | menu | Esc anywhere | top level | Single Player, Multiplayer, Options, Help/Ordering, Quit; spinning Quake icon cursor | up/down, Enter, Esc | menu sound (off here) | [05](../shots/start/quake_dos_na_05_menu_main.start.png) [29](../shots/start/quake_dos_na_29_menu_ingame.start.png) | Over the running demo or the paused game |
| Single Player menu | menu | main menu | New Game, Load, Save | three entries | up/down, Enter | - | [06](../shots/start/quake_dos_na_06_menu_single_player.start.png) | |
| Help/Ordering | screen | main menu | ordering info, then help pages | text pages in a frame | left/right pages, Esc | - | [07](../shots/start/quake_dos_na_07_menu_ordering.start.png) [08](../shots/start/quake_dos_na_08_menu_help_movement.start.png) | Opens on the ordering page, not on help (verified) |
| Status bar | hud element | always in play | state | armor, face, health, ammo of the current weapon; ammo counts and weapons row above | - | numbers change at once (verified 25) | [16](../shots/start/quake_dos_na_16_gameplay_e1m1_start.start.png) [25](../shots/start/quake_dos_na_25_battle_e1m1_yard_attack.start.png) | |
| Centre messages | message | map triggers | instructions | "This hall selects NORMAL skill", "Walk into the Slipgate...", shareware notice | - | timed | [10](../shots/start/quake_dos_na_10_gameplay_normal_hall.start.png) [13](../shots/start/quake_dos_na_13_gameplay_hub_shareware.start.png) [14](../shots/start/quake_dos_na_14_gameplay_hub_e1_gate.start.png) | |
| Pickup and console lines | message | pickups, saves | report | "You got the shells", "Saving game to ... done." at the top | - | timed, several lines stack | [04](../shots/start/quake_dos_na_04_title_demo_play.start.png) [34](../shots/start/quake_dos_na_34_save_saved.start.png) | |
| Loading plaque | transition | slipgate to a level | wait | LOADING over the last frame | - | - | [15](../shots/start/quake_dos_na_15_system_loading.start.png) | |
| TAB scores | hud element | TAB held | progress | Monsters, Secrets, Time, level name over the status bar | TAB | - | [28](../shots/start/quake_dos_na_28_hud_e1m1_scores.start.png) | |
| Options | menu | main menu | settings | Customize controls, Go to console, Reset, screen size, brightness, volumes, run, mouse, Video Options | up/down, left/right sliders | - | [30](../shots/start/quake_dos_na_30_options_options.start.png) | |
| Customize controls | list | Options | key binds | action and its keys | Enter to change, Backspace to clear | - | [31](../shots/start/quake_dos_na_31_options_keys.start.png) | |
| Video Modes | list | Options | display | DOS mode list (320x200 to 1280x1024 here), T to test, D for default | arrows, Enter, T, D | - | [32](../shots/start/quake_dos_na_32_options_video.start.png) | |
| Save / Load | list | F2, F3, Single Player | slots | 12 slots, level name and kills per used slot | up/down, Enter | console line after saving | [33](../shots/start/quake_dos_na_33_save_menu.start.png) [34](../shots/start/quake_dos_na_34_save_saved.start.png) [35](../shots/start/quake_dos_na_35_save_load_menu.start.png) | |
| Console | screen | backquote in play or demo -> back to play | commands and log | drops over the top half, the id 1.06 logo, typed lines with a ] prompt, answers ("godmode ON") | typing, Enter, backquote | answers in the log; pauses single player | [console](../shots/main/quake_dos_na_system_console.png) | |
| Weapon and ammo rows | hud element | always in play | arsenal | the eight weapon icons (lit when owned, highlighted when in hand), four ammo counters, keys and power-up icons at the right | 1-8 | the big ammo counter follows the weapon in hand | [armor_yellow](../shots/main/quake_dos_na_hud_armor_yellow.png) [weapon_lg](../shots/main/quake_dos_na_inventory_weapon_lg.png) | |
| Armor icon and value | hud element | status bar left | protection | green, yellow or red armor icon and the value; 666 under the Pentagram | - | changes on pickup | [armor_green](../shots/main/quake_dos_na_inventory_armor_green.png) [armor_red](../shots/main/quake_dos_na_inventory_armor_red.png) [power_pentagram](../shots/main/quake_dos_na_system_power_pentagram.png) | |
| Status face | hud element | status bar centre | health at a glance | the marine's face, bloodier as health falls; eyes only under the Ring | - | - | [power_ring](../shots/main/quake_dos_na_system_power_ring.png) | |
| Power-up tints | hud element | power-up active | which power-up runs | whole view tinted blue (Quad), gold-red (Pentagram), grey (Ring), green (Biosuit) | - | fades as the time runs out (source) | [power_quad](../shots/main/quake_dos_na_system_power_quad.png) [power_pentagram](../shots/main/quake_dos_na_system_power_pentagram.png) [power_ring](../shots/main/quake_dos_na_system_power_ring.png) [power_biosuit](../shots/main/quake_dos_na_system_power_biosuit.png) | |
| Damage flash | hud element | being hit | feedback | red tint, stronger with the damage; shown under god mode too | - | - | [act_knight](../shots/main/quake_dos_na_battle_act_knight.png) [boss_chthon_lava](../shots/main/quake_dos_na_boss_boss_chthon_lava.png) | |
| Completed screen | screen | level exit -> next level on a key | level results | COMPLETED plaque, time, secrets, kills over the exit view | fire / jump (source) | - | [intermission](../shots/main/quake_dos_na_system_intermission.png) | |
| Obituary and death view | message | death -> restart | who killed the player | one line at the top, the view on the floor, scores overlay | fire (source) | - | [gameover](../shots/main/quake_dos_na_gameover_gameover.png) | |
| Attract demo and main menu (again) | screen | demo loop, Esc | as in the start set | a later demo frame; the main menu | Esc | - | [title_demo](../shots/main/quake_dos_na_title_title_demo.png) [menu_main](../shots/main/quake_dos_na_menu_menu_main.png) | |
| Main view | screen | play | the world | first-person 3D view with the weapon in hand at the bottom centre | movement keys | - | [e1m1_start](../shots/main/quake_dos_na_gameplay_e1m1_start.png) | |

## 3. Screen flow
- Command line -> start-up console -> attract demos (loop) -Esc-> main menu (verified)
  - Single Player -> New Game -> start map (play) -> skill hall slipgate -> hub -> episode slipgate -> Loading -> E1M1
  - Single Player -> Load / Save -> slot list; Options -> Customize controls, Video Modes; Help/Ordering -> pages
- In play: Esc -> main menu (game paused); F2 -> Save list; TAB -> score overlay while held (verified)

## 4. Elements in detail
For the screens that carry the game (main view, status, combat, shop): each element on it, its position, what
it tells the player and when it changes.

## Open questions
