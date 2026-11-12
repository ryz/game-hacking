# Shot set `compare3`: original | this patch | other patch

Three-way visual comparison of every curated shot in `tools/routes/shots.txt` (35 shots): the Japanese original,
our English build and the other (reference) fan translation, played with the same inputs from power-on and
captured on the same frame.

- `<id>.compare3@3x.png`: JP | EN | REF left to right, 3x nearest neighbour, labelled "Original (JP)",
  "This patch", "Other patch"; same 12 px gap and background as the two-way `compare@3x` images.
- `<id>.jp.png`, `<id>.en.png`, `<id>.ref.png`: native 160x144 framebuffer (CGB 5->8 bit, no correction).
- `index.md` / `index.json`: catalogue (tokens, settled per ROM, ROM SHA-1s, commit).

This set is for visual comparison (layout, fonts, box use), not for judging wording.

## ROMs

| panel | ROM | SHA-1 |
|---|---|---|
| Original (JP) | `rom/wizardry_empire_j.gbc` (Japan Rev 1) | `f5f4e8bead0fe45075141133a530a0eb116ea78c` |
| This patch | `build/wizardry_empire_en.gbc` (commit `f19f75f`) | `43c4d7a73ceea927dc79d2e8b60bce0b470aabaf` |
| Other patch | `rom/wizardry_empire_ref.gbc` = `rom/reference_en.bps` on Rev 1 | `3ac9d0273b5708363c8ee00c356f50e405ca1cd4` |

The reference patch and the ROMs are never committed. The patched reference ROM is 1048619 bytes (the BPS
target size, not a power of two); `tools/bps.py` checks the source, target and patch CRCs.

## Regenerate

```
python3 tools/bps.py rom/reference_en.bps rom/wizardry_empire_j.gbc rom/wizardry_empire_ref.gbc   # if missing
python3 tools/build.py                                                                           # if needed
python3 tools/shoot.py compare3 --rom all [--only id,id] [--publish]
```

A full run takes about 3 minutes (turbo, boot/PARTY route cache).

## Same screen?

All 35 shots show the same screen in all three ROMs: no route diverges in the other patch. The JP and EN
images are pixel-identical to the same ids in `docs/shots/rev1_tour/` (31 shared ids; the 4 museum ids
`museum_item_info_dn`, `museum_item_info_rt`, `museum_monster_list`, `museum_monster_page` are newer than that set).

Not settled (expected, animated screens): the 8 `town_*` shots and `party_town` in all three ROMs (town cursor
blink). Text is complete in every panel; the blink phase of the building cursor differs between the panels.

Same screen, but the content differs for a reason other than the translation itself:

| id | difference |
|---|---|
| `title` | the other patch adds a subtitle line under the logo ("THE EMPEROR OF NARAKA") |
| `mode_select` | the other patch puts the cursor on the value column; JP and EN put it on the setting name |
| `tavern_add`, `party_town`, `temple_menu`, `inn_rooms`, `outskirts_menu`, `camp`, `character_sheet`, `maze_dmenu`, `shop_menu`, `shop_buy` | preset roster: the other patch renames the six preset characters (Richard, Mark, Helly, Dave, AgentOr, EsperKn); JP and EN keep the class names as character names |
| `stairs_up_prompt` | the other patch draws the prompt box taller and higher up over the maze view |
| `museum_item_info`, `_dn`, `_rt` | the other patch has no frame around the item name |
| `museum_monster_page` | the other patch lays out the lower boxes differently (Ability / Cast / Petrify / LV, resistances as icons) |
