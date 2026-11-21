# The Bard's Tale III: Thief of Fate - content (variety lens)

What fills the game, as a sample across its range (shot ids of the `main` set unless marked `start`).
Full tables: dungeon levels in [maps/README.md](maps/README.md); city landmarks in `playbook.md`.

## Environments
Totals: 10 city/wilderness maps, 61 dungeon levels (2 disk sides) **(verified: loaded one by one)**.

| Kind | Sample | Look | Shots |
|---|---|---|---|
| Wilderness of Skara Brae | the refugee camp, trees, the Shrine | blue sky, orange ground, trees and tents | `env_wild_camp`, `env_wild_trees`, `gameplay_shrine` |
| Skara Brae ruins | city gates, statue of Tarjan, Review Board, temple | grey stone walls, ruins | `gameplay_skara_gates`, `gameplay_statue` |
| Arboria (city) | the old tower, the lake, a street | orange ground, tree houses | `gameplay_arboria_tower`, `gameplay_arboria_lake`, `arboria_env` |
| Ciera Brannia | street, Wizard's Guild, King's castle | white buildings, trees | `city_where`, `ciera_guild`, `ciera_court` |
| Gelidia | snowfield | white ground | `env_gelidia` |
| Lucencia, Celaria Bree | trees, street | | `env_lucencia`, `celaria` |
| Nowhere, Dark Copse (Tenebrosia) | empty plain, burned forest with a black door | | `nowhere`, `darkcopse` |
| Black Scar (Malefia) | street | | `env_black_scar` |
| Catacombs, UnterBrae (under Skara Brae) | green mossy walls | | `gameplay_catacombs`, `env_catacombs_lit`, `env_lv34` |
| Sacred Grove | green leaf walls | | `env_lv07` |
| Towers (Grey Tower) | wooden pillars | | `env_lv0c` |
| Ice Keep, Mountain, Alliria's Tomb | statues by red doors | | `env_lv16`, `env_lv18`, `env_lv1d` |
| Kinestia (Ferofist's Workshop, Urmech's Paradise, Viscous Plane) | blue stone | | `env_lv2e`, `env_lv31`, `env_lv32` |
| Tenebrosia (Shadow Canyon, Sceadu's Demense) | open sky over a canyon, dark walls | | `env_lv39`, `env_lv3a` |
| Tarmitia (Wasteland, Berlin, Troy, Nottingham) | blue brick, wars of Earth's history | | `env_lv1f`, `gameplay_berlin`, `env_lv21`, `env_lv24`, `env_lv26` |
| Malefia, Tarjan's realm | blue walls, wooden door; Tarjan's level | | `env_lv2a`, `gameplay_tarjan_end` |

## Opponents
| Opponent | Where | Notes | Shots |
|---|---|---|---|
| Puma | wilderness, by the tavern | single beast, takes 12+ damage | `battle_puma`, `battle_round` |
| Nefastmaster | catacombs, first corridor | hits a level-1 warrior for 16 | `encounter` (start) |
| Magic-eaters | the Tunnels | | `battle_magic_eaters` |
| Death Adder, Daemongari | UnterBrae level 4 | | `battle_death_adder` |
| Shade Piranhas, Lochliches, Flying Fish | the Palace (Arboria) | groups of 23 and 21 | `battle_palace` |
| Shade Cougars, Avians | Valarian's Tower | | `battle_cougars` |
| Ice Reaver | Ice Dungeon (Gelidia) | | `battle_ice_reaver` |
| Black Dragon | Tarjan's realm | breath fries for 100+ | `battle_dragon`, `battle_dragon_round` |
| Tarjan and his friends | Tarjan's realm | High Priestesses, 30 Black Slayers, 30 Rock Demons, Lorini | `tarjan_meet`, `tarjan_fight`, `tarjan_round` |

## Items and equipment
| Item | Where | Shots |
|---|---|---|
| Broadsword, Scale Armor, Buckler, Helm, Leather Gloves | starting gear of a fighter | `inv_ironpants` |
| Plate Armor, Halbard, Long Bows, Arrows, Wineskin, Lamps | storage building, free | `inventory_storage` |
| Ale, Beer, Mead, Foul spirits, Ginger Ale | Scrapwood tavern | `tavern_drinks` |

## Abilities
| Ability | Kind | Shots |
|---|---|---|
| MAFL Mage Flame | conjurer spell, light | `system_cast_light` |
| ARFI Arc Fire | conjurer attack spell (start set) | `cast_walk` |
| Six bard songs | Sir Robin's Tune ... Watchwood Melody | `bard_walk` |
| Spell levels for gold | Review Board | `spell_acq_yes` |

## People
| Person | Where | Shots |
|---|---|---|
| The last guild elder | Review Board | `dialogue_review_hint`, `talk_elder` |
| Priest of the Mad God | Skara Brae temple | `dialogue_temple` |
| Barkeep | Scrapwood tavern | `tavern_talk2`, `tavern_tip` |
| Monk of the credits house | Interplay building | `extra_interplay` |
| Hawkslayer | Arboria | `gameplay_hawkslayer` |
| The factory party *Interplayers and the previous owner's veteran party | camp, endgame save | `menu_party_ryz`, `hud_party`, `tarjan_2` |
