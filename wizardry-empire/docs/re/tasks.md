# Cooperative tasks and their stacks

Found by the triage agent while diagnosing the battle hang (2026-11-11), confirmed in `0:06EF`.

- The game runs a small cooperative scheduler. Yield = `call 0:07C5`; resume = `0:07C0` (pop hl/de/bc/af, ret).
- Task table: `$C012 + 4n` (flags/SVBK, ROM bank, SP lo, SP hi); bit 7 of the first byte = alive (e.g. `$C022` = task 4).
- Create: `0:06EF` (A = task n, B = ROM bank, DE = entry): stack area `$CE00 + $40n`, initial SP `$CE36 + $40n`,
  entry address stored at `$CE3E/F + $40n`. `0:0741` is a variant; `0:0717` kills a task.
- So **WRAM0 `$CE00-$CFFF` holds the task stacks** (tasks 0-7). Task 2 = typewriter (`22:4434` creates it with
  entry `0:20DA`), task 4 = battle hit effect (bank `$2F`, started from `32:45E5`, `24:76C8`, `22:6C42`),
  tasks 5 and 7 are used too. The main stack starts at `$CE00` and grows down.
- Consequence for the patch: no variables in `$CE00-$CFFF`. The VWF moved to WRAM bank 7 (`docs/re/vwf.md`).
- Other WRAM0 that looks empty in savestates is not free either: `$C23E-$C2BF` and `$C2EE-$C3C1` hold object
  tables (12- and 32-byte records), `$C640-$C6FF`, `$C7C5-$C857`, `$CAFF-$CB80` are written by `rst $08`
  copies during battle. Always confirm with write watches over the tour routes and a battle.
