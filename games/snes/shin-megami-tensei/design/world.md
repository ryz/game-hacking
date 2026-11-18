# World and views

## Overview
The game switches between three presentations: first-person 3D corridors for buildings and dungeons, a 2D
overhead town map on which a blue marker moves along streets, and full-screen menus **(verified)**. A window in
the corner always shows the moon phase; in 3D it adds the floor and the facing, on the town map the place name
**(verified: `@apartment`, `@kichijoji`)**.

## 1. Opening sequence
1. Intro: Atlus logo, a magic circle, "199X Kichijoji, Tokyo", a computer terminal typing program text
   **(verified: boot probe)**.
2. Dream: the hero walks by himself through red corridors; a talking door asks his name; a crucified man and a
   man pinned by a demon are named and join; a woman at a pond calls herself Yuriko **(verified)**.
3. The hero wakes in his room in Kichijoji; a mail from "STEVEN" on the "DDS-NET" delivers the Demon Summoning
   Program and its manual (talk to demons, store them, summon them) **(verified)**.
4. His mother gives him 10000 yen and sends him to the cafe in the mall **(verified)**.
5. Outside: apartment corridor, exit prompt, Kichijoji town map; policemen close the district because of a
   murder investigation **(verified)**.

## 2. Moon phase
The phase advances with movement: NEW MOON, 1/8, 2/8, 3/8 were passed between the start of the dream and the
hero's room **(verified)**. The game counts steps; every 16 counted steps move the moon on by one eighth: the
window read HALFMOON at 64 steps, 5/8 MOON at 80, 6/8 at 96, 7/8 at 112 and FULLMOON at 128 **(RAM: step
counter read next to the window; `../shots/main/shin-megami-tensei_snes_jp_system_full_moon.png` was reached by setting the counter to 112 and
walking)**. In 3D one step forward counts as one; turning and bumping into a wall do not **(RAM)**. On the
town map the counter rises in jumps of 16 after a stretch of walking rather than once per square **(RAM)**.
What follows the full moon (waning names, the length of the whole cycle) and its effects (negotiation at full
moon) are not seen yet **(source: none yet)**.

## 3. Places
| Place | View | Seen | Tag |
|---|---|---|---|
| Hero's room | menu over a 3D backdrop: Computer, Save, Go to sleep, Leave the room | `@start` | **(verified)** |
| Home | menu: Go to your room, Go outside | after the mother's talk | **(verified)** |
| Apartment building, 1F | 3D corridor with an exit square | `@apartment` | **(verified)** |
| Kichijoji | 2D town map | `@kichijoji`, `../shots/main/shin-megami-tensei_snes_jp_map_map_kichijoji.png` | **(verified)** |
| Clinic (two red roofs south of the apartment) | 3D, four squares; the doctor's room pushes the hero back out after two pages ("My daughter's out at the moment") | `../shots/main/shin-megami-tensei_snes_jp_dialogue_clinic_doctor.png` | **(verified)** |
| Kichijoji arcade (yellow cross-shaped roof north of the railway) | 3D corridor of shop windows, 1F; knife shop, antique shop, cafe, a woman with a rumour about the hospital director | `../shots/main/shin-megami-tensei_snes_jp_gameplay_arcade_mall.png` | **(verified)** |
| Inokashira Park entrance | scene with three policemen: the park is closed after the murder | `../shots/main/shin-megami-tensei_snes_jp_dialogue_kichijoji_police.png` | **(verified)** |
| Street roadblocks (the X-shaped marks on the map) | scene with three policemen: "this area is currently off-limits" | `../shots/main/shin-megami-tensei_snes_jp_dialogue_police_roadblock.png` | **(verified)** |
| Later districts and the three acts | - | not reached | **(source: Wikipedia)**, see the playbook |

## 4. Moving on the town map and into buildings
The marker moves one map square per press and only along streets **(verified)**. Walking against a building
with an entrance (the clinic's red roofs from the street east of them, the arcade's south arm from the street
below it) switches to the 3D view inside **(verified: checkpoints `bldg_red`, `arcade`)**. Inside, the square
behind the entrance asks "There is an exit here. Will you leave?" with Yes preselected, over a view of the
street **(verified: `../shots/main/shin-megami-tensei_snes_jp_gameplay_exit_prompt.png`)**. Squares marked with a pair of X on the map are police
lines in this part of the story: stepping onto one plays the policemen's scene and the marker stays put
**(verified: three of them tried)**. Pressing the confirm button on the map opens the command menu over a
street view of the square the marker stands on **(verified: after the roadblock scenes)**.

Rooms inside buildings are single squares that run their scene as the hero steps in and then put him back in
the corridor **(verified: doctor, knife shop, antique shop, cafe)**. People standing in the corridor speak when
the hero walks into their square **(verified: `../shots/main/shin-megami-tensei_snes_jp_dialogue_arcade_rumor.png`)**.

## 5. Day 1 evening to day 2
The hero's apartment door opens onto the street square just south of a police line; walking left from that
square enters the building, which is the same building as the clinic ("the doctor next door")
**(verified: checkpoint `day2_map`, Left from the apartment square)**. Back home after the coffee errand the
mother talks about the park murder and asks ryz to walk the dog Pascal **(verified: checkpoint `home_back`)**.
Sleeping only leads to the second dream once a story event of day 1 has happened; in the run here that event
was not found and was set by hand **(RAM: checkpoint `dream2`)**. The second dream: the two heroes meet ryz
again, Yuriko appears, and a hooded priest is about to sacrifice a girl; agreeing to save her and calling her
by name (the heroine's name entry, 18 points to divide) rescues her
**(verified: `../shots/main/shin-megami-tensei_snes_jp_dialogue_dream2_save_girl.png`, `../shots/main/shin-megami-tensei_snes_jp_system_name_heroine.png`)**. Next morning a mail
brings the Auto-Mapping Program (a new COMP entry that draws the squares walked)
**(verified: `../shots/main/shin-megami-tensei_snes_jp_map_automap.png`)**, and from then on demons attack on the town map
**(verified: `../shots/main/shin-megami-tensei_snes_jp_battle_first_battle.png`)**.

## Open questions
- ~~How the hero gets back into his apartment building from the map.~~ Walk left from the square south of the
  police line (section 5).
- Which day-1 event opens the second dream (not the cafe, the park police or the roadblock).
- Size of the moon cycle after the full moon (the first half is 16 counted steps per eighth).
- What "Go to sleep" does before the first errand.
