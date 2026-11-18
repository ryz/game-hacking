# Digital Devil Monogatari: Megami Tensei II (Famicom, English translation patch) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Presses during typing text are ignored
**Behavior:** while a text page (the "Caution for Devil Busters" pages, battle messages) is still typing, a button
press is dropped instead of finishing the page or being queued; the next press after the page is complete works.
**Intended:** unclear (many games of the time finish the page instead).
**Confidence:** (verified) with the route of checkpoint `naming`.
**Impact:** none for a player who reads; it only matters for automated input.

## A story-point list left in the cartridge
**Behavior:** the cartridge holds a list of 50 romanised story points ("Elder in Micon" to "The Y.H.V.H"), in the
original Japanese release as well as the translation; it looks like a developer's scenario jump menu.
**Intended:** a debugging aid removed from normal play (inferred).
**Confidence:** (inferred) from the text; no way to open it has been found.
**Impact:** none in normal play.

## A leftover ERROR screen for event squares without a script
**Behavior:** stepping onto an event square that has no entry for the current area shows a black screen with
"ERROR", two pairs of hex numbers (world position and map position) and a letter, and the game stops there. Seen when
the Devil Buster floor-8 stairs target (a grey temple) is reached with Devil Buster's area still active, and when
walking off the bottom edge of that map (shot `error_screen`, checkpoint `db_last`).
**Intended:** a developer check that should never show in normal play (inferred).
**Confidence:** (verified) for the screen; (inferred) that normal play cannot reach it.
**Impact:** none in normal play; a softlock if reached.

## The last Devil Buster stairs are inside a wall
**Behavior:** the stairs pair listed last for Devil Buster (floor 8 to a grey stone temple) starts on a square of
floor 8's top wall that no step can enter; its target, when forced, is a pocket where every step reports ERROR.
**Intended:** unclear: either used by a script after the Devil Buster finale or left over from development.
**Confidence:** (verified) for the wall; (RAM) for the stairs list.
**Impact:** none for a player.

## Untranslated lines show as garbage letters
**Behavior:** some lines are printed as random Latin letters and symbols: the confirmation after SAVE DATA
("G3HL-LP" instead of a "recorded" message) and the ST GOLEM's negotiation questions and answers (shot
`battle_chat_golem`). The bytes are the original Japanese text drawn with the English font.
**Intended:** translated text (the patch's own save prompts "WANT TO SAVE? / CHOOSE A SLOT. / RECORDED." exist in the
ROM).
**Confidence:** (verified) on screen; whether the patch leaves these lines out or one part was applied with the wrong
layout is not known.
**Impact:** negotiation, a core system, is unreadable in places.

## A Devil Buster game over continues the story
**Behavior:** losing every hero inside Devil Buster shows GAME OVER and then the real-world computer room ("EBO
WATCHED RYZ QUIT THE GAME AND SPOKE."); the party keeps its levels but Macca and MAG drop to 0 (route of
`computer_room`).
**Intended:** yes: quitting the computer game is part of the story frame (inferred).
**Confidence:** (verified).
**Impact:** a player can leave Devil Buster at any time by losing; whether the Pazuzu scene still follows is not known.

## Untranslated lines are a gap in the patch, not a mis-applied patch (coordinator, 2026-11-18)
The SAVE DATA confirmation ("G3HL-LP") and the ST GOLEM's negotiation lines show Japanese bytes drawn with the
English font. Checked: the same IPS applied without the iNES header garbles the very first English page (the
"Caution for Devil Busters" text), with the header it is clean. So the headered layout is right and these lines
are simply not translated by the patch. (verified)

## Devil Buster's ending found: Taurus and the S.ORB (round 2, 2026-11-18)
**Behavior:** Devil Buster ends when Taurus (floor 2) is beaten and his S.ORB is offered at the fallen god statue
(floor 3); Pazuzu then appears. The "last stairs inside a wall" (entry above) are not on this route.
**Intended:** yes, the hints in Micon town spell it out.
**Confidence:** (verified) shots `taurus_appears` to `pazuzu_armory`, checkpoint `real_world`.
**Impact:** corrects round 1: the floor-8 stairs are a leftover, not a missing way out.

## Kiyohime kills a demon in one blow, always for its exact HP
**Behavior:** an overworld Kiyohime pair took a summoned PIXIE from 17 to 0 and KOBOL from 25 to 0 in one attack each;
raised to 41 HP, PIXIE still lost exactly 41 (route of `battle_demon_hit`).
**Intended:** probably an instant-death attack on demons (inferred).
**Confidence:** (verified) three samples.
**Impact:** early demons are lost at once against this enemy.

## Names and roles after Pazuzu
**Behavior:** Pazuzu addresses "RYZ AND EBO" as the messiahs and gives EBO magic; the real-world party is RYZ + EBO,
while CONDI is the second fighter inside Devil Buster.
**Intended:** unclear whether the three name prompts map to hero / girlfriend / friend as their texts say.
**Confidence:** (verified) on screen (`pazuzu_messiahs`, `pazuzu_program`).
**Impact:** captions of round 1 call CONDI the girlfriend and EBO the friend; check against later story scenes.

## Untranslated names in shops and battles
**Behavior:** some demon names (Kiyohime), shop items (Fire Guard, Dragon Mail, the weapon shop's list), town labels,
the Teleport entry and NPC lines show Japanese kana or garbled letters (shots `shop_armor`, `battle_demons`,
`teleport_list`).
**Intended:** translated text.
**Confidence:** (verified) on screen; a patch gap like the save confirmation (coordinator's check, above).
**Impact:** part of the shops and the later towns is unreadable in English.

## Naming prompts checked (coordinator, 2026-11-18)
The three prompts read, in order: "Your character is the young hero. Name him." (RYZ), "Name your girlfriend."
(CONDI), "Give a name for your best friend." (EBO). So the captions follow the game's own labels: the girlfriend is
the second fighter inside Devil Buster, the best friend is the second party member in the real world (and the one
Pazuzu calls the second messiah). **(verified: naming screens of the English-patched ROM)**
