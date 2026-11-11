; =====================================================================
; Wizardry Empire (GBC) - variable width font engine
; See docs/re/vwf.md for the design. Assembled by tools/asm.py.
; =====================================================================

VWF_BANK    equ $40

; ---- game addresses
FarCall     equ $c1a0          ; A = bank, HL = address
EnqueueDMA  equ $142a          ; (internal entry used by our stub)
hSVBK       equ $9d            ; ldh mirror of SVBK
hROMB       equ $9e            ; ldh mirror of ROM bank
hSrcLo      equ $b8
hSrcHi      equ $b9
hSrcBank    equ $ba
hDstLo      equ $bb
hDstHi      equ $bc
hDstVBank   equ $bd
qHead       equ $d004          ; WRAM bank 2: DMA queue head/tail, entries at $d400
qTail       equ $d005
twAttr      equ $c1c2
twCol       equ $c1c5
twRow       equ $c1c6
twBufLo     equ $c1d3
twBufHi     equ $c1d4

; ---- our WRAM: bank 7 $df00-$dfff (the shadows use $d000-$deff). Bank 7 is the engine's home bank:
; every entry point saves the caller's SVBK, switches to 7 and restores it on exit. Buffers (bank 3) and
; the cell map (bank 6) are only touched through Read3/Write3/Read6/Write6. (WRAM0 $ce00-$cfff is NOT
; free: it holds the stacks of the game's cooperative tasks, see docs/re/tasks.md.)
wLayout     equ $df00          ; 1 = split (codes $80+ in VRAM1:$9000), 0 = flat (VRAM0:$8800)
wReset      equ $df01          ; nonzero = clear allocation before next allocation
wNext       equ $df02          ; ring index into Pool
wTmp0       equ $df03
wTmp1       equ $df04
wTmp2       equ $df05
wTmp3       equ $df06
wSaveSVBK   equ $df07
; renderer state (active context)
S_px        equ $df10
S_slot      equ $df11
S_cellLo    equ $df12
S_cellHi    equ $df13
S_attr      equ $df14
S_col       equ $df15
S_imm       equ $df16          ; nonzero: commit after every glyph (typewriter)
S_cur       equ $df18          ; 8 bytes
S_nxt       equ $df20          ; 8 bytes
S_SIZE      equ $18
; typewriter persistent context
TW_ctx      equ $df30          ; S_SIZE bytes
TW_row      equ $df48
TW_rep      equ $df49
TW_baseLo   equ $df4a
TW_baseHi   equ $df4b
; rect parameters
R_w         equ $df50
R_h         equ $df51
R_tbank     equ $df52
R_tLo       equ $df53
R_tHi       equ $df54
R_row       equ $df55
R_mode      equ $df56          ; 0 = tiles only, 1 = tiles + attribute block
R_baseLo    equ $df57
R_baseHi    equ $df58
R_srcBank   equ $df59
R_srcLo     equ $df5a
R_srcHi     equ $df5b
R_end       equ $df5c
wBits       equ $df60          ; 32 bytes: allocation bitmap, bit per slot code
wValid      equ $dfa0          ; 32 bytes: shadow copy in WRAM7 matches VRAM
wUp         equ $df80          ; 16 bytes (16-aligned): HDMA source
wSkip       equ $df08          ; VWF_FontLoad result (returned in L)
wNameBuf    equ $dfc0          ; 32 bytes
wInL        equ $dfe0
wInH        equ $dfe1
wInBank     equ $dfe2
wInLo       equ $dfe3
wInHi       equ $dfe4
wInE        equ $dfe5
wInD        equ $dfe6
wFL_code    equ $dfe7
wFL_n       equ $dfe8
wFixN       equ $dfe9
wFixTB      equ $dfea
wCallerSVBK equ $dfeb
wCallerBank equ $dfec
wSPsave     equ $dfed          ; 2 bytes: caller SP while on the private stack
wPT         equ $dfef          ; 2 bytes: PrivCall target / HL on return
wPA         equ $dff1          ; PrivCall: A on return
wPanel      equ $dff2          ; nonzero: finished tiles go to the monster-panel bitmap (WRAM1)
wPanG       equ $dff3          ; monster panel: group 0-3
wPanW       equ $dff4          ; monster panel: width of the name / split index
wDmaLo      equ $dff5          ; VWF_DmaCheck: destination start, end (16-bit each), VRAM bank
wDmaHi      equ $dff6
wDmaEndLo   equ $dff7
wDmaEndHi   equ $dff8
wDmaV       equ $dff9
wDmaI       equ $dffa
wSkipCopy   equ $dffb          ; nonzero: the next VBlank skips the game's map copy (menus appear at once)
wHoldStart  equ $dffc          ; frame ($C00A) the current print burst started
wLastPrint  equ $dffd          ; frame of the last non-typewriter print
HOLD_MAX    equ 6              ; frames a burst may hold the screen
wKeepOff    equ $df09          ; nonzero: the pool ran dry in this burst, old-screen protection dropped
wKeep       equ $d2a0          ; 32 bytes (shadow area of codes $2A/$2B): slots in use when the burst began;
                               ; the old screen still shows them until the map copy, so GC keeps them
PRIV_SP     equ $cd80          ; private stack top (WRAM0 $CCE0-$CDD5 is never used by the game)
wGame       equ $d200          ; 32 bytes: slots holding game graphics (shadow area of codes $20/$21, not pool)
wSpell      equ $d280          ; 32 bytes: full English name of the last spell read by 0:24CF (shadow area of
                               ; codes $28/$29, not pool); messages print it with {F8 00 07 D280}
wMagic      equ $dffe          ; 'V','X' once initialised (bump when the variable layout changes)
HOME_BANK   equ 7

STAGING_BANK equ 7             ; WRAM bank 7 $d000 + code*16 = shadow of the VRAM tile
MAP_BANK    equ 6              ; WRAM bank 6: cellmap $d000-$d7ff, owners $d800 + code*2

; =====================================================================
; Bank 0 patches and stubs
; =====================================================================

; --- DMA enqueue: watch for the font's upper half being loaded to learn the layout
    org 0, $142a
    jp Stub_Enqueue

; --- typewriter character output (replaces 1c11-1c76)
; New control code $F2 bank lo hi: continue the message at bank:lo/hi (used to redirect
; every original message to its English text).
    org 0, $1c11
    cp $f2
    jr z, .jump
    push hl
    ld b, a
    ld a, VWF_BANK
    ld hl, TW_Char
    call FarCall
    pop hl
    jp $1bc7
.jump:
    ld a, [hli]
    ld b, a
    ld a, [hli]
    ld h, [hl]
    ld l, a
    ld a, b
    ld [$c1c1], a
    rst $28
    ld a, l
    ld [$c1bf], a
    ld a, h
    ld [$c1c0], a
    jp $1bc7

Stub_Fix:                   ; call Stub_Fix / db n: copy n chars from HL (current bank) to DE, via the VWF;
                            ; db n|$80, bank: the source is in that ROM bank
    push bc
    push hl
    ld hl, VWF_Fix
    jp StubCommon

Stub_TWInit:
    push hl
    ld a, VWF_BANK
    ld hl, VWF_TWInit
    call FarCall
    pop hl
    xor a
    ld [twCol], a
    ret
    assert @ <= $1c79, "typewriter stub overflow"

; --- {FA} word look-ahead (1c9a: ld a,[hli] / cp $fa / jr nc,$1d05): also stop at our $F2 jump, so the
;     jump bytes at the end of English text are not counted as part of the last word
    org 0, $1c9a
    call Stub_Measure
    jr nc, $1d05
    org 0, $3ff0
Stub_Measure:
    ld a, [hli]
    cp $f2
    jr z, .stop
    cp $fa                  ; carry = ordinary character
    ret
.stop:
    or a                    ; no carry = end of word
    ret
    assert @ <= $4000, "stub area 3 overflow"

; --- typewriter init: forget the previous message's VWF context
    org 0, $1b3f
    call Stub_TWInit
    nop

; --- rect blitters: tiles only (1770) / tiles + attributes (1723)
    org 0, $1770
    jp Stub_Rect0
    org 0, $1723
    jp Stub_Rect1
; --- attributes-only blitter (17a7): mask the VWF marker bit when reading w
    org 0, $17bd
    call Stub_ReadW

; --- $00-terminated name copy loops (ld a,[hli] / or a / jr z / ld [de],a / inc de / jr) -> VWF
    org $26, $4ca3
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $26, $5648
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $4529
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $49a3
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $529c
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $558e
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $67a3
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $6a66
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $6b50
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $7084
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2a, $57cd
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2a, $624e
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2a, $6f0e
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2a, $6f6f
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2b, $56fc
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2e, $57cd
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2e, $58c6
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop

; --- rst $38: inline text. Followed by db bank (bit 7: destination in HL, else DE), dw text.
    org 0, $0038
    jp Stub_Inline

; --- free space at $00b1-$00f0
    org 0, $00b1
Stub_Enqueue:              ; font from bank 1 $4400-$50ff? let the VWF decide (verdict in L)
    ldh a, [hSrcBank]
    dec a
    jr nz, Stub_EnqDma
    ldh a, [hSrcHi]
    cp $44
    jr c, Stub_EnqDma
    cp $51
    jr nc, Stub_EnqDma
    push bc
    ld a, VWF_BANK
    ld hl, VWF_FontLoad
    call FarCall
    pop bc
    ld a, l
    dec a
    ret z                   ; 1 = drop this load
    dec a
    jr nz, .go
    ld bc, 16               ; 2 = load only the 16 frame/arrow tiles
.go:
    ldh a, [hSVBK]
    push af
    ld a, $02
    jp $142f

Stub_ReadW:
    ld a, [hli]
    and $7f
    ld b, a
    ld a, [hli]
    ret

; Far byte fetch for the VWF bank: A = [B:HL+], returns with VWF bank mapped.
VWF_Fetch:
    ld a, b
    rst $28
    ld a, [hli]
    push af
    ld a, VWF_BANK
    rst $28
    pop af
    ret
Stub_EnqDma:
    jp Stub_Dma
    assert @ <= $00f1, "bank0 stub area 1 overflow"

; --- free space at $3f50-$3fd9
    org 0, $3f50
Stub_Rect0:
    ld c, 0
    jr Stub_RectCommon
Stub_Rect1:
    ld c, 1
Stub_RectCommon:            ; C = mode (0 tiles, 1 tiles + attributes), passed to VWF_Rect
    ldh a, [hROMB]
    push af
    ldh a, [hSrcBank]
    rst $28
    ldh a, [hSrcHi]
    ld h, a
    ldh a, [hSrcLo]
    ld l, a
    bit 7, [hl]
    jr nz, .vwf
    pop af
    rst $28
    ldh a, [hSVBK]          ; the three overwritten bytes (f0 9d 47)
    ld b, a
    bit 0, c
    jp z, $1773
    jp $1726
.vwf:
    pop af
    rst $28
    ld a, VWF_BANK
    ld hl, VWF_Rect
    jp FarCall              ; tail call: returns to the blitter's caller

Stub_PrintZ:                ; print the $00-terminated string at HL at cell DE; HL ends past the $00
    push bc
    push hl
    ld a, VWF_BANK
    ld hl, VWF_PrintZ
    call FarCall
    add sp, 2               ; drop the pushed HL (the VWF returns HL in the register)
    pop bc
    xor a
    ret

; VWF entry from here sees: [sp+0] FarCall return, [+2] caller ROM bank, [+3] return into StubCommon,
; [+5] caller HL, [+7] caller BC, [+9] the site's return address (= argument pointer, advanced by the VWF).
Stub_Inline:                ; rst $38 + db bank, dw text
    push bc
    push hl
    ld hl, VWF_Inline
StubCommon:
    ld a, VWF_BANK
    call FarCall
    add sp, 2
    pop bc
    ret

Stub_Dma:                   ; any other VBlank DMA: tell the VWF which tiles the game overwrites, then queue it
    push bc                 ; (0:142A clobbers HL itself; callers do not expect it kept)
    ld a, VWF_BANK
    ld hl, VWF_DmaCheck
    call FarCall
    pop bc
    dec l
    ret z                   ; L = 1: drop this load
    ldh a, [hSVBK]
    push af
    ld a, $02
    jp $142f

Stub_Hold:                  ; 0:167D in the VBlank map copy (SVBK = 3 here): skip the copies (and keep the
    ld a, HOME_BANK         ; request flags) while the VWF is printing a menu, see HoldMark
    ldh [$70], a
    ld a, [wSkipCopy]
    push af
    xor a
    ld [wSkipCopy], a
    ld a, 3
    ldh [$70], a
    pop af
    or a
    ld a, [$c48b]
    ret z
    add sp, 2
    jp $16e0

Stub_SpellPre:              ; 0:24CF entry (A = spell id): fetch the full English name, then the original start
    ld c, a
    push af
    ld a, VWF_BANK
    ld hl, VWF_SpellName
    call FarCall
    pop af
    ld l, a
    ld h, 0
    ret
    assert @ <= $3fda, "bank0 stub area 2 overflow"

; =====================================================================
; Bank $40: engine
; =====================================================================
    org VWF_BANK, $4000
FontAdv:
    incbin "../build/font_adv.bin"      ; 256 bytes
FontRows:
    incbin "../build/font_rows.bin"     ; 256 * 8 bytes
Pool:
    incbin "../build/pool.bin"          ; POOL_SIZE codes
PoolEnd:
PoolFlags:
    incbin "../build/poolflags.bin"     ; 256 bytes: nonzero = code is a VWF slot
POOL_SIZE   equ PoolEnd - Pool

; ---------------------------------------------------------------------
; Font upper-half load (called from Stub_Enqueue). Codes $80-$EF become VWF slots, so the
; kana are not loaded; codes $F0-$FF (cursor arrow, window frame) still are.
; wSkip: 0 = enqueue unchanged, 1 = drop, 2 = enqueue 16 tiles from the adjusted params.
VWF_FontLoad:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    xor a
    ld [wSkip], a
    ldh a, [hSrcLo]
    or a
    jr nz, .exit
    ldh a, [hSrcHi]
    cp $4c
    jr z, .hi
    cp $44
    jr z, .lo
    cp $48
    jr z, .lo
    cp $50
    jr nz, .exit
    ; $5000: codes $c0-$ff
    ldh a, [hDstVBank]
    or a
    jr z, .drop             ; flat layout loads only $c0-$ef here
    ld a, $53
    ldh [hSrcHi], a
    ldh a, [hDstHi]
    add 3
    ldh [hDstHi], a
    ld a, 2
    ld [wSkip], a
    jr .exit
.hi:
    ldh a, [hDstVBank]
    ld [wLayout], a         ; VRAM1:$9000 -> split (1), VRAM0:$8800 -> flat (0)
    or a
    jr z, .nb
    ; split: VRAM1 tile $20 (code $A0) = blank paper, see build.py POOL
    ld hl, wUp
    ld b, 8
.bt: xor a
    ld [hli], a
    dec a
    ld [hli], a
    dec b
    jr nz, .bt
    ld a, $a0
    call Upload
.nb:
    ld a, 1
    ld [wReset], a          ; new font = new screen: VRAM no longer matches the shadows
.drop:
    ld a, 1
    ld [wSkip], a
.exit:
    ld a, [wSkip]
    ld l, a
    pop af
    jp SetSVBK
.lo:                        ; 64 tiles from ROM1:hSrcHi00: copy the ones that are not pool slots
    ld a, 1
    ld [wReset], a
    ldh a, [hSrcHi]
    sub $44
    add a
    add a
    add a
    add a                   ; first code: 0 or $40
    ld [wFL_code], a
    ld a, 64
    ld [wFL_n], a
.fl:
    ld a, [wFL_code]
    ld e, a
    ld d, 0
    ld hl, PoolFlags
    add hl, de
    ld a, [hl]
    or a
    jr nz, .next
    ; source = ROM1:$4400 + code*16
    ld l, e
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    ld de, $4400
    add hl, de
    ld de, wUp
    ld b, 16
.cp:
    push bc
    ld b, 1
    call VWF_Fetch
    pop bc
    ld [de], a
    inc de
    dec b
    jr nz, .cp
    ld a, [wFL_code]
    call Upload
.next:
    ld hl, wFL_code
    inc [hl]
    ld hl, wFL_n
    dec [hl]
    jr nz, .fl
    jr .drop

; ---------------------------------------------------------------------
; SVBK helpers (keep the game's hSVBK mirror in sync). The engine runs with SVBK = HOME_BANK.
SetSVBK:                    ; A = bank
    ldh [hSVBK], a
    ldh [$70], a
    ret

Read3:                      ; A = [HL] in WRAM bank 3
    ld a, 3
    jr ReadBank
Read6:                      ; A = [HL] in WRAM bank 6
    ld a, MAP_BANK
ReadBank:
    ldh [hSVBK], a
    ldh [$70], a
    ld a, [hl]
    push af
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    pop af
    ret

Write3:                     ; [HL] = A in WRAM bank 3
    push af
    ld a, 3
    jr WriteBank
Write1:                     ; [HL] = A in WRAM bank 1
    push af
    ld a, 1
    jr WriteBank
Write6:                     ; [HL] = A in WRAM bank 6
    push af
    ld a, MAP_BANK
WriteBank:
    ldh [hSVBK], a
    ldh [$70], a
    pop af
    ld [hl], a
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret

; WRAM bank 7 is not cleared at power-on: zero the variables once (signature at wMagic).
CheckInit:
    ld a, [wMagic]
    cp $56
    jr nz, .init
    ld a, [wMagic + 1]
    cp $58
    ret z
.init:
    push hl
    push bc
    ld a, [wCallerSVBK]
    push af
    ld hl, $df00
    ld b, wMagic - $df00
    xor a
.z: ld [hli], a
    dec b
    jr nz, .z
    pop af
    ld [wCallerSVBK], a
    ld a, $56
    ld [wMagic], a
    ld a, $58
    ld [wMagic + 1], a
    ld a, 1
    ld [wReset], a          ; shadows are not valid yet
    pop bc
    pop hl
    ret

; Fetch [B:HL+] with the caller's WRAM bank mapped (strings may live in banked WRAM).
FetchSrc:
    ld a, [wCallerSVBK]
    ldh [hSVBK], a
    ldh [$70], a
    call VWF_Fetch
    push af
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    pop af
    ret

; ---------------------------------------------------------------------
; Context copy: HL = src, DE = dst, S_SIZE bytes
CopyCtx:
    ld b, S_SIZE
.l: ld a, [hli]
    ld [de], a
    inc de
    dec b
    jr nz, .l
    ret

; ---------------------------------------------------------------------
; Begin a run: HL = cell address (bank-3 buffer), A = base attribute
Begin:
    ld [S_attr], a
    ld a, l
    ld [S_cellLo], a
    ld a, h
    ld [S_cellHi], a
    xor a
    ld [S_px], a
    ld [S_slot], a
    ld [S_col], a
    ld hl, S_cur
    ld b, 16
.c: ld [hli], a
    dec b
    jr nz, .c
    ret

; ---------------------------------------------------------------------
; Draw glyph A into the context.
Glyph:
    ld e, a
    ld d, 0
    ld hl, FontAdv
    add hl, de
    ld a, [hl]
    ld [wTmp0], a           ; advance
    ; hl = FontRows + code*8
    ld h, d
    ld l, e
    add hl, hl
    add hl, hl
    add hl, hl
    ld de, FontRows
    add hl, de
    ld d, h
    ld e, l                 ; de = glyph rows
    ld hl, S_cur
    ld a, 8
    ld [wTmp1], a
.row:
    ld a, [de]
    inc de
    ld b, a
    ld c, 0
    ld a, [S_px]
    or a
    jr z, .ns
.sh:
    srl b
    rr c
    dec a
    jr nz, .sh
.ns:
    ld a, [hl]
    or b
    ld [hl], a
    push hl
    ld a, l
    add 8
    ld l, a                 ; S_nxt row (same page)
    ld a, [hl]
    or c
    ld [hl], a
    pop hl
    inc hl
    ld a, [wTmp1]
    dec a
    ld [wTmp1], a
    jr nz, .row
    ; advance
    ld a, [wTmp0]
    ld b, a
    ld a, [S_px]
    add b
    ld [S_px], a
    ld a, [S_imm]
    or a
    call nz, CommitIfInk
.adv:
    ld a, [S_px]
    cp 8
    ret c
    sub 8
    ld [S_px], a
    ld a, [S_imm]
    or a
    call z, CommitIfInk     ; tile complete (immediate mode already committed)
    call NextCell
    ld a, [S_imm]
    or a
    jr z, .adv
    call CommitIfInk        ; spill-over pixels visible right away
    jr .adv

; ---------------------------------------------------------------------
; Move to the next cell: cur <- nxt, nxt <- 0, slot <- 0
NextCell:
    ld hl, S_cellLo
    inc [hl]
    jr nz, .n
    inc hl
    inc [hl]
.n: ld hl, S_col
    inc [hl]
    xor a
    ld [S_slot], a
    ld hl, S_nxt
    ld de, S_cur
    ld b, 8
.c: ld a, [hl]
    ld [hli], a
    ld [de], a
    inc de
    dec b
    jr nz, .c
    ld hl, S_nxt
    ld b, 8
    xor a
.z: ld [hli], a
    dec b
    jr nz, .z
    ret

; ---------------------------------------------------------------------
; Commit the current tile if it has ink (or already owns a slot).
CommitIfInk:
    ld a, [wPanel]
    or a
    jp nz, PanelCommit
    ld a, [S_slot]
    or a
    jr nz, Commit
    ld hl, S_cur
    ld b, 8
    xor a
.o: or [hl]
    inc hl
    dec b
    jr nz, .o
    or a
    ret z
    ; fall through
Commit:
    ld a, [S_slot]
    or a
    jr nz, .have
    ld a, [S_imm]           ; typewriter: never reuse - the game scrolls by copying rows, so the
    or a                    ; slot this cell owned may now be shown by the row above
    jr nz, .new
    call CellSlot           ; reuse the slot this cell already shows (if it owns it)
    or a
    jr nz, .reuse
.new:
    call Alloc
    ld [S_slot], a
    call SetOwner
    jr .have
.reuse:
    ld [S_slot], a
    call KeptNow            ; the old screen still shows this slot (print burst): take a new one if one is
    jr z, .keep             ; free, else reuse it anyway (a short flicker beats overwriting other text)
    call AllocSoft
    jr c, .got
    ld a, 1                 ; pool full: stop protecting the old screen for the rest of this burst
    ld [wKeepOff], a
    jr .keep
.got:
    ld [S_slot], a
    call SetOwner
    jr .have
.keep:
    ld a, [S_slot]
    call MarkCode
.have:
    ; build the 2bpp tile in wUp (ink -> colour 3, paper -> colour 2, like the original font)
    ld hl, wUp
    ld de, S_cur
    ld b, 8
.s: ld a, [de]
    inc de
    ld [hli], a
    ld a, $ff
    ld [hli], a
    dec b
    jr nz, .s
    ; compare with / update the shadow copy (home bank 7); skip the upload if VRAM already has it
    ld a, [S_slot]
    call StagingAddr        ; hl = shadow
    ld de, wUp
    ld b, 16
    ld c, 0                 ; c = differences
.cmp:
    ld a, [de]
    inc de
    cp [hl]
    jr z, .eq
    inc c
    ld [hl], a
.eq:
    inc hl
    dec b
    jr nz, .cmp
    ld a, [S_slot]
    call ValidAddr          ; hl = byte, b = mask
    ld a, [hl]
    and b
    jr z, .up               ; shadow not valid for this screen
    ld a, c
    or a
    jr z, .cell
.up:
    ld a, [hl]
    or b
    ld [hl], a
    ld a, [S_slot]
    call Upload
.cell:
    ; write the cell (buffer in WRAM bank 3)
    ld a, [S_slot]
    call SlotTile           ; a = tile, c = bank bit
    ld b, a
    ld a, [S_cellLo]
    ld l, a
    ld a, [S_cellHi]
    ld h, a
    ld a, b
    call Write3
    ld de, $0400
    add hl, de
    ld a, [S_attr]
    and $f7
    or c
    jp Write3

; A = slot code -> HL = shadow address in WRAM bank 7 ($d000 + code*16)
StagingAddr:
    ld l, a
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    ld de, $d000
    add hl, de
    ret

; A = code -> HL = wValid + code/8, B = mask
ValidAddr:
    call BitAddr
    ld a, l
    add low(wValid) - low(wBits)
    ld l, a
    ret

; A = slot code -> A = tile number, C = attribute bank bit ($08 or 0)
SlotTile:
    ld c, 0
    bit 7, a
    ret z                   ; codes < $80: VRAM0:$9000 in both layouts
    ld b, a
    ld a, [wLayout]
    or a
    ld a, b
    ret z                   ; flat: tile = code, VRAM bank 0 ($8800+)
    and $7f
    ld c, $08               ; split: tile = code & $7f, VRAM bank 1 ($9000+)
    ret

; The slot this cell used last time (cellmap in WRAM bank 7), if the cell still owns it; else 0.
CellSlot:
    call CellMapAddr
    call Read6
    ld e, a
    ld d, 0
    ld hl, PoolFlags
    add hl, de
    ld a, [hl]
    or a
    ld a, e
    jr nz, CheckOwner
    xor a
    ret

; HL = cellmap entry (WRAM bank 6) for the current cell: buffer $d000-$d3ff -> $d000-$d3ff, $d800-$dbff -> $d400-$d7ff
CellMapAddr:
    ld a, [S_cellLo]
    ld l, a
    ld a, [S_cellHi]
    ld b, a
    and $03
    bit 3, b
    jr z, .a
    or $04
.a: or $d0
    ld h, a
    ret

; A = code. Returns A = code if owner[code] == current cell, else 0.
CheckOwner:
    ld [wTmp2], a
    call OwnerAddr
    call Read6
    ld b, a
    ld a, [S_cellLo]
    cp b
    jr nz, .x
    inc hl
    call Read6
    ld b, a
    ld a, [S_cellHi]
    cp b
    jr nz, .x
    ld a, [wTmp2]
    ret
.x: xor a
    ret

; owner[code] = current cell, cellmap[cell] = code (code in A)
SetOwner:
    ld [wTmp2], a
    call OwnerAddr
    ld a, [S_cellLo]
    call Write6
    inc hl
    ld a, [S_cellHi]
    call Write6
    call CellMapAddr
    ld a, [wTmp2]
    jp Write6

; A = code -> HL = owner entry in WRAM bank 6 ($d800 + code*2)
OwnerAddr:
    ld l, a
    ld h, 0
    add hl, hl
    ld de, $d800
    add hl, de
    ret

; ---------------------------------------------------------------------
; Upload wUp (16 bytes) to the VRAM tile of slot A.
; LCD on: one-block HBlank DMA started on a visible line (< 140) so it finishes long before
; VBlank; interrupts are masked while the DMA registers are set up. LCD off: CPU copy.
Upload:
    ld l, a
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl              ; code*16
    ld c, 0
    bit 7, a
    jr z, .lo
    ld a, [wLayout]
    or a
    jr z, .flat
    ld a, h
    and $07
    ld h, a
    ld de, $9000            ; VRAM1:$9000 + (code&$7f)*16
    add hl, de
    ld c, 1
    jr .go
.flat:
    ld de, $8000            ; VRAM0:$8800 + (code-$80)*16
    add hl, de
    jr .go
.lo:
    ld de, $9000            ; VRAM0:$9000 + code*16
    add hl, de
.go:
    ldh a, [$4f]
    push af
    ldh a, [$40]
    bit 7, a
    jr z, .off
.wly:
    ldh a, [$44]
    cp 140
    jr nc, .wly
    ldh a, [$ff]
    push af
    xor a
    ldh [$ff], a
    ld a, c
    ldh [$4f], a
    ld a, high(wUp)
    ldh [$51], a
    ld a, low(wUp)
    ldh [$52], a
    ld a, h
    ldh [$53], a
    ld a, l
    ldh [$54], a
    ld a, $80               ; 1 block, HBlank mode
    ldh [$55], a
.dw:
    ldh a, [$55]
    inc a
    jr nz, .dw
    pop af
    ldh [$ff], a
    pop af
    ldh [$4f], a
    ret
.off:
    ld a, c
    ldh [$4f], a
    ld de, wUp
    ld b, 16
.c: ld a, [de]
    inc de
    ld [hli], a
    dec b
    jr nz, .c
    pop af
    ldh [$4f], a
    ret

; ---------------------------------------------------------------------
; Allocation. Returns A = slot code.
; Alloc without the last resorts (no protection drop, no ring overwrite): carry + A = code, or no carry.
AllocSoft:
    call AllocReset
    call TryAlloc
    ret c
    call GC
    jp TryAlloc

Alloc:
    call AllocReset
    jr AllocScan

AllocReset:
    ld a, [wReset]
    or a
    ret z
    xor a
    ld [wReset], a
    ld hl, wValid
    ld b, 32
    xor a
.cv: ld [hli], a
    dec b
    jr nz, .cv
    ld hl, wGame            ; new screen (font load): the game's graphics no longer block slots
    ld b, 32
.cg: ld [hli], a
    dec b
    jr nz, .cg
    ret

AllocScan:
    call TryAlloc
    ret c
    call GC
    call TryAlloc
    ret c
    ld a, [wKeepOff]        ; still dry: drop the old-screen protection for this burst and try again
    or a
    jr nz, .ring
    inc a
    ld [wKeepOff], a
    call GC
    call TryAlloc
    ret c
.ring:
    ; everything referenced: overwrite the next ring entry
    ld a, [wNext]
    ld e, a
    ld d, 0
    ld hl, Pool
    add hl, de
    inc a
    cp POOL_SIZE
    jr c, .w
    xor a
.w: ld [wNext], a
    ld a, [hl]
    ret

; carry set + A = code on success
TryAlloc:
    ld a, [wNext]
    cp POOL_SIZE
    jr c, .ok
    xor a
    ld [wNext], a
.ok:
    ld a, POOL_SIZE
    ld [wTmp3], a
.l: ld a, [wNext]
    ld e, a
    ld d, 0
    ld hl, Pool
    add hl, de
    inc a
    cp POOL_SIZE
    jr c, .w
    xor a
.w: ld [wNext], a
    ld a, [hl]
    ld [wTmp2], a
    call BitAddr            ; hl = byte, b = mask
    ld a, [hl]
    and b
    jr nz, .used
    ld a, [hl]
    or b
    ld [hl], a
    ld a, [wTmp2]
    scf
    ret
.used:
    ld a, [wTmp3]
    dec a
    ld [wTmp3], a
    jr nz, .l
    and a
    ret

; A = code -> HL = wBits + code/8, B = 1 << (code&7)
BitAddr:
    ld c, a
    srl a
    srl a
    srl a
    add low(wBits)
    ld l, a
    ld h, high(wBits)
    ld a, c
    and 7
    ld b, 1
    jr z, .d
.s: sla b
    dec a
    jr nz, .s
.d: ret

ClearBits:
    ld hl, wBits
    ld b, 32
    xor a
.c: ld [hli], a
    dec b
    jr nz, .c
    ret

MarkCode:                   ; A = code
    call BitAddr
    ld a, [hl]
    or b
    ld [hl], a
    ret

; Call HL with SP on a private stack when the caller runs on a task stack ($CE00-$CFFF: 64 bytes per
; task, too small for the VWF; overflowing it corrupts the next task's frames). DE/BC go in, DE/HL/A
; come back (flags are not preserved). SVBK must be HOME_BANK (variables) on entry and on return.
PrivCall:
    ld a, l
    ld [wPT], a
    ld a, h
    ld [wPT + 1], a
    ld [wSPsave], sp
    ld a, [wSPsave + 1]
    cp $ce
    jr c, .go               ; main stack or already private: stay
    ld sp, PRIV_SP
    call .go
    ld [wPA], a             ; keep A
    ld a, l
    ld [wPT], a
    ld a, h
    ld [wPT + 1], a
    ld a, [wSPsave]
    ld l, a
    ld a, [wSPsave + 1]
    ld h, a
    ld sp, hl
    ld a, [wPT]
    ld l, a
    ld a, [wPT + 1]
    ld h, a
    ld a, [wPA]
    ret
.go:
    ld a, [wPT]
    ld l, a
    ld a, [wPT + 1]
    ld h, a
    jp hl

; =====================================================================
; Battle monster-group panel (replaces 0:199B, called from 22:5682 through a trampoline at 22:7F00).
; Names: 4 x 13 bytes at $C50F ($00 = end/empty). Each group owns 16 tiles in WRAM1 $D200 + $100*g:
; tiles 0-9 = row 1, tiles 10-15 = row 2 (the game's rects show them as $C0+16g.. with "(n) m" after).
; Names are drawn proportionally; a name wider than 80 px breaks at its last space that fits.
; Then the same DMA as the original: WRAM1 $D200 -> VRAM1 $8C00, $40 blocks, via 0:142A.
; =====================================================================
VWF_Panel:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    call HoldMark
    ld hl, PanelBody
    call PrivCall
    pop af
    jp SetSVBK

PanelBody:
    ; blank glyph pattern (two bytes) from the font, like the original
    ld b, 1
    ld hl, $43f0
    call VWF_Fetch
    ld d, a
    call VWF_Fetch
    ld e, a
    ld a, 1
    call SetSVBK
    ld hl, $d200
    ld bc, $0200
.fill:
    ld a, d
    ld [hli], a
    ld a, e
    ld [hli], a
    dec c
    jr nz, .fill
    dec b
    jr nz, .fill
    ld a, HOME_BANK
    call SetSVBK
    xor a
    ld [wPanG], a
.group:
    ; hl = $C50F + 13*g
    ld a, [wPanG]
    ld l, a
    ld h, 0
    ld d, h
    ld e, l
    add hl, hl
    add hl, de
    add hl, hl
    add hl, hl
    add hl, de
    ld de, $c50f
    add hl, de
    ; copy to wNameBuf (max 13), measure, find the split
    ld de, wNameBuf
    ld b, 13
.cp: ld a, [hli]
    ld [de], a
    inc de
    or a
    jr z, .cpe
    dec b
    jr nz, .cp
    xor a
    ld [de], a
.cpe:
    ld a, [wNameBuf]
    or a
    jr z, .next
    call PanelSplit         ; wPanW = index of the space to break at (0 = none)
    ld a, 1
    ld [wPanel], a
    ld hl, 0
    xor a
    call Begin
    xor a
    ld [S_imm], a
    ld hl, wNameBuf
    ld c, 0                 ; index
.ch: ld a, [hli]
    or a
    jr z, .end
    push hl
    push bc
    ld b, a
    ld a, [wPanW]
    or a
    jr z, .draw
    cp c
    jr nz, .draw
    ; break: flush row 1, continue at tile 10
    call PanelFlush
    ld hl, 0
    xor a
    call Begin
    ld a, 10
    ld [S_col], a
    pop bc
    pop hl
    inc c
    jr .ch
.draw:
    ld a, b
    call Glyph
    pop bc
    pop hl
    inc c
    jr .ch
.end:
    call PanelFlush
    xor a
    ld [wPanel], a
.next:
    ld a, [wPanG]
    inc a
    ld [wPanG], a
    cp 4
    jr c, .group
    ; DMA WRAM1 $D200 -> VRAM1 $8C00, $40 blocks (as 0:1A02-1A1D)
    ld a, $00
    ldh [$b8], a
    ld a, $d2
    ldh [$b9], a
    ld a, $01
    ldh [$ba], a
    ld a, $00
    ldh [$bb], a
    ld a, $8c
    ldh [$bc], a
    ld a, $01
    ldh [$bd], a
    ld bc, $0040
    jp $142a

; commit the partial tile if it has pixels
PanelFlush:
    ld a, [S_px]
    or a
    ret z
    jp PanelCommit

; wPanW = index of the space where a name wider than 80 px breaks (last space with prefix <= 80 px), else 0
PanelSplit:
    xor a
    ld [wPanW], a
    ld hl, wNameBuf
    ld bc, 0                ; b = width so far, c = index
.l: ld a, [hli]
    or a
    ret z
    cp $20
    jr nz, .w
    ld a, b
    cp 81
    jr nc, .w0
    ld a, c
    ld [wPanW], a
.w0:
    ld a, $20
.w: push hl
    ld e, a
    ld d, 0
    ld hl, FontAdv
    add hl, de
    ld a, [hl]
    pop hl
    add b
    ld b, a
    inc c
    jr .l

; Write the current tile (S_cur) to WRAM1 $D200 + $100*g + 16*col (col < 16): lo = ink, hi = $FF
PanelCommit:
    ld a, [S_col]
    cp 16
    ret nc
    swap a
    ld l, a
    ld a, [wPanG]
    add $d2
    ld h, a
    ld de, S_cur
    ld b, 8
.r: ld a, [de]
    inc de
    call Write1
    inc hl
    ld a, $ff
    call Write1
    inc hl
    dec b
    jr nz, .r
    ret

; =====================================================================
; A non-font VBlank DMA (pictures, panels) is about to overwrite VRAM [hDst, hDst + BC*16) in VRAM bank
; hDstVBank. Pool slots in that range lose their owner (no cell may reuse them) and their shadow copy
; (the next use uploads again). Fixes text drawn into the chest/bag pictures.
; =====================================================================
VWF_DmaCheck:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ; the kanji block 1:$4160 (26 tiles -> codes $D6-$EF, spell screens) is not needed in English (its
    ; labels are translated) and would overwrite VWF text: load only its last tile, the level cursor
    ; arrow ($EF, not a pool slot). Stack: [sp+7] = BC pushed by Stub_Dma (the tile count).
    ldh a, [hSrcBank]
    cp 1
    jr nz, .keep
    ldh a, [hSrcHi]
    cp $41
    jr nz, .keep
    ldh a, [hSrcLo]
    cp $60
    jr nz, .keep
    ld a, $f0
    ldh [hSrcLo], a
    ld a, $42
    ldh [hSrcHi], a
    ld a, $f0
    ldh [hDstLo], a
    ld a, $8e
    ldh [hDstHi], a
    ld hl, sp, 7
    ld a, 1
    ld [hli], a
    xor a
    ld [hl], a
    pop af
    call SetSVBK
    ld l, 0
    ret
.keep:
    ldh a, [hDstHi]
    cp $80
    jp c, .out
    cp $98
    jp nc, .out             ; not tile data
    ld [wDmaHi], a
    ld h, a
    ldh a, [hDstLo]
    ld [wDmaLo], a
    ld l, a
    ldh a, [hDstVBank]
    and 1
    ld [wDmaV], a
    ; end = dst + BC*16
    ld a, c
    ld e, a
    ld a, b
    ld d, a
    sla e
    rl d
    sla e
    rl d
    sla e
    rl d
    sla e
    rl d
    add hl, de
    ld a, l
    ld [wDmaEndLo], a
    ld a, h
    ld [wDmaEndHi], a
    xor a
    ld [wDmaI], a
.l: ld a, [wDmaI]
    ld e, a
    ld d, 0
    ld hl, Pool
    add hl, de
    ld a, [hl]
    ld [wTmp2], a
    ; c = VRAM bank, hl = tile address
    ld c, 0
    ld l, a
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl              ; code*16
    bit 7, a
    jr z, .low
    ld a, [wLayout]
    or a
    jr z, .flat
    inc c                   ; split: VRAM1 $9000 + (code & $7f)*16
    ld de, $9000 - $0800
    jr .add
.flat:
    ld de, $8000            ; flat: VRAM0 $8000 + code*16 ($8800-$8FFF)
    jr .add
.low:
    ld de, $9000
.add:
    add hl, de
    ld a, [wDmaV]
    cp c
    jr nz, .next
    ; hl >= start ?
    ld a, [wDmaLo]
    ld e, a
    ld a, [wDmaHi]
    ld d, a
    ld a, l
    sub e
    ld a, h
    sbc d
    jr c, .next
    ; hl < end ?
    ld a, [wDmaEndLo]
    ld e, a
    ld a, [wDmaEndHi]
    ld d, a
    ld a, l
    sub e
    ld a, h
    sbc d
    jr nc, .next
    ; disown + invalidate
    ld a, [wTmp2]
    call OwnerAddr
    xor a
    call Write6
    inc hl
    call Write6
    ld a, [wTmp2]
    call ValidAddr
    ld a, b
    cpl
    and [hl]
    ld [hl], a
    ld a, [wTmp2]
    call BitAddr
    ld a, [hl]
    or b
    ld [hl], a              ; in use now (wBits)
    ld a, l
    sub low(wBits)
    ld l, a
    ld h, high(wGame)
    ld a, l
    add low(wGame)
    ld l, a
    ld a, [hl]
    or b
    ld [hl], a              ; and kept through GC (wGame)
.next:
    ld a, [wDmaI]
    inc a
    ld [wDmaI], a
    cp POOL_SIZE
    jp c, .l
.out:
    pop af
    call SetSVBK
    ld l, 0
    ret

; NZ if slot [S_slot] was in use when the current print burst began and the burst's map copy is pending.
KeptNow:
    ; disabled: fresh slots for redrawn cells raised churn so much that screens the game restores from a saved
    ; copy (spell overview after the detail box) came back with reused tiles. Kept for reference.
    xor a
    ret
    ld a, [wKeepOff]
    or a
    jr nz, .no
    ld a, [wHoldStart]
    ld b, a
    ld a, [$c00a]
    sub b
    cp HOLD_MAX + 2
    jr nc, .no
    ld a, [S_slot]
    call BitAddr            ; hl = wBits + code/8, b = mask
    ld a, l
    add low(wKeep) - low(wBits)
    ld l, a
    ld h, high(wKeep)
    ld a, [hl]
    and b
    ret
.no:
    xor a
    ret

; Menus print over several frames; ask the VBlank handler to hold the game's map copy while a burst of
; prints lasts (at most HOLD_MAX frames; a frame without prints starts a new burst). Not for the typewriter.
HoldMark:
    ret                     ; disabled (2026-11-11): holding the map copy kept a half-overwritten old screen up
    push hl                 ; longer; protecting the old screen's slots broke screens restored from a copy
    ld a, [$c00a]           ; VBlank frame counter (WRAM0)
    ld h, a
    ld a, [wLastPrint]
    ld l, a
    ld a, h
    ld [wLastPrint], a
    sub l
    cp 2
    jr c, .same             ; printed in this or the previous frame: same burst
    ld a, h
    ld [wHoldStart], a
    xor a
    ld [wKeepOff], a
    push de
    push bc
    ld hl, wBits            ; new burst: remember what the screen shows now
    ld de, wKeep
    ld b, 32
.k: ld a, [hli]
    ld [de], a
    inc de
    dec b
    jr nz, .k
    pop bc
    pop de
    ld a, [$c00a]
    ld h, a
.same:
    ld a, [wHoldStart]
    ld l, a
    ld a, h
    sub l
    cp HOLD_MAX
    jr nc, .x
    ld a, 1
    ld [wSkipCopy], a
.x: pop hl
    ret

; =====================================================================
; Spells. VWF_SpellName (C = spell id): wSpell = full English name from SpellNames (bank, ptr per id; filled
; by tools/insert.py from script/spells.json), else the 11-byte record name (36:6C38 + 16*id).
; VWF_SpellList: print wSpell in the spell list row just blitted (hDst + 1 cell, after the castable marker).
; =====================================================================
VWF_SpellName:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ld l, c
    ld h, 0
    ld d, h
    ld e, l
    add hl, hl
    add hl, de              ; id*3
    ld de, SpellNames
    add hl, de
    ld a, [hli]
    or a
    jr z, .rec
    ld b, a
    ld a, [hli]
    ld h, [hl]
    ld l, a
    ld c, 31
    jr .copy
.rec:
    ld l, c
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    ld de, $6c38
    add hl, de
    ld b, 36
    ld c, 11
.copy:
    ld de, wSpell
.cl: call VWF_Fetch
    ld [de], a
    inc de
    or a
    jr z, .done
    dec c
    jr nz, .cl
    xor a
    ld [de], a
.done:
    pop af
    jp SetSVBK

VWF_SpellList:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    call HoldMark
    ld hl, wSpell
    ld de, wNameBuf
.c: ld a, [hli]
    ld [de], a
    inc de
    or a
    jr nz, .c
    ldh a, [hDstLo]
    ld e, a
    ldh a, [hDstHi]
    ld d, a
    inc de
    ld hl, VWF_PrintBuf
    call PrivCall
    pop af
    jp SetSVBK

; Rebuild the bitmap from what the bank-3 buffers reference.
GC:
    ; start from the slots the game just loaded graphics into (DMA seen, cells maybe not written yet);
    ; reservations last one GC: after that the picture's own cells keep them marked
    ld hl, wGame
    ld de, wBits
    ld b, 32
.gb: ld a, [hl]
    ld [de], a
    xor a
    ld [hli], a
    inc de
    dec b
    jr nz, .gb
    ; during a print burst (map copy pending) the old screen's slots stay reserved - disabled with HoldMark
    jr .nk
    ld a, [wHoldStart]
    ld b, a
    ld a, [$c00a]
    sub b
    cp HOLD_MAX + 2
    jr nc, .nk
    ld a, [wKeepOff]
    or a
    jr nz, .nk
    ld hl, wKeep
    ld de, wBits
    ld b, 32
.kb: ld a, [de]
    or [hl]
    ld [de], a
    inc hl
    inc de
    dec b
    jr nz, .kb
.nk:
    ld a, [S_slot]
    or a
    call nz, MarkCode
    ld a, [TW_ctx + 1]
    or a
    call nz, MarkCode
    ld hl, $d000
    call .scan
    ; the window buffer only counts while the window is on screen (battle hides the party list
    ; with WX=167 and re-sends/redraws it before showing it again)
    ldh a, [$ff40]
    bit 3, a                ; BG shows the $9C00 map (= this buffer, e.g. camp spell screens)
    jr nz, .win
    bit 5, a
    ret z
    ldh a, [$ff4b]
    cp 167
    ret nc
    ldh a, [$ff4a]
    cp 144
    ret nc
.win:
    ld hl, $d800
.scan:                      ; 18 rows x 32 cells at HL (bank 3; what the game's GDMA copies), attributes at HL+$400
    ld bc, 18*32
.l: push bc
    push hl
    call Read3
    ld e, a
    ld bc, $0400
    add hl, bc
    call Read3
    ld d, a                 ; attr
    ; current layout as before; the other layout's reading counts only for cells that own the slot (a font
    ; load can switch the layout while text drawn under the other one is still on screen: battle spell list)
    ld a, [wLayout]
    or a
    jr z, .flat
    bit 3, d                ; split
    ld a, e
    jr z, .s0
    cp $70
    jr nc, .skip
    or $80
    jr .mk
.s0: bit 7, a
    jr z, .mk               ; low codes: same in both layouts
    jr .other               ; VRAM0 $8800 code: flat reading
.flat:
    bit 3, d
    ld a, e
    jr z, .mk
    cp $70
    jr nc, .skip
    or $80                  ; VRAM1 tile: split reading
.other:
    ld [wTmp2], a
    ld a, h
    sub 4
    ld b, a                 ; bc = cell address (bc is free here: pushed above)
    ld c, l
    ld a, [wTmp2]
    call OwnerAddr
    call Read6
    cp c
    jr nz, .skip
    inc hl
    call Read6
    cp b
    jr nz, .skip
    ld a, [wTmp2]
.mk:
    call MarkCode
.skip:
    pop hl
    inc hl
    pop bc
    dec bc
    ld a, b
    or c
    jr nz, .l
    ret

; =====================================================================
; Typewriter entry (from 0:1c11). B = character. Caller saved HL.
; =====================================================================
TW_Char:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ld a, b
    ld [wTmp3], a
    ld hl, TWBody
    call PrivCall
    pop af
    jp SetSVBK

TWBody:
    ; resync if the game moved the cursor
    ld a, [twRow]
    ld hl, TW_row
    cp [hl]
    jr nz, .resync
    ld a, [twCol]
    ld hl, TW_rep
    cp [hl]
    jr nz, .resync
    ld a, [twBufLo]
    ld hl, TW_baseLo
    cp [hl]
    jr nz, .resync
    ld a, [twBufHi]
    ld hl, TW_baseHi
    cp [hl]
    jr z, .cont
.resync:
    ld a, [twBufLo]
    ld [TW_baseLo], a
    ld a, [twBufHi]
    ld [TW_baseHi], a
    ld a, [twRow]
    ld [TW_row], a
    ; cell = buf + row*32 + col
    ld l, a
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    ld a, [twCol]
    ld e, a
    ld d, 0
    add hl, de
    ld a, [twBufLo]
    ld e, a
    ld a, [twBufHi]
    ld d, a
    add hl, de
    ld a, [twAttr]
    call Begin
    ld a, [twCol]
    ld [S_col], a
    ld a, 1
    ld [S_imm], a
    jr .draw
.cont:
    ld hl, TW_ctx
    ld de, S_px
    call CopyCtx
.draw:
    ld a, [twAttr]
    and $f7
    ld [S_attr], a
    ld [twAttr], a
    ld a, [wTmp3]
    call Glyph
    ; report the column the game should see
    ld a, [S_px]
    or a
    ld a, [S_col]
    jr z, .r
    inc a
.r: ld [twCol], a
    ld [TW_rep], a
    ld hl, S_px
    ld de, TW_ctx
    jp CopyCtx

; =====================================================================
; Rect entry (from bank-0 stub, tail-called through FarCall).
; Source header at [hSrcBank]:[hSrcHi/Lo]: [w|$80] [h] [text bank] [ptr lo] [ptr hi]
; Text: rows separated by $FD, end $FF, $FC n = move to pixel n of the row.
; =====================================================================
VWF_Rect:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    call HoldMark
    ld a, c
    ld [R_mode], a
    ldh a, [hSrcBank]
    ld [R_srcBank], a
    ld b, a
    ldh a, [hSrcLo]
    ld l, a
    ldh a, [hSrcHi]
    ld h, a
    call VWF_Fetch
    and $7f
    ld [R_w], a
    call VWF_Fetch
    ld [R_h], a
    call VWF_Fetch
    ld [R_tbank], a
    call VWF_Fetch
    ld [R_tLo], a
    call VWF_Fetch
    ld [R_tHi], a
    ; attribute block (mode 1) starts at src + 2 + w*h
    ldh a, [hSrcLo]
    ld l, a
    ldh a, [hSrcHi]
    ld h, a
    inc hl
    inc hl
    ld a, [R_h]
    ld c, a
    ld a, [R_w]
    ld e, a
    ld d, 0
.mul:
    add hl, de
    dec c
    jr nz, .mul
    ; use the attribute of each row's LAST cell: for blocks of only 2 cells the first attribute byte
    ; is overwritten by the 5-byte VWF header, the last one never is
    ld a, [R_w]
    dec a
    ld e, a
    ld d, 0
    add hl, de
    ld a, l
    ld [R_srcLo], a
    ld a, h
    ld [R_srcHi], a
    ldh a, [hDstLo]
    ld [R_baseLo], a
    ldh a, [hDstHi]
    ld [R_baseHi], a
    xor a
    ld [R_row], a
    ld [R_end], a
    ld [S_imm], a
    ld hl, RectRows
    call PrivCall
    pop af
    jp SetSVBK

RectRows:
.rowloop:
    ; base attribute for the row
    ld a, [R_mode]
    or a
    jr z, .attrbuf
    ld a, [R_srcBank]
    ld b, a
    ld a, [R_srcLo]
    ld l, a
    ld a, [R_srcHi]
    ld h, a
    call VWF_Fetch
    ld c, a
    ; advance attribute pointer by w
    ld a, [R_srcLo]
    ld l, a
    ld a, [R_srcHi]
    ld h, a
    ld a, [R_w]
    ld e, a
    ld d, 0
    add hl, de
    ld a, l
    ld [R_srcLo], a
    ld a, h
    ld [R_srcHi], a
    ld a, c
    jr .gotattr
.attrbuf:
    ld a, [R_baseLo]
    ld l, a
    ld a, [R_baseHi]
    ld h, a
    ld de, $0400
    add hl, de
    call Read3
.gotattr:
    ld [wTmp3], a
    ld a, [R_baseLo]
    ld l, a
    ld a, [R_baseHi]
    ld h, a
    ld a, [wTmp3]
    call Begin
    ld a, [R_end]
    or a
    jp nz, .fill
.chr:
    ld a, [R_tbank]
    ld b, a
    ld a, [R_tLo]
    ld l, a
    ld a, [R_tHi]
    ld h, a
    call VWF_Fetch
    ld c, a
    ld a, l
    ld [R_tLo], a
    ld a, h
    ld [R_tHi], a
    ld a, c
    cp $ff
    jr z, .eot
    cp $fd
    jr z, .eol
    cp $fc
    jr z, .setx
    call Glyph
    jr .chr
.setx:
    ld a, [R_tbank]
    ld b, a
    ld a, [R_tLo]
    ld l, a
    ld a, [R_tHi]
    ld h, a
    call VWF_Fetch
    ld c, a
    ld a, l
    ld [R_tLo], a
    ld a, h
    ld [R_tHi], a
    ; same cell: just move px forward; else finish this cell, blank up to col n/8
    ld a, c
    srl a
    srl a
    srl a
    ld hl, S_col
    cp [hl]
    jr z, .sx2
    jr c, .chr              ; never move left
    push bc
    call CommitIfInk
    ld a, [S_slot]
    or a
    jr nz, .sxn
    ld a, [S_px]
    or a
    jr z, .sx1
.sxn:
    call NextCell
.sx1:
    pop bc
    push bc
    ld a, c
    srl a
    srl a
    srl a
    ld hl, S_col
    cp [hl]
    jr z, .sx3
    jr c, .sx3
    call NextCellBlank
    jr .sx1
.sx3:
    pop bc
.sx2:
    ld a, c
    and 7
    ld hl, S_px
    cp [hl]
    jp c, .chr
    ld [hl], a
    jp .chr
.eot:
    ld a, 1
    ld [R_end], a
.eol:
    call CommitIfInk
    ld a, [S_slot]
    or a
    jr nz, .adv1
    ld a, [S_px]
    or a
    jr z, .fill
.adv1:
    call NextCell
.fill:                      ; blank the rest of the row
    ld a, [S_col]
    ld hl, R_w
    cp [hl]
    jr nc, .nextrow
    call NextCellBlank
    jr .fill
.nextrow:
    ld a, [R_baseLo]
    add 32
    ld [R_baseLo], a
    jr nc, .nc
    ld a, [R_baseHi]
    inc a
    ld [R_baseHi], a
.nc:
    ld a, [R_row]
    inc a
    ld [R_row], a
    ld hl, R_h
    cp [hl]
    jp c, .rowloop
    ret

; Fixed-length copy (Stub_Fix). Looks the source address up in FixMap (entries: src bank, src lo, src hi,
; text bank, text lo, text hi; $FF ends); prints the English if found, else the raw bytes.
; Returns DE and wInL/H advanced by n-1 like the original unrolled copy.
VWF_Fix:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    call HoldMark
    ld a, e
    ld [wInE], a
    ld a, d
    ld [wInD], a
    ld hl, sp, 4            ; caller ROM bank = source bank
    ld a, [hl]
    ld [wInBank], a
    ld [wCallerBank], a
    ld hl, sp, 7            ; caller HL = source
    ld a, [hli]
    ld [wInL], a
    ld a, [hl]
    ld [wInH], a
    ld hl, sp, 11           ; argument pointer -> n
    ld a, [hli]
    ld h, [hl]
    ld l, a
    ld a, [wInBank]
    ld b, a
    call VWF_Fetch
    bit 7, a                ; n | $80: the next argument byte is the source ROM bank (far table)
    jr z, .n
    and $7f
    ld [wFixN], a
    ld a, [wInBank]
    ld b, a
    call VWF_Fetch
    ld [wInBank], a
    ld a, [wFixN]
.n: ld [wFixN], a
    ld d, h
    ld e, l
    ld hl, sp, 11
    ld a, e
    ld [hli], a
    ld [hl], d
    ld a, [wInE]
    ld e, a
    ld a, [wInD]
    ld d, a
    ld hl, FixBody
    call PrivCall
    ld a, [wInL]
    ld l, a
    ld a, [wInH]
    ld h, a
    pop af
    jp SetSVBK

FixBody:
    ; blank the n destination cells first (English is often shorter than the field); screen buffers only
    ld a, [wInD]
    cp $d0
    jr c, .nb
    cp $dc
    jr nc, .nb
    ld h, a
    ld a, [wInE]
    ld l, a
    ld a, [wFixN]
    ld c, a
.bl:
    ld a, $20
    call Write3
    push hl
    ld de, $0400
    add hl, de
    call Read3
    and $f7
    call Write3
    pop hl
    inc hl
    dec c
    jr nz, .bl
.nb:
    ld a, [wInE]
    ld e, a
    ld a, [wInD]
    ld d, a
    ld hl, FixMap
.f: ld a, [hli]
    cp $ff
    jr z, .raw
    ld b, a
    ld a, [wInBank]
    cp b
    jr nz, .n2
    ld a, [wInL]
    cp [hl]
    jr nz, .n2
    inc hl
    ld a, [wInH]
    cp [hl]
    jr nz, .n1
    inc hl
    ld a, [hli]
    ld [wFixTB], a
    ld a, [hli]
    ld [wInLo], a
    ld a, [hl]
    ld [wInHi], a
    ld a, [wInBank]
    push af
    ld a, [wFixTB]
    ld [wInBank], a         ; DE destination (bit 7 clear)
    call InlineBody
    pop af
    ld [wInBank], a
    jr .done
.n2: inc hl
.n1: inc hl
    inc hl
    inc hl
    inc hl
    jr .f
.raw:
    ld a, [wInBank]
    ld b, a
    ld a, [wInL]
    ld l, a
    ld a, [wInH]
    ld h, a
    ld de, wNameBuf
    ld a, [wFixN]
    ld c, a
.r: call FetchSrc
    ld [de], a
    inc de
    dec c
    jr nz, .r
    xor a
    ld [de], a
    ld a, [wInE]
    ld e, a
    ld a, [wInD]
    ld d, a
    call VWF_PrintBuf
.done:
    ld a, [wFixN]
    dec a
    ld c, a
    ld b, 0
    ld a, [wInE]
    ld l, a
    ld a, [wInD]
    ld h, a
    add hl, bc
    ld d, h
    ld e, l
    ld a, [wInL]
    ld l, a
    ld a, [wInH]
    ld h, a
    add hl, bc
    ld a, l
    ld [wInL], a
    ld a, h
    ld [wInH], a
    ret

; Inline text (rst $38): copy [wInBank&$7f]:[wInHi/Lo] ($FF or $00 terminated) to wNameBuf, print at DE.
; For HL-destination sites the caller's DE is kept in wInE/wInD.
VWF_Inline:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    call HoldMark
    ld a, e
    ld [wInE], a
    ld a, d
    ld [wInD], a
    ld hl, sp, 4
    ld a, [hl]
    ld [wCallerBank], a
    ld hl, sp, 7            ; caller HL
    ld a, [hli]
    ld [wInL], a
    ld a, [hl]
    ld [wInH], a
    ld hl, sp, 11           ; argument pointer -> db bank, dw text
    ld a, [hli]
    ld h, [hl]
    ld l, a
    ld a, [wCallerBank]
    ld b, a
    call VWF_Fetch
    ld [wInBank], a
    call VWF_Fetch
    ld [wInLo], a
    call VWF_Fetch
    ld [wInHi], a
    ld d, h
    ld e, l
    ld hl, sp, 11
    ld a, e
    ld [hli], a
    ld [hl], d
    ld hl, InlineBody
    call PrivCall
    ld a, [wInL]
    ld l, a
    ld a, [wInH]
    ld h, a
    pop af
    jp SetSVBK

; Copy [wInBank&$7f]:[wInHi/Lo] to wNameBuf and print it at wInE/D (bit 7 of wInBank: at wInL/H).
InlineBody:
    ld a, [wInBank]
    and $7f
    ld b, a
    ld a, [wInLo]
    ld l, a
    ld a, [wInHi]
    ld h, a
    ld c, low(wNameBuf)
.c: call VWF_Fetch
    cp $ff
    jr nz, .s
    xor a
.s: push af
    push hl
    ld h, high(wNameBuf)
    ld l, c
    ld [hl], a
    pop hl
    inc c
    pop af
    or a
    jr nz, .c
    ld a, [wInBank]
    bit 7, a
    jr z, .de
    ld a, [wInL]            ; destination in HL
    ld e, a
    ld a, [wInH]
    ld d, a
    call VWF_PrintBuf
    ld a, e
    ld [wInL], a
    ld a, d
    ld [wInH], a
    ld a, [wInE]
    ld e, a
    ld a, [wInD]
    ld d, a
    ret
.de:
    ld a, [wInE]
    ld e, a
    ld a, [wInD]
    ld d, a
    jp VWF_PrintBuf

; Stub_PrintZ entry: the string at caller HL (caller ROM/WRAM bank) printed at DE; returns HL past the $00.
VWF_PrintZ:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    call HoldMark
    ld hl, sp, 4
    ld b, [hl]              ; caller ROM bank
    ld hl, sp, 7
    ld a, [hli]
    ld h, [hl]
    ld l, a
    ld c, low(wNameBuf)
.c: call FetchSrc
    push hl
    ld h, high(wNameBuf)
    ld l, c
    ld [hl], a
    pop hl
    inc c
    or a
    jr nz, .c
    push hl
    ld hl, VWF_PrintBuf
    call PrivCall
    pop hl
    pop af
    jp SetSVBK

VWF_TWInit:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ld a, $ff
    ld [TW_row], a
    pop af
    jp SetSVBK

; Print the $00-terminated string in wNameBuf at cell DE (bank-3 buffer); returns DE after it.
VWF_PrintBuf:
    ld h, d
    ld l, e
    push hl
    ld bc, $0400
    add hl, bc
    call Read3
    pop hl
    call Begin
    xor a
    ld [S_imm], a
    ld hl, wNameBuf
.l: ld a, [hli]
    or a
    jr z, .e
    push hl
    call Glyph
    pop hl
    jr .l
.e: call CommitIfInk
    ld a, [S_slot]
    or a
    jr nz, .adv
    ld a, [S_px]
    or a
    jr z, .done
.adv:
    call NextCell
.done:
    ld a, [S_cellLo]
    ld e, a
    ld a, [S_cellHi]
    ld d, a
    ret

; Write a space tile into the current cell (bank 0 tile $20), then NextCell.
NextCellBlank:
    ld a, [S_cellLo]
    ld l, a
    ld a, [S_cellHi]
    ld h, a
    ld a, $20
    call Write3
    ld de, $0400
    add hl, de
    ld a, [S_attr]
    and $f7
    call Write3
    jp NextCell

; Address-keyed English for fixed-length copies; filled in by tools/build.py after assembly.
SpellNames:                 ; 125 x [bank][lo][hi], filled by tools/insert.py (bank 0 = use the record)
    ds 125*3, $00
FixMap:
    ds 6 * 600, $ff
