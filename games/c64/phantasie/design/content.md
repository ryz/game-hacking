# Phantasie - content (variety lens)

What the game is filled with, as a sample. Rules: [systems.md](systems.md); screens: [interface.md](interface.md).
Notation: [README.md](README.md). Shot ids: `main` set.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | wilderness of 16 sections, 11 towns, 10 dungeons (source; DNG 1-10 files on disk 2) | 1 wilderness section, 2 towns, 1 dungeon | - |
| Opponents | 80 monster files MX 1-80 on each disk (verified: directory) | bantir, giant ant, giant bee | - |
| Items | weapons, armour, shields, potions, scrolls, treasure (verified: file names) | club, robes, small shield, scroll 8 | - |
| Abilities / spells | numbered spells (source) | spell 5, spell 9 | - |
| Characters and people | 5 races + random creature, 6 classes (verified) | the party of six, the old Pineville party | - |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Town (Pelnor) | town 1 | six buildings, gate | `env_town_pelnor`, `town_pelnor_party` |
| Town (Pineville) | town 2 | same layout, other name | `town_pineville_old` |
| Wilderness: paths, grass, forest, lake, hills | Pelnor's section | sea all around, hills with a door | `env_world_pelnor`, `env_world_west`, `world_hillside_door` |
| Independent inn | west of Pelnor | "The Red Pony Inn" | `world_red_pony`, `world_inn_prompt` |
| Dungeon | north of Pelnor | passages with torches, guard room, hall with columns, crumbling hallway, doors | `env_dungeon_passage`, `env_dungeon_guardroom`, `env_dungeon_hall`, `env_dungeon_hallway`, `dungeon_exit_prompt` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Bantir | wilderness east of Pelnor, group of 3 | green spiky creature | melee, missed every time in round 1 | `battle_bantirs`, `battle_spell_damage` |
| Giant ant | dungeon 1, ranks 1 and 3 | purple insect | bites for 1-2 damage | `battle_ants`, `battle_member_hurt`, `battle_ant_dies` |
| Giant bee | dungeon 1, rank 2 | brown insect | stings | `battle_bee_hits`, `battle_bee_dies` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Club, robes, small shield | starting weapon, armour, shield | new character | points 4, 2, 4 | `char_sheet_ryz` |
| Small shield | shield | Pelnor armory, 2 gp | points 4 | `armory` |
| Scroll 8 | story scroll | Pelnor armory, 121 gp | story text (source) | `armory_buy` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Spell 5 | wizard (cubi at level 1) | 1 magic (RAM) | fire on one monster, any rank: 5 damage | `battle_cast`, `battle_fire_rank3` |
| Spell 9 | wizard, learned at the Guild | 10 gp per try | not tried in combat | `guild_spell_learned` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| ryz, condi, ebo, cubi, deddo, mnz | the party: human fighter, dwarf fighter, human priest, elf wizard, halfling thief, human monk | Pelnor | `guild_party`, `char_sheet_ryz`, `guild_inspect_cubi` |
| grunt, hit, scott, borack (robert dead) | a previous owner's party on the dump | Pineville | `guild_roster`, `town_pineville_old` |
| The Mystic | rates the party | every town | `mystic` |

## Open questions
- Other towns, sections, dungeons 2-10, the Black Knights and Nikademus not reached.
