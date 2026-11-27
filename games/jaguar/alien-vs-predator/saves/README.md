# Alien vs Predator - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the cartridge EEPROM (128 bytes, 64 big-endian words): rename it to the game's `.srm` for RetroArch's Virtual Jaguar core. `.state` = Virtual Jaguar libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | Marine (Pvt. Lewis) in GAME 1 at the start: brig, sublevel 3, no weapon, security 0, score 0 | `pow,TITLE,settle,a,w120,settle,a,w240,settle,left,w60,a,w1000,a,w300,settle,pause,w30,option,w30,down,w20,b,w120,settle` | `f37045414b79` | 2026-11-27 |
