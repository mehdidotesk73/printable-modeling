"""Positioning and repetition."""
from build123d import Axis, Location, Plane, Pos, Rot, mirror as _mirror


def move(part, x=0, y=0, z=0):
    return Pos(x, y, z) * part


def rotate(part, x=0, y=0, z=0):
    """Rotate by degrees about the X, Y, Z axes."""
    return Rot(x, y, z) * part


def mirror(part, plane=Plane.YZ, keep_original=True):
    m = _mirror(part, about=plane)
    return part + m if keep_original else m


def linear_pattern(part, count, dx=0, dy=0, dz=0):
    """`count` copies, each shifted by (dx, dy, dz) from the previous."""
    result = part
    for i in range(1, count):
        result = result + Pos(dx * i, dy * i, dz * i) * part
    return result


def polar_pattern(part, count, axis_degrees=360):
    """`count` copies rotated evenly around Z."""
    result = part
    for i in range(1, count):
        result = result + Rot(0, 0, axis_degrees * i / count) * part
    return result
