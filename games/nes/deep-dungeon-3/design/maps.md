# Deep Dungeon III - towns and dungeon floors

## Overview
The world is a set of square grids walked in first person: one grid that holds the towns (32 squares wide, 48 long,
several towns packed side by side) and four dungeons, each a stack of 32 by 32 floors: the underground (2 floors),
the cave (4), the tower (6) and the castle (4) **(verified: the tower and castle entrances name themselves,
shots `tower_entrance`, `castle_entrance`; the underground's own wall text calls it ちか, the cave's どうくつ)**. A sixth
"area" is the ending sequence (section 6).
Every square is either solid wall or open; doors, stairs and events sit on squares, not on the edges between them
**(verified: walking and bumping into walls matches the grids)**. The maps in [maps/](maps/) are drawn from the
game's own data by `../tools/maps.py`: dark blue wall, white floor, blue door, red shut door, green U/D stairs
(up/down), yellow numbered event squares, pink other specials. `maps/grids.md` has the same grids as text.
Coordinates are (x, y) with (0,0) the north-west corner; x grows east, y grows south **(verified)**.

## 1. Square types
| Code | Look | What happens | How sure |
|---|---|---|---|
| wall | solid | walking into it: "いたい! かべに ぶつかってしまった。" ("Ouch! You bumped into a wall.") | verified |
| floor | open | - | verified |
| door | door in the wall | A opens it / enters the building behind it | verified (inn door) |
| shut door | door | unknown (locked house? 16 in the towns) | open question |
| stairs down (D) | ladder down | "くだるかいだんが ある。つかいますか?" (There are stairs going down. Use them?) | verified |
| stairs up (U) | ladder up | "のぼるかいだんが ある。つかいますか?" (stairs going up) | verified |
| numbered squares | - | towns: buildings by kind (section 5); dungeons: per-floor events - fixed fights, messages, people, traps, items, masters (section 7) | verified |
In the tower the "up" stairs lead to the next floor (floor 1's U squares match floor 2's D squares) **(computed)**;
in the underground and cave the "down" stairs do **(computed)**. Stairs keep the position: a staircase is on the same
square on both floors **(computed)**.

## 2. Town stairs
Eight stair squares in the town grid lead to the first floor of the underground or the cave **(ROM)**:
| Town square | Leads to |
|---|---|
| (1,25) | underground floor 1 (1,1) (verified) |
| (16,46) | underground floor 1 (30,30) |
| (29,17) | cave floor 1 (3,27) |
| (30,1) | cave floor 1 (1,1) (verified) |
| (30,6) | cave floor 1 (1,6) |
| (6,23) | underground floor 1 (21,1) |
| (4,23) | underground floor 1 (13,1) |
| (8,18) | cave floor 1 (30,16) |
The tower and the castle have no stairs: their entrances are buildings. Building 7 of Ail (the door at (27,46))
opens on tower floor 1 at (1,15); building 8 of the north town (door at (3,7)) opens on castle floor 1 at (30,15)
**(verified: shots `tower_entrance`, `castle_entrance`)**. Stepping back onto that square asks "とうの/しろの
いりぐち まちにでますか?" ("Tower/Castle entrance - go out to the town?").

## 3. Stairs per floor (computed from the grids)
| Dungeon | Floor | Up | Down |
|---|---|---|---|
| underground | 1 | (1,1) (13,1) (21,1) (30,30) to town | (30,1) (1,30) (20,30) |
| underground | 2 | (30,1) (1,30) (20,30) | - |
| cave | 1 | (1,1) (1,6) (30,16) (3,27) to town | (30,1) (25,3) (6,17) |
| cave | 2 | (30,1) (25,3) (6,17) | (4,3) (29,3) |
| cave | 3 | (4,3) (29,3) | (30,4) (18,7) (18,24) (5,30) |
| cave | 4 | (1,2) (30,4) (9,5) (14,29) | - |
| tower | 1 | (27,8) (16,15) | - |
| tower | 2 | (15,14) (4,23) | (27,8) (16,15) |
| tower | 3 | (17,2) (2,14) (16,17) (29,17) (14,29) | (15,14) (4,23) |
| tower | 4 | (17,5) (5,14) (15,14) (26,17) (14,26) | (17,2) (2,14) (16,17) (29,17) (14,29) |
| tower | 5 | (16,2) (2,15) (21,16) (29,16) (15,29) | (17,5) (5,14) (15,14) (26,17) (14,26) |
| tower | 6 | - | (16,2) (2,15) (21,16) (29,16) (15,29) |
| castle | 1 | (4,3) (27,3) (27,16) (4,28) (27,28) | - |
| castle | 2 | (21,16) | (4,3) (27,3) (27,16) (4,28) (27,28) |
| castle | 3 | - | (21,16) |
| castle | 4 | - | - (reached by an event) |

## 4. Maps
| File | What |
|---|---|
| [maps/towns.png](maps/towns.png) | the town grid: three towns (section 5) |
| [maps/area1_f1.png](maps/area1_f1.png), [f2](maps/area1_f2.png) | the underground |
| [maps/area2_f1.png](maps/area2_f1.png) .. [f4](maps/area2_f4.png) | the cave |
| [maps/area3_f1.png](maps/area3_f1.png) .. [f6](maps/area3_f6.png) | the tower |
| [maps/area4_f1.png](maps/area4_f1.png) .. [f4](maps/area4_f4.png) | the castle (floor 4: twelve rooms of statues) |

## 5. The three towns
The town grid holds three separate towns that cannot be walked between; they are linked only through the
dungeons **(computed: flood fill of the grid; verified walking and by the buildings' contents)**.
| Town | Part of the grid | Buildings (number on the map: what) | Stairs |
|---|---|---|---|
| Dirige (ディリージュ), the starting town | south-west, x 0-15, y 24-47 | 1 (1,27) item shop, 2 (7,36) weapons and armour, 3 (13,44) temple, 4 (7,42) information seller, 5 (13,39) inn, 6 (3,40) magic training hall | (1,25) to the underground |
| Ail (アイル), "the eastern town" | south-east and middle, x 11-31, y 15-47 | 1 (13,23) item shop, 2 (29,28) weapons and armour, 3 (21,45) temple, 4 (23,39) information seller, 5 (19,33) inn, 6 (23,17) magic hall, **7 (28,46) the tower entrance**, the single $C7 square at (29,20) | (16,46) to the underground, (29,17) to the cave |
| the north town (not named in the game's text) | north, x 3-31, y 0-23 | 1 (23,12) item shop, 2 (17,2) weapons and armour, 3 (9,1) temple, 4 (30,10) information seller, 5 (20,12) inn, 6 (23,2) magic hall, **8 (2,7) and (8,7) the castle entrance** | (4,23), (6,23) to the underground; (30,1), (30,6) to the cave |
| a closed pocket | x 8-15, y 17-19 | 1 (13,18) an item shop | (8,18) to the cave (cave floor 1 at (30,16)) |
The building number is the kind of building, the same in every town **(verified in Dirige for 1-6, Ail 7, north
town 8: shots `item_shop`, `shop_arms_dirige`, `temple_menu`, `info_broker`, `inn_menu`, `magic_guild`,
`tower_entrance`, `castle_entrance`; the other towns' 1-6 inferred from the same numbers)**. Red "shut doors"
(16 squares, `d` in `maps/grids.md`) lead nowhere **(inferred: A does nothing at the one tried)**.
The underground joins Dirige (1,25) to Ail (16,46) ("this underground leads to the eastern town Ail, but a key is
missing", wall text on its floor 2) **(ROM stairs table + verified text)**.

## 6. The ending ("area 6")
Area number 6 is not a place: entering it plays the ending - the princess (portrait) thanks the party: the monsters
came out because she broke the seal of the stone monument by mistake; the seal stones and the sword must be put back
into the monument. Then a staff roll and "the End" under the monument **(verified by warping there: shots
`ending_princess`, `ending_credits`, `ending_thanks`, `ending_the_end`)**. Staff (on screen): game design Hiroshi
Takayama, Tetsuo Yasuda, Shinichi Tsuruta, Hidenori Katsura; scenario and visual design Tetsuo Yasuda; music and
sound Kazuya Matsusita; main programmer Shinichi Tsuruta, Hidenori Katsura; advice Yuka Inoue; director Hiroshi
Imanishi; producer HummingBird Soft.

## 7. Event squares per floor
Event numbers are local to a floor: the same number does different things on different floors **(verified)**.
Each square below was entered from the side given (N = walking north into it), with a level-1 party and no
special items; "-" means nothing happened from that side. Fixed fights fire every time the square is entered
**(verified for the ones shot; inferred for the rest)**. Numbers repeated on a floor behave alike **(inferred: one
square per number was tried)**. Squares $C1-$CF are solid (the party bumps) **(verified)**; the tips about pushing
walls suggest some are hidden passages **(inferred)**.

### Underground (ちか), floor 1 - green walls
| Square | No. | From | What happens |
|---|---|---|---|
| (17,2) | 0B | N | fixed fight: ants x3 and poison spiders (どくぐも) x2 |
| (17,3) | 01 | S | the stone monument: "a stone monument. The monsters must have come out from here!" (shot `ev_monument`) |
| (25,3) | 07 | N | fixed fight: バグボーン x1 |
| (25,4), (17,10), (6,14) | 08, 0C, 06 | N, E, E | - |
| (17,5) | 02 | E | "holes in the north and south walls: something broke through" |
| (17,9) | 03 | N | "a hole in the north wall: something broke through" |
| (1,11) | 04 | N | wall writing: "below is a prison! Rescue the people held there" (shot `ev_wall_writing`) |
| (13,28) | 09 | E | fixed fight: grizzlies x2 |
| (19,23) | C1 | E | solid |

### Underground, floor 2 - the prison (yellow walls)
| Square | No. | From | What happens |
|---|---|---|---|
| (17,1) | 0E | N | prisoner: "thank you for rescuing me!" |
| (27,1) | 0F | N | prisoner: "I thought nobody would come to rescue us" |
| (28,11) | 10 | N | prisoner: "the king and the princess have vanished - caught by the monsters?" |
| (13,13) | 0D | N | prisoner gives a bell (すず): "it will surely help" (shot `ev_prisoner_bell`) |
| (2,29) | 11 | N | "this underground leads to Ail, but it is locked: beat the monster and take back the key" |
| (8,30) | 13 | S | prisoner: "Buy Final Fantasy, it will surely help!" (Square's advertisement; shot `ev_final_fantasy`) |
| (13,27) | 0A | E | pit trap: the priest loses 22 HP (dies at level 1; shot `ev_pit_trap`) |
| (20,3) | 06 | S | fixed fight: rats x3 and mad dogs (きょうけん) |
| (19,15), (17,30) | 12, 07 | E, S | fixed fight: guards (えいへい) x3 |
| (8,25) | 08 | W | fixed fight: zombies x3 |
| (6,2), (29,4) | C1, C2 | N | solid |

### Cave (どうくつ), floor 1 - orange brick, dark
| Square | No. | From | What happens |
|---|---|---|---|
| (11,2) | 04 | S | an old man in a robe speaks |
| (15,3) | 0A | W | trap: the swordsman loses over 20 HP - at level 1 he dies and the game ends |
| (7,4) | 0D | E | "What are you? Get out, quickly!" |
| (23,5) | 07 | N | fixed fight: gorgon (ゴーゴン) x1 |
| (5,14) | C2 | N | fixed fight: バグボーン x2 and a vampire (バンパイア) |
| (17,24) | 01 | N | "a cursed sword! Keep away!" |
| (18,26) | 0B | S | "a well. With a rope ladder you could climb down" |
| (30,30) | 0C | E | "found a Sun Shield (サンシールド) - pick it up?" (shot `ev_sun_shield`) |
| (17,2), (10,5), (25,15), (26,15) | 81, 06, 13, 14 | - | - |

### Cave, floor 2 - blue brick
| Square | No. | From | What happens |
|---|---|---|---|
| (9,1) | 04 | N | wall writing: "the cave is a maze. If lost, use the Circlet" |
| (18,1) | 10 | W | "someone is here!" - a priest asks to join; he is ビルマン (Birman), level 15 (shots `ev_someone_here`, `companion_offer`, `companion_joins`) |
| (30,30) | 0F | S | "someone is here!" (another companion) |
| (27,1) | 0E | W | a man in a robe: "I am a messenger of the castle..." |
| (20,1) | 0A | E | pit trap: 23 HP |
| (23,4), (18,11) | 11, 12 | N, W | "suspicious water / white water wells up - drink it?" |
| (6,5) | 07 | N | fixed fight: giants (ジャイアント) x2 and a バグボーン |

### Cave, floor 3
| Square | No. | From | What happens |
|---|---|---|---|
| (19,26), (19,27) | 01, 0E | N, E | "a sword is stuck in the rock! Try to pull it out?" (shot `ev_sword_in_rock`) |
| (18,26) | 0F | N | "found a rope ladder - climb it?" |
| (14,2) | 04 | E | wall writing: "the master of the underground hates light!" |
| (30,20) | 0D | E | a man: "do you have the orb of light (ひかりのたま)?" |
| (30,30) | 10 | E | a man offers a sword for 3000 gold |
| (17,1) | 0A | N | pit trap: 23 HP |
| (7,1), (29,25), (24,28) | 06, 08, 07 | N, E, N | fixed fights: chimeras x2; gorgon and chimera; familiars (つかいま) x2 |

### Cave, floor 4 - Zosem's lair
| Square | No. | From | What happens |
|---|---|---|---|
| (14,4) | 14 | E | a voice: "Welcome. I am Zosem (ゾセム), master of the world below! Come quickly, I am waiting!" (shot `ev_zosem_voice`) |
| (28,4), (29,4) | 1B, C4 | N, E | **Zosem**, the master, attacks (shot `boss_zosem`) |
| (5,10) | 13 | E | a warrior: "at the end of the long corridor push the north wall: that is the entrance to the master's room" |
| (23,14), (17,21) | 17, 16 | S, N | "black water wells up - drink it?"; "found something - pick it up?" |
| (3,5) | 18 | N | a trap that kills the level-1 priest |
| (9,7) | 0A | E | pit trap: 26 HP, the swordsman dies at level 1 |
| (29,28) | 04 | E | wall writing |
| (19,1), (21,1), (23,1), (25,1), (19,2), (21,2), (27,4) | 07 08 09 0B 15 12 0C | - | fixed fights: dwarves x3; chimera; gorgon; familiars x3; dwarves x9; gorgons x2; catman (キャットマン) |

### Tower (とう), floors 1-6 - wall colour changes per floor (1-2 blue, 3 brown, 4 yellow, 5 green, 6 purple)
| Floor | Square | No. | What happens |
|---|---|---|---|
| 1 | (1,15) | 18 | the entrance from Ail: "go out to the town?" |
| 1 | (15,1), (15,30) | 0A, 0B | carry the party to floor 2 |
| 1 | (10,3) | 01 | a man: "a strong monster lives on the top floor" |
| 1 | (25,10) | 02 | a man: "they say the master of the tower hates beautiful sounds" (the bell from the prison) |
| 1 | (13,11) | 03 | a man: "the hand mirror (てかがみ) is somewhere on this floor" |
| 1 | (17,10) | 05 | "someone is here!" (a companion) |
| 1 | (14,28) | 04 | wall writing: steps east of the entrance, search between two pillars |
| 1 | (21,3), (22,8), (5,13) | 06, 08, 07 | fixed fights: kobolds; kobolds and a sylph; tower soldiers (とうのへいし) |
| 2 | (22,8) <-> (9,23) | 16, 15 | teleporters into each other |
| 2 | (3,12) | 10 | wall writing: "always draw a map! The adventurer's first rule!" |
| 2 | (26,25) | 0F | "『Room of the Guide』(しるべのへや) is written here" |
| 2 | (14,23) | 11 | a man: the monsters on this floor took the king |
| 2 | (21,3) | 12 | "someone is here!" |
| 3 | (8,8) | 02 | a woman: the seal that held the monsters broke - find the seal stones |
| 3 | (20,17) | 03 | a man: "would you give me a grass dew?" (yes/no) |
| 3 | (14,21) | 04 | "someone is here!" |
| 4 | (8,8) | 0E | wall writing: the two triangular stone tablets together make the seal |
| 4 | (16,15) | 0D | a man: the monster that made this world; the gods' sword |
| 5 | (7,2) | 03 | a man: the gods' sword cannot show its power... |
| 5 | (24,28) | 04 | wall writing: "the tower, the cave, the castle each have a master; the monster in the castle made this world" |
| 5 | (11,3) | 08 | "someone is here!" |
| 6 | (28,6) | 0B | a woman: "the master of the tower is in the Hall of Demons (ようまのま)!" |
| 6 | (12,15) | 16 | a door marked 『ようまのま』 |
| 6 | (18,16) | 15 | **バーザス (Barzas)**, master of the tower (shot `boss_tower_master`) |
| 6 | (3,4), (14,7) | 13, 14 | "blue water / white water - drink it?" |
| 6 | (7,2) | 0C | "someone is here!" |
Fixed fights in the tower: kobolds, sylphs, tower soldiers, harpies, death eyes (デスアイ), werewolves (おおかみおとこ),
lizardmen (リザードマン), hellhounds.

### Castle (しろ), floors 1-4 - green pillars
| Floor | Square | No. | What happens |
|---|---|---|---|
| 1 | (30,15) | 12 | the entrance from the north town: "go out to the town?" |
| 1 | (30,12), (30,13) | C5, 0A | a knight: "without a pass (つうこうしょう) you cannot go further!" |
| 1 | (5,6), (20,8) | 0C, 0D | knights: the king is held on floor 3, but the key...; a beast on floor 3 |
| 1 | (26,8) | 05 | wall writing about the flame of life and a sword |
| 1 | (27,5), (25,14), (1,6) | 09, 08, 07 | fixed fights: wyverns x3; wyverns x3; royal guards (しんえいたい) x2 |
| 2 | (14,1), (24,8), (12,9), (24,25) | 02, 01, 04, 03 | door signs: weapon store, soldiers' room, storeroom, the princess's room |
| 2 | (12,2) | 10 | a knight: "please save this country" (and the party is moved to floor 1) |
| 2 | (17,18) | 11 | a man laughing: "everyone was eaten by monsters!" |
| 2 | (9,16) | 05 | wall writing: two orbs, of light and of darkness |
| 2 | (18,15) | 07 | fixed fight: demons (デーモン) x2 and a wraith (レイス) |
| 3 | (29,15) | 05 | the king: the princess is under a monster's spell; show her this necklace (shot `ev_king`) |
| 3 | (27,4) | 03 | the flame of life: "whose sword will you search for?" (shot `ev_flame_of_life`) |
| 3 | (18,16) | 04 | a hole in the ceiling |
| 3 | (16,4), (2,5), (25,6), (11,12), (12,15), (13,15) | 0A 07 09 08 06 CE | fixed fights: high demons (ハイデーモン); royal guards x3; twilight (トワイライト) |
| 4 | (15,17) | 0B | a demon-faced figure: "the right door leads back to the first room; the middle door..." (shot `ev_castle_sage`) |
| 4 | (15,15), (25,29) | 1A, 18 | move the party (a hole up to floor 3 (18,16); to (15,18)) |

## 8. Warp tokens (for routes)
From the checkpoint `@warp` (cave floor 1, on the down-stairs prompt):
`poke:7003=AREA,poke:7004=FLOOR-1,poke:00EE=X,poke:00EF=Y,a,w150,poke:006F=FACING,left,right,w30`
(AREA 1 underground, 2 cave, 3 tower, 4 castle, 6 ending; FACING 00 north, 10 east, 20 south, 30 west; add `up,w150`
to step into the square ahead). Examples used by the shots: underground floor 2 bell prisoner `1,1,13,14,00` +
`up`; Zosem `2,4 (7004=03),28,5,00` + `up`; tower master `3,6,17,16,10` + `up`; ending `6,1,1,1`. In towns, move
with `poke:00EE=X,poke:00EF=Y,poke:006F=F,left,right,w30` and press `a` facing a door (from `@town`).

## 9. Data format (for tools; addresses are in ../playbook.md)
One byte per square, rows of 32, stored uncompressed. Wall = $80 (any value with the top bit set and the door
bit clear counts as solid), floor $00, door $C0, shut door $C8, stairs up $40, stairs down $41, events $01-$1B,
$81, $C1-$CF, town $C7 (one square). Dungeon floor F of dungeon A lives in the PRG bank listed by `tools/maps.py`
(underground 1, cave 2-3, tower 4-6, castle 7-8; odd floors at $9800, even at $9C00); the town grid in bank 9 at
$9700. The game copies the current grid to battery RAM.

## Open questions
- Squares marked "-" were tried from one side only, with no item in hand; several are probably item-gated (wells,
  waters, hidden walls), found with しらべる (search), or one-time events.
- The solid event squares ($C1-$CF) bump like walls from the side tried; tips such as "push the north wall at the end
  of the long corridor" suggest some open when pushed from one side. Not tested from every side.
- The third town's name: no text in the ROM names it (only Dirige and Ail are named).
- What the castle's "pass" (つうこうしょう) is, and how the castle floor 4 rooms connect.
