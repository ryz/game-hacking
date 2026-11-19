# Wizardry II: The Knight of Diamonds (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | Roster after the import and Leave game: CALEB BOREE ODDLER NAUTUS ZIL GUYDOMAN (stock, levels 12-13) plus ryz condi ebo cubi deddo mnz moved from Wizardry I 03_werdna_beaten (levels 11-13, Chevron of Rank, 55,077-74,817 gold, no items); party not formed (RESUME adds them); WIZAR2/SAVE1.DSK holds the Wizardry I disk with the six marked lost | `@start,e,w120,l,w600,settle` | `3f97a927888b` | 2026-11-19 |
