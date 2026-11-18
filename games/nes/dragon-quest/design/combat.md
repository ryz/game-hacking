# Combat

## Overview
Battles are one hero against one enemy, turn by turn, drawn in a small window over the map: a landscape picture
on the overworld, plain black in caves, towns and castles. **(verified)** [battle_slime](../shots/main/dragon-quest_nes_jp_battle_battle_slime.png),
[battle_archmage](../shots/main/dragon-quest_nes_jp_battle_battle_archmage.png), [boss_green_dragon](../shots/main/dragon-quest_nes_jp_boss_boss_green_dragon.png)
Each turn the player picks Fight, Spell, Flee or Items, the hero acts, then the enemy acts. **(verified)**
[battle_command](../shots/main/dragon-quest_nes_jp_battle_battle_command.png) Random battles come while walking outside towns; three
enemies stand at fixed places and block the way until beaten (Golem, the Dragon of the swamp cave, the Dragon
King). **(verified)** `@late_golem`, `@late_green_dragon`, `@late_dragon_king_1`

## 1. Flow of a battle
1. "<Enemy> appeared!" and "Command?". **(verified)** [battle_slime](../shots/main/dragon-quest_nes_jp_battle_battle_slime.png)
2. Some battles start with the enemy acting before the first command ("... was ready!"): an Archmage in the
   ruined town cast Begira for 20 damage before the hero could move. **(verified)**
   [battle_archmage](../shots/main/dragon-quest_nes_jp_battle_battle_archmage.png)
3. A weak enemy may leave at once: "Wizard appeared! Wizard ran!" against a level 21 hero in the swamp cave.
   **(verified)** route `@late_swampcave` + Remira + 20 steps south
4. Winning gives experience (E) and Gold; a level-up is announced right after ("ryz's Lvl rose!", then each
   stat that rose). **(verified)** [battle_levelup](../shots/main/dragon-quest_nes_jp_battle_battle_levelup.png)
5. Losing: see section 5.

## 2. Hero actions
| Action | What was seen | Confidence |
|---|---|---|
| Fight | level 1, bare hands: 3 damage to a Slimess with "Critical!!!" | **(verified)** `@start_battle` |
| Fight | level 21, Loto's sword: 26, 27, 38 and 46 damage to the Dragon King's first form; 10 to 16 to his true form; 49 to the Dragon | **(RAM)** enemy life before and after each hit |
| Spell | the field list minus nothing: all ten spells are offered in battle | **(verified)** [battle_spell](../shots/main/dragon-quest_nes_jp_battle_battle_spell.png) |
| Spell, Begira | costs 5 MP; the screen flashes grey; an Archmage shrugged it off: "Spell not heard!" | **(verified)** [battle_spell_cast](../shots/main/dragon-quest_nes_jp_battle_battle_spell_cast.png) |
| Flee, Items | in the menu; not tried | **(verified)** menu only |

## 3. Enemies met
Life differs between two meetings with the same enemy, so it is rolled within a range at the start of the
battle. **(RAM)**
| Enemy | Where | Life seen | Its attacks seen | Reward | Confidence |
|---|---|---|---|---|---|
| Slimess | forest north-west of Tantegel | 4 | attack: 2 to a level 1 hero | 1 E, 2 G | **(verified)** [battle_slime](../shots/main/dragon-quest_nes_jp_battle_battle_slime.png) |
| Wizard | swamp cave | 13 | ran away | - | **(verified)** |
| Archmage | ruined town | 58 | Begira: 20; attack: 8 | - | **(verified)** [battle_archmage](../shots/main/dragon-quest_nes_jp_battle_battle_archmage.png) |
| Dragon | overworld north of Cantlin; one fixed in the swamp cave | 52, 65 | - | - | **(verified)** [battle_dragon](../shots/main/dragon-quest_nes_jp_battle_battle_dragon.png), [boss_green_dragon](../shots/main/dragon-quest_nes_jp_boss_boss_green_dragon.png) |
| Golem | fixed, one step north of Cantlin's gate | 54, 56 | attack: 34 to a level 21 hero in Loto's armour | - | **(verified)** [boss_golem](../shots/main/dragon-quest_nes_jp_boss_boss_golem.png) |
| Dragon King (shown as DrgnKing) | his throne, bottom floor of his castle | 90, 93 | attack: 4 | none: the true form follows | **(verified)** [boss_dragon_king_1](../shots/main/dragon-quest_nes_jp_boss_boss_dragon_king_1.png) |
| Dragon King, true form | follows the first form at once | 130 | fire: 44; attack: 40 | the ending | **(verified)** [boss_dragon_king_2](../shots/main/dragon-quest_nes_jp_boss_boss_dragon_king_2.png) |

## 4. The Dragon King
Talking to him on his throne brings "Welcome, ryz. I am king of all, the Dragon King.", "I've waited for one
like you.", "Be my ally and half the world is yours.", then the question "Will you be my ally?" with Yes and
No. **(verified)** [dragon_king_offer](../shots/main/dragon-quest_nes_jp_cutscene_dragon_king_offer.png),
[dragon_king_question](../shots/main/dragon-quest_nes_jp_cutscene_dragon_king_question.png) No starts the battle with the first form.
**(verified)** What Yes does was not tried. When the first form falls ("DrgnKing slain!") the true form appears
without a break and with the hero's HP and MP as they were. **(verified)** When the true form falls the hero
takes the Light Orb from his hands ("Raising it, Light pours out! So peace returns..."), and stands outside
the castle with HP and MP full. **(verified)** [ending_light_orb](../shots/main/dragon-quest_nes_jp_ending_ending_light_orb.png),
[ending_overworld](../shots/main/dragon-quest_nes_jp_ending_ending_overworld.png)

## 5. Death
At 0 HP every window turns red and the message is "You are dead.". **(verified)**
[death_battle](../shots/main/dragon-quest_nes_jp_gameover_death_battle.png) The hero then stands before the king in the throne room with
full HP and half his Gold (6135 became 3067); experience and items are kept; the king says "Oh ryz! How could
you have died?". **(verified)** [death_king](../shots/main/dragon-quest_nes_jp_gameover_death_king.png) There is no game-over screen.
**(verified)**

## Open questions
- Damage formulas, hit and flee chances, the full enemy list and rewards: not measured.
- What the Dragon King does when answered Yes.
- Whether the first-strike ("was ready!") depends on the enemy or on chance.
