# Phantasy Star - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the game's own battery save: copy it next to your ROM as `<rom name>.sav` in any emulator, then Continue. `.state` = Genesis Plus GX libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | New game at first control in Camineet, saved in slot 1 (Alis Lv 1, 0 meseta, no items); made in one route from power-on (see playbook: SMS savestates do not carry cartridge RAM) | `pow,TITLE,NEWGAME,b1,w120,down*4,b2,w90,b2,w90,b2,w90,b2,w90,w30,settle` | `c904b97cdc82` | 2026-11-19 |
