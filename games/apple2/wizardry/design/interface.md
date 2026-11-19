# Wizardry: Proving Grounds of the Mad Overlord - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only. A choice is one letter, printed in the text with a bracket (`A)DD A MEMBER`,
  `[A] THE STABLES`); party members are chosen by number 1-6; names of characters, spells and traps are typed
  and ended with Return; Return alone means leave, none or go on wherever the text says `[RETURN]` / `[RET]`
  **(verified)**. A wrong key is ignored without a message; a wrong password returns to the prompt before
  **(verified)**. Keys typed while the disk works are lost **(verified)**.
- **Layout:** two kinds of screen. Castle, Training Grounds, camp, sheets and shops are 40-column upper-case
  text: a framed header (`! CASTLE   MARKET !`, the right word names the place), the party table, then the
  options as a sentence **(verified)**. The maze, fights and chests are a hi-res screen in four panes: the
  view or monster picture top left, commands or the monster groups top right with a `SPELLS :` line, a
  message pane in the middle, the party table at the bottom **(verified)**.
- **Text:** capitals only; white in text mode, green with purple frame lines in the hi-res panes on a colour
  set **(verified, colour TV picture)**. Abbreviations in the party table: `G-FIG`, `N-THI` (alignment-class),
  `AC`, `HITS`, `STATUS` (shows hit-point maximum when OK, else the condition) **(verified)**.
- **Feedback:** results are timed messages in the middle pane (the T)ime command sets the delay); errors are
  short starred lines (`** WHO? **`, `** THATS NOT IT **`: program text); irreversible steps ask
  (`ARE YOU SURE YOU WANT TO DELETE (Y/N) ?`, `CONFIRM (Y/N) ?`, `KEEP THIS CHARACTER (Y/N)? >`) **(verified)**.
- **State visibility:** the party table (class, armour class, hit points, status) is on almost every screen;
  gold, experience, age, spell points and the pack need the character sheet; the position needs the DUMAPIC
  spell; there is no map **(verified)**.
- **Help and onboarding:** every screen lists its own keys; the maze pane lists all commands permanently;
  nothing explains classes, spells or scores (the manual does) **(verified; the manual was not read)**.

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Opening animation | transition | power-on -> title | sets the tone | "PREPARE YOURSELF FOR THE ULTIMATE IN FANTASY GAMES", wizard, cauldron, smoke forming the logo; loops | any key | - | `title` | **Observation:** 30 s before the logo is complete |
| Boot menu | menu | title -> Castle, Utilities, title | start, copyright, version | copyright text, version and serial, `S)TART GAME U)TILITIES T)ITLE PAGE` | `s u t` | - | `menu` | |
| Disk prompts | prompt | boot menu -> Castle | disk change | `SCENARIO MASTER IN DRV 1, PRESS [RET]`, then `MASTER/DUPLICATE IN DRV 1, PRESS [RET]` | Return | `NOT SCENARIO DISK` (program text) | `menu` + `s` | |
| Utilities | menu | boot menu | disk and roster maintenance | seven entries (recover, transfer, backup, make scenario disk, update, change names, leave) | letters | - | `@menu,u` | |
| Castle | menu | start, every castle place | hub | header, party table, the five places as a sentence | `a g b c e` | - | `castle`, `start` | |
| Tavern | menu + prompt | Castle | form the party | party table, add / remove / see, `WHO WILL JOIN ? >`, `ENTER PASSWORD  >` | letter, typed name, Return | `** WHO? **`, `** OUT **`, `** BAD ALIGNMENT **`, `** THATS NOT IT **` (program text) | `start` route | **Observation:** the password is asked even when none was set |
| Inn | menu | Castle | rest and level up | `WHO WILL STAY`, five rooms with prices, then healing and the experience needed | digit, `a`-`e`, Return | - | `@vet,a,w300,1,w400` | |
| Temple | prompt | Castle | cure | `WELCOME TO THE TEMPLE OF RADIANT CANT!`, `WHO ARE YOU HELPING ? >`, donation, `WHO WILL TITHE` | typed name, digit | `IS NOT HERE`, `IS OK`, `CHEAP APOSTATES! OUT!` (program text) | `@vet,c,w400` | |
| Trading post | menu + list | Castle | buy, sell, uncurse, identify | `WHO WILL ENTER`, gold, four services; stock six per page with prices | digit, `b s u i l`, `p f b s l` | `YOU CANNOT AFFORD IT`, `YOU CANT CARRY ANYTHING MORE`, `UNUSABLE ITEM - CONFIRM BUY` (program text) | `@vet,b,w300,1,w400,b,w500` | |
| Edge of Town | menu | Castle | leave the castle | maze (party only), training grounds, castle, leave the game | `m t c l` | - | `edge` | |
| Training Grounds | prompt | Edge of Town | make and edit characters | instructions and `NAME >` | typed name, `*ROSTER`, Return | `THERE IS NO ROOM LEFT - TRY DELETING`, `NAME ALREADY IN USE` (program text) | `@start,e,w300,t,w300` | **Observation:** no menu, the name is the command |
| Roster | list | Training Grounds | names in use | one line per character: name, level, race, class, (status) | `l` | - | `...type:*ROSTER\n` | long names are cut at column 40 (verified: DIRK THE DARING) |
| Creation form | screen | Training Grounds | build a character | the form fills line by line: name, password, race, points, six scores with an arrow, alignment, class; eligible classes appear beside the scores | Return, letters, `+ -`, Esc, `y n` | Esc is refused while points are left (DOS: verified; here: inferred) | `start` route | |
| Character options | menu | Training Grounds (known name + password) | edit | summary line, inspect / delete / reroll / change class / set password | `i d r c s`, Return | Y/N confirmations | `...type:RYZ\n,w300,enter` | |
| Character sheet | screen | Tavern, camp, Training | everything about one member | name line (with `">"` after the ending), scores, gold, experience, level, age, hits, AC, status, spell points by level, legend, pack in two columns, options that fit the place | `e d t r s u i l` | `NOT EQUIPPED`, `CURSED`, `NOT BISHOP`, `YOU CANT CAST IT` (program text) | `@gcamp,1` | |
| Spell books | list | sheet | known spells | mage or priest spells grouped by level in two columns | `m p l` | - | `@start,VET,g,w300,5,w400,r,w300,m,w400` | |
| Equip | prompt | camp, sheet | wear items | `SELECT WEAPON FOR RYZ`, numbered candidates, `WHICH ONE ([RET] FOR NONE) ? >`; then armor, shield, helmet, gauntlets, misc | digit, Return | `** CURSED **` (program text) | `gcamp` route | only slots with a candidate are asked (verified) |
| Camp | menu | maze `c`, maze entry | manage the party in the maze | party table, reorder / equip / disband / inspect / leave | `r e d`, digit, `l` | `CONFIRM (Y/N) ?` | `camp` | |
| Maze screen | screen | camp | explore | view (wireframe), command list, `SPELLS :` (active party spells), message pane, party table | `f l r k c s q t i`, `a w d` | `OUCH!` in the view | `maze1` | |
| Stairs, elevator, messages | prompt | maze squares | level changes and story | `STAIRS GOING UP. TAKE THEM (Y/N) ?`, `THERE ARE BUTTONS ON THE WALL MARKED A THROUGH D. PRESS ONE (OR RETURN TO LEAVE THEM)`, quoted signs, `[RET] FOR MORE` | `y n`, letters, Return | - | `maze1` route, `werdna_sign` | |
| Battle | screen | maze | fights | monster picture, numbered groups `1) 3 SLIMES (3)` (count and how many can act), `RYZ'S OPTIONS`, messages, party table | `f s p r u d`, digits, typed spell, Return, `b` | `YOU DONT KNOW THAT SPELL`, `SPELL POINTS EXHAUSTED` (program text) | `battle`, `werdna` | |
| Victory and chest | screen | battle | rewards | `FOR KILLING THE MONSTERS EACH SURVIVOR GETS 27 EXPERIENCE POINTS`, chest picture, `A CHEST! YOU MAY: O)PEN C)ALFO L)EAVE I)NSPECT D)ISARM` | `o c l i d`, digit, typed trap | `DISARM FAILED!!`, `YOU SET IT OFF!` (program text) | `chest` | |
| Location and teleport | screen | camp spells | DUMAPIC report; MALOR displacement counters | text | `l`; `n s e w u d`, Return, Esc | failure texts (playbook) | `malor_home` route | |
| Ending | screen | stairs up with the amulet | reward | the Congratulations text | Return | - | `ending` | |
| Leave game | screen | Edge of Town | end the session | `PRESS [RETURN] FOR MORE WIZARDRY` | Return | - | `@final,e,w300,l,w900` | |

## 3. Screen flow
No shot set exists yet: the Shots column names the checkpoint or route that reaches the screen
(`../checkpoints.txt`). Rows are **(verified)** on screen unless a cell says program text.

- power-on -> opening animation -> (key) -> boot menu
  - `U` utilities; `T` title again
  - `S` -> two disk prompts -> **Castle**
    - Tavern (add by name, remove, see -> sheet) ; Inn ; Temple ; Trading post (services -> stock pages)
    - Edge of Town
      - Training Grounds (name -> creation form, or options -> sheet / delete / reroll / class / password; roster)
      - Leave game -> "FOR MORE WIZARDRY" -> disk prompts -> Castle
      - Maze -> Camp -> maze screen
        - `C` camp -> sheet -> spell books, equip, spells (DUMAPIC, MALOR)
        - squares: stairs (up from floor 1 = Castle), elevator, messages
        - encounter -> battle rounds -> victory -> chest -> maze screen; or the cemetery
        - Castle with the amulet -> ending -> Castle

## 4. Elements in detail
- **Party table** (bottom pane in the maze, upper block in the castle): `# CHARACTER NAME  CLASS AC HITS
  STATUS`; STATUS repeats the hit-point maximum while the member is OK and becomes `DEAD`, `STONED` ... (the
  hit points then print as 0 or with a dash: `47-STONED`) **(verified in the Werdna tries)**.
- **Group lines** in battle: `2) 1 W E R D N A (1)`: group number, how many, name as far as it is known, and in
  brackets how many of them are able to act **(verified: counts; the meaning of the bracket is the DOS
  documents')**.
- **Maze view**: about a quarter of the screen width; walls as purple outlines, doors as an inner frame, dark
  squares draw nothing **(verified)**.
- The rest: to be written by the capture run from the shots.

## Open questions
- The Inn's level-up screen, the Temple's cure sequence, trading and the chest results were not opened.
- What Status and Quick plot change on the maze screen.
