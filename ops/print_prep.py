"""Getting parts ready to print: splitting, size checks, export."""
from pathlib import Path

from build123d import Keep, Plane, export_step, export_stl, split as _split


def split(part, plane):
    """Cut a part in two along `plane`; returns (below, above) relative to its normal.

    Joints (dovetails, pins, slide fits) are added by separate ops on the halves.
    """
    below = _split(part, bisect_by=plane, keep=Keep.BOTTOM)
    above = _split(part, bisect_by=plane, keep=Keep.TOP)
    return below, above


def bbox_size(part):
    """(x, y, z) extents in mm."""
    bb = part.bounding_box()
    return (bb.size.X, bb.size.Y, bb.size.Z)


def fits_bed(part, bed=(256, 256, 256)):
    """True if the part's bounding box fits the bed in its current orientation."""
    return all(s <= b for s, b in zip(bbox_size(part), bed))


def export(part, path):
    """Write .stl (for slicer) or .step (for other CAD) based on extension."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".step":
        export_step(part, str(path))
    else:
        export_stl(part, str(path))
    return path
