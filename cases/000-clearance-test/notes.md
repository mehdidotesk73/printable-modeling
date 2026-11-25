# Case 000 — Calibration suite (fits, print-in-place motion, snaps × orientation)

## Brief
Measure this printer's real behaviour before designing parts that fit or move.
User asked for: assembly fits, print-in-place rotation, print-in-place translation, snap
connections — each printed both lying and standing, since orientation changes the result.

## Print set (all PLA, default settings, no supports)
| File | What | Read it as |
|---|---|---|
| `A_fit_lying` | plate, holes vertical, gaps 0–0.4 per side | push pin in each hole |
| `A_fit_standing` | wall, holes horizontal, same gaps | same |
| `A_pins_x2` | 10 mm pins (head down) | used with both A plates |
| `B_rotate_lying` / `_standing` | captive axle in housing, gaps 0.2/0.3/0.4/0.5 | twist the axle (slot on top) |
| `C_slide_lying` / `_standing` | captive hex slider in block, same gaps | push slider through |
| `D_snap_lying` / `_standing` | plug with 2 hook arms, hook depth 0.4/0.6/0.8/1.0 | snap into a receiver |
| `D_snap_receivers_x2` | plates with window | — |

Labels engraved on each coupon. For each one record: fused / breaks free with force /
stiff / smooth / loose (motion) and won't go / press / snug-turn / free / sloppy (fits);
snaps: won't engage / engages-holds / engages-releasable / arm broke.

## Design choices (Claude's, not yet taught)
- 0.4 mm relief where a moving part meets another part at the bed (elephant's foot).
- All captive shapes use 45° flanks (diamond collar, hexagon slider) so nothing needs supports.
- In the lying rotation test the axle has nothing under it but the gap: its underside is printed
  over air. That is exactly the weakness of horizontal print-in-place hinges, so it is left in.
- Snap arms 1.6 thick, 13 long, 30° lead-in, square catch. Lying = layers run along the arm
  (expected strong); standing = layers stacked across the arm (expected to snap off).

## Log
- v1: single fit plate (vertical holes only).
- v2 (user): add print-in-place rotation, translation, snaps, and lying vs standing for all.
  → built suite above; verified every moving part is a separate body with exactly the set gap.

## Takeaways

## Seems-to-be

## Open questions
- Pins printed lying (not round underneath) vs standing — worth a test later?
- Are 4 gap steps fine enough, or should a second round narrow in once we see the first result?
