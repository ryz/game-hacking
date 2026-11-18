; =====================================================================
; Wizardry Empire (GBC) - variable width font engine
; See docs/re/vwf.md for the design. Assembled by tools/asm.py.
; =====================================================================

VWF_BANK    equ $40

; ---- game addresses
FarCall     equ $c1a0          ; A = bank, HL = address
EnqueueDMA  equ $1443          ; (internal entry used by our stub)
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
wLayout     equ $df00          ; 1 = split (codes $80+ in VRAM1:$9000), 0 = flat (VRAM0:$8800), 2 = museum
                               ; monster room: unsigned tiles, every code in VRAM1:$8000 + code*16
wReset      equ $df01          ; nonzero = clear allocation before next allocation
wNext       equ $df02          ; ring index into Pool (low-code search, last resort)
wNextB      equ $df0f          ; TryAlloc1: wBits byte where the free-slot search starts
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
wGCrows     equ $df4c          ; GC scan: rows left
wGCc        equ $df4d          ; GC scan: current column (0-31)
wGCn        equ $df4e          ; GC scan: visible cells left in the row
wGCchk      equ $df4f          ; GC scan: nonzero = BG with SCX != 0 (all 32 columns, each checked)
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
wGCOwnerless equ $df5d         ; 1: GC marks only slots no text cell owns (game graphics) or recent text; 2: only recent text
wGCcol0     equ $df5e          ; first visible BG column (SCX/8) for GC
wMusClose   equ $df5f          ; $5A while the museum page closes (41:612E redraws the list under the shown page)
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
wDedI       equ $df0b          ; Dedupe: pool index
wDedH       equ $df0c          ; Dedupe: hash
wDedS       equ $df0d          ; Dedupe: own slot
wShared     equ $d410          ; 32 bytes: slot is shown by more than one cell (shadow area of 'A'-'B', not pool)
wDedNew     equ $df0e          ; the current cell got a newly allocated slot (only those are deduped)
wHash       equ $d2c0          ; 256 bytes: content hash per slot (shadow area of codes $2C-$3B, not pool)
wGCSkipWin  equ $df0a          ; 1: GC ignores the window buffer while the window is hidden (2nd pass); 2: GC ignores BG text (layout 2, window print); 3: window text reclaimable even if shown (layout 2, BG print); 4: only recent BG text and the window count
wKeepOff    equ $df09          ; nonzero: the pool ran dry in this burst, old-screen protection dropped
wKeep       equ $d2a0          ; RETIRED: same address as wGameNew; only the disabled HoldMark/KeptNow bodies name it. Was:
                               ; the old screen still shows them until the map copy, so GC keeps them
PRIV_SP     equ $cd80          ; private stack top (WRAM0 $CCE0-$CDD5 is never used by the game)
wGameNew    equ $d2a0          ; 32 bytes: slots the game DMA'd graphics into since the last GC (was wKeep,
                               ; whose hold code is disabled); GC moves them to wGame
; Rect redraw cache (shadow area of code $22, not pool): the town redraws the selected building's info box on
; every main-loop pass; re-rendering it each time ran the town at a fifth of its speed.
wRC_srcBank equ $d220
wRC_srcLo   equ $d221
wRC_srcHi   equ $d222
wRC_dstLo   equ $d223
wRC_dstHi   equ $d224
wRC_mode    equ $d225
wRC_w       equ $d226
wRC_h       equ $d227
wRC_cells   equ $d440          ; 128 bytes: the box's cell codes (shadow area of codes $44-$4B, not pool)
wRC_attrs   equ $d4c0          ; 128 bytes: its attributes (codes $4C-$53)
RC_MAX      equ 128
wRC_epoch   equ $d22a
wRC_valid   equ $d22b
wEpoch      equ $d22c          ; +1 whenever slot tiles change (upload, font load, game DMA over a slot)
; Name print cache (VWF_PrintZ): the town redraws the party names on every main-loop pass.
wVer        equ $da00          ; WRAM bank 6, 256 bytes: per-code tile version, +1 on every upload or game DMA
                               ; over the slot (bank 6 $DA00-$DFFF: no game writes on the tour routes or in battle)
wRC_sumC    equ $d59a          ; 2: Fletcher sum of the cached box's codes (as rendered)
wRC_sumA    equ $d59c          ; 2: ... of its attributes
wRC_sumB    equ $d59e          ; 2: ... of the same box with every code $20 (cleared by the game)
wGCCount    equ $d5a0          ; +1 per GC
wRC_gc      equ $d5a1          ; wGCCount when the box was saved
RC_SCR      equ $cce0          ; WRAM0 scratch for the box restore (private stack area, idle outside PrivCall)
GCF_MODE    equ $cda0          ; GCFilter: the wGCOwnerless mode (WRAM0 free area)
GCB         equ $cd80          ; 32 bytes (WRAM0 above the private stack, never used by the game): GCRowMark's marks
RC_SCRW     equ $cd70          ; box width while switched to bank 3
; Party list cache (39:4931 draws the party rows $D160-$D21F every main-loop pass after the game cleared them)
PL_ROW0     equ $d160          ; 6 rows x 20 cells
wPL_codes   equ $dd00          ; WRAM bank 6, 120 bytes: the rows' codes after the last real draw (before it
                               ; while the draw runs)
wPL_attrs   equ $dd80          ; WRAM bank 6, 120 bytes: their attributes
wPL_valid   equ $d5a2
wPL_pend    equ $d5a3          ; a real draw is running: snapshot at its end
wPL_data    equ $d5a4          ; 2: Fletcher sum of the shown party data
wPL_sumC    equ $d5a6          ; 2: rows' codes after the draw
wPL_sumA    equ $d5a8          ; 2: rows' attributes after the draw
wPL_sumB    equ $d5aa          ; 2: rows' codes before the draw (as the game left them)
wPL_sumBA   equ $d5ac          ; 2: rows' attributes before the draw
wPL_epoch   equ $d5ae
wPL_gc      equ $d5af
wPL_n       equ $d22d          ; cells in wPL_list, $ff = too many (copy all 120 codes)
wPL_list    equ $df00          ; WRAM bank 6, PL_MAX x (offset from PL_ROW0, code): the cells the draw changed
PL_MAX      equ 64             ; 128 bytes: fits the WRAM0 scratch
PL_OFF      equ $cd71          ; PLSnap.list temporaries (WRAM0, private stack area, idle outside PrivCall)
PL_CNT      equ $cd72
PL_COL      equ $cd73
wStamp      equ $de00          ; WRAM bank 6, 256 bytes: frame ($C00A) a slot's tile was last drawn
STAMP_KEEP  equ 8              ; the dry GC pass keeps text slots drawn this recently (a screen being built)
wHIdx       equ $db00          ; WRAM bank 6, 256 bytes: tile hash -> last slot given that hash (HashCur)
wHIdx2      equ $dc00          ; WRAM bank 6, 256 bytes: the slot before it (Dedupe checks both)
wNC         equ $d610          ; NC_N entries (shadow area of 'a'-'z', not pool, up to $D7AF): dstLo, dstHi,
                               ; n cells, hashLo, hashHi, attr, epoch, n x (code, version)
wNC_clr     equ $d597          ; check pass: a cell was cleared (restore needed)
wNC_fast    equ $d598          ; check pass: epoch unchanged, skip the version reads
wNC_ep      equ $d599          ; 2: address of the entry's epoch byte
NC_N        equ 24
NC_MAXC     equ 5
NC_SIZE     equ 7 + 2 * NC_MAXC         ; + epoch (wEpoch when the entry was last verified)
wN_de       equ $d58c          ; numbers: low byte of the cell after the padding
wN_dig      equ $d58d          ; low byte of the first digit in HRAM
wN_cnt      equ $d58e
wN_cells    equ $d58f
wN_x        equ $d590
wN_st       equ $d591          ; 2: field start
wN_end      equ $d593          ; 2: field end (returned in DE)
wN_deHi     equ $d596
wN_done     equ $d250
wN_cb       equ $d251          ; bank of 0:0FE9's caller (wN_*: shadow area of non-pool code $25)
wFS_end     equ $d256          ; 2: FixFind bucket end
wMA_f       equ $d254          ; 2: museum monster abilities as flag bits (MusAbilBody)
wN_cr       equ $d252          ; 2: its return address          ; VWF_Num drew the number (0: the game's 8 px loop runs)
wLowOnly    equ $d595          ; nonzero: prefer low pool codes (VRAM0 in both layouts): numbers in the
                               ; split layout, so cells the game later overwrites with 8 px text keep attribute bit 3 clear
wNC_px      equ $d58b          ; start pixel of the print in its first cell (numbers right-aligned in a field)
wNCNext     equ $d582          ; round-robin replacement index
wNC_hash    equ $d583          ; 2
wNC_ent     equ $d585          ; 2: entry's cell triples
wNC_cell    equ $d587          ; 2: destination cell
wNC_n       equ $d589
wNC_pass    equ $d58a          ; NCWalk: 0 check, 1 restore, 2 save
wGame       equ $d200          ; 32 bytes: slots holding game graphics (shadow area of codes $20/$21, not pool)
wSpell      equ $d280          ; 32 bytes: full English name of the last spell read by 0:24CF (shadow area of
                               ; codes $28/$29, not pool); messages print it with {F8 00 07 D280}
wMagic      equ $dffe          ; 'V','^' once initialised (bump when the variable layout changes)
HOME_BANK   equ 7

STAGING_BANK equ 7             ; WRAM bank 7 $d000 + code*16 = shadow of the VRAM tile
MAP_BANK    equ 6              ; WRAM bank 6: cellmap $d000-$d7ff, owners $d800 + code*2

; =====================================================================
; Bank 0 patches and stubs
; =====================================================================

; --- DMA enqueue: watch for the font's upper half being loaded to learn the layout
    org 0, $1443
    jp Stub_Enqueue

; --- typewriter character output (replaces 1c2a-1c8f)
; New control code $F2 bank lo hi: continue the message at bank:lo/hi (used to redirect
; every original message to its English text).
    org 0, $1c2a
    cp $f2
    jr z, .jump
    push hl
    ld b, a
    ld a, VWF_BANK
    ld hl, TW_Char
    call FarCall
    pop hl
    jp $1be0
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
    jp $1be0

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

Stub_Num:                   ; 0:10A4 (number printer 0:0FE9, digit store): base '0' into a screen buffer -> VWF
    ldh a, [$ad]            ; digit base ($30 = 8 px font digits; $F4 = symbol sheet stays)
    cp $30
    jr nz, .no
    ld a, d
    cp $d0
    jr c, .no
    cp $dc
    jr nc, .no
    ld c, l                 ; first digit to print at $FF00+C (the digits end at $FFC1)
    ld a, VWF_BANK
    ld hl, VWF_Num
    call FarCall            ; L = 1: done, DE past the field; L = 0: not drawn (DE, C kept) -> 8 px loop
    ld b, 0                 ; as the digit loop leaves it: callers test B after 0:0FE9 (2D:7BB3: bit 7 =
    ld a, l                 ; poisoned -> '-' instead of '/'; the VWF's B made every row look poisoned)
    ld h, $ff
    ld l, c
    rra
    ret
.no:
    and a
    ret
    assert @ <= $1c92, "typewriter stub overflow"

; --- {FA} word look-ahead (1cb3: ld a,[hli] / cp $fa / jr nc,$1d1e): also stop at our $F2 jump, so the
;     jump bytes at the end of English text are not counted as part of the last word
    org 0, $1cb3
    call Stub_Measure
    jr nc, $1d1e
    org 0, $1d1e
    call Stub_WrapCmp
    jr c, $1d2d
    ds 6, $00
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
    org 0, $1b58
    call Stub_TWInit
    nop

; --- rect blitters: tiles only (1789) / tiles + attributes (173C)
    org 0, $1789
    jp Stub_Rect0
    org 0, $173c
    jp Stub_Rect1
; --- attributes-only blitter (17c0): mask the VWF marker bit when reading w
    org 0, $17d6
    call Stub_ReadW

; --- $00-terminated name copy loops (ld a,[hli] / or a / jr z / ld [de],a / inc de / jr) -> VWF
    org $26, $4caa
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $26, $5652
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $452b
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $49a2
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $52b3
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $55a5
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $67e9
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $6ab0
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $6b9a
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $27, $70ce
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2a, $57e3
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2a, $6267
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2a, $6f2c
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2a, $6f8d
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2b, $571b
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2e, $5811
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop
    org $2e, $590a
    call Stub_PrintZ
    jr @+5
    nop
    nop
    nop

; --- shop/item lists (41:4A4F): counted copy of the name at $C54F (max 16, stops at $00) -> VWF
    org $29, $4a52
    call Stub_PrintZ
    jr @+8
    ds 6, $00

; --- unidentified item name in a list (41:574C, record [len][$01][text][$00] at DE, cell at HL): blank the
;     16 cells, then the VWF (tools/insert.py insert_unid writes ASCII records)
    org $29, $574c
    push bc
    push hl
    ld c, $10
    ld a, $20
.unidfill:
    ld [hli], a
    dec c
    jr nz, .unidfill
    pop hl
    inc de
    inc de
    push de
    ld d, h
    ld e, l
    pop hl
    call Stub_PrintZ
    pop bc
    ret
    assert @ <= $5764, "unid name copy"

; --- museum item list name (41:62C7): name at $C54F -> VWF (docs/re/museum.md hook B)
    org $29, $62c7
    ld hl, $c54f
    call Stub_PrintZ
    jr @+8
    ds 6, $00
; --- museum page header / unidentified name (41:66C2): $00-terminated at HL -> VWF (hook A; both callers reload
;     HL and DE afterwards)
    org $29, $66c2
    jp Stub_PrintZ

; --- museum item page 'Equip:' (41:65A2-662B: tile and attribute loops of the class letters) -> the allowed
;     classes as two-letter abbreviations in the VWF, packed: row 1 the 8 basic classes, row 2 the 6 extras
    org $29, $65a2
    call MusClasses
    jp $662c
    org $29, $7b00
MusClasses:                 ; SVBK = 3 here (the original loops wrote the window buffer directly)
    ld hl, MusAbbr
    ld de, MUS_STR
    ld a, [$c565]
    ld b, a
    ld c, 8
.l1: srl b
    call c, .add
    inc hl
    inc hl
    dec c
    jr nz, .l1
    ld hl, $d9e6
    call .print
    ld hl, MusAbbr + 16
    ld de, MUS_STR
    ld a, [$c566]
    ld b, a
    ld c, 6
.l2: srl b
    jr nc, .s2
    push hl
    ld a, 6
    sub c
    ld hl, $ffb0
    add l
    ld l, a
    ld a, [hl]
    pop hl
    or a
    call nz, .add
.s2: inc hl
    inc hl
    dec c
    jr nz, .l2
    ld hl, $da06
.print:                     ; blank 13 cells at HL, print MUS_STR there
    xor a
    ld [de], a
    push hl
    ld c, 13
    ld a, $20
.b: ld [hli], a
    dec c
    jr nz, .b
    pop de
    ld hl, MUS_STR
    jp Stub_PrintZ
.add:                       ; append the two letters at HL and a space to DE
    ld a, [hli]
    ld [de], a
    inc de
    ld a, [hld]
    ld [de], a
    inc de
    ld a, $20
    ld [de], a
    inc de
    ret
MUS_STR     equ $cce0       ; WRAM0 scratch (private VWF stack area; VWF_PrintZ copies it before using that stack)
MusAbbr:                    ; class order: Fighter Mage Priest Thief Bishop Samurai Lord Ninja / Archer Valiant
    db "FiMaPrThBiSaLoNi"   ; Avenger Musashi Kunoichi Summoner
    db "ArVaAvMuKuSu"
; --- shop header (29:422D: 8 px 'A','C' at $D04E over the card's age row; 29:4253: 8 px '-') -> 'AC' in the VWF
;     at $D04D (covers the card's 'Age' label, under 'Lvl'), small '-' at the right of its cell
    org $29, $422d
    call ShopAC
    ds 8, $00
    org $29, $4270          ; AC out of range: 8 px 'Lo'/'Hi' -> VWF, right-aligned in the field
    call ShopLoHi
    jr $4285
    org $29, $424a          ; negative AC: as the card (ShopNeg)
    jp ShopNeg
    org $29, $4298          ; gold field: the Japanese label + 4 spaces put it at $D069 (ends col 18); the VWF
    ld de, $d065            ; label is narrower and left DE a cell early: the field starts at $D065 and is 14
    ds 7, $00               ; cells (the game's own clear loop blanks them, incl. the card's 'Status' row)
    org $29, $42a6
    db $0e
    org $29, $42b0
    db $8e
    org $29, $7e40
ShopAC:
    ld de, $d04d
    ld hl, ShopACText
    call Stub_PrintZ
    ld de, $d050
    ret
ShopACText:
    db "AC", 0
    org $29, $7a02
ShopNeg:                    ; A = AC (negative), HL = $FFB0
    cpl
    inc a
    ld [hl], a
    ld b, a
    ld a, $2d
    ldh [$b2], a            ; sign flag (read by the Lo/Hi path)
    ld a, b
    cp 100
    jp nc, $4258           ; 'Lo': original path
    ld de, $d050
    call ShopNegPrint
    jp $4285
; A = 1..99, DE = 3-cell field: '-<digits>' right-aligned at the field's right edge (the minus right before the
; digits); the string is built at $FFB8 (0:0FE9's digit scratch, unused here). Advances: '-' 4, digits 5, '1' 4.
ShopNegPrint:
    push de
    ld h, d
    ld l, e
    ld b, 3
    ld c, a
    ld a, $20
.bl: ld [hli], a
    dec b
    jr nz, .bl
    ld a, c
.t: cp 10
    jr c, .o
    sub 10
    inc b
    jr .t
.o: ld d, a                 ; d = ones, b = tens
    ld e, 9                 ; width: '-' + ones
    cp 1
    jr nz, .a
    dec e
.a: ld a, b
    or a
    jr z, .b
    ld a, e
    add 5
    ld e, a
    ld a, b
    cp 1
    jr nz, .b
    dec e
.b: ld a, 24
    sub e                   ; x in the field (10..16)
    ld e, a
    and 7
    ld h, a                 ; h = lead px
    ld a, e
    srl a
    srl a
    srl a
    ld l, a                 ; l = start cell in the field
    ld a, h
    cp 1
    jr nz, .c
    dec l
    ld h, 9
.c: ld c, $b8
    bit 0, h
    jr z, .ev
    ld a, $20               ; 3 px blank
    ldh [c], a
    inc c
    dec h
    dec h
    dec h
.ev: srl h                  ; 2 px blanks
    jr z, .m
.p: ld a, $7c
    ldh [c], a
    inc c
    dec h
    jr nz, .p
.m: ld a, $2d
    ldh [c], a
    inc c
    ld a, b
    or a
    jr z, .u
    add $30
    ldh [c], a
    inc c
.u: ld a, d
    add $30
    ldh [c], a
    inc c
    xor a
    ldh [c], a
    pop de
    push de
    ld a, e
    add l
    ld e, a
    ld hl, $ffb8
    call Stub_PrintZ
    pop de
    inc de
    inc de
    inc de
    ret
ShopLoHi:
    ld de, $d051
    ldh a, [$b2]            ; sign flag: negative = 'Lo'
    or a
    ld hl, ShopLoText
    jr nz, .p
    ld hl, ShopHiText
.p: jp Stub_PrintZ
ShopLoText:
    db $7c, $7c, $7c, "Lo", 0   ; 10 px, ends at the field's right edge
ShopHiText:
    db " ", " ", " ", "Hi", 0   ; 7 px: 9 px lead from the field's 2nd cell
    assert @ <= $7b00, "ShopNeg overflow"

; --- museum damage / monster HP range: '~' (8 px) -> a VWF '-' centred in its cell; AC minus (41:689D) -> a VWF
;     '-' at the right of its cell, next to the digits. One cell each, so DE advances as before.
    org $29, $650b
    call MusRange
    nop
    org $29, $6917
    call MusRange
    nop
    org $29, $689d
    call MusMinus
    nop
    org $29, $7e00
MusRange:
    ld hl, MusRangeStr
    jp Stub_PrintZ
MusMinus:                   ; keeps HL ($FFB0, the value for 0:0FE9)
    push hl
    ld hl, MusMinusStr
    call Stub_PrintZ
    pop hl
    ret
MusRangeStr:
    db $7c, "-", 0
MusMinusStr:
    db $7c, $7c, "-", 0

; --- character card 'L' (26:567A: ld a,'L' / ld [de],a / inc de at $D02E) -> 'Lvl' in the VWF at the cell before
;     (cols 13-14), DE ends at the level field like the original
    org $26, $5684
    call CardLvl
    nop
    org $26, $7f00
CardLvl:
    dec de
    push de
    ld hl, CardLvlText
    call Stub_PrintZ
    pop de
    ld de, $d030            ; level field: 3 cells ending at col 18 (the right edge shared with Age and AC)
    ret
CardLvlText:
    db "Lvl", 0

; --- character card age (26:570B: 2-cell field at $D04E, then 'さい' at DE by 26:5723) -> 'Age' at col 13 and
;     the number in the VWF ending at col 18; HP and AC labels (26:57BE, 26:5804: 8 px 'H','P' / 'A','C') in
;     the VWF, AC under Lvl/Age (col 13)
    org $26, $570b
    ld de, $d051
    org $26, $5723
    call CardAge
    ds 4, $00
    org $26, $57be
    call CardHP
    ds 9, $00
    org $26, $57d5          ; HP separator '/' (8 px) -> VWF
    call CardSlash
    nop
    org $26, $57ea          ; max HP: '/' + the number as one VWF string from the slash cell ("10/10", no gap)
    call CardMaxHP
    ds 8, $00
    org $26, $5804
    call CardAC
    ds 8, $00
    org $26, $5812          ; AC value: right-aligned 2-cell field ending at col 18 ($D091-$D092) for every value
    ld bc, $3082
    org $26, $5857          ; (positive values under 10 skipped one more cell for the left-aligned 8 px digit)
    nop
    org $26, $5870          ; AC out of range: 8 px 'Lo'/'Hi' -> VWF, right-aligned in the field
    call CardLoHi
    jr $5885
    org $26, $5843          ; negative AC: '-<digits>' as one right-aligned VWF string (CardNeg)
    jp CardNeg
    org $26, $5949          ; sheet EXP / Gold fields at the Japanese columns (cols 9-18): the English labels are
    ld de, $d109            ; narrower and left DE early
    org $26, $5975
    ld de, $d129
    nop
    org $26, $7f80
CardAge:
    ld de, $d04d
    ld hl, CardAgeText
    jp Stub_PrintZ
CardHP:                     ; DE ends at $D084 (the HP field) like the original
    ld de, $d081
    ld hl, CardHPText
    call Stub_PrintZ
    ld de, $d084
    ret
CardAC:                     ; DE ends at $D090 (the AC value) like the original
    ld de, $d08d
    ld hl, CardACText
    call Stub_PrintZ
    ld de, $d090
    ret
CardSlash:                  ; DE -> DE + 1; HL is reloaded by the caller
    ld hl, CardSlashText
    jp Stub_PrintZ
CardSlashText:
    db "/", 0
CardMaxHP:                  ; DE = cell after the slash (its 4 cells blanked by the caller)
    push de
    ld a, $2f
    ld [MUS_STR], a
    ld de, MUS_STR + 1      ; outside $D000-$DBFF: 0:0FE9 stores the digit codes here (Stub_Num passes)
    ld a, 2
    ld bc, $3000
    ld hl, $c4f1
    call $0fe9
    xor a
    ld [de], a
    pop de
    dec de
    ld hl, MUS_STR
    jp Stub_PrintZ
CardAgeText:
    db "Age", 0
CardHPText:
    db "HP", 0
CardACText:
    db "AC", 0

; --- character card status (26:575C: ld de,$D068 / 'Status:' (inline, 26:575F) / 26:579D: pop de / 5-byte copy of
;     the word at HL = 26:7574 + 5k) -> 'Status: <word>' right-aligned at col 18 like Lvl/Age/AC, the label one
;     space before the word (table built by tools/build.py card_status()); DE ends at $D072 like the original
;     (the bit-1 variant at 26:57DA prints a number there)
    org $26, $575f
    jr @+$18                ; skip the fixed label (-> 26:5777)
    org $26, $579e
    call CardStatus
    ds 11, $00
    org $26, $7800
CardStatus:
    ld a, l                 ; k = (L - $74) / 5
    sub $74
    ld b, -1
.d: inc b
    sub 5
    jr nc, .d
    ld l, b                 ; HL = CardStatusTab + 32k
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    ld de, $7840            ; CardStatusTab
    add hl, de
    push hl
    ld hl, $d068            ; blank cols 8-18 (a longer word shown before)
    ld a, $20
    ld b, 11
.b: ld [hli], a
    dec b
    jr nz, .b
    pop hl
    ld a, [hli]             ; start cell
    ld e, a
    ld d, $d0
    call Stub_PrintZ
    ld de, $d072
    ret
    assert @ <= $7840, "CardStatus overflow"
    org $26, $7a00
CardNeg:                    ; A = AC (negative), HL = $FFB0
    cpl
    inc a
    ld [hl], a
    ld b, a
    ld a, $2d
    ldh [$b2], a            ; sign flag (read by the Lo/Hi path)
    ld a, b
    cp 100
    jp nc, $5858           ; 'Lo': original path
    ld de, $d090
    call CardNegPrint
    jp $5885
; A = 1..99, DE = 3-cell field: '-<digits>' right-aligned at the field's right edge (the minus right before the
; digits); the string is built at $FFB8 (0:0FE9's digit scratch, unused here). Advances: '-' 4, digits 5, '1' 4.
CardNegPrint:
    push de
    ld h, d
    ld l, e
    ld b, 3
    ld c, a
    ld a, $20
.bl: ld [hli], a
    dec b
    jr nz, .bl
    ld a, c
.t: cp 10
    jr c, .o
    sub 10
    inc b
    jr .t
.o: ld d, a                 ; d = ones, b = tens
    ld e, 9                 ; width: '-' + ones
    cp 1
    jr nz, .a
    dec e
.a: ld a, b
    or a
    jr z, .b
    ld a, e
    add 5
    ld e, a
    ld a, b
    cp 1
    jr nz, .b
    dec e
.b: ld a, 24
    sub e                   ; x in the field (10..16)
    ld e, a
    and 7
    ld h, a                 ; h = lead px
    ld a, e
    srl a
    srl a
    srl a
    ld l, a                 ; l = start cell in the field
    ld a, h
    cp 1
    jr nz, .c
    dec l
    ld h, 9
.c: ld c, $b8
    bit 0, h
    jr z, .ev
    ld a, $20               ; 3 px blank
    ldh [c], a
    inc c
    dec h
    dec h
    dec h
.ev: srl h                  ; 2 px blanks
    jr z, .m
.p: ld a, $7c
    ldh [c], a
    inc c
    dec h
    jr nz, .p
.m: ld a, $2d
    ldh [c], a
    inc c
    ld a, b
    or a
    jr z, .u
    add $30
    ldh [c], a
    inc c
.u: ld a, d
    add $30
    ldh [c], a
    inc c
    xor a
    ldh [c], a
    pop de
    push de
    ld a, e
    add l
    ld e, a
    ld hl, $ffb8
    call Stub_PrintZ
    pop de
    inc de
    inc de
    inc de
    ret
CardLoHi:
    ld de, $d091
    ldh a, [$b2]            ; sign flag: negative = 'Lo'
    or a
    ld hl, CardLoText
    jr nz, .p
    ld hl, CardHiText
.p: jp Stub_PrintZ
CardLoText:
    db $7c, $7c, $7c, "Lo", 0   ; 10 px, ends at the field's right edge
CardHiText:
    db " ", " ", " ", "Hi", 0   ; 7 px: 9 px lead from the field's 2nd cell
    assert @ <= $7f00, "CardNeg overflow"
    org $26, $7840
CardStatusTab:
    incbin "../build/card_status.bin"   ; 10 x 32 bytes: start cell low byte, blank-glyph lead, text, $00

; --- character creation: unset fields filled with 8 px '?' (26:56C6 6 cells, 56F5 4, 571D 2 = age, 5751 5)
;     -> the same '?' strings in the VWF (the code after each site reloads DE and HL)
    org $26, $56c6
    ld hl, CardQ6
    call Stub_PrintZ
    jr $56d3
    org $26, $56f5
    ld hl, CardQ4
    call Stub_PrintZ
    jr $56fe
    org $26, $571d
    ld hl, CardQ2
    call Stub_PrintZ
    org $26, $5751
    ld hl, CardQ5
    call Stub_PrintZ
    jr $575c
    org $26, $7d40
CardQ6:
    db "??????", 0
CardQ4:
    db "????", 0
CardQ5:
    db "?????", 0
CardQ2:
    db "??", 0

; --- item list marks: '?' unidentified and '-' cursed were 8 px (the equipped bullet '●' = 8 px '*' stays: an
;     icon). Sheet item list 2A:6EC3, Camp Equip lists 2A:620B, shop Sell list 29:560A, battle Item > Equip 22:5448.
    org $2a, $6ec3
    ld a, [hl]
    call MarkSel
    jr $6ee0
    org $2a, $620b
    ld a, [hl]
    call MarkSel
    jr $6228
    org $2a, $7980
MarkSel:                    ; A = item flag byte (bit 7 equipped, 6 unidentified, 5 cursed), DE = cell -> DE + 1;
    bit 7, a                ; HL, BC kept
    jr z, .ne
    bit 5, a
    jr nz, .m
    ld a, $2a               ; equipped: the 8 px bullet icon stays
    ld [de], a
    inc de
    ret
.ne: bit 6, a
    jr nz, .q
    bit 5, a
    jr nz, .m
    inc de
    ret
.q: push hl
    ld hl, MarkQ
    jr .p
.m: push hl
    ld hl, MarkM
.p: call Stub_PrintZ
    pop hl
    ret
MarkQ:
    db $7c, "?", 0
MarkM:
    db $7c, "-", 0

    org $29, $560a
    call ShopMarkSel
    jr $5629
    org $29, $7f90
ShopMarkSel:                ; B = flag byte, HL = cell -> HL + 1 (ld [hli],a); a blank cell when no mark
    ld a, b
    and $e0
    jr nz, .mk
    ld a, $20
    ld [hli], a
    ret
.mk: push de
    ld d, h
    ld e, l
    ld a, b
    call ShopMarkSel2
    ld h, d
    ld l, e
    pop de
    ret
ShopMarkSel2:
    bit 7, a
    jr z, .ne
    bit 5, a
    jr nz, .m
    ld a, $2a
    ld [de], a
    inc de
    ret
.ne: bit 6, a
    jr nz, .q
.m: ld hl, ShopMarkM
    jp Stub_PrintZ
.q: ld hl, ShopMarkQ
    jp Stub_PrintZ
ShopMarkQ:
    db $7c, "?", 0
ShopMarkM:
    db $7c, "-", 0
    assert @ <= $8000, "bank 41 overflow"
    org $22, $5444
    call BtlMark
    nop
    nop
    org $22, $7900
BtlMark:                    ; HL = row offset, B = mark code ('?', '-' or the bullet '*'); DE ends $D842 as before
    ld de, $d842
    add hl, de
    ld a, b
    cp $2a
    jr nz, .v
    ld [hl], b
    ret
.v: push hl
    ld d, h
    ld e, l
    ld hl, BtlMarkQ
    cp $3f
    jr z, .p
    ld hl, BtlMarkM
.p: call Stub_PrintZ
    pop hl
    ld de, $d842
    ret
BtlMarkQ:
    db $7c, "?", 0
BtlMarkM:
    db $7c, "-", 0

; --- Search Person ("Look for whom?", priest spell): five animated 8 px '.' (2E:5640 + 18k), the raw code $5E
;     (Japanese particle, now a VWF pool slot -> random glyph) after the name at 2E:5819, and the location line at
;     $D122 built from 8 px 'B', 'X', ',', 'Y' around VWF digits (2E:5774-57DC, 'B1    X0 ,Y0')
;     -> VWF dots, no particle, and 'B1 X0, Y0' as one VWF string (digits by 0:0FE9 into MUS_STR)
    org $2e, $5640
    call SPDot
    nop
    org $2e, $5652
    call SPDot
    nop
    org $2e, $5664
    call SPDot
    nop
    org $2e, $5676
    call SPDot
    nop
    org $2e, $5688
    call SPDot
    nop
    org $2e, $5819
    inc de                  ; (was ld a,$5E / ld [de],a / inc de)
    nop
    nop
    nop
    org $2e, $5774
    jp SPLine
    org $2e, $7800
SPDot:                      ; DE = cell -> DE + 1; HL kept
    push hl
    ld hl, SPDotText
    call Stub_PrintZ
    pop hl
    ret
SPDotText:
    db " ", ".", 0
SPLine:                     ; B = location byte (floor index & $1F), C = y << 4 | x; ends at 2E:57DD with DE
    push bc                 ; past the text and BC as the original leaves them
    ld de, MUS_STR
    ld a, $42 ; B
    ld [de], a
    inc de
    ld a, b
    and $1f
    ld hl, $56eb            ; floor number table (2 bytes per entry), as 2E:577F
    add a
    add l
    ld l, a
    jr nc, .f
    inc h
.f: ld a, [hli]
    ldh [$b0], a
    ld a, [hl]
    ldh [$b1], a
    ld a, 2
    ld bc, $3000
    ld hl, $ffb0
    call $0fe9              ; DE outside $D000-$DBFF: plain digit codes into MUS_STR
    ld a, $20
    ld [de], a
    inc de
    ld a, $58 ; X
    ld [de], a
    inc de
    pop bc
    push bc
    ld a, c
    and $0f
    ldh [$b0], a
    ld a, 1
    ld bc, $3000
    ld hl, $ffb0
    call $0fe9
    ld a, $2c ; ,
    ld [de], a
    inc de
    ld a, $20
    ld [de], a
    inc de
    ld a, $59 ; Y
    ld [de], a
    inc de
    pop bc
    push bc
    ld a, c
    swap a
    and $0f
    ldh [$b0], a
    ld a, 1
    ld bc, $3000
    ld hl, $ffb0
    call $0fe9
    xor a
    ld [de], a
    ld hl, $d122            ; blank the line (14 cells) before printing
    ld a, $20
    ld b, 14
.b: ld [hli], a
    dec b
    jr nz, .b
    ld de, $d122
    ld hl, MUS_STR
    call Stub_PrintZ
    pop bc
    jp $57dd

; --- camp heal result box (0:37FC, A = 0 branch of the camp result dispatcher 0:37B9): 8 px 'H','P' at $D0E4,
;     current HP (4 cells, right-aligned) at $D0E7, 8 px '/' at $D0EB, max HP at $D0EC -> HealBox (bank 26):
;     'HP' and '/max' in the VWF like the character card
    org 0, $380b
    ld a, $26
    ld hl, HealBox
    call FarCall
    jr $3831
    org $26, $7d00
HealBox:
    ld de, $d0e4
    ld hl, CardHPText
    call Stub_PrintZ
    ld hl, $d0eb            ; blank the slash + max cells (the box is redrawn as HP rises)
    ld a, $20
    ld b, 6
.b: ld [hli], a
    dec b
    jr nz, .b
    ld de, $d0e7
    ld a, 2
    ld bc, $3084
    ld hl, $c4f3
    call $0fe9              ; current HP, DE -> $D0EB
    inc de
    jp CardMaxHP            ; '/' + max from the slash cell

; --- name entry: typed name field (26:6C62-6C9B built a [7][1] rect at $FFA8 from the name at $D060 and blitted
;     it to $D02A) -> blank the 7 cells, copy up to 7 characters + $00 to $FFA8, print it in the VWF
    org $26, $6c62
    jp NameField
    org $26, $7f20
NameField:
    ldh a, [$9d]            ; the field is in the WRAM bank 3 buffer
    push af
    ld a, 3
    ldh [$9d], a
    ldh [$70], a
    ld hl, $d02a
    ld b, 7
    ld a, $20
.bl: ld [hli], a
    dec b
    jr nz, .bl
    pop af
    ldh [$9d], a
    ldh [$70], a
    ld hl, $d060
    ld de, $ffa8
    ld b, 7
.cp: ld a, [hli]
    or a
    jr z, .e
    ld [de], a
    inc de
    dec b
    jr nz, .cp
.e: xor a
    ld [de], a
    ld hl, $ffa8
    ld de, $d02a
    jp Stub_PrintZ
; cursor box (26:6C37-6C51: x = $50 + 8 * letters, the 7th letter keeps x on it) -> $50 + the VWF width
    org $26, $6c37
    push hl
    call NameCursorX
    pop hl
    ld [hl], a
    jr @+21
    ds 19, $00
    org $26, $7f60
NameCursorX:                ; A = x of the cursor box
    ld hl, $d060
    ld de, $ffa8
    ld b, 7
.cp: ld a, [hli]
    or a
    jr z, .e
    ld [de], a
    inc de
    dec b
    jr nz, .cp
.e: xor a
    ld [de], a
    ld a, VWF_BANK
    ld hl, VWF_NameW
    call FarCall
    ld a, l
    add $50
    ret

; --- bank-45 event party list (magic circle 'Who will step inside?', 2D:7BE7: name copy with 'and $7f';
;     DE/HL are pushed around it at 2D:7BE5) -> VWF
    org $2d, $7be7
    call Stub_PrintZ
    jr @+7
    ds 5, $00

; --- temple result '<name> went to the tavern.' / ' turned to ashes.' / ' is lost.' (27:67D0 right-aligned the
;     name in 7 cells by letter count, 27:681D put the rect at the fixed cell $D0A8: a gap after short VWF
;     names) -> the name at $D0A1, the rect right after it (Stub_PrintZ leaves DE past the name)
    org $27, $67d0
    ld de, $d0a1
    jr @+10
    ds 8, $00
    org $27, $681d
    ld a, e
    ldh [$bb], a
    ld a, d
    ldh [$bc], a
    nop
    nop

; --- Maze view graphics (20:4100-4240): each 2 KB block is loaded as a queued GDMA (0:1443, seen by
;     VWF_DmaCheck) plus an immediate HBlank DMA of its second KB (0:1553, B = 16-byte blocks), which bypassed
;     the check: VRAM0 $8C00-$8FFF (flat codes $C0-$FF, the walls) kept its owners/shadows and was never
;     reserved, so the dungeon menu's text took the wall slots (mirrored 'Pick a lock' in the view strip).
;     The four 'di / ld b,$40 / call $1553 / ei' sites call MazeHdma (check after the transfer, interrupts on).
    org $20, $41b0
    call MazeHdma
    ds 4, $00
    org $20, $41d8
    call MazeHdma
    ds 4, $00
    org $20, $420b
    call MazeHdma
    ds 4, $00
    org $20, $4233
    call MazeHdma
    ds 4, $00
    org $20, $7f00
MazeHdma:
    di
    ld b, $40
    call $1553
    ei
    ld a, VWF_BANK          ; the view's tiles fill VRAM0/1 $8000-$8FFF: back to the split text layout
    ld hl, VWF_MazeSplit
    call FarCall
    ld bc, $0040            ; tiles, as Stub_Dma passes them (hSrc*/hDst* are unchanged by 0:1553)
    ld a, VWF_BANK
    ld hl, VWF_DmaCheck
    jp FarCall

; --- spell slot grid (2A:4B7B, from 2A:45B2/45BB/4BF2 after the 8 px ' / / / / / /' rect 2A:7227 at DE+1): 7 digits
;     one per cell between the rect's 8 px slashes -> blank the 13 cells, one VWF string on the same 16 px grid
;     (the level cursor moves 2 cells per level): digit ink at px 2-5 of its 16 px, the slash between
    org $2a, $4b84
    jp SpellSlots
    org $2a, $7900
SpellSlots:                 ; HL = 7 slot counts, DE = first cell (SVBK 3 set, its old value pushed)
    push de
    push hl
    ld h, d
    ld l, e
    ld a, $20
    ld b, 13
.b: ld [hli], a
    dec b
    jr nz, .b
    pop hl
    ld de, MUS_STR
    ld c, 7
.l: ld a, [hli]
.m: cp 10                   ; the original kept the low digit (0:0FE9 with C = 1)
    jr c, .d
    sub 10
    jr .m
.d: ld b, a
    ld a, $7c               ; 2 px lead
    ld [de], a
    inc de
    ld a, b
    add $30
    ld [de], a
    inc de
    dec c
    jr z, .e
    ld a, b                 ; then '[3 px] / [2 px]' (after a '1', 4 px: '[2+2 px] / [2 px]'): 16 px per level,
    cp 1                    ; 4 px ink gap before the slash, 5 after
    ld a, $20
    jr nz, .s
    ld a, $7c
    ld [de], a
    inc de
.s: ld [de], a
    inc de
    ld a, $2f
    ld [de], a
    inc de
    ld a, $7c
    ld [de], a
    inc de
    jr .l
.e: xor a
    ld [de], a
    pop de
    ld hl, MUS_STR
    call Stub_PrintZ
    jp $4b99                ; restore SVBK, ret

; --- item info AC (29:651A: 2-cell right-aligned value at $D8E6, 8 px '-' before it when the AC byte is negative)
;     -> negative values as one right-aligned '-N' (ShopNegPrint, 3-cell field $D8E5-$D8E7)
    org $29, $652c
    jp ItemNeg
    org $29, $7f80
ItemNeg:                    ; A = AC byte (negative), HL = $FFB0
    cpl
    inc a
    ld [hl], a
    ld de, $d8e5
    call ShopNegPrint
    jp $653e

; --- item info 'Range:' value (29:6553: 8 px letter from 'SML-' at 29:6374 into $D8F2) -> the word in the VWF,
;     right-aligned at col 18 (field cols 14-18, blank-glyph lead computed for this font)
    org $29, $6553
    call RangeWord
    nop
    nop
    org $29, $7f00
RangeWord:                  ; HL = 29:6374 + index, DE = $D8F2; ends with HL = $C562 like the original
    ld a, l
    sub $74
    add a
    ld e, a
    ld d, 0
    ld hl, RangeTab
    add hl, de
    ld a, [hli]
    ld h, [hl]
    ld l, a
    push hl
    ld hl, $d8ee
    ld a, $20
    ld b, 5
.b: ld [hli], a
    dec b
    jr nz, .b
    pop hl
    ld a, [hli]             ; start cell in the field
    add $ee
    ld e, a
    ld d, $d8
    call Stub_PrintZ
    ld hl, $c562
    ret
RangeTab:
    dw RangeS, RangeM, RangeL, RangeN
RangeS:                     ; start cell, blank-glyph lead ($7C 2 px, ' ' 3 px), word: ends at col 18 (40 px field)
    db 1, " ", $7c, $7c, $7c, "Short", 0       ; 23 px -> x 17 = cell 1 + 9
RangeM:
    db 1, " ", "Medium", 0                     ; 29 px -> x 11 = cell 1 + 3
RangeL:
    db 2, $7c, $7c, "Long", 0                  ; 20 px -> x 20 = cell 2 + 4
RangeN:
    db 4, "--", 0                              ; 8 px -> x 32 = cell 4
    assert @ <= $8000, "bank 41 overflow"

; --- Find allies list (20:62C6: name copy DE (SRAM roster) -> HL, codes $80+ with the VRAM1 bit; BC/HL are
;     popped from the stack at 20:62E2) -> VWF
    org $20, $62c6
    push hl
    push de
    pop hl
    pop de
    call Stub_PrintZ
    jr @+21
    ds 19, $00

; --- Camp reorder list (2A:7082: $00-terminated name copy ending in 'ret z', called from 2A:7075) -> VWF
    org $2a, $7082
    jp Stub_PrintZ

; --- museum monster list name (41:633E): name at $C50F -> VWF
    org $29, $633e
    ld hl, $c50f
    call Stub_PrintZ
    jr @+12
    ds 8, $00
; --- museum monster page name / unidentified name (41:66E5: 2 rows of 8 cells) -> VWF, word-wrapped at 64 px
    org $29, $66e5
    jp Mus2Line
    org $29, $7d00
; --- museum monster page abilities (41:6989-6AB1: glyph pairs at fixed cells) -> words in the VWF; the
;     resistance values (41:6AB2..) stay
    org $29, $6989
    call MusAbil
    jp $6ab2
    org $29, $7d20
MusAbil:
    ld a, VWF_BANK
    ld hl, VWF_MusAbil
    jp FarCall
; --- museum monster page 'EXP:' label (41:68A6-68B9: glyph tiles $D4 $D5 + ':' and their attributes) -> VWF
    org $29, $68a6
    ld hl, MusExpStr
    ld de, $d90a
    call Stub_PrintZ
    jr @+11
    ds 9, $00
; --- museum monster page resistance labels (41:6844-685D: one glyph tile per element at $DA03+4i/$DA23+4i)
;     -> 3-letter VWF words in the 2 cells left of each value ($DA02+4i, cols 2-3, 6-7, 10-11, 14-15)
; --- museum resistance 100 (41:6B10-6B1D: '10' printed, then glyph $EE '00' over the second cell) -> VWF '100'
;     in both cells (15 px); DE stays past the field like the original
    org $29, $6b10
    push de
    dec de
    dec de
    push hl
    ld hl, Mus100Str
    call Stub_PrintZ
    pop hl
    pop de
    ret
    ds 1, $00
    org $29, $6844
    call MusElem
    jr @+23
    ds 21, $00
; --- museum monster page closed (41:612E: list redraw under the still shown page) -> flag for AllocScan
    org $29, $612e
    call MusClose
    ds 3, $00
    org $29, $7d40
MusClose:
    ld a, VWF_BANK
    ld hl, VWF_MusCloseOn
    call FarCall
    call $621d
    call $61bd
    ld a, VWF_BANK
    ld hl, VWF_MusCloseOff
    jp FarCall
MusElem:                    ; keeps BC (41:685E uses B)
    push bc
    ld hl, MusElemStr
    ld de, $da02
    call .row
    ld de, $da22
    call .row
    pop bc
    ret
.row:
    ld b, 4
.l: push bc
    push de
    call Stub_PrintZ        ; HL ends past the $00
    pop de
    inc de
    inc de
    inc de
    inc de
    pop bc
    dec b
    jr nz, .l
    ret
MusElemStr:                 ; 地 水 火 風 / 精(神) 気 (神)聖 無 (glossary: Earth Water Fire Air / Mind Aura Holy None)
    db $7c, "Ear", 0, $7c, "Wat", 0, $7c, "Fir", 0, $7c, "Air", 0   ; $7C = 2 px space
    db $7c, "Min", 0, $7c, "Aur", 0, $7c, "Hol", 0, $7c, "Non", 0
MusExpStr:
    db "EXP:", 0
Mus100Str:
    db "100", 0
    org $29, $7d00
Mus2Line:                   ; HL = string ($00-terminated, $FD = line break), DE = first cell; like Stub_PrintZ
    push bc
    push hl
    ld a, VWF_BANK
    ld hl, VWF_Print2
    call FarCall
    add sp, 2
    pop bc
    ret

; --- shop "sold out" row (41:49EB): DE-source copy of 41:70E1 to HL -> VWF
    org $29, $49eb
    ld d, h
    ld e, l
    ld hl, $70e1
    call Stub_PrintZ
    jr @+3
    nop

; --- character item list (shop Sell etc., 41:5674): 16 cells from $C54F, $00 padded with spaces -> blank the
;     16 cells, then VWF
    org $29, $5674
    push hl
    ld c, $10
    ld a, $20
.sellfill:
    ld [hli], a
    dec c
    jr nz, .sellfill
    pop de
    ld hl, $c54f
    call Stub_PrintZ

; --- number printer 0:0FE9, digit store loop (0:10A4): VWF first; the loop always ends at the end of the
;     digit buffer ($FFC1), so the count in B and the 'skip $00' check are not needed
    org 0, $10a4
    call Stub_Num
    ret c
.numl:
    ld a, [hli]
    ld [de], a
    inc de
    ld a, l
    cp $c2
    ret z
    jr .numl
    ret
    ds 5, $00
    assert @ == $10b7, "number loop size"

; --- party list (39:4931): skip the redraw when nothing changed (VWF_PartyHit), snapshot after a real draw
    org $27, $4930
    call Party_Entry
    ret c
    push bc
    nop
    org $27, $4989
    jp Party_End
    nop
    nop
; --- party list separators (27:49C3 '/', 27:4A1C '+'/'-' and 27:4A28 '-' (poisoned) over the '/' cell) -> VWF
    org $27, $49c3
    call PLSlash
    nop
    org $27, $4a1c
    call PLSign             ; Z: '+' (record +$6A bit 7 clear), else '-'
    ds 6, $00
    org $27, $4a28
    call PLMinus
    nop
    org $27, $7f40
PLSlash:                    ; DE = cell -> DE + 1; HL kept
    push hl
    ld hl, PLSlashText
    call Stub_PrintZ
    pop hl
    ret
PLSign:                     ; the cell before DE; DE kept
    push hl
    ld hl, PLPlusText
    jr z, .p
    ld hl, PLMinusText
.p: dec de
    call Stub_PrintZ
    pop hl
    ret
PLMinus:                    ; the cell before DE; DE ends on it (as the original)
    push hl
    dec de
    ld hl, PLMinusText
    call Stub_PrintZ
    dec de
    pop hl
    ret
PLSlashText:
    db "/", 0
PLPlusText:
    db "+", 0
PLMinusText:
    db "-", 0
    assert @ <= $8000, "bank 27 overflow"

; --- event party list (bank-45 twin of 27:4931, magic circle 'Who will step inside?'): '/' 2D:7B4E (then an
;     attribute $80 at the cell), '+'/'-' 2D:7BAA, poison '-' 2D:7BB6 -> VWF (attribute written first, the VWF
;     keeps the cell's attribute bits)
    org $2d, $7b4e
    call EvSlash
    ds 12, $00
    org $2d, $7baa
    call EvSign
    ds 6, $00
    org $2d, $7bb6
    call EvMinus
    nop
    org $2d, $7b93          ; status word (Japanese table 2D:7ADF + 5k, copied by 2D:7BE5) -> English, 4 cells
    call EvStatus
    org $2d, $7f00
EvSlash:                    ; DE = cell -> DE + 1; HL kept
    push hl
    push de
    ld hl, $0400
    add hl, de
    ld [hl], $80
    pop de
    ld hl, EvSlashText
    call Stub_PrintZ
    pop hl
    ret
EvSign:
    push hl
    ld hl, EvPlusText
    jr z, .p
    ld hl, EvMinusText
.p: dec de
    call Stub_PrintZ
    pop hl
    ret
EvMinus:
    push hl
    dec de
    ld hl, EvMinusText
    call Stub_PrintZ
    dec de
    pop hl
    ret
EvStatus:                   ; HL = Japanese word 2D:7ADF + 5k: 4 fixed cells via Stub_Fix (FixMap, fixtables.json
    push de                 ; bank 45), not the name printer (which blanks one cell per character); DE, BC kept
    call Stub_Fix
    db 4
    pop de
    ret
EvSlashText:
    db "/", 0
EvPlusText:
    db "+", 0
EvMinusText:
    db "-", 0
    assert @ <= $8000, "bank 45 overflow"

    org $27, $7f00
Party_Entry:                ; returns carry = skip; C = 0, B kept, HL = $CB85 like the original (its caller
    push bc                 ; uses B after the call)
    ld a, VWF_BANK
    ld hl, VWF_PartyHit
    call FarCall            ; L = 1: skip
    ld a, l
    pop bc
    ld c, 0
    ld hl, $cb85
    rra
    ret
Party_End:                  ; the original end (restore SVBK), snapshot, then pop bc / ret at $498F
    pop af
    ldh [$9d], a
    ldh [$70], a
    ld a, VWF_BANK
    ld hl, VWF_PartySnap
    call FarCall
    jp $498e

; --- $F8 number insert (0:1D66): pad the right-aligned digits with $7F (blank glyph 5 px wide, like a digit)
;     instead of $20 (3 px), so typewriter number columns line up (battle/maze party lists)
    org 0, $1d7f
    ld a, $7f

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
    jp $1448

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

; --- bank-0 stub area 2: Rev 1 has no free block here any more; the original monster-panel routine 0:19B4-1A3A
;     is dead (VWF_Panel replaces its only call, 22:5688), its tail at 1A3B is shared and stays
    org 0, $19b4
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
    jp z, $178c
    jp $173f
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
    jp $1448

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
Stub_WrapCmp:               ; 0:1D1E ({FA} look-ahead result): C = characters up to the next break, counted as
    ld a, c                 ; 8 px cells by the game; the VWF averages ~5 px, so count 3/4 cell per character
    ld b, a                 ; (6 px, slightly generous). Carry = the word does not fit in the row.
    srl a
    srl a
    cpl
    inc a
    add b
    ld c, a
    ld a, [$c1c5]
    ld b, a
    ld a, [$c1c3]
    sub b
    sub c
    ret
    assert @ <= $1a3b, "bank0 stub area 2 overflow (Rev 1: the dead monster-panel routine 0:19B4-1A3A)"

; =====================================================================
; Bank $40: engine
; =====================================================================
    org VWF_BANK, $4000
FontAdv:
    incbin "../build/font_adv.bin"      ; 128 bytes (codes $00-$7F; callers mask with $7F)
FontRows:
    incbin "../build/font_rows.bin"     ; 128 * 8 bytes
Pool:
    incbin "../build/pool.bin"          ; POOL_SIZE codes
PoolEnd:
PoolFlags:
    incbin "../build/poolflags.bin"     ; 256 bytes: nonzero = code is a VWF slot
PoolMask:
    incbin "../build/poolmask.bin"      ; 32 bytes: bit (code & 7) of byte code/8 = code is a VWF slot
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
    ldh a, [hDstHi]
    cp $90
    jr nc, .split
    ld a, 2                 ; VRAM1:$8800 (museum monster room, unsigned tiles) -> layout 2
    ld [wLayout], a
    jr .nb
.split:
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
    ldh a, [hDstVBank]      ; VRAM1 destination ($8000/$8400): layout 2 (museum monster room); a VRAM0 load
    or a                    ; after it returns to a $9000 layout (low codes are VRAM0 $9000 in flat and split)
    ld a, 2
    jr nz, .setl
    ld a, [wLayout]
    cp 2
    jr nz, .keepl
    xor a
.setl:
    ld [wLayout], a
.keepl:
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
    cp $5e
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
    ld a, $5e
    ld [wMagic + 1], a
    ld a, 1
    ld [wReset], a          ; shadows are not valid yet
    xor a
    ld [wRC_valid], a       ; redraw cache (shadow area, random at power-on)
    call NCClear
    xor a
    ld [wLowOnly], a
    ld [wPL_valid], a
    ld [wPL_pend], a
    ld a, MAP_BANK          ; slot owners (bank 6, $d800 + code*2): 0 = no text cell (random at power-on)
    ldh [hSVBK], a
    ldh [$70], a
    ld hl, $d800            ; + wVer, wHIdx, wHIdx2 ($DA00-$DCFF)
    ld bc, $0500
.zo: xor a
    ld [hli], a
    dec bc
    ld a, b
    or c
    jr nz, .zo
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
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
    and $7f                 ; font tables hold codes $00-$7F
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
    ; d = shift table page for S_px (right part; +1 = spill into the next tile), bc = S_cur
    ld a, [S_px]
    add a
    add high(ShiftTab)
    ld d, a
    ld bc, S_cur
    ld a, [hli]
    or a
    jr z, .s0
    push hl
    ld l, a
    ld h, d
    ld a, [bc]
    or [hl]
    ld [bc], a
    inc h
    ld a, c
    add 8
    ld c, a
    ld a, [bc]
    or [hl]
    ld [bc], a
    ld a, c
    sub 8
    ld c, a
    pop hl
.s0: inc c
    ld a, [hli]
    or a
    jr z, .s1
    push hl
    ld l, a
    ld h, d
    ld a, [bc]
    or [hl]
    ld [bc], a
    inc h
    ld a, c
    add 8
    ld c, a
    ld a, [bc]
    or [hl]
    ld [bc], a
    ld a, c
    sub 8
    ld c, a
    pop hl
.s1: inc c
    ld a, [hli]
    or a
    jr z, .s2
    push hl
    ld l, a
    ld h, d
    ld a, [bc]
    or [hl]
    ld [bc], a
    inc h
    ld a, c
    add 8
    ld c, a
    ld a, [bc]
    or [hl]
    ld [bc], a
    ld a, c
    sub 8
    ld c, a
    pop hl
.s2: inc c
    ld a, [hli]
    or a
    jr z, .s3
    push hl
    ld l, a
    ld h, d
    ld a, [bc]
    or [hl]
    ld [bc], a
    inc h
    ld a, c
    add 8
    ld c, a
    ld a, [bc]
    or [hl]
    ld [bc], a
    ld a, c
    sub 8
    ld c, a
    pop hl
.s3: inc c
    ld a, [hli]
    or a
    jr z, .s4
    push hl
    ld l, a
    ld h, d
    ld a, [bc]
    or [hl]
    ld [bc], a
    inc h
    ld a, c
    add 8
    ld c, a
    ld a, [bc]
    or [hl]
    ld [bc], a
    ld a, c
    sub 8
    ld c, a
    pop hl
.s4: inc c
    ld a, [hli]
    or a
    jr z, .s5
    push hl
    ld l, a
    ld h, d
    ld a, [bc]
    or [hl]
    ld [bc], a
    inc h
    ld a, c
    add 8
    ld c, a
    ld a, [bc]
    or [hl]
    ld [bc], a
    ld a, c
    sub 8
    ld c, a
    pop hl
.s5: inc c
    ld a, [hli]
    or a
    jr z, .s6
    push hl
    ld l, a
    ld h, d
    ld a, [bc]
    or [hl]
    ld [bc], a
    inc h
    ld a, c
    add 8
    ld c, a
    ld a, [bc]
    or [hl]
    ld [bc], a
    ld a, c
    sub 8
    ld c, a
    pop hl
.s6: inc c
    ld a, [hli]
    or a
    jr z, .s7
    push hl
    ld l, a
    ld h, d
    ld a, [bc]
    or [hl]
    ld [bc], a
    inc h
    ld a, c
    add 8
    ld c, a
    ld a, [bc]
    or [hl]
    ld [bc], a
    ld a, c
    sub 8
    ld c, a
    pop hl
.s7: inc c
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
    ld a, [S_imm]           ; typewriter leaving a cell without ink (a space): blank it like the original,
    or a                    ; which wrote a space tile into every cell it passed
    jr z, .nc
    ld a, [S_slot]
    or a
    jr nz, .nc
    call NextCellBlank
    jr .ncd
.nc:
    call NextCell
.ncd:
    ld a, [S_imm]
    or a
    jr z, .adv
    call CommitIfInk        ; spill-over pixels visible right away
    jr .adv

; ---------------------------------------------------------------------
; Move to the next cell: cur <- nxt, nxt <- 0, slot <- 0
NextCell:
    ld a, [wDedNew]
    or a
    jr z, .nd
    xor a
    ld [wDedNew], a
    ld a, [S_slot]
    or a
    jr z, .nd
    ld a, [wLowOnly]
    or a
    jr nz, .nd
    ld a, [wPanel]
    or a
    call z, Dedupe          ; finished cell with a new slot: share an identical tile if one is on screen
.nd:
    ld hl, S_cellLo
    inc [hl]
    jr nz, .n
    inc hl
    inc [hl]
.n: ld hl, S_col
    inc [hl]
    xor a
    ld [S_slot], a
    ld a, [S_nxt + 0]
    ld [S_cur + 0], a
    ld a, [S_nxt + 1]
    ld [S_cur + 1], a
    ld a, [S_nxt + 2]
    ld [S_cur + 2], a
    ld a, [S_nxt + 3]
    ld [S_cur + 3], a
    ld a, [S_nxt + 4]
    ld [S_cur + 4], a
    ld a, [S_nxt + 5]
    ld [S_cur + 5], a
    ld a, [S_nxt + 6]
    ld [S_cur + 6], a
    ld a, [S_nxt + 7]
    ld [S_cur + 7], a
    xor a
    ld [S_nxt + 0], a
    ld [S_nxt + 1], a
    ld [S_nxt + 2], a
    ld [S_nxt + 3], a
    ld [S_nxt + 4], a
    ld [S_nxt + 5], a
    ld [S_nxt + 6], a
    ld [S_nxt + 7], a
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
    ld a, [S_slot]
    call SharedClear
    ld a, 1
    ld [wDedNew], a
    jr .have
.reuse:
    ld [S_slot], a
    ld a, [wLowOnly]
    or a
    jr z, .ro
    ld a, [S_slot]
    bit 7, a
    jr z, .ro
    xor a                   ; low-only print: the cell's high slot is not usable
    ld [S_slot], a
    jr .new
.ro:
    call SharedDiff         ; content changes: take a new slot (rows copied by scrolling or a shared tile may
                            ; still show the old one; GC frees it once nothing does)
    jr z, .rk
    xor a
    ld [S_slot], a
    jr .new
.rk:
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
    ld a, [S_slot]          ; stamp: drawn now
    ld l, a
    ld h, high(wStamp)
    ld a, [$c00a]
    ld c, a
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ld [hl], c
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ; build the 2bpp tile in wUp (ink -> colour 3, paper -> colour 2, like the original font)
    ld a, [S_cur + 0]
    ld [wUp + 0], a
    ld a, [S_cur + 1]
    ld [wUp + 2], a
    ld a, [S_cur + 2]
    ld [wUp + 4], a
    ld a, [S_cur + 3]
    ld [wUp + 6], a
    ld a, [S_cur + 4]
    ld [wUp + 8], a
    ld a, [S_cur + 5]
    ld [wUp + 10], a
    ld a, [S_cur + 6]
    ld [wUp + 12], a
    ld a, [S_cur + 7]
    ld [wUp + 14], a
    ld a, $ff
    ld [wUp + 1], a
    ld [wUp + 3], a
    ld [wUp + 5], a
    ld [wUp + 7], a
    ld [wUp + 9], a
    ld [wUp + 11], a
    ld [wUp + 13], a
    ld [wUp + 15], a
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
    call HashCur            ; wHash[slot] = hash of the tile (for Dedupe)
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
    ld a, [S_attr]
    and $f7
    or c
    ld c, a                 ; c = attribute
    ld a, [S_cellLo]
    ld l, a
    ld a, [S_cellHi]
    ld h, a
    ld a, 3                 ; bank 3 for both writes
    ldh [hSVBK], a
    ldh [$70], a
    ld [hl], b
    set 2, h                ; +$400: attributes
    ld [hl], c
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret

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
    cp 2
    ld a, b
    jr nz, .n2
    ld c, $08               ; layout 2: tile = code, VRAM bank 1 ($8000+)
    ret
.n2:
    bit 7, a
    ret z                   ; codes < $80: VRAM0:$9000 in flat and split
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

; A = code. Returns A = code if owner[code] == current cell, else 0. One bank-6 visit.
CheckOwner:
    ld [wTmp2], a
    ld l, a
    ld h, 0
    add hl, hl
    ld a, h
    add high($d800)
    ld h, a                 ; owner entry $d800 + code*2
    ld a, [S_cellLo]
    ld c, a
    ld a, [S_cellHi]
    ld b, a
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ld a, [hli]
    cp c
    jr nz, .x
    ld a, [hl]
    cp b
    jr nz, .x
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ld a, [wTmp2]
    ret
.x: ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    xor a
    ret

; owner[code] = current cell, cellmap[cell] = code (code in A). One bank-6 visit.
SetOwner:
    ld [wTmp2], a
    call CellMapAddr        ; hl = cellmap entry
    push hl
    ld a, [wTmp2]
    ld l, a
    ld h, 0
    add hl, hl
    ld a, h
    add high($d800)
    ld h, a                 ; owner entry
    ld a, [S_cellLo]
    ld c, a
    ld a, [S_cellHi]
    ld b, a
    ld a, [wTmp2]
    ld e, a
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ld [hl], c
    inc hl
    ld [hl], b
    pop hl
    ld [hl], e
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret

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
    call EpochBump
    call VerBump
    ld l, a
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl              ; code*16
    ld c, 0
    push af
    ld a, [wLayout]
    cp 2
    jr nz, .nl2
    pop af
    ld de, $8000            ; layout 2: VRAM1:$8000 + code*16
    add hl, de
    ld c, 1
    jr .go
.nl2:
    pop af
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
    ld hl, wGameNew
    ld b, 32
.cn: ld [hli], a
    dec b
    jr nz, .cn
    ld [wRC_valid], a
    ld [wPL_valid], a
    ld hl, wEpoch
    inc [hl]
    jp NCClear

AllocScan:
    call TryAlloc
    ret c
    call GC
    call TryAlloc
    ret c
    ld a, [wLayout]         ; museum monster room: pages are built in one buffer while the other (list) is
    cp 2                    ; still shown. Pass 3 drops the BG's text (the window counts); pass 2 drops a
    jr nz, .p2              ; hidden window's text. A print into the window: 3 then 2; into the BG: 2 then 3.
    ld a, [S_cellHi]
    and $fc
    cp $d8
    jr nz, .bgfirst
    call .pass3
    ret c
    jr .p2
.bgfirst:                   ; a BG print (the list). Under the shown page first only recent BG text counts
    ldh a, [$ff40]          ; (the list rows the game redraws while paging), then the window's older text
    bit 5, a                ; goes (the page closing or hidden; text drawn in the last STAMP_KEEP frames
    jr z, .bg3              ; stays), the BG counts
    ldh a, [$ff4a]
    cp 144
    jr nc, .bg3
    ld a, [wMusClose]       ; closing: the page goes, the list it uncovers stays
    cp $5a
    jr z, .bg3
    ld a, 4
    ld [wGCSkipWin], a
    call GC
    xor a
    ld [wGCSkipWin], a
    call TryAlloc
    ret c
.bg3:
    ld a, 3
    ld [wGCSkipWin], a
    call GC
    xor a
    ld [wGCSkipWin], a
    call TryAlloc
    ret c
    jr .ring
.pass3:
    ld a, 2
    ld [wGCSkipWin], a
    call GC
    xor a
    ld [wGCSkipWin], a
    jp TryAlloc
.pass2:
    ld a, 1
    ld [wGCSkipWin], a
    call GC
    xor a
    ld [wGCSkipWin], a
    jp TryAlloc
.p2:
    ld a, 1                 ; still dry: try again without a hidden window's text
    ld [wGCSkipWin], a
    call GC
    xor a
    ld [wGCSkipWin], a
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

; carry set + A = code on success. wLowOnly: low codes preferred, any free slot if none is (the inn and shop
; pictures fill the low codes; the last-resort ring would overwrite visible tiles)
TryAlloc:
    call TryAlloc1
    ret c
    ld a, [wLowOnly]
    or a
    ret z
    xor a
    ld [wLowOnly], a
    call TryAlloc1
    push af
    ld a, 1
    ld [wLowOnly], a
    pop af
    ret

TryAlloc1:                  ; free = PoolMask & ~wBits, searched a byte (8 codes) at a time from wNextB
    ld a, [wLowOnly]
    or a
    jr nz, TryAllocLow
    ld a, [wNextB]
    and $1f
    ld e, a
    ld d, 32
.l: ld hl, PoolMask
    ld a, l
    add e
    ld l, a
    jr nc, .p
    inc h
.p: ld c, [hl]              ; slots in this byte
    ld a, low(wBits)
    add e
    ld l, a
    ld h, high(wBits)
    ld a, [hl]
    cpl
    and c
    jr nz, .found
    ld a, e
    inc a
    and $1f
    ld e, a
    dec d
    jr nz, .l
    and a
    ret
.found:                     ; lowest free bit
    ld b, 0
    ld c, 1
.lb: rrca
    jr c, .got
    inc b
    sla c
    jr .lb
.got:
    ld a, [hl]
    or c
    ld [hl], a
    ld a, e
    inc a                   ; next search starts at the next byte (spreads reuse like the old ring: cached
    and $1f                 ; boxes keep their slots longer)
    ld [wNextB], a
    ld a, e
    add a
    add a
    add a
    add b                   ; code = byte*8 + bit
    scf
    ret

TryAllocLow:                ; wLowOnly: only codes < $80 (VRAM0 in both layouts), ring order
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
    ld a, [wLowOnly]
    or a
    jr z, .any
    ld a, [wTmp2]
    bit 7, a
    jr nz, .used
.any:
    ld a, [wTmp2]
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
    and 7
    add low(BitMask)
    ld l, a
    ld h, high(BitMask)
    ld b, [hl]
    ld a, c
    rrca
    rrca
    rrca
    and $1f
    add low(wBits)
    ld l, a
    ld h, high(wBits)
    ret

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
    cp $fd                  ; unidentified names hold a line break ('Robed/figure'): a space here, the
    jr nz, .cp1             ; panel splits by width itself
    ld a, $20
.cp1: ld [de], a
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
    jp c, .group
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
    jp $1443

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
    jr z, .end
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
    and $7f                 ; font tables hold codes $00-$7F
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
.end:                       ; the whole name fits in row 1 (80 px): no break ('Eye Wing' on one line)
    ld a, b
    cp 81
    ret nc
    xor a
    ld [wPanW], a
    ret

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
; Maze view graphics loaded (MazeHdma, 20:4100-4240): VRAM0/VRAM1 $8000-$8FFF now hold the view, so Camp's
; flat font (VRAM0 $8800) is gone and the game is back to its split text: the dungeon messages, prompts and
; menus use codes < $80 with the attribute bank bit for the upper half (VRAM1 $9000), like the frame 7D'-7F'
; the game redraws. No font load marks the return (the split font in VRAM1 $9000 survived Camp), so wLayout
; stayed 0 and flat slots $80-$EF (VRAM0 $8800-$8EFF = the wall/floor tiles) took the text: stairs prompt
; in the front wall after a step, 'Pick a lock' in the view strip.
; =====================================================================
VWF_MazeSplit:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ld a, [wLayout]
    cp 1
    jr z, .out
    ld a, 1
    ld [wLayout], a
    ld [wReset], a          ; like a font load: shadows/caches/reservations restart at the next Alloc
    ld hl, wUp              ; VRAM1 tile $20 (code $A0) = blank paper, as the split font load does
    ld b, 8
.bt: xor a
    ld [hli], a
    dec a
    ld [hli], a
    dec b
    jr nz, .bt
    ld a, $a0
    call Upload
.out:
    pop af
    jp SetSVBK

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
    ld b, a
    ld a, [wLayout]
    cp 2
    ld a, b
    jr nz, .nl2
    inc c                   ; layout 2: VRAM1 $8000 + code*16
    ld de, $8000
    jr .add
.nl2:
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
    call EpochBump
    ld a, [wTmp2]
    call VerBump
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
    ld h, high(wGameNew)
    ld a, l
    add low(wGameNew)
    ld l, a
    ld a, [hl]
    or b
    ld [hl], a              ; and kept through the next GC (wGameNew)
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
; Notice Board (2B:57C0): the scroll is one picture with the Japanese text drawn into it. After the fade-in
; (trampoline 2B:7F00) the text area (rows 2-15, cols 2-17 of the BG buffer) is blanked to paper (tile $20,
; palette 5: palette 6's colour 3 is nearly the paper colour) and the English lines (script/notice.json -> NoticeRows/NoticeText) are printed.
; =====================================================================
VWF_Notice:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ld hl, NoticeBody
    call PrivCall
    pop af
    jp SetSVBK

NoticeBody:
    ld hl, $d000 + 2*32 + 2
    ld c, 14
.row:
    push hl
    ld b, 16
.cell:
    ld a, $20
    call Write3
    push hl
    ld de, $0400
    add hl, de
    call Read3
    and $80                 ; no flip, VRAM0, palette 5: same paper (colour 2) as palette 6, dark ink (colour 3)
    or $05
    call Write3
    pop hl
    inc hl
    dec b
    jr nz, .cell
    pop hl
    ld de, 32
    add hl, de
    dec c
    jr nz, .row
    ; lines (index in B on the stack: VWF_PrintBuf uses every register and the wDed* variables)
    ld b, 0
.line:
    ld a, b
    cp NOTICE_LINES
    ret nc
    ld e, a
    ld d, 0
    ld hl, NoticeRows
    add hl, de
    ld a, [hl]
    cp $ff
    ret z
    push bc
    ; de = $D000 + row*32 + NOTICE_COL
    ld l, a
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    ld de, $d000 + NOTICE_COL
    add hl, de
    push hl
    ; copy NoticeText + 28*i to wNameBuf
    ld l, b
    ld h, 0
    add hl, hl
    add hl, hl              ; *4
    ld d, h
    ld e, l
    add hl, hl              ; *8
    add hl, de              ; *12
    add hl, hl              ; *24
    add hl, de              ; *28
    ld de, NoticeText
    add hl, de
    ld de, wNameBuf
.cp: ld a, [hli]
    ld [de], a
    inc de
    or a
    jr nz, .cp
    pop de
    call VWF_PrintBuf
    pop bc
    inc b
    jr .line

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
    ld de, $6c95
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

; A = code -> HL = wShared byte, B = mask
SharedAddr:
    call BitAddr
    ld a, l
    sub low(wBits)
    add low(wShared)
    ld l, a
    ld h, high(wShared)
    ret

SharedClear:
    call SharedAddr
    ld a, b
    cpl
    and [hl]
    ld [hl], a
    ret

; NZ if the content changes AND the tile may be shown elsewhere: shared (Dedupe) or the same tile code in the
; same column 1-2 rows above/below (a row copied by scrolling, e.g. the inn level-up lines). Otherwise in-place
; reuse stays allowed: screens the game restores from a saved copy rely on stable slot numbers.
SharedDiff:
    call ContentDiff
    ret z
    ld a, [S_slot]
    call SharedAddr
    ld a, [hl]
    and b
    ret nz
    ; same tile one or two rows away in the same column?
    ld a, [S_cellLo]
    ld l, a
    ld a, [S_cellHi]
    ld h, a
    call Read3
    ld c, a                 ; tile code this cell shows now
    ld de, -64
    call .near
    ret nz
    ld de, -32
    call .near
    ret nz
    ld de, 32
    call .near
    ret nz
    ld de, 64
.near:
    push hl
    add hl, de
    call Read3
    pop hl
    cp c
    jr z, .y
    xor a
    ret
.y: or 1
    ret

; NZ if S_cur differs from the shadow of [S_slot] (ink bytes = even shadow bytes)
ContentDiff:
    ld a, [S_slot]
    call StagingAddr
    ld de, S_cur
    ld b, 8
.c: ld a, [de]
    cp [hl]
    ret nz
    inc de
    inc hl
    inc hl
    dec b
    jr nz, .c
    xor a
    ret

; wHash[S_slot] = hash of S_cur (the ink rows; paper is constant)
HashCur:
    push bc
    push de
    push hl
    ld hl, S_cur
    ld b, 8
    xor a
.h: rlca
    xor [hl]
    inc hl
    dec b
    jr nz, .h
    ld b, a
    ld a, [S_slot]
    ld e, a
    ld d, 0
    ld hl, wHash
    add hl, de
    ld [hl], b
    ; hash index: wHIdx[hash] = slot, the previous holder moves to wHIdx2[hash]
    ld l, b
    ld h, high(wHIdx)
    call Read6
    ld c, a
    ld a, [S_slot]
    cp c
    jr z, .hx
    call Write6
    inc h                   ; wHIdx2
    ld a, c
    call Write6
.hx:
    pop hl
    pop de
    pop bc
    ret

; The cell at S_cell (slot S_slot) is finished. If another slot in use holds an identical tile (same hash, same
; shadow, VRAM valid), point the cell at that slot and free ours. Shared slots get no owner (owner $FFFF), so
; nobody rewrites them in place. Keeps busy screens (lists with repeated digits/words) inside the pool.
Dedupe:
    ld a, [wReset]          ; font load pending: the VRAM-valid flags are stale (cleared at the next Alloc)
    or a
    ret nz
    ld a, [S_slot]
    ld [wDedS], a
    ld e, a
    ld d, 0
    ld hl, wHash
    add hl, de
    ld a, [hl]
    ld [wDedH], a
    xor a
    ld [wDedI], a
.l: ld a, [wDedI]           ; candidates: wHIdx[hash], then wHIdx2[hash] (was: a scan of the whole pool)
    cp 2
    ret nc
    inc a
    ld [wDedI], a
    ld b, a
    ld a, [wDedH]
    ld l, a
    ld h, high(wHIdx)
    dec b
    jr z, .i1
    inc h
.i1: call Read6
    ld c, a
    or a
    jr z, .l
    ld d, 0
    ld a, [wDedS]
    cp c
    jr z, .l
    ld a, [TW_ctx + 1]      ; the typewriter's current cell is still being drawn
    cp c
    jr z, .l
    ld e, c
    ld hl, wHash
    add hl, de
    ld a, [wDedH]
    cp [hl]
    jr nz, .l
    ld a, c
    call BitAddr            ; in use?
    ld a, [hl]
    and b
    jr z, .l
    ld a, c
    call ValidAddr          ; VRAM holds its shadow?
    ld a, [hl]
    and b
    jr z, .l
    ; compare the two shadows
    ld a, c
    call StagingAddr
    ld d, h
    ld e, l
    ld a, [wDedS]
    push de
    call StagingAddr
    pop de
    ld b, 16
.cmp: ld a, [de]
    cp [hl]
    jr nz, .l
    inc de
    inc hl
    dec b
    jr nz, .cmp
    ; found: cell -> candidate
    ld a, c
    ld [wTmp2], a
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
    call Read3
    and $f7
    or c
    call Write3
    ld a, [wTmp2]           ; candidate: shared (its owner may still redraw it, but only unchanged)
    call SharedAddr
    ld a, [hl]
    or b
    ld [hl], a
    ld a, [wDedS]           ; our slot: free it if it is still ours alone (owner = this cell)
    call OwnerAddr
    call Read6
    ld b, a
    ld a, [S_cellLo]
    cp b
    ret nz
    inc hl
    call Read6
    ld b, a
    ld a, [S_cellHi]
    cp b
    ret nz
    dec hl
    xor a
    call Write6
    inc hl
    call Write6
    ld a, [wDedS]
    call BitAddr
    ld a, b
    cpl
    and [hl]
    ld [hl], a
    ret

; Rebuild the bitmap from what the bank-3 buffers reference, plus the game's graphics reservations.
; Reservations (wGame) live only while a buffer still shows the slot: the full first pass keeps the reserved
; slots it found referenced (it counts BG rows under the window, so the maze keeps its wall tiles while the
; dungeon menu hides the view) and drops the rest; DMAs since the last GC (wGameNew) survive one GC unchecked
; (the cells are written after the tiles). Before 2026-11-11 reservations stayed until the next font load and
; filled the pool in the maze/town: every glyph ran both GC passes (slowdown) and the dry pass overwrote
; wall tiles (text in the walls, garbled Camp numbers).
GC:
    ld hl, wGCCount
    inc [hl]
    ld hl, GCB
    ld b, 32
    xor a
.z: ld [hli], a
    dec b
    jr nz, .z
    call GCScan
    call GCFlush            ; wBits |= the marks GCRowMark made in WRAM0
    ld hl, wGame
    ld de, wBits
    ld bc, wGameNew
    ld a, [wGCSkipWin]
    or a
    jr nz, .p2
.p1: ld a, [de]             ; wGame = (wGame & referenced) | wGameNew; wGameNew = 0; wBits |= wGame
    and [hl]
    push hl
    ld h, b
    ld l, c
    or [hl]
    ld [hl], 0
    pop hl
    ld [hli], a
    push hl
    ld h, d
    ld l, e
    or [hl]
    ld [hl], a
    pop hl
    inc de
    inc bc
    ld a, e
    cp low(wBits) + 32
    jr nz, .p1
    ret
.p2: ld a, [bc]             ; dry pass: reservations still count (wGame | wGameNew), nothing is dropped
    or [hl]
    push hl
    ld h, d
    ld l, e
    or [hl]
    ld [hl], a
    pop hl
    inc hl
    inc de
    inc bc
    ld a, e
    cp low(wBits) + 32
    jr nz, .p2
    ret

GCScan:
    ldh a, [$ff43]          ; SCX: first visible BG column
    srl a
    srl a
    srl a
    ld [wGCcol0], a
    ld de, wBits
    ld b, 32
    xor a
.gz: ld [de], a
    inc de
    dec b
    jr nz, .gz
    ; (the print-burst hold that reserved the old screen's slots from wKeep is gone: HoldMark is disabled)
.nk:
    ld a, [S_slot]
    or a
    call nz, MarkCode
    ld a, [TW_ctx + 1]
    or a
    call nz, MarkCode
    ; BG: only the rows above a full-width window are visible (rows under it are old screens)
    ld bc, 18*32
    ld a, [wGCSkipWin]      ; BG rows under a full-width window count, except in the dry second pass: they come
    or a                    ; back when the window closes ('Cast the spell on whom?' under the spell detail box)
    jr z, .bg
    cp 2
    jr z, .bgown            ; third pass (museum): BG text reclaimable
    cp 3
    jr z, .bg               ; museum BG print: the BG counts
    cp 4
    jr z, .bgstamp          ; museum BG print under the shown page: only recent BG text counts
    ldh a, [$ff40]
    bit 5, a
    jr z, .bg
    ldh a, [$ff4b]
    cp 8
    jr nc, .bg              ; window not covering the full width
    ldh a, [$ff4a]
    cp 144
    jr nc, .bg
    add 7
    and $f8                 ; rows above the window = ceil(WY/8); *32 = *4 of the pixel value
    ld l, a
    ld h, 0
    add hl, hl
    add hl, hl
    ld b, h
    ld c, l
    push bc
    ld a, b
    or c
    jr z, .noabove
    ld hl, $d000
    call .scan2             ; rows above the window: everything
.noabove:
    pop bc
    ld hl, $d000            ; rows under it: only game graphics (slots no text cell owns, e.g. the maze walls)
    add hl, bc
    ld a, low(18*32)
    sub c
    ld c, a
    ld a, high(18*32)
    sbc b
    ld b, a
    call .ownerless
    jr .bgskip
.bg:
    ld hl, $d000
    call .scan2
    jr .bgskip
.bgstamp:
    ld hl, $d000
    ld bc, 18*32
    ld a, 2
    call .filtered
    jr .bgskip
.bgown:                     ; third pass: no BG cell counts (the game's own tiles stay reserved by wGame; the
                            ; list's restored cells have no owner entry, so an ownerless scan kept them all)
.bgskip:
    ; normally the window buffer always counts (the game types screens into it before showing them, e.g.
    ; the disarm trap list). Second pass when the pool is dry: a hidden window does not count (battle hides
    ; the party list with WX=167 and re-sends/redraws it before showing it again)
    ld a, [wGCSkipWin]
    or a
    jr z, .win
    cp 2
    jr z, .win              ; third pass: the window being built counts
    cp 3
    jr z, .winown           ; museum BG print: the window's older text goes, shown or not
    cp 4
    jr z, .win              ; museum BG print under the shown page: the page counts
    ldh a, [$ff40]
    bit 3, a                ; BG shows the $9C00 map (= this buffer, e.g. camp spell screens)
    jr nz, .win
    bit 5, a
    jr z, .winown
    ldh a, [$ff4b]
    cp 167
    jr nc, .winown
    ldh a, [$ff4a]
    cp 144
    jr c, .win
.winown:                    ; hidden window: only its game graphics count
    ld hl, $d800
    ld bc, 18*32
.ownerless:                 ; scan BC cells at HL marking only slots without an owning text cell
    ld a, 1
.filtered:                  ; A = wGCOwnerless mode for this scan: GCRowMark collects the codes in GCB (emptied
    ld [wGCOwnerless], a    ; first), GCFilter keeps those the mode marks (one owner/stamp check per code)
    push bc
    push hl
    call GCFlush
    pop hl
    pop bc
    call .scan2
    call GCFilter
    call GCFlush
    xor a
    ld [wGCOwnerless], a
    ret
.win:
    ld hl, $d800
.scan:                      ; 18 rows x 32 cells at HL (bank 3; what the game's GDMA copies), attributes at HL+$400
    ld bc, 18*32
.scan2:                     ; HL = row start (32-aligned), BC = cells (a multiple of 32)
    ld a, c                 ; rows = BC / 32
    srl b
    rra
    srl b
    rra
    srl b
    rra
    srl b
    rra
    srl b
    rra
    or a
    ret z
    ld [wGCrows], a
.row:
    push hl                 ; row start
    xor a                   ; only the 21 visible columns count: columns 20-31 are off screen and hold
    ld [wGCc], a            ; uninitialised RAM on many screens (it held ~80 slots as 'in use')
    ld [wGCchk], a
    ld a, 21
    ld [wGCn], a
    ld a, h
    and $08
    jr nz, .chk             ; window buffer ($D800-$DBFF): columns 0-20
    ld a, [wGCcol0]         ; BG with SCX = 0: columns 0-20. Otherwise columns 0-20 and SCX/8.. +20: a
    or a                    ; raster split (battle: the monster area scrolls, the party panel below does
    jr z, .chk              ; not) makes SCX read mid-frame wrong for some rows
    ld a, 32
    ld [wGCn], a
    ld [wGCchk], a
.chk:
    ld a, [wGCchk]          ; columns 0-20 (any pass; GCSlot handles the ownerless modes): the fast row loop
    or a
    jr nz, .l
    pop hl
    push hl
    ld a, [wLayout]         ; layout 0/1: marks in WRAM0 without leaving bank 3 (GCFilter after ownerless scans)
    cp 2
    jr nc, .old
    ld c, a
    call GCRowMark
    jp .rowdone
.old:
    call GCRowFast
    jp .rowdone
.l: pop hl
    push hl
    ld a, [wGCchk]
    or a
    jr z, .cin
    ld a, [wGCc]
    cp 21
    jr c, .cin
    ld b, a
    ld a, [wGCcol0]
    cpl
    inc a
    add b
    and $1f
    cp 21
    jp nc, .skip
.cin:
    ld a, [wGCc]
    add l
    ld l, a
    ld a, 3                 ; code and attribute in one bank-3 window (inlined Read3)
    ldh [hSVBK], a
    ldh [$70], a
    ld e, [hl]              ; code
    ld a, h
    add 4
    ld h, a
    ld d, [hl]              ; attr (HL stays at the attribute, as before)
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ld b, high(MaybeSlot)   ; codes that are never a slot (frames, spaces, most game tiles): nothing to mark
    ld c, e
    ld a, [bc]
    or a
    jp z, .skip
    call GCSlot
.skip:
    ld a, [wGCc]
    inc a
    and $1f
    ld [wGCc], a
    ld hl, wGCn
    dec [hl]
    jp nz, .l
.rowdone:
    pop hl
    ld de, 32
    add hl, de
    ld a, [wGCrows]
    dec a
    ld [wGCrows], a
    jp nz, .row
    ret

; GC fast row (columns 0-20, SCX = 0 or the window buffer, normal pass): HL = row start. WRAM bank 3 stays
; mapped while cells that can never be a slot are skipped (most of them: frames, spaces, game tiles); only the
; others switch to the home bank for GCSlot.
GCRowFast:
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
    ld b, 21
.f: ld a, [hli]
    ld e, a
    ld d, high(MaybeSlot)
    ld a, [de]
    or a
    jr nz, .slot
.n: dec b
    jr nz, .f
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret
.slot:
    push bc
    push hl
    dec hl
    ld a, h
    add 4
    ld h, a
    ld d, [hl]              ; attribute (bank 3)
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    call GCSlot
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
    pop hl
    pop bc
    jr .n

; GC fast row, normal pass (wGCOwnerless = 0), layout C = 0 (flat) or 1 (split): HL = row start. Bank 3 stays
; mapped: the slot code comes from the cell's code and attribute (GCSlot's rules) and is marked in GCB (WRAM0;
; GC ORs it into wBits). Only a cell in the other layout's reading (owner check, bank 6) goes through GCSlot.
GCRowMark:
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
    ld b, 21
.f: ld a, [hli]
    ld e, a
    ld d, high(MaybeSlot)
    ld a, [de]
    or a
    jr nz, .slot
.n: dec b
    jr nz, .f
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret
.slot:
    dec hl
    set 2, h                ; attribute (+$400)
    ld d, [hl]
    res 2, h
    inc hl
    ld a, c
    or a
    jr z, .flat
    bit 3, d                ; split: VRAM1 code < $70 = slot code | $80; VRAM0 low code = itself; VRAM0 $80+ =
    ld a, e                 ; the flat reading (owner check)
    jr z, .s0
    cp $70
    jr nc, .n
    or $80
    jr .mk
.s0: bit 7, a
    jr z, .mk
    jr .slow
.flat:
    bit 3, d                ; flat: VRAM0 = itself; VRAM1 code < $70 = the split reading (owner check)
    ld a, e
    jr z, .mk
    cp $70
    jr nc, .n
.slow:
    push bc
    push hl
    dec hl
    set 2, h
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    call GCSlot
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
    pop hl
    pop bc
    jr .n
.mk: push hl                ; GCB[code >> 3] |= 1 << (code & 7)
    ld l, a
    ld h, high(GCMaskTab)
    ld e, [hl]
    inc h                   ; GCByteTab
    ld l, [hl]
    ld h, high(GCB)
    ld a, [hl]
    or e
    ld [hl], a
    pop hl
    jr .n

; wBits |= GCB, GCB = 0
GCFlush:
    ld hl, GCB
    ld de, wBits
    ld b, 32
.m: ld a, [de]
    or [hl]
    ld [de], a
    xor a
    ld [hli], a
    inc de
    dec b
    jr nz, .m
    ret

; after an ownerless scan (wGCOwnerless 1 or 2): keep in GCB only the codes GCSlot's rules mark in that mode
; (1: no owning text cell, or text drawn in the last STAMP_KEEP frames; 2: that recent text only)
GCFilter:
    ld a, [wGCOwnerless]
    ld [GCF_MODE], a
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ld hl, GCB
    ld e, 0                 ; code of the current bit
.byte:
    ld a, [hl]
    or a
    jr nz, .bits
    ld a, e
    add 8
    ld e, a
    jr .next
.bits:
    ld b, 1
.bit:
    ld a, [hl]
    and b
    jr z, .nb
    call .keep
    jr c, .nb
    ld a, b
    cpl
    and [hl]
    ld [hl], a
.nb: inc e
    sla b
    jr nz, .bit
.next:
    inc hl
    ld a, l
    cp low(GCB) + 32
    jr nz, .byte
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret
.keep:                      ; E = code, bank 6 mapped: carry = mark
    push hl
    ld a, [GCF_MODE]
    cp 2
    jr z, .st
    ld l, e                 ; owner word ($D800 + code * 2)
    ld h, 0
    add hl, hl
    ld a, h
    add $d8
    ld h, a
    ld a, [hli]
    or [hl]
    jr nz, .st
    pop hl
    scf
    ret
.st:
    ld l, e
    ld h, high(wStamp)
    ld a, [$c00a]
    sub [hl]
    pop hl
    cp STAMP_KEEP           ; carry = drawn in the last STAMP_KEEP frames
    ret

; GC: mark the slot a cell shows. E = code, D = attribute, HL = the cell's attribute address (bank 3 + $400);
; home bank mapped. Current layout as before; the other layout's reading counts only for cells that own the slot
; (a font load can switch the layout while text drawn under the other one is still on screen: battle spell list).
GCSlot:
    ld a, [wLayout]
    or a
    jr z, .flat
    cp 2
    jr nz, .sp
    bit 3, d                ; layout 2: VRAM1 cells hold the code itself; VRAM0 cells are graphics
    ld a, e
    jr nz, .mk
    ret
.sp:
    bit 3, d                ; split
    ld a, e
    jr z, .s0
    cp $70
    ret nc
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
    ret nc
    or $80                  ; VRAM1 tile: split reading
.other:
    ld [wTmp2], a
    ld a, h
    sub 4
    ld b, a                 ; bc = cell address
    ld c, l
    ld a, [wTmp2]
    call OwnerAddr
    call Read6
    cp c
    ret nz
    inc hl
    call Read6
    cp b
    ret nz
    ld a, [wTmp2]
.mk:
    ld [wTmp2], a
    ld a, [wGCOwnerless]
    or a
    jr z, .mk2
    cp 2
    jr z, .stamp            ; stamp only (museum: restored list cells have no owner entry)
    ld a, [wTmp2]
    call OwnerAddr
    call Read6
    ld b, a
    inc hl
    call Read6
    or b
    jr z, .mk2              ; no text cell owns it: game graphics, keep
.stamp:
    ld a, [wTmp2]           ; text: reclaimable in the dry pass unless drawn in the last STAMP_KEEP frames (the
    ld l, a                 ; museum builds its page in the hidden window and would lose its own labels)
    ld h, high(wStamp)
    call Read6
    ld b, a
    ld a, [$c00a]
    sub b
    cp STAMP_KEEP
    ret nc
.mk2:
    ld a, [wTmp2]
    jp MarkCode

; =====================================================================
; Typewriter entry (from 0:1c2a). B = character. Caller saved HL.
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
; Rect blit (0:1789/0:173C via Stub_RectCommon). Returns DE = destination + h*32 like the original blitter
; (2C:498C returns right after a blit and its caller prints at that DE).
VWF_Rect:
    call VWF_RectBody
    ldh a, [hSrcBank]
    ld b, a
    ldh a, [hSrcLo]
    ld l, a
    ldh a, [hSrcHi]
    ld h, a
    inc hl
    call VWF_Fetch          ; A = h
    ld l, a
    ld h, 0
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    add hl, hl
    ldh a, [hDstLo]
    add l
    ld e, a
    ldh a, [hDstHi]
    adc h
    ld d, a
    ret
VWF_RectBody:
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
    call RectCacheHit
    jr nc, .render
    pop af                  ; same box, same place, cells and tiles unchanged: nothing to draw
    jp SetSVBK
.render:
    xor a
    ld [wRC_valid], a
    ldh a, [hSrcBank]
    ld [wRC_srcBank], a
    ldh a, [hSrcLo]
    ld [wRC_srcLo], a
    ldh a, [hSrcHi]
    ld [wRC_srcHi], a
    ldh a, [hDstLo]
    ld [wRC_dstLo], a
    ldh a, [hDstHi]
    ld [wRC_dstHi], a
    ld a, [R_mode]
    ld [wRC_mode], a
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
    call RectCacheSave
    pop af
    jp SetSVBK

; carry = the last rendered rect is asked for again (source, destination, mode), no tile was uploaded or
; overwritten since (wEpoch) and every cell of the box still holds the saved code or was cleared to $20 (the
; town clears the info box before each redraw) with its attributes unchanged. Cleared cells are restored.
RectCacheHit:
    ld a, [wReset]          ; font loaded since: the saved slots are gone. Reset now (see PLHit): a redraw that
    or a                    ; reuses its own slots never allocates, and the flag would make every redraw miss
    jr z, .nr
    call AllocReset
    jr .miss
.nr:
    ld a, [wRC_valid]
    or a
    ret z
    ld hl, wRC_srcBank
    ldh a, [hSrcBank]
    cp [hl]
    jr nz, .miss
    inc hl
    ldh a, [hSrcLo]
    cp [hl]
    jr nz, .miss
    inc hl
    ldh a, [hSrcHi]
    cp [hl]
    jr nz, .miss
    inc hl
    ldh a, [hDstLo]
    cp [hl]
    jr nz, .miss
    inc hl
    ldh a, [hDstHi]
    cp [hl]
    jr nz, .miss
    inc hl
    ld a, [R_mode]
    cp [hl]
    jr nz, .miss
    ld a, [wEpoch]
    ld hl, wRC_epoch
    cp [hl]
    jr nz, .miss
    ld b, 4                 ; attributes unchanged?
    call RectSum
    ld hl, wRC_sumA
    call Cmp16
    jr nz, .miss
    ld b, 0
    call RectSum            ; codes: as rendered -> nothing to do
    ld hl, wRC_sumC
    call Cmp16
    jr z, .hit
    ld hl, wRC_sumB         ; every code $20 (the town clears the box before each redraw) -> restore
    call Cmp16
    jr nz, .miss
    call RectRestore
.hit:
    scf
    ret
.miss:
    and a
    ret

; Z if DE == [HL] (16 bit, little endian)
Cmp16:
    ld a, [hli]
    cp e
    ret nz
    ld a, [hl]
    cp d
    ret

; DE = Fletcher sum (d += byte, e += d) over the cached box in bank 3; B = 0: codes, 4: attributes
RectSum:
    ld a, [wRC_w]
    ld [RC_SCRW], a
    ld a, [wRC_dstLo]
    ld l, a
    ld a, [wRC_dstHi]
    add b
    ld h, a
    ld a, [wRC_h]
    ld b, a
; HL = first cell (bank 3), B = rows, [RC_SCRW] = width -> DE = Fletcher sum
SumRegion:
    ld de, 0
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
.r: ld a, [RC_SCRW]
    ld c, a
.c: ld a, [hli]
    add d
    ld d, a
    add e
    ld e, a
    dec c
    jr nz, .c
    ld a, [RC_SCRW]
    cpl
    inc a
    add 32
    add l
    ld l, a
    jr nc, .n
    inc h
.n: dec b
    jr nz, .r
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret

; write the saved codes back into the cached box (bank 3) through the WRAM0 scratch
RectRestore:
    ld a, [wRC_w]
    ld [RC_SCRW], a
    ld c, a
    ld a, [wRC_h]
    ld b, a
    xor a
.m: add c
    dec b
    jr nz, .m
    ld c, a                 ; w*h <= RC_MAX
    ld hl, wRC_cells
    ld de, RC_SCR
.cp: ld a, [hli]
    ld [de], a
    inc de
    dec c
    jr nz, .cp
    ld a, [wRC_dstLo]
    ld l, a
    ld a, [wRC_dstHi]
    ld h, a
    ld a, [wRC_h]
    ld b, a
    ld de, RC_SCR
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
.r: ld a, [RC_SCRW]
    ld c, a
.c: ld a, [de]
    inc de
    ld [hli], a
    dec c
    jr nz, .c
    ld a, [RC_SCRW]
    cpl
    inc a
    add 32
    add l
    ld l, a
    jr nc, .n
    inc h
.n: dec b
    jr nz, .r
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ; a GC since the save may have freed the box's slots while it was cleared: mark them in use again
    ld a, [wGCCount]
    ld hl, wRC_gc
    cp [hl]
    ret z
    ld a, 1
    ld [wTmp3], a           ; RectWalk pass 1 also marks
    jp RectWalk

RectCacheSave:
    ld a, [wRC_dstHi]
    and $f0
    cp $d0                  ; only boxes drawn into the bank-3 buffers
    ret nz
    ld a, [R_w]
    or a
    ret z
    ld [wRC_w], a
    ld c, a
    ld a, [R_h]
    or a
    ret z
    ld [wRC_h], a
    ld b, a
    xor a
.m: add c                   ; w*h <= RC_MAX
    jr c, .big
    dec b
    jr nz, .m
    cp RC_MAX + 1
    jr nc, .big
    ld a, 2
    ld [wTmp3], a           ; pass 2: save
    call RectWalk
    ld b, 0
    call RectSum
    ld a, e
    ld [wRC_sumC], a
    ld a, d
    ld [wRC_sumC + 1], a
    ld b, 4
    call RectSum
    ld a, e
    ld [wRC_sumA], a
    ld a, d
    ld [wRC_sumA + 1], a
    ld a, [wRC_w]           ; sum of the same box with every code $20
    ld c, a
    ld a, [wRC_h]
    ld b, a
    xor a
.m2: add c
    dec b
    jr nz, .m2
    ld b, a
    ld de, 0
.bs: ld a, $20
    add d
    ld d, a
    add e
    ld e, a
    dec b
    jr nz, .bs
    ld a, e
    ld [wRC_sumB], a
    ld a, d
    ld [wRC_sumB + 1], a
    ld a, [wGCCount]
    ld [wRC_gc], a
    ld a, [wEpoch]
    ld [wRC_epoch], a
    ld a, 1
    ld [wRC_valid], a
.big:
    ret

; Walk the cached box. wTmp3: 0 = check (carry = every cell is the saved code or $20, attributes equal),
; 1 = restore the saved codes, 2 = save codes and attributes.
RectWalk:
    ld a, [wRC_dstLo]
    ld l, a
    ld a, [wRC_dstHi]
    ld h, a
    ld de, wRC_cells
    ld a, [wRC_h]
    ld b, a
.r: push hl
    ld a, [wRC_w]
    ld c, a
.c: ld a, [wTmp3]
    cp 1
    jr z, .rest
    jr nc, .save
    ; check
    call Read3
    push hl
    ld h, d
    ld l, e
    cp [hl]
    jr z, .ok
    cp $20
    jr nz, .bad
.ok: pop hl
    push hl
    ld a, h
    add 4
    ld h, a
    call Read3
    ld h, d
    ld l, e
    push de
    ld de, wRC_attrs - wRC_cells
    add hl, de
    pop de
    cp [hl]
    jr nz, .bad
    pop hl
    jr .next
.bad:
    pop hl
    pop hl
    and a
    ret
.rest:                      ; (only after a GC since the save: the codes are already in the cells) mark in use
    push bc
    push de
    push hl
    call CellCode
    call BitAddr
    ld a, [hl]
    or b
    ld [hl], a
    pop hl
    pop de
    pop bc
    jr .next
.save:
    call Read3
    ld [de], a
    push hl
    ld a, h
    add 4
    ld h, a
    call Read3
    ld h, d
    ld l, e
    push de
    ld de, wRC_attrs - wRC_cells
    add hl, de
    pop de
    ld [hl], a
    pop hl
.next:
    inc hl
    inc de
    dec c
    jr nz, .c
    pop hl
    ld a, l
    add 32
    ld l, a
    jr nc, .nc
    inc h
.nc: dec b
    jr nz, .r
    scf
    ret

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
    jr z, .sx1              ; no ink in the current cell: the loop below blanks it (see .eol)
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
    jr z, .fill             ; no ink in the current cell (at most the 1-px advance): .fill blanks it - skipping it
.adv1:                      ; left an older text's tile there (26:729B 'Choose a class.' showed 'classsir')
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
    ld e, a
    ld a, [wLayout]
    cp 2
    ld a, e
    jr nz, .bl0
    or $08                  ; layout 2: blank = VRAM1 font space
.bl0:
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
    call FixFind
    jr nc, .raw
    ld a, [wInBank]
    push af
    ld a, [wFixTB]
    ld [wInBank], a         ; DE destination (bit 7 clear)
    call InlineBody
    pop af
    ld [wInBank], a
    jr .done
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
    xor a
    ld [wNC_px], a
    push de
    call NameCacheHit       ; same name at the same cells, tiles unchanged: restore, no render
    pop de                  ; (NameCacheHit uses DE; PrintBuf needs the destination)
    jr c, .hit
    ld hl, VWF_PrintBuf
    call PrivCall
    push de                 ; DE = the cell after the text: the game's copy loops leave DE there and some
    call NameCacheSave      ; callers print next to it (inn: name + ' gained a level!')
    pop de
    jr .done
.hit:
    ld a, [wNC_n]           ; restored: start + the entry's cells
    add e
    ld e, a
    jr nc, .done
    inc d
.done:
    pop hl
    pop af
    jp SetSVBK

; ---------------------------------------------------------------------
; Numbers (0:0FE9 via Stub_Num): DE = next cell after the padding the game skipped, C = low byte of the first
; digit ($FF00+C .. $FFC1), [$FFAC] = digit count or (bit 7) the field width, [$FFAE/F] = field start.
; Right-aligned in the field when the game padded it or gave it a fixed width; else left-aligned.
VWF_Num:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ld a, e
    ld [wN_de], a
    ld a, d
    ld [wN_deHi], a
    ld a, c
    ld [wN_dig], a
    ld a, 1
    ld [wN_done], a
    ; 0:0FE9's caller (after our push af): [sp+4] bank (FarCall), [sp+5] Stub_Num's FarCall return,
    ; [sp+7] return into 0:10A7, [sp+9] 0:0FE9's caller
    ld hl, sp, 4
    ld a, [hl]
    ld [wN_cb], a
    ld hl, sp, 9
    ld a, [hli]
    ld [wN_cr], a
    ld a, [hl]
    ld [wN_cr + 1], a
    ld hl, NumBody
    call PrivCall
    ld a, [wN_dig]
    ld c, a
    ld a, [wN_done]
    ld l, a
    or a
    jr z, .keep
    ld a, [wN_end]
    ld e, a
    ld a, [wN_end + 1]
    ld d, a
    jr .r
.keep:
    ld a, [wN_de]
    ld e, a
    ld a, [wN_deHi]
    ld d, a
.r: pop af
    jp SetSVBK

NumBody:
    ld a, [wN_dig]
    ld c, a
    ld a, $c2
    sub c
    ld [wN_cnt], a
    ld b, a
    ld de, wNameBuf
    ld l, c
    ld h, $ff
.cp: ld a, [hli]
    ld [de], a
    inc de
    dec b
    jr nz, .cp
    xor a
    ld [de], a
    ldh a, [$ae]
    ld [wN_st], a
    ldh a, [$af]
    ld [wN_st + 1], a
    ldh a, [$ac]
    bit 7, a
    jr z, .nb
    and $7f
    ld [wN_cells], a
    jr .right
.nb: ld a, [wN_st]
    ld b, a
    ld a, [wN_de]
    sub b                   ; padding cells the game skipped
    jr z, .left
    ld b, a
    ld a, [wN_cnt]
    add b
    ld [wN_cells], a
    jr .right
.left:
    ld a, [wN_cnt]
    ld [wN_cells], a
    xor a
    jr .x
.right:
    call NumWidth
    ld b, a
    ld a, [wN_cells]
    add a
    add a
    add a
    sub b
    jr nc, .x
    xor a
.x: ld [wN_x], a
    ; fields the game overwrites with 8 px text afterwards keep the 8 px digits (NumExcl)
    call NumExcluded
    jr nc, .ok
    xor a
    ld [wN_done], a
    ld a, [wN_st]           ; clear the VRAM1 bit left by an earlier VWF print in these cells
    ld l, a
    ld a, [wN_st + 1]
    add 4
    ld h, a
    ld a, [wN_cells]
    ld b, a
.cb: call Read3
    and $f7
    call Write3
    inc hl
    dec b
    jr nz, .cb
    ret
.ok:
    ; end = start + cells
    ld a, [wN_st]
    ld l, a
    ld a, [wN_st + 1]
    ld h, a
    ld a, [wN_cells]
    ld e, a
    ld d, 0
    add hl, de
    ld a, l
    ld [wN_end], a
    ld a, h
    ld [wN_end + 1], a
    ; first cell = start + x/8, start pixel x&7
    ld a, [wN_st]
    ld l, a
    ld a, [wN_st + 1]
    ld h, a
    ld a, [wN_x]
    ld c, a
    srl a
    srl a
    srl a
    ld e, a
    ld d, 0
    add hl, de
    ld a, c
    and 7
    ld [wNC_px], a
    ld d, h
    ld e, l
    push de
    call NameCacheHit       ; unchanged since the last print: nothing to do (the padding cells stay blank)
    pop de
    ret c
    ; blank the field's cells (codes only), then render
    ld a, [wN_st]
    ld l, a
    ld a, [wN_st + 1]
    ld h, a
    ld a, [wN_cells]
    ld b, a
.bl: call Blank3
    inc hl
    dec b
    jr nz, .bl
    push de
    ld a, [wLayout]
    ld [wLowOnly], a
    call NumPrint
    xor a
    ld [wLowOnly], a
    pop de
    jp NameCacheSave

; carry = the caller (wN_cb:wN_cr) is in NumExcl
NumExcluded:
    ld hl, NumExcl
.l: ld a, [hli]
    or a
    ret z                   ; (carry clear)
    ld b, a
    ld a, [wN_cb]
    cp b
    jr nz, .n2
    ld a, [wN_cr]
    cp [hl]
    jr nz, .n2
    inc hl
    ld a, [wN_cr + 1]
    cp [hl]
    jr nz, .n1
    scf
    ret
.n2: inc hl
.n1: inc hl
    jr .l

NumExcl:                    ; bank, return address of 0:0FE9 calls that stay 8 px; 0 ends
    db 0                    ; (empty since 2026-11-12: the card age moved to cols 17-18, clear of the shop header)

; A = pixel width of wNameBuf
NumWidth:
    ld hl, wNameBuf
    ld c, 0
.w: ld a, [hli]
    or a
    jr z, .e
    push hl
    and $7f                 ; font tables hold codes $00-$7F
    ld e, a
    ld d, 0
    ld hl, FontAdv
    add hl, de
    ld a, c
    add [hl]
    ld c, a
    pop hl
    jr .w
.e: ld a, c
    ret

; print wNameBuf at cell DE starting at pixel wNC_px
NumPrint:
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
    ld a, [wNC_px]
    ld [S_px], a
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
    ret z
.adv:
    jp NextCell

; ---------------------------------------------------------------------
; Party list (39:4931 via 39:7F00). The game clears the party rows and redraws all of them on every main-loop
; pass (6 names + 12 numbers through the VWF). If the shown party data is unchanged, no tile changed since
; (wEpoch), no font load is pending and the rows are either still as drawn or exactly as the game left them
; before the last real draw, the drawn rows are restored and the routine is skipped (B = 1).
VWF_PartyHit:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    call PLHit
    ld l, 0
    jr nc, .r
    inc l
.r: pop af
    jp SetSVBK

VWF_PartySnap:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call PLSnap
    pop af
    jp SetSVBK

; DE = Fletcher sum over the party members' name, status, HP and marker bytes (+ count)
PLData:
    ld a, [$cb85]
    ld b, a
    ld d, a
    ld e, a
    or a
    ret z
    ld hl, $c880
.m: push hl
    ld c, 8
    call .add               ; name
    pop hl
    push hl
    ld a, l
    add $0c
    ld l, a
    ld c, 1
    call .add               ; status
    pop hl
    push hl
    ld a, l
    add $62
    ld l, a
    ld c, 4
    call .add               ; HP, max HP
    pop hl
    push hl
    ld a, l
    add $6a
    ld l, a
    ld c, 1
    call .add
    pop hl
    ld a, l
    add $80
    ld l, a
    jr nc, .nc
    inc h
.nc: dec b
    jr nz, .m
    ret
.add:
    ld a, [hli]
    add d
    ld d, a
    add e
    ld e, a
    dec c
    jr nz, .add
    ret

; DE = sum of the party rows' codes (B = 0) or attributes (B = 4): SumRegion's Fletcher sum, 4 cells per loop
PLSum:
    ld hl, PL_ROW0
    ld a, h
    add b
    ld h, a
    ld de, 0
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
    ld b, 6
.r: ld c, 5
.c: ld a, [hli]
    add d
    ld d, a
    add e
    ld e, a
    ld a, [hli]
    add d
    ld d, a
    add e
    ld e, a
    ld a, [hli]
    add d
    ld d, a
    add e
    ld e, a
    ld a, [hli]
    add d
    ld d, a
    add e
    ld e, a
    dec c
    jr nz, .c
    ld a, l
    add 12
    ld l, a
    jr nc, .n
    inc h
.n: dec b
    jr nz, .r
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret

; carry = skip the draw (rows restored if needed); else note the rows as the game left them for the snapshot.
; The town clears the box every main-loop pass before this draw: the codes are put back from the change list
; (PLRestore), the attributes only when the game changed them too.
PLHit:
    ld a, [wReset]          ; font load since the snapshot: do the pending allocator reset now (drops this cache,
    or a                    ; bumps wEpoch). Leaving it to the next Alloc is not enough: a redraw that reuses every
    jr z, .nr               ; cell's own slot never allocates, so the flag stayed set and every pass missed
    call AllocReset         ; (town at 1/4 speed after the tavern/temple menus until the inn, triage 2026-11-12)
    jr .miss
.nr:
    ld a, [wPL_valid]
    or a
    jr z, .miss
    ld a, [wEpoch]
    ld hl, wPL_epoch
    cp [hl]
    jr nz, .miss
    call PLData
    ld hl, wPL_data
    call Cmp16
    jr nz, .miss
    ld b, 4
    call PLSum
    ld hl, wPL_sumA
    call Cmp16
    ld c, 0                 ; C = 0: attributes as drawn
    jr z, .attrsDrawn
    ld hl, wPL_sumBA
    call Cmp16
    jr nz, .miss
    inc c                   ; C = 1: as the game left them, restore them
.attrsDrawn:
    push bc
    ld b, 0
    call PLSum
    pop bc
    ld hl, wPL_sumC
    call Cmp16
    jr z, .codesDrawn
    ld hl, wPL_sumB
    call Cmp16
    jr nz, .miss
    call PLRestore
    jr .hit
.codesDrawn:
    ld a, c
    or a
    jr z, .hit
    ld hl, wPL_attrs
    ld de, PL_ROW0 + $400
    call PLRestore.put
.hit:
    scf
    ret
.miss:
    xor a
    ld [wPL_valid], a
    ld b, 0
    call PLSum
    ld a, e
    ld [wPL_sumB], a
    ld a, d
    ld [wPL_sumB + 1], a
    ld b, 4
    call PLSum
    ld a, e
    ld [wPL_sumBA], a
    ld a, d
    ld [wPL_sumBA + 1], a
    ld hl, PL_ROW0          ; the codes before the draw (PLSnap lists the cells the draw changes)
    ld de, wPL_codes
    call PLSnap.copy
    ld a, 1
    ld [wPL_pend], a
    and a
    ret

; after a real draw: snapshot the rows into bank 6 (attributes; codes plus the list of cells the draw changed)
; and remember the sums
PLSnap:
    ld a, [wPL_pend]
    or a
    ret z
    xor a
    ld [wPL_pend], a
    ld hl, PL_ROW0 + $400
    ld de, wPL_attrs
    call .copy
    call .list
    ld b, 0
    call PLSum
    ld a, e
    ld [wPL_sumC], a
    ld a, d
    ld [wPL_sumC + 1], a
    ld b, 4
    call PLSum
    ld a, e
    ld [wPL_sumA], a
    ld a, d
    ld [wPL_sumA + 1], a
    call PLData
    ld a, e
    ld [wPL_data], a
    ld a, d
    ld [wPL_data + 1], a
    ld a, [wGCCount]
    ld [wPL_gc], a
    ld a, [wEpoch]
    ld [wPL_epoch], a
    ld a, 1
    ld [wPL_valid], a
    ret
.list:                      ; codes now -> RC_SCR; bank 6: list (offset, code) of the cells that differ from the
    ld hl, PL_ROW0          ; codes before the draw (wPL_codes), then keep the codes now in wPL_codes
    call .in
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
    xor a
    ld [PL_OFF], a
    ld [PL_CNT], a
    ld hl, RC_SCR
    ld de, wPL_codes
    ld bc, wPL_list
.lr: ld a, 20
    ld [PL_COL], a
.lc: ld a, [de]
    cp [hl]
    jr z, .same
    ld a, [PL_CNT]
    cp PL_MAX
    jr nc, .ovf
    inc a
    ld [PL_CNT], a
    ld a, [PL_OFF]
    ld [bc], a
    inc bc
    ld a, [hl]
    ld [bc], a
    inc bc
    jr .same
.ovf: ld a, $ff             ; too many: PLRestore copies all 120 codes
    ld [PL_CNT], a
.same:
    ld a, [hli]
    ld [de], a
    inc de
    ld a, [PL_OFF]
    inc a
    ld [PL_OFF], a
    ld a, [PL_COL]
    dec a
    ld [PL_COL], a
    jr nz, .lc
    ld a, [PL_OFF]
    add 12
    ld [PL_OFF], a
    cp 6 * 32
    jr nz, .lr
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ld a, [PL_CNT]
    ld [wPL_n], a
    ret
.copy:                      ; 6 rows x 20 cells from HL (bank 3) to DE (bank 6), through the WRAM0 scratch
    push de
    call .in
    pop de
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ld hl, RC_SCR
    ld c, 120
.w: ld a, [hli]
    ld [de], a
    inc de
    dec c
    jr nz, .w
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret
.in:                        ; 6 rows x 20 cells from HL (bank 3) to RC_SCR; leaves bank 3 mapped
    ld de, RC_SCR
    ld b, 6
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
.r: ld c, 20
.c: ld a, [hli]
    ld [de], a
    inc de
    dec c
    jr nz, .c
    ld a, l
    add 12
    ld l, a
    jr nc, .n
    inc h
.n: dec b
    jr nz, .r
    ret

; put the drawn codes back (change list, or all 120 when it overflowed), the attributes too when C != 0; after a
; GC since the snapshot, mark the slots in use
PLRestore:
    ld a, c
    or a
    jr z, .codes
    ld hl, wPL_attrs
    ld de, PL_ROW0 + $400
    call .put
.codes:
    ld a, [wPL_n]
    cp $ff
    jr nz, .list
    ld hl, wPL_codes
    ld de, PL_ROW0
    call .put
    jr .mark
.list:
    or a
    jr z, .mark
    ld b, a
    add a
    ld c, a
    ld hl, wPL_list         ; gather the list (bank 6) into the WRAM0 scratch
    ld de, RC_SCR
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
.g2: ld a, [hli]
    ld [de], a
    inc de
    dec c
    jr nz, .g2
    ld a, 3                 ; scatter into the rows (bank 3)
    ldh [hSVBK], a
    ldh [$70], a
    ld hl, RC_SCR
.s: ld a, [hli]
    add low(PL_ROW0)
    ld e, a
    ld a, high(PL_ROW0)
    adc 0
    ld d, a
    ld a, [hli]
    ld [de], a
    dec b
    jr nz, .s
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
.mark:
    ld a, [wGCCount]
    ld hl, wPL_gc
    cp [hl]
    ret z
    ld [hl], a
    ld hl, PL_ROW0
    ld b, 6
.mr: ld c, 20
.mc: push bc
    push hl
    call CellCode
    call BitAddr
    ld a, [hl]
    or b
    ld [hl], a
    pop hl
    pop bc
    inc hl
    dec c
    jr nz, .mc
    ld a, l
    add 12
    ld l, a
    jr nc, .mn
    inc h
.mn: dec b
    jr nz, .mr
    ret
.put:                       ; 120 bytes from HL (bank 6) to the rows at DE (bank 3)
    push de
    ld de, RC_SCR
    ld c, 120
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
.g: ld a, [hli]
    ld [de], a
    inc de
    dec c
    jr nz, .g
    pop hl
    ld de, RC_SCR
    ld b, 6
    ld a, 3
    ldh [hSVBK], a
    ldh [$70], a
.r: ld c, 20
.c: ld a, [de]
    inc de
    ld [hli], a
    dec c
    jr nz, .c
    ld a, l
    add 12
    ld l, a
    jr nc, .n
    inc h
.n: dec b
    jr nz, .r
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    ret

; ---------------------------------------------------------------------
; Two rows of 8 cells at DE / DE+$20 (museum monster page): string at the caller's HL (same frame as VWF_PrintZ),
; $FD = space; wrapped at the last space that keeps row 1 within 64 px.
VWF_Print2:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ld hl, sp, 4
    ld b, [hl]              ; caller ROM bank
    ld hl, sp, 7
    ld a, [hli]
    ld h, [hl]
    ld l, a
    ld c, low(wNameBuf)
.c: call FetchSrc
    cp $fd
    jr nz, .nf
    ld a, $20
.nf:
    push hl
    ld h, high(wNameBuf)
    ld l, c
    ld [hl], a
    pop hl
    inc c
    or a
    jr nz, .c
    ld a, e
    ld [wN_st], a
    ld a, d
    ld [wN_st + 1], a
    ld hl, Print2Body
    call PrivCall
    pop af
    jp SetSVBK

Print2Body:
    ; blank both rows (8 cells each)
    ld a, [wN_st]
    ld l, a
    ld a, [wN_st + 1]
    ld h, a
    push hl
    ld b, 8
.b1: call Blank3
    inc hl
    dec b
    jr nz, .b1
    pop hl
    ld de, $0020
    add hl, de
    ld b, 8
.b2: call Blank3
    inc hl
    dec b
    jr nz, .b2
    ; split index: last space with the width before it <= 64 (c = index, b = width); 0 = no break
    xor a
    ld [wPanW], a
    ld hl, wNameBuf
    ld bc, 0
.w: ld a, [hli]
    or a
    jr z, .wd
    cp $20
    jr nz, .wa
    ld a, b
    cp 65
    jr nc, .wa0
    ld a, c
    ld [wPanW], a
.wa0:
    ld a, $20
.wa:
    push hl
    and $7f
    ld e, a
    ld d, 0
    ld hl, FontAdv
    add hl, de
    ld a, [hl]
    pop hl
    add b
    ld b, a
    inc c
    jr .w
.wd:
    ld a, b                 ; fits in one row: no break
    cp 65
    jr nc, .two
    xor a
    ld [wPanW], a
.two:
    ; row 1
    ld a, [wN_st]
    ld e, a
    ld a, [wN_st + 1]
    ld d, a
    ld hl, wNameBuf
    ld a, [wPanW]
    ld c, a
    call .print
    ld a, [wPanW]
    or a
    ret z
    ; row 2 from the character after the space
    ld e, a
    ld d, 0
    ld hl, wNameBuf + 1
    add hl, de
    ld a, [wN_st]
    add $20
    ld e, a
    ld a, [wN_st + 1]
    adc 0
    ld d, a
    ld c, 0
.print:                     ; HL = text, DE = cell, C = stop index (0 = to the end)
    push hl
    ld h, d
    ld l, e
    push hl
    ld de, $0400
    add hl, de
    call Read3
    pop hl
    call Begin
    xor a
    ld [S_imm], a
    pop hl
    ld b, 0
.pl: ld a, c
    or a
    jr z, .pc
    cp b
    jr z, .pe
.pc: ld a, [hli]
    or a
    jr z, .pe
    push hl
    push bc
    call Glyph
    pop bc
    pop hl
    inc b
    jr .pl
.pe: call CommitIfInk
    ld a, [S_slot]
    or a
    jr nz, .pn
    ld a, [S_px]
    or a
    ret z
.pn: jp NextCell

; [HL] (bank 3) = $20 (blank); layout 2 also sets the cell's VRAM1 bit (the VRAM0 tile $20 is picture there).
; Keeps BC, DE, HL.
Blank3:
    ld a, $20
    call Write3
    ld a, [wLayout]
    cp 2
    ret nz
    push hl
    ld a, h
    add 4
    ld h, a
    call Read3
    or $08
    call Write3
    pop hl
    ret

; ---------------------------------------------------------------------
; Museum monster abilities: rows 12-13 (cols 1-18) list the abilities set in $C536 (bits 0-6), $C537 (drain),
; $C538 (calls help / flees) and $C52F-31 (spells) as words, wrapped at 136 px.
VWF_MusCloseOn:
    ld b, $5a
    jr MusCloseSet
VWF_MusCloseOff:
    ld b, 0
MusCloseSet:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    ld a, b
    ld [wMusClose], a
    pop af
    jp SetSVBK
VWF_MusAbil:
    ldh a, [hSVBK]
    push af
    ld a, HOME_BANK
    call SetSVBK
    pop af
    push af
    ld [wCallerSVBK], a
    call CheckInit
    ld hl, MusAbilBody
    call PrivCall
    pop af
    jp SetSVBK

MusAbilBody:
    ld hl, $d981            ; blank rows 12 and 13, cols 1-18
    ld b, 18
.b1: call Blank3
    inc hl
    dec b
    jr nz, .b1
    ld hl, $d9a1
    ld b, 18
.b2: call Blank3
    inc hl
    dec b
    jr nz, .b2
    ; flags: bits 0-6 = $C536, bit 7 = drain, bit 8 = calls help, bit 9 = flees, bit 10 = spells
    ld a, [$c536]
    and $7f
    ld e, a
    ld a, [$c537]
    or a
    jr z, .f1
    set 7, e
.f1: ld d, 0
    ld a, [$c538]
    and $f0
    jr z, .f2
    set 0, d
.f2: ld a, [$c538]
    and $0f
    jr z, .f3
    set 1, d
.f3: ld a, [$c52f]
    ld b, a
    ld a, [$c530]
    or b
    ld b, a
    ld a, [$c531]
    or b
    jr z, .f4
    set 2, d
.f4: ld a, e
    ld [wMA_f], a
    ld a, d
    ld [wMA_f + 1], a
    ld hl, $d981
    ld a, l
    ld [wN_st], a
    ld a, h
    ld [wN_st + 1], a
    xor a
    ld [wNC_px], a
    ld [wNameBuf], a
    ld [wTmp3], a           ; line width
    ld hl, MusAbilWords
    ld c, 11
.w: ld a, [wMA_f]           ; next flag into carry
    ld b, a
    ld a, [wMA_f + 1]
    srl a
    ld [wMA_f + 1], a
    rr b
    ld a, b
    ld [wMA_f], a
    jr nc, .skip
    push bc
    push hl
    call .add
    pop hl
    pop bc
.skip:                      ; next word
    ld a, [hli]
    or a
    jr nz, .skip
    dec c
    jr nz, .w
    jp .flush
.add:                       ; word at HL: append (a new row when it does not fit 136 px)
    push hl
    call .wordw             ; b = width
    pop hl
    ld a, [wNameBuf]
    or a
    jr z, .fits
    ld a, [wTmp3]
    add 4                   ; space
    add b
    jr c, .nl
    cp 137
    jr c, .sp
.nl:
    push hl
    call .flush
    ld a, [wN_st]           ; next row
    add $20
    ld [wN_st], a
    jr nc, .nc
    ld a, [wN_st + 1]
    inc a
    ld [wN_st + 1], a
.nc:
    xor a
    ld [wNameBuf], a
    ld [wTmp3], a
    pop hl
    jr .fits
.sp:
    push hl
    ld hl, .space
    call .app
    pop hl
.fits:
.app:                       ; append the $00-terminated string at HL to wNameBuf, add its width
    push hl
    call .wordw
    ld a, [wTmp3]
    add b
    ld [wTmp3], a
    pop hl
    ld de, wNameBuf
.e: ld a, [de]
    or a
    jr z, .cp
    inc de
    jr .e
.cp: ld a, [hli]
    ld [de], a
    inc de
    or a
    jr nz, .cp
    ret
.space:
    db " ", 0
.wordw:                     ; B = pixel width of the string at HL
    ld b, 0
.ww: ld a, [hli]
    or a
    ret z
    push hl
    and $7f
    ld e, a
    ld d, 0
    ld hl, FontAdv
    add hl, de
    ld a, b
    add [hl]
    ld b, a
    pop hl
    jr .ww
.flush:                     ; print wNameBuf at the current row
    ld a, [wNameBuf]
    or a
    ret z
    ld a, [wN_st]
    ld e, a
    ld a, [wN_st + 1]
    ld d, a
    jp NumPrint

MusAbilWords:
    db "Poison", 0, "Fear", 0, "Sleep", 0, "Paralyze", 0, "Petrify", 0, "Critical", 0, "Breath", 0
    db "Drain", 0, "Calls help", 0, "Flees", 0, "Spells", 0

; FixMap lookup (bank FIXMAP_BANK, tools/insert.py): $4000 = 65 bucket starts (one per source page $40-$7F +
; end), each bucket = entries [src bank][src lo][text bank][text lo][text hi]. Key wInBank:wInH:wInL.
; Carry + wFixTB/wInLo/wInHi on success. Keeps DE.
FIXMAP_BANK equ $7f
FixFind:
    push de
    ld a, [wInH]
    sub $40
    jr c, .no
    cp $40
    jr nc, .no
    add a
    ld l, a
    ld h, $40
    ld b, FIXMAP_BANK
    call VWF_Fetch
    ld e, a
    call VWF_Fetch
    ld d, a                 ; de = bucket start
    call VWF_Fetch
    ld [wFS_end], a
    call VWF_Fetch
    ld [wFS_end + 1], a
    ld h, d
    ld l, e
.l: ld a, [wFS_end]
    cp l
    jr nz, .go
    ld a, [wFS_end + 1]
    cp h
    jr z, .no
.go:
    ld b, FIXMAP_BANK
    call VWF_Fetch
    ld c, a
    call VWF_Fetch
    ld e, a
    ld a, [wInBank]
    cp c
    jr nz, .n
    ld a, [wInL]
    cp e
    jr nz, .n
    call VWF_Fetch
    ld [wFixTB], a
    call VWF_Fetch
    ld [wInLo], a
    call VWF_Fetch
    ld [wInHi], a
    pop de
    scf
    ret
.n: inc hl
    inc hl
    inc hl
    jr .l
.no:
    pop de
    and a
    ret

; A = code: its tile changed (wVer[code] += 1). Keeps all registers.
VerBump:
    push af
    push hl
    ld l, a
    ld h, high(wVer)
    ld a, MAP_BANK
    ldh [hSVBK], a
    ldh [$70], a
    inc [hl]
    ld a, HOME_BANK
    ldh [hSVBK], a
    ldh [$70], a
    pop hl
    pop af
    ret

NCClear:                    ; n = 0 marks an entry unused
    ld hl, wNC + 2
    ld b, NC_N
    ld de, NC_SIZE
.z: ld [hl], 0
    add hl, de
    dec b
    jr nz, .z
    ret

; wNC_hash = hash of wNameBuf
NameHash:
    ld hl, wNameBuf
    ld de, 0
.l: ld a, [hli]
    or a
    jr z, .e
    sla e
    rl d
    jr nc, .n
    inc e
.n: add e
    ld e, a
    jr nc, .l
    inc d
    jr .l
.e: ld a, [wNC_px]
    add e
    ld [wNC_hash], a
    ld a, d
    ld [wNC_hash + 1], a
    ret

; DE = destination cell. Carry = an entry for this cell and string matches, every cell still holds its code
; (or was cleared to $20) with the same attribute, and no slot was re-uploaded since (wVer): cells restored.
NameCacheHit:
    ld a, e
    ld [wNC_cell], a
    ld a, d
    ld [wNC_cell + 1], a
    call NameHash
    ld a, [wReset]          ; font load pending: slots are gone
    or a
    jr nz, .miss
    ld hl, wNC
    ld c, NC_N
.f: push hl
    ld a, [wNC_cell]
    cp [hl]
    jr nz, .nx
    inc hl
    ld a, [wNC_cell + 1]
    cp [hl]
    jr nz, .nx
    inc hl
    ld a, [hli]
    or a
    jr z, .nx
    ld [wNC_n], a
    ld a, [wNC_hash]
    cp [hl]
    jr nz, .nx
    inc hl
    ld a, [wNC_hash + 1]
    cp [hl]
    jr nz, .nx
    inc hl
    ld a, [hli]
    ld [wTmp1], a           ; the entry's attribute
    ld a, l
    ld [wNC_ep], a
    ld a, h
    ld [wNC_ep + 1], a
    ld a, [wEpoch]
    cp [hl]
    ld a, 0
    jr nz, .slow
    inc a                   ; no upload anywhere since the last check: versions cannot have changed
.slow:
    ld [wNC_fast], a
    inc hl
    pop de
    ld a, l
    ld [wNC_ent], a
    ld a, h
    ld [wNC_ent + 1], a
    xor a
    ld [wNC_pass], a
    ld [wNC_clr], a
    call NCWalk
    jr nc, .miss
    ld a, [wNC_ep]          ; verified: remember the epoch
    ld l, a
    ld a, [wNC_ep + 1]
    ld h, a
    ld a, [wEpoch]
    ld [hl], a
    ld a, [wNC_clr]
    or a
    jr z, .done             ; nothing cleared: the cells already show it
    ld a, 1
    ld [wNC_pass], a
    call NCWalk
.done:
    scf
    ret
.nx: pop hl
    ld de, NC_SIZE
    add hl, de
    dec c
    jr nz, .f
.miss:
    and a
    ret

; after a render: store the cells from wNC_cell to the end cell (S_cellLo) in the entry for this cell (or the
; next round-robin entry)
NameCacheSave:
    ld hl, wNameBuf         ; cells = ceil((start px + width) / 8)
    ld a, [wNC_px]
    ld c, a
    ld b, 0
.w: ld a, [hli]
    or a
    jr z, .we
    push hl
    and $7f                 ; font tables hold codes $00-$7F
    ld e, a
    ld d, 0
    ld hl, FontAdv
    add hl, de
    ld a, [hl]
    pop hl
    add c
    ld c, a
    jr nc, .w
    inc b
    jr .w
.we: ld a, b
    or a
    ret nz                  ; 256 px or more: not cached
    ld a, c
    add 7
    ret c
    srl a
    srl a
    srl a
    ret z
    cp NC_MAXC + 1
    ret nc
    ld [wNC_n], a
    ld a, [wNC_cell + 1]
    and $f0
    cp $d0
    ret nz
    ld hl, wNC
    ld c, NC_N
.f: ld a, [wNC_cell]
    cp [hl]
    jr nz, .nx
    inc hl
    ld a, [wNC_cell + 1]
    cp [hl]
    dec hl
    jr z, .got
.nx: ld de, NC_SIZE
    add hl, de
    dec c
    jr nz, .f
    ld a, [wNCNext]
    inc a
    cp NC_N
    jr c, .r
    xor a
.r: ld [wNCNext], a
    ld hl, wNC
    or a
    jr z, .got
    ld de, NC_SIZE
.m: add hl, de
    dec a
    jr nz, .m
.got:
    ld a, [wNC_cell]
    ld [hli], a
    ld a, [wNC_cell + 1]
    ld [hli], a
    ld a, [wNC_n]
    ld [hli], a
    ld a, [wNC_hash]
    ld [hli], a
    ld a, [wNC_hash + 1]
    ld [hli], a
    push hl
    ld a, [wNC_cell]
    ld l, a
    ld a, [wNC_cell + 1]
    add 4
    ld h, a
    call Read3
    pop hl
    ld [hli], a             ; attribute of the first cell
    ld a, [wEpoch]
    ld [hli], a
    ld a, l
    ld [wNC_ent], a
    ld a, h
    ld [wNC_ent + 1], a
    ld a, 2
    ld [wNC_pass], a
    jp NCWalk

; HL = cell (bank 3) -> A = slot code (split layout: VRAM1 cells are codes $80+), B = attribute. Keeps HL, C, DE.
CellCode:
    push hl
    ld a, h
    add 4
    ld h, a
    call Read3
    pop hl
    ld b, a
    call Read3
    push af
    ld a, [wLayout]
    or a
    jr z, .f
    cp 2
    jr z, .f                ; layout 2: the tile is the code
    bit 3, b
    jr z, .f
    pop af
    or $80
    ret
.f: pop af
    ret

; walk the wNC_n cells from wNC_cell with the entry pairs (slot code, version) at wNC_ent (mode wNC_pass);
; wTmp1 = entry attribute (bank bit ignored)
NCWalk:
    ld a, [wNC_ent]
    ld e, a
    ld a, [wNC_ent + 1]
    ld d, a
    ld a, [wNC_cell]
    ld l, a
    ld a, [wNC_cell + 1]
    ld h, a
    ld a, [wNC_n]
    ld c, a
.k: ld a, [wNC_pass]
    cp 1
    jr z, .rest
    jr nc, .save
    ; check: attribute (without the VRAM bank bit)
    call CellCode
    push af
    ld a, b
    and $f7
    ld b, a
    ld a, [wTmp1]
    and $f7
    cp b
    jr nz, .bad1
    pop af
    ; code: saved, or a cleared cell (tile $20)
    ld b, a
    ld a, [de]
    cp b
    jr z, .cv
    call Read3
    cp $20
    jr nz, .bad
    ld a, 1
    ld [wNC_clr], a
.cv: ld a, [wNC_fast]
    or a
    jr nz, .next
    ld a, [de]              ; version unchanged
    push hl
    ld l, a
    ld h, high(wVer)
    call Read6
    pop hl
    ld b, a
    inc de
    ld a, [de]
    dec de
    cp b
    jr nz, .bad
    jr .next
.rest:
    push bc
    ld a, [de]
    call SlotTile           ; a = tile, c = bank bit
    call Write3
    push hl
    ld a, h
    add 4
    ld h, a
    call Read3
    and $f7
    or c
    call Write3
    pop hl
    ld a, [de]
    push hl
    call BitAddr            ; in use again before the next GC sees the cell
    ld a, [hl]
    or b
    ld [hl], a
    pop hl
    pop bc
    jr .next
.save:
    call CellCode
    ld [de], a
    push hl
    ld l, a
    ld h, high(wVer)
    call Read6
    pop hl
    inc de
    ld [de], a
    dec de
.next:
    inc de
    inc de
    inc hl
    dec c
    jr nz, .k
    scf
    ret
.bad1:
    pop af
.bad:
    and a
    ret

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
    ld a, [wLayout]
    cp 2
    ld a, [S_attr]
    jr z, .l2
    and $f7
    call Write3
    jp NextCell
.l2: or $08                 ; layout 2: blank = VRAM1 font space
    call Write3
    jp NextCell

; Name entry cursor: L = pixel width of the $00-terminated name at $FFA8; with 7 letters (field full) the width
; up to the last letter, so the box sits on it as in the original. HRAM and ROM only (any SVBK).
VWF_NameW:
    ld hl, $ffa8
    ld bc, 0                ; b = letters, c = width
    ld e, 0                 ; advance of the last letter
.l: ld a, [hli]
    or a
    jr z, .e
    push hl
    and $7f
    ld l, a
    ld h, 0
    ld de, FontAdv
    add hl, de
    ld a, [hl]
    pop hl
    ld e, a
    add c
    ld c, a
    inc b
    jr .l
.e: ld a, b
    cp 7
    ld a, c
    jr nz, .r
    sub e
.r: ld l, a
    ret

; wEpoch += 1. Keeps all registers. The caches compare one byte (wRC_epoch, wPL_epoch, wNC entry epochs), so
; after 256 bumps an old epoch matched again and a cache restored codes of slots reused since (tavern 'Inspect
; whom?' list after the sheet's Spells/Items/Pool: exactly 512 bumps). On the wrap to 0 every cache is dropped.
EpochBump:
    push af
    push hl
    ld hl, wEpoch
    inc [hl]
    jr nz, .r
    xor a
    ld [wRC_valid], a
    ld [wPL_valid], a
    push bc
    push de
    call NCClear
    pop de
    pop bc
.r: pop hl
    pop af
    ret

; Address-keyed English for fixed-length copies; filled in by tools/build.py after assembly.
NOTICE_LINES equ 8
NOTICE_COL  equ 2
NoticeRows:                 ; row of each line ($FF = end), filled by tools/insert.py
    ds NOTICE_LINES, $ff
NoticeText:                 ; NOTICE_LINES x 28 bytes, $00-terminated lines
    ds NOTICE_LINES * 28, $00
SpellNames:                 ; 125 x [bank][lo][hi], filled by tools/insert.py (bank 0 = use the record)
    ds 125*3, $00
    assert @ <= $6c00, "VWF bank: code and data run into GCMaskTab/MaybeSlot/BitMask/ShiftTab"
    org VWF_BANK, $6c00
GCMaskTab:                  ; 256 bytes: 1 << (code & 7)   (GCRowMark)
    incbin "../build/gcmask.bin"
GCByteTab:                  ; 256 bytes: low(GCB) + code >> 3 (must follow GCMaskTab)
    incbin "../build/gcbyte.bin"
    assert low(GCB) == $80, "gcbyte.bin assumes GCB at $xx80"
    assert high(GCMaskTab) + 1 == high(GCByteTab), "GCByteTab must follow GCMaskTab"
    org VWF_BANK, $6e00
MaybeSlot:                  ; 256 bytes (page-aligned), built by tools/build.py: nonzero = this cell code can
    incbin "../build/maybeslot.bin"     ; be a slot (code, or code|$80 for a VRAM1 code < $70)
    org VWF_BANK, $6ff8
BitMask:                    ; 1 << n (page-safe: $6FF8-$6FFF)
    db $01, $02, $04, $08, $10, $20, $40, $80
    org VWF_BANK, $7000
ShiftTab:                   ; 16 pages, built by tools/build.py: page 2p = b >> p, 2p+1 = (b << (8-p)) & $FF
    incbin "../build/shift.bin"

