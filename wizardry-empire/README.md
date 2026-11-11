# Wizardry Empire (GBC) English translation

Unofficial English fan translation of **Wizardry Empire** (Game Boy Color, Starfish, 1999): source text and tools that
build the patch. Work in progress - see `docs/status.md`.

This repository holds no game data. You need your own dump of the Japanese ROM
(1048576 bytes, SHA-1 `041c125115c83c6fef1b888761ba0b2b1f9bd291`, see `rom.sha1`).

## What's here

| Path | What it is |
|---|---|
| `script/` | Text blocks: original Japanese and English. |
| `tbl/` | Character tables (`jp.tbl` = original font, `en.tbl` = patched font). |
| `asm/` | Assembly patches (VWF, hooks), built by `tools/asm.py`. |
| `fonts/` | VWF font source. |
| `tools/` | Python build chain (no external deps besides Pillow for font/QA images). |
| `tests/` | pytest suite (ROM-dependent tests skip when the ROM is absent). |
| `docs/re/` | Reverse-engineering notes. |
| `docs/status.md` | Current snapshot: done, next, known issues. |
| `docs/progress-log.md` | History: what changed per session and per test ROM. |

## Build

```sh
cp /path/to/your/dump.gbc rom/wizardry_empire_j.gbc
python3 tools/build.py          # -> build/wizardry_empire_en.gbc + build/wizardry_empire_en.ips
python3 -m pytest -q tests
```

Emulator for testing (headless SameBoy for agents): `sh tools/setup_emu.sh` builds
[gbemu-cli](https://github.com/gopherbone/gbemu-cli) into `tools/gbemu-cli`.

## Licence

Tools and English translation: MIT. The Japanese text in `script/` is the original publisher's and is included only so
the translation can be checked against it. Do not share patched ROMs.
