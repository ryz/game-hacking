import os, sys, zlib

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import patch  # noqa: E402


def vlq(n):
    out = bytearray()
    while True:
        x = n & 0x7F
        n >>= 7
        if not n:
            out.append(0x80 | x)
            return bytes(out)
        out.append(x)
        n -= 1


def c32(b):
    return zlib.crc32(b).to_bytes(4, "little")


def make_bps(src, tgt):
    """Whole target as one TargetRead (enough to exercise the CRC checks and layouts)."""
    body = b"BPS1" + vlq(len(src)) + vlq(len(tgt)) + vlq(0) + vlq(((len(tgt) - 1) << 2) | 1) + tgt
    body += c32(src) + c32(tgt)
    return body + c32(body)


def make_ups(a, b):
    body = bytearray(b"UPS1" + vlq(len(a)) + vlq(len(b)))
    x = bytes(p ^ q for p, q in zip(a.ljust(len(b), b"\0"), b))
    i = 0
    while i < len(x):
        j = i
        while j < len(x) and x[j] == 0:
            j += 1
        if j == len(x):
            break
        k = j
        while k < len(x) and x[k]:
            k += 1
        body += vlq(j - i) + x[j:k] + b"\0"
        i = k + 1
    body += c32(a) + c32(b)
    return bytes(body) + c32(body)


NES_HDR = b"NES\x1a" + bytes(12)
PRG = bytes(range(256)) * 4
NEW = PRG[:100] + b"HELLO" + PRG[105:]


def test_ips_rle_and_truncate():
    ips = b"PATCH" + b"\0\0\2\0\2AB" + b"\0\0\6\0\0\0\4Z" + b"EOF" + b"\0\0\x08"
    assert bytes(patch.apply_ips(bytearray(16), ips)) == b"\0\0AB\0\0ZZ"


@pytest.mark.parametrize("make", [make_bps, make_ups])
def test_crc_patches_find_header_layout(make):
    # patch made for the unheadered PRG, dump has an iNES header: header is kept, layout detected
    out, layout, _ = patch.apply(NES_HDR + PRG, make(PRG, NEW), ".nes")
    assert (out, layout) == (NES_HDR + NEW, "unheadered")
    # patch made for the headered file
    out, layout, _ = patch.apply(NES_HDR + PRG, make(NES_HDR + PRG, NES_HDR + NEW), ".nes")
    assert (out, layout) == (NES_HDR + NEW, "headered")
    with pytest.raises(ValueError, match="source CRC"):
        patch.apply(NES_HDR + bytes(1024), make(PRG, NEW), ".nes")


def test_ups_is_symmetric():
    assert patch.apply(NEW, make_ups(PRG, NEW), ".nes")[0] == PRG


def test_ips_layout_and_snes_header():
    ips = b"PATCH" + b"\0\0\0\0\1X" + b"EOF"
    rom = bytes(1024)
    assert patch.apply(rom, ips, ".sfc", "headered")[0] == rom    # write lands in the added header, removed again
    assert patch.apply(rom, ips, ".sfc")[0][:1] == b"X"
    assert patch.apply(NES_HDR + PRG, ips, ".nes", "unheadered")[0][:17] == NES_HDR + b"X"
