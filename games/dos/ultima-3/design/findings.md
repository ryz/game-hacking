# Ultima III: Exodus (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The shop behind a counter depends on the row
**Behavior:** Transact over a counter opens the pub, grocer, healer, weapons, armour, Guild, oracle or stables
by the party's row on the town map (row mod 8), not by the sign or the merchant (code; verified for five kinds
at their counters, `try_t4.png`).
**Intended:** the maps were laid out so that each counter sits on the right row; a compact way to store shops.
**Confidence:** (code), (verified).
**Impact:** none in normal play; a counter on a "wrong" row would open another shop.

## Digging for Exotics is not limited
**Behavior:** DIG on the two islet squares adds one Exotic weapon or armour to the digger each time; the code
marks two bytes of the party file but never tests them (code).
**Intended:** probably one find per game.
**Confidence:** (code), not repeated in play.
**Impact:** every character can dig its own Exotics.

## Idle turns count as moves
**Behavior:** the moves counter shown by Quit & Save and the ending grows with the automatic Pass every five
seconds: a party that never moved showed "00000008 moves" (verified, `@start,q`).
**Intended:** unclear (the Apple II original counts turns the same way).
**Confidence:** (verified).
**Impact:** the "Report thy feat!" count rewards fast play at the keyboard.

## The level shown is not the level Lord British counts
**Behavior:** the panels show L = experience / 100 + 1, while Lord British raises maximum hit points only when
the experience hundreds reach the current maximum's hundreds (code; verified "Experience more!" and "Thou art
greater").
**Intended:** levels as hit-point tiers.
**Confidence:** (code), (verified).
**Impact:** a character can show L:24 with far fewer hit points until it visits the king.

## Spelling in the game's text
**Behavior:** "compleated" in the ending, "pannels" in Montor East, "Resurect whom?" in the spell prompt, "Bobbit"
for the halfling race (ROM text, the ending verified).
**Intended:** typos of the period (Bobbit is deliberate).
**Confidence:** (ROM text).
**Impact:** quote them as written in captions.
