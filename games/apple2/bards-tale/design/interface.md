# The Bard's Tale: Tales of the Unknown - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface. The same shots also
appear in [systems.md](systems.md) (rules) and [content.md](content.md) (variety). Notation:
[README.md](README.md). Check: `python3 tools/lenses.py apple2/bards-tale`. Shot ids are from the `main` set.
A judgement is written as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only. Menus show their choices as `(L)etter` entries and take the letter; members are
  chosen by number 1-6; monster groups by letter A-D; Y-N questions take Y or N; names, spell codes, riddle
  answers and tips are typed and ended with Return (`spell_cast_prompt`, `gameplay_ky_riddle`). ESC aborts
  creation and target choices. Movement: I forward, K kick (doors, buildings), J and L or the arrows turn
  **(verified)**. One key is buffered at a time (Apple II latch).
- **Layout:** one fixed screen for everything (`hud_city`): the picture window top left (street view, dungeon
  view, building or monster portrait) with the place name under it, the title banner "The Bard's Tale" top
  right, the message window below the banner, a column of status icons between picture and message (light,
  compass, levitation, detection: `spell_maco`, `spell_levi`, `spell_aren`), and the party roster across the
  bottom (name, AC, Hits, Cond, SpPt, Cl) **(verified)**.
- **Text:** capitals and small letters in the message window; menu letters and some key words in colour
  (green or purple through the Apple's colour fringes); the roster's Cond column on a white field.
- **Feedback:** every action answers in the message window; fight reports scroll on their own at about one
  line every 30 frames; messages that need a key end with "(Press a key)" or "Press Any Key...". Money
  questions name the price before asking who pays (`system_roscoe_price`).
- **State visibility:** hit points, condition and spell points of all six are always on screen; gold, level,
  experience only on the member's page (`inventory_hero_stats`); position never (no coordinates, no map) except
  through SCSI (`spell_scsi`); time of day only with `?` (`gameplay_where`).
- **Help and onboarding:** none in the game: the command keys are in the manual.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Crack banner and EA logo | transition | power-on -> title | credits of the crack | "Soft-cracked by Number 6", EA, "Thanks to the artist" | - | - | `boot_crack` | not part of the original game |
| Title | screen | boot -> disk prompt | title, song verse | bard and drinker, black and white then colour, verse lines | any key | - | `title_bw`, `title_colour` | - |
| Utilities | menu | title -> Guild | disk tools before play | Start game, Copy, Make a disk, Transfer | S C M T | - | `menu_utilities` | - |
| Guild of Adventurers | menu | start, city -> roster, disk options, city | party management | Check roster, Add, Remove, Disk options, New order, View, Exit | C A R D N 1-6 E | - | `menu_guild` | - |
| Roster | list | Guild C | characters and parties on the disk | names with class, `*` parties | any key | - | `menu_roster` | - |
| Disk options | menu | Guild D | make, save, delete, leave | Create, Save party, Delete, Leave the game | C S D L E | - | `menu_disk_options` | - |
| Race choice | menu | Create | first step of creation | seven races | 1-7, ESC | - | `system_race` | - |
| Attributes and class | menu | race | rolled attributes and allowed classes | St IQ Dx Cn Lk HP, classes by number | 0-9, ESC | only classes open to the race are listed | `system_class` | no re-roll key |
| Member page | screen | 1-6 anywhere | statistics | race, class, attributes, level, spell points, experience, gold | any key -> items | - | `inventory_stats`, `inventory_hero_stats` | - |
| Items page | menu | member page | items and spell levels | 8 slots with marks, Sorc Conj Magi Wizd levels | E T D P | Equip asks a slot number | `inventory_items`, `inventory_hero_spells`, `inventory_bard_items` | - |
| Street view | screen | Guild exit | the city around the party | buildings, street, "Facing north" after a turn | movement keys | - | `hud_city`, `env_city_street`, `env_city_houses` | - |
| Location message | message | ? | where and when | street name, time of day | - | - | `gameplay_where` | - |
| Building messages | message | kicking into a square | what stands here | gate, statue, iron gate, magic mouth, entry chambers, portal question | A L T Y N, keys | - | `gameplay_gate`, `gameplay_guardian`, `gameplay_iron_gate`, `gameplay_magic_mouth`, `gameplay_castle_entry`, `gameplay_tower_entry`, `gameplay_sewer_portal`, `extra_credits` | - |
| Shop greeting and menu | menu | Garth's square | trade | greeting, then Buy Sell Identify Pool Exit with the gold | member, B S I P E | - | `shop_garth`, `shop_menu`, `shop_pool` | - |
| Shop lists | list | Buy, Sell, Identify | goods and prices | 9 lines per page, gold, P)urchase F)orward B)ack or "Sell item #(1-8)" | numbers, F B | - | `shop_buy`, `shop_buy2`, `shop_sell`, `shop_identify` | names cut to 10 letters ("Broadswor") |
| Review Board | menu | its square | levels, spells, class | Advancement, Spell acquiring, Class change | A S C E, member, Y-N | "still needeth N experience", "must know at least 3 spell levels" | `system_review`, `system_review_xp`, `system_advance`, `system_spell_buy`, `system_class_change` | - |
| Temple | menu | temple squares | healing | welcome, then the price per member | member, payer | - | `system_temple` | - |
| Roscoe's | menu | its square | spell points | welcome, price | member, payer | - | `system_roscoe`, `system_roscoe_price` | - |
| Tavern | menu | tavern squares | drinks, talk | Order, Talk, Exit; drink list; tip prompt; rumour | O T E, letters, amount | "Talk ain't cheap" | `dialogue_tavern`, `dialogue_drinks`, `dialogue_barkeep`, `dialogue_barkeep_tip`, `dialogue_rumour` | - |
| Mad God priest | prompt | temple of the Mad God, S | entrance by name | "What wilt thou say?" and a typed answer | text | - | `dialogue_madgod` | - |
| New order | prompt | N | reorder | numbered picks | 1-6 | - | `menu_new_order` | - |
| Use / Party attack | prompt | U, P | out-of-fight commands | who uses; the attack options | member, letter | - | `system_use`, `system_party_attack` | - |
| Cast prompt | prompt | C | spells | who casts, then "Spell to cast:" and a target if needed | member, code, member | unknown codes do nothing visible | `spell_cast_prompt`, `spell_wohl` | **Observation:** a wrong code gives no message, so a typo looks like a spell without effect |
| Status icons | hud element | spells | lasting effects | torch (MAFL), blue light (LERE), compass (MACO), feather (LEVI), eye (AREN) | - | - | `system_mafl`, `spell_lere`, `spell_maco`, `spell_levi`, `spell_aren` | - |
| SCSI report | message | spell | position | facing, levels below, squares north and east of the entry stairs | key | - | `spell_scsi` | the only position readout |
| Bard prompt | prompt | B | songs | who plays, "Play tune #[1-6]" | member, 1-6 | "He is not using an instrument!" | `song_no_instrument`, `song_prompt` | - |
| Dungeon view | screen | entrances, stairs | the corridor ahead | walls and doors up to three squares, level name | movement keys | black without light | `env_cellar_corridor`, `env_cellar_door`, `env_kylearan_door`, `env_mangar3_door` | - |
| Stairs question | prompt | stepping on stairs | change level | "There are stairs here, going down. Do you wish to take them? [Y-N]" | Y N | - | `gameplay_stairs` | - |
| Dungeon messages | message | special squares | events | inscriptions, voices, traps, darkness, smoke | key or typed answer | - | `gameplay_sewers_arrival`, `gameplay_trap`, `gameplay_darkness`, `gameplay_ky_riddle2`, `gameplay_m5_pool` | - |
| Encounter | prompt | random or forced | fight or run | portrait of the first group (animated), the groups, "Fight or Run?" | F R | - | `battle_encounter`, `battle_green_dragons` | - |
| Round orders | menu | F | one order per member | the member's options | A P D U C B, group letter, ESC | "Use these attack commands? (Y-N)" | `battle_target` | - |
| Round report | message | Y | what happened | blows, spells, deaths, "You still face ..." | - (auto-scroll) | - | `battle_round`, `boss_mangar_spell` | **Observation:** the scroll speed is fixed; long rounds cannot be read back |
| Victory | message | last enemy dead | reward | experience and gold per character, items found, treasure picture | key | - | `ending_treasure` | - |
| Party dead | screen | all members dead | game over | "Sorry, bud" portrait, "adventurer heaven" | key | - | `gameover_party_dead` | - |
| Ending | screen | Mangar defeated | ending text | Kylearan portrait and four pages | key | - | `ending_kylearan`, `ending_winter`, `ending_bonus`, `ending_vanishes` | - |

## 3. Screen flow
```
power-on -> crack banner -> title -> (key) "Insert CHARACTER disk" -> Utilities -> Guild
Guild: roster | disk options (create: race -> class -> name; save party) | add / remove | view -> items | exit
  -> city street view -> movement, ?, C, B, U, P, N, 1-6
       -> kick into a square: shop | temple | Roscoe's | Review Board | tavern | Mad God | gates/statues | entries
       -> encounter -> orders -> round report -> (next round | victory | run | party dead -> game over)
       -> dungeon entrance ("Insert DUNGEON disk") -> dungeon view -> stairs / specials / encounters
            -> top of Mangar's Tower -> Mangar -> victory -> Kylearan ending -> dungeon view
```

## 4. Elements in detail
- **Picture window (top left):** street or dungeon view three squares deep; in buildings the keeper's picture;
  in fights the first group's animated portrait with its name below (`boss_mangar_group`).
- **Message window (right):** every prompt and report; menus list their letters; it is cleared on a turn or
  step, but some messages stay until the next action (`gameplay_trap`).
- **Roster (bottom):** six lines, Cond shows the hit points left on a white column or "Dead"; dead members
  are moved to the bottom after a fight round (start set `31_fight_or_run`).

## Open questions
- Whether the portrait animation can be turned off; whether the scroll speed of fights can be set (no such
  key found).
