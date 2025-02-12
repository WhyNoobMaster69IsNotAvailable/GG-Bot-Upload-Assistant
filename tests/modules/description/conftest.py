from pathlib import Path

import pytest

working_folder = Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope="module")
def working_folder_path():
    yield f"{str(working_folder)}/resources"
