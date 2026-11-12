# Reaching a chest and the bank-45 maze events (EN build)

Build used: `build/wizardry_empire_en.gbc` at e45012c, copied to `work/re/reach/wizardry_empire_en.gbc`
(SHA-1 efc0cb41f6daa69141e95acdbd905cfe02042ec8). Party states: `python3 tools/party.py --rom
work/re/reach/wizardry_empire_en.gbc --out work/re/reach/start`. Code addresses are Rev 1 (JP); every routine
named below was also hit by a breakpoint in the EN build (25:40CB, 25:4134, 2D:63EB), so they are unchanged there.

## 1. Answer
Random encounters never drop chests. After a victory, 25:40CB shows a chest only when `$C00B` bit 2 = 1 and
bit 3 = 0. The only code that sets bit 2 and leaves it set is 20:5D0B (`or $06`), the handler for **guarded
squares** (map square type 6). Floor 1 has seven of them; the nearest is **(6,15), 22 steps from the maze
entrance**, and a party walking there with no pokes gets a guardian fight and then a chest. The other way:
poke `$C00B |= $04` during any battle. Events are map squares too. Each cell of the floor map (WRAM4 `$D000`,
a copy of ROM `3E:4000 + $400*floor`) has a type. Types 6/7/A-F/10/11 call the bank-45 dispatcher 2D:63EB,
with `$FFB0` = type (or a per-floor code) and `$FFB1` = parameter. The handler comes from the table at
`2D:4400` (index = `$FFB0`-7). To reach an event, poke the party onto the square next to it, facing it
(`$CB80`/`$CB81`/`$CB83`), and press Up.

## 2. Evidence

### RAM (maze)
| addr | meaning |
|---|---|
| `$CB80` | x (0-15) |
| `$CB81` | y (0-15); map row = y XOR 15 |
| `$CB82` | floor - 1 (floor 1 = 0, floor 2 = 1) |
| `$CB83` | facing: 0 = y+1, 1 = x+1, 2 = y-1, 3 = x-1. `right` = +1, `left` = -1 (20:4740 move code: bit 0 = x/y, bit 1 = dec) |
| `$CB96-$CB98` | previous x, y, floor (copied at 20:472E before a move) |
| `$CB85` | party count |
| `$C00B` | encounter flags: bit 0 = moved, bit 1 = fixed/event battle, **bit 2 = chest after victory**, bit 3 = no chest, bit 4 at 25:4010 = other screen (25:5337) |
| `$C48E` | monster group of the fixed encounter (from map byte 1) |
| `$C6DB+` / `$C6DD+` | one-shot bitfields (0:2B8C tests bit `a&7` of `[hl + a>>3]`): guarded squares by parameter (20:5CF7), type-E events by parameter (20:5F95) |
| `$C634` / `$DD35` | chest type picked at 25:4135 |
| `$C880+$80*n` | party records: +$09 class, +$0C status, +$10..$1F 8 item pairs [flags][id] |

maze.state (party.py): x=0 y=15 floor 0 facing 2, on the up-stairs square.

### Map format (20:5909)
Cell = 4 bytes at `$D000 + ((y^15)<<4 | x)*4`, WRAM bank 4. Floors 1 and 2 match ROM `3E:4000`/`3E:4400` byte
for byte (checked in the emulator).
- byte 0: walls, 2 bits per facing (bits 2d..2d+1). 0 = open, 1 = wall ("Ouch!"), 2 = door (20:46F4), 3 = depends on `e` bit 0 (20:45EF).
- byte 1: parameter (group id for type 6)
- byte 2 & $3F: square type
- byte 3: parameter c

Square dispatch 20:5A82: the handler is `[[$6405 + 2*floor] + 2*type]` (bank 20). The first 15 types are the
same on every floor:
0/5 nothing, 1 = 5AC7, 2 up stairs, 3 down stairs, 4 = trap 5BFE, **6 = guarded square 5CF0**, 7 = 5D1C,
8 = 5D36 (spinner/pit, by c&$E0), 9 = 5F4C, A/B/C = 5F4E -> 60EB (event with b = type, c = param), D = 5F51,
E = 5F85 (event, one-shot via `$C6DD`). F/10/11 are per floor: floor 1 F = 609C -> b=$1A, floors 2-4 F = 60AB -> b=$1D.

### Chest decision (bank 25 = post-battle treasure screen)
- 25:4000 runs after every victory (found with a breakpoint while fighting; the caller is 2F:5313 via 0:2121).
- 25:40CB: `ld a,[$C00B] / bit 3 / jp nz,$416E / bit 2 / jp z,$416E`. $416E = gold pile, no chest.
- 25:40D8-410E: b = the highest `[$D4E5 + $40*g]` among the groups present (`$D4B8 + $40*g` != 0). That is a
  row of the 256-byte table at 37:4000 + row*$100. The roll at 25:4117 (`call 0:0DA6`) picks a byte from the row
  -> chest type. 25:4125: if `$C003`=$A5 and `$FFC4`!=0, the type is `$FFC5` (debug override; `$FFC4/C5` have many
  other users, so I did not use it).
- Type ranges (25:413E): 0-6 leather bag, 7-12 bronze, 13-18 copper, 19-24 silver, 25-30 gold, 31-35 platinum,
  36-40 paulownia, 41-45 lacquered, 46 jet-black, 47+ bewitching. Rows 0-6 always give a bag, so floor 1 gives
  bags (the JP reference chest_menu is also a bag).
- Setters of `$C00B` bit 2, from a byte search of every `$C00B` access: 20:5D0B `or $06` (guarded squares only);
  2C:4C96 `or $04` is a temporary push/pop around the found-character sheet. Random encounters (20:5F6C,
  5FF4, 6035, 610E) `or $02` only. **This is why the playtester saw no chest in 25 random battles.**

### Events (bank 45)
- 2D:63EB: b = `[$FFB0]`; handler = word at `2D:4400 + 2*(b-7)`. Type $0E indexes a sub-table by `[$FFB1]`.
  The full table and the map from each bank-45 message to its handler are in `work/re/reach/scr/evtab.txt` (untracked),
  made by `work/re/reach/scr/evtab.py`, which scans `ld a,lo/ld [$C1BF]/ld a,hi/ld [$C1C0]`. NPC texts (45B7-4F28) have no
  inline site: they come from the table `2D:66C5 + param*8` (2D:6775).
- Floor 1 squares (ROM 3E:4000): guarded (6) at (6,15) (11,12) (9,9) (0,5) (9,4) (13,2) (7,1) (5,0);
  traps (4) at (11,15) (12,15) (4,10) (0,9) (1,9) (4,9); type 8 at (9,13) (0,2); down stairs (15,0);
  events: **(5,4) E p0, (2,12) F, (15,15) A**.
- Floor 2 (3E:4400): up stairs (15,0), down stairs (0,15); **(9,10) C p0**; guarded (5,12) (10,8) (6,2);
  traps (6,9) (6,8); type 8 at seven squares.

| square | $FFB0 | handler | messages | variant condition |
|---|---|---|---|---|
| F1 (5,4) | $0E p0 | 2D:6976 | 5009 "Gold coins lie scattered. Pick them up?" -> 5043 (they come alive) / 5064 (gold) | one-shot `$C6DD` bit 0 |
| F1 (2,12) | $1A | 2D:728A | 5C6D "A fairy is here... it fled"; **with item $AD (Fairy's Heart) and gold**: 5C97 + 5CC3 (teleport for 1G), 5D18 | 2D:7293 item scan, 2D:72B4 gold >= 1 |
| F1 (15,15) | $0A | 2D:64CF | 4490 "A strange pattern..."; **with a class-$0D member (status < 3)**: 44A8 magic circle "Who will step inside?", then 44CF/4512/452F/453D | 2D:64DA class at +$09 |
| F2 (9,10) | $0C p0 | 2D:6705 | 45B7 Murphy, 4626, 46A1 "Add Murphy?", 46E0; 45A6 party full | roster < 20 (2B:4037), join flag (2D:6722) |

## 3. States (`work/re/reach/states/`), and how to rebuild them
Scripts: `tools/maze_goto.py`, `tools/maze_route.py`, `tools/maze_make_chest.py`. Every one takes the ROM and absolute state paths, so they work with a new
build. Inputs use `tools/emu.py` press timing (8 frames held, 40 released).

| state | what | how |
|---|---|---|
| `guardian_before.state` | F1 (6,14) facing (6,15) | maze.state + `tools/maze_route.py 1 0 15 2 6 15` tokens without the last `up`: `left,up,right,up,up,left,up,up,right,up,left,up,up,right,up,left,up,up,up,up,left,up,left,up,right,up,up,left,up,up,right` (`work/re/reach/scr/walk.py`, untracked). No pokes; no random battle on this route |
| `guardian_battle.state` | guarded-square battle start (`$C00B`=04) | guardian_before + `up,w120` |
| `chest_victory.state`, **`chest_menu.state`** | victory at 25:40CB, then the chest menu (leather bag), **no pokes** | `tools/maze_make_chest.py ROM states/guardian_battle.state OUT` (A held 4 frames + 20 frames free, x89 until 25:40CB; then `w60,a,w60`). Its `$C00B\|=4` poke changes nothing here (bit 2 is already set) |
| `chest_menu_poke.state` (+`chest_victory_poke`) | chest after a **random** battle (Skeleton) | `tools/explore.py ROM start/maze.state walk7 1500 7` (hit at step 64) -> `tools/maze_make_chest.py ROM walk7/hit.state OUT`: pokes `$C00B\|=$04` at battle start, x34 A |
| `chest_menu_bronze.state` | bronze chest | same as poke + type 9: `tools/maze_make_chest.py ROM walk7/hit.state OUT 9` (sets B=9 at 25:4134) |
| `event_5009.state` | F1 (5,3) facing (5,4), gold coins | `tools/maze_goto.py ROM start/maze.state 5 4 OUT` |
| `event_5C6D.state` | F1 (1,12) facing (2,12), fairy (flees) | `tools/maze_goto.py ROM start/maze.state 2 12 OUT` |
| `event_5C97.state` | fairy, teleport offer | event_5C6D + poke `$C896,$C897 = 00 AD` (Fairy's Heart in ryz slot 3) (`work/re/reach/scr/variant.py IN OUT C896=00ad`, untracked) |
| `event_4490.state` | F1 (14,15) facing (15,15), strange pattern | `tools/maze_goto.py ROM start/maze.state 15 15 OUT` |
| `event_44A8.state` | magic circle (who steps inside) | event_4490 + poke `$C889 = $0D` (ryz class) |
| `stairs_f1_down.state` | F1 (14,0) facing the down stairs | `tools/maze_goto.py ROM start/maze.state 15 0 OUT 60` |
| `floor2.state` | floor 2 arrival (15,0) | stairs_f1_down + `up,w60,a,w200,down,a,w60` (Yes to go down; No to "climb up?") |
| `event_45B7.state` | F2 (9,11) facing (9,10), Murphy | `tools/maze_goto.py ROM states/floor2.state 9 10 OUT` |

In every `event_*` state, a single `up` starts the event. `tools/maze_goto.py` checks this with a count-only breakpoint on
2D:63EB (`$FFB0` matched in all six) and writes `*_before.png` / `*_after.png`. How `tools/maze_goto.py` works: it picks
the first neighbour whose wall bits towards the target are 0, pokes `$CB80/$CB81` (and `$CB96/97`) plus
`$CB83` = facing, then presses `left,right` so the view redraws. The event squares on floors 1-2 cannot be
walked to without crossing trap, guarded or type-8 squares (`tools/maze_route.py` BFS), so they use the poke.
`tools/maze_route.py FLOOR X0 Y0 DIR0 X1 Y1` prints walking tokens. `ROUTE_ALLOW=4,6,8` lets it cross special squares.

## 4. Hook proposal
None needed (reachability task, no text routed).

## 5. Open questions
- `$C00B` bit 3 (no chest even with bit 2): no direct setter found (`set 3` absent); it may come from a whole-byte
  write. Not needed here.
- The guarded-square flags (`$C6DB` by parameter): not checked whether they reset per floor or on leaving the maze.
  If a rebuilt party has already cleared (6,15), clear bit 0 of `$C6DB`.
- I did not check whether type 7/D/9 squares exist on floors 1-2 (none in the maps), or what types 1 and 8 do.
- The fights take 34/89 A presses with the default party: deterministic for this build. If a text change alters
  timing, the scripts still stop at 25:40CB, but the press count can differ.
