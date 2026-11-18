# Wizardry: Knight of Diamonds (NES) - story, regalia and ending

## Overview
Gnilda's apparition on floor 1 tells the party that the staff of Gnilda was taken back: 'To obtain my staff, one
must acquire the five, and get over seven barriers' **(verified: `gnilda_apparition`, `gnilda_will`)**. The five
are the regalia of the Knight of Diamonds, each held by a guardian or hidden behind a barrier; keys and badges are
traded along a chain of NPCs. A lone character wearing all five passes the trials on floor 6 and trades them for
the staff; returning to the castle ends the game **(verified: `ending_*`)**.

## 1. The regalia
| Piece | Where | How sure |
|---|---|---|
| Hrathnir (sword; unidentified 'Broad sword') | floor 3 (16,3), 'A friendly' group | verified (scan), item from argument c |
| KOD's helmet | floor 4 (16,3), guardian Animated Object | verified fight, item inferred |
| KOD's shield | floor 2 (17,1), guardian | inferred |
| KOD's gauntlets | floor 5 (9,4), guardian | inferred |
| KOD's armor | floor 1 (15,2), guardian Animated Object ('The armor you seek... three steps ahead') | verified fight, item inferred |
Wearing all five: armor class shown as LO **(verified: `regalia_inspect`)**.

## 2. The key chain
Search on floor 1 (7,12) finds the Corroded key; the Kobold King gives the Gory badge; the orc on floor 2
trades the Weird emblem for the badge ('Attack the saucy kobold!'); the old man on floor 1 trades the key of
ebony for the 'red key'; the small man on floor 2 gives the key of cloister for it; the Wizardress on floor 3
gives the Mithril key for the emblem; 'the man' on floor 4 makes the Master key **(verified texts; the trades as
offered by each record: item given = argument a, item wanted = argument c, inferred)**.

## 3. Other encounters
The wishing well (floor 3, 5000 G.P.), the sage (floor 4, 100,000 G.P.), 'Mapiro Mahama Diromat' (floor 4, back
to the castle), the riddle of the cavern and the clear blue fountain (floor 5, 'Who will wade?'), the evil voice
'Where is the stuff now?' and the red writing 'I will leave it to the brave who brought back the stuff' (floor 6)
**(verified; outcomes of paying, wading not tested)**. Details per square: [maps.md](maps.md).

## 4. Ending
1. Floor 6, north of the stairs: 'One alone.' sends a larger party back to the castle; the room on fire sends back
   anyone not wearing all five pieces **(verified: `one_alone`, `room_fire`)**.
2. The lone knight is carried to Gnilda's room: 'Through your valor, wit, and presence of mind...', 'Behold! The
   staff of Gnilda!', 'RYZ traded an Item!' (the five pieces are gone, the staff is in the pack)
   **(verified: `ending_apparition` to `ending_staff_inspect`)**.
3. Taking the stairs to the castle: 'Congratulations! ... the Mark of Gnilda ... the order of Knight of the City',
   then 'Press [A] to select Knights' (other roster members get 'Make CONDI a Knight?'), then the staff roll
   **(verified: `ending_congrats`, `ending_knights`, `credits`)**.
4. Afterwards the hero shows a 'G' after the name, has 150,000 more E.P. and no staff **(verified: `ending_mark`)**.

## Open questions
- Which items the floor 5 barrier wants; what paying the well or the sage gives.
- What a knight who has already won finds at floor 6 (3,3) (message 7A, unseen).
