# Ultima II: The Revenge of the Enchantress (DOS) - content (variety lens)

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
| Environments | 5 Earth surfaces, 9 planet surfaces, about 20 town/castle maps, dungeons and towers (files) | section 2 | `tools/u2map.py --list` |
| Opponents | people of 8 kinds, monster pictures, Minax | section 3 | - |
| Items | 16 special items | section 4 | playbook Game structure |
| Equipment | 9 weapons, 6 armours | section 4 | - |
| Abilities / spells | 9 spells | section 5 | - |
| Characters and people | the hero (4 races, 4 types); named talkers in every town (TLK files) | section 6 | - |
| Vehicles | horse, frigate, plane, rocket | section 4 | - |

## 2. Environments
One row per distinct look or place type (tile or wall set, terrain, interior, special place), not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Today's continents | 1423 B.C., 1990, 2112 surfaces | the same coasts, different places (verified 1423 B.C.) | planned `gameplay_start` |
| Pangea | 9,000,000 B.C. | one supercontinent (verified) | planned `gameplay_surface_1` |
| Legends | Time of Legends | a round island with Shadow Guard in the middle, a walled islet in the south (verified) | planned `gameplay_legends_islet` |
| Towne and village | Linda, New San Antonio, villages | brick floors, grey walls, counters, names in letters (verified) | planned `gameplay_linda` |
| Castle | Lord British, Shadow Guard, Ozys Place | throne room, force-field gate, chambers (verified) | planned `gameplay_castle_lb` |
| Launch site | 2112 village | "CCCP TEST LAUNCH", three rockets on pads (verified) | planned `gameplay_launch_site` |
| Dungeon / tower | every period but Legends | wireframe, dark (verified) | planned `gameplay_dungeon_torch` |
| Space | anywhere | star field, hyperwarp tunnel (verified) | planned `gameplay_space_earth` |
| Planet X | 9-9-9 | its own continents, Ozys Place, a kitchen (verified) | planned `gameplay_planet_x` |

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Guard | towns | soldier | stands, carries keys ("PAY YOUR TAXES!") (verified line) | planned `dialogue_guard` |
| Thief | towns, jail | horned figure | steals ("A THIEF STOLE SOMETHING!" ROM text), drops special items (code) | planned |
| Devil | surface (poked) | horned beast | fights; 4 experience, 3 gold (verified) | planned `battle_devil` |
| Winged daemon | Shadow Guard | winged figure | guards Minax (verified) | planned `boss_minax` |
| Minax | Shadow Guard | robed enchantress | casts "DIE FOOL!", jumps between chambers (verified) | planned `boss_*` |

## 4. Items and equipment
A spread over types and tiers; the special ones (quest items, cursed, charged) marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Enilno, the quicksword | weapon 9 | Santre, 500 gold (verified) | best weapon; needs Agility 49+ (code) | planned `system_enilno` |
| Light sword | weapon 7 | shops (inferred) | damage 7 x 8 + Strength, / 4 (code) | planned `inventory_ztats_late` |
| Reflect armour | armour 5 | shops (inferred) | needed for space (verified) | - |
| Ring | quest item | the old man, 500 gold after the blessing (verified) | walk through force fields (verified) | planned `system_ring` |
| Ankh | special | thieves (code) | board a rocket (ROM text) | - |
| Tri-lithium | special | thieves, dungeon level 16 (code, talk) | rocket fuel (verified) | planned `gameplay_space_earth` |
| Blue tassle | special | thieves; sailors (pub tip) | board a frigate (ROM text) | - |
| Strange coin | special | thieves (code) | negate time for 20 turns (code) | - |
| Green idol | special | thieves (code) | may stop Minax's spell ("SAVED BY IDOL!", verified) | planned `boss_saved_by_idol` |
| Rocket | vehicle | 2112 village (verified) | flies to the planets (verified) | planned `gameplay_launch_site` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Light, Down ladder, Up ladder | clerics and wizards | bought in villages (ROM text) | dungeon travel | - |
| Passwall, Surface, Prayer | clerics (ROM text) | | | - |
| Magic missile, Blink, Kill | wizards (ROM text) | | | - |

## 6. Characters and people
Playable classes or characters, and the people of the world (shopkeepers, quest givers, rulers).

| Who | Role | Where | Shots |
|---|---|---|---|
| ryz | the hero: male human fighter | everywhere | planned `inventory_ztats_new` |
| Lord British | king, sells hit points for tribute | castle of 1423 B.C. (verified) | planned `dialogue_lord_british` |
| Santre the Swashbuckler | jailed, sells Enilno ("Beware, I've a quick blade!") | New San Antonio jail (verified) | planned `system_enilno` |
| The old man | under A TREE, sells the ring | New San Antonio (verified) | planned `system_ring` |
| Father Antos | blesses ("You have earned my blessing.") | Ozys Place, planet X (verified) | planned `dialogue_father_antos` |
| Brother Antos | "Search the stars for my kin!" / "Have you found my father?" | castles of 1423 B.C. / 1990 (TLK) | - |
| The Sightless Sage | "Find the Father Earn the Ring!" | village of 1990 (TLK) | - |
| The Phylosopher | "She's GOT to be at 9-9-9!" | village of Pangea (TLK) | - |
| Minax | the enchantress: "A coward dies a thousand deaths, a hero only one. Either way, you lose!!!" | Shadow Guard (TLK) | planned `boss_minax` |
| Cameos | Richard Garriott, Owen K. Garriott, Robert Woodhead, Dupre, Marlin Perkins, Margot and Al Tommervik, the Hotel California clerk | towns of Earth and the planets (TLK) | - |

## 7. Talk lines
Every named person's line, in the order of the talk file (person types 81, 82, ... in the map's object list; `tools/u2town.py MAP` shows where they stand). Text as the game shows it (ROM text).

| Place | Lines |
|---|---|
| Shadow Guard (Legends castle) | The she-creature begs: Take me I'm yours! / Homer the Salesman asks: Ya want some life insurance? / David Alpert whimpers: I've done a bad thing... / Minax cries: A coward dies a thousand deaths, a hero only one. Either way, you lose!!! |
| village of Pangea | An astronaut claims: There is a planet 'X'! / An astronaut claims: Father Antos lives on 'X' / The druid: Anol nathrac uth das bessod dien doch dientes! / The Phylosopher theorizes: She's GOT to be at 9-9-9! |
| village of 1423 B.C. | Grendel the Bum says: Masters of riddle are masters indeed! / Andy Greenberg complains: What? No software?!? / Robert Woodhead exclaims: Copy protect! Copy protect! / The chaste nubile nymph asks: Visit the Hotel California? |
| Towne Linda (1423 B.C.) | Ithilian the Wench calls: Make me an offer sailor! / John Mayer orders: TAKE OUT THE TRASH!!! / Gerry Mayer proclaims: We know small computers! / Keith says: No thanks, trying to cut down. |
| Lord British's castle (1423 B.C.) | Brother Antos ordains: Search the stars for my kin! / Bishop Bob preaches: Confess to Brother Antos! / Andre the French chef burps: I drink therefore, I am! / Commander Decker screams: Is it soup yet?!! / The wandering bard asks: Do you know the way to San Jose? |
| village of 1990 A.D. | Lady Sherrie cries: Gag me with a spoon! / Ronall Mc Donall sings: Try our new Ride-Through! / The Sightless Sage says: Find the Father Earn the Ring! / Lady Mary Ellen pleads: Beat me kick me tell me lies! |
| New San Antonio (1990 A.D.) | Santre the Swashbuckler warns:Beware, I've a quick blade! / An old man mumbles: I'm an old man. / The Flopy Fighter brags: I own one of everything! / A clerk states: Welcome to the Hotel California! |
| castle of 1990 A.D. | Brother Antos inquires: Have you found my father? / Sister Sledge sings: We are family! / Andre the French chef says: Hic, wan som colduck, hic? / The merchant orders: Give the King a tribute! / The subdued balron whimpers: Lithium packs the 16th level! |
| village of 2112 A.D. | Waren Beatty asks: Have you seen Diane Keaton? / Chuckles the Bumble cries: Can I look yet, is it over? / The Village Idiot suggests: Offer the hotel clerc gold! / Red the Pirate boasts: I've a broken Ultima ]I[, want one? |
| towne of Mars | Marlin Perkins threatens: Go in and I'll zap you! / Owen K. Garriott asks: Have you seen my shuttle? / Hecate chants: Bubble bubble toil and trouble! / The Historian declares: George Washington slept here! |
| village of Jupiter | The Jocker laughs: You're half way there! / The Pirate chortles: I own 30 tassles! / Dupre the Swashbuckler asks: Wanna buy a duck? / Johnny Jones asks: Know where I can get a duck? / U bother me! |
| village of Uranus | The Swamp Jester laughs: You lose, cadet! / The Court Jester says: Isn't this a silly Place? / The French Jester begs: Manger moi! / The Stoned Jester complains: Rocks have spirits, too! |
| village of Neptune | Debbie the lifeguard yells: Get a big grip! / Richard Garriott promises: Tomorrow--for sure! / Howie the Pest hounds: Isn't Ultima ][ finished yet? / Johnathon Ben asks: This ever happen to you? |
| village of Pluto | Margot Tommervik exclaims: Talk softly to me! / Al Tommervik inquires: Do you read me? / Big Bob jaws: Give Bill 300 gold! / Bill Bruiser demands: Give Bob 600 gold! |
| towne of Pluto | The Seaworthy Pirate says: See the clerk in New San. / The Burly Pirate says: New San. is full of magic! / The Ugly Smelly Pirate says: Antos is the answer! / The Big Bouncer stalls: Where the hell is your I.D.? |
| towne of planet X | Ugly Irving states: No mages allowed! / Kieth Zabalaoui says: I've never done this before! / An experienced warrior says: Find Antos, earn the Ring! / A wimpy warrior squeals: Antos is on 'X'! |
| Ozys Place (planet X castle) | Father Antos chants: You have earned my blessing. Return and claim the Ring! / Sing Lee the cook yells: Kichen clost, com bac lato! / Justin the Jailer warns: I wouldn't go in there! / Queen Susan says: Father Antos awaits you! |

## Open questions
What exists but was not seen, and how it could be reached.
- Natural surface monsters (none appeared at the start), the frigate and plane, other planets, dungeon
  monsters: reach by `TIME`, `POS`, object pokes and the planet coordinates in the playbook.
