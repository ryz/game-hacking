# SWORD OF VERMILION - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. The rules behind the content are in [systems.md](systems.md), the screens it appears on in
[interface.md](interface.md); the same shots appear there, overlap is intended. Notation: [README.md](README.md).
Check: `python3 tools/lenses.py md/sword-of-vermilion`. Shots: set `main` unless marked (start).

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 14 towns, overworld maps, caves **(ROM text: town table)** | 2 towns, 5 overworld views, 2 caves | [../playbook.md](../playbook.md) Game structure |
| Opponents | not counted | green slimes, blue slimes, goblins | - |
| Items | 44 named items **(ROM text, decoded table)** | Herbs, Candle, Lantern | playbook RAM map (item ids) |
| Equipment | 20 swords, 20 shields, 17 armours incl. cursed and duplicates **(ROM text)** | Bronze Sword; shop list of 2 shields and 2 armours | - |
| Abilities / spells | 23 spells **(ROM text)** | Aero, Volti, Aries, Ferros, Sangua | - |
| Characters and people | - | Blade, the woman in his house, keepers, priest, Parma soldiers | - |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Wyclif village | start | wooden houses, fences, forest, stream | `start_wyclif_gate`, `env_wyclif_blade_house`, `gameplay_tavern` |
| Parma town | two maps north of Wyclif | cobbled streets, stone church with a spire, fountain, soldiers | `env_parma_gate`, `env_parma_church`, `env_parma_street`, `env_parma_fountain`, `gameplay_parma_inn`, `gameplay_magic_shop` |
| Interiors | both towns | brown wood (Wyclif) and grey stone walls (Parma inn) | `shop_weapon`, `save_church_menu`, `gameplay_parma_inn` |
| Overworld forest road | around Wyclif | dense pines, dirt road | `env_overworld_road`, `env_overworld_trees` |
| Overworld meadow | west of the cave turn-off | open grass, scattered pines, mountains | `env_overworld_meadow`, `env_overworld_north` |
| Overworld hills | south of Parma | the road between hills | `env_overworld_hills`, `env_overworld_parma` |
| Cave (stone) | south of Wyclif; east of Parma | rounded stone pillars, ladder, barred doors | `gameplay_cave_lit`, `gameplay_cave_door`, `env_cave_corridor`, `gameplay_cave_entrance` |
| Battle field (forest) | every battle so far | tree trunks at the top, grass | `battle_first`, `battle_goblins` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Green slime | road south of Wyclif | slime, packs of 6-8 | hops at the prince, about 3 HP per touch at level 1 **(verified)** | `gameplay_encounter_slime`, `battle_first`, `battle_magic` |
| Blue slime | south of Wyclif | slime | same behaviour, packs of 4-6 **(verified)** | `gameplay_encounter_blue`, `battle_blue_slimes` |
| Goblin | road to Parma | armed beast-man with a sword, packs of 6 | walks in and strikes **(verified)** | `gameplay_encounter_goblin`, `battle_goblins` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Bronze Sword | weapon | Wyclif weapon shop, 100 | STR 4 -> 32 when readied **(verified)** | `shop_weapon`, `inventory_readied` |
| Leather/Small Shield, Leather/Bronze Armor | shield, armour | Wyclif shop, 50-400 | not bought | `shop_weapon` |
| Lantern | light | (poked) | lights a whole cave **(verified)** | `system_lantern`, `gameplay_cave_lit` |
| Candle | light | chest in the cave south of Wyclif | lights part of a cave **(ROM text)** | `system_open_chest`, `system_take` |
| Herbs | healing | (poked) | not used | `inventory_items` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Ferros | prince, book from Parma (500) | 1 MP | combat spell fired with A **(verified)** | `shop_magic_list`, `system_magic_readied`, `battle_magic` |
| Sangua | prince, Parma (800) | ? | field spell (not combat-ready); healing by name, not tested | `shop_magic_list` |
| Aries | prince (poked) | ? | lists visited towns to return to **(verified)** | `system_aries_towns` |
| Aero, Volti | prince (poked) | ? | listed, not cast | `menu_magic_cast` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Blade | foster father, dies in the opening | Wyclif | `cutscene_blade_deathbed`, `11_blade_father` (start), `13_blade_farewell` (start) |
| Woman in Blade's house | sends the prince upstairs | Wyclif | `dialogue_blade_house` |
| Shopkeepers | weapons, books | Wyclif, Parma | `shop_buy_confirm`, `shop_magic_greeting` |
| Innkeeper | 13-kim nights | Parma | `shop_inn_offer` |
| Priest | save, cures, revival | Wyclif church | `save_church_menu` |
| Soldiers in blue | patrol the street | Parma | `env_parma_gate` |
| King Tsarkon, King Erik V | prologue | - | `cutscene_prologue_tsarkon` |

## Open questions
What exists but was not seen: bosses, rings, later towns (Watling and beyond), most equipment and spells. A
route east of Parma reaches the next cave (`m_cave2_lit`); poked money (FFC620) buys later gear.
