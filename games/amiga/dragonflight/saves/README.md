# Dragonflight - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = a ZIP of the disk images the game has written to (whole images, same names as in the game's ZIP): unzip it and use those images in place of the originals in any Amiga emulator. `.state` = PUAE libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `rom/saves/amiga/dragonflight/01_start.sav` (not committed) | New game, party of four (Bladus, Rinakles, Dobranur, Andariel) on the overworld just outside Pegana, saved via the disk icon on Disk B | `pow,w300,mouse1:10,w2400,mouse1:10,w3500,n,w1200,mouse1:10,w100,mouse1:10,w100,mouse1:10,w100,mouse1:10,w100,settle,disk:2,w100,w2800,settle,poke:3bf4=00050005,poke:118b2=00050005,kp6,w60,mouse1,w1200,settle,poke:3bca=012700b7,w4,mouse1,w100,poke:3bca=0127008f,w4,mouse1,w100,settle,mouse1,w600,settle,mouse1:10,w300,settle,mouse2:10,w100,poke:3bca=012700b7,w4,mouse1,w100,settle` | `ae07f47d0aa1` | 2026-11-22 |
| 02_armed | `rom/saves/amiga/dragonflight/02_armed.sav` (not committed) | Party on the land outside Pegana, armed (Bladus sword, Rinakles dagger, Dobranur battleaxe, Andariel bow), Rinakles carries a scroll of Magic arrow; ready for land fights | `TITLE,w900,n,w1200,mouse1:10,w100,mouse1:10,w100,mouse1:10,w100,mouse1:10,w100,disk:2,w100,w2800,LEAVE,ARM,poke:2EFC=00500201,SAVEGAME,settle` | `21a55e39eb03` | 2026-11-22 |
