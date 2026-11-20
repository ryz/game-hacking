---
skill: game-scout
project: all games (shared tools at the repo root)
summary: Research a newly registered game (controls, structure, strategy, shortcuts) into its playbook and verify the basics in the emulator.
access: write (games/<platform>/<slug>/ except shots/, work/scout/<slug>/)
updated: 2026-11-19 (parallel variants for quest conditions)
---

# Game scout - research a game before anyone plays it

> **Before you start:** paths are relative to the repo root. Read `docs/emulator/README.md` (how to drive the emulator), the file for the game's platform (`docs/emulator/gb.md`, `nes.md`, `snes.md`, `sms.md`, `md.md`, `dos.md`, `apple2.md` or `amiga.md`) and
> `docs/capture-guide.md` (what the database needs), and the open entries in this skill's `feedback.md`.

Owner's rules (2026-11-15): this is cataloguing, not a fair playthrough, so the most valuable research is
**shortcuts**: completed saves, codes, passwords, debug menus, level selects, RAM maps. Main character name:
**ryz**. Cheated values look realistic (`docs/emulator/README.md`, "Cataloguing, not playing fair").

You turn a ROM nobody has played here into a **playbook** that lets a capture agent play it efficiently: verified
controls and boot route, the game's structure, a shot plan, strategy notes and shortcuts, all with sources. You
do not capture the database set (that is `game-capture`), but you do create the first checkpoints.

## Inputs (from the dispatch)
- Game slug (`games/<platform>/<slug>/game.json` exists: `tools/intake.py` ran) and the ROM in `rom/`.
- Optional: what the owner wants emphasised.

## Steps
1. **Identify.** `game.json` (header title, region, revision, SHA-1/CRC32) + `work/intake/<platform>/<slug>/sheet.png`
   (first 30 s, no input). Pin down the exact game and release: the header title is often abbreviated; match the
   CRC32/SHA-1 against No-Intro naming if a source lists it. Fill the playbook Identity table; set
   `game.json` "title" to the official English title (or the romanised original).
2. **Research** (web search and fetch; prefer primary and specific sources, in this order):
   - The **instruction manual** (scans/transcriptions: controls, modes, menus, items, official names).
   - **GameFAQs** FAQs/walkthroughs (controls, critical path, bosses, passwords/codes), **StrategyWiki**.
   - **The Cutting Room Floor** (tcrf.net): debug menus, level selects, sound tests, unused content, regional
     differences. Often the fastest way to reach late content.
   - **Data Crystal** (datacrystal.tcrf.net): RAM maps, ROM maps.
   - GameShark / Game Genie code lists (GameFAQs "Cheats", gamehacking.org). NES: no GameShark (use `freeze:`), Game Genie rules in `docs/emulator/nes.md`. GB GameShark `01VVAAAA` = write VV
     to address AAAA, low byte first: use as `gs:` tokens; Game Genie codes go into a `rom:` variant.
   - **Saves:** GameFAQs game pages often have a "Saves" section (100% / late-game battery saves). Fetch the
     best one into `rom/saves/<slug>/` if the site serves it directly, test it with the `sav:NAME` prefix, and
     record URL, SHA-1 and contents in the playbook. If it needs a browser, list the URL for the owner.
   - Fan wikis for item/enemy/area names. Wikipedia only for release facts.
   A site that refuses automated access is noted as unavailable; never work around bot protection.
   Record every source in the playbook Sources table (URL, what you took, date). Take facts, not prose: no copied
   walkthrough text beyond short quotes of names.
3. **Verify in the emulator** (`tools/play.py`, small steps, look at every screenshot):
   - The boot route to the title and to first control: write macros `TITLE`, `NEWGAME` (and others you need)
     into `game.json` "macros"; checkpoints `title` and `start` (`play.py checkpoint`).
   - Every control in the table: mark **verified** with the context, or note where the source is wrong.
   - Input timing: does the default press (hold 8, wait 40) work in menus and in play? Adjust `game.json`
     "press" if not, and write the symptom in Emulation notes.
   - 2-4 RAM addresses that make capture easier (lives/health, money, stage, position): from the sources, else
     `play.py find`. Confirm each with a poke; add them to `game.json` "ram" and the RAM map.
   - Shortcuts from the sources (passwords, level select, debug menu): try them; mark verified/failed.
   - Macros: run every macro once as a single `do` from power-on (or with `emu.py`) before checkpointing: presses
     while a sign, prompt or keyboard is still drawing are lost, and `play.py`'s settles between calls hide it (Wizardry
     II, Might and Magic). Pad name keyboards with a harmless key (delete on an empty name). After editing a macro,
     rebuild the checkpoints whose routes use it.
   - New screen, unclear confirm button: try every button in parallel `emu.py` runs first (Deep Dungeon III confirms
     title menus with Start, everything else with A). Name keyboards may skip blank squares when moving.
   - A quest end or unlock with an unclear condition: test the variants in parallel `emu.py` runs (party size,
     item equipped or carried, item from the event or poked) before decoding code (Wizardry II's "one alone"
     rule in two runs, 2026-11-19).
   - Look cheaply: a small helper in `work/scout/<slug>/` that runs several token groups and tiles the
     screenshots into one image saves a look per step (used by two scouts, 2026-11-17/18).
   - Blocked web sources and a translated game: decode the ROM script (relative search for a known word) for
     names, save mechanics, places and bosses; tag those facts "ROM text".
   - Rebuild every checkpoint once with an empty cache (`work/cache/<platform>/<slug>`) and compare with a cache hit: the
     frames must be identical.
4. **Start the design reference** (`games/<platform>/<slug>/design/README.md`, notation in that file): the Overview and a
   document list for the game's systems, filled with what the research says, tagged **(source)**, plus what you
   verified. The capture agent extends it while playing.
   Once the `start` checkpoint exists, save in the game if it allows it that early and
   `play.py export 01_start "contents"` (if the game cannot save before a long prologue, say so in the playbook and
   leave the export to the capture run's first save point) (`docs/emulator/README.md`, "Saves for the owner").
5. **Plan the shots.** From the structure and `docs/capture-guide.md`: the playbook Shot plan (ids, category,
   what and where), with the systems that make this game distinctive. For each area the plan needs, say how to
   reach it (save, password, code, poke, debug menu, play) and pick the fastest.
6. **Strategy notes.** What a capture agent needs to reach the plan's targets: the critical path, the hard parts
   and how to beat them (patterns, items, levels), which pokes are safe. Short and concrete.
7. Fill the playbook completely (empty sections: "none found" + where you looked). Leave Open questions for
   whatever you could not settle.

## Guardrails
- Write only `games/<platform>/<slug>/game.json`, `playbook.md`, `checkpoints.txt`, `shots.txt` (plan lines without routes
  are fine as comments), `design/`, `tools/` (game-specific helpers), `rom/saves/<slug>/`, `rom/patches/<slug>/` and `work/scout/<slug>/`. Commits: one at the end of a long
  scout, or when the `start` checkpoint and its save exist, with the same rules as game-capture's in-between
  commits (only `games/<platform>/<slug>/`, pull --rebase, push to the branch named in the dispatch); the coordinator makes the final commit.
- Never commit or upload the ROM; never send ROM data, hashes of private dumps or the user's details to web
  services (searching for a public CRC32 of a retail game is fine).
- Mark every fact verified or source. A control or code you could not confirm stays "source".
- Time box: research ~15 min of fetching; verification until boot, controls and the first area work. Deeper
  play is the capture agent's job.

## Report (your final message)
- Playbook path; one-paragraph summary of the game as the database will describe it.
- Verified: boot macros, checkpoints made (names), controls verified / unverified / wrong in sources.
- RAM addresses and shortcuts found (verified or not): saves, codes, passwords, debug features.
- Design reference: documents started, claims by tag.
- Shot plan size by category; areas that need special effort to reach, with the method.
- Sources used (count, best ones) and open questions.

## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/game-scout/feedback.md` and in
`agent-log/YYYY-MM.md`:

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill, the tools or docs/emulator/>
- Proposed rule change: <a concrete change to skill.md or docs/emulator/, or "none">
```
