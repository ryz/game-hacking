# Phantasie - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Begging mercy can cost more gold than the party carries
**Behavior:** against 5 giant ants, 5 giant bees and a giant ant, BEG MERCY ends the fight with "the monsters
stop and take your gold" and "each survivor gets 0 XP and -256 GP" (route `@d1_ants`, shots `battle_beg_mercy`,
`battle_beg_result`).
**Intended:** probably the loss of the carried gold, shown as a negative share.
**Confidence:** (verified) message; how the loss is booked against each member not checked.
**Impact:** begging is a way out of a lost fight at the price of the purse.

## Combat choices that a member cannot use silently become thrust
**Behavior:** choosing ATTACK or SLASH for ryz (level 1 fighter with a club) in the option list set his option
to THRUST; LUNGE and SPELL were taken as chosen (preview routes from `@enc_bantir`).
**Intended:** unclear: maybe attack/slash need more than one attack per round.
**Confidence:** (inferred)
**Impact:** the option column must be read back after every choice.

## The first fight's experience is split unevenly into shares
**Behavior:** after "each survivor gets 73 XP" the town entry reports "each share is 71 XP" (`battle_reward`,
`town_shares_return`).
**Intended:** unclear (rounding over shares, or XP kept by a member).
**Confidence:** (verified) numbers; cause unknown.
**Impact:** small.
