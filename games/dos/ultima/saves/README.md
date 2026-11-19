# Ultima I: The First Age of Darkness (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | ryz, level 1 human fighter (Str 30 Agi 28 Sta 17 Cha 13 Wis 10 Int 17), 150 hits, 200 food, 100 copper, leather armour, dagger; overworld east of the Castle of Lord British; saved with Q right after the start (slot 1, PLAYER1.U1) | `@start,q,w200,settle` | `6fd8a2aee4f9` | 2026-11-19 |
| 02_endgame | `02_endgame.sav` | ryz level 8 (by poke): 2489 hits, Str 47 Agi 52 Sta 38 Cha 29 Wis 33 Int 41, 8973 copper (89 gold crowns), 7340 exp, 1342 food, reflect suit, pistol and blaster readied, all four gems, 23 enemy vessels (space ace); overworld east of the Castle of Lord British. Next: rescue a princess for the time machine. | `@endgame,q,w200,settle` | `9e29395d20c3` | 2026-11-19 |
