"""Render a build123d shape to a PNG for review on any device.

Usage from Python:  from tools.preview import render; render(part, "out.png")
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

VIEWS = {"iso": (30, -60), "front": (0, -90), "top": (90, -90), "side": (0, 0)}


def _mesh(shape, tol=0.2):
    verts, tris = shape.tessellate(tol)
    v = np.array([(p.X, p.Y, p.Z) for p in verts])
    return v[np.array(tris)]


def render(shapes, path, views=("iso", "front", "top"), title=None):
    """Save one image with a panel per view. `shapes` may be a shape or a list (coloured)."""
    if not isinstance(shapes, (list, tuple)):
        shapes = [shapes]
    colors = ["#c9a227", "#4a90d9", "#d95f4a", "#5ab56a", "#9b6ad9"]
    meshes = [_mesh(s) for s in shapes]
    allv = np.concatenate([m.reshape(-1, 3) for m in meshes])
    lo, hi = allv.min(0), allv.max(0)
    centre, span = (lo + hi) / 2, (hi - lo).max() / 2 or 1

    fig = plt.figure(figsize=(5 * len(views), 5))
    light = np.array([0.4, -0.5, 0.8]) / np.linalg.norm([0.4, -0.5, 0.8])
    for i, view in enumerate(views):
        ax = fig.add_subplot(1, len(views), i + 1, projection="3d")
        for m, c in zip(meshes, colors * 10):
            n = np.cross(m[:, 1] - m[:, 0], m[:, 2] - m[:, 0])
            n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
            shade = 0.45 + 0.55 * np.abs(n @ light)
            base = np.array(matplotlib.colors.to_rgb(c))
            fc = np.clip(shade[:, None] * base, 0, 1)
            ax.add_collection3d(Poly3DCollection(m, facecolors=fc, edgecolor="none"))
        for set_lim, k in ((ax.set_xlim, 0), (ax.set_ylim, 1), (ax.set_zlim, 2)):
            set_lim(centre[k] - span, centre[k] + span)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(*VIEWS[view])
        ax.set_title(view)
        ax.set_axis_off()
    if title:
        fig.suptitle(title)
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return path
