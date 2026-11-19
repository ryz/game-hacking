"""msgdump.py FIRST LAST: show maze messages FIRST..LAST on screen and tile their pages into one image.

  python3 games/dos/wizardry-3/tools/msgdump.py 0 30   -> work/scout/wizardry-3/msg/msg_000_030.png

Messages are compressed on WIZ3.DSK; the game shows message N when a plain-message square (kind 1) points at it.
Each run starts from `start`, carries a crystal (floor 6 admits the party), warps next to the floor 6 riddle square
(11,4), points that square (special B: AUX1 = N, AUX2 = 1, in both copies of the floor in memory, 0B6E4 and 0E524)
at message N and steps in, pressing Enter between pages (playbook "Shortcuts").
"""
import os, sys
from multiprocessing import Pool
sys.path.insert(0, '/home/user/game-hacking/tools')
OUT = '/home/user/game-hacking/work/scout/wizardry-3/msg'
def run(n):
    import emu as E
    g = E.Game('dos/wizardry-3')
    route = '@start,poke:DE86=0100,poke:DE88=000000000100EB03,WARP:06:0C:04,poke:DB6C=0300,a,w60,d,w60,poke:BA1A=%02X%02X,poke:BA3A=0100,poke:E85A=%02X%02X,poke:E87A=0100,w' % (n & 255, n >> 8, n & 255, n >> 8)
    m, rest, _ = E.start(g, route)
    for t in rest: E.step(m, g, t)
    pages = []
    for k in range(7):
        E.step(m, g, 'w200')
        im = m.image().convert('RGB').crop((0, 0, 320, 96))
        if not pages or im.tobytes() != pages[-1].tobytes():
            pages.append(im.copy())
        E.step(m, g, 'enter')
    m.close()
    return n, pages
if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2])
    os.makedirs(OUT, exist_ok=True)
    with Pool(4) as p: res = p.map(run, range(a, b + 1), chunksize=1)
    from PIL import Image, ImageDraw
    rows = []
    for n, pages in res:
        rows.append((n, pages))
    W = 320 * 3 + 40
    H = sum(96 * ((len(pg) + 2) // 3) for _, pg in rows) + 4 * len(rows)
    sh = Image.new('RGB', (W, H), (60, 0, 0)); dr = ImageDraw.Draw(sh); y = 0
    for n, pg in rows:
        dr.text((2, y + 2), str(n), fill=(255, 255, 0))
        for i, im in enumerate(pg):
            sh.paste(im, (40 + (i % 3) * 320, y + (i // 3) * 96))
        y += 96 * ((len(pg) + 2) // 3) + 4
    p = '%s/msg_%03d_%03d.png' % (OUT, a, b); sh.save(p); print(p, sh.size)
