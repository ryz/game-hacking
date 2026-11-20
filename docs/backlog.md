# Tool backlog - shared tooling

One list of tool work that agents asked for or that the coordinator planned, so a wish is written once instead
of in every feedback entry. Rule (2026-11-20): a wish asked for by a **second** run is built before the next
dispatch of that skill, or dropped here with the reason; agents do not write a private copy of a tool that is
on this list, they report the need. "Asked" counts runs; sources are in `skills/<name>/feedback-log.md`.

## Open
| Wish | Asked | Notes |
|---|---|---|
| Shared module for series on one engine (Wizardry I-III on DOS and Apple II: `maps.py`, `roster.py`, `transfer.py`; survey / event scan / text scan for first-person RPGs: `scan.py`, `survey.py`, `eventscan`, `mapgrab`, `textscan`, `explore`) | 6 | 12 `maps.py`, 4 `roster.py`, 4 `transfer.py` live per game and differ by 30-60 lines. Needs the dumps to test against; do it at the next Wizardry or Might and Magic run |
| `play.py checkpoint`: scratch checkpoints kept out of `checkpoints.txt` (`--scratch`), a replaced line stays in place instead of moving to the end | 3 | Megami Tensei scout, Wizardry II DOS scout, Might and Magic II scout |
| Deeper `undo` (more than one level) | 3 | Pokémon Blue, Megami Tensei, Ultima III; a `checkpoint` before a risky step is the workaround |
| Z80 disassembler like `dis6502.py` | 1 | Phantasy Star part 2 |
| `sample` leaves the screen stale so `record` refuses; `record` taking leading tokens | 1 | Phantasy Star early game |
| `lenses.py SLUG SET --work` (check the working set, not the published one) | 1 | Might and Magic 1 DOS fix-up |
| `"fmt": "bcd-le"` RAM watch (`set:...:bcd` already writes it) | 1 | Ultima III scout |
| `intake.py` records a DOS ZIP's `dosbox*.conf` autoexec lines and cycles in `game.json` | 1 | Might and Magic II scout |
| `cachecheck.py --show-diff NAME`: the first differing addresses between flat and cached state | 1 | Sword of Vermilion scout (a stack word, found by hand) |
| `preview.py --repeat TOKENS N`: a sheet of the route after 1..N repetitions | 1 | Sword of Vermilion scout (one more step per line) |
| `play.py find` warns when nothing ran since the last narrowing (0 candidates without a hint); `preview.py --timeline` per route, not per call | 1 | Sword of Vermilion capture run 3 |
| `dis6502.py` for Apple II: disassemble live memory (a `play.py dump` or main/aux `2xxxx` addresses), not only ROM banks | 1 | Might and Magic II Apple II scout (py65 + scratch script) |
| `play.py dump` JSON: zero-padded hex keys or a note in the output that keys are hex | 1 | Might and Magic II Apple II scout (read as decimal, several calls lost) |
| `shoot.py --verify`/`--publish-only` take captions and categories from the work `shots.txt` when they differ from `index.json` (or warn); `preview.py --set` flags identical frames within an unshot plan | 1 | Wizardry II Apple II capture (second `recaption` pass; stairs-down = dark warp found only at shoot) |
| `dis68k.py`: hint when an address points inside an instruction or string (pointer searches off by a few bytes) | 1 | Sword of Vermilion capture run 3 |
| `set:ADDR=N:bcd` follows the platform's byte order (big-endian on md; today little-endian unless told) | 1 | Sword of Vermilion capture run 4 |
| `snap` warns when the route has `freeze:` before one long `wN` (freezes are applied between tokens) | 3 | the guide says `w10*N`; a warning would catch it |
| Contact sheet labels when frame sizes are mixed (SNES hi-res rows) | 1 | Shin Megami Tensei run 1 |
| Macros used by published shots change those routes when edited: store expanded routes in `index.json`, or refuse the edit | 2 | today a rule in the emulator guide (new macro name) |
| `--model sgb` hangs on the SGB transfer screen (gbemu-cli handshake) | 1 | Pokémon Blue; capture in `dmg` |
| `play.py undo`: a route recorded after `undo` replayed differently | 1 | Wizardry II NES; needs a reproduction |
| DOSBox Pure prints its log to stderr (about 16 lines per shot: 3,600 for a 228-shot verify); silence it in the core patch or the driver | 1 | seen 2026-11-20; until then run `shoot.py ... 2>/dev/null` or filter for `reproduce\|MISMATCH\|check:` |
| DOS: mouse tokens, CD images, installers, sound card choice | - | untested; expect work with the first game that needs each |
| Wizardry Empire: `floormap --list` per-door gating, connected parts, warp landings; `play.py --dir`; JP variant of `party.py`; emu.py `hold:keys:N`; census segment mode and attributes; `gbdis --rom`; `explore.py` change | 1 each | from the tracer, triage, design-writer and playtester logs (its own tools in `translation/tools/`) |

## Done
| Wish | Asked | Done |
|---|---|---|
| Shared previewer (parallel runs, shoot.py's settle, plan-file input, frames from a marker, paged timelines, text screens, checkpoint-only lines) | 6 | 2026-11-20 `tools/preview.py` |
| Duplicate check per batch and at snap | 4 | 2026-11-20 `shoot.py --only`, `play.py snap`, `preview.py --set` |
| Shared cold check of the checkpoint cache with a contact sheet | 4 | 2026-11-20 `tools/cachecheck.py` |
| Full verify too slow (15-35 minutes: every checkpoint from power-on, one process) | 6 | 2026-11-20 chained checkpoint builds, `shoot.py --jobs` |
| `play.py text` for the Apple II text screen, a 1x look | 3 | 2026-11-20 `Apple2.text()`, native pictures by default |
| `goto` after a macro edit used the old state | 3 | 2026-11-20 `goto` reloads `game.json`; the cache key follows the macro |
| "Shot = route + N more steps" (`snapafter`), typewriter and auto-advancing text | 4 | 2026-11-20 `preview.py --timeline` prints the exact route of every frame |
| Reordering a set (`--reorder`), `recaption` not reaching the game's `shots.txt`, `--publish-only` ordering by the game's list | 4 | 2026-11-20 the set's own `shots.txt` is the order and the record |
| Session clock for budgets | 3 | 2026-11-20 budgets in tool calls, `call=N` in the status line |
| Scout cannot run `shoot.py` | 3 | 2026-11-20 scouts write under `work/` and preview with `preview.py` |
| `play.py diff`: more than 80 rows, an address range (Apple II screen memory, Mega Drive tile maps) | 2 | 2026-11-20 `diff A [B] --range LO-HI --max N` |
| `preview.py --out` with a path doubled it; `--peek ADDR:0x10` refused | 1 | 2026-11-20 fixed (base name taken, hex lengths) |
| `tools/dis68k.py`: 68000 disassembler (boss and ending triggers on the Mega Drive) | 1 | 2026-11-20 built on capstone (owner: install it), with `--xref` |
| Earlier, by date | - | `unsnap`/`recaption` (2026-11-17), hex and BCD watches, `dis6502.py`, `dump`/`diff`, macros with arguments, sheets in pages, `--prune`, stale PNGs removed at publish (2026-11-18), `do` rollback, `export` route from power-on (2026-11-19) |
