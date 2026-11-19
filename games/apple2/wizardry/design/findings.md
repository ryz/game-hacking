# Wizardry: Proving Grounds of the Mad Overlord - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The boot disk must be write-protected
**Behavior:** after the title the program writes to its own boot disk and stops for ever unless the write is
refused (black screen, no message). Reproduce: `w2100,space,w3000` on a model without `wp1`.
**Intended:** a check that the player protected the boot side, as the update utility's text asks ("PUT A
WRITE-PROTECT TAB ON THE NOTCH YOU PUNCHED!").
**Confidence:** (verified) the loop read from memory; with the boot side write-protected the menu appears.
**Impact:** a boot disk without a write-protect tab (or an emulator without write protection) never reaches
the menu, and nothing on screen says why.

## Werdna can be friendly
**Behavior:** with one timing at his door the fight opens with "A FRIENDLY GROUP OF W E R D N A. THEY HAIL
YOU IN WELCOME! YOU MAY F)IGHT OR L)EAVE IN PEACE." (`@gwerdna_sign,enter,w300,r,w300,w7,k,w600,w1500`).
**Intended:** unclear; the friendly-group roll seems to apply to every encounter.
**Confidence:** (verified) `boss_werdna_friendly`; L)eave puts the party in his room with no fight and no amulet (`boss_friendly_left`).
**Impact:** a curiosity; the amulet still needs the fight.

## The ending takes the equipment and most gold
**Behavior:** after the Congratulations screen the packs are empty and gold is cut to its last four digits
(24,817 -> 4,817); 250,000 experience points and the chevron are added. The DOS port gives 50,000 gold and
experience and keeps the equipment.
**Intended:** as written on the screen ("YOU MUST GIVE UP ALL YOUR EQUIPMENT AND MOST OF YOUR MONEY").
**Confidence:** (verified) sheets and the roster on disk.
**Impact:** characters carried to the next scenario arrive without gear.

## Floor 2's elevator-type square
**Behavior:** floor 2 has one square of the elevator type at (10,9); the DOS port has it at (10,8). All other
squares of the ten floors are identical.
**Intended:** unclear (floor 1's elevator is at (10,8); a shaft would pass (10,8) on floor 2).
**Confidence:** (verified) disk data of both versions; stepping on it shows the elevator's buttons A through D (`gameplay_elevator_f2`).
**Impact:** on floor 2 the elevator is entered one square north of where it is on floors 1, 3 and 4.

## A password is asked for characters that have none
**Behavior:** the Tavern and the Training Grounds ask "PASSWORD >" for every character; Return passes when
none was set, anything else returns to the name prompt without a message.
**Intended:** probably so as not to reveal which characters are protected.
**Confidence:** (verified).
**Impact:** one more key press per member when forming a party.

## The Temple treats only characters who are not in the party
**Behavior:** typing a party member's name answers "** RYZ IS NOT HERE **" (`temple_not_here`). A dead member
has to be removed in the Tavern first; then the Temple names the donation and a party member pays
(`temple_donation`). The raised character comes back with 1 hit point (`temple_healed_sheet`).
**Intended:** yes: the dead are carried to the Temple and the living pay.
**Confidence:** (verified).
**Impact:** two extra visits (Tavern before, Tavern after) for every cure; nothing on the Temple screen says so.

## A class change resets the scores and adds years
**Behavior:** ZED, an elf mage with 11 11 10 7 11 6, changed to fighter: scores back to the elf's base
7 10 10 6 9 6, age 19 to 25, level 1 (`training_class_changed_sheet`).
**Intended:** yes (the series' rule), but the screen that offers the change does not say it.
**Confidence:** (verified) one change.
**Impact:** the bonus points bought at creation are lost by a class change.

## MALOR: rock bounces, the sky kills, and Esc still costs the spell
**Behavior:** a teleport into solid rock answers "YOU BOUNCED BACK TO WHERE YOU WERE!" (`camp_malor_bounce`);
one floor above floor 1 is the Castle (safe); two or more floors up: "YOU MATERIALIZED IN MID-AIR AND FELL
TO A PAINFUL DEATH!" and all six are DEAD on the roster (`gameover_malor_midair`, `gameover_roster_dead`).
Leaving the displacement screen with Esc takes one level 7 spell point all the same.
**Intended:** the program also holds "YOU LANDED IN SOLID ROCK ... LOST FOREVER!" and "YOU APPEARED IN THE
CASTLE MOAT" (program text); neither was met with the targets tried.
**Confidence:** (verified) the three outcomes above; the conditions of the other two are unknown.
**Impact:** MALOR is safer in this version than its reputation, except upward.

## Doors are passed only by K)ick
**Behavior:** F)orward into a door answers "OUCH!" like a wall; K)ick goes through (14 doors tried).
**Intended:** yes, the command list has both.
**Confidence:** (verified) `gameplay_door`, every `dialogue_*` route that enters a room.
**Impact:** routes translated from the DOS port (where walking opens doors) bump into every door.

## Spells are not named in battle messages
**Behavior:** "DEDDO CASTS A SPELL", "ARCH MAGE CASTS A SPELL": the name is left out for both sides; only
some result lines name it ("MNZ IS HIT BY MABADI!", `boss_mabadi`).
**Intended:** unclear (the DOS port prints "casts a TILTOWAIT").
**Confidence:** (verified) every cast in the set.
**Impact:** the player learns what a monster cast only from its effect.
