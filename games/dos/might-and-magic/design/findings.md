# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Training makes a character a year older
**Behavior:** RYZ, age 18, trained from level 1 to 2 and the profile then showed age 19 (`train_levelup`, `profile_level2`).
**Intended:** probably intended (training takes time); the manual was not checked for it.
**Confidence:** (verified)
**Impact:** levels cost lifetime as well as gold.

## A leprechaun without payment still moves the party
**Behavior:** asking the Sorpigal leprechaun for a town with no gems in the party ends with the party on another square of Sorpigal, (8,5), in front of the blacksmith's sign.
**Intended:** unclear; looks like a deliberate "nothing happens, off you go".
**Confidence:** (RAM) for the cause, (verified) for the result (scout run).
**Impact:** none beyond confusion.

## The same fight square holds different monsters
**Behavior:** stepping on a fight square a moment earlier or later changes the group: Snakes or Strangling Vines on one forest square of sector C-2, Poltergeists or Vampire Bats in the room at Sorpigal (3,6) (`outdoors_vines`, `encounter_poltergeists`).
**Intended:** yes, random groups from the area's list.
**Confidence:** (verified)
**Impact:** a party can re-enter for an easier group.

## The ending does not check where the party came from
**Behavior:** the Inner Sanctum square only looks at one mark on each character (impostor defeated). A level 1 party placed on the square with that mark set gets the full ending and 500,000 experience each (`ending_sanctum`).
**Intended:** the door with the Key Card slot is the real gate; the square itself trusts it.
**Confidence:** (verified) with a memory edit, (RAM) for the condition.
**Impact:** none in normal play.

## A failed trap removal can end the game for a new party
**Behavior:** "Find/remove trap" by the level 1 Robber on the gold chest in Dusk set off the blade trap; all six characters went down and the game-over text followed (`chest_find_trap`). "Open it" on the same chest by the same Robber, or by the Knight, just opened it (`chest_opened`).
**Intended:** unclear; the manual says only the Robber has a real chance with traps.
**Confidence:** (verified), one try each.
**Impact:** on this chest, opening blindly was safer than trying to disarm.

## The shop sells what the shopper cannot use
**Behavior:** the blacksmith marks items the shopper's class cannot use with "-" but still sells them (Sorcerer, Short Sword, 20 gold); Equip then says "WRONG CLASS" (`shop_cant_use`, `equip_wrong_class`).
**Intended:** probably (buying for another character).
**Confidence:** (verified)
**Impact:** none; trade the item on.

## Rumors need tips
**Behavior:** "listen for rumors" at the Sorpigal tavern prints nothing until the bartender has been tipped twice (`tavern_rumor`).
**Intended:** yes.
**Confidence:** (verified), counts of one and two tips tried.
**Impact:** 2 gold per rumor.

## A bribe can cost every character's food
**Behavior:** Guardsmen with Gnomes took the bribe for "all your food": all six characters at 0 food afterwards (`encounter_bribe_food`).
**Intended:** yes (manual: food, gold and/or gems).
**Confidence:** (verified)
**Impact:** resting needs food; a cheap escape early, expensive far from a market.

## Fire Ball burned the party
**Behavior:** MNZ (set to level 7) cast Fire Ball (Sorcerer 3-1) at monster A in the first round against four Poltergeists standing in hand-to-hand range; the messages were "RYZ TAKES 18 POINTS OF DAMAGE!", then CONDI, then EBO; no monster was hurt (`combat_fire_ball`). Lightning Bolt from the same position hit the monsters (`combat_lightning_bolt`).
**Intended:** unclear: either an area spell that includes whoever stands next to the target, or a fault in this version. The manual's entry was not compared.
**Confidence:** (verified), one cast.
**Impact:** an area spell in melee can cost more than it gains.
- **The performance total of the ending depends on how many members carry the quest marks** (fix-up round
  2026-11-18). With only RYZ marked (record +7D = 5F; what the old `WORTHY` macro did by mistake) the Data
  Keeper said "PERFORMANCE TOTAL=70122"; with all six marked (`WORTHY2`) the same level-1 party gets
  "PERFORMANCE TOTAL=399602" (`ending_sanctum`). After the ending the mark byte of every marked member reads FF
  **(RAM)**. Both runs got the "excellent rating" text and +500,000 experience. What else enters the total was
  not measured.
- **Retreat at the encounter options has no message**, and a poisoned and a wounded character get the same
  temple menu: see [combat.md](combat.md) 6 and [sorpigal.md](sorpigal.md).
