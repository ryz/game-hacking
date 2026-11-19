# Ultima III: Exodus (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima-3`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only. On the play screen one letter is one command, arrows move; the command then asks
  for a player number (1-4) and/or a direction (an arrow). In the menus (title, Organize, Create) a choice is a
  letter **and Enter**: the letter echoes the whole word ("Option:Organize") and Enter confirms; numbers are typed
  digits + Enter; words (Other command, Yell) are typed + Enter **(verified)**. A wrong key on the map is
  ignored or answered ("Not a DNG cmd!", "Enter <-What?", "Not Here!") **(verified)**.
- **Layout:** 320x200 in four CGA colours. Play screen: the map view (11x11 squares) at the left framed by a
  magenta border with the two moons "(a)(b)" on top and the wind ("North Wind") below; four status panels at
  the right (number, name, condition letter G/P/D/A, sex-race-class letters, M: magic points, L: level, H: hit
  points, F: food); the message area below them scrolls one line at a time **(verified)**. Menus use the same
  frame with the big cyan "Exodus" logo on top **(verified)**.
- **Text:** grey upper and lower case in a fixed 8x8 font; names keep the case typed ("ryz"); prompts end in
  "?" or "-"; a small triangle is the text cursor **(verified)**.
- **Feedback:** every action prints its name ("North", "Pass", "Enter Castle!") and its result; loading prints
  "Please wait..."; pictures (shrine, fountain, rod, Time Lord) replace the map view for the moment of the event
  **(verified)**.
- **State visibility:** the four panels always show H.P., food, magic and level; gold, statistics, equipment,
  cards and marks only through Ztats, one line per key **(verified)**. **Observation:** Ztats scrolls through
  the four-line message area, so a character sheet is never seen whole on the play screen (Look at a Character
  in the Organize menu shows one page).
- **Help:** none in the game; hints come from townspeople and the oracle **(ROM text)**.

## 2. Screen inventory
| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title | screen | power-on -> demo | identity | Exodus, Ultima III, by Lord British, a walking party and a dragon **(verified)** | nothing while drawing | - | `title_drawing`, `title_screen` | drawn slowly (40 s at the original speed) |
| Attract demo | screen | title -> main menu (space) | show play | a strip of Sosaria with moving ships and monsters, "Press <Space>" **(verified)** | space | - | `title_demo` | |
| Main menu | menu | demo -> Organize, Journey, demo | start | "From the depths of hell... he comes for VENGEANCE!", three options **(verified)** | R/O/J + Enter | - | `menu_main` | |
| Party Organization | menu | main -> register, create, form, disperse, terminate, look | roster | seven options **(verified)** | letter + Enter | "(No one there)", "(Party in Use)" **(ROM text)** | `menu_organize` | |
| Create | screen | Organize -> Organize | new character | Entry#, Points:50, form fields, O.K.? **(verified)** | digits, letters + Enter | "(Not Empty!)", "(1-20 Only!)" **(ROM text)** | `menu_create_*` | |
| Register | list | Organize | roster | entries 01-20 with sex-race-class-status letters and names **(verified)** | space | - | `menu_register` | |
| Form the Party | prompt | Organize | party | Player-1..4 = entry numbers, "(Formed)" **(verified)** | digits + Enter | "Already Selected" **(ROM text)** | `menu_form` | |
| Play screen | screen | Journey -> everything | play | map view, moons, wind, panels, messages **(verified)** | command keys | "Invalid Move!" | `hud_status` | |
| Status panel | hud element | play screen | party state | per player: number, name, G/P/D/A, letters, M:, L:, H:, F: **(verified)** | - | updates each turn | `hud_status` | |
| Message area | hud element | play screen | log and prompts | the last seven lines or so **(verified)** | - | - | all | |
| Ztats | message | Z -> play | character sheet | one line per key: statistics, H.P., H.M., gold, exp., gems, keys, powders, torches, cards, marks, weapon, armour, owned arms **(verified)** | any key | - | `ztats_*` | slow to read |
| Peer at gem | screen | P -> play | map | miniature of the whole land **(verified)** | any key | - | `peer_gem` | |
| Combat screen | screen | a fight -> play | battle | the 11x11 field, "---Conflict!!---", "->Orcs", "----Player 1----" **(verified)** | arrows, A, C, R, space | "Missed!", "Hit!", "Killed! Exp.+03", "****Victory!****" | `battle_*` | |
| Dungeon view | screen | E on a dungeon -> play | explore | first-person walls, "LVL:01", "Head--East" **(verified)** | arrows, K, D, I | "It's dark!", "Not a DNG cmd!" | `dungeon_*` | |
| Event pictures | screen | shrine, fountain, rod, Time Lord | moments | a full picture in the map view with its text **(verified)** | player, number | "Shazam!", "How wonderful!", "It left a mark!" | `shrine_enter`, `dungeon_fountain`, `dungeon_rod`, `timelord` | |
| Shop dialogue | message | T over a counter | trade | the shop's name and lists in the message area **(verified)** | letters, Y/N, numbers | "Not enough gold!", "Out you scum!" **(ROM text)** | `shop_*` | |
| Talk | message | T with a person | hints | the person's line **(ROM text)** | - | "No One There" | `talk_*` | |
| Quit & Save | message | Q | save | "Quit & Save", moves, "Please wait..." **(verified)** | - | - | `save_quit` | play goes on |
| All Players Out | message | all dead | game over | the message and a still screen **(verified)** | nothing | - | `gameover` | |
| Ending | screen | the fourth card | end | "Congratulations!...", the moves, "Report thy feat!" in the messages, the closing text in the map view **(verified)** | nothing | - | `ending_*` | |

## 3. Screen flow
- power-on -> title -> attract demo -> (space) main menu
  - Organize a Party -> register / create / form / disperse / terminate / look -> main menu
  - Return to the View -> attract demo
  - Journey Onward -> play screen (Sosaria)
    - E -> towne / castle (walk off the edge back to Sosaria), dungeon (ladder up on level 1 back)
    - a monster -> combat screen -> play screen (chest)
    - whirlpool -> Ambrosia (shrine pictures) -> whirlpool -> Sosaria
    - moongate -> another square of Sosaria
    - fourth card in Castle Exodus -> ending (stays)
    - all dead -> "All Players Out!" (stays)

## 4. Elements in detail
Play screen (verified, `start`): map view 176x176 pixels at the left (11x11 squares of 16x16), the party in the
centre; moons "(0)(1)" centred on the top border; the wind name centred on the bottom border; four panels of
three lines at the right (row 1: number in the border, name, condition letter at the far right; row 2: sex,
race and class letters, M:nn, L:nn; row 3: H:nnnn, F:nnnn); the message area (about seven lines) at the bottom right,
each command line led by a small arrow.

## Open questions
- The Organize screens Disperse, Terminate and Look were not opened yet; the combat screen's spell lists.
