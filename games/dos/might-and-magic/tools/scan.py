"""scan.py AREA [BASE] [--tail TOKENS]: visit every event square of the current area and tile the results.

  python3 games/dos/might-and-magic/tools/scan.py 0 @start         # Sorpigal, party standing anywhere in Sorpigal

AREA is the index/name used by maps.py (the party must already be IN that area: this only moves it inside the
16x16 map). For each event square: poke the party onto it facing one turn clockwise of the event's facing, press
Left (the turn redraws the view and runs the square's event), wait, keep the last frame.
Output: work/scout/dos/might-and-magic/scan_AREA.png (+ scan_AREA/NN/ with the emu.py frames), labels x,y,facing.
"""
import os, subprocess, sys, zipfile
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
FACE = {"N": "C003300C10FF01F0", "E": "30C00C030110F0FF", "S": "0C3003C0F001FF10", "W": "030CC030FFF01001"}  # 15E6D..15E74
CW = {"N": "E", "E": "S", "S": "W", "W": "N"}

def goto(x, y, face):
    """Tokens that put the party on (x,y) facing `face` (view not redrawn until the next move or turn)."""
    return "poke:15E68=%02X%02X%02X,poke:15E6D=%s" % (x, y, y * 16 + x, FACE[face])

def main():
    args = sys.argv[1:]; tail = "left,w250"
    if "--tail" in args:
        i = args.index("--tail"); tail = args[i + 1]; del args[i:i + 2]
    area = args[0]; base = args[1] if len(args) > 1 else "@start"
    sys.argv = ["maps.py", os.path.join(ROOT, "rom", "might-and-magic.zip")]
    import maps
    idx = int(area) if area.isdigit() else maps.NAMES.index(area.upper())
    ev, _ = maps.events(maps.NAMES[idx])
    out = os.path.join(ROOT, "work", "scout", "dos", "might-and-magic", "scan_%s" % area)
    jobs = []
    for o, m in sorted(ev.items()):
        f = next((k for k, v in (("N", 0xC0), ("E", 0x30), ("S", 0x0C), ("W", 0x03)) if m & v), "N")
        jobs.append((o & 15, o >> 4, f))
    def run(j):
        x, y, f = j; d = os.path.join(out, "%02d_%02d_%s" % (x, y, f))
        seq = "%s,%s,%s" % (base, goto(x, y, CW[f]), tail)
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "emu.py"), "dos/might-and-magic", "--seq", seq, "--out", d],
                       capture_output=True, text=True)
        pngs = sorted(p for p in os.listdir(d) if p[:2].isdigit())
        return j, Image.open(os.path.join(d, pngs[-1])).convert("RGB")
    with ThreadPoolExecutor(4) as ex: res = list(ex.map(run, jobs))
    cols = 4; w, h = res[0][1].size; rows = (len(res) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * (h + 12)), (60, 0, 0)); dr = ImageDraw.Draw(sheet)
    for i, ((x, y, f), im) in enumerate(res):
        px, py = (i % cols) * w, (i // cols) * (h + 12)
        sheet.paste(im, (px, py + 12)); dr.text((px + 2, py), "(%d,%d) facing %s" % (x, y, f), fill=(255, 255, 0))
    sheet.save(out + ".png"); print(out + ".png")

if __name__ == "__main__":
    main()
