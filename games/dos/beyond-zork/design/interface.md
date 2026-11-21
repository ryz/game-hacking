# Beyond Zork: The Coconut of Quendor (DOS) - interface (UI/UX lens)

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

## 3. Screen flow
Which screen leads to which, as an indented list or a text diagram, from power-on through the main loop.

## 4. Elements in detail
For the screens that carry the game (main view, status, combat, shop): each element on it, its position, what
it tells the player and when it changes.

## Open questions
