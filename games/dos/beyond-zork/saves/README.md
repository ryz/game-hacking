# Beyond Zork: The Coconut of Quendor (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | Hilltop at the start, preset character Frank Booth, saved with SAVE (default name DATA\BEYONDZO.SAV) | `pow,BOOT,settle,type:begin\n,w300,space,w200,space,w300,settle,space,w300,settle,enter,w300,space,w300,settle,type:look\n,w200,settle,type:name me ryz\n,w200,settle,type:save\n,w200,settle,enter,w300,settle` | `dab9b7aa969a` | 2026-11-21 |
