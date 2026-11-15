# Pokémon Blue Version - shots: seq-fishing

Platform gb, model dmg, ROM SHA-1 `d7037c83e1ae5b39bde3c30787637ba1d4c48ce2`. 15 shots. Contact sheet: [sheet.png](sheet.png).

| id | category | caption | settled | image |
|---|---|---|---|---|
| 01_shore | gameplay | ryz stands on Vermilion City's harbour, facing the water | no | [png](01_shore.png) [3x](01_shore@3x.png) |
| 02_start_menu | menu | Press START, move the cursor to ITEM | no | [png](02_start_menu.png) [3x](02_start_menu@3x.png) |
| 03_bag | menu | ITEM: the bag opens on BICYCLE | no | [png](03_bag.png) [3x](03_bag@3x.png) |
| 04_super_rod | menu | Scroll down to SUPER ROD | no | [png](04_super_rod.png) [3x](04_super_rod@3x.png) |
| 05_use | menu | A on SUPER ROD: USE / TOSS, cursor on USE | no | [png](05_use.png) [3x](05_use@3x.png) |
| 06_used_rod | dialogue | A on USE: "ryz used SUPER ROD!" | yes | [png](06_used_rod.png) [3x](06_used_rod@3x.png) |
| 07_cast_clip | gameplay | Clip: ryz casts the line and waits; the rod jerks when something bites | clip | [png](07_cast_clip.png) [3x](07_cast_clip@3x.png) [gif](07_cast_clip.gif) [gif 3x](07_cast_clip@3x.gif) |
| 08_bite | dialogue | "Oh! It's a bite!" - the cast was hooked | no | [png](08_bite.png) [3x](08_bite@3x.png) |
| 09_battle_clip | battle | Clip: A closes the text; the wild-battle transition flashes and wipes the screen, the hooked POKéMON slides in | clip | [png](09_battle_clip.png) [3x](09_battle_clip@3x.png) [gif](09_battle_clip.gif) [gif 3x](09_battle_clip@3x.gif) |
| 10_hooked | battle | Battle starts: "The hooked SHELLDER..." (6 party balls shown) | yes | [png](10_hooked.png) [3x](10_hooked@3x.png) |
| 11_attacked | battle | A: "...SHELLDER attacked!" | yes | [png](11_attacked.png) [3x](11_attacked@3x.png) |
| 12_battle_menu | battle | BLASTOISE L52 is sent out; the battle menu opens vs the wild SHELLDER L15 | yes | [png](12_battle_menu.png) [3x](12_battle_menu@3x.png) |
| 13_nibble_clip | gameplay | Branch from the same USE menu, A pressed one frame sooner: ryz casts and waits, nothing bites | clip | [png](13_nibble_clip.png) [3x](13_nibble_clip@3x.png) [gif](13_nibble_clip.gif) [gif 3x](13_nibble_clip@3x.gif) |
| 14_nibble | dialogue | Failed outcome: "Not even a nibble!" - no battle | no | [png](14_nibble.png) [3x](14_nibble@3x.png) |
| 15_nibble_end | gameplay | A closes the text: ryz is back on the harbour, free to cast again | no | [png](15_nibble_end.png) [3x](15_nibble_end@3x.png) |

Sequence: [full.gif](full.gif) ([3x](full@3x.gif)) = all steps stitched (stills held, clips played), [strip.png](strip.png), [steps.gif](steps.gif) ([3x](steps@3x.gif)) = stills only.

Routes (replay with `tools/shoot.py`) are in `index.json` and `shots.txt`.
