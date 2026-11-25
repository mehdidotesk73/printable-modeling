"""2D building blocks: cross-section profiles and paths."""
from build123d import (
    Circle, Face, Plane, Polyline, Rectangle, RectangleRounded, Wire, Location,
)


def profile(points, plane=Plane.XY):
    """Closed cross-section from a list of (x, y) points, on `plane`.

    For sweeps, draw the profile in local XY where +X points *outward/sideways*
    from the path and +Y points *up*; `sweep` orients it onto the path for you.
    """
    wire = Wire(Polyline(*points, close=True).edges())
    return plane * Face(wire)


def rect_face(width, height, plane=Plane.XY):
    """Centred rectangle face."""
    return plane * Rectangle(width, height).face()


def circle_face(radius, plane=Plane.XY):
    """Centred circle face."""
    return plane * Circle(radius).face()


def rect_path(width, height, corner_radius=0.0, plane=Plane.XY):
    """Closed rectangular path centred on the origin (e.g. a frame's centreline).

    The path starts at the middle of the bottom edge heading +X, so sweep seams
    land mid-edge rather than in a corner.
    """
    if corner_radius > 0:
        wire = RectangleRounded(width, height, corner_radius).wire()
    else:
        wire = Rectangle(width, height).wire()
    # Re-start the closed wire at the middle of the bottom edge.
    w, h = width / 2, height / 2
    if corner_radius <= 0:
        wire = Wire(Polyline((0, -h), (w, -h), (w, h), (-w, h), (-w, -h), (0, -h)).edges())
    return plane * wire


def polyline_path(points, close=False, plane=Plane.XY):
    """Open or closed path through (x, y) or (x, y, z) points."""
    return plane * Wire(Polyline(*points, close=close).edges())
