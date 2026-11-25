# Wolfenstein 3D (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | E1M1 Bring 'em on: three guards killed, first secret (pushwall to the machine-gun room), machine gun, ammo 26, health 100, score 300; slot 1 'E1M1 machine gun' (SAVEGAM0.WL6) | `pow,NEWGAME,E1HALL,E1GUARD,E1NORTH,E1GUARD2,E1GUARD3,E1PUSH,E1SECRET,SAVE1:E1M1 machine gun` | `261f4eeb1cbb` | 2026-11-25 |
