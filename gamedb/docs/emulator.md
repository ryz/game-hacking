# Emulator use - the general rules

How agents drive games here, for any game. Game-specific facts (controls, routes, RAM) go into
`games/<slug>/playbook.md`, never into this file. Paths are relative to `gamedb/`.

## Setup (once per container)
```sh
sh tools/setup_emu.sh                         # gbemu-cli: headless SameBoy, JSON-lines API (~1 min)
python3 tools/intake.py /path/to/game.gbc     # registers the ROM -> games/<slug>/, rom/<slug>.gbc
```
Containers are wiped between sessions: ROMs (`rom/`), states and caches (`work/`) are gone next time, routes and
playbooks (committed) are not. That is why every state is defined by a route.

## The model: routes, not states
- Emulation is **deterministic**: fixed seed (1), fixed boot ROM, turbo mode. The same route from power-on
  always gives the same frames. A route is the permanent record; a savestate is only a cache of it.
- **Checkpoints** (`games/<slug>/checkpoints.txt`, `name | description | route`) name the important points
  (title, first control, each world, each boss). Routes can start from another checkpoint (`@world2,...`).
  They are built on demand and cached per exact ROM in `work/cache/`.
- Every capture keeps its full route, so `tools/shoot.py --verify` can prove it reproduces.
- **RNG follows frame timing.** Different waits change encounters, drops and rolls. If a shot depends on luck,
  try `wN` variations before the deciding input and keep the one that works; it stays reproducible.

## Tokens (comma-separated; full list in `tools/emu.py`)
| Token | Effect | Use for |
|---|---|---|
| `a` `b` `start` `select` `up` `down` `left` `right` | press 8 frames, then wait 40 | menus, dialogue |
| `b+a` | press together | combos |
| `select>a` | hold the first 4 frames, then both | held-modifier shortcuts |
| `right:30` `a+right:60` | hold N frames, release, no wait | walking, running, charging, jump height |
| `a*5` `right:16*4` | repeat | repeated menu steps, walking tile by tile |
| `w60` | wait 60 frames (1 s) | fades, animations, enemy movement |
| `mash:a:600` | tap A every 8 frames for 600 frames | skipping text and intros |
| `settle` | run until two frames 10 apart are identical (max 300) | before a capture |
| `!` | last token: capture as is, no settle | auto-advancing messages, mid-animation |
| `poke:C0A2=09` | write RAM | shortcuts (recorded in the route) |
| `NAME` | macro from `game.json` "macros" | `TITLE`, `NEWGAME`, `MENU` |
| `@name` | first token: start from a checkpoint | everything after the boot |

Press timing is per game (`game.json` "press": hold/wait). Symptoms of wrong timing: a press does nothing (the
game polls slowly or ignores presses during a transition -> add `w30` before it or raise `hold`), two presses act
as one (edge-triggered input -> keep the release wait), a menu skips an entry (key repeat -> shorter hold).

## The working loop (play.py)
```sh
python3 tools/play.py start SLUG [--route @checkpoint]
python3 tools/play.py do "TITLE"                 # play; prints screenshot path + PC + RAM watches
python3 tools/play.py checkpoint title "Title screen, settled"
python3 tools/play.py do "start,w60,a"           # small steps: 1-10 tokens, then LOOK at the screenshot
python3 tools/play.py undo                       # one step back if it went wrong
python3 tools/play.py snap menu_main menu "Main menu: New game / Continue / Options"
python3 tools/play.py stop
```
1. **Look at every screenshot** (Read the PNG) before the next input. Never chain long blind sequences in an
   unknown game; once a sequence is known, put it in a macro or checkpoint.
2. **Checkpoint every milestone** (new area, before a boss, after a menu was reached). Cheap, and other agents
   reuse them.
3. **Snap as you go**: when the screen is worth having, `snap` it now; do not plan to come back.
4. Parallel work: `--name N` gives an independent session (one emulator each).
5. `do` settles after the tokens (the wait is recorded as `settle` in the route). Screens that never settle
   (animated backgrounds, blinking cursors, moving enemies) report "still changing": that is normal in action
   games; use `do!` and exact `wN` to pick the frame you want.

One-shot runs with a screenshot per token (good for finding timings): `python3 tools/emu.py SLUG --seq "@title,a,w10,a" --out work/x`
-> `work/x/NN_token.png`, `sheet.png`, `log.txt` (PC per token, the full route).

## RAM: find it once, write it down
Most shortcuts come from a few addresses: lives, health, money, level/stage, position, timer, inventory.
1. Look in the playbook and its sources first (Data Crystal RAM maps, TCRF, GameShark codes: a GameShark code
   `01VVAAAA` writes value VV to address AAAA (low byte first: `01 09 A2 C0` -> `poke:C0A2=09`)).
2. Otherwise search: `find reset`, change the value in game (lose a life), `find "new == old - 1"`, repeat with
   `find "new == old"` while nothing changes, until 1-3 candidates remain; confirm with `poke` and a screenshot.
   16-bit values: add `--wide`.
3. Record it in `game.json` "ram" (`"lives": {"addr": "C0A2", "size": 1}`: shown by every `do`) and the playbook
   RAM map.
- Pokes are part of the route. A poke may make capture possible (lives, money, stage select), but the shot must
  not show an impossible value (999 lives, 9999999 gold) unless the caption says so.

## Choosing the model (GB/GBC)
- `game.json` "model" comes from the header: CGB games -> `cgb`, everything else -> `dmg` (the original grey).
- Dual-mode games (CGB-enhanced) are shot in `cgb`; a `--model dmg` set may be added. Super Game Boy games:
  `--model sgb` captures 256x224 with the border and SGB colours (a separate set, e.g. `sgb`).
- Screenshots are the raw framebuffer (CGB colours 5->8 bit, no colour correction, no filter); `@3x` is nearest
  neighbour. Never resample by non-integer factors.

## Hangs and dead ends
- There is no generic hang detector. If several inputs change nothing: check `status` (PC moving?), wait 300
  frames, try Start/B. A PC stuck in one tight loop with no screen change across inputs is a hang: report the
  route, PC and bank.
- A softlock or a lost fight: `undo`, or `goto` the last checkpoint. Do not grind blindly: read the strategy
  notes, or poke.
- Battery saves live in the savestate (SRAM included). In-game save/load screens are worth a shot (`save`).

## Speed
`do` ~0.5-2 s; a cached checkpoint loads instantly; `shoot.py` replays ~1-5 s per shot. Long routes: make
checkpoints so replays start late.
