import pytest
from reader import ContextManager
from schemas import Package
from unittest.mock import patch, mock_open


@pytest.fixture
def context_manager():
    return ContextManager("dummy.txt")


def test_read_file_success(context_manager):
    mock_packages = "package1==1.0.0\npackage2\n# Comment\npackage3==2.1.0\n"

    with patch("builtins.open", mock_open(read_data=mock_packages)):
        result = context_manager.read_file()

    assert len(result) == 4
    assert result[0] == Package(name="package1", version="1.0.0")
    assert result[1] == Package(name="package2")
    assert result[2] is None
    assert result[3] == Package(name="package3", version="2.1.0")
