# Wizardry II: The Knight of Diamonds (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The ending needs a party of one
**Behavior:** carrying the Staff of Gnilda into the Castle with a party of six only makes the staff disappear
(no message, no reward); the same with the bearer alone gives the Congratulations screen (scout routes:
`@start,STAFF,HOMESTAIRS` vs `@start,SOLO,STAFF,HOMESTAIRS`). Gnilda's test also answers only a lone bearer.
**Intended:** yes: the apparition says "One alone." on floor 6 (1,3).
**Confidence:** (verified)
**Impact:** a player who brings the staff back with the whole party loses it and must win the five pieces
again (inferred: the guardians fight on every visit).

## Imported characters show their old armour class until the first camp
**Behavior:** after Move characters the Castle list still shows Wizardry I's AC (-4, -1, 3 ...) although the
packs are empty; the first camp shows AC 10 for all (`start` vs `camp`).
**Intended:** no (a display left over from the source disk).
**Confidence:** (verified)
**Impact:** cosmetic.

## Same names for different items
**Behavior:** items 114 and 122 are both "Wand of mages", 115 and 123 "Coin of power", 120 and 121 "Amulet of
skill"; the fighter cannot use 114 but can use 122 (sheet "#" mark).
**Intended:** unclear (an unidentified or cursed twin?).
**Confidence:** (verified names; purpose unknown)
**Impact:** none known.

## Gnilda takes the whole pack, not only the five pieces
**Behavior:** RYZ came to the test with eight items: the five pieces worn and his old long sword, plate mail
and shield+1 unequipped. After "Behold! The Staff of Gnilda!" his pack held only the staff (pack count 1):
the three ordinary items were gone too (capture route `gtest` -> `gstaff`, RAM: pack of RYZ; shot
`inventory_staff`).
**Intended:** probably not: the text says the regalia is reclaimed; the code seems to clear the pack and add the staff.
**Confidence:** (RAM) one run.
**Impact:** a bearer who keeps his own gear in his pack loses it; hand it to a friend before going alone.

## The bearer's AC stays "LO" (-18) after the pieces are taken
**Behavior:** after the gift and after the ending RYZ's party list shows AC "LO" and his sheet AC -18 with an
empty pack, until the next camp E)quip recomputes it (`inventory_staff`, `ending_sheet_ryz`, `ending_castle_knights`).
**Intended:** no (a display left over, like the imported AC).
**Confidence:** (verified)
**Impact:** cosmetic.

## A one-way message room on floor 2
**Behavior:** floor 2 (16,3) holds a message square (kind 9) whose three doors open only outwards; the
neighbouring squares have walls on their side, so the party cannot step or kick in from (15,3), (17,3) or
(16,2); a warp onto it shows nothing (capture survey, disk data `tools/maps.py`).
**Intended:** unclear: probably reached only through a teleport not found here.
**Confidence:** (verified walls, inferred purpose)
**Impact:** the message is unknown.

## Status pokes in the maze show only after a camp
**Behavior:** writing DEAD into the party records in the maze changes nothing on screen until the party
camps; then the camp list shows DEAD and, with all six dead, leaving camp goes to the cemetery
(`gameplay_member_dead`, `gameover_slaughtered`, `gameover_cemetery`). Hit points written during a battle are
overwritten at the end of the round (RAM).
**Intended:** n/a (tooling note: the game redraws the list only on a menu change).
**Confidence:** (verified)
**Impact:** none for players.
