"""Generic CAD operations ("buttons") that design steps are strung together from.

All units are millimetres. Every function returns build123d objects so results can
be fed into the next operation. See ops/README.md for the catalogue.
"""
from .sketch import profile, rect_path, polyline_path, circle_face, rect_face
from .solid import extrude, revolve, sweep, loft, union, cut, intersect, fillet, chamfer, shell
from .arrange import move, rotate, mirror, linear_pattern, polar_pattern
from .text import text_solid
from .print_prep import split, bbox_size, fits_bed, export

__all__ = [
    "profile", "rect_path", "polyline_path", "circle_face", "rect_face",
    "extrude", "revolve", "sweep", "loft", "union", "cut", "intersect",
    "fillet", "chamfer", "shell",
    "move", "rotate", "mirror", "linear_pattern", "polar_pattern",
    "text_solid",
    "split", "bbox_size", "fits_bed", "export",
]
