# Test saves

Save files for testing the English build, made by our own tools (no game data from the cartridge beyond the
save format). Committed by the owner's decision (2026-11-12); everything else in `AGENTS.md` "Never commit game
data" still applies.

## test-party-all-spells.sav

A roster of six powerful characters for testing spells, menus and battles:

| # | Name | Class | Spells known |
|---|---|---|---|
| 1 | ryz | Valiant | all Mage + Priest, all Valiant Prayers |
| 2 | condi | Avenger | all Mage + Priest, all Avenger Arts |
| 3 | ebo | Musashi | all Mage + Priest, all Musashi Arts |
| 4 | cubi | Kunoichi (female) | all Mage + Priest, all Kunoichi Arts |
| 5 | deddo | Summoner | all Mage + Priest, all summons (pacts) |
| 6 | mnz | Bishop | all Mage + Priest |

Everyone: level 60, all stats 20, HP 999, AC -10, gold 999,999, EXP 9,999,999, 9 casts left at every spell level
of every school (an inn stay recomputes the casts from the class rules; the special classes keep 9 in their own
school, other schools drop to one cast per known spell). Equipment and age are the default characters'.

**Use:** copy it next to the ROM with the ROM's base name (`wizardry_empire_en.sav` for
`wizardry_empire_en.gbc`; most emulators look for that), power on, and form the party at Rose's Tavern (the party is
not formed in the save). Mode Settings has already been passed (defaults: Inn and Save on Mania).

**Rebuild** (after a change to the save format or the default characters):

```sh
python3 tools/party.py --out work/states/party      # standard party states for the current build
python3 tools/testsave.py --out saves/test-party-all-spells.sav
```

`tools/testsave.py` rewrites the six roster records in both save halves (working `$A001`, backup `$B001`; layout in
`docs/tech/characters.md` section 4) and cold-boots the build to check that the game keeps them. Tested with the
English build; the Japanese ROM uses the same save layout, but the names are in the English font's codes.
