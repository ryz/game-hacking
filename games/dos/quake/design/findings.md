# Quake (DOS, shareware 1.06) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## God mode still flashes red
**Behavior:** with `god` on, a monster's hit still tints the view red for a moment although health stays 100 (main shots act_knight, boss_chthon_lava).
**Intended:** probably: the damage total for the flash is added before the god check (source: QuakeC T_Damage order).
**Confidence:** (verified) for the flash; (source) for the cause.
**Impact:** none in play; for screenshots fire before monsters close in.

## Console impulses wait for the console to close
**Behavior:** single player pauses while the console is open; `impulse 9` and `impulse 255` typed in one console session: only the last one acts once it closes (verified: only the Quad cheat took effect).
**Intended:** likely (one impulse per input frame).
**Confidence:** (verified).
**Impact:** cheat routes need one console opening per impulse.
