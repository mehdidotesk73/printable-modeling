"""Case NNN — <object>. Regenerates the final part(s) from scratch."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ops import *  # noqa: E402,F403

OUT = Path(__file__).parent / "out"
