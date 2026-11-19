# Wizardry III: Legacy of Llylgamyn (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The orb leaves an invisible item behind
**Behavior:** surrendering the Orb of Earithin replaces it in its bearer's pack with item 1000, which has no name
and is not listed, but still counts as one of the eight pack entries (verified: `after_ending`, CUBI's pack count 1).
**Intended:** probably "remove the orb".
**Confidence:** (RAM)
**Impact:** one pack slot lost for the bearer after the ending.

## The party gets no star of its own
**Behavior:** the Queen says she gives "your party the Star of Llylgamyn", but only the six other characters chosen
afterwards get the "*" award and 150,000 E.P.; the party's records are unchanged on disk and in memory (verified:
`02_ending`).
**Intended:** unclear (the party may be meant to receive it too).
**Confidence:** (verified)
**Impact:** the bearers of the orb end without the award they were promised.

## Floor 6 refuses an all-neutral party even with a crystal
**Behavior:** a party of neutral characters carrying any crystal or the orb is sent back from floor 6 ("You are
forbidden to enter here!"), while good or evil parties with the same item enter (verified with poked parties).
**Intended:** fits L'kbreth's "neither good nor evil alone" only partly; unclear.
**Confidence:** (verified)
**Impact:** the all-neutral party that serves both halves cannot take the last step.

## The crystals' power hides behind E)quip
**Behavior:** the Neutral Crystal is made by E)quip (camp or sheet): after the slots, the game asks "Will you
invoke the special power of your Crystal of Evil/Good (Y/N)?" for each crystal carried. U)se, the statues and
L'kbreth do nothing with them (scout, verified). A good or evil bearer holding both who invokes the crystal of
his own alignment gets the Neutral Crystal in silence; the other crystal burns him to ashes ("Powers there be
that the wise may use. Fools who play with these powers shall perish in flame!"); a neutral bearer ("Power
springs for both extremes, from extremes must be employed!") or a bearer of one crystal ("Nor good nor evil
alone, the balance shall remain, alone each one shall fail, to triumph, have the twain!") loses the crystals
(verified 2026-11-19: `invoke_*` shots, checkpoint `gneutral`; the item records carry SPECIAL 28 and 29).
**Intended:** yes (the riddle-like verses explain the rule after a failure).
**Confidence:** (verified)
**Impact:** a player who tries U)se never finds it; the neutral party that serves both halves cannot make it;
a wrong guess costs a resurrection from ashes. The neutral try also cost CUBI 4 maximum hit points (61 -> 57).

## Floor gates count "any good member", not the majority
**Behavior:** floors 2 and 4 admit a party with at least one good member even when most are evil (1 good, 3
evil, 2 neutral: admitted), and refuse one with evil members and no good one; floors 3 and 5 refuse every party
with a good member, even 3 good against 1 evil; all-neutral parties enter all four (verified 2026-11-19 with
poked alignments, `try.py` runs; the scout's "any evil member" for 2/4 and the walkthrough's majority rule were
both wrong).
**Intended:** probably "a party counts as good if anyone in it is good".
**Confidence:** (verified)
**Impact:** only reachable with mixed parties, which the Tavern forbids ("* Bad alignment *"), so it shows when
an alignment changes in the maze.

## A raise can fail into ashes at once
**Behavior:** raising dead CONDI (level 11, 2750 gold) failed: "* CONDI needs KADORTO now *" (verified,
`temple_failed`).
**Intended:** yes (Wizardry I rule).
**Confidence:** (verified)
**Impact:** the gold is spent either way.
