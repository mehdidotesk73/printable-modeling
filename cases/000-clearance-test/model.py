"""Case 000 — clearance test: one plate with holes of increasing gap + loose pins.

Every pin is the same 10 mm diameter; each hole is 10 mm + 2 x gap. Try the pin in
each hole and record which gap gives which kind of fit in shop.md.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from build123d import Axis, GeomType  # noqa: E402
from ops import *  # noqa: E402,F403
from tools.preview import render  # noqa: E402

OUT = Path(__file__).parent / "out"

PIN_D = 10.0
GAPS = [0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4]  # per side, mm
PITCH = 18.0
PLATE_T = 6.0
FOOT_CHAMFER = 0.4  # counters elephant's foot on the bed side of holes


def plate():
    length = PITCH * len(GAPS) + 6
    centre = PITCH * (len(GAPS) - 1) / 2
    body = move(extrude(rect_face(length, 32), PLATE_T), x=centre)
    for i, gap in enumerate(GAPS):
        x = i * PITCH
        hole = move(extrude(circle_face(PIN_D / 2 + gap), PLATE_T), x=x, y=5)
        body = cut(body, hole)
        label = text_solid(f"{gap:g}", size=4.5, depth=0.6, x=x, y=-10, z=PLATE_T - 0.6)
        body = cut(body, label)
    bottom_circles = (
        body.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[0]
    )
    return chamfer(body, FOOT_CHAMFER, bottom_circles)


def pin():
    """Head-down pin: 16 mm head, 10 mm shaft, chamfered tip."""
    head = extrude(circle_face(8), 3)
    shaft = move(extrude(circle_face(PIN_D / 2), 10), z=3)
    p = union(head, shaft)
    tip = p.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-1]
    return chamfer(p, 0.5, [tip])


if __name__ == "__main__":
    pl, pn = plate(), pin()
    export(pl, OUT / "clearance_plate.stl")
    export(pn, OUT / "clearance_pin.stl")
    pins_preview = [move(pn, x=30 * k, y=-45) for k in range(2)]
    render([pl, *pins_preview], OUT / "preview.png", title="Clearance test (print 1 plate + 2 pins)")
    print("plate", bbox_size(pl), "pin", bbox_size(pn))
