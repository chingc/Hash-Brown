"""Allow tests to discover the modules."""

import sys
from pathlib import Path


_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "hb"))
