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

## Open questions
- How the areas connect on foot (exits, stairs, portals) beyond Sorpigal and C-2.
- The quest chains of Lord Ironfist, the king and the other lords; where the Key Card and the Eye of Goros are.
- The other 34 areas were not visited.
