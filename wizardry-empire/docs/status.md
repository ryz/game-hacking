# Status

## Done
- Toolchain: disassembler, assembler (round-trip tested), build (2 MB MBC5, checksums, IPS), census tools,
  emulator setup (gbemu-cli). Width checks fail the build when English overflows a box.
- VWF engine (mixed case, `fonts/vwf.txt`), 161-tile slot pool, hooks for:
  rect boxes, typewriter messages (`$F2` redirect), `$00`-terminated name copies (17 sites),
  inline code text (`rst $38`, 19 strings), fixed-length table copies (8 sites, address-keyed map),
  bank-49 string tables (177 entries, repointed), chest names (bank-37 immediates).
- Translated: 207 menu/info boxes, 185 messages (bank 45 events/NPCs, bank 49 dungeon/system),
  224 item names, 166 monster names, 6 default characters, character-sheet labels, tavern menu.
- Verified in the emulator from boot: town (all 8 building infos), tavern (add/inspect), shop, Outskirts menu,
  camp, character sheet, dungeon menu and stairs prompt.

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
1. Notice Board scroll and museum item pages: they use a separate glyph set (not `tbl/jp.tbl`); needs a
   tracer run for the glyph mapping and the printer.
2. Shop item lists and the name-entry field still in the 8 px font (owner's rule: words in the VWF).
3. Friendly-encounter prompt (49:555B) translated but not yet seen on screen.
4. Item effect descriptions (bank 46), prologue, title screen.
5. VWF: Dedupe search makes the town accept input ~60 frames after arrival (JP 20); a faster lookup
   (hash buckets) would bring it back. Short transients while screens are typed (1-4 frames).

## Known issues
- Untranslated text shows as blank/garbage (kana tiles are no longer loaded; their slots belong to the VWF).
- Unhooked printers fall back to the original 8 px font (ASCII letters/digits/punctuation are kept).
- Monster names are limited to 12 characters (record field); some are abbreviated (e.g. "Gr. Demon").
- When more than 161 distinct text tiles are needed on one screen, the allocator reuses tiles (visible
  as wrong letters). Battle with a full 6-line log was the tightest case; fixed by the GC rules in `re/vwf.md`.
- After a kill, the last battle line flickers for a few frames while the chest picture loads.
- When the battle party list slides back in, it shows menu letters for a few frames (window hidden at the
  last GC, its slots reused).
- `tools/emu.py` reports false hangs on slow VWF screens (frame counter stalls up to ~110 frames).
