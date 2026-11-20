# SWORD OF VERMILION - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Several levels granted at once at the end of a battle
**Behavior:** with 2417 EXP (poked) at level 1, one won battle raised the prince straight to level 5 (MHP 33 -> 162)
and the status window opened by itself (checkpoint `m_strong`, shot `battle_levelup`).
**Intended:** probably; the game checks the level only when a battle ends, not on each kill.
**Confidence:** (RAM) EXP set by poke; the level-up itself is the game's.
**Impact:** none in normal play; a large EXP gain shows only one level-up window.

## Battle escape by being pushed off the edge
**Behavior:** while swinging in place, the prince can be pushed by slimes to the screen edge and leaves the battle
(EXP unchanged; preview `won` of the capture run, 2026-11-20).
**Intended:** the edge escape is intended; being pushed into it probably not.
**Confidence:** (verified) seen once.
**Impact:** a fight can end without its reward.

## Priest's menu shows no cursor
**Behavior:** the church menu (Remove a curse / Apply poison balm / Save your game / Stop) has no arrow until a key
is pressed (`save_church_menu`, `32_priest_menu` in set start).
**Intended:** unclear.
**Confidence:** (verified)
**Impact:** cosmetic.
