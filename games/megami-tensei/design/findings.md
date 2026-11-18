# Digital Devil Monogatari: Megami Tensei (Famicom, English translation patch) - findings: quirks, exploits and likely bugs

Each entry: what the game does, what was probably intended, how sure we are, and what it means for a player.

<!-- Template:
## Short name of the quirk
**Behavior:** what happens, how to reproduce (route/checkpoint, shot id).
**Intended:** what the designers most likely meant, or "unclear".
**Confidence:** (verified) / (source) / (RAM) / (inferred).
**Impact:** what it changes for a player (exploit, softlock, balance).
-->

## Negotiation outcome follows the moment of the answer
**Behavior:** the same talk with Nekomata (from checkpoint `rich`) ends with "Thanks!" and the demon fleeing with
the MAG when Yes is pressed at once, but with "Nekomata suddenly joined the party." when Yes is pressed about
16 x 60 frames later (shots `negotiation_fled`, `negotiation_join`).
**Intended:** a random roll per answer; the random numbers advance every frame.
**Confidence:** (verified) for the two routes; (inferred) for the cause.
**Impact:** a player who is refused can retry with different timing; MAG is lost when the demon flees.

## Password does not keep EXP
**Behavior:** after the sage's password is entered, Nakajima's Stats page shows EXP 0 although EXP had been
earned (shot `status_nakajima`, checkpoint `password_loaded`).
**Intended:** unclear (the password may store levels only).
**Confidence:** (verified) once.
**Impact:** EXP toward the next level is lost on every password restart.
