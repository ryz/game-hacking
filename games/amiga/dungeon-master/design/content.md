# Dungeon Master - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py amiga/dungeon-master`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 14 levels, one stone wall set throughout, set apart by ornaments, doors, stairs, pits, fountains and light (RAM, verified) | the hall, levels 2-6, 8, 10, 12-14 | [maps.md](maps.md) |
| Opponents | 27 creature kinds (ROM text); 24 placed in the dungeon (RAM) | 22 kinds | section 3, [maps.md](maps.md) |
| Items | about 180 item names on the disk: weapons, armour, food, keys, potions, scrolls, magical objects (ROM text) | torch, apple, keys, Screamer slice, potion, club, axe, Firestaff | section 4 |
| Abilities / spells | rune spells and object actions (ROM text: FIREBALL, LIGHTNING, HEAL, FLUXCAGE, SPELLSHIELD ...) | ON FUL, LO VI, THROW, BASH, FUSE | section 5 |
| Characters and people | 24 champions in the hall (source: manual), 23 found; the Grey Lord, Lord Chaos and Lord Order of the story | 9 champions, the three lords | section 6 |

## 2. Environments
One row per distinct look or place type.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Entrance | outside | carved doors in a stone arch overgrown with ivy (verified) | `title_entrance`, `cutscene_doors_open` |
| Hall of Champions | level 1 | lit corridors, mirrors with portraits, the inscription, an iron gate, the entrance doors from inside (verified) | `hall_start`, `hall_inscription`, `hall_mirror`, `hall_gate_closed`, `hall_gate_open`, `hall_entrance_inside` |
| Behind the hall | level 1 | shackles, an apple, a torch in a sconce, the first stairs (verified) | `env_hall_shackles`, `system_torch_sconce`, `gameplay_stairs_down` |
| Dark corridors | level 2 without light | outlines only (verified) | `env_l2_dark` |
| Upper dungeon | levels 2-6 | wooden doors with buttons and windows, iron gates, keyholes, pits, shackles, a lion-head fountain, small wall ornaments (verified) | `env_l2_corridor`, `env_l2_junction`, `gameplay_l2_door_button`, `gameplay_door_closed`, `gameplay_door_window`, `gameplay_lock_key`, `gameplay_pit`, `gameplay_stairs_up`, `gameplay_fountain`, `env_l3_corridor`, `env_l4_corridor`, `env_l5_shackles`, `env_l6_corridor` |
| Lower dungeon | levels 8-14 | wide open areas, long corridors fading into the dark (verified) | `env_l8_corridor`, `env_l10_corridor`, `env_l12_corridor`, `env_l14_corridor` |
| Chaos's lair | level 13 | Lord Chaos and Demons among fluxcage-sized corridors (RAM, verified) | `boss_lord_chaos`, `battle_demon` |
| The dragon's level | level 14 | the deepest level, the Red Dragon (verified) | `boss_red_dragon` |

## 3. Opponents
A spread over families, strengths and behaviours (all verified on screen; levels from RAM).

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Screamer | level 2 (also 4, 5) | a fungus on roots, groups of four | stands still; drops slices of food when killed | `battle_screamers`, `battle_hit`, `system_pick_up` |
| Mummy | level 2 (also 3, 8) | bandaged walker | slow; came up to the party when its gate opened (start set) | `battle_mummies` |
| Trolin | levels 3 and 11 | blue club-bearer | hit RYZ for 28 | `battle_trolin`, `battle_trolins` |
| Rockpile | levels 3 and 4 | heap of stones | - | `battle_rockpiles` |
| Giant Wasp | levels 4 and 11 | flying insect | - | `battle_giant_wasp`, `battle_giant_wasps` |
| Magenta Worm | level 4 | purple worm with a round mouth | - | `battle_magenta_worms` |
| Ghost | levels 4 and 8 | green outline | nearly invisible | `battle_ghost` |
| Couatl | level 5 | winged serpent | - | `battle_couatl` |
| Wizard Eye | levels 6 and 10 | floating eyes on stalks | - | `battle_wizard_eye` |
| Stone Golem | level 7 | grey giant | blocks a doorway | `battle_stone_golem` |
| Skeleton | levels 6, 8, 10 | sword and shield | - | `battle_skeletons` |
| Vexirk | level 9 | small robed caster | casts fireballs (71/86/74/63 damage) | `battle_fireball` |
| Pain Rat | level 9 | brown giant rat | - | `battle_pain_rat` |
| Ruster | level 9 | small beast | eats metal (source: manual) | `battle_ruster` |
| Giggler | levels 8, 10, 11 | small blue thief | steals (source: manual) | `battle_giggler` |
| Water Elemental | level 11 | a pool on the floor | - | `battle_water_elemental` |
| Animated Armour | level 12 | empty suit of armour with a sword | - | `battle_animated_armour` |
| Oitu | level 12 | long-legged spider | - | `battle_oitu` |
| Materializer | level 12 | a whirl of flame | - | `battle_materializer` |
| Demon | level 13 | red demon | throws fireballs | `battle_demon` |
| Lord Chaos (boss) | level 13 | robed dark figure | moves even when walled in; must be trapped and fused | `boss_lord_chaos`, `boss_chaos_fused` |
| Red Dragon (boss) | level 14 | huge red dragon | - | `boss_red_dragon` |
| Swamp Slime, Giant Scorpion, Black Flame | levels 5, 10 | - | not captured (out of sight at the warp points) | none: not met at the warp points |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Torch | light (weapon slot) | sconce behind the hall gate (verified) | lights the view while held | `system_torch_sconce`, `system_torch_taken` |
| Apple | food | floor behind the gate (verified) | eaten at the mouth (source: manual) | `env_hall_shackles` |
| Gold key | key | floor of level 2 (verified) | opens the gate lock at (0,3) | `gameplay_lock_key`, `system_key_taken`, `system_key_used` |
| Screamer slice | food | a killed Screamer (verified) | eaten: food bar up | `system_pick_up`, `inventory_feed`, `system_eat` |
| Healing potion (VI) | potion | made by Wuuf from an empty flask (verified) | heals (source: manual) | `system_potion`, `inventory_potion` |
| Club, axe, wand | weapons | carried by RYZ (Halk), Stamm, Tiggy (verified) | each with its own actions | `system_action_menu`, `inventory_examine`, `system_throw` |
| The Firestaff (complete) | quest weapon | levels below (source: Wikipedia; in the shots set by a RAM change of the club) | INVOKE, FUSE, FLUXCAGE; FUSE ends the game | `boss_chaos_fused` |
| Champions' gear | armour and odds | the mirrors (verified): Halk's helmet and hide, Wu Tse's throwing stars, Chani's moonstone, Gothmog's wand | - | `system_champion_panel`, `hall_champion_ninja`, `hall_champion_priestess`, `hall_champion_gothmog` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| ON FUL (magic torch) | Tiggy | mana (bar drops, verified) | lights a dark level (verified) | `system_magic_light`, `system_runes` |
| ON FUL IR (fireball) | Tiggy | mana | a ball of flame down the corridor (verified) | `system_spell_fireball`, `battle_spell_cast` |
| LO VI (healing potion) | Wuuf, with an empty flask in hand | 3 mana (30 -> 27, verified) | fills the flask with a potion | `system_potion`, `inventory_potion` |
| BASH, THROW | RYZ with a club | stamina (source: manual) | melee blow 17-21 damage; throws the club | `battle_hit`, `system_throw` |
| PUNCH, KICK, WAR CRY | empty hand | - | unarmed actions | `system_action_wuuf` |
| FUSE | the Firestaff | - | fuses Lord Chaos when he cannot move | `boss_chaos_fused` |
| Fireball (creature) | Vexirk, Demon | - | burst over the party | `battle_fireball`, `battle_demon` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| ryz (Halk the Barbarian, reincarnated) | fighter, leader | mirror (7,9) | `system_reincarnated`, `ending_champions` |
| Tiggy Tamal | wizard (36 mana, the most in the hall) | mirror (9,13) | `hall_champion_wizard`, `system_resurrected` |
| Wuuf the Bika | ninja and priest with a flask | mirror (12,13) | `inventory_potion`, `system_action_wuuf` |
| Stamm Bladecaster | fighter with an axe | mirror (11,15) | `system_party_four` |
| Hissssa Lizar of Makan | lizard champion (not taken) | mirror (16,14) | `hall_champion_lizard` |
| Wu Tse Son of Heaven | ninja (not taken) | mirror (7,13) | `hall_champion_ninja` |
| Chani Sayyadina Sihaya | priestess (not taken) | mirror (14,3) | `hall_champion_priestess` |
| Gothmog | hooded wizard (not taken) | mirror (16,17) | `hall_champion_gothmog` |
| Lord Order and the Grey Lord | the two halves and the whole of the player's master | the ending | `ending_lord_order`, `ending_fusion`, `ending_grey_lord`, `ending_truth`, `ending_harmony`, `ending_names` |

## Open questions
- Items deeper down (armour sets, magical objects, scrolls, chests) were not picked up in this run.
- Swamp Slime, Giant Scorpion, Black Flame and the Red Dragon's behaviour in a fight were not seen.
