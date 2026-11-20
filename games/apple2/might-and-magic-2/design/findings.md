# Might and Magic II: Gates to Another World - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The status line shows year 900 again after an event in another century
**Behavior:** with the century set to 800 the status line reads "Year= 800" when the area loads
(`system_year_800`), but after a step onto an event square (Castle Xabran's gate, King Kalohn) it reads
"Year= 900" while the game still treats the party as being in year 800 (the castle stands, Kalohn speaks)
(`gameplay_xabran_800`, `dialogue_kalohn_asks`).
**Intended:** unclear; probably the event redraw prints the home century.
**Confidence:** (verified) on screen; the century was set through memory, not by the game's own time travel,
so the in-game path may redraw differently (inferred).
**Impact:** cosmetic; a player could misread which century the party is in.

## Resting can pull the party back to its own century
**Behavior:** the rest command checks the century: outside year 900 a random roll can set it back to 900 and
move the party (the game code compares the century with 9 and on one result of a roll writes 9 and a new
square). A century set to 800 was back at 900 after four rests.
**Intended:** yes: the manual's "your stay in any century is limited" (source: DOS playbook).
**Confidence:** (RAM) code read, (verified) the reset after resting.
**Impact:** time in the past is limited; plan the visit to King Kalohn without resting.

## The Square Lake gate opens for a party that has not saved King Kalohn
**Behavior:** a fresh party poked to levels 29-31, without any quest done, gets Sheltem's speech and the final
fight at the gate (`boss_sheltem`, `boss_sheltem_options`); the DOS version refuses with "You shouldn't be here
until you save the King in the 9th century".
**Intended:** the DOS check (inferred).
**Confidence:** (verified) the gate opened; whether the Apple version checks another condition (party level)
was not tested.
**Impact:** the final fight can be reached early (it cannot be won early: the elementals kill a level-30 party
in two rounds).

## Breath damage follows the monster's remaining hit points
**Behavior:** with the Elementals' hit points set to 0 their breath did 0 points ("condi takes 0 pts"), while
their blows still did over 100 (`boss_sheltem_breath` shows the normal case).
**Intended:** yes, as in other Might and Magic games (breath = a part of the monster's hit points) (inferred).
**Confidence:** (RAM).
**Impact:** wounding a breather first weakens its breath.
