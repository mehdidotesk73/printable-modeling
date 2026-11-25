"""Labels: engraved text on any flat face."""
from build123d import Align, Plane, Text, Vector, extrude

_FACING = {
    "+Z": ((1, 0, 0), (0, 0, 1)),
    "-Z": ((-1, 0, 0), (0, 0, -1)),
    "+Y": ((-1, 0, 0), (0, 1, 0)),
    "-Y": ((1, 0, 0), (0, -1, 0)),
    "+X": ((0, 1, 0), (1, 0, 0)),
    "-X": ((0, -1, 0), (-1, 0, 0)),
}


def text_solid(label, size=4, depth=0.6, at=(0, 0, 0), facing="+Z"):
    """Text solid that sinks `depth` into a face whose outward normal is `facing`.

    `at` is the centre of the label on the face surface. Text reads upright when the
    face is viewed from outside. Keep size >= 3.5 mm and depth >= 0.4 mm to stay legible.
    """
    x_dir, normal = _FACING[facing]
    n = Vector(*normal)
    origin = Vector(*at) - n * depth
    plane = Plane(origin=origin, x_dir=x_dir, z_dir=normal)
    face = Text(label, font_size=size, align=(Align.CENTER, Align.CENTER))
    return extrude(plane * face, amount=depth + 0.05)


def engrave(part, label, at, facing="+Z", size=4, depth=0.6):
    """Cut a text label into a face of `part`."""
    return part - text_solid(label, size, depth, at, facing)
