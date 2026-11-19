# Ultima II: The Revenge of the Enchantress (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).

## 1. Core loop
Walk the surface of a period, enter places, talk and trade, fight what comes near, and collect money, hit points
and items (verified for walking, entering, talking, a fight). The world clock runs: waiting passes turns
(verified). Between loops the player changes period through a time door or flies to a planet, and gathers the
few things the ending needs: the quicksword, the blessing, the ring, then Shadow Guard (verified with pokes).

## 2. Systems
Go through every group; write "none" where the game has nothing, do not drop the group.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Commands A-Z | 26 one-key commands (Attack, Board, Cast, Descend, Enter, Fire, Get, Hyperwarp, Ignite, Jump, Klimb, Launch, Magic, Negate time, Offer, Pass, Quit, Ready, Steal, Transact, Unlock, View, Wear, X-it, Yell, Ztats) (verified: prompts of all) | letter + direction or digit | - | playbook Controls | planned `system_cmd_*` | described |
| Player verbs | Real-time pass | with no key for about a second the game passes a turn ("CMD: PASS") (verified) | none | about 1 per second at the chosen speed | playbook | planned `gameplay_start` | described |
| Player verbs | Offer gold | gold in hundreds to a person in a direction; three people of New San Antonio answer with a quest item, a weapon or a statistic (verified for two) | `o`, direction, digit | 500 for Enilno and the ring | playbook Game structure | planned `system_enilno`, `system_ring` | described |
| Characters and progression | Generation | 90 points over six statistics, minimum 10 each; sex, race (human, elf, dwarf, hobbit), type (fighter, cleric, wizard, thief) add bonuses (human +5 intelligence, fighter +20 strength seen) (verified) | numbers | 90 points | playbook Boot | planned `menu_gen_*` | described |
| Characters and progression | Level | the level is the hundreds of experience ("A LEVEL 20" at 2083) (verified) | - | experience per kill: 4 for a devil | - | planned `inventory_ztats_late` | described |
| Characters and progression | Lord British | 50 gold buys 300/200/100 hit points below 500/750/1,000 (verified for 300; code for the rest) | Transact | | playbook | planned `dialogue_lord_british` | described |
| Characters and progression | Requirements | a weapon needs Agility above 8 x its number, armour Strength above 8 x its number (code) | Ready, Wear | quicksword 9, power armour 6 | playbook | - | described |
| Resources and economy | Gold, food, hit points | four numbers on the panel; food runs down with turns (verified) | - | start 400 / 399 / 400 | - | planned `hud_status` | described |
| Resources and economy | Shops | by quarter of a towne (weapons, armour, horses, pub) or village (oracle, food, cleric and wizard spells) (code; transport, pub, refusals verified) | Transact | horse 84 gold | playbook | planned `shop_*` | described |
| Resources and economy | Steal | try to take from a counter ("NO LUCK!") (verified) | `s` | | - | planned `system_steal` | described |
| Conflict | Melee | hit if a random number is below Agility; damage = (weapon x 8 + Strength) / 4 (code; hits and misses verified) | `a` + direction | | playbook | planned `battle_hit_kill` | described |
| Conflict | Status effects | paralysed legs or arms, sleep, magic missile; boots, cloak and green idol may save (ROM text, code) | - | | - | planned `boss_saved_by_idol` | described |
| Opponents | Surface and town people | guards, merchants, jesters, fighters, clerics, wizards, thieves; monsters with pictures from serpent to winged daemon (verified by pokes) | - | | content.md | planned `battle_*` | described |
| Opponents | Minax | 255 hit points, casts every turn, jumps to the mirrored chamber after each hit that does not kill (verified) | - | 255 | playbook | planned `boss_*` | described |
| Items and equipment | Weapons, armour | 9 weapons (dagger .. quicksword), 6 armours (cloth .. power) (ROM text) | Ready, Wear | | content.md | planned `inventory_ztats_late` | described |
| Items and equipment | Special items | 16 kinds, each opening something: ring (fields), ankh (rocket), tri-lithium (fuel), blue tassle (frigates), skull key and brass button (planes), wand or staff (magic), boots, cloak, helm, green idol, strange coin (code) | - | | playbook | - | described |
| Items and equipment | Loot | thieves drop a random special item, fighters torches and helms, wizards wands and staffs, guards keys (code) | kill | | playbook | - | described |
| Abilities and magic | Spells | light, down ladder, up ladder, passwall, surface, prayer (clerics); magic missile, blink, kill (wizards); bought in villages, cast with a wand or staff (ROM text) | `m`, `c` | | - | planned `system_shop_refused` | described |
| World and navigation | Five periods, time doors | doors wander over four squares per period, each leads to another period (code, verified) | walk onto the door | first door after 256 turns, moves every 8 | playbook | planned `system_time_door` | described |
| World and navigation | Places | one village, towne, castle, tower and dungeon at most per period (code, verified for 1423 B.C.) | `e` | | playbook | planned `gameplay_*` | described |
| World and navigation | Dungeons and towers | first-person, dark without a torch, ladders (verified entry) | arrows, `i`, `k`, `d` | 16 levels per map (inferred) | - | planned `gameplay_dungeon_*` | described |
| World and navigation | Vehicles | horse, frigate, plane, rocket (code; rocket verified) | `b`, `x`, `l` | | playbook | planned `gameplay_launch_site` | described |
| World and navigation | Space | hyperwarp by three coordinates, ten destinations, the sun, deep space, landing on grass only (verified) | `h`, digits, `l`, any key | 9-9-9 planet X | playbook | planned `gameplay_space_earth`, `system_hyperwarp` | described |
| World and navigation | Doors and fields | locked doors need keys; force fields cost 1,000 hit points without the ring (verified) | `u`, walk | 1,000 | playbook | planned `system_field_*` | described |
| Goals and gating | Main quest | Enilno -> blessing on planet X -> ring -> Shadow Guard -> Minax (verified) | | | playbook | planned quest shots | described |
| Chance | Rolls | hits, loot, monster creation, the hyperwarp off-course rule (deterministic from the fuel count) (code) | | | findings.md | - | described |
| Failure and recovery | Death | "RYZ IS DEAD!" when hit points run out (verified); what follows not seen | | | - | planned `gameover_dead` | open |
| Saving and sessions | Q | saves on the surface of Earth only; the game continues (verified) | `q` | | playbook | planned `save_quit` | described |
| Pacing and difficulty | Real time | turns pass on their own; Minax drains about 200 hit points a turn (verified) | | | - | - | described |

## 3. How the systems feed each other
- Fights give gold and experience; slain thieves, fighters, wizards and guards give the special items and keys
  (code) -> items open vehicles, magic, space and doors.
- Gold buys hit points from Lord British, food, horses, spells, and the two quest purchases (verified).
- Statistics gate weapons and armour; armour 5+ gates space; space gates the blessing; the blessing gates the
  ring; the ring gates Shadow Guard (verified chain).
- Time doors connect the periods: the rocket is in 2112, the quest people in 1990, Minax in Legends (verified).

## Open questions
- What happens after death; monster creation rules on the surface; spell effects; dungeon contents.
