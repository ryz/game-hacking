# Wizardry II: The Knight of Diamonds - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/wizardry-2`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
Wizardry I's conventions on this machine apply ([interface](../../wizardry/design/interface.md)): letters and
typed names, capitals only, 40-column text screens for the town and a hi-res screen with drawn text for the
maze **(verified by the screens listed below)**. Differences found: the title wants Return **(verified)**.
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
| Title picture | screen | power-on -> copyright menu | name the game | logo, knight and dragon, "KNIGHT of DIAMONDS" **(verified)** | Return (space does nothing) | none | `title` | **Observation:** nothing says which key continues |
| Copyright menu | menu | title -> game, utilities, title | start | copyright, version, `S)TART GAME U)TILITIES T)ITLE PAGE` **(verified)** | `S U T` | - | `menu` | - |
| Utilities | menu | copyright menu -> each utility; L)eave asks for the boot disk | disk housekeeping | `R)ECOVER T)RANSFER B)ACKUP M)AKE SCENARIO DISK U)PDATE C)HANGE NAMES L)EAVE` **(verified)** | letters | - | route in playbook | - |
| Transfer | prompts and list | Utilities -> Utilities | move a character between scenario disks | begin/exit line, "INSERT SCENARIO WITH CHAR(S) TO BE MOVED", the source's name and characters by letter, "MOVING RYZ / PASSWORD >", "INSERT SCENARIO TO MOVE CHAR(S) TO", "CHAR HAS BEEN MOVED" **(verified)** | Return, Esc, letter, password | "CANT COPY TO BACKUP", "DUPLICATE NAME", "ALL SLOTS USED - PUT IN SOURCE", "CHAR HAS NON-XFERRABLE ITEMS" **(program text)** | route in playbook | **Observation:** two disk changes per character, six characters take twelve |
| Disk prompts | prompt | start, utilities | ask for a disk | "SCENARIO MASTER IN DRV 1, PRESS [RET]", "MASTER/DUPLICATE IN DRV 1, PRESS [RET]", "PLACE BOOT DISK IN DRIVE 1, PRESS RETURN" **(verified)** | Return | - | route in playbook | - |
| Castle | menu | start -> the five places | hub | box with "LLYLGAMN" and the place name, the party table, the choices **(verified)** | `A G B C E` | - | `start`, `gcastle` | - |
| Training Grounds | prompt | Edge of Town -> Castle | inspect or delete | the "cannot create" text, "NAME >" **(verified)** | name, `*ROSTER`, Return | disbands the party without saying so | route in playbook | **Observation:** the party list is empty afterwards |
| Camp, sheet, equip | menus | maze entry, `C` | party care | as Wizardry I **(verified: camp, a sheet, 19 equip prompts)** | digits, letters | - | `camp`, `gcamp` | - |
| Maze view | screen | camp -> everything below | play | wireframe view, command list, "SPELLS :" box, message box, party table with AC and hits (`LO`, `112+` with the five pieces) **(verified)** | `F L R K C Q T S I` | "AN ENCOUNTER" before a fight | `maze1`, `gmaze` | - |
| Message pages | message | special squares | story | text in the message box, "[RET] FOR MORE" or "PRESS [RET]" in the spell box **(verified)** | Return | - | `sphinx`, `gnilda_test`, `staff_gift` | - |
| Riddle prompt | prompt | Gnilda's temple (and the sphinx, source) | typed answer | "ANSWER ?" and a block cursor **(verified)** | text + Return | - | `gnilda_answer` | - |
| Battle | screen | encounter | fight | monster picture, groups with counts, "RYZ'S OPTIONS", surprise line **(verified)** | `F S P R U`, group digit, Return, `B` | "PRESS [RET] TO FIGHT, OR GO B)ACK AND RE-ENTER." | `battle`, `guard1`-`guard5` | - |
| Chest | menu | after a fight | loot | experience line, chest picture, `O)PEN C)ALFO L)EAVE I)NSPECT D)ISARM` **(verified)** | letters | - | `chest` | - |
| Ending | screen | stairs with the staff | reward | "*** GAUDEAMOUS ***" text screen **(verified)** | Return | - | `ending` | - |
| Awards | prompt | ending -> Castle | knighthoods | "KNIGHTHOODS LEFT : 5 / AWARD ONE TO CONDI (Y/N) ? >" **(verified)** | `Y N` | counter goes down | `knights` | - |

## 3. Screen flow
Power-on -> title -> copyright menu -> (Utilities -> Transfer -> Utilities -> boot disk prompt -> copyright
menu) -> scenario disk prompts -> Castle -> Tavern / Inn / Trading post / Temple / Edge of Town -> Training
Grounds or Camp -> Maze -> Battle -> Chest -> Maze -> stairs -> Castle; with the staff: stairs -> Ending ->
Awards -> Castle **(verified)**.

## 4. Elements in detail
For the screens that carry the game (main view, status, combat, shop): each element on it, its position, what
it tells the player and when it changes.

## Open questions
- Trading post, Temple, sheet commands, chest results, the other utilities: not opened by the scout.
