; Patch entry point (tools/build.py assembles this file).
    include "vwf.asm"

; Inn "Next level in / <n> の / more EXP.": the の tile after the number ($5D, now a VWF slot) -> blank.
org 39, $5439
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

; Shop "sold out" row (41:70E1, $00-terminated; the copy at 41:49EB goes through Stub_PrintZ, asm/vwf.asm):
; in-place ASCII, 17 bytes max (JP: ----- うりきれ -----).
org 41, $70e1
    db "--- Sold out ---", 0

; Character title (2B:5FB8): keep ld de,$C632, drop the [w=12][h=1] writes so the record (now a VWF rect
; header, script/titles.json) is copied as the header of the RAM rect.
org 43, $5fda
    ds 8, $00

; Training 'change class' prompt (26:5072): keep ld a,$10 / ld c,a (copy count), drop the [w=16][h=1] writes
; so the record (now a VWF rect header, script/classprompts.json) is copied as the header of the RAM rect.
org 38, $5082
    ds 6, $00

; Battle monster-group panel: 22:5682 call $199B -> trampoline -> VWF_Panel (proportional names).
org 34, $5688
    call $7f00
org 34, $7f00
    ld a, VWF_BANK
    ld hl, VWF_Panel
    jp FarCall

; Spells (docs/re/vwf.md, 'Spells'): 0:24E8 also fetches the full English name into wSpell (bank 7 $D280).
org 0, $24e8
    call Stub_SpellPre
; Spell list (2A:4CBB): the 11 name cells of the RAM rect are blanked (copy from zeros) and, after the blit,
; the VWF prints wSpell in the row (88 px).
org 42, $4d58
    ld hl, $7fe0
org 42, $4da4
    call $7f00
org 42, $7f00
    call $173c
    ld a, VWF_BANK
    ld hl, VWF_SpellList
    jp FarCall
; Spell detail, element (2A:4A29-4A35 copied 2 kanji tiles + 2 attributes): English via Stub_Fix, key 2A:49A9+4i
org 42, $4a3f
    call Stub_Fix
    db 3
    jr $4a4c
    ds 7, $00

; Notice Board (2B:57E0): far call to the fade-in -> trampoline: VWF_Notice, then the fade-in (English text)
org 43, $57ff
    call $7f00
    ds 5, $00
org 43, $7f00
    ld a, VWF_BANK
    ld hl, VWF_Notice
    call FarCall
    ld a, $26
    ld hl, $4054
    jp FarCall

; "Look for whom?" maze location (2E:5774-57F2): now one VWF string, see SPLine in vwf.asm.
org 46, $57c1
    db $80

