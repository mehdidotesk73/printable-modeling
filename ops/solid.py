"""Operations that make or modify solids."""
from build123d import (
    Axis, Plane, Solid, Transition, Vector, chamfer as _chamfer, extrude as _extrude,
    fillet as _fillet, loft as _loft, offset as _offset, revolve as _revolve,
    sweep as _sweep,
)


def extrude(face, distance, both=False):
    """Push a face along its normal by `distance` (both=True: symmetric)."""
    return _extrude(face, amount=distance, both=both)


def revolve(face, axis=Axis.Y, degrees=360):
    """Spin a face around `axis` (lathe-like parts, knobs, bottles)."""
    return _revolve(face, axis=axis, revolution_arc=degrees)


def sweep(profile_face, path, mitered=True):
    """Drag a cross-section along a path (frames, rails, handles, gaskets).

    `profile_face` is drawn in local XY (X = outward from the path, Y = up) and is
    placed perpendicular to the path start automatically. mitered=True gives sharp
    corners (picture frame); False gives rounded corners.
    """
    start = path @ 0
    tangent = (path % 0).normalized()
    up = Vector(0, 0, 1)
    outward = tangent.cross(up)  # right-hand side of travel direction
    # Local frame: X -> outward, Y -> up, normal (Z) -> along the path.
    plane = Plane(origin=start, x_dir=outward, z_dir=tangent)
    # Plane's y = z_dir x x_dir = tangent x outward = up for a horizontal path.
    placed = plane * profile_face
    transition = Transition.RIGHT if mitered else Transition.ROUND
    return _sweep(placed, path=path, transition=transition)


def loft(faces, ruled=False):
    """Blend between cross-sections at different positions (transitions, funnels)."""
    return _loft(list(faces), ruled=ruled)


def union(*parts):
    """Join parts into one."""
    result = parts[0]
    for p in parts[1:]:
        result = result + p
    return result


def cut(part, *tools):
    """Subtract tools from part (holes, pockets, slots)."""
    for t in tools:
        part = part - t
    return part


def intersect(a, b):
    """Keep only the overlap of a and b."""
    return a & b


def fillet(part, radius, edges=None):
    """Round edges (all edges if none given)."""
    return _fillet(edges if edges is not None else part.edges(), radius)


def chamfer(part, length, edges=None):
    """Bevel edges (all edges if none given). Bevels print better than fillets on overhangs."""
    return _chamfer(edges if edges is not None else part.edges(), length)


def shell(part, thickness, open_faces=()):
    """Hollow a solid, leaving walls of `thickness`; listed faces are left open."""
    return _offset(part, amount=-thickness, openings=list(open_faces))
