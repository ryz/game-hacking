; Patch entry point (tools/build.py assembles this file).
    include "vwf.asm"

; Inn "Next level in / <n> の / more EXP.": the の tile after the number ($5D, now a VWF slot) -> blank.
org 39, $5422
    ld a, $20
