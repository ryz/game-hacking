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

## The Square Lake gate prints "Version 1.01" and resets the battle counters
**Behavior:** stepping onto the gate (area 17 (0,15), facing east) with the right marks shows Sheltem's face and
fills the party window with four lines "Version 1.01" instead of the names (`boss_sheltem_appears`,
`boss_sheltem_surprise`); the battles-won and battles-lost counters are 0 afterwards, so a party that had won
2,316 battles is told after Sheltem that it has won "its 1st battle", and the final screen reads "Battles: 1 won
/ 0 lost" **(verified, RAM: both counters read 0 right after the gate)**.
**Intended:** a message (perhaps the party names or a warning) printed from a missing text, string 0 of the
program being its version string; the counters are probably cleared by the same stray write.
**Confidence:** (verified) behaviour; (inferred) cause.
**Impact:** the ending's battle statistics are wrong for every player; the capture sets the counters again
after the gate so the shown ending is plausible.

## Paying a service pools the party's gold
**Behavior:** at Otto Mapper (10 gold) with 5,000 gold on ryz and none on the others, ryz is left with 835 and
every other member with 831: the game gathers all the party's gold, takes the price and shares the rest out
evenly, the remainder to the payer. Blacksmiths and taverns take the price from the shopper only **(verified,
RAM: three gold amounts measured)**.
**Intended:** probably a convenience so that a poor member can buy a skill; the side effect redistributes gold.
**Confidence:** (verified).
**Impact:** a player who keeps gold on one character finds it spread over the party after any event service.

## The final code is fixed, the cryptogram is random
**Behavior:** the override code is always WAFE; the second answer is the word "Preamble" in a substitution
cipher drawn at random when the cryptogram appears, so it differs between games **(verified: code read from
2SMITH.OVL; key and answer read from memory, two different keys seen)**.
**Intended:** yes: the player must decode the enciphered preamble to learn the cipher.
**Confidence:** (verified).
**Impact:** walkthroughs cannot give the second answer, only the method.

## Defeat costs nothing that was saved (set start, 2026-11-20)
- Seen: the level-1 party lost to ten Orcs in C2 (2,5) before ever signing in. "Death Strikes!" and Enter put
  it at the Middlegate inn list with all six alive and full hit points; ryz's Short Sword, equipped after the
  start, was back in his backpack (profile identical to the one before equipping). Route: checkpoints `s_dead`,
  `s_resume` (shots start `48_death_strikes`, `49_inn_after_death`).
- Likely cause: the game reloads ROSTER.DAT, which creation and renaming had already written; a defeat only
  loses what happened since the last write. **(verified on screen; cause inferred)**
- Also: the Middlegate fixed fight at (8,1) (cats and rodents) cannot be reached on foot: the square is walled
  in on every side (wall map, see the playbook RAM map 161D6); the main set reached it by position poke.
