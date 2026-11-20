# SWORD OF VERMILION - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py md/sword-of-vermilion`.
Shots: set `main` unless marked (start).

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** three-button pad. C confirms and opens the field command window; B backs out and closes; Start
  chooses on the title and ends the name; A casts the readied spell in battle and does nothing elsewhere seen
  **(verified)**. Lists use an arrow cursor; menus with two columns move with left/right **(verified)**.
- **Layout:** 320x224. Field screens: the view fills the screen in towns; on the overworld and in caves a
  first-person window (top-left), a compass/minimap panel (top-right), KIM/EXP (right), HP/MP and MAGIC (bottom)
  **(verified: `env_overworld_road`)**. Battles keep the bottom HP/MP/MAGIC bar **(verified: `battle_first`)**.
  Menus stack as framed blue windows from the top-left, messages in a wide box at the bottom **(verified)**.
- **Text:** white mixed-case font on dark blue boxes; the hero's name is inserted ("ryz uses the Lantern.")
  **(verified)**. Text types out letter by letter; a page ends with a down-arrow and waits for C **(verified)**.
- **Feedback:** every command answers in the message box, also when nothing happens ("There's no one here to
  talk to.", "You can't use that here.") **(verified)**. Purchases ask "Is X OK?" Yes/No **(verified)**.
- **State visibility:** HP, MP, KIM, EXP and the readied spell are always on screen outside towns; level and the
  other statistics need Str **(verified)**.
- **Help and onboarding:** none in-game beyond townspeople's hints ("Be sure to buy armor, a weapon, and a shield
  before you leave the village.") **(verified, scout)**. **Observation:** the battle buttons (C sword, A magic)
  and the edge escape are not explained anywhere on screen.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| SEGA logo, intro | transition | power-on -> title | boot | logo; tree, sword in the stone, lightning | Start skips to the title | - | `boot_sega`, `cutscene_intro_rise`, `cutscene_intro_tree`, `cutscene_title_letters` | the tree rises from the bottom, a white lightning flash, the two title lines slide in from both sides **(verified)** |
| Title | menu | intro -> keyboard / Continue | start a game | Start / Continue | up/down, Start | C and A do nothing **(verified)** | `title_screen`, `03_title` (start) | - |
| Continue slot list | list | title -> church | load | Saved Game 1-3 with name and level | C | empty slots show level 4096 **(verified, scout)** | `menu_continue_slots` | - |
| Name keyboard | prompt | title -> prologue | name the prince | 10-column letters, END | D-pad, C, B, Start | the only 256-wide screen **(verified)** | `menu_name`, `04_name_entry` (start) | - |
| Prologue | transition | name -> Wyclif | story | captioned pictures | none (runs by itself) | - | `cutscene_prologue_tsarkon`, `cutscene_prologue_fought`, `cutscene_prologue_blade`, `cutscene_prologue_flight`, `cutscene_prologue_years`, `06_prologue_blade` (start), `08_prologue_years` (start) | **Observation:** about 70 s with no skip |
| Town view | screen | world -> doors | walk, meet people | top-down town | D-pad, C | - | `start_wyclif_gate`, `env_parma_gate` | - |
| Field command window | menu | C on any field screen | all actions | 8 commands in 2 columns | D-pad, C, B | - | `hud_field_menu` | - |
| Dialogue box | message | Talk | speech | 3 lines, arrow when more | C per page | - | `dialogue_blade_house`, `cutscene_blade_deathbed`, `dialogue_map_gift`, `dialogue_ring_keeper`, `12_blade_ring` (start) | - |
| Status window | screen | Str, or after a level-up | character sheet | 13 values | B/C closes | - | `inventory_status`, `battle_levelup` | the level-up shows it unasked |
| Item list | list | Item -> Use/Discard | items | up to the carried items | C | "You have nothing to use!" when empty **(verified)** | `inventory_items` | - |
| Equip menus | menu | Equip | gear | Put on/Remove/Stop, Weapon/Shield/Armor, list | C | "ryz readied Bronze Sword." | `inventory_equip`, `inventory_readied` | - |
| Magic menus | menu | Magic | spells | Cast/Ready/Discard, book list | C | "You have no Books of Spells that can be used in combat." | `menu_magic_cast`, `menu_magic_ready`, `menu_magic_ready_list`, `system_magic_readied` | - |
| Aries town list | list | Magic, Cast, Aries | town return | visited towns | C | fade out, the prince at the town's gate | `system_aries_towns`, `system_aries_arrival`, set `seq-aries` | - |
| Area map panel | hud element | top right outside towns | where am I | the current 16x16 map (roads, trees, hills, towns, cave walls) with the prince's marker, or only the marker without a map | - | redrawn on entering a map | `map_area_wyclif`, `map_area_south`, `map_area_hills`, `map_area_east`, `map_cave_south`, `map_cave_east`, `env_overworld_road` | **Observation:** the only map the game has; no full-screen world map |
| Mirror messages | message | Item, Use | maps | "We have maps of the whole world." / "A glowing map of this area appears in the mirror." / "Nothing happened!" | C | the panel fills at once | `system_mirror_atlas`, `map_world_mirror`, `system_titania_mirror`, `system_titania_cave` | - |
| Transitions | transition | doors, gates, cave squares, encounters, travel | change of place | fade to black and back | none | - | `gameplay_battle_fade`, `battle_start`, seq-aries `03_fade`, `04_warp_clip`, `06_enter_fade` | **Observation:** one fade for everything; the battle start adds enemies dropping in |
| Shop | menu | Talk to a keeper | trade | Kim window, Buy/Sell/Stop, price list, Yes/No | C, B | "Anything else for you today?" | `shop_weapon`, `shop_buy_confirm`, `shop_sell_offer`, `shop_magic_greeting`, `shop_magic_list`, `shop_magic_bought` | after a buy the cursor stays where it was **(verified, scout)** |
| Inn | prompt | Talk to the innkeeper | rest | price question, Yes/No | C | fade to black, "You look much better this morning!" | `shop_inn_offer`, `system_inn_rest`, `system_inn_morning` | - |
| Church menu | menu | Talk to the priest | save, cures | 4 entries, slot list | C | "Your game was saved successfully!" | `save_church_menu`, `save_slots`, `34_saved` (start) | the menu shows no cursor until a key is pressed **(verified)** |
| Overworld view | screen | town gate -> towns, caves, battles | travel | first-person road, side panels | up/down/left/right, C | - | `env_overworld_road`, `env_overworld_meadow`, `env_overworld_parma` | - |
| Cave view | screen | cave square | explore | first-person stone walls, minimap icon | as overworld | black without light | `gameplay_cave_dark`, `gameplay_cave_lit`, `env_cave_corridor` | - |
| Chest and door messages | message | Open / Take | loot | "You opened the chest. There's Candle inside!" | C | - | `system_open_chest`, `system_take`, `system_open_door`, `system_open_money`, `system_seek_chest`, `system_seek_person` | Seek names what stands in front |
| Battle screen | screen | encounter -> overworld | fight | side view, HP/MP/MAGIC bar | D-pad, C, A | fade out at the end | `battle_start`, `battle_first`, `battle_attack`, `battle_magic`, `battle_goblins`, `battle_cyclopes` | - |
| Revival | message | HP 0 -> church | failure | "Arise, brave warrior! ..." | C | - | `gameover_revived`, `31_revived` (start) | - |
| HUD panels | hud element | always outside towns | state | KIM, EXP, HP/MHP, MP/MMP, MAGIC (readied spell) | - | MAGIC reads "nothing" with no spell readied | `env_overworld_road`, `env_overworld_parma` | - |

## 3. Screen flow
- Power-on -> SEGA -> intro -> title -> Start -> name keyboard -> prologue -> Wyclif (town)
  - title -> Continue -> slot list -> church of the save
- Town <-> doors (houses, shops, inn, church) ; town gate <-> overworld
- Overworld -> encounter -> battle -> overworld (win, escape) or church (death)
- Overworld <-> cave (entrance square / ladder) ; overworld -> town square of another town
- Any field screen -> C -> command window -> sub-menus -> message box -> B back

## 4. Elements in detail
Overworld (`env_overworld_road`): top-left 160x136 first-person view; top-right the area map panel: the prince's
marker (a medallion outdoors, a small figure in caves), on the area map when it is owned (`map_area_wyclif`); right column KIM and EXP; bottom-left HP current/maximum and MP current/maximum;
bottom-right MAGIC with the readied spell's name or "nothing" **(verified)**. Battle (`battle_first`): full-width
field, the same bottom bar, no enemy names or HP shown **(verified)**.

## Open questions
- Where Message Speed (ROM text) is set; whether Start does anything in the field.
- The boss screen layout (not reached).
