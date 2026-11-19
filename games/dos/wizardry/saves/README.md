# Wizardry: Proving Grounds of the Mad Overlord (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | Roster after Leave Game: the six pre-made characters plus ryz (fighter), condi (fighter), ebo (priest), cubi (thief), deddo (mage), mnz (bishop), level 1, about 180 gold each, no equipment; party not formed (RESUME adds them) | `@start,e,w120,l,w600,settle` | `155612d15e3e` | 2026-11-19 |
| 02_ending | `02_ending.sav` | Roster after the ending (veterans from VET, amulet by AMULET, scout run): ryz condi ebo cubi deddo mnz level 13 with the Chevron of Rank (>), 50,000 more G.P. and E.P., no equipment; party not formed (RESUME adds them). Superseded as the transfer source by 03_werdna_beaten (kept: routes use it) | `@after_ending,e,w120,l,w600,settle` | `d9d241a73281` | 2026-11-19 |
| 03_werdna_beaten | `03_werdna_beaten.sav` | Roster after beating Werdna in a real fight and the ending: ryz (L11, drained, cured of paralysis at the temple), condi (L11), ebo cubi deddo mnz (L13), all with the Chevron of Rank, equipped (long swords, plate/breast plate, shields, helms), 58,000-75,000 gold each; party not formed (RESUME adds them). Transfer source for Wizardry II | `@final,e,w120,l,w600,settle` | `5fb39c686e6d` | 2026-11-19 |

## Transfer source for Wizardry II
`03_werdna_beaten` is the save to import from (owner's queue, 2026-11-19): the six after a real Werdna fight and
the ending, in the Castle, not in the maze ("out" 0 for all), each with the Chevron of Rank and the gear bought
for floor 10. Levels and values as the fight left them: RYZ and CONDI level 11 (drained by the vampires), EBO,
CUBI, DEDDO, MNZ level 13; E.P. 184,587-616,313; gold 55,077-74,817; armour class -4 to 9. CONDI's pack
keeps an empty entry where the amulet was (item count 6, one entry item 0), like 02_ending.
List it with `python3 games/dos/wizardry/tools/roster.py games/dos/wizardry/saves/03_werdna_beaten.sav`; for a
Wizardry II transfer the file inside (`WIZAR1/SAVE1.DSK`) is the source scenario disk.
