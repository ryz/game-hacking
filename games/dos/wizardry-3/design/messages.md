# Wizardry III: Legacy of Llylgamyn (DOS) - messages

Every text a maze square can show, as read in play (**verified**: shown on screen by pointing the floor 6 riddle
square at each message number, `../tools/msgdump.py`, and for the riddles, signs, statues and search squares also by stepping onto the
square). The disk stores them compressed. Numbers are the game's message numbers; a message runs on over the
following numbers (those show as blank boxes on their own). Where: floor (x,y), from [maps/floors.txt](maps/floors.txt).

## Overview
107 message records: signs and atmosphere, five riddles and a password, a merchant (Abdul) with a taxi and a crystal
for sale, a monk and an apparition who trade, statues, and the dragon L'kbreth's warning and farewell.

## 1. Messages
| No. | Text | Where | Square kind |
|---|---|---|---|
| 0 | You stand on a beach. Beyond it lies a dark lake, in which is a small island. | floor 1 (1,2), (2,1) | 13 (AUX0 31) |
| 2 | You are at the water's edge. If you go any further, you will drown! | floor 1, 14 lake squares | 5 (AUX0 5) |
| 4 | A sign on the door reads: "Barracks" | floor 1 (2,19) | 1 |
| 5 | Before you stands a great fortress. Between its parapets lies a deep moat, and a sign by the moat reads: "Beware of the moat monsters!" | floor 1 (1,17) | 1 |
| 9 | Hear ye the words of L'kbreth: To all who trespass here, good or bad, I give my warning: neither good nor evil alone can triumph here. | floor 1 (18,13) | 1 |
| 13 | Farewell. May your way be easy. (with a picture) | floor 6 (8,3) | 13 (AUX0 0) |
| 14 | I'd turn back if I were you. | floor 3 (2,3) | 1 |
| 15 | Have you considered another direction? | floor 3 (3,2) | 1 |
| 16 | A sign on the door reads "Wine cellar" | floor 2 (12,19) | 1 |
| 17 | A glowing message appears in mid-air: S.E.G. Po'le, Grand Wizard / Office hours by appointment only / The wizard is *out* / Do not enter under pain of undeath! | floor 2 (2,1) | 1 |
| 21 | Shhh! Did you hear a noise back there? | not on a map square (inferred: used by code) | - |
| 22 | A large, dusty desk stands against the far wall. Its drawers are overflowing with books and papers. Inlaid in the desktop is an ornate letter 'P'. | floor 2 (7,1) | 4 (search: Staff of Earth) |
| 26 / 28 | An elegantly dressed woman with a whip demands, "What's the password?" / answer: ABDUL SENT YOU | floor 2 (7,11) | 10 |
| 29 | A short, swarthy man in a turban sidles up to you and whispers: "Tell them Abdul sent you" | floor 4 (12,12) | 1 |
| 32 | An oily black liquid drips from the ceiling, forming a pool on the floor. | floor 4 (10,5) | 3 (AUX0 4) |
| 34 | Look out! | floor 4, 11 squares at x = 17-18 | 9 |
| 35 | An aged monk appears before you: "In exchange for your soul, you may have what you find in this chest!" | floor 3 (7,7) | 4 (swap) |
| 38 | An apparition beckons to you from above a murky pool. Ominous shadows can be seen moving in the depths. | floor 3 (10,19) | 4 (swap) |
| 41 / 43 | Abdul's ethereal taxi service, 2500 GP one way / answer G2500 | floor 3 (18,19), (19,0) | 11 |
| 44 | An inscription on the door reads: Temple of the irascible Fung / Private!! No trespassing!! | floor 5 (19,9) | 1 |
| 47 / 49 | Abdul's ethereal taxi service... give up yet? Still only 5000 GP! / answer C5000 | floor 5 (0,2), (6,1), (6,16) | 11 |
| 50 / 59 | A short, swarthy man in a turban greets you. "May the winds of the desert be at your back and the sun leave you always in shade!" "My friends, I have just the thing for you: a powerful magic crystal; a gem containing the fire of the gods! And for you, my good friends, a bargain... only 25000 pieces of gold!" / answer 25000 | floor 5 (4,8) | 11 |
| 60 | Abdul opens a jewel encrusted coffer, and motions for you to look inside. With a low chuckle, he vanishes! | floor 5 (4,7) | 2 (AUX0 9) |
| 63 | A radiant statue stands before you. It's hands outstretched. In one hand it holds a shining crystal sphere. The other hand is empty. | floor 6 (4,5), (12,2), (18,17) | 13 (AUX0 2) |
| 67-69 | "A graveyard's dark..." / "And this trap's a crock..." / "Don't go any further, or..." | floor 3 (16,16), (16,17), (17,17) | 1 |
| 70 | You have reached the statue. (then "Will you search (Y/N)?") | floor 6 (17,17), (13,2), (4,4) | 4 |
| 71 / 80 | I am around you always but you have never seen me. You would never leave me, but were I gone, you would not cry out for me. What am I? / AIR | floor 2 (4,19) | 10 |
| 81 / 89 | Ours is an uneasy friendship. Your fathers toiled long to tame me, but even now I will go my own way if you do not tend me well. I am a powerful destroyer, yet my frailty is great. What am I? / FIRE | floor 4 (18,11) | 10 |
| 90 / 95 | Black figure on a black horse, he carries the white rose. The rising sun -- change will come, it follows wherever he goes. What card is he? / DEATH | floor 6 (19,17) | 10 |
| 96 / 100 | On my roll, you move forward; my turn is your turn. What am I? / WHEEL | floor 6 (11,4) | 10 |
| 101 / 106 | I am one of the deck of seventy-eight, and victory I foretell. Two bold steeds draw me forth, and stars shine from my crown. What card am I? / CHARIOT | floor 5 (5,13) | 10 |
| 107 | This is the grand dining room of the Grand Wizard. To the north is a large kitchen area, and to the south is the wizard's opulent boudoir. | floor 2 (18,12) | 1 |
Messages 73 and 74 (the two guardian squares) are empty boxes on their own (verified).

## Open questions
- Messages 1, 3, 6-8, 10-12, 18-20, 23-25, 27, 30-31, 33, 36-37, 39-40, 42, 45-46, 48, 51-58, 61-62, 64-66, 72-79,
  82-88, 91-94, 97-99, 102-105 show as blank boxes alone: continuation lines of the message before (inferred) or
  texts used by code.
