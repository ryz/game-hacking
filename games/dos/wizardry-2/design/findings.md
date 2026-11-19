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
