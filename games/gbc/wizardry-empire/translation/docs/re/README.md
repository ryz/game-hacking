# Reverse-engineering notes (translation patch)

**RE = reverse engineering:** finding out how the game works by reading its machine code and data in the ROM and
watching it run in an emulator, because there is no source code. This folder holds what the translation patch
needed to know: where each text lives, how the game prints it, and how the patch (small font, hooks, inserted
text) plugs in. How the *game systems* work (combat, items, characters) is in `../tech/` (implementation) and
`../design/` (rules for designers). Conventions: `../README.md`.

| File | Covers |
|---|---|
| [text.md](text.md) | Text engines (fixed boxes, typewriter messages, control codes), screen buffers, data records with names. Start here. |
| [vwf.md](vwf.md) | Design of the small variable-width font (VWF): tile pool, allocation, garbage collection, layouts, caches. Read before touching `asm/`. |
| [numbers.md](numbers.md) | Number printing (0:0FE9) and the 8 px labels/separators around numbers. |
| [glyphs8.md](glyphs8.md) | Census of screen cells still drawn with the original 8 px font, and their status. |
| [battle-text.md](battle-text.md) | Where battle messages live and how they are printed. |
| [verbs.md](verbs.md) | Attack verbs and the battle templates that print them. |
| [museum.md](museum.md) | The museum screens (item/monster pages): text locations and printing. |
| [msgcov.md](msgcov.md) | Coverage census of every typewriter message the game can show. |
| [missing-text.md](missing-text.md) | Texts that were thought missing (title, options, item effects) and where they are. |
| [overflow.md](overflow.md) | Fixed-size RAM buffers that English text could overflow, and the limits. |
| [reach.md](reach.md) | Recipes to reach chests, maze events and other hard-to-reach screens in the emulator. |
| [rev1.md](rev1.md) | What changed between v1.0 and Rev 1 that matters for the translation. |
| [tasks.md](tasks.md) | The game's cooperative task scheduler and its stacks. |
| [debug-mode.md](debug-mode.md) | The hidden developer debug mode (logo button code), not translated. |
