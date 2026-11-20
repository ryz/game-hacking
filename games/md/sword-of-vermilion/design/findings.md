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

## Round 3 (2026-11-20)
- Town lines are chosen once, on entering the town, from (table, flag) pairs at ROM 0x1EB0C (Wyclif: FFC818 ring
  -> 0x2D494, FFC720 Blade -> 0x2D45C, else 0x2D424); a flag set inside the town changes nothing until the town is
  left and entered again **(verified: poke inside Wyclif kept the old line)**.
- Map gifts set the map flags when the line is shown, before the next page **(RAM)**.
- The area-map panel is redrawn only on map entry or a mirror use: a flag poked mid-map shows nothing until the
  next map edge or town exit **(verified)**.
- Encounter types 0x56 and above (and 0x80-0xFF) crash or hang the battle loader **(verified)**: no range check.
- The battle HP readout can show 0 while HP is frozen at 33: the panel is drawn from the value before the
  freeze is applied again **(verified: `w10*28` frames)**.

## The boss-start routine clears the byte before the boss's flag
**Behavior:** the code that starts a boss fight (ROM 0x2A92, again at 0xEB22) finds the first non-zero byte in
FFC800-FFC80F (the boss index), then clears FFC817 and `-2(a0)`, which is the byte *before* the found one (a0
points one past it), and then clears FFC800-FFC80F anyway. The extra write lands on FFC7FF for boss 0.
**Intended:** probably `-1(a0)` (clear the found flag); harmless because the whole block is cleared next.
**Confidence:** (code) read with `tools/dis68k.py`; not traced in play.
**Impact:** none seen (FFC7FF's use is unknown).

## Boss 3 is boss 2 again
**Behavior:** poking boss index 2 and 3 gives the same two-skulled beast picture at the same moment (preview of
all 14 indices, 2026-11-20); both point at the same setup routine (0x594) in the table at 0x3694.
**Intended:** two placements of the same boss (the game has 14 table slots for fewer distinct bosses; 8-12 are
recolours of 0, 1, 2 and 4).
**Confidence:** (verified) picture; stats not compared.
**Impact:** none.
