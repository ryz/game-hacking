# World and structure - Devil Buster, the shelter, Tokyo

## Overview
The game opens inside **Devil Buster**, a computer game the hero plays: an overhead maze of eight connected floors
linked by stairs, with random battles **(verified, warp table read from the ROM: (RAM))**. Losing a fight inside
Devil Buster is not the end: the GAME OVER page ("THE WORLD WILL PERISH!") is followed by the real-world computer
room, where the best friend (EBO) laughs at the hero for quitting, and the home computer offers BOOT GAME / LEAVE /
SAVE DATA **(verified: shots `gameover`, `computer_room`, `computer_menu`)**. LEAVE puts the hero and his friend in
the **shelter**, a first-person maze (floor B4 at first) guarded by soldiers **(verified: `shelter`,
`shelter_soldier`, `shelter_gate_guard`)**. Outside lies an overhead map of ruined Tokyo with first-person caves and
buildings **(verified: `tokyo_overworld`, `dungeon_3d`, `heal`)**.

## 1. Views
- **Overhead maps:** Devil Buster and the Tokyo overworld are drawn from above; one step is one 16-pixel square
  **(verified)**. Walking onto a stairs square changes floor at once, without a fade **(verified)**.
- **First-person mazes:** caves, the shelter and buildings use a large first-person view with the floor and facing
  ("1F S", "B4 S") in the top right and the moon phase top left **(verified: `dungeon_3d`, `shelter`)**. Up steps
  forward, Down turns round, Left/Right turn **(verified)**. Walking back out of the entrance square returns to the
  overworld **(verified)**.
- **Field command screen** (A): moon phase, WEALTH (Macca, MAG), a picture window (the corridor ahead in a maze, a
  landscape picture on the overworld), CMD COMP / MAGIC / ITEM / STATS and the party list **(verified: `hud_cmd`,
  `cmd_overworld`)**.

## 2. Devil Buster floors
Eight floors, each a 24 x 24 block of one large map; stairs come in pairs (down and back up) **(RAM: warp table)**.
| From floor | Stairs to | Notes |
|---|---|---|
| 1 | 2 | the first room's stairs square **(verified)** |
| 2 | 3 | |
| 3 | 4 | six pairs of stairs between floors 3 and 4 (a stairs maze) **(RAM)** |
| 4 | 5 | |
| 5 | 6 | |
| 6 | 7 | |
| 7 | 8 | arrival square on floor 8 **(verified)** |
| 8 | ? | the last listed stairs sit inside the top wall of floor 8 and cannot be walked onto **(verified)**; their target is drawn as a grey stone temple where every step reports ERROR (see findings) |
How Devil Buster is completed (round 2) **(verified: shots `taurus_appears` to `pazuzu_armory`)**: floor 1 is **Micon
town** ("8F of the Daedalus Tower"), with an elder, a healer, a shop, a fusion master and townsfolk whose hints give the
goal: Taurus holds the S.ORB, Taurus must be killed, and the S.ORB must be offered to the fallen god statue. Taurus waits
on a fixed square of floor 2; beating him gives the S.ORB. Offering it at the statue frees **Pazuzu** ("BORN FROM FIRE
AND STORM / I AM PAZUZU... FREEDOM.. REALITY AT LAST..."), who tells of the war at the end of the 20th century, the
demons coming through a dimensional rift in Tokyo, and Bael, Tokyo's ruler, who sealed him in the machine. He names
RYZ and EBO messiahs, gives magic to EBO, the Demon Summoning Program and an auto-mapping program to RYZ, and sends
them to kill Nebro on B1; they head for the armory and play continues in the shelter, floor B4. Full room and event
list: [maps.md](maps.md). The listed floor-8 stairs are not part of this route.

## 3. Places seen
| Place | What is there | Evidence |
|---|---|---|
| Computer room | the home computer; EBO's remarks after a Devil Buster game over; BOOT GAME / LEAVE / SAVE DATA | `computer_room`, `computer_menu` (verified) |
| Shelter B4 | green metal corridors; a soldier ("REAL LIFE IS NOT A GAME."); guards at four DANGER gates who turn the boys away; three staircases ("USE THE STAIRS?" YES/NO) | `shelter`, `shelter_soldier`, `shelter_gate_guard` (verified) |
| Floor below the B4 stairs | grey stone corridors with a ladder hole | checkpoint `shelter_stairs1` (verified) |
| Healer's temple | grey stone hall with statues and pools; a hooded healer ("I CAN HEAL.") | `heal` (verified) |
| Tokyo overworld | red wasteland, grass, hills, a settlement, cliff caves, purple holes that lead into caves | `tokyo_overworld` (verified) |
| Settlement north of 11,2B | houses, an armour shop (clerk in Jamaican patois: "WAGWAN?"), a save totem (LEAVE / SAVE / Teleport) | `village`, `shop`, `save_totem` (verified) |
| Other towns | registry, slot machines, gambling, drugstore, bar, gun and weapon shops (maps.md) | round-2 scan (verified) |
| Cave 1F | blue organic rock corridors | `dungeon_3d` (verified) |

## 4. Saving
The home computer's SAVE DATA and the totems in the towns offer two slots, DATA1 and DATA2 **(verified: `save_slots`,
`save_recorded`)**; the totem's confirmation "RECORDED." is translated. The totem's Teleport lists the totems already
visited (only HANEDA at first, untranslated) **(verified: `teleport_list`)**. The confirmation line
after saving is printed as unreadable characters in this translation (findings) **(verified)**.

## Open questions
- Where the first shop is; the events of the other shelter floors.
- Whether BOOT GAME resumes Devil Buster where it was left.
