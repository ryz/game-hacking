# Dungeon Magic: Sword of the Elements (NES, USA) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the game's own battery save: copy it next to your ROM as `<rom name>.sav` in any emulator, then Continue. `.state` = Mesen libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | Granville, new hero after one night at the inn: LV 0, HP 12, 98 gold, no equipment (start of the game) | `@start,set:0040=100:2,poke:008A=94,poke:008F=94,left,w30,a,w60,up,w300,settle,a,w150,w150,a,w150,w300,w300` | `779429de9171` | 2026-11-18 |
| 02_granville_fire_lv1 | `02_granville_fire_lv1.sav` | Granville inn after a night: Fire apprentice (Granville wizard), level 1, HP 15, 397 EXP, 212 gold; no items | `@start,poke:008A=6B,poke:008F=6B,right,w30,a,w60,up,w300,a,w300,settle,set:004B=412:2,poke:008A=6B,poke:008F=6B,left,w30,right,w30,a,w60,up,w300,a,w300,settle,set:0040=214:2,poke:008A=94,poke:008F=94,right,w30,right,w30,a,w60,up,w300,a,w300,settle` | `2b65cad032bb` | 2026-11-18 |
