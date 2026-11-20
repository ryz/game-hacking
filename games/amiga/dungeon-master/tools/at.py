"""Pointer token for a screen spot: python3 games/amiga/dungeon-master/tools/at.py SX SY [click]

SX SY are pixel coordinates in the 360x287 screenshot (tools/play.py, emu.py). Dungeon Master's pointer
tip is at screenshot (21, 19) after the macro HOME (pushed into the top-left corner); one mouse count moves it
half a pixel, and one `mouse:` token moves it at most 120 counts (60 px). The macro AT:A:B:C:D
(game.json) does HOME, then A moves of 120 counts right, B moves of 120 counts down, then C, D counts:
tip at x = 21 + 60*A + C/2, y = 19 + 60*B + D/2. CLICK takes the same arguments and presses the left button.
"""
import sys


def at(sx, sy):
    dx, dy = 2 * (sx - 21), 2 * (sy - 19)
    if not (0 <= dx and 0 <= dy):
        raise SystemExit("spot left of / above the pointer's corner (21, 19)")
    a, c = divmod(dx, 120)
    b, d = divmod(dy, 120)
    return "%d:%d:%d:%d" % (a, b, c, d)


if __name__ == "__main__":
    sx, sy = int(sys.argv[1]), int(sys.argv[2])
    print(("CLICK:" if len(sys.argv) > 3 else "AT:") + at(sx, sy))
