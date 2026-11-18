# Wizardry Empire - English translation

Unofficial English fan translation of the Japanese Rev 1: source text and the tools that build the patch.
Status: [docs/status.md](docs/status.md). History: [docs/progress-log.md](docs/progress-log.md).

You need your own dump of the Japanese ROM, **Rev 1** (SHA-1 in `rom.sha1`), as `rom/wizardry_empire_j.gbc`.
(The project started on v1.0, SHA-1 `041c1251...`; `tools/revmap.py` needs that dump as
`rom/wizardry_empire_j_v10.gbc` only to map old addresses.)

All commands run from this folder (`games/gbc/wizardry-empire/translation/`).

| Path | What it is |
|---|---|
| `script/` | Text blocks: original Japanese and English, side by side. Edit these, never the ROM. |
| `glossary.md` | Binding names and terms. |
| `tbl/` | Character tables (`jp.tbl` = original font, `en.tbl` = patched font). |
| `asm/` | Assembly patches (variable-width font, hooks), built by `tools/asm.py`. |
| `fonts/` | Variable-width font source. |
| `tools/` | Python build chain, emulator driver, QA (tour, pixel check), reference screenshots, design-table and map generators. Only Pillow is needed besides Python. |
| `tests/` | pytest suite (ROM-dependent tests skip when the ROM is absent). |
| `docs/re/` | Reverse-engineering notes on text, display and the patch ([index](docs/re/README.md)). |
| `rom/`, `build/`, `work/` | Your dump, the built ROM and patch, scratch (all ignored by git). |

## Build

```sh
cp /path/to/your/dump.gbc rom/wizardry_empire_j.gbc
python3 tools/build.py          # -> build/wizardry_empire_en.gbc + build/wizardry_empire_en.ips
python3 -m pytest -q tests
```

Emulator for the automated checks: `sh tools/setup_emu.sh` builds the shared headless emulator (gbemu-cli) at
the repo root; then `python3 tools/check.py` runs build, tests, screen tour and pixel diff.

## Licence

Tools and English translation: MIT. The Japanese text in `script/` is the original publisher's and is included
only so the translation can be checked against it. Do not share patched ROMs.
