# Phantasie - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface. The same shots also
appear in [systems.md](systems.md) and [content.md](content.md); overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py phantasie`. Shot ids: `main` set.

## 1. Conventions
- **Input:** cursor keys move a highlight bar, Return selects (manual: also space and the joystick fire
  button) **(verified for Return)**. Letters only in towns: C cast, U use items, G game save, P printout
  **(verified)**. Numbers are entered with a +10/-1/+1/-10 selector or by typing digits **(verified: bank,
  spell, rank)**. Yes/no prompts put YES highlighted first **(verified)**. Keys pressed while the game is busy
  are often lost (verified; see playbook). **Observation:** menus are fully cursor-driven, a C64-specific
  rewrite of the letter menus of the original (source: C64 supplement).
- **Layout:** a 40-column screen in fixed regions: party list at the top, a picture area at the left, a menu
  column at the right, a name plate (town name, building picture or COMBAT) in the brown box at the bottom right
  **(verified: `town_pelnor_party`, `bank_menu`)**. Messages appear in a coloured bar above the picture.
- **Text:** capitals in a custom font; bar colours: cyan for terrain and actions, green for descriptions of
  places, yellow for rewards, white for deaths and "monsters killed", purple for spells, red for warnings
  **(verified: battle and world shots)**.
- **Feedback:** combat messages appear one at a time and advance by themselves **(verified)**; disk loads show
  a static screen for up to a minute (verified).
- **State visibility:** the party list (name, race, class, status) stays on every town screen; hit points and
  magic need Health (wilderness) or the combat list **(verified)**.
- **Help and onboarding:** none on screen; everything is in the manual (source).

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Boot credits | screen | power-on -> title | publisher, version 1.4 | SSI, LDW, Drive Technology loader | - | - | `boot_ssi` | - |
| Title picture | screen | boot -> start menu | title while the game loads | logo with a sword | - | - | `title_logo` | - |
| Start menu | menu | title -> Pelnor / saved town | new or continued game | 1 Start in Pelnor, 2 Continue saved game | 1, 2 | - | `menu_start` | - |
| Town screen | screen | town entry -> buildings, gate | hub of the town | party list, six buildings, letter commands, town name | cursor, return, C U G P | ENTER marker over the chosen building | `env_town_pelnor`, `town_pelnor_party`, `town_pineville_old` | - |
| Guild menu | menu | town -> creation, roster | characters | spells ... exit | cursor | - | `guild_menu`, `guild_party` | - |
| New character | menu | guild -> roll | race, class | lists | cursor | - | `guild_new_race`, `guild_new_class` | - |
| Attribute roll | prompt | class -> name | keep the rolled character | five attributes, KEEP THIS CHARACTER? yes/no | yes/no | - | `guild_roll` | - |
| Name entry | prompt | roll -> sheet | name | INPUT NAME field | letters | - | `guild_name` | - |
| Character sheet | screen | creation, inspect | everything about one character | level, class, race, attributes, HP, magic, bank gold, XP, score, skills, equipment, spells | key | - | `char_sheet_ryz`, `guild_inspect_cubi`, `char_sheet_level2` | full-screen text page |
| Roster "who?" | list | add, rename, purge, inspect | pick a character | name, status, class, town number | cursor | dead characters marked | `guild_roster`, `guild_rename` | - |
| Drop | list | guild | remove from party | party list highlight | cursor | - | `guild_drop` | - |
| Spells (guild) | prompt | guild -> who? | learn a spell | how many more, cost, possible numbers | selector, digits | YOU LEARNED | `guild_spells`, `guild_spell_learned` | - |
| Training | prompt | guild -> who? | buy a level | IT WILL COST N GP. OKAY? | yes/no | "you need N more experience points" (start set) | `guild_training_cost` | - |
| Bank | menu | town | gold | withdraw, deposit, exit; per-member amounts | cursor, selector | gold carried line | `bank_menu`, `bank_withdraw`, `bank_deposit` | - |
| Armory | list | town -> who will shop | buy | cash, stock with price and points; buy / another shopper / exit / armory | cursor | SOLD, YOU CAN'T PURCHASE THAT | `armory`, `armory_buy` | - |
| Inn | menu | town | rest, distribute | exit, distribute | cursor | - | `inn` | - |
| Mystic | message | town | party score | text panel with crystal ball | key | - | `mystic` | - |
| Cast / use / printout | prompt | town letters | who will cast / use; printer | - | cursor | - | `town_cast`, `use_items`, `printout` | - |
| Shares | prompt | town entry, save, deposit | divide gold and XP | shares 0-3 per member, value of a share | 0-3 | SAVING | `town_shares_return`, `save_saving`, `bank_deposit` | - |
| Leaving | transition | gate -> wilderness | load | LEAVING PELNOR | - | - | `leaving_pelnor` | - |
| Wilderness map | screen | town gate | travel | section map, party figure, compass, minimap of the island | directions, return | terrain message bar | `env_world_pelnor`, `env_world_west`, `world_path_message`, `world_red_pony`, `world_hillside_door` | - |
| Place prompts | prompt | wilderness square | enter a town, inn, dungeon | A TOWN/AN INN/A DUNGEON ... YES/NO | yes/no | - | `world_town_prompt`, `world_inn_prompt`, `world_dungeon_prompt`, `world_inn_rest` | - |
| Wilderness commands | menu | return on the map | actions | inspect ... move | cursor | - | `world_cmd_menu` | - |
| Party health | screen | command menu | HP and magic | table, dead/okay/sleep legend | key | - | `world_health` | - |
| Status report | screen | command menu: inspect | trip summary | days out, XP, gold, items acquired | key | - | `world_status` | - |
| Disk request | prompt | dungeon entry | swap disks | INSERT DUNGEON DISK AND PRESS A KEY | any key | - | `dungeon_disk` | - |
| Dungeon exit | prompt | first dungeon square | leave | AN EXIT. TAKE IT? with the gate picture | no/yes | - | `dungeon_exit_prompt` | - |
| Dungeon view | screen | dungeon | explore | explored corridors and rooms in black on grey, room name bar, compass | menu, directions | - | `dungeon_menu`, `env_dungeon_passage`, `env_dungeon_guardroom`, `env_dungeon_hall`, `env_dungeon_hallway` | - |
| Encounter | transition | walking -> combat | warn | AN ENCOUNTER | - | - | `world_encounter` | - |
| Combat picture | screen | each round | show the fight | monsters by rank, party figures, one message bar | - | hit/miss/damage/dies messages | `battle_bantirs`, `battle_ants`, `battle_hit`, `battle_cast`, `battle_spell_damage`, `battle_member_hurt`, `battle_ant_dies`, `battle_bee_hits`, `battle_fire_rank3`, `battle_bee_dies` | - |
| Party options | menu | combat start, each round | approach | party table (attacks, HP, magic), legend, ranks | cursor | MONSTERS DON'T RESPOND, THE MONSTERS STOP AND TAKE YOUR GOLD | `battle_party_options`, `battle_ants_options`, `battle_round2_options`, `battle_threaten`, `battle_beg_mercy` | - |
| Individual options | menu | fight -> go on fighting | per-member action | name, HP, MP, option; option list | cursor, selector | - | `battle_individual`, `battle_spell_select`, `battle_thief_rank` | - |
| Round result | message | end of fight | reward | MONSTERS KILLED, EACH SURVIVOR GETS N XP AND N GP | - | negative gold after begging | `battle_killed`, `battle_reward`, `battle_ants_reward`, `battle_beg_result`, `battle_flee` | - |

## 3. Screen flow
- Power-on -> credits -> title -> start menu -> (1) Pelnor town / (2) saved party's town.
- Town -> Guild (new, add, train, spells, inspect...), Armory, Bank, Inn, Mystic, letters C U G P; gate ->
  LEAVING -> wilderness.
- Wilderness -> town/inn/dungeon prompts; return -> command menu; random encounter -> combat -> wilderness.
- Dungeon prompt -> disk request -> exit prompt -> dungeon view -> encounters -> combat -> dungeon view.
- Combat: party options -> (fight) individual options -> go on fighting -> round messages -> party options ...
  -> monsters killed -> reward.

## 4. Elements in detail
- **Combat table** (`battle_party_options`): # and name, attacks per round, hit points current/max, magic
  current/max; legend DEAD (grey), OKAY (yellow), SLEEP (blue) colours the rows; bottom bar lists every rank
  with count and monster name.
- **Wilderness side panel** (`env_world_pelnor`): compass words, the chosen direction highlighted after a step;
  minimap of the island with the current section in green.

## Open questions
- Use items and cast in town were opened (who?) but not followed through (scroll text not shown).
- Dungeon Look showed nothing new on the first square.
