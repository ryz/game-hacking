# Combat, magic, negotiation and growth

## Overview
Battles start at random while walking (overhead and first-person) and are fought from a first-person view: the
enemy picture over a backdrop that depends on the place (Devil Buster's walls, a purple sky over grass outdoors)
**(verified: `battle_menu`, `battle_overworld`)**. Each round the player picks FIGHT, FLEE, CHAT or AUTO, then one
command per hero, then confirms with "IS THIS CORRECT?" YES/NO **(verified)**. Victory pays experience, Macca and
magnetite (MAG) **(verified: `battle_victory`)**; a level up lets the player add a point to one of five stats
**(verified: `levelup`)**.

## 1. Commands
| Hero | Commands | Notes |
|---|---|---|
| Hero (RYZ) | RUSH / COMP / ITEM / GUARD | COMP summons demons from the program **(verified: `battle_action`)** |
| Girlfriend (CONDI) | RUSH / MAGIC / ITEM / GUARD | MAGIC lists her spells with their MP cost **(verified: `battle_magic`)** |
ITEM with an empty bag answers "NO ITEMS TO USE." **(verified: `battle_item`)**. The friend EBO takes the second
slot in the shelter, with the same numbers the girlfriend had **(verified: `shelter`)**.

## 2. Magic
- DIA: heals one hero, 2 MP; usable in and out of battle (MAGIC > "WHO SHOULD CAST?" > "WHICH SPELL?")
  **(verified: `magic_spells`, `battle_dia`)**. One cast in battle healed RYZ "FOR 1 HEALTH" when he was 1 below his
  maximum **(verified)**; the full amount is not measured.
- The spell list in the cartridge also names MEND, MENDALL, POISUMDI, PARALAD, PETRADI and MAPPER **(RAM: ROM text)**.

## 3. Negotiation (CHAT)
- "RYZ CONVERSES.." then the demon answers. Seen answers: it calls another of its kind ("WILLOWISP CALLS A
  WILLOWISP."), "THEY WILL NOT TALK!", or a question with a YES/NO box **(verified: `battle_chat`,
  `battle_chat_golem`)**.
- The answer depends on the frame the command is given: over 60 one-frame variations a Willowisp in Devil Buster
  only ever called a friend or refused; ST GOLEMs on the overworld also asked questions **(verified)**.
- No demon joined in this run; the COMP's CALL then says "NO DEMON TO SUMMON." **(verified: `comp_call`)**.

## 4. Rewards and growth
| Fight | EXP | Macca | MAG | Evidence |
|---|---|---|---|---|
| Willowisp x1 | 4 | 20 | 8 | `battle_victory` (verified) |
| Willowisp x2 | 8 | 40 | 16 | play (verified) |
Rewards scale with the number of enemies beaten: 4 EXP, 20 Macca and 8 MAG per Willowisp **(computed from the two
rows)**. Level 2 came at 12 EXP; the status page then shows NEXT 28 **(verified: `levelup`)**. At level 2 the hero's
maximum HP went from 8 to 12 and the girlfriend's from 6 to 7, her MP from 11 to 12-13 **(verified)**. Each level up
gives each hero one point to spend ("SPEND 1 PTS") **(verified)**.

## 5. Healing and defeat
- The healer charges per hero; with RYZ 4 HP below his maximum and CONDI 1 below, the prices were 4 and 1 Macca:
  1 Macca per missing HP at this level **(verified: `heal`; inferred rate from one sample)**.
- When every hero falls: GAME OVER, "THE WORLD WILL PERISH!" **(verified: `gameover`)**. Inside Devil Buster this
  only ends the computer game and the story continues in the computer room with 0 Macca and 0 MAG **(verified)**.

## Open questions
- Damage formulas, DIA's heal amount, flee chance, what AUTO does.
- What a YES or NO answer changes in negotiation; how demons join; summoning cost in MAG.
