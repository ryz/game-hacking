# Dungeon Master - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
One paragraph or table each; "not applicable" where the game has none.
- **Input:** the mouse does everything (left button; one click picks up, a second puts down or swaps); the
  pointer is an arrow, or the leader's hand over the view and object boxes, or the carried object (verified,
  manual). Keyboard: numeric keypad for the six moves, F1-F4 for the inventories, Esc to freeze, typing in the
  name entry (verified). No confirmation for clicks; dialogs have buttons (verified).
- **Layout:** one fixed screen of 320x200: the party bar across the top (four champion boxes with name, two hands
  and three bars, formation icons at right), the dungeon view (or an inventory, or a dialog) at left centre, the
  spell panel, action buttons and movement arrows at right, three lines of messages below (verified).
- **Text:** capitals only, one font; each champion has a colour (green, yellow, red, blue) used for the bars, the
  formation icon and their messages ("WUUF RESURRECTED." in red) (verified).
- **Feedback:** short messages under the view ("RYZ REINCARNATED."); dialogs show progress ("FORMATTING DISK .
  . ." with a bar, "SAVING GAME . . ."); inactive controls are drawn hatched (verified).
- **State visibility:** bars for health, stamina and mana always; numbers, food, water and load only in the
  inventory; no map, no compass on screen (verified for what is shown).
- **Help and onboarding:** none in the game; the manual explains everything (source: manual).

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Entrance | screen | power-on -> hall (ENTER) / load dialog (RESUME) | start or resume | the dungeon doors, ENTER / RESUME / QUIT carved at right | click | the doors open | title_entrance | - |
| Hall view | screen | ENTER -> mirrors, gate | choose champions | corridors with mirrors | moves, clicks | - | hall_start | - |
| Champion panel | menu | click a mirror -> name entry / party | resurrect or reincarnate | portrait, name and title, body slots, possessions, health/stamina/mana, load | RESURRECT, REINCARNATE, CANCEL | message line | system_champion_panel | - |
| Name entry | prompt | REINCARNATE -> party | name the champion | first name and title lines, letter board, BACKSPACE, OK | clicks, keyboard | letters appear | system_reincarnate_name | **Observation:** the keyboard works although the manual describes only the letter board |
| Party bar | hud element | always | state of the four champions | names (leader highlighted), hands, health/stamina/mana bars | click bars (inventory), name (leader), hands | - | hud_party | - |
| Formation icons | hud element | always | positions of the champions | four coloured figures | drag | swap | system_formation | - |
| Spell panel | menu | always | cast spells | caster tabs, six runes, incantation line, recant arrow | clicks | symbols appear; caster's hand greys while recovering | system_runes | - |
| Action buttons / action list | menu | always | attack and use items | one button per champion with the action-hand object; list of actions | clicks | - | system_action_menu | - |
| Movement arrows | hud element | always | move | six arrows | clicks, keypad | - | hud_party | - |
| Inventory | screen | bars or F1-F4 -> view | items, statistics, food, sleep, save | slots, eye, mouth, food/water bars, numbers, load, disk/ZZZ/X icons | drag, clicks | - | inventory_ryz | - |
| Save dialog | menu | disk icon -> blank-disk prompt, saving | save, quit, format | "PUT THE GAME SAVE DISK IN DF0:" with SAVE / QUIT / FORMAT FLOPPY / CANCEL | clicks, disk changes | "THAT DISK IS UNREADABLE", progress messages | save_menu | **Observation:** no "game saved" message after saving: the dialog simply returns |
| Load dialogs | prompt | RESUME -> game | load a save | disk prompts, LOAD SAVED GAME, "GAME LOADED, READY TO PLAY." | clicks, disk changes | inserting the disk acts at once | save_resume_prompt, save_loaded | - |
| Freeze | message | Esc | pause | "GAME FROZEN", controls hatched | any input | - | system_freeze | - |
| Message lines | message | always | events | up to three coloured lines under the view | - | - | system_reincarnated | - |

## 3. Screen flow
- Power-on -> crack note (click) -> logo while loading -> Entrance
  - ENTER -> Hall view -> mirror -> Champion panel -> (REINCARNATE -> Name entry) -> Hall view with party
  - RESUME -> save-disk prompt -> game-disk prompt -> "GAME LOADED" -> dungeon view
- Dungeon view <-> Inventory (bars, F1-F4) -> Save dialog -> blank-disk prompt / saving -> back
- Dungeon view -> Esc -> Freeze -> back (verified)

## 4. Elements in detail
For the screens that carry the game (main view, status, combat, shop): each element on it, its position, what
it tells the player and when it changes.

## Open questions
