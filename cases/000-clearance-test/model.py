"""Case 000 — calibration suite. Each test is printed lying (L) and standing (S).

  A. fit_*      pin-in-hole fits for separately printed parts (holes vertical vs horizontal)
  B. rotate_*   print-in-place axle in a housing (rotation), 4 gaps
  C. slide_*    print-in-place slider in a channel (translation), 4 gaps
  D. snap_*     cantilever snap hooks, 4 hook depths, + receivers

Run:  python cases/000-clearance-test/model.py   -> out/*.stl and out/*.png
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from build123d import Axis, GeomType, Plane  # noqa: E402
from ops import *  # noqa: E402,F403
from tools.preview import render  # noqa: E402

OUT = Path(__file__).parent / "out"
FOOT = 0.4  # elephant's-foot relief at the bed (first layer spreads)

# ---------------------------------------------------------------- A. fits
PIN_D = 10.0
FIT_GAPS = [0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4]
PITCH = 18.0


def fit_lying():
    """Plate printed flat: holes run vertically (round, accurate)."""
    t = 6.0
    length = PITCH * len(FIT_GAPS) + 6
    body = move(extrude(rect_face(length, 32), t), x=PITCH * (len(FIT_GAPS) - 1) / 2)
    for i, g in enumerate(FIT_GAPS):
        body = cut(body, move(extrude(circle_face(PIN_D / 2 + g), t), x=i * PITCH, y=5))
        body = engrave(body, f"{g:g}", at=(i * PITCH, -10, t), size=4.5)
    bottom = body.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[0]
    return chamfer(body, FOOT, bottom)


def fit_standing():
    """Wall printed upright: holes run horizontally (top of each hole is an overhang)."""
    t, h, zc = 8.0, 28.0, 17.0
    length = PITCH * len(FIT_GAPS) + 6
    body = move(extrude(rect_face(length, t), h), x=PITCH * (len(FIT_GAPS) - 1) / 2)
    for i, g in enumerate(FIT_GAPS):
        hole = extrude(circle_face(PIN_D / 2 + g, Plane.XZ), t / 2, both=True)
        body = cut(body, move(hole, x=i * PITCH, z=zc))
        body = engrave(body, f"{g:g}", at=(i * PITCH, -t / 2, 5), facing="-Y", size=4.5)
    return body


def pin():
    """Head-down pin: 16 mm head, 10 mm shaft, chamfered tip. Print 2."""
    p = union(extrude(circle_face(8), 3), move(extrude(circle_face(PIN_D / 2), 12), z=3))
    tip = p.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-1]
    return chamfer(p, 0.5, [tip])


# ------------------------------------------------- B. print-in-place rotation
PIP_GAPS = [0.2, 0.3, 0.4, 0.5]


def _axle_profiles(gap):
    """Half cross-sections (r, z) of axle and of the cavity around it.

    The axle has a 45-degree 'diamond' collar that locks it in the housing; every
    surface is <= 45 degrees so nothing needs support.
    """
    shape = [(4, 3.5), (6.5, 6), (4, 8.5), (4, 16), (0, 16), (0, 0)]
    axle = profile([(0, 0), (4 - FOOT, 0), (4, FOOT), *shape[:-2], (0, 16)], Plane.XZ)
    solid_axle = profile([(0, -1), (4, -1), *shape[:-2], (0, 16)], Plane.XZ)
    cavity = grow(solid_axle, gap)
    keep = rect_face(20, 30, Plane.XZ)
    cavity = cavity & move(keep, x=10, z=5)  # only r >= 0 can be revolved
    relief = profile([(0, -1), (4 + gap + FOOT, -1), (4 + gap + FOOT, 0), (4 + gap, FOOT), (0, FOOT)], Plane.XZ)
    return axle, cavity + relief


def rotate_coupon(gap, standing_axis):
    """Housing 26x18x12 with a captive axle. standing_axis=True: axle vertical."""
    axle_f, cavity_f = _axle_profiles(gap)
    axle = revolve(axle_f, Axis.Z)
    axle = cut(axle, move(extrude(rect_face(9, 1.2), 1.5), z=16 - 1.5))  # grip slot
    housing = move(extrude(rect_face(26, 18), 12), x=4)
    housing = cut(housing, revolve(cavity_f, Axis.Z))
    if standing_axis:
        housing = engrave(housing, f"{gap:g}", at=(13, 0, 12), size=4, depth=0.5)
        return union(housing, axle)
    housing = engrave(housing, f"{gap:g}", at=(13, -9, 6), facing="-Y", size=4, depth=0.5)
    return drop_to_bed(rotate(union(housing, axle), x=-90))


# ---------------------------------------------- C. print-in-place translation
def _hexagon(dy=0.0, bottom=0.0):
    return [(-3, bottom), (3, bottom), (6, 3), (3, 6), (-3, 6), (-6, 3)]


def slide_coupon(gap, standing_axis):
    """Block 20 long with a captive hexagonal slider (45-degree flanks).

    Lying: slider travels along the bed. Standing: slider travels up/down.
    """
    plane = Plane.YZ  # profile drawn in (y, z), extruded along +X (travel)
    slider_pts = [(-3 + FOOT, 0), (3 - FOOT, 0), (3, FOOT), (6, 3), (3, 6), (-3, 6), (-6, 3), (-3, FOOT)]
    slider_f = profile(slider_pts, plane)
    cavity = grow(profile([(-3, -1), (3, -1), (6, 3), (3, 6), (-3, 6), (-6, 3)], plane), gap)
    relief = profile([(-3 - gap - FOOT, -1), (3 + gap + FOOT, -1), (3 + gap + FOOT, 0),
                      (3 + gap, FOOT), (-3 - gap, FOOT), (-3 - gap - FOOT, 0)], plane)
    block = extrude(rect_face(20, 10, plane), 20)
    block = move(block, z=5)
    block = cut(block, extrude(cavity + relief, 20))
    if standing_axis:
        slider = extrude(slider_f, 30)  # flush with the block at the bed end
        slider = chamfer(slider, FOOT, slider.faces().sort_by(Axis.X)[0].edges())
        block = engrave(block, f"{gap:g}", at=(10, 0, 10), size=4, depth=0.5)
        return drop_to_bed(rotate(union(block, slider), y=-90))
    slider = move(extrude(slider_f, 34), x=-7)
    block = engrave(block, f"{gap:g}", at=(10, 0, 10), size=4, depth=0.5)
    return union(block, slider)


# ----------------------------------------------------------- D. snap fits
SNAP_DEPTHS = [0.4, 0.6, 0.8, 1.0]  # how far each hook sticks out (interference)
ARM_T, ARM_W, ARM_L = 1.6, 6.0, 13.0
HOLE_W = 10.0  # distance across the outside of the two arms
RECV_T = 4.0
BASE_T = 5.0


def snap_plug(depth, lying):
    """Base + two flexing arms with hooks. Lying = arms flat on bed (strong layers)."""
    plane = Plane.XZ  # side view: x across arms, z up the arms
    zb = BASE_T + RECV_T + 0.3  # retention face sits just above the receiver plate
    ramp = depth / 0.577  # 30-degree lead-in
    half = HOLE_W / 2
    arm = [(half - ARM_T, BASE_T), (half, BASE_T), (half, zb), (half + depth, zb),
           (half, zb + ramp), (half, BASE_T + ARM_L), (half - ARM_T, BASE_T + ARM_L)]
    right = profile(arm, plane)
    arms = extrude(right, ARM_W / 2, both=True)
    arms = mirror(arms, Plane.YZ)
    base = move(extrude(rect_face(24, ARM_W), BASE_T), z=0)
    plug = union(base, arms)
    plug = engrave(plug, f"{depth:g}", at=(-8.5, -ARM_W / 2, BASE_T / 2), facing="-Y", size=3.5, depth=0.5)
    if lying:
        return drop_to_bed(rotate(plug, x=90))
    return plug


def snap_receiver():
    """Plate with a window the plug snaps through. Print flat, 2 copies."""
    c = 0.25
    plate = extrude(rect_face(26, 16), RECV_T)
    plate = cut(plate, extrude(rect_face(HOLE_W + 2 * c, ARM_W + 2 * c), RECV_T))
    return plate


# ----------------------------------------------------------------- build
def build():
    sets = {
        "A_fit_lying": [fit_lying()],
        "A_fit_standing": [fit_standing()],
        "A_pins_x2": row([pin(), pin()]),
        "B_rotate_lying": row([rotate_coupon(g, False) for g in PIP_GAPS]),
        "B_rotate_standing": row([rotate_coupon(g, True) for g in PIP_GAPS]),
        "C_slide_lying": row([slide_coupon(g, False) for g in PIP_GAPS]),
        "C_slide_standing": row([slide_coupon(g, True) for g in PIP_GAPS]),
        "D_snap_lying": row([snap_plug(d, True) for d in SNAP_DEPTHS]),
        "D_snap_standing": row([snap_plug(d, False) for d in SNAP_DEPTHS]),
        "D_snap_receivers_x2": row([snap_receiver(), snap_receiver()]),
    }
    for name, parts in sets.items():
        export(union(*parts) if len(parts) > 1 else parts[0], OUT / f"{name}.stl")
        render(parts, OUT / f"{name}.png", title=name)
        print(name, [tuple(round(v, 1) for v in bbox_size(p)) for p in parts[:1]])
    return sets


if __name__ == "__main__":
    build()
