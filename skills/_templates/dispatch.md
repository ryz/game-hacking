# Dispatch template (coordinator -> subagent)

Agents start cold: they see none of the conversation. Fill every field; leave none implicit.

```
Skill: <name> (agent type <name>)      Project dir: wizardry-empire/
Goal: <one sentence: what "done" means>
Inputs: <exact paths: batch file / state / ROM (+ commit) / sheets / question>
Output: <exact path(s) it may write; "none (report only)" for read-only skills>
Context: <facts it cannot find in the repo: user report text, how to reach the screen, inputs used>
Known issues: <things it must not re-report, with "mention only if worse">
Stop when: <condition, e.g. "after 3 battles" or "once the hang is reproduced and explained">
Report: per skills/<name>/skill.md, ending with the ## Feedback block.
```

Tracer notes go in `wizardry-empire/work/re/<topic>.md` (scratch under `work/re/<topic>/`; "do not patch" still
allows scratch ROM copies there).
