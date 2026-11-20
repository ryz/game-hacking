# Dungeon Master - content (variety lens)

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
| Environments | 14 levels (source); grey stone walls with ornaments (mirrors, sconces, shackles, rings, grates, inscriptions) | hall, level 2 | - |
| Opponents | 27 creature names on the disk (ROM text) | - | section 3 |
| Items | about 180 item names on the disk: weapons, armour, food, keys, potions, scrolls, magical objects (ROM text) | torch, apple | section 4 |
| Equipment | armour sets from robes to Lyte/Darc plate (ROM text) | - | section 4 |
| Abilities / spells | rune spells; action names such as FIREBALL, LIGHTNING, HEAL, FLUXCAGE, SPELLSHIELD (ROM text) | LO FUL | section 5 |
| Characters and people | 24 champions (manual); 23 found with their stats | 4 in the party | playbook Hall map |

## 2. Environments
One row per distinct look or place type (tile or wall set, terrain, interior, special place), not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Hall of Champions | level 1 | lit corridors, 24 mirrors, inscription, iron gate (verified) | hall_start, hall_inscription |
| Dungeon corridors | level 2 | dark without a torch; wooden doors with buttons (verified) | env_l2_corridor, env_l2_dark |

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Giant Scorpion, Swamp Slime, Giggler, Wizard Eye, Pain Rat, Ruster, Screamer, Rockpile, Ghost, Stone Golem, Mummy, Black Flame, Skeleton, Couatl, Vexirk, Magenta Worm, Trolin, Giant Wasp, Animated Armour, Materializer, Water Elemental, Oitu, Demon, Red Dragon, Lord Chaos (boss), Lord Order, Grey Lord | not met yet | names only (ROM text) | - | battle_* planned |

## 4. Items and equipment
A spread over types and tiers; the special ones (quest items, cursed, charged) marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Torch | light | sconce behind the hall gate (verified) | lights the view when held | system_torch_taken |
| Apple | food | floor behind the gate (verified) | eaten at the mouth (manual) | system_eat |
| Club, Axe, Samurai Sword, Sword | weapons | carried by champions (verified) | action-hand attacks (club: THROW, BASH, verified) | system_action_menu |
| The Firestaff | quest item | deep levels (source) | the goal | - |
| Magical Box, Moonstone, Flask | special | carried by Elija, Chani, Wuuf (verified pictures; names from ROM text) | - | - |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| LO FUL (magic torch) | Tiggy | a share of 36 mana (verified: mana bar dropped) | magic torch: light (source: manual; effect not measured here) | system_cast |

## 6. Characters and people
Playable classes or characters, and the people of the world (shopkeepers, quest givers, rulers).

| Who | Role | Where | Shots |
|---|---|---|---|
| ryz (Halk the Barbarian, reincarnated) | fighter, party leader | mirror (7,9) | system_reincarnated |
| Stamm Bladecaster | fighter (axe) | mirror (11,15) | system_party_four |
| Tiggy Tamal | wizard (most mana in the hall) | mirror (9,13) | hall_champion_wizard |
| Wuuf the Bika | caster with a flask | mirror (12,13) | system_party_four |
| Hissssa Lizar of Makan | lizard champion (not taken) | mirror (16,14) | hall_champion_lizard |

## Open questions
What exists but was not seen, and how it could be reached.
