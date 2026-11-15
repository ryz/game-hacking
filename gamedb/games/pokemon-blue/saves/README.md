# Pokémon Blue Version - saves

Made by the agents while playing (owner's rule 2026-11-15: committed so the owner can jump in). `.sav` = the game's own battery save: copy it next to your ROM as `<rom name>.sav` in any emulator, then Continue. `.state` = SameBoy savestate of the exact moment (SameBoy only). In routes: `sav:NAME` prefix (power on with that save).

| Save | Files | What it contains | Route at export | SHA-1 (.sav) | Date |
|---|---|---|---|---|---|
| 01_start | `01_start.sav`, `01_start.state` | Player ryz in his room (Red's house 2F), new game, rival RED, no Pokemon, 3000 money | `@start,start,down*3,a,settle,a,w120,settle,a,w30,settle` | `21655e84661a` | 2026-11-15 |
| 02_late_game_test | `02_late_game_test.sav`, `02_late_game_test.state` | RAM-recipe test (LATE macro): Indigo Plateau lobby, 8 badges, 48215 money, 27:47 play time, Pokedex 71 owned/104 seen, party BLASTOISE 52, PIDGEOT 47, RAICHU 45, SNORLAX 46, VICTREEBEL 44, KADABRA 42 (HM moves Surf/Strength/Fly/Flash/Cut), 19 bag items; only basic event flags set (Pokedex, starter, parcel) | `@start,LATE,TO_DOOR,settle,poke:D3B1=00AE,poke:D3B5=00AE,poke:D365=09,poke:D719=09,EXIT,settle,up:16*3,settle,start,down*3,a,w60,settle,b,w30,poke:DA41=1B,poke:DA43=2E,a,w60,settle,b,w30,start,up,a,w30,settle,a,w60,settle,a,w60,settle,a,w200,settle,a,w240,settle,a,w60,settle,w200,a,w60,a,w60,settle,a,w30,start,down*2,a,w30,settle,left,b,w30,up*3,a,w30,settle,b,w20,down*2,a,w30,settle,a,w60,settle,w120,settle` | `44148b414c76` | 2026-11-15 |
