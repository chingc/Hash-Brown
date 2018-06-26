"""Fixtures"""

from pathlib import Path

import pytest


@pytest.fixture
def get_file():
    return lambda x: Path(__file__).parent / "test_files" / x
