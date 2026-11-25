"""Smoke tests: each op produces a valid solid. Run: python -m pytest tests"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build123d import Axis, Plane  # noqa: E402
from ops import *  # noqa: E402,F403


def frame():
    # L-shaped section: 20 wide, 10 tall, with a 5x4 rebate for the picture.
    sec = profile([(0, 0), (20, 0), (20, 10), (5, 10), (5, 6), (0, 6)])
    return sweep(sec, rect_path(150, 100))


def test_sweep_frame_is_closed_solid():
    f = frame()
    assert f.is_valid and len(f.solids()) == 1
    x, y, z = bbox_size(f)
    assert abs(x - 190) < 0.5 and abs(y - 140) < 0.5 and abs(z - 10) < 0.5


def test_split_gives_two_halves():
    a, b = split(frame(), Plane.YZ)
    assert a.volume > 0 and b.volume > 0
    assert abs(a.volume + b.volume - frame().volume) < 1


def test_basic_solids():
    box = extrude(rect_face(20, 10), 5)
    assert abs(box.volume - 1000) < 1e-6
    holed = cut(box, extrude(circle_face(2), 5))
    assert holed.volume < box.volume
    assert revolve(profile([(5, 0), (8, 0), (8, 10), (5, 10)], Plane.XZ), Axis.Z).volume > 0
    assert shell(box, 1, [box.faces().sort_by(Axis.Z)[-1]]).volume < box.volume
    assert len(linear_pattern(box, 3, dx=30).solids()) == 3


def test_engraved_text():
    plate = extrude(rect_face(30, 10), 3)
    engraved = engrave(plate, "0.2", at=(0, 0, 3), size=5)
    assert engraved.is_valid and engraved.volume < plate.volume
