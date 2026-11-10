"""IPS patch writer/applier (with RLE records). Bytes past the original size are always emitted."""


def make(orig_padded, new, orig_len):
    out = bytearray(b"PATCH")
    i, n = 0, len(new)
    while i < n:
        if i < orig_len and orig_padded[i] == new[i]:
            i += 1
            continue
        # start of a changed (or appended) region
        j = i
        while j < n and j - i < 0xFFFF and (j >= orig_len or orig_padded[j] != new[j]):
            j += 1
        chunk = new[i:j]
        k = 0
        while k < len(chunk):
            # RLE for runs >= 8
            r = 1
            while k + r < len(chunk) and chunk[k + r] == chunk[k] and r < 0xFFFF:
                r += 1
            off = i + k
            if r >= 8:
                out += off.to_bytes(3, "big") + b"\x00\x00" + r.to_bytes(2, "big") + bytes([chunk[k]])
                k += r
                continue
            # literal until next long run
            m = k
            while m < len(chunk):
                r2 = 1
                while m + r2 < len(chunk) and chunk[m + r2] == chunk[m] and r2 < 8:
                    r2 += 1
                if r2 >= 8:
                    break
                m += r2
            lit = chunk[k:m]
            out += off.to_bytes(3, "big") + len(lit).to_bytes(2, "big") + lit
            k = m
        i = j
    out += b"EOF"
    return bytes(out)


def apply(orig, patch):
    rom = bytearray(orig)
    assert patch[:5] == b"PATCH"
    p = 5
    while patch[p:p + 3] != b"EOF":
        off = int.from_bytes(patch[p:p + 3], "big"); p += 3
        size = int.from_bytes(patch[p:p + 2], "big"); p += 2
        if size == 0:
            r = int.from_bytes(patch[p:p + 2], "big"); p += 2
            data = bytes([patch[p]]) * r; p += 1
        else:
            data = patch[p:p + size]; p += size
        if off + len(data) > len(rom):
            rom += b"\x00" * (off + len(data) - len(rom))
        rom[off:off + len(data)] = data
    return bytes(rom)
