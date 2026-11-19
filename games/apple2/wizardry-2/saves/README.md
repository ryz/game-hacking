# Wizardry II: The Knight of Diamonds - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = a ZIP of the disk images the game has written to (whole images, same names as in the game's ZIP): unzip it and use those images in place of the originals in any Apple II emulator. `.state` = AppleWin libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `rom/saves/apple2/wizardry-2/01_start.sav` (not committed) | roster after the transfer: RYZ CONDI EBO CUBI DEDDO MNZ, level 13, chevron, no items, in the Castle; the scenario disk's four stock characters deleted; the Wizardry I disk with the six gone from it | `pow,sav:00_transfer,PARTY,settle,e,w300,l,w900,settle` | `83686fb50ef7` | 2026-11-19 |
| 02_ending | `rom/saves/apple2/wizardry-2/02_ending.sav` (not committed) | roster after the ending: RYZ >G (Keeper of the Holy Staff, 986,327 E.P., no items), CONDI EBO CUBI DEDDO MNZ >K with their Boltac gear, level 13, in the Castle | `pow,sav:00_transfer,PARTY,settle,REST,settle,GEAR,e,w300,m,w1500,EQUIP,settle,l,w400,y,w900,settle,SOLO,KOD,MAZE,WARP:01:09:09,poke:730E=0000,k,w900,settle,enter,w600,settle,type:THE KNIGHT OF DIAMONDS\n,w600,settle,enter,w600,settle,enter,w600,settle,enter,w600,settle,HOME,settle,KNIGHTS,settle,REFORM,e,w300,m,w1500,l,w400,y,w900,settle,e,w300,l,w900,settle` | `9e3cd5b3f589` | 2026-11-19 |
