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
**Confidence:** (verified) screen; what leaving does to the quest was not tried.
**Impact:** a curiosity, possibly a way past the fight without the amulet.

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
**Confidence:** (verified) disk data of both versions; not stepped on.
**Impact:** unknown.

## A password is asked for characters that have none
**Behavior:** the Tavern and the Training Grounds ask "PASSWORD >" for every character; Return passes when
none was set, anything else returns to the name prompt without a message.
**Intended:** probably so as not to reveal which characters are protected.
**Confidence:** (verified).
**Impact:** one more key press per member when forming a party.
