# Dragonflight - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.
Shot ids are the `main` set (`../shots/main/index.md`); the `start` set shows the same early game in play order.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
The party of four walks the land and the towns square by square (top-down), talks to people for leads, buys
and finds equipment, and fights the groups that ambush it on the land in turn-based grid combat
**(verified)**. Fights give experience and gold; dead heroes are carried back to a temple by their Ring of
Stasis **(RAM: game text)**. Parts of the Great Map, scrolls with spells and keys open the way to new towns and
first-person dungeons **(RAM: game text)**. Between outings the party camps, eats and saves on Disk B
**(verified)**.

## 2. Systems

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Move | One square per keypad press or arrow click; walls answer "Blocked" **(verified)** | keypad 8 2 6 4, arrow panel | about 1 step per 1.3 s of input **(verified)** | playbook Controls | `env_land_forest`, `system_arrows`, `hud_land` | shown |
| Player verbs | Look (eye) | Names what is in front: a house's owner ("It's Housens."), on the land "You found nothing" **(verified)** | eye icon | - | - | `13_look_house` (start set) | shown |
| Player verbs | Use / open (hand) | Tries the door in front: "Nobody at home.", "You enter.", "The door is locked!" **(verified first; RAM the rest)** | hand icon | - | - | `gameplay_door_nobody` | shown |
| Player verbs | Speak | The person next to the party, in the facing direction, answers in a full text window; the party can show or deliver an item **(verified)** | lips icon next to a person | - | - | `dialogue_redhair`, `dialogue_show` | shown |
| Player verbs | Camp | On the land only ("Not here!" in town): a campfire scene, the party rests ("zzz...") **(verified)** | campfire icon | - | - | `system_camp` | shown |
| Player verbs | Search (land) | Finds hidden dungeon entrances ("You discover a well hidden entrance to a dungeon!") **(RAM: text)**; near Pegana "You found nothing" **(verified)** | eye icon on the land | - | - | none: nothing found near Pegana | described |
| Player verbs | Enter | Enters the town or place the party stands on **(verified for Pegana)**; the cave arch east of Pegana did not open **(verified)** | enter icon | town load about 1200 frames | - | `env_pegana_road` | shown |
| Player verbs | Ship | "There is no ship!" away from one; ships carry the party over sea, crews mutiny when supplies run out **(RAM: text)** | ship icon | - | - | none: no ship reached | described |
| Player verbs | Land sword icon | Clicked on the land: nothing visible ("Loading...") **(verified)** | - | - | - | none | open |
| Player verbs | Wait | A turn passes by itself about every 800 frames ("Pass") **(verified)** | nothing | 800 frames | - | `hud_land` | shown |
| Characters and progression | Four fixed heroes | Bladus (fighter, 100 HP, 5 magic), Rinakles (wizard, 50 HP, 10 magic), Dobranur (dwarf, 120 HP, no magic), Andariel (elf, 60 HP, 8 magic) at the start **(verified)** | none: no creation | values on the status screens | [content.md](content.md) | `inventory_status`, `inventory_status_dobranur` | shown |
| Characters and progression | Experience and character points | Kills give experience; fleeing a fight costs character points **(RAM: text "fled from the battle, losing N characterpoints")** | - | start: experience 0, character 50 **(verified)** | - | `inventory_status` | described |
| Resources and economy | Gold and food | Each hero carries own gold and food (100 each at the start) **(verified)**; "Hunger!" when food runs out **(RAM: text)** | - | 100 / 100 | - | `inventory_items` | shown |
| Resources and economy | Shops | Drugstore, Grocery, Blacksmith, Healer, Shipping company, University, Palace; "bought from", "doesn't have enough money!" **(RAM: text)** | - | - | - | none: no shop door found in the budget | described |
| Conflict | Encounters | Groups ambush the party on the land at random ("Your opponents' attack surprises you. They are Snakes! They have no weapons!"); none in 150 steps near Pegana, one after 162 steps of a random walk further south-east **(verified)** | none | - | playbook Shot plan | `battle_encounter`, `battle_msg_orcs` | shown |
| Conflict | Orders phase | Each hero in turn gets one order (move by arrow: "Forward"; Attack; Shoot arrow; Cast spell; Parry; Throw; Change weapon), then all orders are carried out at once **(verified for move, attack, parry)** | arrow panel / icon panel | 1 move per round at the start **(verified "Move(1)")** | - | `battle_start`, `battle_arrows`, `battle_orders`, `battle_orders` | shown |
| Conflict | Melee and ranged | The sword icon (Attack) appears only next to an enemy; far away it is a shooting hand that needs a bow ("Has no longrange weapon!") **(verified)**; no weapon at all: "No weapon for close combat." **(RAM: text)** | sword / bow icon | Bladus with a sword hit a snake for 27 **(verified)** | - | none (seen live: "Has no longrange weapon!"), `battle_hit` | shown |
| Conflict | Death and the Ring of Stasis | A hero at 0 hit points is "mortually wounded"; a living hero takes his Ring of Stasis, and a temple revives the bearer **(verified first half; RAM: temple text)** | - | - | - | `battle_wounded`, `battle_statue`, `gameover` | shown |
| Conflict | Fleeing | A hero can flee; killing a fleeing monster costs character points **(RAM: text)** | - | - | - | none | described |
| Opponents | Monster kinds | 15 kinds named in the game text, 13 poked into an encounter and seen with their own picture: Orc, Skeleton, Ghost, Bear, Snake, Beast, Ghoul, Gnoll, Troll, Balron, Energyball, Statue, Guardian **(verified)**; count and kind are combat RAM 13B58/13B5A **(RAM)** | - | 1-4 per group (positions fixed by count) **(RAM: code at 1316E)** | [content.md](content.md) | `battle_orcs`, `battle_skeleton`, `battle_ghost`, `battle_bear`, `battle_beast`, `battle_ghoul`, `battle_gnoll`, `battle_troll`, `battle_balron`, `battle_energyball`, `battle_statue` | shown |
| Items and equipment | Inventory | Each hero has a list of items with counts; Examine, Use, Prepare (oils, potions) and drop icons **(verified)**; a weapon shows on the status screen **(verified)** | inventory icons, item picture | - | [interface.md](interface.md) | `inventory_items`, `inventory_examine`, `inventory_weapon` | shown |
| Items and equipment | The Great Map | Parts of the world map are items; Use adds a part to the "Worldmap" item ("You added the piece of map to the world-map!") **(verified)**; the Worldmap itself cannot be used from the inventory ("Can't use this item!") **(verified)** | Use icon | 12 parts (intro) | - | `inventory_map_piece`, `map_worldmap_added` | shown |
| Abilities and magic | Spells | Three schools: white (w), black (b) and a third (c) of nature spells; 33 names, scroll N teaches spell N of the list (Light 0, Dispell undead 1, Magic arrow 2, Dazzle 3 ...) **(verified for 3)**. Use a scroll -> "Who should read this scroll?" -> hero -> "learned this spell", the scroll is used up **(verified)**; a learned spell must be prepared on the Spells page ("Spell ready", check mark) before the pentagram casts it; a cast can fail ("Spell has failed!") **(verified)** | Use icon, Prepare icon, magic icon | Rinakles 10 magic at the start | [content.md](content.md) | `inventory_spells`, `system_cast_no_spell`, `inventory_scroll`, `magic_read_scroll`, `magic_learned`, `magic_spells_known`, `magic_prepared`, `magic_cast_failed` | shown |
| Abilities and magic | Potions | Ten potions plus mixtures ("Own potion mixed"), weapon oils +1 to +5 prepared on a weapon **(RAM: text)** | Prepare icon | - | - | none | described |
| World and navigation | Land and towns | One land map with towns as icons; towns are walled top-down maps left by stepping off the edge ("Leave this place?") **(verified)** | - | Pegana 117 x 117 squares **(RAM)** | playbook | `env_land_river`, `env_land_bridge`, `env_pegana_square`, `env_pegana_road` | shown |
| World and navigation | Dungeons | First person, with doors, chests, traps, secret panels **(RAM: text)** | - | - | - | none: no entrance opened | described |
| Goals and gating | Main quest | Find the 12 parts of the Great Map, Benglur in Brindil-Bun next; free the dragons **(verified intro; RAM ending text)** | - | - | - | `cutscene_sage` | shown |
| Chance | Random encounters, hits | Ambushes and hit damage are random: Bladus with a sword hit a snake for 27, 24, 21 in three rounds; a snake hit Bladus for 41 **(verified)** | - | - | - | `battle_hit` | shown |
| Failure and recovery | Death | See Ring of Stasis; when the last hero falls: a blue screen "Is this the end of all hope?" with the four faces, then "Insert disk A please" (restart) **(verified)** | - | - | - | `battle_wounded`, `gameover` | shown |
| Saving and sessions | One saved game | Disk icon on the land: save ("Gamesave?") or load ("Gameload?"); Old game on the Main Menu **(verified)** | disk menu, yes = left button | save about 1500 frames | - | `save_prompt`, `save_done`, `save_load_prompt`, `menu_oldgame` | shown |
| Pacing and difficulty | Start | The party starts unarmed (only a torch each) and must buy weapons before fighting **(verified)** | - | - | - | `inventory_items`, none (seen live: "Has no longrange weapon!") | shown |

## 3. How the systems feed each other
- Fights give experience and gold -> gold buys weapons, armour, food and potions in town shops -> weapons win
  fights **(RAM: text; inferred loop)**.
- People in towns name places and people -> places hold map parts, scrolls and keys -> map parts complete the
  Great Map -> new destinations, ship travel and dungeons **(inferred)**.
- Death -> the Ring of Stasis is carried by another hero -> a temple revives **(RAM: text)**.

## Open questions
- Where the shops of Pegana are (the doors tried said "Nobody at home."), and how prices run.
- What the land's sword icon does; how the Worldmap is viewed.
- Encounter rate: none in about 150 steps near Pegana, one in 162 steps further south-east: by region?
- Game over: shown with a Guardian group. A won fight is still open: no monster hit-point value was found in RAM (a snake took 27+24+21+... and stayed).
