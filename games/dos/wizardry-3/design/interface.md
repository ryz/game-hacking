# Wizardry III: Legacy of Llylgamyn (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry-3`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only; every menu entry is chosen by its initial letter or a digit, Enter (drawn as a bent
  arrow) leaves or confirms; roster lists by letter A-T; prompts take Y/N; riddles take typed text (verified).
  Keys pressed during a "One moment" load are lost (verified).
- **Layout:** 320 x 200 CGA, white frames on black with cyan/magenta pictures; the party list (# name class AC hits
  status) at the bottom of the Castle, camp and maze screens; the maze view above it with a one-line command bar
  "C)amp S)tatus I)nspect O)ff A-W-D K" (verified).
- **Text:** capitals only; "OF" drawn as one ligature glyph in item names; the Enter key drawn as a bent arrow
  (verified).
- **Feedback:** messages in boxes over the view, most with "Press Enter"; refusals in boxes ("* Bad alignment *",
  "You can't walk through walls!", "That character is already a legacy!", "You are forbidden to enter here!
  Begone!!") (verified).
- **State visibility:** the party list always shows class, AC, hit points and status; place and facing are not
  shown (no map, no coordinates) (verified).
- **Help and onboarding:** none in the game; run.bat prints the transfer steps (verified).

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title | screen | power-on -> Castle | start or make a disk | logo, scenario name, monster picture | S, M | - | `title_screen` | |
| Castle "Llylgamyn" | menu | title, Utilities, Training -> Tavern, Inn, Temple, Boltac's, Edge | town hub | five places, party list | G A T B E | - | `menu_castle_start` | |
| Gilgamesh's Tavern | menu | Castle | form the party | A)dd R)emove #)Inspect D)ivvy gold | letters | "* Bad alignment *" | `menu_tavern*` | |
| Edge of Town | menu | Castle -> Training, Maze, Utilities, Leave | leave town | five entries | T M C U L | - | `menu_edge` | |
| Wizardry Utilities | menu | Edge -> Move characters | disk work | C)hange name M)ove characters R)estart an "out" party | C M R, Enter (to the Castle) | - | `menu_utilities` | |
| Move characters | list | Utilities | import from Wizardry I/II | "1)Proving Grounds 2)Knight of Diamonds", then the old roster with "+" marks | 1/2, letters, Enter, Esc | - | `menu_move_*` | **Observation:** the source disk prompt is answered by the 1998 loader, the player never sees it |
| Training Grounds | menu | Edge -> inspect, roster | manage characters | I)nspect R)oster Leave (no create) | I R | - | `menu_training` | |
| Character options | menu | Training inspect | per character | L)egate I)nspect D)elete C)hange class A)lter password | letters | "That character is already a legacy!" | `menu_char_options` | |
| Rite of passage | message + prompt | L)egate | the legacy | ceremony text, then "Choose an alignment for descendant" with only the allowed letters | Enter, A/B/C | wrong letters ignored | `dialogue_rite`, `menu_alignment*` | |
| Character sheet | screen | Tavern, Training, camp | statistics | name, level, alignment-class, race, awards in quotes, six statistics, gold, E.P., HP, AC, age, spell points, items 1-8 | R T P E D I (camp: S U) | - | `inventory_*` | |
| Camp | menu | entering the maze, C | between steps | #)Inspect R)eorder E)quip Leave | digits, letters | - | `camp_menu` | |
| Maze view | screen | camp -> fights, messages, stairs | explore | wireframe view, command bar, party list | W A D K C S I O | "You can't walk through walls!" | `gameplay_*` | |
| Stairs prompt | prompt | stairs squares | change floor | "Stairs up/down take them (Y/N) ?" | Y N | refusal box | `gameplay_stairs_up` | |
| One moment | transition | stairs to floors 5 and 6, warps | loading | "One moment" box | none (keys lost) | - | `gameplay_one_moment` | **Observation:** up to 30 seconds at 8088 speed |
| Message box | message | special squares | story, signs | text, sometimes a picture, "Press Enter" | Enter | - | `dialogue_*` | |
| Search prompt | prompt | search squares | take or swap items | "Will you search (Y/N) ?" | Y N | - | `dialogue_search` | |
| Riddle prompt | prompt | riddle squares | gate | "What is your answer ?" | text, Enter | wrong: pushed back | `dialogue_riddle_*` | |
| Combat | screen | fights | battle | groups with counts, picture, member options, messages | F P S D U R T, digits | - | `battle_*` | |
| Chest | menu | after fights | loot | "A chest! You may: O)pen C)alfo L)eave alone I)nspect D)isarm" | O C L I D | - | `battle_chest` | |
| Ending | screens | the orb in the Castle | the end | Congratulations prompt, the Queen's page, star prompts | Y N, Enter | - | `ending_*` | |
All rows (verified) in play on 2026-11-19 (playbook checkpoints); shot ids are planned.

## 3. Screen flow
```
power-on -> DOSBox Pure menu (front end) -> title -S-> Castle
Castle -G-> Tavern | -A-> Inn | -T-> Temple | -B-> Boltac's | -E-> Edge of Town
Edge -T-> Training (inspect -> L)egate rite -> alignment) -> Castle
Edge -U-> Utilities -M-> Move characters (1/2 -> old roster -> moved) -> Castle
Edge -M-> camp -> maze <-> fights, chests, messages, stairs; stairs down on floor 1 (0,0) -> Castle
Edge -L-> "Thanks for playing Wizardry!" (program ends)
Castle with the orb -> Congratulations -> the Queen's page -> star prompts -> Castle
```

## 4. Elements in detail
- **Maze screen:** command bar on top (one line); the wireframe view (doors as frames, stairs as hatched bars,
  dark squares a grey fill) in the middle; the party list below with six rows (verified).
- **Character sheet:** first line "NAME L level A-CLA RACE "awards"" - the awards string is where the legacy shows
  ("">DG"" for RYZ after the rite) (verified).

## Open questions
- Inn, Temple and Boltac's screens past their first page were not opened in this scout.
