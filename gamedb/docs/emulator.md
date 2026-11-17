# Emulator use - the general rules

How agents drive games here, for any game. Game-specific facts (controls, routes, RAM) go into
`games/<slug>/playbook.md`, never into this file. Paths are relative to `gamedb/`.

## Setup (once per container)
```sh
sh tools/setup_emu.sh                         # GB/GBC: gbemu-cli (headless SameBoy); NES/Famicom: Mesen core (~2 min)
python3 tools/intake.py /path/to/game.gbc     # registers the ROM -> games/<slug>/, rom/<slug>.gbc (or .gb, .nes)
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
| `rec:240:2` | last token of a shot: record 240 frames as a GIF clip (every 2nd kept); elsewhere a wait | clips (`play.py record`) |
| `poke:C0A2=09` | write RAM bytes once | shortcuts (recorded in the route) |
| `set:C0B0=8973:2` | write a decimal value (N bytes; `:bcd`, `:be`) | money, score, EXP |
| `gs:0109A2C0` | GameShark code, held for the rest of the route (GB/GBC only; NES: `freeze:`) | infinite health/lives, codes from the web |
| `freeze:C0A2=09` / `unfreeze` | hold a raw value / drop all held values | same, own addresses |
| `rom:NAME` | route prefix: patched ROM (Game Genie, IPS, bytes) | level select, debug menu, invincibility |
| `sav:NAME` | route prefix: power on with a battery save | late-game saves from the web |
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
4. After `goto` or `undo` the screen still shows an old frame: `snap` refuses until a `do` has run (`do settle`).
   `game.json` edits (macros, watches) are picked up by the next `do`, no restart needed.
   `undo` is one level deep: before a risky sequence make a `checkpoint` (or `do` it in smaller steps).
5. Parallel work: `--name N` gives an independent session (one emulator each).
6. **Never mash into a prompt.** `mash:a:N` happily types A's into a name-entry keyboard or picks a menu entry.
   Mash in short blocks (`mash:a:150,settle`) and look at the screenshot before a naming or Yes/No prompt.
7. **Settle stops on blank frames.** A fully white or black frame (mid-fade) counts as stable. After transitions
   (title START, doors, cutscene cuts) add `w60` before `settle`. Do not change `settle` itself: routes depend
   on its exact behaviour.
8. `do` settles after the tokens (the wait is recorded as `settle` in the route). Screens that never settle
   (animated backgrounds, blinking cursors, moving enemies) report "still changing": that is normal in action
   games; use `do!` and exact `wN` to pick the frame you want.

Pick animation frames (`do!` + `wN`) in `play.py`, not with `emu.py` montages: `shoot.py` reproduces play.py's
timing, and a frame found with emu.py may not appear at the same `wN` there (seen with the Safari rock).

One-shot runs with a screenshot per token (good for finding timings): `python3 tools/emu.py SLUG --seq "@title,a,w10,a" --out work/x`
-> `work/x/NN_token.png`, `sheet.png`, `log.txt` (PC per token, the full route).

## Cataloguing, not playing fair (owner's rule, 2026-11-15)
The goal is a complete, good-looking catalogue, not an honest playthrough. Skip, cheat, hack RAM and patch the
ROM whenever it is faster than playing. Prefer, in this order, whatever reaches the target soonest:
1. **What others already made:** completed saves (GameFAQs "Saves" section on many game pages), password lists,
   GameShark/Game Genie code lists (GameFAQs "Cheats", gamehacking.org), debug menus and level selects (TCRF).
   Downloaded saves go to `rom/saves/<slug>/NAME.sav` (gitignored: `rom/`), loaded with the `sav:NAME` route
   prefix; record URL, SHA-1 and what the save contains in the playbook Shortcuts table so it can be fetched again.
   A save made for another revision or emulator may not load: check the in-game file screen.
2. **Codes:** `gs:` tokens (held like the device), Game Genie codes in a `rom:` variant (game.json
   `"rom_variants": {"gg": {"gg": ["ABC-DEF-GHI"]}}`), IPS hacks (e.g. a debug-menu patch) the same way
   (`"ips": ["rom/patches/x.ips"]`; patches are not committed either).
3. **RAM:** stage/level number, position, items, flags (see below).
4. **Playing** only for what cannot be reached otherwise, or where the play itself is the shot.

**Realistic values.** Whatever is set by cheating must look like a plausible save, not like a cheat: below the cap
and not round, varied between stats and characters, consistent with the progress shown. Money capped at 9999 ->
`8973`, not `9999`; lives 3-7, not 99; a level-30 party has HP in the level-30 range, each member different;
one or two items short of a full inventory. Pick the numbers yourself, write them as `set:`/`poke:` tokens (so
they stay reproducible) and vary them between games. Infinite health/lives via `gs:` is fine because it does not
show; a frozen value that does show on screen also follows this rule.

**Names.** If the game lets you name the main character, the name is **ryz** (owner's rule). Further party
members, if the game asks for names too: condi, ebo, cubi, deddo, mnz (the owner's standard party, in that
order). Pets, rivals, towns, files: keep the game's default or suggested name.

## Saves for the owner (owner's rule, 2026-11-15)
The owner wants to jump into a game at any milestone and take screenshots by hand, so agents leave saves behind:
1. At every milestone (after naming, each town/badge/world, before the final boss, the end) **save in the game**
   (its own Save menu, or the save point) and check the "saved" message.
2. `python3 tools/play.py export NAME "what it contains"` writes the battery save to
   `games/<slug>/saves/NAME.sav` and adds a row (contents, route, SHA-1, date) to `saves/README.md`. Add
   `--state` for an emulator savestate of that exact moment (SameBoy for GB/GBC, Mesen core for NES; useful where the game saves only at fixed points).
3. Names say where you are: `01_start`, `02_pewter_badge1`, `08_before_elite_four` (sortable).
The `.sav` loads in any emulator (copy it next to the ROM as `<rom name>.sav`) and in routes as `sav:NAME`.
Values in an exported save follow the realistic-values rule: it is what the owner will see. Only saves made here
are committed; downloaded ones stay in `rom/saves/`.

## RAM: find it once, write it down
Most shortcuts come from a few addresses: lives, health, money, level/stage, position, timer, inventory.
1. Look in the playbook and its sources first (Data Crystal RAM maps, TCRF, GameShark codes: a GameShark code
   `01VVAAAA` writes value VV to address AAAA (low byte first: `01 09 A2 C0` -> `poke:C0A2=09`)).
2. Otherwise search: `find reset`, change the value in game (lose a life), `find "new == old - 1"`, repeat with
   `find "new == old"` while nothing changes, until 1-3 candidates remain; confirm with `poke` and a screenshot.
   16-bit values: add `--wide`.
3. Record it in `game.json` "ram" (`"lives": {"addr": "C0A2", "size": 1}`: shown by every `do`; `"fmt": "bcd"`
   for packed-BCD values such as money, `"be"` for big-endian) and the playbook RAM map.
- A position poke does not redraw the map: the old background stays until the screen scrolls. For a clean warp
  poke during a map transition (door, stairs, town entry), or leave and re-enter the map before the shot.
- Pokes are part of the route and fine anywhere; values that show on screen follow the realistic-values rule.

## Choosing the model (GB/GBC; NES: see NES / Famicom)
- `game.json` "model" comes from the header: CGB games -> `cgb`, everything else -> `dmg` (the original grey).
- Dual-mode games (CGB-enhanced) are shot in `cgb`; a `--model dmg` set may be added. Super Game Boy games:
  `--model sgb` captures 256x224 with the border and SGB colours (a separate set, e.g. `sgb`).
- Screenshots are the raw framebuffer (CGB colours 5->8 bit, no colour correction, no filter); `@3x` is nearest
  neighbour. Never resample by non-integer factors.

## NES / Famicom
- Backend: Mesen as a libretro core, run inside the Python process (`tools/lrcore.py`); one process = one game,
  parallel sessions work as on GB (`--name`). Cartridge games as `.nes` files with an iNES or NES 2.0 header
  (Famicom carts included). Famicom Disk System images are not set up (they need the disk BIOS).
- Screenshots are 256x240, the full frame without overscan crop, Mesen's default palette (the NES has no RGB
  output, so every palette is a choice; this one is fixed for all sets). Many games leave garbage in the top and
  bottom 8 lines and the left column: that is what the console outputs, do not crop.
- `game.json` "model": `ntsc` (NES and Famicom, 60 Hz; default), `pal` (50 Hz) or `dendy`, taken from the header.
  iNES headers often lack the region: a European ROM that runs too fast or glitches needs `--model pal`.
- Buttons: `a b start select up down left right` (player 1). No second controller, microphone or Zapper yet.
- Memory is the CPU address space: `0000-07FF` RAM (mirrored to 1FFF), `6000-7FFF` cartridge RAM (battery
  save or work RAM, when the cartridge has it), `8000-FFFF` the PRG banks mapped at that moment. `peek` has no
  side effects; `poke` reaches RAM and mapped PRG, not the PPU/APU/mapper registers. `find` searches
  `0000-07FF` and `6000-7FFF`. `status` shows the PC (no bank number: it depends on the mapper).
- Cheats: no GameShark on the NES, so `gs:` is refused; hold RAM values with `freeze:ADDR=HEX` (Pro Action
  Replay style RAM codes `AAAA:VV` are exactly that). Game Genie in a `rom:` variant: 8-letter codes always;
  6-letter codes only for games without bank switching (PRG <= 32 KiB), otherwise the bank is unknown: find
  the 8-letter form or patch the file offset with `"bytes"`.
- Exported `.sav` files are the raw battery RAM (8 KiB on most cartridges), the format every NES emulator uses.
- A screenshot never advances emulation. Savestates are the core's own state plus a trailer holding the frame on
  screen, so a cached checkpoint and a freshly built one give the same picture and the same timing (they
  differed by one frame before 2026-11-17: rebuild any cache older than that).
- Many NES games sit in one frame-wait loop, so `status` shows the same PC all the time; that is not a hang.
- Password games (no battery): make a "save" by poking the state you want and asking the game for its
  password; put the password and the tokens that type it into a macro (see `games/dragon-quest/tools/pw.py`).
- Power-on RAM is all zeros (fixed, so routes reproduce). A few games seed their RNG from uninitialised RAM and
  behave the same on every boot here; that is intended.

## Hangs and dead ends
- There is no generic hang detector. If several inputs change nothing: check `status` (PC moving?), wait 300
  frames, try Start/B. A PC stuck in one tight loop with no screen change across inputs is a hang: report the
  route, PC and bank.
- A softlock or a lost fight: `undo`, or `goto` the last checkpoint. Never grind: poke, use a code or a save.
- Battery saves live in the savestate (SRAM included). In-game save/load screens are worth a shot (`save`).

## Speed
`do` ~0.5-2 s; a cached checkpoint loads instantly; `shoot.py` replays ~1-5 s per shot. Long routes: make
checkpoints so replays start late.

## Web research from the container
- Use WebSearch/WebFetch. The environment allows: gamefaqs.gamespot.com, tcrf.net, datacrystal.tcrf.net,
  strategywiki.org, en.wikipedia.org, gamehacking.org, doc.kodewerx.org, archive.org (owner approved 2026-11-15).
  Another host: ask the coordinator; it cannot be added from inside an agent.
- A site that refuses automated access (403, captcha) is skipped and noted as unavailable in the playbook
  Sources; never work around bot protection.
- Binary downloads (saves, patches) with `curl -L -o rom/saves/<slug>/NAME.sav URL` where the site serves the file
  directly; otherwise note the URL for the owner to fetch.
