"""Put the party next to a maze square and face it (EN build), save the state, then step in and check the event.

  python3 tools/maze_goto.py ROM MAZE_STATE X Y OUT.state [STEP_FRAMES=240]

Pokes $CB80 (x), $CB81 (y), $CB83 (facing: 0 y+1, 1 x+1, 2 y-1, 3 x-1) and the copies $CB96/$CB97 to the first
neighbour of (X,Y) on the same floor whose wall bits towards (X,Y) are 0 (open), presses left,right (redraw),
saves OUT.state, then presses up and reports whether 2D:63EB (event dispatcher) ran and with which $FFB0/$FFB1.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import emu
rom, st = [os.path.abspath(x) for x in sys.argv[1:3]]
X, Y = int(sys.argv[3]), int(sys.argv[4]); out = os.path.abspath(sys.argv[5])
fr = int(sys.argv[6]) if len(sys.argv) > 6 else 240
g = emu.open_emu(rom, st)
m = g.mem_read(0xD000, 0x400, bank=4)
cell = lambda x, y: m[(((y ^ 15) << 4) | x) * 4:][:4]
D = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
for d, (dx, dy) in D.items():
    nx, ny = (X - dx) & 15, (Y - dy) & 15          # neighbour from which moving in dir d enters (X,Y)
    if (cell(nx, ny)[0] >> (2 * d)) & 3 == 0 and cell(nx, ny)[2] & 0x3f in (0, 1, 5):
        break
else:
    sys.exit('no open neighbour')
print('neighbour (%d,%d) facing %d; target cell %s' % (nx, ny, d, cell(X, Y).hex()))
g.mem_write(0xCB80, bytes([nx, ny])); g.mem_write(0xCB83, bytes([d]))
g.mem_write(0xCB96, bytes([nx, ny]))
emu.press(g, ['left']); emu.press(g, ['right'])
p = g.mem_read(0xCB80, 4); print('after redraw x=%d y=%d f=%d dir=%d' % tuple(p))
g.snapshot_save(path=out)
g.screenshot_png(out.replace('.state', '_before.png'))
g.break_add(0x63EB, bank=0x2D, stop=False)
emu.press(g, ['up'], wait=fr)
print('pos', list(g.mem_read(0xCB80, 4)), 'dispatcher hits', g.break_list()[0]['hits'], 'FFB0/1', g.mem_read(0xFFB0, 2).hex(),
      'msg', g.mem_read(0xC1BF, 3).hex())
g.screenshot_png(out.replace('.state', '_after.png'))
