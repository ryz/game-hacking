# Dragon Quest (Famicom, English translation patch) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The password shortens the hero's name
**Behavior:** a hero named ryz who enters his own Return Spell comes back as "r56": the second and third
letters turn into digits. Route: `@password_entry` + `PW_LATE` without `NAME_FIX`.
**Intended:** the password keeps each name symbol only within the 64 symbols of the password grid; in the
Japanese game the same happens to name symbols outside that set. In the English patch the lower-case letters
r to z fall outside it. Probably an accepted side effect of the translation.
**Confidence:** (verified)
**Impact:** cosmetic; a player should pick a name from the symbols of the password grid (capitals, digits, a-q).

## Level and stats come from experience only when a password is entered
**Behavior:** raising experience from 0 to 34218 leaves the hero at level 1 with 15 HP; the king then quotes a
meaningless "next level after 31325". After entering the password he is level 21 with 149 HP.
**Intended:** experience only changes through battles, where the level-up check runs; the direct change is
outside normal play.
**Confidence:** (RAM)
**Impact:** none in normal play; matters for cataloguing.

## The king tells a different Return Spell each time
**Behavior:** asked twice in the same state (level 21, 34218 experience, 6135 Gold, same items), the king gave
two different 20-symbol passwords. Shot: [king_password](../shots/main/king_password.png) against the password
in the playbook Shortcuts.
**Intended:** the password seems to carry a changing part besides the progress, so that the same progress does
not always look the same. Only the first of the two was entered again.
**Confidence:** (verified) that they differ; (inferred) why.
**Impact:** none; any of them restores the same progress.

## Weak enemies run from a strong hero
**Behavior:** "Wizard appeared! Wizard ran!" before any command, level 21 hero in the swamp cave.
**Intended:** intended: it spares a strong hero the easy fights.
**Confidence:** (verified)
**Impact:** no experience or Gold from such meetings.

## Loto's armour and the poison swamp
**Behavior:** stepping on the swamp beside the Dragon King's castle cost no HP while wearing Loto's armour.
**Intended:** intended (the armour's known property in later versions).
**Confidence:** (RAM) one step measured.
**Impact:** the last approach is free of floor damage with the best armour.
