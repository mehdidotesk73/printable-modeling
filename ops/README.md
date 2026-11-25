# Operations catalogue ("buttons")

Each step of a design is one or more of these. All in `ops/`, units in mm.

| Button | Function | Typical use |
|---|---|---|
| Sketch profile | `profile(points)` | Cross-section for sweep/extrude/revolve |
| Rectangle / circle | `rect_face`, `circle_face` | Simple sections, holes |
| Path | `rect_path(w, h, corner_radius)`, `polyline_path(points)` | Sweep paths (frame centreline, rails) |
| Extrude | `extrude(face, d)` | Plates, walls, pegs |
| Revolve | `revolve(face, axis, degrees)` | Knobs, round containers |
| Sweep | `sweep(profile, path, mitered=True)` | Frames, handles, edge trims |
| Loft | `loft([faces])` | Transitions between shapes |
| Boolean | `union`, `cut`, `intersect` | Combine, holes, pockets |
| Round / bevel | `fillet`, `chamfer` | Edge finishing (chamfers print better on overhangs) |
| Shell | `shell(part, t, open_faces)` | Boxes, hollow parts |
| Move / rotate / mirror | `move`, `rotate`, `mirror` | Positioning, symmetric parts |
| Pattern | `linear_pattern`, `polar_pattern` | Repeated features |
| Split for print | `split(part, plane)` | Cutting into bed-sized pieces |
| Size check | `bbox_size`, `fits_bed` | Will it fit the printer? |
| Export | `export(part, "x.stl" / "x.step")` | Files for slicer / other CAD |
| Preview | `tools/preview.py: render(parts, png)` | Images to review on phone |

**Profile convention for sweeps:** draw in local XY with X pointing *outward* from the
path and Y pointing *up*; `sweep` places it on the path.

Missing so far (to add when a case needs it): joints for split pieces (slide/dovetail/pin),
hinges, text/embossing, threads.
