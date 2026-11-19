# Phantasy Star - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
Coverage so far: the early game (Camineet, the Palma fields next to it, the first cave), set `main`, 53 shots.
Shot ids are those of `../shots/main/index.md`.

## 1. Core loop
Alis walks a top-down town or planet surface; on the surface and in caves, monsters attack at random
**(verified: `battle_sworm`, `battle_wing_eye`)**. Each fight gives experience and sometimes a treasure chest
with meseta **(verified: `battle_exp`, `battle_chest_meseta`)**; meseta buys equipment, food and tools in the
towns **(verified: `shop_armory`, `shop_food`, `shop_list`)**, experience raises the level and the statistics
**(verified: `battle_levelup`, RAM)**. Dark caves need a light before they can be explored **(verified:
`cave_dark`, `dungeon_corridor`)**. What changes between loops: stronger monsters further from Camineet, more
party members, vehicles and other planets **(source)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Walk (towns, surface) | Alis moves tile by tile; walking into a door enters the building **(verified)** | D-pad | 1 pixel per frame, 16 frames per tile **(verified)** | playbook Controls | `camineet_start`, `camineet_shops`, `palma_camineet`, `palma_forest` | shown |
| Player verbs | Walk (first person) | in caves and passages each press steps one square or turns 90 degrees, animated **(verified)** | up / down, left / right | a step takes about 36 frames, a turn about 48 **(verified)** | interface.md section 4 | `dungeon_step`, `dungeon_turn`, `dungeon_corridor`, `camineet_passage` | shown |
| Player verbs | Field menu | STAS, MAGC, ITEM, SRCH, SAVE over a picture of the place **(verified)** | button 1 or 2 | | interface.md | `hud_menu`, `menu_forest` | shown |
| Player verbs | STAS | shows Alis's equipment, level, EP, attack, defense, max HP/MP and meseta **(verified)** | menu | | | `menu_status`, `status_shield` | shown |
| Player verbs | MAGC (field) | with no spells known the command does nothing **(verified: Alis, level 1)** | menu | | | none: no visible answer at level 1 (route `@menu,down,b2`) | described |
| Player verbs | ITEM: USE / EQP / DRP | each carried item can be used, equipped or dropped **(verified)** | menu, item, command | up to 24 items **(RAM)** | | `menu_items`, `item_commands`, `item_equip`, `item_use_burger` | shown |
| Player verbs | DRP | drops the item **(source: manual)** | ITEM, DRP | | | none: not tried in this run | described |
| Player verbs | SRCH | searches the square ahead; nothing found gives "There doesn't seem to be anything" **(verified)** | menu | | | `menu_search` | shown |
| Player verbs | Talk to townspeople | the manual says to talk to people **(source)**; walking into a townsperson or a robotcop, and pressing a button beside one, did nothing here: the button opens the field menu **(verified)** | unknown | | findings.md | none: the way to start a talk was not found | open |
| Player verbs | Enter buildings | walking into a door opens a scene inside: shop, church, house, passage **(verified)** | D-pad | | | `alis_home`, `camineet_church`, `shop_secondhand`, `camineet_passage` | shown |
| Characters and progression | Fixed heroes, no naming | Alis starts alone; nobody is named by the player **(verified)** | none | | playbook Naming | `menu_status` | shown |
| Characters and progression | Levels | experience raises the level; level 2 comes at 20 EP **(RAM: 18 EP + 2 levelled, 17 + 2 did not)** | fight | level 1: HP 16, attack 12, defense 13; level 2: HP 20, attack 14, defense 16 (without shield) **(RAM)** | | `battle_levelup`, `menu_status` | shown |
| Characters and progression | Equipment adds to statistics | weapon, armour and shield add to attack and defense **(verified: the leather shield raised defense 13 to 16)** | ITEM, EQP | leather shield +3 defense **(verified)** | | `status_shield`, `item_equip` | shown |
| Resources and economy | Meseta | the money; from chests and sales; shown in ITEM, STAS and shop windows **(verified)** | | Alis starts with 0 **(verified)** | | `menu_items`, `battle_chest_meseta`, `shop_list` | shown |
| Resources and economy | Shops | armory, food shop and second-hand shop in Camineet; a purchase is taken at once, without a confirm **(verified)** | BUY / SELL, list, YES / NO | food: COLA 10, BURGER 40; armory: LTH. SLD 30, IRN. SLD 520, CRC. SLD 1400; second-hand: FLASH 20, ESCAPER 10, TRANSER 48 **(verified)** | content.md | `shop_food`, `shop_bought`, `shop_armory`, `shop_list`, `shop_secondhand` | shown |
| Resources and economy | Selling | the second-hand shop buys items back at half their price **(verified: ESCAPER 10 -> 5)** | SELL, item, YES / NO | 50% **(verified, one item)** | | `shop_sell`, `shop_sell_offer` | shown |
| Conflict | Battle commands | ATTK, MAGC, ITEM, TALK, RUN per party member **(verified)** | menu | | | `battle_sworm`, `battle_wing_eye` | shown |
| Conflict | Attack and damage | Alis strikes first, then the monster; the struck monster flashes, a hit on the party flashes the whole screen **(verified)** | ATTK | short sword on a Sworm: 5 damage (HP 8 -> 3); Sworm on Alis: 1-2 damage **(verified)** | | `battle_attack`, `battle_hit`, `battle_killed` | shown |
| Conflict | TALK | talking to a monster; a Sworm "cannot understand" **(verified)**; some monsters answer **(source)** | TALK | | | `battle_talk` | shown |
| Conflict | RUN | the screen fades out and Alis is back on the map, no message **(verified: one try against a Sworm)**; a second monster may block the way **(source)** | RUN | | | none: only a fade to black, no screen of its own | described |
| Conflict | Death | a member at 0 HP dies; with nobody left: "Alis's hope cannot overcome the power of Lassic. The adventure is over." and the title **(verified)** | | | | `battle_died`, `gameover` | shown |
| Opponents | Random encounters | one monster at a time so far, on the surface and in caves **(verified)** | | first SWORM after about 10 long walks; in the cave after 5 paces **(verified)** | content.md | `battle_sworm`, `battle_scorpion`, `battle_wing_eye` | shown |
| Items and equipment | Food | BURGER heals: Alis 9 -> 16 HP (her maximum) **(verified)** | ITEM, USE | | | `item_use_burger` | shown |
| Items and equipment | Equipment slots | weapon, armour, shield shown under STAS **(verified)** | EQP | | | `item_equip`, `status_shield` | shown |
| Abilities and magic | Spells | Alis has none at level 1 (MP 0) **(verified)**; Myau and Noah cast spells **(source)** | MAGC | | | none: no spell known in the early game | described |
| World and navigation | Towns and surface | Camineet is a walled town with an EXIT gate to the Palma surface **(verified)** | | | | `camineet_gate`, `palma_camineet` | shown |
| World and navigation | Darkness and light | a dark cave cannot be entered without light; a FLASH lights it **(verified)** | ITEM, USE FLASH | | | `cave_dark`, `dungeon_corridor` | shown |
| World and navigation | Lit passages | the passage under Camineet's grey dome is lit and needs no FLASH **(verified)** | | 16x16 squares per floor **(RAM)** | | `camineet_passage` | shown |
| World and navigation | Treasure on the floor | caves hold chests on fixed squares, opened with YES **(verified: 10 meseta)** | YES / NO | | | `dungeon_chest` | shown |
| Goals and gating | Story start | Nero's dying words name Lassic and send Alis on her way **(verified)** | | | | `intro_nero_beaten`, `intro_nero_dying`, `intro_alis_vow` | shown |
| Goals and gating | Guarded gate | a gate in western Camineet is guarded by two robotcops **(verified, picture)**; what opens it is not known | | | | `camineet_gate` | open |
| Chance | Encounters and rolls | follow frame timing: the same route meets the same monster **(verified, emulator)** | | | playbook Emulation notes | none: a rule without a screen | described |
| Chance | Monster chests | a beaten monster may leave a chest with meseta **(verified)** or a trap **(source)** | YES / NO | SWORM: 3 meseta **(verified)** | | `battle_chest`, `battle_chest_meseta` | shown |
| Failure and recovery | Church | resurrects dead members; with Alis alive it says so **(verified)** | YES / NO | price not seen | | `camineet_church`, `church_alive` | shown |
| Saving and sessions | Save | SAVE anywhere outside battle to one of five slots; CONTINUE loads or deletes **(verified)** | menu, slot | 5 slots **(verified)** | | `save_slots`, `continue_prompt`, `continue_slots` | shown |
| Pacing and difficulty | Early danger | Alis alone with 16 HP; Sworm 8 HP, Scorpion 12, Wing Eye 11 **(verified)** | | | content.md | `battle_scorpion`, `battle_wing_eye` | shown |


### 2b. The rest of the game (capture 2026-11-19, part 2)
Shot ids of `../shots/main/index.md`; `battles:` ids are in `../shots/battles/index.md`, `seq-*:` in the
sequence sets. Values come from the ROM tables (RAM map in the playbook) or the screens.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Talk | take one step toward a person, then push again into them: a scene with the person and a text box opens **(verified)**; a push from standstill does nothing | D-pad | | playbook Controls | `talk_townsperson`, `nekise`, `parolit_medusa`, `bortevo_junk` | shown |
| Player verbs | Questions | many people end on a YES / NO window; the answer branches the talk **(verified)** | up/down, button 2 | | | `npc_question`, `cola_beggar`, `cat_thief`, `dungeon_robotcop` | shown |
| Player verbs | Doors in dungeons | facing a door, button 2 opens it; walking into it does nothing **(verified)** | button 2, up | | interface.md | `seq-dungeon-door:01_door`, `seq-dungeon-door:02_open_clip`, `seq-dungeon-door:04_through` | shown |
| Player verbs | Stairs | stepping onto a stair square fades to black and loads the floor above or below **(verified)** | up | about 90 frames black | | `seq-dungeon-stairs:01_stairs`, `seq-dungeon-stairs:02_climb_clip`, `seq-dungeon-stairs:03_arrived` | shown |
| Player verbs | Dungeon walk and turn | one square per press, a quarter turn per left/right, four turns make a full circle **(verified)** | up, right | step ~36 frames, turn ~48 | | `seq-dungeon-walk:02_step_clip`, `seq-dungeon-walk:06_step4`, `seq-dungeon-turn:02_turn_clip`, `seq-dungeon-turn:06_north` | shown |
| Characters | Party of four | Myau joins in Paseo when the merchant trades him for the Laconian pot; Odin waits in stone in a cave; party size in RAM `C4F0` (members - 1) **(verified)** | | Myau joins at level 1 (HP 22) **(RAM)** | playbook RAM map | `myau_merchant`, `myau_trade`, `myau_traded`, `myau_meet_alis`, `myau_meet`, `odin_stone` | shown |
| Characters | Level tables | per character and level: max HP, attack, defense, max MP, EXP needed, number of battle and field spells (ROM `F8AF`, 4 x 30 levels) **(RAM)** | | Alis L1 16 HP / L30 218; Myau L30 214; Odin L30 192, no MP; Noah L30 195 HP, 83 MP | playbook | `magic_who` | shown |
| Resources | Hospital | heals for a fee asked after YES **(verified)** | YES / NO | 10 meseta for Alis alone at the start of the scene **(verified)** | | `hospital`, `hospital_fee` | shown |
| Resources | Shops in dungeons | a few merchants sit inside dungeons (shortcake, gas shield) **(verified)** | | shortcake 1000, gas shield 1000 (ROM text) | | `dungeon_shop` | shown |
| Conflict | Groups | several monsters of one kind come together; the HP box gets one line per monster **(verified)** | | up to 5 lines seen | | `battles:marman_group`, `battles:fishman_group`, `battles:sorcerers` | shown |
| Conflict | Talk in battle | most monsters "cannot understand"; Dezorians and Barbarians answer **(verified)** | TALK | | | `battles:talk_dezorian`, `battles:talk_barbarian` | shown |
| Conflict | Status: stone | Medusa's gaze turns a member to stone **(verified)** | | | | `battles:medusa_attack`, `boss_medusa` | shown |
| Conflict | Party wipe | when every member dies: "You are all dead.", then the game-over pages **(verified)** | | | | `battles:wipe_myau`, `battles:wipe_all` | shown |
| Opponents | Bosses | fixed battles on event squares: Medusa, Dr. Mad, dragons, Titan, Lassic's shadow; table in ROM `EF5C` (floor, square, flag, type, data) **(RAM)** | | Medusa 200 HP, Dr. Mad 233, blue dragon 210, red dragon 175, Titan 190, Lassic 238 | content.md | `boss_medusa`, `boss_dr_mad`, `boss_blue_dragon`, `boss_red_dragon`, `boss_titan`, `boss_shadow`, `battle_skull_en`, `battles:lassic`, `battles:dark_falz`, `battles:gold_dragon`, `battles:magician` | shown |
| World | Three planets | Palma (green), Motavia (sand), Dezoris (ice); each overworld 128 tiles wide, wrapping **(verified)** | | map ids 0 / 1 / 2 in `C309` | playbook | `palma_parolit`, `palma_drasgow`, `palma_coast_cave`, `palma_mountains`, `palma_gothic`, `motavia_desert`, `dezoris_ice`, `dezoris_village` | shown |
| World | Space travel | the spaceport liner (passport) flies Palma - Motavia; later the Luveno, flown by Hapsby, goes to Gothic, Uzo or Skure **(verified)** | YES / NO, destination list | passport 100 meseta (ROM text) | | `palma_spaceport`, `spaceport_guard`, `spaceship_board`, `spaceship_flight`, `paseo_spaceport`, `luveno_ship` | shown |
| World | Vehicles | LANDROVR used from ITEM on the surface turns the party into a tank-like rover; a vehicle used in the wrong place "will do no good" **(verified)** | ITEM, USE | | | `landrover_menu`, `landrover`, `vehicle_no_good` | shown |
| Goals | Key-item chain | the pot buys Myau, the shortcake opens the governor, his letter recruits Noah, the Alsulin cures Odin (ROM text, partly verified) | | | playbook Strategy | `governor`, `mansion_guard` | shown |
| Saving | Save name | a new slot asks for a name on a letter grid (ADV RUB END) **(verified)** | D-pad, button | | | `save_name` | shown |
| Ending | Ending and credits | not reached: Dark Falz dodges every blow when forced outside his chamber; the trigger of the real fight was not found | | | findings.md | (no shot: not reached) | open |

## 3. How the systems feed each other
- Fights -> experience -> levels -> more HP, attack, defense -> safer fights further out.
- Fights and cave chests -> meseta -> armory and food -> better defense and healing.
- Second-hand shop -> FLASH -> light -> dark caves -> chests and stronger monsters.
- Death -> game over -> continue from the last save; the church revives fallen members (source).

## Open questions
- How to talk to townspeople (findings.md).
- Church price and the manual's "experience needed for the next level" at the church: not seen (answering NO
  only gives a blessing).
- Trap chests, multi-monster groups, spells: later in the game.
