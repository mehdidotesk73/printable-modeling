# printable-modeling

A teaching lab for designing 3D-printable objects with Claude.

**How it works:** you break an object into steps (sketch a cross-section, sweep it,
cut it into printable pieces…). Claude works out what each step needs to contribute to
the final object, makes an attempt, renders a preview, asks questions, and iterates with
you. Everything learned is written down here so it can be reused on the next object.

| Folder / file | What it holds |
|---|---|
| `ops/` | The "buttons": generic CAD operations (build123d, Python) that steps are built from. See `ops/README.md`. |
| `cases/NNN-name/` | One folder per object: your step breakdown, each iteration and why it changed, takeaways, "seems-to-be"s, open questions, and the final script. |
| `patterns/` | Consolidated design knowledge drawn from many cases (clearances, hinges, joints…), each claim marked *observed / emerging / rule* and linked to its cases. |
| `shop.md` | Your printer, materials, slicer and **measured** tolerances. |
| `INDEX.md` | One line per note, so Claude can find the right ones quickly. |
| `CLAUDE.md` | Working rules Claude follows in this repo. |

Setup (Claude does this): `pip install -r requirements.txt`
