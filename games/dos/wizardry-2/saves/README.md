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
| 03_wizardry3_transfer | `03_wizardry3_transfer.sav` | After the ending (capture route): RYZ L12 with the Mark of Gnilda (>G) and gear bought at Boltac's, CONDI EBO CUBI DEDDO MNZ Knights of the City (>K) with their gear, all in the Castle; SAVE2.DSK = this roster (the Wizardry III transfer source); SAVE1.DSK = the Wizardry I disk with the six LOST | `@final,e,w120,l,w600,settle` | `5f32dd603b3c` | 2026-11-19 |

## 03_wizardry3_transfer: the source for Wizardry III (capture 2026-11-19)
- Made from checkpoint `final` (`@final,e,w120,l,w600`, Leave game, then `play.py export`): the party is in
  the Castle, not in the maze ("out" 0 for all), gear on, levels as played.
- `WIZAR2/SAVE2.DSK` (this game's scenario disk) is the file Wizardry III needs: roster at `1D200`,
  slots 2-5 (RYZ CONDI EBO CUBI), 10-11 (DEDDO MNZ). RYZ L12 fighter ">G" (Mark of Gnilda, 484,587 E.P., 89 HP,
  long sword, plate mail, shield+1, helm bought after the ending), CONDI L11 ">K", EBO L13 ">K", CUBI L13
  ">K", DEDDO L13 ">K", MNZ L13 ">K", each with the Boltac's outfit of the capture (`GEAR`), gold 52,062-64,057.
  The six stock veterans (CALEB BOREE ODDLER NAUTUS ZIL GUYDOMAN) are unchanged, not knights.
- `WIZAR2/SAVE1.DSK` is the Wizardry I disk after the move: the six are there as LOST (status 7) with their
  Wizardry I items still in their records (5, 6, 5, 4, 3, 3); the stock Wizardry I characters TARKIN ...
  MEWO are level 1. Nothing in it is useful for Wizardry III's transfer (the legacy characters are the ones on
  SAVE2.DSK); keep it only as the Wizardry I history.
- List both rosters: `python3 games/dos/wizardry-2/tools/roster.py games/dos/wizardry-2/saves/03_wizardry3_transfer.sav`.
