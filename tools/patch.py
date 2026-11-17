"""Apply ROM patches (IPS, BPS, UPS) to a dump: python3 tools/patch.py SOURCE OUTPUT PATCH[:LAYOUT] ...

Patches are applied in the order given. LAYOUT says which file layout a patch was made for:
  auto        (default) BPS/UPS: the layout whose CRC32 matches; IPS: the layout the dump already has
  headered    with the copier/iNES header (NES 16 bytes, SNES 512 bytes)
  unheadered  without it
  ines1       NES only: the dump's iNES header rewritten as plain iNES 1.0 (same mapper, sizes, mirroring,
              battery; NES 2.0 fields and bytes 8-15 cleared). Many patches were made against old iNES 1.0
              dumps; a dump re-headered as NES 2.0 differs only there. The patch's own target header is kept.
BPS and UPS check source, target and patch CRC32s; IPS has no checksum, so give the layout when the patch notes
name one (a wrong layout shifts every write by the header size). Used by tools/intake.py --patch.
"""
import os, sys, zlib


def crc(b):
    return zlib.crc32(bytes(b)) & 0xFFFFFFFF


def apply_ips(data, patch):
    """IPS onto a bytearray in place (RLE records, truncation extension supported)."""
    if patch[:5] != b"PATCH":
        raise ValueError("not an IPS patch")
    i = 5
    while patch[i:i + 3] != b"EOF":
        off = int.from_bytes(patch[i:i + 3], "big")
        size = int.from_bytes(patch[i + 3:i + 5], "big")
        i += 5
        if size:
            chunk = patch[i:i + size]
            i += size
        else:
            n = int.from_bytes(patch[i:i + 2], "big")
            chunk = patch[i + 2:i + 3] * n
            i += 3
        if off + len(chunk) > len(data):
            data.extend(b"\0" * (off + len(chunk) - len(data)))
        data[off:off + len(chunk)] = chunk
    if len(patch) == i + 6:                      # optional truncation length after EOF
        del data[int.from_bytes(patch[i + 3:i + 6], "big"):]
    return data


def _vlq(patch, pos):
    data, shift = 0, 1
    while True:
        x = patch[pos]
        pos += 1
        data += (x & 0x7F) * shift
        if x & 0x80:
            return data, pos
        shift <<= 7
        data += shift


def _crcs(patch):
    return [int.from_bytes(patch[-12 + 4 * i:len(patch) - 8 + 4 * i], "little") for i in range(3)]


def bps_source_crc(patch):
    return _crcs(patch)[0]


def apply_bps(src, patch):
    if patch[:4] != b"BPS1":
        raise ValueError("not a BPS patch")
    s_crc, t_crc, p_crc = _crcs(patch)
    if crc(patch[:-4]) != p_crc:
        raise ValueError("BPS patch CRC mismatch (damaged patch)")
    if crc(src) != s_crc:
        raise ValueError("BPS source CRC mismatch (wrong ROM, revision or header layout)")
    pos = 4
    src_size, pos = _vlq(patch, pos)
    tgt_size, pos = _vlq(patch, pos)
    meta, pos = _vlq(patch, pos)
    pos += meta
    out = bytearray(tgt_size)
    o = s_rel = t_rel = 0
    end = len(patch) - 12
    while pos < end:
        d, pos = _vlq(patch, pos)
        cmd, ln = d & 3, (d >> 2) + 1
        if cmd == 0:                                 # SourceRead
            out[o:o + ln] = src[o:o + ln]
            o += ln
        elif cmd == 1:                               # TargetRead
            out[o:o + ln] = patch[pos:pos + ln]
            pos += ln
            o += ln
        else:
            d2, pos = _vlq(patch, pos)
            off = (-1 if d2 & 1 else 1) * (d2 >> 1)
            if cmd == 2:                             # SourceCopy
                s_rel += off
                out[o:o + ln] = src[s_rel:s_rel + ln]
                s_rel += ln
                o += ln
            else:                                    # TargetCopy (may overlap)
                t_rel += off
                for _ in range(ln):
                    out[o] = out[t_rel]
                    o += 1
                    t_rel += 1
    if crc(out) != t_crc:
        raise ValueError("BPS target CRC mismatch")
    return out


def apply_ups(src, patch):
    if patch[:4] != b"UPS1":
        raise ValueError("not a UPS patch")
    a_crc, b_crc, p_crc = _crcs(patch)
    if crc(patch[:-4]) != p_crc:
        raise ValueError("UPS patch CRC mismatch (damaged patch)")
    pos = 4
    a_size, pos = _vlq(patch, pos)
    b_size, pos = _vlq(patch, pos)
    if crc(src) == a_crc and len(src) == a_size:
        tgt_size, tgt_crc = b_size, b_crc
    elif crc(src) == b_crc and len(src) == b_size:   # UPS is symmetric: patching B gives A
        tgt_size, tgt_crc = a_size, a_crc
    else:
        raise ValueError("UPS source CRC mismatch (wrong ROM, revision or header layout)")
    out = bytearray(src[:tgt_size]) + bytearray(max(0, tgt_size - len(src)))
    o = 0
    end = len(patch) - 12
    while pos < end:
        skip, pos = _vlq(patch, pos)
        o += skip
        while patch[pos]:
            if o < tgt_size:
                out[o] ^= patch[pos]
            o += 1
            pos += 1
        pos += 1
        o += 1
    if crc(out) != tgt_crc:
        raise ValueError("UPS target CRC mismatch")
    return out


def kind(patch):
    for magic, k in ((b"PATCH", "ips"), (b"BPS1", "bps"), (b"UPS1", "ups")):
        if patch[:len(magic)] == magic:
            return k
    raise ValueError("unknown patch format (IPS, BPS and UPS are supported)")


def header_size(data, ext):
    """Size of the copier/iNES header the dump carries now (0 if none)."""
    ext = ext.lower()
    if ext in (".nes", ".fds") and data[:4] in (b"NES\x1a", b"FDS\x1a"):
        return 16
    if ext in (".sfc", ".smc") and len(data) % 1024 == 512:
        return 512
    return 0


def _layouts(data, ext):
    """(name, bytes) for the dump with and without its header; the header to re-add when one is missing."""
    h = header_size(data, ext)
    if h:
        out = [("headered", bytes(data)), ("unheadered", bytes(data[h:]))]
        if h == 16 and data[:4] == b"NES\x1a":
            ines1 = data[:7] + bytes([data[7] & 0xF0]) + bytes(8) + data[16:]
            if ines1 != data:
                out.append(("ines1", bytes(ines1)))
        return out, data[:h]
    if ext.lower() in (".sfc", ".smc"):
        return [("unheadered", bytes(data)), ("headered", b"\0" * 512 + bytes(data))], b""
    return [("unheadered", bytes(data))], b""


def apply(data, patch, ext, layout="auto"):
    """Apply one patch. Returns (new bytes in the dump's original layout, layout used, format)."""
    k = kind(patch)
    variants, hdr = _layouts(data, ext)
    have = variants[0][0]
    if layout != "auto":
        variants = [v for v in variants if v[0] == layout]
        if not variants:
            raise ValueError("layout %s not possible for this dump (no header to add for %s)" % (layout, ext))
    if k == "ips":
        name, src = variants[0]
        out = apply_ips(bytearray(src), patch)
    else:
        fn = apply_bps if k == "bps" else apply_ups
        errors = []
        for name, src in variants:
            try:
                out = fn(src, patch)
                break
            except ValueError as e:
                if "source CRC" not in str(e):
                    raise
                errors.append("%s: %s" % (name, e))
        else:
            raise ValueError("; ".join(errors))
    if name != have and name != "ines1":     # back to the dump's own layout
        out = bytearray(hdr) + out if have == "headered" else out[512 if ext.lower() in (".sfc", ".smc") else 16:]
    return bytes(out), name, k


def main():
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    src, dst = sys.argv[1:3]
    data = open(src, "rb").read()
    ext = os.path.splitext(src)[1]
    for spec in sys.argv[3:]:
        path, _, layout = spec.partition(":")
        data, used, k = apply(data, open(path, "rb").read(), ext, layout or "auto")
        print("applied %s (%s, %s layout)" % (path, k, used))
    open(dst, "wb").write(data)
    print("wrote %s (%d bytes)" % (dst, len(data)))


if __name__ == "__main__":
    main()
