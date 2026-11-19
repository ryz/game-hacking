# Wizardry III: Legacy of Llylgamyn (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 00_transfer | `00_transfer.sav` | Not a save made by the game: the transfer input. Only `WIZAR3/SAVE2.DSK` = the Wizardry II scenario disk from `games/dos/wizardry-2/saves/03_wizardry3_transfer.sav` (ryz condi ebo cubi deddo mnz after the Wizardry II ending: RYZ L12 Mark of Gnilda, the others Knights of the City, with gear, in the Castle), byte for byte; what run.bat's menu 2 would copy. Rebuilt by `python3 games/dos/wizardry-3/tools/transfer.py` (identical bytes) | - (script) | `0893b0790a0f` | 2026-11-19 |
| 01_start | `01_start.sav` | Roster after the transfer and the legacy, then Leave game: KLINDT LEIF ZETT VERPA SENA GITTER (stock, level 1) plus RYZ CONDI EBO CUBI DEDDO MNZ moved from Wizardry II 03_wizardry3_transfer and legated (level 1, 500 gold, honors kept + D; RYZ and CUBI neutral, the others good); party not formed (RESUME adds them); WIZAR3/SAVE2.DSK = the Wizardry II disk with the six marked LOST | `@edge,l,w600,settle` | `bcdaadd4b4be` | 2026-11-19 |
| 02_ending | `02_ending.sav` | Roster after the ending (scout route, veterans by VET poke, Neutral Crystal poked): RYZ CONDI EBO CUBI DEDDO MNZ as veterans (levels 11-13, no gear; their awards unchanged: the party itself gets no star on disk); CUBI carries an empty item where the orb was (surrendered); the Star of Llylgamyn ("*", +150,000 E.P.) on KLINDT LEIF ZETT VERPA SENA GITTER; party not formed (RESUME adds them) | `@after_ending,e,w120,l,w600,settle` | `1b7915e4c6be` | 2026-11-19 |

## The transfer (Wizardry II -> III) and the legacy
- `00_transfer` is derived from a capture save (owner's exception 2026-11-12/15: saves made here). With
  `sav:00_transfer` the game finds `SAVE2.DSK` next to `WIZ3.COM`; Utilities M)ove characters, 2) Knight of
  Diamonds reads it (the 1998 loader opens `Save2.Dsk` on the "source disk" prompt: the only source file it knows,
  so a Wizardry I disk would have to be copied under that name). `SAVE1.DSK` is not needed.
- `01_start` and `02_ending` carry both disks: `SAVE3.DSK` (this game's roster, offset `1DE00`) and `SAVE2.DSK`
  (the Wizardry II disk, the six marked LOST by the move).
- For the owner: copy `SAVE2.DSK` from a Wizardry II game folder into the Wizardry III folder (what run.bat's
  menu 2 does), or unzip `01_start.sav` / `02_ending.sav` over the game folder.
- List the rosters: `python3 games/dos/wizardry-3/tools/roster.py games/dos/wizardry-3/saves/01_start.sav`.
