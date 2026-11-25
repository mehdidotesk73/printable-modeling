# Case 000 — Clearance test (calibration)

## Brief
Measure this printer's real fits for a pin in a hole before designing parts that fit together.
Plate with 7 holes (gap per side 0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4 mm, engraved under each)
plus two identical 10 mm pins with a grip head. PLA, printed flat; pins head-down.

## Design choices (Claude's, not yet taught)
- 0.4 mm chamfer on the bed side of each hole, to offset elephant's foot (first layer squish).
- 0.5 mm chamfer on the pin tip for easy entry.
- Two pins in case one gets stuck in a tight hole.

## How to read it
For each hole, push the pin in by hand and note: won't go / press fit (needs force, stays put)
/ snug turn (turns with resistance) / free spin / sloppy (wobbles). Fill the table in `shop.md`.

## Log
- v1: printed? _pending_

## Takeaways

## Seems-to-be

## Open questions
- Do holes printed upright (in a wall) behave differently from flat ones? Likely; test later if needed.
- Print-in-place gaps (parts printed already assembled) need their own test.
