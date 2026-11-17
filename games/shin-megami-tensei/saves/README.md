# Shin Megami Tensei (Super Famicom, English translation patch) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the game's own battery save: copy it next to your ROM as `<rom name>.sav` in any emulator, then Continue. `.state` = Mesen-S libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav`, `01_start.state` | Hero's room right after the dream: ryz (STR 11 VIT 10 SPD 9 LUK 8), Law hero condi and Chaos hero ebo named (not in the party yet), level 1, no money yet (mother gives 10000 yen on leaving the room). File 1. | `@start,down:4,w30,a,w90,settle,a,w90,settle,a,w150,settle,a,w90,settle,a,w90,settle` | `7d37778d44a5` | 2026-11-17 |
| 02_kichijoji_arcade | `02_kichijoji_arcade.state` (state only) | Kichijoji arcade, square 5,2 facing south, after the cafe errand: ryz level 1, HP 22/22, Attack Knife bought and equipped, 5000 yen. No in-game save exists for this point: the route never saves (saving was only seen in the hero's room, which was not re-entered), so the battery file exported with it was empty (8192 zero bytes) and was deleted. Load the `.state` in the Mesen-S core, or replay the route. | `@coffee,w10,settle` | none (no .sav) | 2026-11-17 |
