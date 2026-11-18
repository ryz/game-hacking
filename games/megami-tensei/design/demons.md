# Demons: negotiation, the Comp, fusion

## Overview
Demons are met as random or fixed encounters in the labyrinth. Nakajima can talk to them in battle; a demon
that agrees joins the Comp (the Devil Summoning Program), from which it is called into the party for a fee in
Makka. Two demons whose classes are compatible can be fused by the Heretic on 8F into a new, stronger demon,
provided Nakajima's level is high enough to control the result.

## 1. Talking (negotiation)
- Talk is not in the party menu: in battle choose Fight, then for Nakajima Comp -> Talk (Comp in battle offers
  Call / Talk) **(verified: `comp_talk`)**. "Order" in the party menu only changes the party order **(verified)**.
- The talk opens with "Nakajima started talking." and the demon introduces itself or reacts ("It looks
  bewildered. Will you approach it?", "It's trembling. Try to scare it?", "Green Slime is drooling.")
  **(verified: route experiments from `neko_joined`)**.
- Demands seen: MAG ("84 MAG... Would you give it to me?", Nekomata), Makka ("80 Makka. Could I have it?"),
  a Jewel ("Jewel? Should you try giving it that?", Dryad) **(verified: `negotiation_mag`, `negotiation_jewel`)**.
  Without enough MAG: "That's not enough." and the demon asks for something else **(verified)**.
- A demon may take what it is given and still ask for more ("Hmm, that's still not enough."), may then join
  ("I will fight at your side." / "Nekomata suddenly joined the party."), or may take the gift and flee
  ("Thanks!" ... "Nekomata fled from the battle.") **(verified: `negotiation_join`, `negotiation_fled`)**.
- The outcome depends on the moment each answer is given: the same conversation with a later Yes gave a
  different result **(verified: two routes from `rich`)**. Other replies seen: "Dryad reluctantly joined",
  "Harpy/Ghost went berserk. Give up and fight it?", "... ran away" **(verified)**.

## 2. The Comp
- Field menu Comp: Call / Bind / Order **(verified: `comp_menu`)**. With no demons: "No allied demons."
  **(verified)**.
- Call lists the stocked demons with HP and the summon cost (Nekomata 58/58 HP, cost 86 Makka) **(verified:
  `summon_select`)**; a called demon appears as a third party line with HP and MP (Nekomata 58 HP, 22 MP)
  **(verified: `summon`)**.
- Up to seven demons can be stocked (the Stats list showed seven demon lines after a memory test) **(RAM)**.

## 3. Fusion at the Heretic
- The Heretic (8F) says "I can offer you no assistance now, but if you bring your allies to me, I will do what
  I can to help you." without demons **(verified: `heretic`)**.
- With two demons: "Fuse with which demon?" lists class, name and a 1-7 compatibility chart (o = can be fused
  with that slot) **(verified: `fusion_select`)**.
- Feral Nekomata + Fairy Dryad = Astral Trent (STR 10 WIS 9 ATT 9 AGI 8 DEF 9, Shift Points 6, MP 32, spells
  Psycho 4 and Hama 5; HP 80) **(verified: `fusion_result`, `fusion_confirm`)**.
- The result is shown before confirming; if its level is too high: "Its level is too high. Nakajima could not
  possibly control it!" (Nakajima level 1 and 7 refused, 14 allowed; level set through memory) **(RAM)**.
- Confirm "Will you fuse it?" Yes -> "Let us fuse it, then!", the two demons flash in turn, then "I'm Astral
  Trent and from now on, we are partners..." **(verified: `fusion_clip`, `fusion_done`)**.

## Open questions
- Exact level rule for controlling a fused demon (somewhere between 8 and 14 for Trent).
- What MAG is gained from (a Gnome battle gave EXP and Makka but no MAG).
- What decides the negotiation outcome besides timing (moon phase is said to matter: game text).
