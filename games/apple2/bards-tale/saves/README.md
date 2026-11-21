# The Bard's Tale: Tales of the Unknown - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = a ZIP of the disk images the game has written to (whole images, same names as in the game's ZIP): unzip it and use those images in place of the originals in any Apple II emulator. `.state` = AppleWin libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `rom/saves/apple2/bards-tale/01_start.sav` (not committed) | Character disk with six new level-1 characters RYZ CONDI EBO CUBI DEDDO MNZ and the saved party *RYZ PARTY (Guild, Disk options, Save party), on top of the archive's played roster | `GUILD,MAKE6,ADD6,w30,d,w300,s,w400,settle,type:RYZ PARTY\n,w1500,settle,e,w300,c,w1500,settle,space,w300,settle` | `992d679ee105` | 2026-11-21 |
