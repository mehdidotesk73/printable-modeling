"""Labels: engraved or embossed text."""
from build123d import Align, Plane, Pos, Text, extrude


def text_solid(label, size=4, depth=0.6, x=0, y=0, z=0):
    """Text as a solid sitting on z (cut it to engrave, union it to emboss).

    Keep size >= 4 mm and depth >= 0.4 mm (two layers at 0.2) so it stays legible.
    """
    face = Text(label, font_size=size, align=(Align.CENTER, Align.CENTER))
    return Pos(x, y, z) * extrude(face, amount=depth)
