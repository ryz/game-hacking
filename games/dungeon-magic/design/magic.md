# Dungeon Magic - magic

## Overview
Magic comes from wizards. Each wizard teaches one element - Earth, Water, Fire, Wind or Fairies - and asks
"Will you be apprenticed in the magic art of <element>?"; answering yes adds that element's runes to the Spell
panel **(verified)** (`wizard_apprentice`, `wizard_magic`). A spell is a short row of runes entered by the player
and cast in real time; it costs hit points, there are no magic points **(verified)** (`rune_cast`). Magic cannot
be used in town **(source)** (in-game text "You cannot use magic in town", ROM).

## 1. Wizards
- Every town has at least one wizard's house; Granville has all five: Earth and Water in the two houses on the
  north street, Fire and Wind on the east street, Fairies on the south street **(verified)** (door survey, see
  [maps.md](maps.md)). Town 01 has a Fire wizard, town 02 a Water wizard, town 05 a Wind wizard **(verified)**.
- The wizard you serve is also your wise man: coming back with enough experience he asks "Have your journeys
  made you wiser?" and raises your level ([progression.md](progression.md)) **(verified)** (`wise_man_level`).
- Becoming an apprentice reduced the carrying capacity shown as WEIGHT (49.6 before) **(RAM)** (the stored value
  dropped by 2.0; the panel was not looked at).

## 2. The Spell panel and casting
The Spell panel lists the five element symbols in a column; an element you serve shows its runes beside it
(Fire: three runes after the Fire apprenticeship) **(verified)** (`wizard_magic`, `rune_select`).
Controls **(verified)** (routes of `rune_select`, `rune_cast`):
1. Start pauses; Left/Right move to the Spell icon; Select opens the panel.
2. Left/Right (and Up/Down between elements) move the cursor over the runes; **B** adds the highlighted rune to
   the spell, shown as small symbols at the top left of the panel (up to three).
3. Start resumes play; **A** casts the composed spell while the Spell icon is active.
- Casting two Fire runes against a monster took 6 of its 29 HP and cost the hero 6 HP **(verified)**
  (`rune_cast`); the same spell cast in the empty field cost 6 HP too, with no visible effect **(verified)**.
- 243 combinations (3 runes per element, up to three runes) **(source)** (Wikipedia; StrategyWiki summary); the
  first runes choose the spell and a third rune modifies its power **(source)** (StrategyWiki summary via search).

## Open questions
- The effect of each rune combination; whether the cost depends on the runes.
- Whether more runes per element are learned later (books, swords).
