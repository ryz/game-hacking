# Status

## Done
- Toolchain: disassembler, assembler (round-trip tested), build (2 MB MBC5, checksums, IPS), census tools,
  emulator setup (gbemu-cli). Width checks fail the build when English overflows a box.
- VWF engine (mixed case, `fonts/vwf.txt`), 157-tile slot pool, hooks for:
  rect boxes, typewriter messages (`$F2` redirect), `$00`-terminated name copies (17 sites),
  inline code text (`rst $38`, 19 strings), fixed-length table copies (9 sites, address-keyed map),
  bank-49 string tables (177 entries, repointed), chest names (bank-37 immediates).
- Translated: 251 menu/info boxes, 429 messages (bank 45 events/NPCs, bank 49 dungeon/system),
  224 item names, 166 monster names, 6 default characters, character-sheet labels, tavern menu.
- Verified in the emulator from boot: town (all 8 building infos), tavern (add/inspect), shop, Outskirts menu,
  camp, character sheet, dungeon menu and stairs prompt.

## Done 2026-11-12 (eleventh session: Rev 1 port, museum monster room, editor pass)
- Base ROM is now the Japanese **Rev 1** (SHA-1 f5f4e8be..., CRC32 FA82620F). `tools/revmap.py` maps v1.0
  addresses; script, asm, insert constants and docs converted (docs/re/rev1.md: what Rev 1 changed - a wall bump
  shows "Ouch!", two new magic-circle messages, 31 status words). v1.0 saves may be wiped (Rev 1 writes an
  SRAM signature); old savestates do not load.
- Reference English patch applies to Rev 1 (rom/wizardry_empire_ref.gbc, not committed); 164 reference shots in
  work/shots/ref_tour/ (not published).
- Museum monster page: "Special"/"Resistance" headers, AC:/EXP:/HP: labels and element labels (Ear Wat Fir Air
  / Min Aur Hol Non) in the VWF, resistance 100 as VWF digits; GC pass order for the page/list double buffer.
- Editor pass applied (names, battle past tense, maze wording); breath verbs no longer read "breathed fire at!"
  (docs/re/verbs.md).
- Tools: emulator turbo by default (~7x faster, same frames); shoot.py `poke` token; museum and maze shot lines.
- Last untranslated screens (docs/re/missing-text.md): the ending (7 pages) and credits (10 rects, now VWF),
  the "End the quest" power-off screen, two museum ring descriptions, Training "Become a <class>?" prompt.

## Done 2026-11-12 (tenth session: museum items, owner's list)
- GC counted the off-screen columns 20-31 (uninitialised RAM): ~80 slots wasted; now only visible columns.
- Museum item side: category words written out, 'Not found', item list and page in the VWF, labels and all
  use/special values translated, 'Equip:' as allowed-class abbreviations, '2-7' ranges.
- Unidentified names: '?AX' fixed (ASCII records at 41:5706); every item 'looked like' an Axe because the
  item name insert overwrote the class byte (item names now max 16 chars).
- Character card: 'Lvl' in the VWF instead of the 8 px 'L'.
- Reference translation: tools/bps.py applies an existing fan patch (kept out of git, rom/reference_en.bps);
  it targets Rev 1 (CRC32 FA82620F), which is now our base.

## Done 2026-11-11 (ninth session: render speed)
- Letter drawing ~2.5x faster (shift tables), smaller bookkeeping costs; cursor move without a party: reaction
  at frame 6-12 (was 7-13; JP 2). The rest is per-tile bookkeeping (docs/re/vwf.md "Render speed").
- Fixed: shop header 'AC' garbled on some frames (in ROM 2edfeec): the card's age stays in 8 px (NumExcl).

## Done 2026-11-11 (eighth session: speed, numbers)
- Town speed: with a party 360 loops/120 frames and reaction at frame 2, like the Japanese (was 174 and a
  half-speed cursor); without a party (info box) reaction at frame 7-13 (was 14-18, JP 2). Caches: names,
  numbers, party list, rect sums; Dedupe hash index (`docs/re/vwf.md` "Speed").
- Numbers in the small font everywhere 0:0FE9 prints them (84 sites: party lists, character sheet, shop
  prices, inn, gold, EXP ...); tabular digits; typewriter number padding 5 px.

## Done 2026-11-11 (seventh session)
- Shop Buy/Sell lists, "Sold out" rows and the character item lists (Camp, tavern sheet) in the small VWF font
  (41:4A52, 41:49EB, 41:5674 through Stub_PrintZ).
- Coverage tests (`tests/test_coverage.py`); signature `VY` (old savestates re-init); redraw cache blocked while
  a font load is pending; `tools/explore.py` (moved from work/).

## Done 2026-11-11 (sixth session, owner's report: town slowdown, maze walls, Camp)
- Town speed: idle town runs its main loop as often as the Japanese (360 per 120 frames, was 72); the info box
  redraw is served from a cache (`docs/re/vwf.md`). Cursor moves: ~310 (one render).
- Text no longer drawn into maze wall tiles (dry GC pass keeps game graphics; reservations pruned instead of
  piling up until a font load).
- Party list status words (Camp and the other party lists): English, 32 px forms Paral./Silent/Poison.

## Done 2026-11-11 (fifth session)
- Notice Board scroll in English (`script/notice.json`, `VWF_Notice`): the picture's Japanese text area is
  blanked to paper and the VWF prints over it before the fade-in (palette 5: the scroll's palette 6 has an
  ink colour that matches the paper). Ink is the scroll's dark brown, lighter than the Japanese black.

## Done 2026-11-11 (fourth session, playtest pt2 fixes)
- Disarm trap list, Training class lists (create, bonus panel, change class), battle Fight/Go back box and
  party action column ("10/Normal"), party status words, friendly-encounter prompt, battle Equip "None"
  and slot titles, inn level-up lines (no duplicates while scrolling, "20 more max HP."), camp spell
  screens, kanji block on spell screens trimmed to the cursor arrow, maze view wall tiles, temple
  "No one in need.", name-entry hint, town input lag, named standard playtest party (`tools/party.py`).
- VWF: identical tiles are shared (Dedupe); in-place reuse takes a fresh slot when the content changes and
  the tile may be shown elsewhere; GC counts everything first and only a dry second pass ignores a hidden
  window, BG rows under the window and graphics reservations; typewriter blanks cells it passes without ink.

## Done 2026-11-11 (third session)
- Character titles (140), battle monster panel (proportional, "(n) m"), temple prompts, name entry in Latin
  letters, chest picture no longer overwritten by text, shop header garbage, spells (names, list, headers,
  detail box, element, 110 descriptions, battle "casts <spell>"), no double spaces in battle text.
- Font rule: words in the small VWF font; 8 px only for numbers and grids (`glossary.md`).

## Fixed 2026-11-11 (second session)
- Battle: command menus and sub-menus, round messages (attack verbs, damage, kills), "called for help", chest
  menu and chest names are English and stay intact while the log scrolls.
- Gold/EXP corruption: RAM data copies were stubbed as text (buying added gold, the inn charged nothing,
  "Next level in" showed garbage). Fixed.
- Shop hang (card drawn from a task): VWF bodies now run on a private stack.
- Character card: gender, status, location, shop alignment, Gold label; mode-select screen.

## Fixed 2026-11-11
- Battle hang on the first attack: VWF variables sat in the game's task stacks (`docs/re/tasks.md`); moved to
  WRAM bank 7. Verified: a full battle (attacks, kill, gold, chest prompt) plays through.
- Redirected messages left the text bank on the English bank; English now jumps back to the original terminator.

## Next (in rough priority)
1. Museum monster page: opening takes 37 frames (JP 9; each VWF GC ~5-6 frames), closing shows a few frames of
   garbage in the page; AC/HP minus signs still 8 px. A faster GC would help every screen.
2. Name-entry field still in the 8 px font (owner's rule: words in the VWF).
3. Friendly-encounter prompt (49:555B) translated but not yet seen on screen.
4. Ending/credits checked only with the forced route ($D000=8 from the town); a real final-boss ending (maze
   layout) not seen. The game has no prologue; item effect texts are the museum rects (all translated).
5. VWF: short transients while screens are typed (1-4 frames). Town input delay after arrival not re-measured
   since the redraw cache.
6. Owner's report "gets slower the longer I play" not reproduced in the emulator (random walks, door messages,
   battle); the two causes found are fixed. Needs a long playtest on the new ROM.
7. Flicker (owner's request): the new screen reuses tiles the old one still shows until the game copies its
   buffer (in-place redraws and freed slots), e.g. inn list -> character sheet (~35 frames of wrong letters),
   message -> chest menu (3 frames). A quarantine by frame count did not help (in-place case) and slowed screens
   (repeated GC); next try: tie reuse to the game's buffer copy (hook 0:1696) - see docs/re/vwf.md.
8. Still 8 px (docs/re/numbers.md): '/', '-', '~', ':' separators and the labels L/HP/AC/HP-MAX/Lo/Hi/ON/OFF,
   spell-slot grid separators, monster panel and automap digits (symbol sheet), Camp reorder digits.
   Stylistic candidates for the owner: big L/HP/AC on the character sheet, the name-entry chart.
9. Seen once, not reproduced: wrong digits in the chest "Who will inspect?" list after inputs during the trap
   message.
10. Tool backlog (from agent feedback): `tools/emu.py` hang check should report a hang only when the PC stays
   in a tight range, plus a soft-lock check (screen and task table unchanged); shoot.py state-based shots
   (`@STATE` lines, `!` no-settle); explore.py answers No at the entrance stairs; contact-sheet tool; census
   segment mode (`$FC`) and attributes; lint: ignore `{..}` inserts before punctuation, label lists.json
   entries, Ifrit-style spell/monster pairs; a width helper for suggested rect lines; gbdis xref mode;
   revmap inv_addr()/gaps().
11. Editor items not applied: Maze Robe vs Magic Gate (まどう ruling), ADISH monster-speak in caps, plural
   counts with N = 1 ("1 levels"), remaining Polish list (skills/editor/feedback.md 2026-11-12).

## Known issues
- Untranslated text shows as blank/garbage (kana tiles are no longer loaded; their slots belong to the VWF).
- Unhooked printers fall back to the original 8 px font (ASCII letters/digits/punctuation are kept).
- Monster names are limited to 12 characters (record field); some are abbreviated (e.g. "Gr. Demon").
- When more than 157 distinct text tiles are needed on one screen, the allocator reuses tiles (visible as
  wrong letters); no current case known (battle with a full 6-line log was the tightest, `docs/re/vwf.md`).
- After a kill, the last battle line flickers for a few frames while the chest picture loads.
- When the battle party list slides back in, it shows menu letters for a few frames (window hidden at the
  last GC, its slots reused).
- `tools/emu.py` reports false hangs on slow VWF screens (frame counter stalls up to ~110 frames).
