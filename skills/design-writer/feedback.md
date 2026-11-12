---
skill: design-writer
---

# Feedback - design-writer

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-12 - floor pages 23-30
- Task: floor pages 23-30 from the floormap data, monsters_table and the dungeon/spells/findings docs.
- Worked: scripts over floormap.floor_cells for doors, connected parts and zone/trap counts; monster tables
  generated from monsters_table rows; scripted coordinate and number checks.
- Friction: shared session scratchpad overwritten by other writers; generated table hid repeated formations;
  dungeon.md section 8 and findings disagreed with the data; "plain E markers" ambiguous next to E1.
- Proposed rule change: private scratch subfolders; "parts that connect on foot" only with the stated method and a
  tag; generator shows formation weights.
- Corrected: weights now "(2 of 4)" in monsters_table; dungeon/findings fixed (zones, floor 26 traps, floor 24
  hidden spot, levels 21-30, findings 22). Its "closed pockets" assumed special walls are walls: they are secret or
  locked doors (traced and verified afterwards), so a revision round redoes them.
- Status: promoted 2026-11-12 (scratch folders, floormap --list data, fixed tables, walking-fact rule)

### 2026-11-12 - floor pages 16-22
- Task: floor pages 16-22.
- Worked: walking-graph script with the verified one-way rule (floor 20 spiral, floor 21 pocket); monster tables by
  script; check that every special square and one-way door appears on the page.
- Friction: scratchpad overwritten by another writer; four different table layouts across the round; docs said
  "level 20-30" and "panels on floors 3-7"; shared guard marks untraced.
- Proposed rule change: private scratch folders; coordinator fixes table layout before dispatch; walking facts
  tagged with how special walls were counted; guard-only areas linked to the floor that owns them.
- Corrected: dungeon.md fixed (panels 3-19, levels, zones); layout fixed in the revision dispatch.
- Status: promoted 2026-11-12

### 2026-11-12 - floor pages 9-15
- Task: floor pages 9-15.
- Worked: floor txt plus floor_events.txt; tables by script; reachability calculation found closed areas.
- Friction: reachability not in the dispatch; encounter table hid repeated formations; floor-01's door count method
  unstated; shared scratchpad overwritten.
- Proposed rule change: `floormap.py --reach`; define door counting in maps/README; generator shows "F146 ×2";
  private scratch folders.
- Corrected: floormap --list prints doors, shared guard marks and on-foot reach; floor-01 door count fixed (18 +
  3 one-way, verified by script); key-hole "item id" doubt kept as an open question.
- Status: promoted 2026-11-12

### 2026-11-12 - floor pages 2-8
- Task: floor pages 2-8.
- Worked: monster rows by script (0 mismatches); reachability script found walled-in chute (floor 6, verified by
  the coordinator from the data) and the floor 3/4 zig-zag.
- Friction: floor txt lacked door counts and wall data; derived facts not in tech; generator Enc/Floors columns
  disagreed with the formation display (Ghast); parallel round not announced.
- Proposed rule change: standard "Route (computed)" bullet with a shared script; richer --list; announce parallel
  rounds.
- Corrected: generator fixed (same group-size rule for both columns; Ghast, Iron Golem, High Ninja, Death Knight
  floors corrected); --list extended.
- Status: promoted 2026-11-12

### 2026-11-12 - revision round 1: dungeon.md + findings.md
- Task: apply review-1 and the tracer's verdicts to dungeon and findings.
- Worked: read review, tracer notes and tech before writing; scripted number and coordinate checks; doclinks run on
  a copy with the unsaved findings in place.
- Friction: findings.md refused by name again; numbering findings renamed every anchor; floor-1 moved mid-run;
  engineering grep hits link targets and item names.
- Proposed rule change: pre-create/whitelist findings.md or rename; state numbering; grep skips link targets.
- Corrected: coordinator saved findings.md (35 entries) and fixed maps/README's anchor; tech fixes applied
  (golem mark, chest rows 30-48 start at 1, verified in the ROM).
- Status: promoted 2026-11-12 (grep scope, parallel links, findings saved by coordinator - skill + coordinator)

### 2026-11-12 - revision round 1: combat.md + monsters.md
- Task: apply review-1 and the tracer's verdicts to combat and monsters.
- Worked: bestiary numbers recounted by script (caught: first level drainer is the Wight); cell-by-cell checks of
  trimmed table rows; tech answered most 'unclear' points.
- Friction: findings/dungeon renumbered mid-run; 'record' grep hits tech anchors; a tech number (lowest AC −16)
  contradicted the table.
- Proposed rule change: freeze findings headings before parallel rounds; grep skips link targets; re-derive
  'against every monster' claims from table extremes.
- Corrected: tech items.md lowest AC fixed (−30) with the to-hit ≤ 18 condition; rules promoted.
- Status: promoted 2026-11-12

### 2026-11-12 - revision round 1: characters.md + spells.md
- Task: apply review-1 and the tracer's verdicts to characters and spells.
- Worked: spell rows converted and re-checked by script; circle table checked against two tech tables; kept the
  headings others link to.
- Friction: banned-word list hits an item name and a tech anchor; a review item asked for '(data)' that the README
  now forbids and the tracer had overtaken; other files renumbered mid-run.
- Proposed rule change: exempt item names and link targets from the grep; coordinator marks overtaken review items;
  link without anchors during parallel rounds.
- Corrected: all applied; coordinator skill gained 'Parallel documentation rounds'.
- Status: promoted 2026-11-12

### 2026-11-12 - revision round 1: items.md + town.md
- Task: apply review-1 and the tracer's verdicts to items and town.
- Worked: review items with line numbers applied mechanically; scripted number check (caught a missing source);
  items_table parsed to answer Range '-' and find the Swings+ contradiction.
- Friction: combat/dungeon renumbered mid-run; 'record' grep hits; README says to ignore roll unevenness while the
  dispatch asked for exact odds; findings had no entry for a linked quirk.
- Proposed rule change: check findings has the entry before linking; grep exceptions; coordinator fixes headings first.
- Corrected: tech dagger swings (+1 to +6) and VIT loss (61 of 101) fixed; rules promoted.
- Status: promoted 2026-11-12

### 2026-11-12 - dungeon.md + findings.md
- Task: dungeon and findings from tech dungeon/items §10/monsters §2,§8, re/reach, re/debug-mode, all tech for quirks.
- Worked: sources.md first with a contradictions section (5 found); chest quality per floor computed from the
  generated table with the method stated; anchor check by script.
- Friction: the harness refused to save findings.md (file name); tech headings with addresses; tech docs disagree;
  'chest value by floor' had no tech source.
- Proposed rule change: return refused files in the report; contradictions list in sources.md; no addresses in
  tech headings.
- Corrected: findings.md saved by the coordinator (door encounter rate retagged data); tech headings cleaned
  (40 headings, 84 links); all three rules promoted.
- Status: promoted 2026-11-12

### 2026-11-12 - combat.md + monsters.md
- Task: combat and monsters from tech monsters.md, items.md §4/§9, characters.md §9.
- Worked: sources list before drafting; scripted anchors/link check; bestiary counts from the generated table.
- Friction: parallel writers (overlaps visible only at the end); findings.md anchors unknown; tech facts vs tables
  (swings 1-7, guarded 3-21); the dispatch overstated one confidence (door rate).
- Proposed rule change: script link check, link findings.md without anchors unless it exists; tables win over
  tech prose; coordinator fixes findings headings in advance for parallel runs.
- Corrected: coordinator slip (door rate) fixed in findings.md; dungeon.md overlap cut to a link; rules promoted.
- Status: promoted 2026-11-12

### 2026-11-12 - items.md + town.md
- Task: items and town from tech items.md §1-3,5-9 and characters.md §7-9.
- Worked: sources list then a number-matching script (caught 2 missing sources); slug anchor checker; parser over
  items_table (caught a wrong claim: 17 of 36 cursed items drain HP).
- Friction: other writers' files appeared mid-run; tech headings with addresses; dispatch omitted some needed tech
  sections (characters §3.5, §5.2, §5.4, §6.2, monsters §7).
- Proposed rule change: re-list docs/design before the final check and cut overlaps; scripted number and anchor
  checks.
- Corrected: generated table 'Lv' in the Use column renamed 'mode N'; rules promoted.
- Status: promoted 2026-11-12

### 2026-11-12 - characters.md + spells.md
- Task: characters and spells from tech characters.md, monsters.md §8, items.md parts.
- Worked: the 125-row spell table generated by script from the tech table; scripted number check; the ownership map.
- Friction: tech headings with addresses; tech docs disagree (pacts, aging, an EXP column); no report slot for
  contradictions; spell effects untraced (effect column dropped).
- Proposed rule change: address-free tech headings; check links both ways; 'Contradictions' section in the report.
- Corrected: tech Human max-stat example fixed; headings cleaned; contradictions batched for a tracer.
- Status: promoted 2026-11-12
