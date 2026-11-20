# SWORD OF VERMILION - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py md/sword-of-vermilion`.
Shots: set `main` (`../shots/main/index.md`) unless marked (start) for set `start` (`../shots/start/index.md`).

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The prince walks a first-person overworld of 16x16-square maps from town to town **(verified: RAM map window,
checkpoints `m_north1`, `m_north2`, `m_parma`)**. Random encounters turn into real-time side-view battles in which he
swings his sword with C, casts the readied spell with A and may walk off the screen edge to flee **(verified)**.
Each enemy killed pays experience and kims at once; levels are granted when the battle ends **(verified: RAM)**.
Money buys weapons, armour, spell books and nights at the inn; churches save the game and revive the fallen
prince for half his money **(verified)**. Dark caves need a Candle or Lantern and hide barred doors and chests
**(verified: cave south of Wyclif)**. What changes between loops: stronger enemies further from Wyclif (slimes,
then goblins), new towns, new spells for sale **(verified for the first two maps)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Field command window | C opens eight commands on every field screen: Talk, Magic, Item, Equip, Str, Seek, Open, Take | C, D-pad, B | 8 commands | [interface.md](interface.md) | `hud_field_menu`, `15_field_menu` (start) | shown |
| Player verbs | Talk | Speak to the person faced; "There's no one here to talk to." otherwise **(verified)** | Talk | - | - | `dialogue_blade_house`, `shop_magic_greeting` | shown |
| Player verbs | Open | Opens a faced chest or barred cave door; "There's nothing to open here!" otherwise **(verified)** | Open | - | - | `system_open_door`, `system_open_chest`, `system_open_money` | shown |
| Player verbs | Take | Picks up what an opened chest holds ("ryz takes Candle.") **(verified)** | Take | - | - | `system_take` | shown |
| Player verbs | Seek | Describes what is in front: "It's a treasure chest!", "Someone is standing in front of you!", else "You searched carefully, but you didn't notice anything unusual." **(verified)** | Seek | - | - | `system_seek_chest`, `system_seek_person` | shown |
| Player verbs | Item: Use / Discard | Lists carried items; Use applies one (Lantern lights a cave) **(verified)** | Item | - | - | `inventory_items`, `system_lantern` | shown |
| Player verbs | Equip | Put on / Remove / Stop, then Weapon / Shield / Armor and a list **(verified)** | Equip | - | - | `inventory_equip`, `inventory_readied`, `22_equip_weapon` (start) | shown |
| Player verbs | Str | Status window: name, condition, level, EXP, next level, HP, MP, STR, AC, INT, DEX, LUK, KIM **(verified)** | Str | - | - | `inventory_status`, `16_status` (start), `35_status_after` (start) | shown |
| Characters and progression | Levels | EXP reaching "Next level EXP" raises the level when the battle ends, several levels at once if earned; the status window opens by itself **(verified: EXP 2423 gave level 1 to 5 in one battle)** | - | level 2 at 90 EXP, level 5 next at 3000 **(RAM)**; level 1 33 HP, level 2 about 60 HP, level 5 162-164 HP (random part) **(RAM)** | - | `battle_levelup` | shown |
| Characters and progression | Statistics | STR, AC, INT, DEX, LUK grow with levels; readying a weapon raises STR (Bronze Sword: 4 to 32) **(verified)** | - | level 1: STR 4, AC 8, INT 7, DEX 103, LUK 6; level 5: STR 73, AC 56, INT 59, DEX 314, LUK 35 (sword readied) **(verified)** | - | `inventory_status`, `battle_levelup`, `35_status_after` (start) | shown |
| Resources and economy | Kims (money) | Paid per enemy killed (slime 1-2), spent in shops and inns; halved at a revival **(verified)** | - | Blade gives 200 **(verified)** | - | `shop_weapon`, `gameover_revived`, `35_status_after` (start) | shown |
| Resources and economy | Weapon shop | Buy / Sell / Stop; a price list, "Is X OK?", sale offers about 30% of the price **(verified)** | Talk to the keeper | Bronze Sword 100 (sells 30), Leather Shield 50, Small Shield 80, Leather Armor 200, Bronze Armor 400 **(verified)** | - | `shop_weapon`, `shop_buy_confirm`, `shop_sell_offer` | shown |
| Resources and economy | Magic shop | Spell books bought like goods **(verified: Parma)** | Talk | Ferros 500, Sangua 800 kims **(verified)** | - | `gameplay_magic_shop`, `shop_magic_list`, `shop_magic_bought` | shown |
| Resources and economy | Inn | A night restores the prince for a fee **(verified)** | Talk, Yes | Parma 13 kims **(verified)** | - | `shop_inn_offer`, `system_inn_rest`, `system_inn_morning` | shown |
| Conflict | Real-time battle | Random encounter on the overworld or in caves; a side-view field where the prince moves freely and enemies touch him for damage **(verified)** | D-pad, C, A | slimes hit about 3 HP per touch at level 1 **(verified)** | - | `gameplay_battle_fade`, `battle_start`, `battle_first`, `battle_attack`, `battle_blue_slimes`, `battle_goblins` | shown |
| Conflict | Sword | One swing per C press; holding C does nothing **(verified)** | C | - | - | `battle_attack`, `28_battle_swing` (start) | shown |
| Conflict | Battle end | Last enemy killed: fade back to the overworld; no result screen; EXP and kims were added per kill **(verified)** | - | - | - | `battle_levelup` | shown |
| Conflict | Escape | Walking off the left or right edge of the battle field leaves the battle with no penalty **(verified)** | D-pad | - | - | none: an escape is a fade to the overworld, the same frame as an ordinary road view | described |
| Opponents | Encounters | Enemies appear on the road ahead in the first-person view, walk toward the prince, then the battle starts; the group type is one byte (FFC68B, 0-0x55; 0x56 and up crash) **(verified, RAM)** | - | groups of 1-8 **(verified)** | [content.md](content.md) | `gameplay_encounter_slime`, `gameplay_encounter_blue`, `gameplay_encounter_goblin`, `battle_tree_monsters`, `battle_crawlers` | shown |
| Items and equipment | Equipment slots | Weapon, shield, armour; each readied item adds to STR or AC **(verified for the weapon)** | Equip | - | - | `inventory_equip`, `inventory_readied` | shown |
| Items and equipment | Light | A cave is black until a Candle or Lantern is used; a Lantern lasts the whole cave, a Candle does not **(verified: black view; ROM text for the duration)** | Item, Use | - | - | `gameplay_cave_dark`, `system_lantern`, `gameplay_cave_lit` | shown |
| Abilities and magic | Spell books | Each spell is a book; Magic: Cast (field spells), Ready (choose the battle spell), Discard **(verified)** | Magic | 23 spells in the ROM **(ROM text)** | [content.md](content.md) | `menu_magic_cast`, `menu_magic_ready`, `menu_magic_ready_list`, `system_magic_readied` | shown |
| Abilities and magic | Battle magic | The readied combat spell is cast with A in battle and costs MP (Ferros: 1 MP) **(verified)** | A | Ferros 1 MP **(verified)** | - | `battle_magic`, `env_overworld_parma` | shown |
| Abilities and magic | Aries (town return) | Field spell listing the towns already visited; the view fades out and the prince stands at the chosen town's gate **(verified: only Wyclif before Parma)** | Magic, Cast | 13 MP (37 to 24) **(verified)** | set `seq-aries` | `system_aries_towns`, `system_aries_arrival`, seq-aries `01_cast` ... `07_wyclif` | shown |
| Items and equipment | Griffin Wing | Item, Use: the same fade and arrival at Wyclif's gate as Aries, without MP; the wing is used up **(verified: arrival frame equals Aries's)** | Item, Use | - | - | `system_griffin_wing` | shown |
| World and navigation | Towns | Top-down, walk into doors; Wyclif and Parma **(verified)** | D-pad | 14 towns **(ROM text)** | - | `start_wyclif_gate`, `env_wyclif_blade_house`, `env_parma_gate`, `env_parma_church`, `env_parma_street`, `env_parma_fountain` | shown |
| World and navigation | Overworld | First-person, 16x16 squares per map, forward/back and 90-degree turns; walking onto a town or cave square enters it **(verified)** | up, down, left, right | about 40 frames a step **(verified)** | [../playbook.md](../playbook.md) | `env_overworld_road`, `env_overworld_trees`, `env_overworld_meadow`, `env_overworld_north`, `env_overworld_hills`, `gameplay_cave_entrance` | shown |
| World and navigation | Caves | First-person stone mazes of one 16x16 map with barred doors and chests; the entrance ladder leads out **(verified)** | as overworld, Open | - | - | `gameplay_cave_lit`, `gameplay_cave_door`, `env_cave_corridor`, `gameplay_cave_chest` | shown |
| World and navigation | Area map panel | The top-right panel shows the current 16x16 map only if the party owns its map; without one it shows just the prince's marker (a medallion outdoors, a small figure in caves). One flag byte per map in a 16x16 grid of maps (FFC820 + y*16 + x); the panel is drawn when a map is entered (leaving a town, crossing a map edge) and after a mirror; owned maps stay owned **(verified, RAM)** | - | 256 map flags **(RAM)** | [../playbook.md](../playbook.md) RAM map | `env_overworld_road`, `gameplay_cave_dark`, `map_area_wyclif`, `map_area_south`, `map_area_hills`, `map_area_east`, `map_cave_south`, `map_cave_east` | shown |
| World and navigation | Maps from people | Villagers hand out maps as part of their lines (Wyclif: the man by the well, after the ring: "Here is a map of the route to Parma." sets the five maps from Wyclif to Parma); ROM text has some 30 such gifts, chests can hold maps ("There's a map inside!") **(verified for Wyclif; ROM text)** | Talk | 5 maps in the Wyclif gift **(RAM)** | - | `dialogue_map_gift`, `map_area_wyclif` | shown |
| Items and equipment | Mirror of Atlas | Item, Use: "We have maps of the whole world." sets all 256 map flags (caves too) and is used up **(verified, RAM)** | Item, Use | - | - | `system_mirror_atlas`, `map_world_mirror`, `map_area_south`, `map_cave_south` | shown |
| Items and equipment | Titania's Mirror | Item, Use outdoors: "A glowing map of this area appears in the mirror." (the current map); in a cave: "Nothing happened!" **(verified)** | Item, Use | - | - | `system_titania_mirror`, `system_titania_cave` | shown |
| World and navigation | Transitions | Every change of place is a fade through black: town to overworld and back, cave entry, battle start (the view darkens, then the enemies drop onto the field), Aries and the Griffin Wing **(verified)** | - | about 60-90 frames **(verified)** | set `seq-aries` | `gameplay_battle_fade`, `battle_start`, seq-aries `03_fade`, `06_enter_fade` | shown |
| Goals and gating | Blade's words | Every door in Wyclif and its south gate stay shut until Blade has spoken **(verified)** | Talk | - | - | `cutscene_blade_deathbed`, `14_wyclif_open` (start) | shown |
| Goals and gating | Rings and the sword | Eight rings of good and the Sword of Vermilion against Tsarkon **(source: Wikipedia; ROM text)**. The Ring of Wisdom is kept by an old man at the north-west end of the cave south of Wyclif (through the north-east barred door); receiving it sets FFC818, which switches Wyclif's people to their third set of lines **(verified, RAM)** | Talk | - | - | `dialogue_ring_keeper`, `gameplay_ring_keeper` | shown |
| Goals and gating | Story phases in towns | A town's lines come from one of several tables chosen on entry by story flags (Wyclif: FFC818 ring received, else FFC720 Blade has spoken, else the first table) **(verified, ROM 0x1EB0C)** | - | 14 people in Wyclif **(ROM)** | [findings.md](findings.md) | `dialogue_map_gift` | shown |
| Pacing and difficulty | Story presentation | Boot: SEGA, the tree on the cliff rises, lightning, the title letters fly in; New game: a four-page illustrated prologue that runs by itself (no skip), then play **(verified)** | - | about 4000 frames **(verified)** | - | `cutscene_intro_rise`, `cutscene_intro_tree`, `cutscene_title_letters`, `cutscene_prologue_tsarkon`, `cutscene_prologue_fought`, `cutscene_prologue_blade`, `cutscene_prologue_flight`, `cutscene_prologue_years` | shown |
| Chance | Encounters, level gains | Encounters come on steps at random; level-up gains differ (MHP 162 or 164 at level 5 on two runs) **(verified)** | - | - | - | none: a roll has no screen of its own | described |
| Failure and recovery | Death and revival | HP 0: the prince falls, wakes in the church ("Arise, brave warrior!") with half his kims, EXP kept **(verified)** | - | kims halved (108 to 54) **(verified)** | - | `gameover_revived`, `30_prince_falls` (start), `31_revived` (start) | shown |
| Saving and sessions | Church save | Talk to the priest: Remove a curse / Apply poison balm / Save your game / Stop; three slots; Continue on the title **(verified)** | Talk | 3 slots | - | `save_church_menu`, `save_slots`, `menu_continue_slots` | shown |
| Pacing and difficulty | Opening | A level-1 prince with a Bronze Sword loses to the first pack of slimes in about 600 frames **(verified: start set)**; the game expects fighting near Wyclif first | - | - | - | `29_battle_hurt` (start) | shown |

## 3. How the systems feed each other
- Kills give EXP and kims at once -> levels at battle end raise HP and statistics -> fights further away.
- Kims -> weapon, armour, spell books, inn nights -> fights; death halves kims (the money sink of failure).
- Spell books -> one readied combat spell (A in battle) and field spells (Aries back to visited towns).
- Light items -> caves -> chests and the rings the story asks for.

## Open questions
- Bosses: not reached. The Ring of Wisdom was found (old man, cave south of Wyclif). The Cave of Troy east of
  Parma (Parma's king wants its Treasure; "the cave does have its guardians") is one 16x16 map with a ladder up at
  window (29,16); its chests and guardians were not reached. Poking the encounter type above 0x55 crashes; the
  boss trigger is not known.
- Ending: its text (ROM 0x17722, "Mother, let's go back to the village...") and the staff roll (0x179CA) exist;
  how to start it without the last boss was not found (no 68000 disassembler at hand).
- What Sangua does (bought, not cast); spell costs other than Ferros; the AR/RAM spell word's high byte (02 = combat?).
- Message speed option (ROM text "Message Speed") not found.
