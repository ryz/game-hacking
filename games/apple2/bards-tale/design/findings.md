# The Bard's Tale: Tales of the Unknown - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Party attack outside a fight
**Behavior:** P in the streets or a dungeon opens the round options "Party attack, Defend, Use" for RYZ: a
member can attack his own party with no monsters present (`system_party_attack`).
**Intended:** probably (a way to get rid of a possessed or unwanted member).
**Confidence:** (verified).
**Impact:** a mistyped P in the street starts a round against the party.

## Wrong spell codes are silent
**Behavior:** a code the caster does not know (or a combat spell outside a fight) gives no message: the
window stays blank (SOSH, TRZP, FRFO, VOPL, QUFI and others typed in the cellar, preview `probe2`).
**Intended:** unclear.
**Confidence:** (verified).
**Impact:** the player cannot tell a typo from a spell without visible effect.

## Forced-fight and trap squares fire once
**Behavior:** the dungeon squares that force a fight and the tripwire traps are cleared from the level as soon
as they fire, so going back to the square gives nothing; the monsters met there are rolled, not fixed (the
same square gave Ogre magi, Magicians, Stone giants, Blue dragons with other timings).
**Intended:** yes.
**Confidence:** (RAM: dungeon code clears the square; verified: arrival fights with different waits).
**Impact:** the "fixed" encounters of a level differ from game to game.

## The ending leaves the party in the dark tower
**Behavior:** after Kylearan's last page ("Kylear vanishes.") the party stands in Mangar's antechamber with a
black view and play goes on (`ending_vanishes`).
**Intended:** yes, the game has no end screen.
**Confidence:** (verified).
**Impact:** the party keeps its 300,000 bonus and can go on playing.
