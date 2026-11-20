# Dungeon Master - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py amiga/dungeon-master`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** the mouse does everything with the left button: one click picks an object up (the pointer becomes
  the object, its name shows above the spell panel), a second click puts it down, uses it on a lock, drops it on
  the mouth (verified: `system_key_taken`, `inventory_feed`). Over the view the pointer is the leader's hand;
  elsewhere an arrow (verified). The keyboard duplicates the six moves on the numeric keypad, opens the four
  inventories with F1-F4, freezes with Esc and types names (verified). There are no confirmations: clicks act at
  once; dialogs (save, load) have big buttons (verified).
- **Layout:** one fixed 320 x 200 screen (verified: `hud_party`): the party bar across the top (four champion
  boxes, formation icons at right), the dungeon view at left (it is replaced by the inventory, a champion panel
  or a dialog), at right the spell panel, the action buttons and the movement arrows, three lines of messages
  under the view.
- **Text:** capitals in one small font; each champion has a colour (RYZ green, Tiggy yellow, Wuuf red, Stamm
  blue) used for his bars, his formation figure and his messages ("WUUF RESURRECTED." in red) (verified). The
  ending and the final roll use a gothic display font (verified: `gameover_the_end`, `ending_champions`).
- **Feedback:** damage numbers in red splashes on the bar of a hurt champion and in a starburst over the action
  button of a striking one (verified: `battle_trolin`, `battle_hit`); short messages under the view
  ("RYZ JUST GAINED A FIGHTER LEVEL!") (verified); hatched controls mean "not available now" (a recovering
  champion's action icon, everything while frozen or asleep) (verified: `system_freeze`, `system_sleep`).
- **State visibility:** the three bars (health, stamina, mana) are always visible; the numbers, food, water and
  load only in the inventory; statistics only while the eye is held (verified). No map and no compass on screen
  (verified; a compass exists as an object, ROM text). Dead champions keep their box with a skull (verified).
- **Help and onboarding:** none in the game; the manual explains the controls (source: manual). The first
  rooms teach by placement: a key lies under its lock, a button sits on the gate it opens (verified:
  `gameplay_lock_key`).

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Crack note | screen | power-on -> logo | this release's crack intro (not the game) | hires AmigaDOS window of text | left click | - | `boot_crack_note` | - |
| Loading logo | screen | crack note -> entrance | covers the 80 s floppy load | the Dungeon Master logo | nothing | nothing moves while loading | `boot_logo` | **Observation:** no progress sign during a long load |
| Entrance | screen | logo -> hall (ENTER), load (RESUME) | title and main menu in one | the dungeon doors, ENTER / RESUME / QUIT carved at right | click | the doors swing open (clip) | `title_entrance`, `cutscene_doors_open` | - |
| Dungeon view | screen | always | the world in first person | three squares deep, walls, ornaments, objects, creatures | clicks with the hand, keypad | - | `hall_start`, `env_l2_corridor`, `env_l14_corridor` | - |
| Dark view | screen | no light | the same without light | only outlines | the same | - | `env_l2_dark` | - |
| Champion panel | menu | click a mirror -> name entry / party | resurrect or reincarnate | portrait, name and title, body slots with possessions, health/stamina/mana, load, RESURRECT, REINCARNATE, CANCEL | the three buttons | message line | `system_champion_panel`, `hall_champion_lizard`, `hall_champion_wizard`, `hall_champion_ninja`, `hall_champion_priestess`, `hall_champion_gothmog` | - |
| Name entry | prompt | REINCARNATE -> party | name the champion | first name and title lines, letter board, BACKSPACE, OK | clicks and the keyboard | letters appear | `system_reincarnate_name` | **Observation:** the keyboard works although the manual describes only the letter board |
| Party bar | hud element | always | state of the four champions | names (the leader's in orange), ready and action hands, three bars | click bars (inventory), name (leader), hands | damage splashes; skull when dead | `system_party_four`, `system_leader`, `gameover_party_dead` | - |
| Formation icons | hud element | always | who stands where | four coloured figures in a 2 x 2 square | drag | - | `system_party_four` | - |
| Spell panel | menu | always | build and cast spells | caster tabs, six rune buttons, incantation line, recant arrow | clicks | the runes appear on the line, the next row of runes shows | `system_runes`, `system_magic_light`, `system_spell_fireball` | - |
| Action buttons and list | menu | always | attack and use items | one button per champion with his action-hand object; the list of that object's actions | clicks | hatched while recovering; damage starburst | `system_action_menu`, `system_action_wuuf`, `battle_hit` | - |
| Movement arrows | hud element | always | move | six arrows | clicks, keypad | hatched while frozen | `hud_party` | - |
| Object name line | message | an object in hand | names the carried object | e.g. GOLD KEY, SCREAMER SLICE above the spell panel | - | - | `system_key_taken`, `system_pick_up` | - |
| Inventory | screen | bars or F1-F4 -> view | items, food, water, sleep, save | slots, eye, mouth, food/water bars, numbers, load, disk/ZZZ/X icons | drag, clicks | - | `inventory_ryz`, `inventory_tiggy`, `inventory_potion`, `system_drink`, `inventory_tiggy_late` | - |
| Statistics | screen | eye held | the champion's statistics | six statistics as current/maximum | hold | disappears on release | `inventory_stats` | **Observation:** only visible while the button is held, easy to miss |
| Object description | screen | an object held on the eye | name and weight | icon, name, WEIGHS n KG | hold | - | `inventory_examine` | - |
| Feeding | element | object over the mouth | eat / drink | the object as pointer on the mouth | click | food or water bar grows | `inventory_feed`, `system_eat` | - |
| Sleep | screen | ZZZ -> view | rest | black view, WAKE UP, everything hatched | any click | - | `system_sleep` | - |
| Freeze | message | Esc | pause | GAME FROZEN, controls hatched | any input | - | `system_freeze` | - |
| Message lines | message | events | report | up to three coloured lines under the view | - | - | `system_reincarnated`, `system_resurrected`, `system_level_up` | - |
| Save dialog | menu | disk icon -> blank-disk prompt / saving | save, quit, format | PUT THE GAME SAVE DISK IN DF0: with SAVE / QUIT / FORMAT FLOPPY / CANCEL | clicks, disk changes | progress text with a bar | `save_menu`, `save_blank_prompt`, `save_formatting`, `save_saving` | **Observation:** no "game saved" message after saving: the dialog simply returns |
| Load dialogs | prompt | RESUME -> game | load a save | disk prompts, LOAD SAVED GAME, GAME LOADED, READY TO PLAY. | clicks, disk changes | inserting the disk acts at once | `save_resume_prompt`, `save_loaded` | - |
| The End | screen | all champions dead | game over | "The End" on dark blue | - | - | `gameover_the_end` | - |
| Ending | cutscene | FUSE on Lord Chaos -> final roll | the victory | the fusion in the view, the Grey Lord's words in the message lines | nothing (plays by itself) | - | `boss_chaos_fused`, `ending_lord_order`, `ending_fusion`, `ending_grey_lord`, `ending_truth`, `ending_harmony`, `ending_names` | **Observation:** the action list stays open over the whole ending |
| Final roll | screen | ending | the champions remembered | four portraits with names, titles and skill ranks | - | - | `ending_champions` | - |

## 3. Screen flow
- Power-on -> crack note (click) -> logo while loading -> Entrance
  - ENTER -> doors open -> Hall view -> mirror -> Champion panel -> (REINCARNATE -> Name entry) -> view with party
  - RESUME -> save-disk prompt -> game-disk prompt -> GAME LOADED -> view
- View <-> Inventory (bars, F1-F4) -> Save dialog -> blank-disk prompt / saving -> back; ZZZ -> Sleep -> view
- View -> Esc -> Freeze -> view
- View -> all champions dead -> The End
- View -> FUSE on Lord Chaos -> Ending -> Final roll

## 4. Elements in detail
The main screen (`hud_party`), from top left:
- **Champion boxes** (four, 69 px wide): name (orange for the leader), ready hand and action hand (the hand
  icons show the objects held), three bars in the champion's colour: health, stamina, mana. Clicking the bars
  opens that champion's inventory (verified), the name makes him leader (verified).
- **Formation icons** (top right): four little figures in the champions' colours, arranged as the party
  stands, front row at the top (verified).
- **Dungeon view** (224 x 136): three squares deep and one to each side; objects on the floor are drawn in the
  four corners of each square (verified: the key in the front-left corner, `gameplay_lock_key`).
- **Spell panel** (right, top): tabs for the caster (the leader's name in the large tab, the others small), six
  rune buttons, the incantation line with the recant arrow (verified).
- **Action buttons** (right, middle): one per champion with the icon of his action-hand object; a click opens
  that object's action list in the same place, a click on an action performs it (verified).
- **Movement arrows** (right, bottom): turn left, forward, turn right; step left, back, step right (verified).
- **Message lines** (under the view): the last three events, in the colour of the champion concerned (verified).

## Open questions
- The leader's hand pointer shape over objects and walls was not captured (the pointer is hidden in shots).
- Dragging a formation figure did not show the figure under the pointer in a captured frame (tried).
