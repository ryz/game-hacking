# Wizardry: Proving Grounds of the Mad Overlord (NES, USA) - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the game's own battery save: copy it next to your ROM as `<rom name>.sav` in any emulator, then Continue. `.state` = Mesen libretro core savestate of the exact moment (that emulator only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_party | `01_party.sav` | Roster with the playtest party RYZ (Human Fighter G), CONDI (Dwarf Fighter G), EBO (Gnome Cleric G), CUBI (Hobbit Thief N), DEDDO (Elf Mage G), MNZ (Elf Wizard=Bishop G), all level 1, no equipment, plus the six pre-made characters; saved by Edge of Town > Leave Game | `@castle,b,w30,down*3,a,w60,settle,w120,settle` | `4c578257badf` | 2026-11-18 |
| 02_veterans | `02_veterans.sav` | Roster with the playtest party as veterans (RYZ L13 Fig, CONDI L12 Fig, EBO L13 Cle, CUBI L12 Thi, DEDDO L13 Mag, MNZ L10 Wiz), all spells to their level, 918-6120 gold; party not formed (Tavern > Add) | `@veterans,b,w30,down*3,a,w60,w120,settle` | `1c2e0a153f44` | 2026-11-18 |
| 03_werdna_defeated | `03_werdna_defeated.sav` | After the ending: Werdna defeated, the party RYZ (L11, Chevron of Rank "RYZ>" seen), CONDI (cured at the Temple), EBO, CUBI, DEDDO, MNZ, about 50,000 gold more each; party not formed (Tavern > Add) | `@ending,a,w120,w3000,a,w120,settle,a,w60,down*2,a,w60,a,w60,settle,b,w60,b,w60,b,w30,b,w30,down*3,a,w60,w120,settle,a,w60,a,w60,w180,settle,a,w60,settle,b,w30,down*3,a,w60,w120,settle` | `40f6a90c8661` | 2026-11-18 |
