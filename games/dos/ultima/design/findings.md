# Ultima I: The First Age of Darkness (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Rolls do not depend on time
**Behavior:** the game's one random number generator advances only when the game rolls, not with the clock or
with waiting. The same keys from the same save give the same steals, tips, hits and monster moves, however long
the player waits between them (seen: four pub visits with different waits all gave the same "no tip"; the
playbook's capture routes set the generator's value to pick a tip or a stolen item).
**Intended:** probably not thought about; on a real PC of 1987 the order of keys differed from game to game.
**Confidence:** (RAM) and code.
**Impact:** a player who reloads a save and repeats the same keys repeats the same outcome; changing the order
of harmless commands changes it.

## Space-age armour stolen on the first day
**Behavior:** stealing behind an armour counter yields a random armour of the whole list, not of the shop's
current goods: a level-1 hero stole a Reflect suit in Britian at 0 moves (`system_steal`), years of game time
before any shop sells one. Castle weaponry rooms give any weapon up to the Blaster the same way
(`system_steal_storeroom`).
**Intended:** the storeroom theft is part of the design (Shamino's hint "take nine items from my storerooms");
the shop theft ignoring the time gate is probably an oversight.
**Confidence:** (verified).
**Impact:** the strongest armour and weapons are available at once for anyone willing to risk the guards
(caught on about 30% of tries, 15% for thieves).

## Docking at a starbase seems out of reach
**Behavior:** the docking ports are fixed squares beside the starbase (from tables in the space program), and
the ship must stop exactly on one with the right heading. Every placement on the two free ports here, including
turning in place on the port square, collided with the station first ("Crunch!", shields lost) because the
collision test compares the ship's picture with the pixels on screen.
**Intended:** docking to buy another ship for 500 pence ("Choose thy ship:").
**Confidence:** (inferred): not tried with every speed and heading; on the original Apple II or CGA pictures the
pixels may not touch.
**Impact:** if real, the ship choice and the vacuum death at the space doors cannot be seen in the EGA version.

## Status panel not redrawn after outside changes
**Behavior:** the Hits, Food, Exp. and Coin numbers are redrawn only when the game itself changes them; a value
changed from outside (a trainer, the capture's pokes) shows its old number until the next change in play.
**Intended:** a speed shortcut of the time.
**Confidence:** (verified).
**Impact:** none in normal play.

## Monsters the player cannot see
**Behavior:** the Hidden archer is not drawn on the overworld (`battle_hidden_archer`), the Gelatinous cube and the
Invisible seeker are not drawn in dungeons (`battle_gelatinous_cube`); the log names them when they attack.
**Intended:** yes (their names say so).
**Confidence:** (verified).
**Impact:** the cube destroys armour before the player can see what hit him.

## Charisma discounts every price
**Behavior:** prices fall with Charisma: leather armour 45 pence at Charisma 13, 43 at 19; the shuttle 1,296 at
13, 1,116 at 29 (`shop_armour`, `shop_armour_late`, `shop_transport_space`).
**Intended:** yes.
**Confidence:** (verified at three Charisma values; formula not read).
**Impact:** Charisma, otherwise little used, pays for itself in the late game's expensive vehicles.
