# Beyond Zork: The Coconut of Quendor (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Which kinds exist depends on the game, its genre and structure: keep the kinds this game has, drop the rest,
add its own (vehicles, tracks, puzzles, levels, minigames ...). For each kind say how many there are in total
if known, then show a sample that spans the range: early and late, common and rare, plain and strange, one of
each visual family. A complete table belongs in its own document (items.md, enemies.md) and is linked here.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | village, moors (random), cellar, lighthouse, seaport, city, more beyond (unknown total) | 13 looks | none: no walkthrough reachable |
| Opponents | unknown total | 4 (eldritch vapor, guttersnipe, rat-ant, pterodactyl) | - |
| Items | potions, scrolls, weapons, armour, money | 8 | - |
| Equipment | weapons and armour | shillelagh, dagger, cloak; tunic, scale and plate mail on sale | - |
| Abilities / spells | scrolls and potions carry the magic | 2 scrolls, 1 potion | - |
| Characters and people | sailor, cook, bandits, old woman, hawker, unicorn, conductor | 7 | - |
| Player characters | preset Frank Booth, six presets, random, created | 9 ways shown | - |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Hilltop and the village street | start | the sea, shanties, gulls | `gameplay_hilltop`, `env_cove_street` |
| Wharf | village | the sailor painting, the driftwood | `gameplay_wharf_sailor` |
| Pub and kitchen | village | bandits by the fire, cook and giant onion | `env_outside_pub`, `env_rusty_lantern`, `dialogue_kitchen_cook` |
| Wine Cellar and Darkness | under the kitchen | refuse, a rat-ant, then a grue's darkness | `battle_ratant`, `env_darkness` |
| Edge of Storms | north-west of the hilltop | gray fields, a billboard, lightning | `env_edge_of_storms`, `system_lightning` |
| Ledge and lighthouse | north-east of the Cove | a riddle on the cliff, a ruined lighthouse | `dialogue_riddle`, `env_lighthouse`, `gameplay_lighthouse_1st` |
| Moors | south of the pub | rooms named by the senses (Noises, Odors, Eyes, Gasses, Deep Mist, Mud Flats), random | `battle_vapor_appears`, `gameplay_eyes`, `gameplay_gasses`, `gameplay_mud_flats` |
| Bluffs | south-west of the moors | a view of the seaport | `env_bluffs` |
| Mizniaport | the seaport | boutique, Private Way, stablehouse, Skyway | `env_mizniaport`, `env_private_way`, `gameplay_stablehouse`, `gameplay_skyway` |
| Fields and Gurth City | north of Mizniaport | gray fields, Southern Mithicus peaks, a market | `env_intersection`, `gameplay_south_market` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Eldritch vapor | moors (Noises) | spirit of the mist (no pictures: text only) | tickles, tries to snatch your weapon; vanishes in a spectral flash | `battle_vapor_appears`, `battle_vapor_attack`, `battle_vapor_won` |
| Guttersnipe | moors (Deep Mist, Odors) | bird with a sharp beak | pecks; battered, it retreats into the fog | `battle_guttersnipe`, `battle_guttersnipe_strong`, `battle_guttersnipe_won`, `battle_guttersnipe_odors` |
| Rat-ant | Wine Cellar | vermin | sharp teeth; strong enough to kill a Level 0 peasant | `battle_ratant`, `gameover_ratant`, `battle_ratant_flees` |
| Pterodactyl | Mud Flats | wounded, an arrow in its wing, a whistle on a chain | snaps, hobbles away when you reach for the arrow (not a fight) | `gameplay_mud_flats`, `gameplay_pterodactyl` |
| Grue | Darkness | never seen | kills those who move on in the dark | `gameover_grue` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Driftwood / shillelagh | weapon | Wharf (wait, then take) | the first weapon | `system_driftwood` |
| Rusty dagger | weapon | thrown into the kitchen wall by a bandit | - | `dialogue_kitchen_cook` |
| Cloak | armour | Boutique, 30 zorkmids | armor class up | `shop_buy`, `inventory_cloak_worn` |
| Leather tunic, scale mail, plate mail | armour | Boutique | on sale, prices not asked | `shop_display_case` |
| Gray potion | potion | Odors, in the mud | Frobozz Magic Potion Company, "Shake before using"; drunk, no visible effect | `inventory_potion_examine`, `system_potion_drink` |
| Crinkly scroll (Blarn / Watkin) | scroll | Wine Cellar | "something to do with refreshment" | `inventory_scroll_blarn` |
| Rumpled scroll (Macuga) | scroll | Gasses | "something to do with weaponry"; sells for 5 zorkmids | `inventory_scroll_macuga`, `shop_sell` |
| Fish cake, horseshoe, saddle, whistle, stave | items seen | Market, stablehouse, Mud Flats | not taken | `gameplay_south_market`, `gameplay_stablehouse`, `gameplay_mud_flats` |
| Zorkmids | money | start (1), selling | buy | `inventory_list`, `shop_sell` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Spell of Saving | the player | none | SAVE, in the game's fiction | `save_prompt` |
| Scroll magic | the reader | the scroll | words of power; use not found (see systems.md) | `inventory_scroll_macuga` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Frank Booth | default preset (Level 0 Male Peasant) | start | `inventory_status` |
| Ryz | created character (Level 0 Female Peasant) | Create your own | `menu_create_done`, `inventory_ryz_status` |
| Presets Lucky, Tank, Muscles, Nimble, Genius, Saint | preset characters | Character Setup | `menu_select_preset` |
| Y'Gael | the old woman of the prologue | prologue | `cutscene_prologue` |
| Old sailor | painter of a galleon, names the shillelagh | Wharf | `dialogue_sailor` |
| Skinny old cook | wants a bottle of wine for the onion | Kitchen | `dialogue_cook_busy`, `dialogue_cook_wine` |
| Bandits | refuse a fight, throw a dagger | Rusty Lantern | `env_rusty_lantern` |
| Old woman | shopkeeper | Boutique | `shop_boutique`, `dialogue_woman` |
| Unicorn | "just a pony", in a closed stall | Stablehouse | `dialogue_unicorn` |
| Street hawker | bumps into you, drops wares | South Market | `gameplay_south_market` |
| Nymphs | helpers who explain the interface | anywhere | `extra_technical_nymph` |
| Skyway conductor | announces the gondola | Skyway Entrance | `gameplay_skyway` |

## Open questions
What exists but was not seen: the regions past Gurth City and the Skyway, the lighthouse above the first level,
the Fields of Frotzen past the lightning, the cellar beyond the darkness, monsters at higher levels.
