"""Fixtures"""

from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture  # type: ignore
def get_file() -> Callable[[str], str]:
    return lambda x: str(Path(__file__).parent / "test_files" / x)
