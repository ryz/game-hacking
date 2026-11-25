# Doom (DOS, registered 1.1) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | E1M2 Nuclear Plant start after an honest E1M1 (kills 6/6, blue armor 190%, health 100%), slot 1 'ryz' (DOOMSAV0.DSG) | `NEWGAME,BIGVIEW,E1DOOR,E1FIGHT1,E1ZIGZAG,E1ARMOR,E1EXIT,E1TALLY,SAVE1:ryz,w60,settle` | `68c723f20a01` | 2026-11-25 |

Doom 1.1 writes its saves to `C:\DOOMDATA\DOOMSAVn.DSG` (a folder at the drive root, created at every start), not to the game folder: unzip `01_start.sav` at the root of the drive DOOM is on. Loaded back with `sav:01_start,TITLE,esc,w20,down*2,w10,enter,w30,enter,w100` (E1M2, health 100, armor 190: verified 2026-11-25).
