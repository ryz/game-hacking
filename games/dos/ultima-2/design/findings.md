# Ultima II: The Revenge of the Enchantress (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

## A statistic under 10 erases the whole generation form
**Behavior:** typing a value below 10 for any statistic (Wisdom 5 tried after four valid values) clears all six
values and the points go back to 90, with no message (scout sheet `work/scout/ultima-2/gen1/sheet.png`).
**Intended:** a minimum of 10 per statistic, probably with a message on the original disk.
**Confidence:** (verified)
**Impact:** a new player loses the whole distribution without being told why.

## The ring-seller keeps the gold when he refuses
**Behavior:** offering 500 gold to the old man under "A TREE" before Father Antos's blessing answers "EARN THE
RING!" and the 500 gold is gone (checkpoint `earn_ring`: gold 5882 -> 5382).
**Intended:** unclear; possibly a deliberate tax on guessing.
**Confidence:** (verified)
**Impact:** 500 gold lost per early try.

## The quicksword is not required to kill Minax
**Behavior:** every hit on Minax subtracts (weapon number x 8 + Strength) / 4 from her 255 hit points; a
bare-handed blow killed her once her hit points were low (route in the playbook, `hand_kill` in the scout's
sheet). Nothing checks for Enilno.
**Intended:** the story says only Enilno can slay her (source: Wikipedia's outline).
**Confidence:** (verified with a poke of her hit points); an honest bare-handed fight (15 hits) was not played.
**Impact:** the quicksword is a strong weapon, not a key.

## Tri-lithium counts ending in binary 11 send the rocket off course
**Behavior:** after a hyperwarp the game looks at the remaining tri-lithium; if its two lowest bits are both set
(3, 7, 13 ... left) the ship lands at random coordinates ("SHIP OFF COURSE!") (code; seen with 3 left: 9-9-9
became 7-1-1).
**Intended:** probably a random malfunction meant to be rare; it is fully predictable from the fuel count.
**Confidence:** (verified once, code read)
**Impact:** with 4 tri-lithium before a jump the player always goes astray.

## Launching without space armour kills at once
**Behavior:** launching the rocket while wearing anything below reflect armour ends with "YOU HAVE EXPLODED!" and
the game stops in space (verified from `rocket` with skin armour).
**Intended:** the space suit requirement (reflect or power armour).
**Confidence:** (verified)
**Impact:** a hard stop with no warning on the ground; save before launching.

## The first object of a map can never be attacked
**Behavior:** the search for "what is in that direction" checks objects 31 down to 1 and never object 0; an
attack on a monster in slot 0 always reports "MISS" (verified with a poked devil).
**Intended:** slot 0 is probably reserved; monsters created by the game may never use it.
**Confidence:** (verified with pokes) (inferred for natural play)
**Impact:** none in normal play as far as known.
