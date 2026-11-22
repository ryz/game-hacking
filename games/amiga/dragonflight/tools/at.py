"""Pointer token for a screen spot: python3 games/amiga/dragonflight/tools/at.py SX SY [click]

SX SY are pixel coordinates in the 720x287 game screenshot (tools/play.py, preview.py: the game runs in a
hires screen, so one game pixel is two screenshot pixels wide). Dragonflight keeps its pointer position in
chip RAM at 3BCA (x, word) and 3BCC (y, word) in game pixels; the scout (2026-11-22) found that poking them
places the pointer exactly, which is safer than relative mouse moves (the game reads the mouse counters only
every few frames, so large `mouse:` moves wrap and land anywhere). Mapping, checked on the icon grid, the
portraits and the disk menu: SX = 2*x + 35, SY = y + 15.

Prints `PT:XXXX:YYYY` (game.json macro: poke the pointer) or `CLK:XXXX:YYYY` (poke + left click + w60).
"""
import sys


def at(sx, sy):
    x, y = (sx - 35) // 2, sy - 15
    if not (0 <= x < 320 and 0 <= y < 256):
        raise SystemExit("spot outside the game screen")
    return "%04X:%04X" % (x, y)


if __name__ == "__main__":
    sx, sy = int(sys.argv[1]), int(sys.argv[2])
    print(("CLK:" if len(sys.argv) > 3 else "PT:") + at(sx, sy))
