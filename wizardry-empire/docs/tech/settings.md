# Game settings (Mode Settings) - technical reference

How the game's nine Mode Settings switches work in the Japanese Rev 1 ROM. Traced 2026-11-12 (tracer; notes, scripts,
states and screenshots in `work/re/settings.md`, `work/re/settings/`). Design counterpart:
[../design/settings.md](../design/settings.md). Conventions: [../README.md](../README.md).

## Overview

The Mode Settings screen (モード せってい) holds nine global switches, saved with the game. It opens once, on the
first power-on of a save. After that it is reached from the maze menu (Start) > Settings. Four rows are On/Off
(BGM, Sound, Effects, Pictures) and five are Normal/Mania (Map, Combat, Items, Inn, Save). A new save starts
with everything On/Normal except Inn and Save, which start on Mania. Once Save has been set to Normal it cannot
be set back. Nothing is per character.

## 1. Storage, defaults, screen
Code: screen `2B:454E` (first boot) / `2B:45FE` (maze menu); toggle table `2B:4545`; load `0:2D83`, save `0:2DE1`;
defaults `0:3510-353B`, `2E:5534-554B`; first-boot check `1:6121-6156`.

| Row | JP | Bit | 0 | 1 | New save |
|---|---|---|---|---|---|
| BGM | BGM | `$CB99` b7 | On | Off | On |
| Sound | こうかおん | `$CB99` b6 | On | Off | On |
| Effects | えんしゅつ | `$CB99` b5 | On | Off | On |
| Pictures | めんが | `$CB99` b4 | On | Off | On |
| Map | マップ | `$CB99` b3 | Normal | Mania | Normal |
| Combat | たたかう | `$CB99` b2 | Normal | Mania | Normal |
| Items | アイテム | `$CB99` b1 | Normal | Mania | Normal |
| Inn | やどや | `$CB9A` b7 | Normal | Mania | Mania |
| Save | セーブ | `$CB99` b0 | Normal | Mania | Mania |

- SRAM: `$AFD3` = `$CB99`, `$AFD4` = `$CB9A` (copied at power-on and on every save). A blank save, or a checksum
  error in `$AFD2-$AFE8`, gives `$01`/`$80` (code; emulator: first boot `$CB99=01 $CB9A=80`).
- First boot: shown while `$C5C6` bit 6 (SRAM `$AFD5`) is clear. B leaves, sets the bit and saves
  (`2B:4753-4762`) (emulator).
- Later: maze menu > Settings (`20:4AAE`); there is no town entry (code: byte search of far calls).
- Save lock: the screen offers 9 rows only while the saved Save bit (`$AFD3` b0) is 1. After Save = Normal is
  saved, the Save row cannot be selected (`2B:4702-4728`; emulator: 8 rows, cursor wraps after Inn).

## 2. BGM and Sound
Code: sound driver bank `$1F` via `0:3C78`: `1F:4006` song, `1F:4009` SE.
- BGM Off: the 28 song starts skip the driver call; `$C04A` still records the song (code; emulator: 0 song starts
  in a battle, 2 with BGM On). Switching BGM in the menu stops the music, or restarts the floor song (`2B:478C`).
- Sound Off: the 15 SE starts are skipped: hits, wall bump, doors, chest, temple results (code; emulator: 0 vs 2 SE
  in a battle). No other sound starts an effect.

## 3. Effects
Code: `2F:4000-4021`, effect id `$DD43`, table `2F:54A8`.
Off: every effect animation task ends at once, except id 4 (`22:6C25`, monster picture reload). This removes
the monster shake on party hits (id 1, `32:460A`), the screen flash on monster hits (id 0, `32:4E8A`) and the
spell animations (`24:7722`, `24:7D9C`). Gameplay and messages are unchanged (code; emulator: shake 2→10 px On, none Off).

## 4. Pictures
Code: `20:408F`, `20:40EC`, `20:4370`; wall set `$CBF2`.
On: per-floor stone wall set (table `20:6F76`: 1 or 2 per floor, ×2; +4 on lake squares). Off: wall set 0, a
wireframe of white lines on black (emulator: `$CBF2` `$85` vs `$81`). Monster, town and shop pictures are not affected.

## 5. Map
See [dungeon.md](dungeon.md) §6 (Mania mode: text location and coordinate Teleport). Reader `23:4020`.

## 6. Combat
Code: `22:4CDA`, `32:441E`, `32:44E7`, `32:4256`.
Normal: Fight opens Normal / Aim to hit / Power hit (`$C4FF` = `$0C/$0D/$0E`). Aim to hit: miss threshold −4
(+20 % hit chance), damage ÷2 (min 1). Power hit: threshold +4, damage ×1.25. Ambush (battle command 2,
`$C4FF & $7F` = 2) takes the Aim-to-hit threshold (−4) and the Power-hit damage (×1.25) in both modes (`32:441E-4438`). Mania: Fight is always Normal
(code; emulator: sub-menu only in Normal).

## 7. Items
Code: `22:4EAF`, `22:509B`, `22:5B90-5BA3`.
Normal: the battle Item command opens Use / Equip / Throw (entries per the carried items' battle flags).
Mania: Item = Use only, and the command is hidden when nothing carried is usable (code; emulator: a Fighter
with only equipment has Item → Equip in Normal, no Item in Mania). Outside battle nothing changes.

## 8. Inn
Code: `27:4D9B`; Normal `27:4DCE-4F2B`; Mania `27:4F94` (rooms, [items.md](items.md) §7).
Mania (default): the room menu. Normal: no rooms. A hurt character pays 10 × level and is healed to full; at full
HP the stay is free. Either way the character ages 7 days and gets the night routine (spell refill) and the
level-up check. Not enough gold: no stay (emulator: L5 100→50 G, HP 1→10, +7 days; full HP 0 G, +7 days).

## 9. Save
Code: autosave `0:2739-2762`; commit `2B:4008` (`$A000-$AFF7` → `$B000-$BFF7`); restore at power-on `1:60C3` →
`2B:4000`; maze menu `20:490D-4929`.
- Every power-on copies the backup (`$B000`) over the working save (`$A000`).
- Normal: every autosave (after each battle, End the quest) is also committed to the backup. The maze menu has
  End the quest ("Make it safe to power off" / "Form another party").
- Mania: autosaves in the maze update only `$A000`. The backup is updated in town (entering and leaving the maze,
  Training Grounds), at power-on and on a party wipe. The maze menu has no End the quest.
- Effect (emulator, JP): after a battle in Mania, a power cycle lost the battle's EXP. "Resume the adventure" put
  the party at the maze entrance, as when it entered. In Normal the EXP and position were kept.

## 10. Open questions
- Effect id 4 and the full effect-id list; battle item flags (`22:6FB0`); song names.
- Mania power cycle after a single death (inferred: the death is undone).
