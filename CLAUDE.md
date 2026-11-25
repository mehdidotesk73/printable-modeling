# Working rules for Claude in this repo

The user teaches 3D-for-printing design by breaking objects into steps. They are
low-code: they guide decisions and methods, Claude writes all code and notes.

## Division of labour
- The user teaches the workflow (steps, order, intent, corrections). They never debug code.
- Claude owns `ops/`: keeps every function working, tested (`tests/`), and fixes it silently
  when a case exposes a bug. A tooling fix is not a design lesson; don't ask the user about it.

## Before designing anything
1. Read `INDEX.md`, `shop.md`, then the 3–5 most relevant `cases/` and `patterns/` notes.
2. Apply `rule` patterns by default; mention `emerging`/`observed` ones as suggestions.

## During a case (`cases/NNN-name/`, copy `cases/_template/`)
- Work one step at a time. For each step: say what it must achieve for the final object,
  ask only the questions that block it, make an attempt, render a preview
  (`tools/preview.py`), and iterate until the user approves the step.
- Log every iteration in the case's `notes.md` as you go: what changed and *why*
  (especially the user's corrections — those are the lessons).
- Keep three running lists: **Takeaways**, **Seems-to-be** (unconfirmed hunches),
  **Open questions**. Record conditions (material, printer, orientation) with every number.
- The case's `model.py` must regenerate the final part(s) from scratch.
- Every iteration exports STL(s) to `cases/NNN-name/out/` (committed, so the user can open
  them on GitHub's 3D viewer or download them) and sends them plus a preview PNG to the user.
- Build geometry from `ops/` functions. If a step needs an operation that doesn't exist,
  add it to `ops/` (with docstring) and to `ops/README.md`.

## Consolidation (only when the user says "consolidate")
- Read all cases; propose changes to `patterns/` as a diff summary *before* writing.
- Each claim: status (`observed` = 1 case, `emerging` = 2+ cases, `rule` = user confirmed)
  plus links to supporting cases. Contradictions become open questions, never averages.
- Patterns are gradual: promote status only on evidence; keep the caveats.

## Always
- Update `INDEX.md` when adding or renaming a note.
- Never invent tolerance values as facts: use `shop.md`, or label them "starting guess".
- Units are millimetres.
