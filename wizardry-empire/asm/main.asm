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


; Automap (Compass / Teleport / map item) floor label: 地下 (tiles $BD $D5 $D4 of the 18:4000 block at cols 17-19 of
; the layouts 23:4D4A and 23:4FFD) -> blank + 'B' (tile $CF of the same block, 8 px like the axis digits), so the
; 'B' sits over the floor number at col 18 (owner's decision 2026-11-12: axis digits stay 8 px, only the label
; is translated).
org 35, $4d4a
    db $ff, $cf, $ff
org 35, $4ffd
    db $ff, $cf, $ff

; Automap cursor labels (23:461D copied 8 tile codes from the table 23:5DB5 + 8i into the top line $D008; the
; kana tiles $90-$BD hold them). English labels do not fit the 42 kana tiles, so: each label is pre-drawn in the
; small VWF glyphs as 8 tiles (build.py patch_automap_labels -> 23:7100 + 128i) and queued into VRAM tiles
; $90-$97 with the game's tile-copy queue 0:1443; the line then shows $90-$97. i = 16 (23:5E35) = no label.
AUTOLABEL_GFX equ $7100
org 35, $461d
    jp AutoLabel

org 35, $7000
AutoLabel:
    ld a, c
    sub $b5
    ld l, a
    ld a, b
    sbc $5d
    ld h, a                 ; hl = bc - $5DB5 = 8 * i
    ld a, l
    cp $80
    jr nz, .draw
    ld a, $03
    ldh [$9d], a
    ldh [$70], a
    ld hl, $d008
    ld a, $ff
    ld b, 8
.blank:
    ld [hli], a
    dec b
    jr nz, .blank
    jr .done
.draw:
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl              ; hl = 128 * i
    ld de, AUTOLABEL_GFX
    add hl, de
    ld a, l
    ldh [$b8], a
    ld a, h
    ldh [$b9], a
    ld a, $23
    ldh [$ba], a
    xor a
    ldh [$bb], a
    ld a, $89
    ldh [$bc], a            ; VRAM $8900 = tile $90 (BG data at $8800)
    xor a
    ldh [$bd], a            ; VRAM bank 0
    ld bc, 8                ; count in tiles (0:1443; the init loads $100 tiles = 4 KB)
    call $1443
    ld a, $03
    ldh [$9d], a
    ldh [$70], a
    ld hl, $d008
    ld a, $90
    ld b, 8
.codes:
    ld [hli], a
    inc a
    dec b
    jr nz, .codes
.done:
    ld a, $04
    ldh [$9d], a
    ldh [$70], a
    ret
