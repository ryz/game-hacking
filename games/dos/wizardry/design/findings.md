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

## The floor 1 statues never offer a search
**Behavior:** the statues on floor 1 (13,3) chicken-cat, (13,5) hooded man with the altar (Murphy's ghost
in the series) and (13,18) boar show their text but never ask "Will you search (Y/N)?", from any side, with
the level 1 or the level 13 party, after Enter, Y or I)nspect (verified: `dialogue_f1_chicken`,
`dialogue_f1_altar`, `dialogue_f1_boar`; routes in the playbook). The same kind of square on floor 2 (bear,
frog) asks and gives the statuette (verified: `system_search`, `system_search_found`). The disk data of the
floor 1 squares is the same kind (message type 4, item or monster number in the first value: -1097 bronze key,
-1098 silver key, 77 a monster).
**Intended:** the floor 1 statues hold the bronze key, the silver key and Murphy's ghost (source, series).
**Confidence:** (verified) behaviour, (inferred) cause unknown.
**Impact:** a player of this version may never find the keys on floor 1; Murphy's ghost, the classic
experience farm, was not reachable in this capture.

## Sleeping and paralyzed members move to the back
**Behavior:** after an arch mage's Katino the sleeping CONDI and MNZ were listed last in the party window;
after Werdna's guards paralyzed RYZ he moved from #1 to #6 and CONDI led the party (verified:
`battle_party_asleep`, `boss_vampires_identified`, `gameplay_after_werdna`).
**Intended:** yes (the front rank is kept for members who can fight; series rule).
**Confidence:** (verified).
**Impact:** the marching order changes by itself during fights; R)eorder in camp restores it.

## Drain after the fight
**Behavior:** after Werdna's fight, besides the drain during the round, the reward screen showed "CONDI was
drained!" and "RYZ was drained!"; both ended at level 11 (verified: `boss_drained_after`, `ending_chevron`).
**Intended:** probably the level loss is applied to the record after the fight.
**Confidence:** (verified) messages; (inferred) the order of the bookkeeping.
**Impact:** none beyond the drain itself.

## A new mage shows no spell points
**Behavior:** the freshly created elf mage ZED shows "MAGE 0/0/0/0/0/0/0" on the Training Grounds sheet
(verified: `training_inspect_new`), while DEDDO, made the same way, shows 2 level-1 points in camp
(verified: `inventory_camp_inspect`).
**Intended:** the points are computed when the party enters the maze (playbook RAM notes).
**Confidence:** (verified) / (inferred).
**Impact:** cosmetic.
