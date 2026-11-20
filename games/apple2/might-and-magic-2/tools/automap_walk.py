"""Honest walker for MM2 Apple II: DFS over the area's wall map (2F800: 2 bits per side, N E S W from bit 7),
avoiding event squares (table 2FA42.., triples square/event/mask), real steps checked against 0030.
Usage: python3 games/apple2/might-and-magic-2/tools/automap_walk.py START_ROUTE START_FACING(N/E/S/W) MAXNEW [AVOID_SQUARES_HEX,..]  -> prints the token route of the walk."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import emu as E
game = E.Game("apple2/might-and-magic-2")
route, face, maxnew = sys.argv[1], "NESW".index(sys.argv[2]), int(sys.argv[3])
avoid = set(int(a, 16) for a in sys.argv[4].split(",")) if len(sys.argv) > 4 else set()
emu, rest, _ = E.start(game, route)
E.play(emu, game, E.expand(game, E.split(",".join(rest))) if rest else [])
walls = emu.peek(0x2F800, 256)
ev = emu.peek(0x2FA42, 0x7E)
mask = {}
for i in range(0, len(ev) - 2, 3):
    mask[ev[i]] = mask.get(ev[i], 0) | ev[i + 1 + 1]
for a in avoid: mask[a] = 0xF0
BIT = [0x80, 0x40, 0x20, 0x10]
def ok_face(sq, d): return not (mask.get(sq, 0) & BIT[d])
def turns(sq, a, b):
    diff = (b - a) % 4
    if diff == 0: return []
    if diff == 1: return [b]
    if diff == 3: return [b]
    r = (a + 1) % 4; l = (a - 1) % 4
    if ok_face(sq, r): return [r, b]
    if ok_face(sq, l): return [l, b]
    return None
events = set()
DX = [(0, 1), (1, 0), (0, -1), (-1, 0)]
toks = []
def do(t):
    ts = E.expand(game, E.split(t)); E.play(emu, game, ts); toks.append(t)
def pos():
    v = emu.peek(0x30, 1)[0]; return v & 15, v >> 4
def side(sq, d):
    return (walls[sq] >> (6 - 2 * d)) & 3
def turn_to(d):
    global face
    x, y = pos(); sq = y * 16 + x
    for t in turns(sq, face, d):
        do("right,w200" if t == (face + 1) % 4 else "left,w200"); face = t
x, y = pos(); seen = {(x, y)}; stack = [(x, y)]; blocked = set(); new = 0
while stack and new < maxnew:
    x, y = stack[-1]
    moved = False
    for d in range(4):
        nx, ny = x + DX[d][0], y + DX[d][1]
        if not (0 <= nx < 16 and 0 <= ny < 16) or (nx, ny) in seen or (x, y, d) in blocked: continue
        if side(y * 16 + x, d) in (1, 3) or not ok_face(ny * 16 + nx, d) or not ok_face(y * 16 + x, d): continue
        if turns(y * 16 + x, face, d) is None: continue
        turn_to(d); do("up,w300")
        if pos() == (nx, ny):
            seen.add((nx, ny)); stack.append((nx, ny)); new += 1; moved = True
            sys.stderr.write("+(%d,%d) wall=%d\n" % (nx, ny, side(y * 16 + x, d)))
        elif pos() != (x, y):
            sys.stderr.write("!! unexpected %s from (%d,%d)\n" % (pos(), x, y)); print(",".join(toks)); sys.exit(1)
        else:
            blocked.add((x, y, d)); sys.stderr.write("-(%d,%d) blocked wall=%d\n" % (nx, ny, side(y * 16 + x, d)))
        break
    if not moved and stack[-1] == (x, y) and all(
            not (0 <= x + DX[d][0] < 16 and 0 <= y + DX[d][1] < 16) or (x + DX[d][0], y + DX[d][1]) in seen
            or (x, y, d) in blocked or side(y * 16 + x, d) in (1, 3) or not ok_face((y + DX[d][1]) * 16 + x + DX[d][0], d) or not ok_face(y * 16 + x, d) or turns(y * 16 + x, face, d) is None
            for d in range(4)):
        stack.pop()
        if stack:
            px, py = stack[-1]
            d = DX.index((px - x, py - y)); turn_to(d); do("up,w300")
            if pos() != (px, py): sys.stderr.write("!! backtrack failed\n"); break
sys.stderr.write("new=%d seen=%d end=%s face=%s\n" % (new, len(seen), pos(), "NESW"[face]))
print(",".join(toks))
