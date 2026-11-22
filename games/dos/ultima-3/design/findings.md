# Ultima III: Exodus (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The shop behind a counter depends on the row
**Behavior:** Transact over a counter opens the pub, grocer, healer, weapons, armour, Guild, oracle or stables
by the party's row on the town map (row mod 8), not by the sign or the merchant (code; verified for five kinds
at their counters, `try_t4.png`).
**Intended:** the maps were laid out so that each counter sits on the right row; a compact way to store shops.
**Confidence:** (code), (verified).
**Impact:** none in normal play; a counter on a "wrong" row would open another shop.

## Digging for Exotics is not limited
**Behavior:** DIG on the two islet squares adds one Exotic weapon or armour to the digger each time; the code
marks two bytes of the party file but never tests them (code).
**Intended:** probably one find per game.
**Confidence:** (code), (RAM: digging twice at (21,03) raised ryz's Exotic weapons from 1 to 2 to 3, 2026-11-19).
**Impact:** every character can dig its own Exotics.

## Idle turns count as moves
**Behavior:** the moves counter shown by Quit & Save and the ending grows with the automatic Pass every five
seconds: a party that never moved showed "00000008 moves" (verified, `@start,q`).
**Intended:** unclear (the Apple II original counts turns the same way).
**Confidence:** (verified).
**Impact:** the "Report thy feat!" count rewards fast play at the keyboard.

## The level shown is not the level Lord British counts
**Behavior:** the panels show L = experience / 100 + 1, while Lord British raises maximum hit points only when
the experience hundreds reach the current maximum's hundreds (code; verified "Experience more!" and "Thou art
greater").
**Intended:** levels as hit-point tiers.
**Confidence:** (code), (verified).
**Impact:** a character can show L:24 with far fewer hit points until it visits the king.

## Spelling in the game's text
**Behavior:** "compleated" in the ending, "pannels" in Montor East, "Resurect whom?" in the spell prompt, "Bobbit"
for the halfling race (ROM text, the ending verified).
**Intended:** typos of the period (Bobbit is deliberate).
**Confidence:** (ROM text).
**Impact:** quote them as written in captions.

## A calm stops every frigate
**Behavior:** the sailing check refuses a move when the wind is calm as well as when the frigate sails toward
the side the wind is named after (code at 0x7233; "Invalid Move!" sailing east into an East Wind,
`system_wind`). The wind turns calm about one time in nine for 25 turns.
**Intended:** probably (a sailing ship needs wind), but the game never says why the ship will not move.
**Confidence:** (code), (verified for the head wind).
**Impact:** a stranded frigate waits up to 25 turns; X-it is impossible at sea.

## Monster damage follows the victim's hit points
**Behavior:** a monster's damage is 1 + a random number below its base plus the first two digits of the
target's maximum hit points (code at 0x92AF; an orc hit a 2300-point ryz for 29, `battle_orc_hits`).
**Intended:** a crude difficulty curve: fights stay dangerous as Lord British raises hit points.
**Confidence:** (code), (verified one hit).
**Impact:** hit points alone never make a party safe; Exotic armour (a miss chance) matters more.

## A wrong card kills the inserter outright
**Behavior:** INSERT with the wrong card or at the wrong slot sets the inserter's hit points to 0 (code at
0x76C9; `system_insert_wrong`: ryz D, H:0000).
**Intended:** yes ("All else fails", the Time Lord).
**Confidence:** (code), (verified).
**Impact:** a guess at Exodus costs a resurrection (500 gold, or Surmandum).

## Surmandum raises with no hit points
**Behavior:** a successful Surmandum turns D into G but leaves H.P. at 0000 (`system_spell_surmandum`).
**Intended:** unclear; the healer's resurrection behaves the same in RAM (status only).
**Confidence:** (verified).
**Impact:** a raised member must be healed at once or the next hit kills again.

## Bribes and the gate guard give no message
**Behavior:** a successful bribe takes 100 gold and removes the guard without a word ("Direct? North" is the
last line, `system_bribe`; gold 4352 -> 4252 in RAM); a failed one says "No effect!".
**Intended:** probably an oversight in the message.
**Confidence:** (verified, RAM).
**Impact:** the player sees the guard vanish but not the cost.

## Ready is not a combat command
**Behavior:** R during a fight answers "Not usable cmd!"; weapons are readied on the map only (verified).
**Intended:** unclear (the program holds a "Ready a weapon!" text).
**Confidence:** (verified).
**Impact:** a party must choose bows or blades before a fight.

## Only one counter in Sosaria can be robbed
**Behavior:** Steal needs a counter square and a chest right behind it; of all townes only Grey has one, at the
Weapons counter (map survey; `system_steal`).
**Intended:** Grey is the thieves' towne.
**Confidence:** (verified, map files).
**Impact:** Steal is a one-place command.

## Ambrosia's whirlpool hands out a frigate
**Behavior:** Ambrosia's whirlpool returns the party to Sosaria aboard a frigate ("All is Dark! You made it!",
`cutscene_ambrosia_return`), although the ship was lost on the way in.
**Intended:** yes, a way home.
**Confidence:** (verified).
**Impact:** a free frigate, also on land squares when the party left Sosaria from land (seen with a poked
whirlpool).

## Fountain kinds by column (corrects the scout)
**Behavior:** a fountain's kind follows its column x mod 4: 0 poison, 1 heal, 2 hurt, 3 cure (verified in the
Dungeon of Fire, `system_fountain_*`); the scout's note had another order.
**Intended:** a compact way to vary fountains.
**Confidence:** (verified).
**Impact:** a player can learn a fountain's kind from its position.

## Wandering monsters stall at brush
**Behavior:** a monster spawned west of LCB walked diagonally towards the party at (2E,13) and stopped at (20,13) for over
200 turns, with brush and the Yew mountains between (start-set scan from `s_out`, 2026-11-22); another run's monster
walked straight in over grass. They seem to step only onto open grass in the party's direction, with no way around.
**Intended:** unclear (simple chase).
**Confidence:** (RAM) positions read each turn; the movement code not read.
**Impact:** a party can wait safely behind brush; to meet a monster early, walk towards it.

## The first chest of a new game can be trapped
**Behavior:** the ghoul's chest opened by ryz (Dex 10) at the start: "Bomb trap!" hurt all four (150 -> 94, 91, 126, 128)
and gave Gold+59 (`s_chest`, start shot `54_chest_bomb`). Nothing protects a new party from traps.
**Intended:** yes (thieves and Appar Unem exist for this).
**Confidence:** (verified).
**Impact:** a new party should open chests with its thief or skip them while hurt.
