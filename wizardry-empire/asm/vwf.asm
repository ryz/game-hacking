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

; ---- our WRAM (bank 0 region $cf00-$cfff is unused by the game; stack lives below $cf00)
wLayout     equ $cf00          ; 1 = split (codes $80+ in VRAM1:$9000), 0 = flat (VRAM0:$8800)
wReset      equ $cf01          ; nonzero = clear allocation before next allocation
wNext       equ $cf02          ; ring index into Pool
wTmp0       equ $cf03
wTmp1       equ $cf04
wTmp2       equ $cf05
wTmp3       equ $cf06
wSaveSVBK   equ $cf07
; renderer state (active context)
S_px        equ $cf10
S_slot      equ $cf11
S_cellLo    equ $cf12
S_cellHi    equ $cf13
S_attr      equ $cf14
S_col       equ $cf15
S_imm       equ $cf16          ; nonzero: commit after every glyph (typewriter)
S_cur       equ $cf18          ; 8 bytes
S_nxt       equ $cf20          ; 8 bytes
S_SIZE      equ $18
; typewriter persistent context
TW_ctx      equ $cf30          ; S_SIZE bytes
TW_row      equ $cf48
TW_rep      equ $cf49
TW_baseLo   equ $cf4a
TW_baseHi   equ $cf4b
; rect parameters
R_w         equ $cf50
R_h         equ $cf51
R_tbank     equ $cf52
R_tLo       equ $cf53
R_tHi       equ $cf54
R_row       equ $cf55
R_mode      equ $cf56          ; 0 = tiles only, 1 = tiles + attribute block
R_baseLo    equ $cf57
R_baseHi    equ $cf58
R_srcBank   equ $cf59
R_srcLo     equ $cf5a
R_srcHi     equ $cf5b
R_end       equ $cf5c
wBits       equ $cf60          ; 32 bytes: allocation bitmap, bit per slot code
wValid      equ $cfa0          ; 32 bytes: shadow copy in WRAM7 matches VRAM
wUp         equ $cf80          ; 16 bytes (16-aligned): HDMA source
wSkip       equ $cf08
wNameBuf    equ $cfc0          ; 32 bytes

STAGING_BANK equ 7             ; WRAM bank 7 $d000 + code*16 = staged 2bpp tile

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
    assert @ <= $1c79, "typewriter stub overflow"

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

; --- free space at $00b1-$00f0
    org 0, $00b1
Stub_Enqueue:              ; font upper half (bank 1 $4c00/$5000)? let the VWF decide
    ldh a, [hSrcBank]
    dec a
    jr nz, .go
    ldh a, [hSrcHi]
    cp $4c
    jr z, .font
    cp $50
    jr nz, .go
.font:
    push bc
    ld a, VWF_BANK
    ld hl, VWF_FontLoad
    call FarCall
    pop bc
    ld a, [wSkip]
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
    assert @ <= $00f1, "bank0 stub area 1 overflow"

; --- free space at $3f50-$3fd9
    org 0, $3f50
Stub_Rect0:
    xor a
    jr Stub_RectCommon
Stub_Rect1:
    ld a, 1
Stub_RectCommon:
    ld [R_mode], a
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
    ld a, [R_mode]
    or a
    jp z, $1773
    jp $1726
.vwf:
    pop af
    rst $28
    ld a, VWF_BANK
    ld hl, VWF_Rect
    jp FarCall              ; tail call: returns to the blitter's caller

Stub_PrintZ:                ; copy the string at HL to wNameBuf, print it at DE with the VWF
    push bc
    ld bc, wNameBuf
.c: ld a, [hli]
    ld [bc], a
    inc c
    or a
    jr nz, .c
    push hl
    ld a, VWF_BANK
    ld hl, VWF_PrintBuf
    call FarCall
    pop hl
    pop bc
    xor a
    ret

Stub_TWInit:
    ld a, $ff
    ld [TW_row], a
    xor a
    ld [twCol], a
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
POOL_SIZE   equ PoolEnd - Pool

; ---------------------------------------------------------------------
; Font upper-half load (called from Stub_Enqueue). Codes $80-$EF become VWF slots, so the
; kana are not loaded; codes $F0-$FF (cursor arrow, window frame) still are.
; wSkip: 0 = enqueue unchanged, 1 = drop, 2 = enqueue 16 tiles from the adjusted params.
VWF_FontLoad:
    xor a
    ld [wSkip], a
    ldh a, [hSrcLo]
    or a
    ret nz
    ldh a, [hSrcHi]
    cp $4c
    jr z, .hi
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
    ret
.hi:
    ldh a, [hDstVBank]
    ld [wLayout], a         ; VRAM1:$9000 -> split (1), VRAM0:$8800 -> flat (0)
    ld a, 1
    ld [wReset], a          ; new font = new screen: VRAM no longer matches the shadows
.drop:
    ld a, 1
    ld [wSkip], a
    ret

; ---------------------------------------------------------------------
; SVBK helpers (keep the game's hSVBK mirror in sync)
SetSVBK:                    ; A = bank
    ldh [hSVBK], a
    ldh [$70], a
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
    call CellSlot           ; reuse the slot this cell already shows (if it owns it)
    or a
    jr nz, .reuse
    call Alloc
    ld [S_slot], a
    call SetOwner
    jr .have
.reuse:
    ld [S_slot], a
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
    ; compare with / update the shadow copy in WRAM bank 7; skip the upload if VRAM already has it
    ldh a, [hSVBK]
    ld [wSaveSVBK], a
    ld a, STAGING_BANK
    call SetSVBK
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
    ld a, [wSaveSVBK]
    call SetSVBK
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
    ld a, 3
    call SetSVBK
    ld a, [S_slot]
    call SlotTile           ; a = tile, c = bank bit
    ld b, a
    ld a, [S_cellLo]
    ld l, a
    ld a, [S_cellHi]
    ld h, a
    ld [hl], b
    ld de, $0400
    add hl, de
    ld a, [S_attr]
    and $f7
    or c
    ld [hl], a
    ld a, [wSaveSVBK]
    jp SetSVBK

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
    ldh a, [hSVBK]
    push af
    ld a, STAGING_BANK
    call SetSVBK
    ld a, [hl]
    ld [wTmp2], a
    pop af
    call SetSVBK
    ld a, [wTmp2]
    cp $80
    jr c, .no
    cp $f0
    jr c, CheckOwner
.no:
    xor a
    ret

; HL = cellmap entry for the current cell: buffer $d000-$d3ff -> $d000-$d3ff, $d800-$dbff -> $d400-$d7ff
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
    ldh a, [hSVBK]
    push af
    ld a, STAGING_BANK
    call SetSVBK
    ld a, [S_cellLo]
    cp [hl]
    jr nz, .x
    inc hl
    ld a, [S_cellHi]
    cp [hl]
    jr nz, .x
    pop af
    call SetSVBK
    ld a, [wTmp2]
    ret
.x: pop af
    call SetSVBK
    xor a
    ret

; owner[code] = current cell, cellmap[cell] = code (code in A)
SetOwner:
    ld [wTmp2], a
    call OwnerAddr
    ldh a, [hSVBK]
    push af
    ld a, STAGING_BANK
    call SetSVBK
    ld a, [S_cellLo]
    ld [hli], a
    ld a, [S_cellHi]
    ld [hl], a
    call CellMapAddr
    ld a, [wTmp2]
    ld [hl], a
    pop af
    jp SetSVBK

; A = code ($80-$ef) -> HL = owner entry in WRAM bank 7 ($df00 + (code-$80)*2)
OwnerAddr:
    sub $80
    add a
    ld l, a
    ld h, $df
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
    add hl, hl              ; code*16 ($800-$eff)
    ld c, 0
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
Alloc:
    ld a, [wReset]
    or a
    jr z, .scan
    xor a
    ld [wReset], a
    ld hl, wValid
    ld b, 32
    xor a
.cv: ld [hli], a
    dec b
    jr nz, .cv
.scan:
    call TryAlloc
    ret c
    call GC
    call TryAlloc
    ret c
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

; Rebuild the bitmap from what the bank-3 buffers reference.
GC:
    call ClearBits
    ld a, [S_slot]
    or a
    call nz, MarkCode
    ld a, [TW_ctx + 1]
    or a
    call nz, MarkCode
    ldh a, [hSVBK]
    push af
    ld a, 3
    call SetSVBK
    ld hl, $d000
    call .scan
    ld hl, $d800
    call .scan
    pop af
    jp SetSVBK
.scan:                      ; 1024 cells at HL, attributes at HL+$400
    ld bc, $0400
.l: push bc
    push hl
    ld e, [hl]
    ld bc, $0400
    add hl, bc
    ld a, [hl]
    ld d, a                 ; attr
    ld a, [wLayout]
    or a
    jr z, .flat
    bit 3, d
    ld a, e
    jr z, .mk
    or $80
    jr .mk
.flat:
    bit 3, d
    jr nz, .skip
    ld a, e
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
    ld a, b
    ld [wTmp3], a
    ldh a, [hSVBK]
    push af
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
    call CopyCtx
    pop af
    jp SetSVBK

; =====================================================================
; Rect entry (from bank-0 stub, tail-called through FarCall).
; Source header at [hSrcBank]:[hSrcHi/Lo]: [w|$80] [h] [text bank] [ptr lo] [ptr hi]
; Text: rows separated by $FD, end $FF, $FC n = move to pixel n of the row.
; =====================================================================
VWF_Rect:
    ldh a, [hSVBK]
    push af
    ; save typewriter-independent context (S_*) is scratch here
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
.rowloop:
    ld a, 3
    call SetSVBK
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
    ld a, [hl]
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
    pop af
    jp SetSVBK

; Print the $00-terminated string in wNameBuf at cell DE (bank-3 buffer); returns DE after it.
VWF_PrintBuf:
    ldh a, [hSVBK]
    push af
    ld a, 3
    call SetSVBK
    ld h, d
    ld l, e
    push hl
    ld bc, $0400
    add hl, bc
    ld a, [hl]
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
    pop af
    jp SetSVBK

; Write a space tile into the current cell (bank 0 tile $20), then NextCell.
NextCellBlank:
    ld a, 3
    call SetSVBK
    ld a, [S_cellLo]
    ld l, a
    ld a, [S_cellHi]
    ld h, a
    ld [hl], $20
    ld de, $0400
    add hl, de
    ld a, [S_attr]
    and $f7
    ld [hl], a
    jp NextCell
