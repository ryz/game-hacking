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

## Death stops the program
**Behavior:** when ryz dies (hit points at 0, a trap without tools) the game sets hit points, food, experience
and gold to 0, prints "RYZ IS DEAD!" and then loops forever: no prompt, no return to the menu (code; screen
unchanged 2,000 frames later, shot `gameover_dead`). The PLAYER file on disk keeps the last Q save.
**Intended:** probably a forced restart from the last save, as on the Apple II original.
**Confidence:** (verified)
**Impact:** the player must reboot; everything since the last Q is lost.

## A dungeon trap without tools is death
**Behavior:** each step below ground springs a trap with chance level/256 (level 1 = 0); the torch goes out, a
tool is used up ("ESCAPED! BY USE OF TOOLS!"), and without tools the game goes straight to "RYZ IS DEAD!"
(code; both verified with a forced roll: `system_trap`, `gameover_dead`).
**Intended:** a punishing trap; whether instant death was meant is unclear.
**Confidence:** (verified)
**Impact:** deep levels (up to 15 in 256 per step) are lethal without tools; the 16th level, where the
tri-lithium lies, is the riskiest.

## Lord British's raise reads only the two high digits of the hit points
**Behavior:** the tribute gives +300 while the high byte of the hit points (thousands and hundreds) is under
50, +200 under 75, +100 under 99, nothing above (code). At 3184 H.P. he still raised 300 (`system_king_1990`).
**Intended:** the scout read the thresholds as 500/750/1000; in play they are 5000/7500/9900, so the king keeps
selling hit points cheaply for almost the whole game.
**Confidence:** (verified at 400 and 3184 H.P.)
**Impact:** 50 gold for 300 H.P. at any time: hit points are never scarce for a player who walks to the castle.

## Weapon and armour requirements compare decimal digits as a number
**Behavior:** statistics are stored as packed decimal; the Ready and Wear tests compare that byte as a plain
number against 8 x the item number, so Strength 45 counts as 69 and passes power armour's "above 48" (code;
verified: power armour worn at Strength 45, refused at 25, `system_strong_refused`).
**Intended:** probably "Strength above 8 x n" on the shown value.
**Confidence:** (verified)
**Impact:** the thresholds on screen are lower than they look: Agility 49 for the quicksword, 39 for the light
sword, Strength 31 for power armour.

## Statistics are typed as two digits
**Behavior:** in player generation each statistic takes exactly two digits; Enter is not needed, and "5" waits for
a second digit. "05" (any value under 10) clears all six values silently (`menu_generation`).
**Intended:** a minimum of 10.
**Confidence:** (verified)
**Impact:** a player typing "5" Enter sees nothing happen until the next digit.

## A chest can hold a weapon with no name
**Behavior:** a chest on dungeon level 1 answered "IT CONTAINS A  WEAPON" with a blank where the name belongs
(seen once from checkpoint `dungeon`; the code picks a random weapon number, and 0 is "hands").
**Intended:** a real weapon.
**Confidence:** (verified once) (inferred cause)
**Impact:** the chest gives nothing usable.

## Surface monsters are created anywhere on the map
**Behavior:** every turn the game tries once to create a monster on a random square of the 64 x 64 map (x below
63, a coin flip for y) of the next kind in a fixed cycle of nine; a land kind on a non-grass square or a sea kind
off water cancels the try (code). Standing still at the start, one devil appeared after about 20,000 frames, 20
squares away (RAM).
**Intended:** wandering monsters that close in on the player.
**Confidence:** (code) (RAM for the rate)
**Impact:** early play is quiet; the set shows monsters placed beside ryz by poke.

## The hotel clerk keeps the gold 250 times in 256
**Behavior:** an offer to the clerk raises a random statistic by 4 per 100 gold only when the random number is
below 6 ("ALAKAZAM!"); otherwise "THANK YOU VERY MUCH!" and the gold is gone (code; `system_alakazam` forced).
**Intended:** the Village Idiot's tip ("Offer the hotel clerc gold!") suggests a reliable reward.
**Confidence:** (code)
**Impact:** about 40 offers per success on average.

## The kings picture is missing from the demonstration
**Behavior:** the program's demonstration lists PICCAS with "PLEAD WITH MEDIEVAL KINGS FOR ASSISTANCE", but the
GOG folder has no PICCAS file, and the demonstration shows only five pictures (creatures, pub, dungeons, space,
Minax) before the intro text returns (verified, `cutscene_demo_*`).
**Intended:** six pictures.
**Confidence:** (verified)
**Impact:** cosmetic.

## Unlock works only east and west
**Behavior:** the Unlock command adds only the horizontal part of the direction; north or south always answers
"NO DOOR THERE!" (code; a west door verified, `system_unlock`).
**Intended:** doors in any direction.
**Confidence:** (code)
**Impact:** doors above or below ryz must be approached from the side.
