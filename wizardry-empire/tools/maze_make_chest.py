"""Chest after a battle in the EN build, from a battle-start state.

  python3 tools/maze_make_chest.py ROM BATTLE_STATE OUTDIR [TYPE]

Pokes $C00B |= $04 (the 'guarded square: chest' bit that 20:5D0B sets for fixed encounters; 25:40CB checks
bit 3 = 0 and bit 2 = 1 after victory), then presses A (4 frames held, 20 released) until 25:40CB runs.
TYPE (optional, 0-47+): chest type forced by setting B at 25:4134 (0-6 bag, 7 bronze, 13 copper, 19 silver,
25 gold, 31 platinum, 36 paulownia, 41 lacquered, 46 jet-black, 47 bewitching); default = the game's own roll.
Writes OUTDIR/chest_victory.state (at 25:40CB, chest decision) and chest_menu.state (+png) after w60,a,w60.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import emu
rom, st, out = [os.path.abspath(x) for x in sys.argv[1:4]]
typ = int(sys.argv[4]) if len(sys.argv) > 4 else None
g = emu.open_emu(rom, st)
v = g.mem_read(0xC00B, 1)[0]
g.mem_write(0xC00B, bytes([v | 4]))
g.break_add(0x40CB, bank=0x25)
for i in range(600):
    g.input_set(['a']); r = g.run_frames(4); g.input_set([])
    if r.get('stopped'): break
    r = g.run_frames(20)
    if r.get('stopped'): break
else:
    sys.exit('no victory')
print('victory after', i + 1, 'A presses; C00B=%02x' % g.mem_read(0xC00B, 1)[0])
g.break_clear()
g.snapshot_save(path=out + '/chest_victory.state')
if typ is not None:
    g.break_add(0x4134, bank=0x25)
    r = g.run_frames(30); assert r.get('stopped'), r
    g.break_clear()
    g.set_regs(b=typ)
for t in ['w60', 'a', 'w60']:
    if t[0] == 'w': g.run_frames(int(t[1:]))
    else: emu.press(g, [t])
name = 'chest_menu' if typ is None else 'chest_menu_t%d' % typ
g.snapshot_save(path=out + '/%s.state' % name)
g.screenshot_png(out + '/%s.png' % name)
print('C634 (type) =', g.mem_read(0xC634, 1)[0])
