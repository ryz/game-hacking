# Ultima III: Exodus (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Ultima III: `ROSTER.ULT`, `PARTY.ULT`, `SOSARIA.ULT` in the folder `ULTI-III/`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | New party of four (ryz Human Paladin, condi Elf Wizard, ebo Dwarf Fighter, cubi Bobbit Cleric; roster 1-4, 150 H.P., 150 food and gold each) on the Sosaria map at (2C,14) beside Lord British's castle, saved with Quit & Save | `pow,MENU,settle,PARTY,settle,JOURNEY,settle,q,w600,settle` | `ef4ede77f813` | 2026-11-19 |
