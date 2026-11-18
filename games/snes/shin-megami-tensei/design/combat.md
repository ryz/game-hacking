# Battles and demon negotiation

## Overview
Random encounters start on the second day, on the town-map streets: the view switches to the street in
first person, the enemy group is named and drawn, with one icon per demon at the top of the screen. Each round
the player picks a party command, then a move per character; then both sides act and every action is reported
in a text box that waits for a button. Talking to demons (negotiation) is a branching conversation that can
end in a deal (money, Magnetite, a new minion) or in a fight. The moon phase shown in the corner matters:
at full moon demons refuse to talk.

## 1. Commands
| Level | Commands | Evidence |
|---|---|---|
| Party command ("Command?") | FIGHT, ESCAPE, TALK, AUTO | **(verified: `../shots/main/shin-megami-tensei_snes_jp_battle_first_battle.png`)** |
| A character's move | SWORD, GUN, COMP, ITEM, DEFEND, then "Is this all right?" Yes / No | **(verified: `../shots/main/shin-megami-tensei_snes_jp_battle_battle_commands.png`)** |
| ESCAPE | "Started to run....... but failed!" is possible; the enemies then act | **(verified: `../shots/main/shin-megami-tensei_snes_jp_battle_battle_escape.png`)** |

## 2. Numbers seen in the first battles
| What | Value | Evidence |
|---|---|---|
| Level-1 hero (STR 11) with the Attack Knife against a Jirae Brownie | 8 damage per hit; 5 of 6 swings landed, one missed ("Crap! They dodged it!") | **(verified: checkpoints `battle1_*`)** |
| Brownie's normal attack on the hero (VIT 10) | 4 damage every time (6 hits) | **(verified)** |
| Brownie's hit points | two 8-damage hits defeat one (16 or less) | **(verified)** |
| Brownie's spells | Sukunda ("The group's accuracy down!"), Sukukaja ("The demons' accuracy went up!") | **(verified: `../shots/main/shin-megami-tensei_snes_jp_battle_battle_enemy_spell.png`)** |
| Reward for two Brownies | 16 EXP, 64 yen | **(verified: `../shots/main/shin-megami-tensei_snes_jp_battle_battle_result.png`)** |
| Level 2 | reached with 16 EXP; at level 2 the screen shows "Next 24" (level 3 at 40 EXP) | **(verified: `../shots/main/shin-megami-tensei_snes_jp_system_level_up.png`)** |
| Level-up | maximum HP 22 -> 26, HP refilled, one stat point to place on the stat screen | **(verified: `../shots/main/shin-megami-tensei_snes_jp_system_level_up.png`)** |
| Death | the hero at 0 HP: "ryz died!", then a river scene ("Do not be afraid...") and back to the title | **(verified: `../shots/main/shin-megami-tensei_snes_jp_gameover_gameover.png`)** |

## 3. Negotiation
TALK opens the conversation **(verified: `../shots/main/shin-megami-tensei_snes_jp_system_demon_talk.png`)**:
1. "Take which attitude?" Friendly / Threatening.
2. The demon reacts in its own voice and offers a choice of the hero's reply (the Pixie: "Pixie is teasing
   you" -> Smile / Act scared; after a threat: Intimidate / Approach it, "Can you kill demons in cold
   blood?" Yes / No) **(verified: `../shots/main/shin-megami-tensei_snes_jp_system_demon_talk_tease.png`)**.
3. A threatened demon gives in: "What will you ask for?" Make it your minion / Money / Magnetite / Go away
   **(verified: `../shots/main/shin-megami-tensei_snes_jp_system_demon_talk_ask.png`)**.
4. Demands: a sum of yen first (the Pixie asked 226 yen on the friendly path, 65 yen on the threatening one),
   then "More! More!" and an item (both times a Bead) **(verified: `../shots/main/shin-megami-tensei_snes_jp_system_demon_talk_offer.png`)**.
   Not having the item ends the talk: "Arrgh! You skinflint!... I want your everything!" and the fight goes on
   **(verified: `../shots/main/shin-megami-tensei_snes_jp_system_demon_talk_fail.png`)**. The yen is paid (5064 -> 4838 and 5064 -> 4999)
   **(verified)**.
5. At full moon the talk stops at once: "It's no good! They're spoiling for a fight!"
   **(verified: `../shots/main/shin-megami-tensei_snes_jp_system_talk_fullmoon.png`)**.
The demand did not change with the timing of the reply (four timings, same Bead request) **(verified)**.

## Open questions
- What a demon that joins says, and the MAG cost of summoning (no Bead was available).
- Whether DEFEND reduces damage (the one try was cut short by a poked HP of 1).
- AUTO, GUN without a gun, COMP and ITEM in battle.
