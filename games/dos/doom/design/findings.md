# Doom (DOS, registered 1.1) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## The E1 end picture is an order form
**Behavior:** after the Episode 1 end text (complete about 2700 frames after the exit teleport) 1.1 shows the
order page ("Get all three episodes ... To order DOOM: call 1-800-IDGAMES") where 1.9 shows the id Software
credits (`ending_e1_order`; the same page as Read This! page 1, `readthis_order`).
**Intended:** yes: the shareware-era order page doubles as the end picture of the free episode.
**Confidence:** (verified)
**Impact:** none for play; registered owners are asked to order what they already have.

## Key 1 gives the chainsaw, not the fist
**Behavior:** with the chainsaw owned, pressing 1 from another weapon selects the chainsaw, even under
berserk; the first `weapon_fist` route (idkfa, berserk, `1`) punched with the chainsaw. Taking the chainsaw
away (route pokes its ownership to 0) gives the fist.
**Intended:** yes (the id source: 1 toggles fist/chainsaw only when already holding the chainsaw with berserk).
**Confidence:** (verified)
**Impact:** a player with berserk must press 1 twice to punch.

## Bosses die off-screen to the BFG spray
**Behavior:** on E3M8 the Spider Mastermind dropped from 210 health to dead while the marine turned away
after a shot; the next frames in view show only its corpse (`boss_spider_tracers`, `boss_spider_dead`). On
E2M8 the end text follows the Cyberdemon's death animation by about 200 frames (`boss_cyber_dies`).
**Intended:** yes: the BFG's tracers fire from the marine's position about a second after the ball bursts.
**Confidence:** (RAM) health read after every round.
**Impact:** turning away right after a BFG shot is safe; the kill still counts.

## The Cyberdemon outlasts a full load of cells
**Behavior:** 296 cells (seven BFG shots) left the Cyberdemon at 1130 of 4000 health because several balls
hit the pillars of the arena; an idkfa refill and two more balls finished it.
**Intended:** the boss is meant to need more than one weapon's ammunition.
**Confidence:** (RAM)
**Impact:** in honest play the arena's cover decides the fight more than ammunition.
