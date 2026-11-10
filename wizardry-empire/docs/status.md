# Status

## Done
- Toolchain: disassembler, assembler (round-trip tested), build (2 MB MBC5, checksums, IPS), census tools,
  emulator setup (gbemu-cli). Width checks fail the build when English overflows a box.
- VWF engine (mixed case, `fonts/vwf.txt`), 161-tile slot pool, hooks for:
  rect boxes, typewriter messages (`$F2` redirect), `$00`-terminated name copies (17 sites),
  inline code text (`rst $38`, 19 strings), fixed-length table copies (34 sites, address-keyed map).
- Translated: 207 menu/info boxes, 185 messages (bank 45 events/NPCs, bank 49 dungeon/system),
  224 item names, 166 monster names, 6 default characters, character-sheet labels, tavern menu.
- Verified in the emulator from boot: town (all 8 building infos), tavern (add/inspect), shop, Outskirts menu,
  camp, character sheet, dungeon menu and stairs prompt.

## Next (in rough priority)
1. Character sheet values still in kana: gender, status (`せいじょう`), location, title (`みならい`).
   Find their copy routines (watch reads of the source tables) and route them through the VWF.
2. Battle text: the battle code (banks 36/50) sets message pointers without the text bank; needs a battle
   at runtime to see `$C1C1` (random walks so far did not reach one).
3. Bank 49 composite strings: `$00`-separated name lists (gender/race/class/status/commands, `49:4000-418F`),
   `$FC`-chained trap messages (`49:541A`), trap list (`49:52F8`). Need the indexing routine before relocating.
4. Spell names and spell/item effect descriptions (bank 46), museum screens (they load a different glyph set:
   their rects decode as garbage with `tbl/jp.tbl`), prologue (`43:6416`, `43:6578`, same issue).
5. Name entry: switch the chart to the Latin page (`38:70C3-7122` already exist) and translate the page rects.
6. Title / mode-select screen (pre-rendered tilemaps with attributes, `2B:779F`), logo graphics if any.
7. Remaining inline strings and rects found later; debug-mode text (bank 44/45) is low priority.
8. QA: scripted routes from boot for every screen; sanitizer run (`sanitize.start`) on the patched ROM.

## Known issues
- Untranslated text shows as blank/garbage (kana tiles are no longer loaded; their slots belong to the VWF).
- Unhooked printers fall back to the original 8 px font (ASCII letters/digits/punctuation are kept).
- Monster names are limited to 12 characters (record field); some are abbreviated (e.g. "Gr. Demon").
- When more than 161 distinct text tiles are needed on one screen, the allocator reuses tiles (visible
  as wrong letters). Not seen since the pool was enlarged.
