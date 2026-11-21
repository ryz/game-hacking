# The Bard's Tale III: Thief of Fate - interface (UI/UX lens)

Every screen, menu, prompt, message type and permanent element, as the player meets them. Shot ids are those
of the `main` set unless marked `start`. Systems behind them: [systems.md](systems.md); content: [content.md](content.md).

## Conventions
- **Input:** single keys, no cursor menus except the scrolling lists (roster, inventory, storage), where the
  arrow keys move a bar and Return picks. A menu entry is chosen by its first letter (Add, Remove, Create ...),
  a member by its number 1-7, a monster group by its letter A-D. Spells are typed as four-letter codes with
  Return. ESC aborts a prompt ("ESC to abort"), "Press any key..." ends a message page. Keys pressed while a
  page is still being written are lost **(verified)**.
- **Layout (one screen for everything):** top left the view window (first-person view, a building's keeper,
  a monster's picture), under it the location plate (Wilderness, Skara Brae, Review Board, the monster's name);
  top right the message window; a strip of effect icons under it; the bottom third is the party roster
  (number, name, AC, Hits, Cond(ition = current HP or Dead), SpPt). `hud_party`, `menu_camp`.
- **Text:** the game's own font on the hi-res screen, white message window, black text; inverse bar for the
  member whose turn it is (`battle_options`).
- **Feedback:** messages type out, combat text scrolls by itself, damage appears in the roster at once;
  saving gives no message (`saved`, start).
- **State visibility:** the effect icon strip (light, compass, levitation, shield, detection, song note) shows
  active spells and the bard's song (`tarjan_meet`, `env_catacombs_lit`); position and time only on request (`?`).
- **Help:** none on screen besides "ESC to abort" and "Press any key"; menus list their choices in full.

## Inventory of screens and elements

| Screen / element | Purpose | Shows | Accepts | Answers / leads to | Shots |
|---|---|---|---|---|---|
| Boot banner | ProDOS loading | APPLE II, PRODOS 8 V1.4 | none | title | `boot_prodos` |
| Title | attract | Bard's Tale III logo, the bard with his lute (flames flicker) | space | character disk prompt | `title_screen` |
| Disk prompts | swap disks | "Please insert your Character disk / Dungeon Disk Side A" | any key | the game reads the disk | `menu_chardisk`, `insert_side_a` (start) |
| Restore prompt | continue a save | "Do you wish to restore your last saved game? Yes No" | y n | the saved place / the camp | `menu_restore` |
| Camp of Skara Brae | party management | Add, Remove, Create, Rename, Delete, Save the party, Leave the game, Enter wilderness | letters | sub-prompts below | `menu_camp`, `menu_party_ryz` |
| Roster list | pick a member | scrolling list of the disk's characters and saved parties (*name) | arrows, Return, ESC | adds to the party | `menu_roster`, `roster_end` (start) |
| Creation prompts | make a character | male/female; race list; rolled statistics + class list; name line | m f, 1-7, 0-9, text | camp | `create_sex` (start), `menu_create_race`, `menu_create_class`, `menu_create_name` |
| Remove / delete / save party / leave | camp upkeep | "Select which party member to remove ... Remove them all!", "Delete who?" list, "Name to save party under?", "Press RETURN to end game play" | number, list, text, Return/ESC | camp | `camp_remove`, `camp_delete`, `camp_save_party`, `camp_leave` |
| Walking view | the world | first-person view with the location plate and a landmark message ("To the north is the refugee camp") | i j l k ? and command letters | moves, buildings, encounters | `env_wild_camp`, `gameplay_skara_gates`, `env_lv16`, `celaria`, seq-dungeon-walk (29 steps, dungeon) |
| Where am I (`?`) | orientation | "You're in Ciera Brannia and 14 paces south and 7 paces west of the city gates. It's now early morning." | any key | view | `system_whereami`, `city_where` |
| Automap (`?` in a dungeon) | dungeon map | a window of the level around the party (x), walls white, doors coloured, unvisited squares blank | ESC | view | `map_catacombs`, `unter_walk`, `map_mountain_seen`, `map_mountain_walk`, `map_mountain_full`, seq-automap (18 steps: the map growing over UnterBrae 2) |
| Character view | one member | "Ironpants is a Level 2 Male Dwarf Paladin", statistics, spell points, experience, gold, Pool gold, Trade gold; then the inventory list | 1-7, space, ESC | inventory | `inventory_view_char`, `view_morganna`, `inv_ironpants` |
| Item menu | one item | "Ironpants do you wish to: Unequip the item" (equip, trade, drop as applicable) | letters | inventory | `inv_item_menu` |
| Command prompts | outside combat | "Who will use an item?", "Who will play?", "Spell to cast:", "New Order: 1>", "(Pausing)", party options | number / code / ESC | the action | `use_item`, `bard_walk`, `cast_walk`, `order`, `pause`, `party_menu` |
| Save prompt | save | "Do you wish to save your game? Yes No" | y n | saved silently | `save_prompt` |
| Storage building | free gear | "Who wishes to inspect?" then "Pick up..." list | number, arrows, Return | "You pick up the item." | `inventory_storage` |
| Review Board | levels and spells | the elder; Advancement, Spell Acquiring, Class Change, Talk to the elder, Exit the guild; messages per member | letters, numbers | "still needeth 2000 experience", "hath earned a level ... +1 to intelligence", "Conjurer spell level 2 will cost 1000 in gold. Who will pay?" | `menu_review_board`, `dialogue_review_hint`, `adv_no`, `adv_yes`, `spell_acq`, `spell_acq_yes`, `class_change`, `class_change2`, `talk_elder` |
| Temple of the Mad God | quest gate | the priest: "Speak to priest? Yes No", then a typed word | y n, text | TARJAN opens the catacombs | `dialogue_temple`, `tarjan` (start) |
| Tavern (Scrapwood) | drinks, rumours | the barkeep: Order a drink, Talk to barkeep, Exit; drink list; "Talk ain't cheap ... How much will you tip him?" | letters, numbers, gold amount | rumour text | `gameplay_tavern`, `tavern_order`, `tavern_drinks`, `tavern_talk`, `tavern_talk2`, `tavern_tip` |
| Shrine | healing | the priest: Heal a character, Pool thy gold, Exit temple; price and payer prompts | h p e, numbers | "Sorry, but without proper sacrifice the prayer will fail." | `gameplay_shrine`, `shrine_pool`, `shrine_price` (start) |
| Credits house (Interplay) | credits | the monk's pages: design Michael A. Stackpole, programming Bill Heineman, music Kurt Heiden | any key | next page | `extra_interplay`, `credits1`, `credits3`, `credits4` |
| Encounter | a fight begins | monster picture, "You see N <name> (distance)", Fight bravely / Advance ahead / Run away | f a r | round orders | `battle_puma`, `battle_dragon`, `battle_palace`, `battle_cougars`, `battle_ice_reaver`, `battle_death_adder`, `tarjan_fight` |
| Round orders | per member | "<name> has these options this battle round: Attack foes, Defend, Party attack, Cast a spell, Use an item, Bard Song", group list A-D | letters | next member; "Use these commands? Yes No" | `battle_options`, `battle_magic_eaters`, `tarjan_target` |
| Round report | outcome | scrolling lines of hits, misses, damage, breath, repelled attacks; "You still face ..." | none | next round | `battle_round`, `battle_dragon_round`, `tarjan_round` |
| Boss speech | story | Tarjan's portrait and pages of speech | any key | the fight | `tarjan_meet`, `tarjan_2`, `tarjan_3`, `tarjan_4` |
| Landmark messages | world text | building names, inscriptions, events ("An explosion!", "The ground seems well worn here.") | none / any key | | `gameplay_statue`, `gameplay_hawkslayer`, `darkcopse`, `env_lv31`, `env_lv21`, `env_lv26`, `gameplay_tarjan_end` |

## Screen flow
Power-on -> title -> character disk -> restore? (Yes: the saved place; No: camp) -> camp (create, add) ->
Enter wilderness -> walking view <-> buildings (each its own menu, Exit returns to the view) / gates (city,
dungeon, with disk prompts) -> encounter -> round orders -> report -> walking view; `s` saves at any time.

## Observations
- **Observation:** one screen layout carries the whole game; a player always sees the party's HP and SP.
- **Observation:** entering a building needs `k`/Return while `i` only bumps; nothing on screen tells this.
- **Observation:** saving gives no confirmation at all (`saved`, start).
