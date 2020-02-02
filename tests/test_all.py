import os
import io
import sys
import pytest
import crestic


@pytest.fixture
def stdout(monkeypatch):
    mock_stdout = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', mock_stdout)
    return lambda: mock_stdout.getvalue().strip()


@pytest.fixture(autouse=True)
def dryrun(monkeypatch):
    monkeypatch.setitem(os.environ, 'CRESTIC_DRYRUN', '1')
    monkeypatch


@pytest.fixture(autouse=True)
def configfile(monkeypatch):
    monkeypatch.setitem(os.environ, 'CRESTIC_CONFIG_FILE', 'tests/config.ini')


def test_plain(stdout):
    crestic.main(["plain", "backup"])
    assert stdout() == 'restic backup --exclude-file bla ~'


def test_boolean(stdout):
    crestic.main(["boolean", "backup"])
    assert stdout() == 'restic backup --exclude-file bla --quiet ~'


def test_multivals(stdout):
    crestic.main(["multivals", "backup"])
    assert stdout() == 'restic backup --exclude-file bla --exclude config.py --exclude passwords.txt ~'


def test_overloaded(stdout):
    crestic.main(["overloaded", "backup"])
    assert stdout() == 'restic backup --exclude-file overloaded ~'


def test_overloaded2(stdout):
    crestic.main(["overloaded2", "backup"])
    assert stdout() == 'restic backup --exclude-file overloaded2 ~'


def test_overloadedargs(stdout):
    crestic.main(["plain", "backup", "--exclude-file", "foo"])
    assert stdout() == 'restic backup --exclude-file foo ~'


def test_extraargs(stdout):
    crestic.main(["plain", "backup", "--quiet"])
    assert stdout() == 'restic backup --exclude-file bla --quiet ~'
