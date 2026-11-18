"""Apply a BPS patch (beat format) to a ROM: python3 tools/bps.py PATCH SOURCE OUTPUT

Used for the reference English translation (an existing fan patch, never committed): put the .bps in rom/ and
run `python3 tools/bps.py rom/reference_en.bps rom/wizardry_empire_j.gbc rom/wizardry_empire_ref.gbc`.
Checks the source, target and patch CRC32s.
"""
import sys, zlib


def apply(patch, src):
    assert patch[:4] == b"BPS1", "not a BPS patch"
    pos = 4

    def num():
        nonlocal pos
        data, shift = 0, 1
        while True:
            x = patch[pos]; pos += 1
            data += (x & 0x7F) * shift
            if x & 0x80:
                return data
            shift <<= 7
            data += shift
    src_size, tgt_size, meta = num(), num(), num()
    pos += meta
    assert len(src) == src_size, "source size %d != %d" % (len(src), src_size)
    s_crc, t_crc, p_crc = (int.from_bytes(patch[-12 + 4 * i:-8 + 4 * i or None], "little") for i in range(3))
    assert zlib.crc32(src) & 0xFFFFFFFF == s_crc, "source CRC mismatch (wrong ROM?)"
    assert zlib.crc32(patch[:-4]) & 0xFFFFFFFF == p_crc, "patch CRC mismatch"
    out = bytearray(tgt_size)
    o = s_rel = t_rel = 0
    end = len(patch) - 12
    while pos < end:
        d = num()
        cmd, ln = d & 3, (d >> 2) + 1
        if cmd == 0:                       # SourceRead
            out[o:o + ln] = src[o:o + ln]; o += ln
        elif cmd == 1:                     # TargetRead
            out[o:o + ln] = patch[pos:pos + ln]; pos += ln; o += ln
        else:
            d2 = num()
            off = (-1 if d2 & 1 else 1) * (d2 >> 1)
            if cmd == 2:                   # SourceCopy
                s_rel += off
                out[o:o + ln] = src[s_rel:s_rel + ln]; s_rel += ln; o += ln
            else:                          # TargetCopy (may overlap)
                t_rel += off
                for _ in range(ln):
                    out[o] = out[t_rel]; o += 1; t_rel += 1
    assert zlib.crc32(out) & 0xFFFFFFFF == t_crc, "target CRC mismatch"
    return out


if __name__ == "__main__":
    p, s, t = sys.argv[1:4]
    out = apply(open(p, "rb").read(), open(s, "rb").read())
    open(t, "wb").write(out)
    print("wrote %s (%d bytes)" % (t, len(out)))
