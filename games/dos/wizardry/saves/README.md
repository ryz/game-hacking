# Wizardry: Proving Grounds of the Mad Overlord (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | Roster after Leave Game: the six pre-made characters plus ryz (fighter), condi (fighter), ebo (priest), cubi (thief), deddo (mage), mnz (bishop), level 1, about 180 gold each, no equipment; party not formed (RESUME adds them) | `@start,e,w120,l,w600,settle` | `155612d15e3e` | 2026-11-19 |
| 02_ending | `02_ending.sav` | Roster after the ending (veterans from VET, amulet by AMULET, scout run): ryz condi ebo cubi deddo mnz level 13 with the Chevron of Rank (>), 50,000 more G.P. and E.P., no equipment; party not formed (RESUME adds them). Base for a Wizardry II transfer save | `@after_ending,e,w120,l,w600,settle` | `d9d241a73281` | 2026-11-19 |
