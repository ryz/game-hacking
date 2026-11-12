"""Regenerate the design data tables from the original ROM (Rev 1) and script/*.json:

  python3 tools/designtables        -> docs/design/items_table.md, docs/design/monsters_table.md

items.py: the 224 item records (bank 40); monsters.py: the 167 monster records (bank 57) + encounter tables.
Field meanings and how they were established: docs/tech/items.md, docs/tech/monsters.md.
"""
import os, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
for name in ("items.py", "monsters.py"):
    runpy.run_path(os.path.join(HERE, name), run_name="__main__")
    print("wrote", name.replace(".py", "_table.md"))
