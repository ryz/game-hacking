# The world: areas and what is in them

Shots are in `../shots/main/`; a shot id `x` in category `c` is the file `might-and-magic_dos_na_c_x.png`.
Coordinates are (x east, y north) from the south-west corner of a 16 by 16 map.

## Overview
The game has 55 maps: five towns, nine caverns, twenty wilderness sectors (A-1 to E-4), five castles, and
dungeons, ending in the Astral Plane, where the Inner Sanctum is **(verified: the game's own area list, read from
the program; the areas below were visited)**. Everything in an area is tied to a square and often to the
direction the party faces. Most areas other than Sorpigal and sector C-2 were reached here by a shortcut, not
on foot, so how they connect is only known where a square says so.

## 1. Areas in the order the game stores them
Sorpigal, Portsmith, Algary, Dusk, Erliquin; caverns 1-9; sectors A-1..A-4, B-1..B-4, C-1..C-4, D-1..D-4,
E-1..E-4; Castle Doom, Castle Blackridge North, Castle Blackridge South; Quivering Forest levels 1-2; Raven's
Wood levels 1-2; Enchanted Forest levels 1-2; Castle White Wolf; Castle Dragadune and three levels below it; the
demon's area; Castle Alamar; four "PP" levels; the Astral Plane **(verified: area list; the long names of the
forest dungeons, Dragadune and the PP levels are from the manual and the NES port: source)**.

## 2. Towns
Each town has an inn, a blacksmith, a market, a temple, training and a tavern, with its own people
**(verified for the squares shot; the rest from the square survey of each town)**:
| Town | Inn | Other places seen |
|---|---|---|
| Sorpigal (1) | The Inn of Sorpigal | see [sorpigal.md](sorpigal.md) |
| Portsmith (2) | Inn of Portsmith: "Lara, the innkeeper's voluptuous daughter" (`portsmith_inn`, `portsmith_signed_in`) | B. Smith's Workshop (`portsmith_blacksmith`), Maid Marion's Market, Temple Succubon, training by "a tall, muscular female clad in leather armor", a bar, Zam (`portsmith_zam`), a mist with a female voice that marks the male characters (`portsmith_secret`), stairs down at (0,15), passage outside at (1,15) |
| Algary (3) | The Inn of Algary: a half-orc (`algary_inn`) | Temple Half-Dead, Swampside Supplies, Arcon's Slop, training by "adventurers armored in dragon scales", Morango the Mystic (`algary_mystic`), Zom at (1,1), three magic portals (`algary_portal`), a "swaze pit", Ye Old Docks, passage outside at (8,15) |
| Dusk (4) | The Inn of Dusk: a ghostly apparition (`dusk_inn`) | Clearman's Training: empty suits of armor (`dusk_training`), Mystical Metal Works, Casper's Fine Spirits, Fewlerd's Feed, Temple Geist, a row of undead fights along the north wall (`dusk_vampires`, `dusk_banshees`), a gold chest (`dusk_chest`), stairs down at (13,1), passage outside at (15,7) |
| Erliquin (5) | The Inn of Erliquin: an elderly gnome (`erliquin_inn`) | Four Star Foods, Temple Gauche, Current Trends Ironworks, training by "three huge armor clad knights" (`erliquin_training`), the wizard Agar (`erliquin_agar`), a square that says "POOF!" at (8,7), stairs down at (15,7), passage outside at (0,7) |
Zam (Portsmith) and Zom (Algary) are "astral brothers" who each turn the party away with "you're not the
couriers"; the courier job is offered by an old man in the cavern below Sorpigal **(verified: `portsmith_zam`,
`cave_courier`; that the three belong to one errand is inferred)**.

## 3. The cavern below Sorpigal
Dark without light (`dungeon_darkness`); with the Light spell: green rock walls, portcullises and doors
(`dungeon_lit`). It holds the courier's desk (`cave_courier`), the Arena, where a man asks "will you
participate?" (`cave_arena`), wall messages ("THE JAIL ABOVE HAS MANY CELLS", "DON'T TURN AROUND!":
`cave_wall_message`), a "shimmering blue and white portal" in the south-east corner (`cave_portal`), and fight
squares: Rabid Lepers, Fire Ants, Skeletons, Mutant Larvae, Flesh Eaters, Snakes **(verified: `cave_skeletons`,
`cave_fire_ants`, `cave_snakes`, the square survey)**.

## 4. Wilderness
Sector C-2 lies outside Sorpigal; the party arrives at (10,10), where "a cavernous passage leads to Sorpigal"
**(verified: `outdoors_first`)**. Seen there: forest and mountain views, a glowing white column (`outdoors_forest`),
strange fountains (`outdoors_fountain`), statues that block the path (`outdoors_statues`), a gypsy seer who reads
a character's sign (`outdoors_gypsy`), a cave entrance (`outdoors_cave`), fights (`outdoors_vines`).
Sector A-1 (ice): the Dark Rider's challenge (`a1_dark_rider`), a block of ice reading "START AT 15-7 AND WALK
TO DOOM!" (`a1_ice`), the entrance of Castle Doom (`a1_castle_doom`). Sector E-1: a passage to Dusk and the
ruins of Castle Dragadune (`e1_dragadune`), a red expanse to the south (`e1_volcano`) **(all verified)**.
The Location spell names sector and squares: in Sorpigal "MAP SECTOR: C-2, SURFACE X=10 Y=10, INSIDE X=6 Y=5"
**(verified: `location_spell`)**.

## 5. Castles and the story
- Castle White Wolf: Lord Ironfist says "YOUR SERVICES ARE NEEDED!"; accepting gives "FIND THE STRONGHOLD IN
  RAVENS WOOD" **(verified: `whitewolf_ironfist`, `whitewolf_quest`)**. Also a chained demon as a prisoner and a
  button under a banner (`whitewolf_button`).
- Castle Alamar: guards at inner doors ("NO MERCHANTS PASS! BEGONE PEASANTS", `alamar_guards`), a maiden in a
  steel cage with the choices set free / torment / leave (`alamar_prisoner`), and the king on his throne:
  "VARNLINGS, I QUEST THEE TO FIND THE CRYPT OF CARMENCA. AWAY WITH YOU..." (`alamar_king`) **(verified)**.
- Castle Doom: a man in an iron suit held in a forcefield: "I AM THE TRUE KING ALAMAR, IMPRISONED BY A DEMONIC
  ALIEN BEING! CONFRONT HIM WITH THIS EYE OF GOROS AND YOU SHALL SEE HIS TRUE SELF" (`doom_true_king`); a golden
  door that repels the party (`doom_golden_door`); silver and gold "message interleave" inscriptions
  **(verified)**.
- Quivering Forest level 1: spinning floor (`qvl_floor_spins`), Okrim (`qvl_okrim`), large mixed groups
  (`qvl_hydras`), gold boxes **(verified)**.

## 6. The Astral Plane and the ending
Five astral projectors, each of which sends the party back to Sorpigal (`astral_projector`); a door with a
small slot: "NO ADMITTANCE!" without a Key Card (`astral_door`); behind it a dimly lit metallic room
(`astral_room`) and the Inner Sanctum: a panel slides open on "a mysterious man in a white coat"
(`ending_panel`); the Data Keeper prints the party's performance total and, for a party that has defeated the
impostor, gives every member 500,000 experience, tells it to return to the Inn of Sorpigal and to go on to the
Gates to Another World, and asks the player to mail the total to New World Computing; the party is then put
back in Sorpigal (`ending_sanctum`) **(verified; the party was placed on the square and marked as having
defeated the impostor, see `../playbook.md`)**. A party without that mark is told "YOU ARE NOT YET WORTHY FOR
TRANSFER. RETURN AFTER DEFEATING THE IMPOSTER." **(RAM: text and condition read from the area's program, not
seen on screen)**. The door wants a Key Card and all five projectors used by every member **(RAM, same
reading; with a Key Card placed in a backpack the door still said "KEY CARD IS REJECTED!": verified, cause
not found)**.

## 7. How each area looks (round 2 survey)
One view down a free corridor of each of the 55 areas was taken with `tools/survey.py` **(verified by those
frames; which picture data each area loads was not decoded: the file with the wall pictures has 17 blocks)**.
| Look | Areas | Shots |
|---|---|---|
| Town: large white bricks, wooden doors between torches, shop signs | Sorpigal, Portsmith, Algary, Dusk, Erliquin | `start_inn_door`, `door_locked`, `portsmith_inn_sign` |
| Cavern: grey-green rock, portcullises | caverns 1-9 | `dungeon_lit`, `env_cave6`; unlit: `dungeon_darkness` |
| Castle and dungeon: smaller white bricks; doors differ by place | Doom (plain), Blackridge North and South and White Wolf (cyan doors under red banners), Alamar (carved wooden doors), Quivering Forest 2 (blue portcullis), Raven's Wood, Enchanted Forest, Dragadune and below, the demon's stronghold, PP 1-4, Astral Plane (plain) | `env_doom`, `env_blackridge_s`, `env_whitewolf`, `env_alamar`, `env_qvl2`, `env_udrag1`, `env_demon`, `astral_room` |
| Wilderness: forest | C-1, C-2, C-4, D-1, D-4, E-1, E-2, E-3 | `env_forest_c1`, `outdoors_first`, `env_road_d1` |
| Wilderness: brown mountains | A-3, B-3, C-2, C-3, D-2, D-3, E-4 | `env_mountains_d3` |
| Wilderness: striped rock walls | A-1, A-4, B-2 | `env_cliffs_a1` |
| Wilderness: ice mountains and frozen ground | A-2, B-1, B-2 | `env_ice_a2`, `env_glacier_b1` |
| Wilderness: sea and beach | A-3, A-4, B-4, C-4 | `env_sea_a3`, `env_beach_a4`, `env_coast_c4` |
| Wilderness: swamp reeds | D-4, E-4 | `env_swamp_d4` |
| Wilderness: volcano and lava (red) | E-1, E-2 | `env_volcano_e1`, `env_lava_e2`, `e1_volcano` |
In the wilderness the terrain belongs to the square, so one sector mixes several of these.

## 8. Fixed fights found by the survey
`tools/survey.py` stepped onto every event square of all 55 areas and read the monster list **(RAM; the groups
with a shot are verified on screen)**. A selection; the full lists are written to
`work/scout/dos/might-and-magic/survey/` when the tool is run.
| Area | Square | Group |
|---|---|---|
| Dusk | north wall (0,12) to (7,13) | Ghouls, Mummies (`battle_mummies`), Specters, Banshees, Phantoms, Wights, Gargoyles, Vampires |
| Cavern 2 | fifteen squares | four of a kind each: Centaurs, Barbarians, Dinolizards, Militiamen, Druids, Giant Spiders, Caryatid Guards (`battle_caryatids`), Gargantuan Ants, Wild Boars, Cyclops (`battle_cyclops`), Ogres, Acidic Blobs, Fire Beetles |
| Cavern 3 | (8,7) | Demon Lord, Greater, Lesser and Minor Demons (`boss_demon_lord`); elsewhere Orc war bands with Chieftains and Ogres |
| Cavern 6 | (1,12), (0,15) | four Aliens (`battle_alien`), four Invisible Things |
| Cavern 9 | (15,4), (13,5), (14,6) | Medusas (`battle_medusas`), Basilisks |
| Sector A-1 | (5,2) after accepting | Dark Rider and eleven Warriors (`boss_dark_rider`) |
| Sector A-2 | (10,4), (14,2), (11,3) | ten, five, one Red Dragons (`battle_red_dragons`) |
| Sector B-2 | (2,1), (0,15) | five Mummies and a Lich (`boss_lich`); five Assassins and a Black Knight (`battle_assassins`) |
| Sector D-1 | (10,5) | the Scorpion and eleven Giant Scorpions (`boss_scorpion`) |
| Quivering Forest 1 | eleven squares | Okrim (`qvl_okrim`), hydras (`qvl_hydras`), Centaurs (`battle_centaurs`), Dinobeetles (`battle_dinobeetles`), Cave Giants with a Warlock, Fire Lizards with Trolls |
| Quivering Forest 2 | ten squares | Hippogriffs and Harpies (`battle_hippogriffs`), Minotaurs, Magicians, Druids and Clerics |
| Raven's Wood 2 | ten squares | Giants of four kinds (`battle_giants`), dragons with a Mummy, hydras, Assassins with a Chaotic Knight |
| Enchanted Forest 1 / 2 | ten / eleven squares | Cockatrices and Pegasi (`battle_cockatrices`); Werewolves (`battle_werewolves`), the Gray Minotaur with twelve Minotaurs (`boss_gray_minotaur`) |
| Below Dragadune 1 / 3 | eleven / thirteen squares | Lepers, Rotting Corpses, Zombies (`battle_lepers`); Elementals (`battle_elementals`), Evil Eyes (`boss_evil_eyes`), White Dragons (`battle_white_dragons`), Arch Mage, High Clerics, Ghosts, Steel Golems |
| PP 1 | eleven squares | Giant Scorpions (`battle_scorpions`), Magicians (`battle_magicians`), Silver Dragons, Gargoyles, Stone Golems |
| Cavern 1 | the Arena (1,13) | two Unicorns (`cave_arena_fight`) |
Other things the survey showed: sector C-1 has deserted merchant wagons to search (`env_forest_c1`); Portsmith's
blacksmith sells Spear 15, Mace 40, Scimitar 40, Short Bow 75, Glaive 80, Bardiche 80; Large Shield 50; 10
Foot Pole 10, Smelling Salt 50, Curing Potion 350, Antidote Brew 500 (`portsmith_weapons`, `portsmith_armor`,
`portsmith_misc`) **(verified)**.

## Open questions
- How the areas connect on foot (exits, stairs, portals) beyond Sorpigal and C-2.
- The quest chains of Lord Ironfist, the king and the other lords; where the Key Card and the Eye of Goros are.
- The other 34 areas were not visited.
