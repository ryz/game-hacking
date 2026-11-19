"""u3rng.py: the random number generator of Ultima III (DOS), for forcing rolls by poke.

The state is 16 bytes at physical 4413-4422 (DS:2A93). Each call (code 0x514B): from the last byte down, every
byte = itself + the byte after it (already updated) + carry; then the last byte is incremented (carry ripples
down); the result is byte 0, reduced modulo the limit by repeated subtraction (limit 0xFF: 0-254, 255 -> 0).

  python3 games/dos/ultima-3/tools/u3rng.py HEX32 N        the first N raw outputs of a state
  from u3rng import outputs, poke                          outputs(state_bytes, n); poke(state) -> token
"""
import sys

def step(s):
    c = 0
    for i in range(14, -1, -1):
        v = s[i] + s[i + 1] + c
        s[i] = v & 0xFF; c = v >> 8
    i = 15
    while i >= 0:
        s[i] = (s[i] + 1) & 0xFF
        if s[i]: break
        i -= 1
    return s[0]

def outputs(state, n):
    s = list(state); return [step(s) for _ in range(n)]

def mod(v, lim):
    while v >= lim: v -= lim
    return v

def poke(state):
    return "poke:4413=" + bytes(state).hex().upper()

if __name__ == "__main__":
    st = bytes.fromhex(sys.argv[1]); n = int(sys.argv[2])
    print(" ".join("%02X" % v for v in outputs(st, n)))
