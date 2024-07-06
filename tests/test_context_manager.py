import pytest
from reader import ContextManager
from schemas import Package
from unittest.mock import patch, mock_open


@pytest.fixture
def context_manager():
    return ContextManager("dummy.txt")


def test_process_line_empty(context_manager):
    assert context_manager.process_line("") is None
    assert context_manager.process_line(" ") is None


def test_process_line_comment(context_manager):
    assert context_manager.process_line("# Hello world") is None


def test_process_line_git_package(context_manager):
    line = "package @ git+https://github.com/user/repo.git@commit"
    result = context_manager.process_line(line)
    assert result == Package(name="package", version="")


def test_process_line_versioned_package(context_manager):
    line = "package==1.0.0"
    result = context_manager.process_line(line)
    assert result == Package(name="package", version="1.0.0")


def test_process_line_unversioned_package(context_manager):
    line = "package"
    result = context_manager.process_line(line)
    assert result == Package(name="package", version="")


def test_read_file_success(context_manager):
    mock_packages = "package1==1.0.0\npackage2\n# comment\npackage3 @ git+https://github.com/user/repo.git@commit"

    with patch("builtins.open", mock_open(read_data=mock_packages)):
        result = context_manager.read_file()

    expected = [
        Package(name="package1", version="1.0.0"),
        Package(name="package2", version=""),
        None,
        Package(name="package3", version=""),
    ]
    assert result == expected


def test_read_file_io_error(context_manager, mocker):
    mocker.patch("builtins.open", side_effect=IOError("Test error"))

    result = context_manager.read_file()
    assert result == []


def test_read_file_empty(context_manager, mocker):
    mock_open = mocker.mock_open(read_data="")
    mocker.patch("builtins.open", mock_open)

    result = context_manager.read_file()
    assert result == []
