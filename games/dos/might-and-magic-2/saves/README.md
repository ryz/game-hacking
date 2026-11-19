# Might and Magic II: Gates to Another World (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic II: `ROSTER.DAT`, 8,293 bytes once the game has written it; the stock file is 8,292), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save); `sav:NAME,RESUME` = the party of that save in its town (the game marks the last party in the inn list).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | Roster after signing in at the Middlegate inn on day 1: ryz (new Human Knight) and the renamed premade characters condi, ebo, cubi, deddo, mnz in the party, Sir Felgar at the inn; nothing bought | `@signed_in` | `7b4ceb7841e7` | 2026-11-19 |
