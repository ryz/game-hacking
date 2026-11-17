"""Parse fonts/vwf.txt -> per-code (advance, 8 row bytes); preview PNG."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "vwf.txt")
SPACING = 1


def load(path=FONT):
    glyphs = {}
    cur = None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("#") and cur is None or not line.strip():
            continue
        if line.startswith("== "):
            m = re.match(r"== (\S+)(?:\s+advance=(\d+))?", line)
            name = m.group(1)
            code = 0x20 if name == "space" else int(name, 16) if name.startswith("0x") else ord(name)
            cur = {"code": code, "rows": [], "adv": int(m.group(2)) if m.group(2) else None}
            glyphs[code] = cur
            continue
        if cur is not None and re.fullmatch(r"[.#]+", line):
            cur["rows"].append(line)
            if len(cur["rows"]) == 8:
                cur = None
    out = {}
    for code, g in glyphs.items():
        assert len(g["rows"]) == 8, hex(code)
        w = len(g["rows"][0])
        assert all(len(r) == w for r in g["rows"]), hex(code)
        rows = [int(r.replace("#", "1").replace(".", "0").ljust(8, "0")[:8], 2) for r in g["rows"]]
        out[code] = (g["adv"] if g["adv"] is not None else w + SPACING, rows)
    return out


def text_width(s_bytes, font=None):
    font = font or load()
    return sum(font[b][0] for b in s_bytes if b in font)


def preview(path, text="The quick brown fox jumps over the lazy dog. 0123456789 !?,.'\"-:;/()+%&"):
    from PIL import Image
    f = load()
    W = text_width(text.encode("latin1"), f) + 4
    im = Image.new("RGB", (W, 12), (40, 40, 80))
    x = 2
    for ch in text.encode("latin1"):
        adv, rows = f[ch]
        for y, r in enumerate(rows):
            for b in range(8):
                if r & (0x80 >> b):
                    im.putpixel((x + b, 2 + y), (255, 255, 255))
        x += adv
    im.resize((W * 4, 48), Image.NEAREST).save(path)


if __name__ == "__main__":
    preview(sys.argv[1] if len(sys.argv) > 1 else "build/font_preview.png")
