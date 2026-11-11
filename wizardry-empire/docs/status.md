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
1. Character card title (`2B:5F6B`, 140 records of 12 bytes, tracer proposal E) and label/value offsets
   (proposal F); bank 44 maze panel (same tables via `0C97`). Notes: `work/re/char-card.md` (not committed).
2. Monster-group panel in battle (`0:199B` bitmap tiles, `docs/re/battle-text.md` hook C): fixed-width, name wraps.
3. Spells: spell names, headers (まほうつかいの じゅもん), detail box, "Priest casts ." (name missing).
4. Playtester pt1 leftovers: maze Search message disturbs the party panel; trap message names; temple
   ("No one is here." garbled, Leave); Training Grounds "ordate character"; Notice Board scroll; shop category
   "Armor"/"Glov." first-open glitch; tavern preview leftovers ("Thief :r"); target lists miss the max-HP column.
5. Spell/item descriptions (bank 46), museum, prologue, name entry (Latin page), title screen.
6. Style: double space after names in battle/status messages ("Fighter  is asleep.").

## Known issues
- Untranslated text shows as blank/garbage (kana tiles are no longer loaded; their slots belong to the VWF).
- Unhooked printers fall back to the original 8 px font (ASCII letters/digits/punctuation are kept).
- Monster names are limited to 12 characters (record field); some are abbreviated (e.g. "Gr. Demon").
- When more than 161 distinct text tiles are needed on one screen, the allocator reuses tiles (visible
  as wrong letters). Battle with a full 6-line log was the tightest case; fixed by the GC rules in `re/vwf.md`.
- After a kill, the last battle line flickers for a few frames while the chest picture loads.
- `tools/emu.py` reports false hangs on slow VWF screens (frame counter stalls up to ~110 frames).
