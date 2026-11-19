# Might and Magic II: Gates to Another World (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Too much free memory stops the game
**Behavior:** started directly, the program prints "Not enough memory for 16 color version. Release TSRs and
retry." and quits; started with 4 KB of low memory taken first (`loadfix -4`, as in GOG's own configuration) it
runs **(verified)**.
**Intended:** a memory check for the 16-colour version; it fails when the machine has more free memory than
the programmers expected (playbook, Boot sequence).
**Confidence:** (verified) for the behaviour; (inferred) for the cause.
**Impact:** none for a player of the GOG release (its launcher does it); anyone running the bare files in DOSBox
has to know the trick.

## The party window shows hit points as "/14"
**Behavior:** the party window under the view prints each member's current hit points after a slash ("ryz /14";
"/9" after damage), with nothing before it **(verified)**.
**Intended:** probably "current/maximum" with one number dropped, or a slash used as a separator.
**Confidence:** (verified) behaviour; intent unclear.
**Impact:** the maximum is only on the profile and the quick reference.
