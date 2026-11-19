# Wizardry II: The Knight of Diamonds (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 00_transfer | `00_transfer.sav` | Not a save made by the game: the transfer input. Only `WIZAR2/SAVE1.DSK` = the Wizardry I scenario disk from `games/dos/wizardry/saves/03_werdna_beaten.sav` (ryz condi ebo cubi deddo mnz after the real Werdna fight, levels 11-13, chevron, in the Castle), byte for byte; what run.bat's menu 2 would copy. Rebuilt by `python3 games/dos/wizardry-2/tools/transfer.py` (identical bytes) | - (script) | `ec4c3886a78e` | 2026-11-19 |
| 01_start | `01_start.sav` | Roster after the import and Leave game: CALEB BOREE ODDLER NAUTUS ZIL GUYDOMAN (stock, levels 12-13) plus ryz condi ebo cubi deddo mnz moved from Wizardry I 03_werdna_beaten (levels 11-13, Chevron of Rank, 55,077-74,817 gold, no items); party not formed (RESUME adds them); WIZAR2/SAVE1.DSK holds the Wizardry I disk with the six marked lost | `@start,e,w120,l,w600,settle` | `3f97a927888b` | 2026-11-19 |
| 02_ending | `02_ending.sav` | Roster after the ending (scout run): RYZ with the Mark of Gnilda (>G, chevron kept, E.P. 484,587), CONDI EBO CUBI DEDDO MNZ Knights of the City (>K), levels 11-13, no items, 55,077-74,817 gold; the stock six unchanged; party not formed (RESUME adds them) | `@knights,e,w120,l,w600,settle` | `6aadfb7bdcc5` | 2026-11-19 |

## The transfer (Wizardry I -> II) and notes for Wizardry III
- `00_transfer` is derived from a capture save (owner's exception 2026-11-12/15: saves made here). With
  `sav:00_transfer` the game finds `SAVE1.DSK` next to `WIZ2.COM`; Utilities M)ove characters reads it (the
  1998 loader opens it on the "source disk" prompt). `01_start` and `02_ending` carry both disks: `SAVE2.DSK`
  (this game's roster) and `SAVE1.DSK` (the Wizardry I disk, the six marked lost by the move).
- For the owner: copy `SAVE1.DSK` from a Wizardry I game folder into the Wizardry II folder (what run.bat's
  menu 2 does), or unzip `01_start.sav` / `02_ending.sav` over the game folder.
- Wizardry III imports from SAVE1.DSK and SAVE2.DSK: this game's roster is in `SAVE2.DSK` at offset `1D200`
  (20 slots of 208 bytes, four per 1024-byte page; the six in slots 2-5, 10, 11). List with
  `python3 games/dos/wizardry-2/tools/roster.py games/dos/wizardry-2/saves/02_ending.sav`.
