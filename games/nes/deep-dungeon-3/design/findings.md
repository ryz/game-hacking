# Deep Dungeon III: Yuushi e no Tabi (Famicom, Japan) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## A level-1 swordsman can die in the first fight
**Behavior:** on underground floor 1 three skeletons kill the 15-HP swordsman in the first round, which ends the
game at once (route `@round1,a,w60,a,w60`, shot `gameover_swordsman`). Several traps (cave floors 1 and 4) also do
more than 20 damage.
**Intended:** probably: the game expects the player to buy armour and build levels near the town first.
**Confidence:** (verified).
**Impact:** harsh start; save at the inn often.

## Square advertises Final Fantasy
**Behavior:** a prisoner on underground floor 2 (8,30) says "Buy Final Fantasy, it will surely help!" (shot
`ev_final_fantasy`). The publisher's own game had come out in December 1987.
**Intended:** yes, a joke/advert.
**Confidence:** (verified).
**Impact:** none.

## The temple's spell lesson went to the hunter
**Behavior:** choosing the third line of the "who learns" list after a level-5 party taught Cure to the hunter
こんでい, not the priest (shot `temple_learned`); the cursor's start position in that list may differ from the
party panel order.
**Intended:** unclear (may be the capture's cursor, not the game).
**Confidence:** (inferred).
**Impact:** none for players reading the screen.
