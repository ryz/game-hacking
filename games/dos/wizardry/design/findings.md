# Wizardry: Proving Grounds of the Mad Overlord (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Every new character starts with 8 hit points
**Behavior:** all six characters created by the scout (fighters with vitality 13 and 15, a mage with 8) and
all twelve characters on the stock disk show 8 of 8 hit points at level 1 (verified: `@start`, `inventory_roster`).
**Intended:** unclear; the Apple original rolls hit points from class and vitality (source: series rule).
**Confidence:** (verified) for the value, (inferred) for the cause.
**Impact:** level 1 mages are much tougher than in other versions; fighters weaker.

## No spells in the first round of a fight
**Behavior:** in the first round of both fights tried (the Slimes on floor 1, Werdna) nobody had S)pell; from
round 2 every member, the fighters too, had it (verified: `@battle`, `@werdna`). The Slime fight opened with
"You surprised the monsters!", so the first round may be the surprise round.
**Intended:** probably the free round after surprising the monsters is melee only.
**Confidence:** (verified) behaviour, (inferred) reason.
**Impact:** a party that surprises monsters cannot open with a sleep or fire spell.

## A poke-made amulet ends the game
**Behavior:** the ending checks only that a party member carries item 94 when the party reaches the castle;
Werdna does not have to be beaten (verified: checkpoint `ending` = veterans + AMULET + floor 1 stairs).
**Intended:** the amulet can only come from Werdna.
**Confidence:** (verified).
**Impact:** none for a player; a shortcut for capture runs.
