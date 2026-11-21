# Beyond Zork: The Coconut of Quendor (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The player reads a room description, types a command at the `>` prompt and reads the answer: move by compass
direction, examine and take things, talk to people, solve a puzzle **(verified, `gameplay_hilltop`,
`dialogue_riddle`)**. On top of that sits a role-playing layer: monsters attack on the moors and in the cellar,
fights are won with typed ATTACK commands, won fights raise experience and level, and the six attributes decide
who wins **(verified, `battle_vapor_attack`, `battle_vapor_won`)**. Loot (potions, scrolls) and money from
selling it buy equipment in the shops of Mizniaport **(verified, `shop_sell`, `shop_buy`)**. Between loops
the world grows: the village, the moors, the seaport, Gurth City beyond **(verified, `env_intersection`)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Movement | compass directions, UP/DOWN, ENTER; blocked exits answer in a sentence ("Tall reeds block your path", "too steep") | `n` `ne` ... `u` `d`, `enter opening` | - | playbook "Game structure" | `env_cove_street`, `system_lightning`, `gameplay_lighthouse_1st` | shown |
| Player verbs | Looking and examining | LOOK (F1), EXAMINE (F4) any noun; READ for writing | `look`, `examine oak`, `read inscription` | - | - | `dialogue_riddle`, `gameplay_pterodactyl`, `dialogue_unicorn` | shown |
| Player verbs | Taking, wielding, wearing | TAKE (F5) picks up; WIELD readies a weapon; WEAR puts on armour (armor class up) | `take driftwood`, `wield shillelagh`, `wear cloak` | cloak: armor class up (message) | - | `system_driftwood`, `inventory_cloak_worn` | shown |
| Player verbs | Talking | `PERSON, TEXT` addresses someone; ASK X ABOUT Y | `cook, hello`, `ask woman about case` | - | - | `dialogue_cook_busy`, `dialogue_sailor`, `dialogue_woman` | shown |
| Player verbs | Saying words | SAY a word to a puzzle (the Ledge riddle answer opens the cliff) | `say lightning` | - | - | `env_lighthouse` | shown |
| Player verbs | Drinking, shaking | DRINK uses a potion; SHAKE is accepted | `shake potion`, `drink potion` | - | - | `system_potion_drink` | shown |
| Player verbs | Function keys | F1-F10 type ten command macros; DEFINE edits them | F1 LOOK AROUND ... F10 OOPS | 10 keys | playbook "Controls" | `options_define_keys`, `inventory_list`, `inventory_status` | shown |
| Player verbs | UNDO | F9 / UNDO takes back the last move (not in combat; offered after a death outside combat) | `undo` | 1 move | - | `system_undo`, `gameover_grue` | shown |
| Characters and progression | Character Setup | preset Frank Booth, six named presets, random roll, or 60% potential spread by hand | arrows, enter, SPACE | 60% potential (verified) | - | `menu_character_setup`, `menu_select_preset`, `menu_random_character`, `menu_random_reroll`, `menu_create_character`, `menu_create_adjust`, `menu_create_confirm` | shown |
| Characters and progression | Sex and name | Create your own asks male or female and a name (default "Frank Booth"), then confirms twice and offers to save the character | typed answers | - | - | `menu_create_name`, `menu_create_done`, `menu_create_begin`, `inventory_ryz_status` | shown |
| Characters and progression | Attributes | Endurance, Strength, Dexterity, Intelligence, Compassion, Luck and Armor Class, shown as bars with percentages | F3 STATUS | Frank Booth: EN 16, ST 8, DX 8, IQ 8, CM 1, LK 25, AC 0 (verified) | - | `inventory_status`, `system_mode_standard` | shown |
| Characters and progression | Experience and level | won fights raise experience; the first win gives Level 1 | fights | experience 9 after the vapor, 16 after a guttersnipe, still Level 1 (RAM) | - | `battle_vapor_won`, `battle_guttersnipe_won` | shown |
| Characters and progression | Level 2 and beyond | not reached in this run (37 experience was still Level 1) | - | - | - | none: not reached (open) | open |
| Resources and economy | Zorkmids | cash; CASH or `$` shows it; the game starts you with 1 | `$` | 1 at the start (verified) | - | `inventory_list`, `shop_buy` | shown |
| Resources and economy | Shops: buying | ask for an item; the price is named when you cannot pay; when you can the item is set out for you to take | `buy cloak` | cloak 30 zorkmids (verified) | - | `shop_display_case`, `shop_price`, `shop_buy` | shown |
| Resources and economy | Shops: selling | the shopkeeper buys found items | `sell scroll` | rumpled scroll: 5 zorkmids (verified) | - | `shop_sell` | shown |
| Conflict | Combat | typed ATTACK (F7 ATTACK MONSTER); each blow hits or misses, the monster answers; wound words (noticeably, seriously, dangerously, gravely, decisive) report its state | `attack vapor`, F7 | Level 0 peasant vs eldritch vapor: 4 attacks (verified) | - | `battle_vapor_attack`, `battle_guttersnipe_strong`, `battle_ratant_flees` | shown |
| Conflict | Combat monitor | Endurance bar in the room window while fighting; MONITOR turns it off | `monitor` | - | - | `battle_vapor_attack`, `options_monitor` | shown |
| Conflict | Monsters retreat | a beaten monster often flees rather than dies ("retreats into the darkness/fog") | - | - | - | `battle_ratant_flees`, `battle_guttersnipe_won` | shown |
| Conflict | Refused fights | the game refuses hopeless attacks (bandits: "Suicide") and some targets (the cook) | - | - | playbook | none: refusal text not kept in the set (playbook "Traps") | described |
| Conflict | Endurance recovery | endurance returns to normal after a fight when you move on | walking | message "[Your endurance is back to normal.]" (verified) | - | `battle_guttersnipe` | shown |
| Opponents | Monsters | eldritch vapor, guttersnipe, rat-ant fight; a wounded pterodactyl only snaps | - | - | [content.md](content.md) | `battle_vapor_appears`, `battle_guttersnipe_odors`, `battle_ratant`, `gameplay_mud_flats` | shown |
| Items and equipment | Weapons | driftwood becomes a shillelagh; a rusty dagger in the kitchen | `take`, `wield` | - | - | `system_driftwood`, `dialogue_kitchen_cook` | shown |
| Items and equipment | Armour | cloak, leather tunic, scale mail, plate mail in the boutique | `buy`, `wear` | - | - | `shop_display_case`, `inventory_cloak_worn` | shown |
| Items and equipment | Potions | found lying about; "Shake before using"; drunk at once, effect not obvious | `drink` | - | - | `inventory_potion_examine`, `system_potion_drink` | shown |
| Items and equipment | Scrolls and identification | a scroll's magic word is random per game (Watkin in one run, Blarn in another); READ gives only a hint (refreshment, weaponry) | `read scroll` | - | [findings.md](findings.md) | `inventory_scroll_blarn`, `inventory_scroll_macuga` | shown |
| Abilities and magic | Spells | none seen apart from scrolls and potions; SAVE is "the Spell of Saving" in the fiction | - | - | - | `save_prompt` | shown |
| World and navigation | Auto-map | a map of nearby rooms beside the room window, current room filled, arrows for up/down, `?` for unknown; ZOOM widens it | `zoom` | - | [interface.md](interface.md) | `gameplay_hilltop`, `system_zoom_map`, `env_darkness` | shown |
| World and navigation | Random moors | the moors' room names, layout and monsters change with what was typed before | - | - | design/README | `battle_vapor_appears`, `gameplay_eyes`, `gameplay_gasses` | shown |
| World and navigation | Darkness | unlit places warn of a grue; moving on in the dark can kill | - | - | - | `env_darkness`, `gameover_grue` | shown |
| World and navigation | Travel | Miznia Jungle Skyway gondola; a unicorn in a stable | - | - | - | `gameplay_skyway`, `gameplay_stablehouse` | shown |
| Goals and gating | Coconut of Quendor | the prologue sets the quest | - | - | - | `cutscene_prologue` | shown |
| Goals and gating | Puzzles that open places | the Ledge riddle (SAY LIGHTNING) opens the way to the lighthouse; lightning bars the Fields of Frotzen; the cook wants a bottle of wine for the giant onion, and an unseen hand locks the cellar door behind you | - | - | - | `dialogue_riddle`, `system_lightning`, `dialogue_cook_wine`, `system_cellar_locked` | shown |
| Chance | Rolls | hits and misses, the random character, the moors and the scroll words are random; the run is deterministic per route | - | - | playbook "Emulation notes" | `menu_random_reroll`, `battle_vapor_attack` | shown |
| Failure and recovery | Death | Endurance 0 or a grue: "You are dead", then RESTORE, RESTART or QUIT (plus UNDO outside combat) | typed choice | - | - | `gameover_ratant`, `gameover_grue` | shown |
| Saving and sessions | SAVE / RESTORE | the Spell of Saving writes a named file (default DATA\BEYONDZO.SAV); RESTORE also at the opening prompt; not in combat (manual) | `save`, `restore` | - | - | `save_prompt`, `save_done`, `save_restore`, `menu_begin` | shown |
| Pacing and difficulty | Early danger | a Level 0 peasant dies to the rat-ant in the cellar within seven exchanges; the first vapor is beatable | - | - | - | `gameover_ratant`, `battle_vapor_won` | shown |

## 3. How the systems feed each other
- Fights -> experience -> level -> attributes; attributes decide fights.
- Found items -> sold for zorkmids -> armour bought -> armor class up -> fewer hits taken.
- Puzzles (riddle, the cook's wine) -> new places -> new items and monsters.
- Typed history -> layout of the moors and the scroll words -> each game differs.

## Options (system side)
| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Display | Palettes | COLOR cycles six palettes | `color` | 6 (verified) | [interface.md](interface.md) | `options_color_palette`, `options_color_4`, `options_color_5`, `options_color_6` | shown |
| Display | Settings | SETTINGS menu; NOTIFY, PRIORITY as commands | `settings`, `notify`, `priority` | - | [interface.md](interface.md) | `options_settings`, `options_notify`, `options_priority` | shown |

## Open questions
- Level thresholds: Level 1 at 9 experience; 37 experience was still Level 1 (RAM). What Level 2 needs.
- Potion effects: the gray potion showed no message; identification of potions not seen.
- How scrolls are used (USE SCROLL: "How do you intend to do it?"); their magic word is random.
- The cellar after the door locks (escape, the wine bottle), the lighthouse floors, the Fields of Frotzen.
