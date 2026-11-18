# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_signed_in | `01_signed_in.sav` | stock party signed in at the inn of Sorpigal; Crag's club is in his backpack | `@after_save` | `99884aa59c67` | 2026-11-18 |
| 02_ryz_party | `02_ryz_party.sav` | new roster, signed in at the inn of Sorpigal: RYZ (Knight created here, slot G) and the five other stock characters renamed CONDI, EBO, CUBI, DEDDO, MNZ; Crag the Hack untouched; nothing bought yet | `pow,PARTY,left,w60,left,w150,y,w250,esc,w150` | `df1be819de99` | 2026-11-18 |
