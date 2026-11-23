# The Bard's Tale III - dungeon level maps (decoded from RAM)

Written by `games/apple2/bards-tale-3/tools/maps.py` (2026-11-21): every level is loaded through the stairs code
from the checkpoint `cat_stairs` and its square table is read from RAM (format in the tool's docstring and in
`playbook.md`, "Game structure"). These are reference maps for `design/`, not shot-set pictures.

Legend: north is up, columns are east, rows are north (the game's own `?` coordinates). Walls white (`|`, `---`),
doors orange (`D`), other sides red (`S`: secret doors or special walls; not told apart yet). Squares with flag
byte 2 set are shaded and show the byte in hex (`01` = stairs up at the catacombs arrival; other values not
decoded); `+` = flag byte 3 set (meaning not decoded); `*` = visited (the automap bit, as the dump's character
disk left it). Messages, fixed fights, gates and teleports come from a separate event list and are not on
these maps (see the shot set and `tools/scan.py` for those).

Not written: 2A-2C Malefia (the arrival teleports at once, the loader check of the tool does not see the level).
The automap bit shows how far the previous owner of the dump explored (a full level = all `*`).

| Level | Name | Disk | Size | Files |
|---|---|---|---|---|
| 00 | Festering Pit | side A | 15x15 | [txt](00_festering-pit.txt) [png](00_festering-pit.png) |
| 01 | Festering Pit | side A | 12x12 | [txt](01_festering-pit.txt) [png](01_festering-pit.png) |
| 02 | Palace | side A | 15x10 | [txt](02_palace.txt) [png](02_palace.png) |
| 03 | Tower | side A | 5x5 | [txt](03_tower.txt) [png](03_tower.png) |
| 04 | Tower | side A | 5x5 | [txt](04_tower.txt) [png](04_tower.png) |
| 05 | Tower | side A | 5x5 | [txt](05_tower.txt) [png](05_tower.png) |
| 06 | Tower | side A | 5x5 | [txt](06_tower.txt) [png](06_tower.png) |
| 07 | Sacred Grove | side A | 10x10 | [txt](07_sacred-grove.txt) [png](07_sacred-grove.png) |
| 08 | White Tower | side A | 5x5 | [txt](08_white-tower.txt) [png](08_white-tower.png) |
| 09 | White Tower | side A | 5x5 | [txt](09_white-tower.txt) [png](09_white-tower.png) |
| 0A | White Tower | side A | 5x5 | [txt](0A_white-tower.txt) [png](0A_white-tower.png) |
| 0B | White Tower | side A | 5x5 | [txt](0B_white-tower.txt) [png](0B_white-tower.png) |
| 0C | Grey Tower | side A | 5x5 | [txt](0C_grey-tower.txt) [png](0C_grey-tower.png) |
| 0D | Grey Tower | side A | 5x5 | [txt](0D_grey-tower.txt) [png](0D_grey-tower.png) |
| 0E | Grey Tower | side A | 5x5 | [txt](0E_grey-tower.txt) [png](0E_grey-tower.png) |
| 0F | Grey Tower | side A | 5x5 | [txt](0F_grey-tower.txt) [png](0F_grey-tower.png) |
| 10 | Black Tower | side A | 5x5 | [txt](10_black-tower.txt) [png](10_black-tower.png) |
| 11 | Black Tower | side A | 5x5 | [txt](11_black-tower.txt) [png](11_black-tower.png) |
| 12 | Black Tower | side A | 5x5 | [txt](12_black-tower.txt) [png](12_black-tower.png) |
| 13 | Black Tower | side A | 5x5 | [txt](13_black-tower.txt) [png](13_black-tower.png) |
| 14 | Ice Dungeon | side A | 9x9 | [txt](14_ice-dungeon.txt) [png](14_ice-dungeon.png) |
| 15 | Ice Dungeon | side A | 5x5 | [txt](15_ice-dungeon.txt) [png](15_ice-dungeon.png) |
| 16 | Ice Keep | side A | 12x10 | [txt](16_ice-keep.txt) [png](16_ice-keep.png) |
| 17 | Ice Keep | side A | 12x10 | [txt](17_ice-keep.txt) [png](17_ice-keep.png) |
| 18 | Mountain | side A | 18x18 | [txt](18_mountain.txt) [png](18_mountain.png) |
| 19 | Mountain | side A | 11x11 | [txt](19_mountain.txt) [png](19_mountain.png) |
| 1A | Cyanis' Tower | side B | 7x7 | [txt](1A_cyanis--tower.txt) [png](1A_cyanis--tower.png) |
| 1B | Cyanis' Tower | side B | 7x7 | [txt](1B_cyanis--tower.txt) [png](1B_cyanis--tower.png) |
| 1C | Cyanis' Tower | side B | 7x7 | [txt](1C_cyanis--tower.txt) [png](1C_cyanis--tower.png) |
| 1D | Alliria's Tomb | side A | 13x17 | [txt](1D_alliria-s-tomb.txt) [png](1D_alliria-s-tomb.png) |
| 1E | Alliria's Tomb | side A | 13x9 | [txt](1E_alliria-s-tomb.txt) [png](1E_alliria-s-tomb.png) |
| 1F | Wasteland | side B | 11x17 | [txt](1F_wasteland.txt) [png](1F_wasteland.png) |
| 20 | Tarmitia | side B | 12x12 | [txt](20_tarmitia.txt) [png](20_tarmitia.png) |
| 21 | Berlin | side B | 12x12 | [txt](21_berlin.txt) [png](21_berlin.png) |
| 22 | Stalingrad | side B | 12x12 | [txt](22_stalingrad.txt) [png](22_stalingrad.png) |
| 23 | Hiroshima | side B | 12x12 | [txt](23_hiroshima.txt) [png](23_hiroshima.png) |
| 24 | Troy | side B | 12x12 | [txt](24_troy.txt) [png](24_troy.png) |
| 25 | Rome | side B | 12x12 | [txt](25_rome.txt) [png](25_rome.png) |
| 26 | Nottingham | side B | 12x12 | [txt](26_nottingham.txt) [png](26_nottingham.png) |
| 27 | K'un Wang | side B | 12x16 | [txt](27_k-un-wang.txt) [png](27_k-un-wang.png) |
| 28 | Catacombs | side A | 13x13 | [txt](28_catacombs.txt) [png](28_catacombs.png) |
| 29 | Tunnels | side A | 22x10 | [txt](29_tunnels.txt) [png](29_tunnels.png) |
| 2D | Barracks | side B | 12x15 | [txt](2D_barracks.txt) [png](2D_barracks.png) |
| 2E | Ferofist's | side B | 18x18 | [txt](2E_ferofist-s.txt) [png](2E_ferofist-s.png) |
| 2F | Private Quarter | side B | 9x17 | [txt](2F_private-quarter.txt) [png](2F_private-quarter.png) |
| 30 | Workshop | side B | 9x9 | [txt](30_workshop.txt) [png](30_workshop.png) |
| 31 | Urmech's Paradi | side B | 15x15 | [txt](31_urmech-s-paradi.txt) [png](31_urmech-s-paradi.png) |
| 32 | Viscous Plane | side B | 15x9 | [txt](32_viscous-plane.txt) [png](32_viscous-plane.png) |
| 33 | Sanctum | side B | 13x13 | [txt](33_sanctum.txt) [png](33_sanctum.png) |
| 34 | UnterBrae | side A | 15x15 | [txt](34_unterbrae.txt) [png](34_unterbrae.png) |
| 35 | UnterBrae | side A | 15x15 | [txt](35_unterbrae.txt) [png](35_unterbrae.png) |
| 36 | UnterBrae | side A | 15x15 | [txt](36_unterbrae.txt) [png](36_unterbrae.png) |
| 37 | UnterBrae | side A | 10x22 | [txt](37_unterbrae.txt) [png](37_unterbrae.png) |
| 38 | Tar quarry | side B | 11x17 | [txt](38_tar-quarry.txt) [png](38_tar-quarry.png) |
| 39 | Shadow Canyon | side B | 13x22 | [txt](39_shadow-canyon.txt) [png](39_shadow-canyon.png) |
| 3A | Sceadu's Demens | side B | 15x15 | [txt](3A_sceadu-s-demens.txt) [png](3A_sceadu-s-demens.png) |
| 3B | Sceadu's Demens | side B | 15x15 | [txt](3B_sceadu-s-demens.txt) [png](3B_sceadu-s-demens.png) |
| 3C | Tarjan | side B | 6x6 | [txt](3C_tarjan.txt) [png](3C_tarjan.png) |
