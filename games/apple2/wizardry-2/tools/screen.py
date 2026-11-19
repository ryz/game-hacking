"""screen.py [--name SESSION] ["tokens"]: print the 40x24 text screen of a running play.py session as text.

  python3 games/apple2/wizardry-2/tools/screen.py --name wiz2 "g,w120"

With tokens it runs `play.py do "tokens"` first. The castle, shops, training grounds, camp and character
sheets are Apple II text screens (page 1 at 0400); reading them as text is cheaper and more exact than
looking at a screenshot. The maze, fights and chests are hi-res pictures (text drawn as pixels): look at
work/play/SESSION/last.png for those. Inverse and flashing characters are printed as plain ones.
"""
import os, subprocess, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))

def rows(mem):
    out = []
    for r in range(24):
        base = 0x80 * (r % 8) + 0x28 * (r // 8)
        out.append("".join(chr(c & 0x7F) if 32 <= (c & 0x7F) < 127 else chr((c & 0x3F) + 64) if (c & 0x7F) < 32 else " " for c in mem[base:base + 40]).rstrip())
    return out

def main():
    a = sys.argv[1:]; name = "main"
    if "--name" in a: i = a.index("--name"); name = a[i + 1]; del a[i:i + 2]
    play = [sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", name]
    if a:
        r = subprocess.run(play + ["do", a[0]], capture_output=True, text=True, cwd=ROOT)
        print((r.stdout + r.stderr).strip())
    r = subprocess.run(play + ["peek", "0400", "1024"], capture_output=True, text=True, cwd=ROOT)
    mem = bytearray()
    for line in r.stdout.splitlines():
        p = line.split()
        if len(p) >= 2 and len(p[0]) == 4:
            try: mem += bytes(int(x, 16) for x in p[1:17])
            except ValueError: pass
    if len(mem) < 1024: print(r.stdout, r.stderr); return
    for line in rows(mem): print("|" + line)

if __name__ == "__main__":
    main()
