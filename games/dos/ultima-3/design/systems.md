# Ultima III: Exodus (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima-3`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
Walk the party over Sosaria, enter townes and castles to talk, trade and heal, and fight the monsters that walk
up to the party; experience turns into hit points at Lord British's throne **(verified: `start`, `towne`,
`fight`, `lordbritish`)**. Between loops the party goes deeper: dungeons for marks and gold, a frigate for the
sea, the whirlpool to Ambrosia for statistics and cards, the moongates for the Time dungeon, until the four
cards end the game in the Castle of Fire **(verified with pokes: `rod`, `ambrosia`, `card`, `timelord`,
`ending`)**. Scout status 2026-11-19: no shots yet; the Shots column names the planned ids of `../shots.txt`.

## 2. Systems
| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | 26 one-key commands on the map | A attack, B board, C cast, D descend, E enter, F fire, G get chest, H hand equipment, I ignite torch, J join gold, K klimb, L look, M modify order, N negate time, O other command, P peer at gem, Q quit & save, R ready, S steal, T transact, U unlock, V volume, W wear, X x-it, Y yell, Z ztats **(verified: every prompt)** | letter, then player number and/or direction | - | ../playbook.md Controls | planned: one per command | described (no shots yet) |
| Player verbs | Other command | a typed word: INSERT, DIG, SEARCH, BRIBE, PRAY; anything else "No effect!" **(verified)** | `o`, player, word + Enter | - | section 3 | `card_found`, `dig_exotics`, `yew_pray`, `bribe_guard`, `insert_love` | described |
| Player verbs | Real-time pass | no key for 5 seconds of the PC's clock and the game passes a turn ("Pass") **(code, verified)** | none | 5 s | - | `hud_status` | described |
| Characters and progression | Creation | name, sex (male, female, other), race (5), type (11), 50 points over Strength, Dexterity, Intelligence, Wisdom **(verified)** | letters + Enter, two-digit numbers | 50 points; new characters 150 H.P., 150 food, 150 gold, dagger, cloth **(verified)** | ../playbook.md Boot | `menu_create_*` | described |
| Characters and progression | Race limits | the highest each statistic can reach: Human 75/75/75/75, Elf 75/99/75/50, Dwarf 99/75/50/75, Bobbit 75/50/75/99, Fuzzy 25/99/99/75 (Str/Dex/Int/Wis) **(ROM text)** | - | table | - | - | described (a table, no screen) |
| Characters and progression | Roster and party | up to 20 characters in the register, a party of 1-4 formed by entry numbers, dispersed, terminated **(verified: create, register, form)** | Organize menu | 20, 4 | interface.md | `menu_register`, `menu_form` | described |
| Characters and progression | Levels and hit points | the level shown is experience / 100 + 1; maximum hit points rise only when Lord British grants them: +100 when the experience hundreds are at least the maximum's hundreds **(code, verified: "Experience more!", "Thou art greater")** | Transact with Lord British | +100 per visit; past 500 needs the Mark of Kings; "No more!" at 2500 **(code)** | section 3 | `lb_experience`, `lb_greater`, `lb_mark` | described |
| Characters and progression | Shrines of Ambrosia | an offering of N hundred gold raises Strength, Dexterity, Intelligence or Wisdom by N, up to the race limit **(code; prompt verified)** | Enter on the shrine, player, number + Enter | 100 gold per point | section 3 | `shrine_enter`, `shrine_shazam` | described |
| Resources and economy | Gold, food, gems, keys, powders, torches | each character carries its own; food drops as the party moves, gold from chests after fights; Join gold pools it **(verified: panel, Ztats)** | J, H | food 1 g.p. per ration; Guild: keys 50, torches 6, powders 90, gems 75 **(ROM text)** | ../playbook.md Shops | `ztats_1`, `shop_guild` | described |
| Resources and economy | Shops | eight kinds, chosen by the counter's row: pub, grocer, healer, weapons, armour, Guild, oracle, horses **(code, verified for five)** | Transact over a counter | weapons 5-6550, armour 75-8250, healing 100-900 **(ROM text)** | ../playbook.md | `shop_*` | described |
| Conflict | Combat screen | a fight moves to an 11x11 field; each player acts in turn (move, attack in a direction, cast, ready), then the monsters; "Killed! Exp.+N", "Victory!" **(verified)** | arrows, A + direction, C, R, space | orcs give 3 experience each **(verified)** | open: formulas | `battle_start`, `battle_attack`, `battle_victory` | described |
| Conflict | Monsters on the map | monsters are visible on Sosaria and in some townes and castles and walk toward the party; touching starts the fight; a chest is left where they stood **(verified)** | move or attack | 13 kinds spawn on Sosaria (land and sea) **(code)** | content.md | `battle_chest` | described |
| Conflict | Death | a character is Good, Poisoned, Dead or Ashes (G, P, D, A on the panel; ROM text); all four out: "All Players Out!" and the game stops **(verified with a poke)** | - | - | - | `gameover` | described |
| Opponents | Kinds | orcs, thieves, skeletons, fighters, giants, daemons, pinchers, wizards, dragons, balrons on land; sea serpents, man-o-wars, pirates at sea; guards, Floors, Exodus in the castle **(code, ROM text)** | - | - | content.md | `battle_*` | described |
| Items and equipment | Weapons and armour | 15 weapons from dagger to +4 sword and Exotic; 7 armours from cloth to +2 plate and Exotic; ready and wear per character **(ROM text, verified in Ztats)** | R, W, buy/sell | prices in content.md | content.md | `shop_weapons`, `shop_armour`, `ztats_2` | described |
| Items and equipment | Exotics | Exotic weapon dug at the islet (21,03), Exotic armour at (13,2C) **(code, verified "Exotics!")** | O + DIG | one per dig | section 3 | `dig_exotics` | described |
| Items and equipment | Cards and marks | four cards (Love, Sol, Moons, Death) found by SEARCH on Ambrosia's shrines; four marks (Force, Fire, Snake, Kings) branded by rods in dungeons **(verified)** | O + SEARCH; touching a rod | rod damage about 50 **(verified)** | section 3 | `card_found`, `dungeon_rod`, `dungeon_mark`, `ztats_cards` | described |
| Abilities and magic | Spells | clerics, paladins and others cast cleric spells, wizards and others wizard spells, by letter, paying magic points that refill each turn **(verified: prompts; ROM text: 16 cleric, 15 named wizard spells)** | C, player, letter | open | content.md | `battle_spell` | open (effects and costs not read) |
| World and navigation | Sosaria | 64x64, wraps; 10 townes, 2 castles, 7 dungeons **(code)** | arrows | coordinates in the playbook | content.md | `start_party`, `towne_lcb` | described |
| World and navigation | Vehicles and wind | horses (bought) and frigates (taken from pirates); a frigate cannot sail into the wind, which changes every 25 turns; frigates fire cannons **(code, verified)** | B, X, F | - | - | `horse_ride`, `frigate`, `frigate_fire`, `wind_change` | described |
| World and navigation | Moongates | the first moon (every 12 turns) chooses where the gate stands, the second (every 4) where it leads; eight squares **(code, verified)** | walk in | 8 phases | ../playbook.md | `moongate_open`, `moongate_through` | described |
| World and navigation | Whirlpool and Ambrosia | a frigate swallowed by the whirlpool washes the party up in Ambrosia without the ship **(verified)** | sail into it | - | - | `whirlpool`, `ambrosia_shore` | described |
| World and navigation | Dungeons | first person, 8 levels of 16x16, dark without a torch; ladders, doors, secret doors, chests, fountains, traps, winds, gremlins, misty writing **(verified: torch, fountain, rod; code: the rest)** | arrows, K, D, I | - | content.md | `dungeon_*` | described |
| World and navigation | Peer at gem | a gem shows the whole map in miniature **(verified)** | P, player | 75 gold per gem | - | `peer_gem` | described |
| Goals and gating | The quest | marks for every member (fields, lava, the snake), the word EVOCARE (Yew), the four cards (Ambrosia), the order Love, Sol, Moons, Death (the Time Lord), Castle Exodus **(verified with pokes)** | - | - | section 3 | `evocare`, `timelord`, `insert_love`, `ending_*` | described |
| Goals and gating | Dawn | the city of Dawn appears in the Dark Forest only when both moons are new **(code, verified)** | wait for the moons | - | - | `dawn_appears`, `dawn_towne` | described |
| Chance | Encounters, fountains, wind | monsters spawn at random on free squares; the wind and the whirlpool move at random **(code)** | - | - | - | - | described (no screen) |
| Failure and recovery | Healing and resurrection | fountains, clerical healing in townes (curing 100, healing 200, resurrection 500, recalling 900 gold) **(ROM text)** | Transact | - | - | `shop_healer` | described |
| Saving and sessions | Quit & Save | only on Sosaria; play continues; entering a place also saves **(verified)** | Q | moves counter shown | - | `save_quit` | described |
| Pacing and difficulty | Gating by knowledge | almost nothing is locked by level; the gates are marks, cards, a word, a moon phase and a whirlpool **(inferred from the code)** | - | - | - | - | described |

## 3. How the systems feed each other
- Fights give experience and gold; Lord British turns experience into hit points; gold buys arms, horses,
  healing and (in Ambrosia) statistics; statistics raise spell power and hits **(verified for the first three)**.
- Dungeons give gold, chests and the marks; the marks open the Castle of Fire and Lord British's levels past
  five **(code, verified)**.
- The sea (frigate, whirlpool) opens Ambrosia: statistics and the cards; the moons open Dawn (shops) and the
  Time dungeon (the card order) **(verified)**.
- Talk ties it together: every hint the player needs is a townsperson's line or the oracle's rhyme **(ROM text)**.

## Open questions
- Combat formulas, monster hit points, spell effects and costs, class restrictions for weapons and armour.
- Starvation and poison rules (food 0 showed nothing in 300 frames).
- The Lark, Barbarian, Druid, Illusionist, Alchemist and Ranger rules.
