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

; Character title (2B:5FB8): keep ld de,$C632, drop the [w=12][h=1] writes so the record (now a VWF rect
; header, script/titles.json) is copied as the header of the RAM rect.
org 43, $5fbb
    ds 8, $00

; Battle monster-group panel: 22:5682 call $199B -> trampoline -> VWF_Panel (proportional names).
org 34, $5682
    call $7f00
org 34, $7f00
    ld a, VWF_BANK
    ld hl, VWF_Panel
    jp FarCall

; Spells (docs/re/spells.md): 0:24CF also fetches the full English name into wSpell (bank 7 $D280).
org 0, $24cf
    call Stub_SpellPre
; Spell list (2A:4CBB): the 11 name cells of the RAM rect are blanked (copy from zeros) and, after the blit,
; the VWF prints wSpell in the row (88 px).
org 42, $4d42
    ld hl, $7fe0
org 42, $4d8e
    call $7f00
org 42, $7f00
    call $1723
    ld a, VWF_BANK
    ld hl, VWF_SpellList
    jp FarCall
; Spell detail, element (2A:4A29-4A35 copied 2 kanji tiles + 2 attributes): English via Stub_Fix, key 2A:49A9+4i
org 42, $4a29
    call Stub_Fix
    db 3
    jr $4a36
    ds 7, $00

; VBlank map copy (0:1674): ld a,[$c48b] -> Stub_Hold (skips the copy while a menu is being printed)
org 0, $167d
    call Stub_Hold
