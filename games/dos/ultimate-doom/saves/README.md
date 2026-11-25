# The Ultimate Doom (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | E1M2 Nuclear Plant start after E1M1 Hangar (kills 100%, items 5%, secret 33%): pistol, 61 bullets, 28 shells, health 19%, armor 163% (MegaArmor); slot 1 'ryz' = DOOMSAV0.DSG | `NEWGAME,E1DOOR,E1FIGHT1,E1ZOMBIE,E1ZIGZAG,E1ARMOR,E1EXIT,E1TALLY,SAVE1:ryz` | `8a681c0735e5` | 2026-11-25 |
