# Ultima II: The Revenge of the Enchantress (DOS) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the files the game has written, as a ZIP (DOSBox Pure's save format; folders have their DOS short names): unzip it and copy the files over the ones in your game folder (Might and Magic: `ROSTER.DTA`), or keep it as `<game zip name>.pure.zip` in DOSBox Pure's save folder. `.state` = DOSBox Pure libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav` | ryz (male human fighter, Str 45 Agi 20 Sta 15 Cha 10 Wis 10 Int 15), new character saved with Q on the 1423 B.C. surface at (14,14): 400 H.P., 399 food, 400 gold, no equipment | `NEWGAME,settle,q,w300,settle` (from power-on) | `f2fc47f1ebef` | 2026-11-19 |
| 02_endgame | `02_endgame.sav` | late ryz (level 20, H.P. 3184, gold 4882) on the 1990 A.D. surface outside New San Antonio, with Enilno (quicksword), the ring and Father Antos's blessing, reflect armour, ankh, tri-lithium, keys, torches; rocket parked in 2112 A.D. | `pow,NEWGAME,settle,HERO,space,w60,TIME:03,ENTER:0F:1A,SANTRE,OLDMAN,LEAVE,ROCKET,LAUNCH,WARP:9:9:9,l,w300,TOUCH:0C:0D,x,w60,up,w60,e,w300,BLESS,RETURN,TIME:03,ENTER:0F:1A,OLDMAN,LEAVE,q,w300` (from power-on) | `666ddf96961d` | 2026-11-19 |
