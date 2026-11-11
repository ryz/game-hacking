; Patch entry point (tools/build.py assembles this file).
    include "vwf.asm"

; Inn "Next level in / <n> の / more EXP.": the の tile after the number ($5D, now a VWF slot) -> blank.
org 39, $5422
    ld a, $20

; Shop header alignment (29:421A): ld a,$26 / ld bc,5 / ld de,$d048 / call $0C97 copied 5 bytes of the
; bank-38 alignment rect raw -> Stub_Fix with a far source bank.
org 41, $421a
    ld de, $d048
    call Stub_Fix
    db $85, $26
    nop
    nop
    nop

; Shop "sold out" row (41:70E1, $00-terminated, printed raw by a DE-source loop at 41:49EB): in-place
; ASCII, 17 bytes max (JP: ----- うりきれ -----).
org 41, $70e1
    db "--- Sold out ---", 0
