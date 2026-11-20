# Wizardry II: The Knight of Diamonds - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## A guardian stays away while its piece is in the roster
**Behavior:** on this copy the scenario disk came with four characters of an earlier player who hold four of the
five pieces. With them in the roster every guardian square gave an ordinary random group; after deleting them
in the Training Grounds the same routes met the five guardians (checkpoints `guard1` to `guard5`).
**Intended:** the pieces are unique: a second copy cannot be won while one exists.
**Confidence:** (verified) for the set of four and piece by piece: with only the gauntlets' holder deleted the
gauntlets' guardian came and the shield's did not.
**Impact:** a used scenario disk can make the quest look broken; the fix is to delete or strip the holders.

## The Training Grounds disband the party
**Behavior:** entering the Training Grounds and coming back leaves the Castle's party list empty.
**Intended:** unclear (the training grounds work on the roster).
**Confidence:** (verified) once, `@edge,t`, roster, leave.
**Impact:** the party must be formed again in the Tavern.

## Space does not leave the title
**Behavior:** Return goes on to the copyright menu, space does not (tried at frames 1200 and 1900 after power-on, and once by hand).
**Intended:** unclear; Wizardry I takes any key.
**Confidence:** (verified).
**Impact:** none beyond a moment of doubt.

## Six at the award ceremony lose a member
**Behavior:** a party of six that reaches the castle with the staff (possible here only with a staff put into
a pack from outside the game) gets the ending; while the awards are asked the second member's place is used for
each candidate, and afterwards the roster holds the last candidate twice and the second member not at all
(route `@start,STAFF,MAZE,HOME`, five times Y, leave the game; roster read from the disk).
**Intended:** the bearer is meant to arrive alone: Gnilda's test wants one alone.
**Confidence:** (verified) once, roster read with `tools/data.py`.
**Impact:** none in normal play; for cataloguing: go up alone.

## The first round after surprising the monsters has no spells
**Behavior:** when the message box says "YOU SURPRISED THE MONSTERS!", the options of every member lack S)PELL
(shot `battle_surprised_no_spell`, also `battle_f1_swarm`, `battle_f6_evil_eyes`); in ordinary rounds S)PELL is
offered (`battle_f1_men_in_armor`, `battle_dispell`). When the monsters surprise the party they act before any
orders are asked (`battle_f2_men_in_armor`, `battle_f3_four_groups`, `battle_f5_swarms`, `battle_f6_succubus`).
**Intended:** a free round of blows only; this answers the scout's open question about when S)PELL appears.
**Confidence:** (verified) in eight encounters.
**Impact:** the surprise round is weaker for a caster-heavy party than it looks.

## Battle messages do not name the spell
**Behavior:** "DEDDO CASTS A SPELL", "MAGIC HELMET CASTS A SPELL": the spell's name is never shown, only its result
(`battle_spell_damage`, `boss_helmet_spell`); DOS writes "casts a LAHALITO".
**Intended:** unclear (screen space).
**Confidence:** (verified).
**Impact:** the player cannot tell which spell a monster used.

## Message squares fire on arrival by warp, and fights do not (except on floor 1)
**Behavior:** the `WARP` macro onto the sage's squares (floor 2 (18,9), (18,10)) and floor 6 (11,17) shows their
text at once (`dialogue_f2_sage`, `dialogue_f6_king_power`), contrary to the scout's note; arriving by warp on a
room square met a random group only on floor 1 (four of six tries) and never on floors 2-6 (30 tries); kicking
a door into a room met one in 13 of 38 tries. The view is not redrawn after a warp until the next turn.
**Intended:** not a game rule: a property of the poke-based warp.
**Confidence:** (verified) for these squares.
**Impact:** routes only; see the playbook.

## The Burma-Shave fountain stones the wader
**Behavior:** floor 4's four signs read as a Burma-Shave rhyme ending "... A CLEAR BLUE FOUNTAIN." BURMA SHAVE
(TM) (`dialogue_f4_fountain`); "WHO (#) WILL WADE" and RYZ, wading, is STONED and moved to the back
(`gameplay_stoned`). DOS poisoned the wader.
**Intended:** a joke with a sting.
**Confidence:** (verified) once.
**Impact:** a stoned member needs the Temple.

## Mapiro's shout and the well send the party home
**Behavior:** on floor 3 (8,10) a familiar figure shouts "MAPIRO MAHAMA DIROMAT" and the next screen is the Castle
(`dialogue_f3_mapiro_shout`). At the well (floor 5 (11,8)) Y to "FEE IS 5000 / PAY (Y/N) ?" also ended in the
Castle, with RYZ holding 2,442 gold (not settled whether the wish or the lack of gold did it).
**Intended:** the shout is Werdna's teleport phrase from Wizardry I (inferred).
**Confidence:** (verified) the Castle after both; the cause at the well (inferred, open).
**Impact:** a free trip home from floor 3.

## The Inn's cot heals one hit point per ten gold
**Behavior:** RYZ poked to 41 of 112 hit points: after the cot's first frames 55 hit points and 140 gold spent,
later 73 and 320 (`inn_healing`).
**Intended:** a week per point, as in Wizardry I.
**Confidence:** (verified) frames, starting value poked (RAM).
**Impact:** none.
