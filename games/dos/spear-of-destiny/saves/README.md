# Spear of Destiny - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | Floor 1 (Tunnels 1), Bring 'em on!: slot 1 'Floor 1 treasure' in the treasure room after three guards, the ammo secret and 8 treasures (score 2700, health 16, ammo 48) | `pow,NEWGAME,F1AMMO,F1DOOR,F1GUARD1,F1GUARD2,F1GUARD3,F1TDOOR,F1TREASURE,SAVE1:Floor 1 treasure` | `3d89b5e5ffe4` | 2026-11-25 |
