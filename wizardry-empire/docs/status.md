# Status

## Done
- Toolchain: disassembler, assembler (round-trip tested), build (2 MB, checksums, IPS), census tools.
- VWF engine (mixed case) for rect boxes and typewriter messages, tested in town and dungeon.
- Sample translations: town-edge info box, dungeon "stairs up" prompt.

## Next
1. Inline text in code (`ld a,$xx / ld [de],a / inc de` runs, e.g. character sheet in bank 38): `rst $38` print hook.
2. Name tables (items, monsters, spells, classes; `$00`-separated, bank 49 and others) and their printer(s).
3. Extract all rects (`tools/census_rects.py`) and messages (`tools/census_msgs.py`) to `script/`, translate.
4. Title/graphics with text (mode screen uses its own tilemaps with attributes).
5. QA routes from boot (savestates from the original ROM are only used for quick checks).

## Known issues
- Text not yet translated renders as garbage (kana tiles are no longer loaded).
- Census tools still report some non-text candidates; entries are curated by hand in `script/`.
