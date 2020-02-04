import os
import io
import sys
import subprocess

import pytest
import crestic

import builtins


@pytest.fixture(autouse=True)
def mock_call(mocker):
    mocker.patch('subprocess.call')
    mocker.patch('sys.exit')


@pytest.fixture
def mock_print(mocker):
    mocker.patch('builtins.print')


@pytest.fixture(autouse=True)
def configfile(monkeypatch):
    monkeypatch.setitem(os.environ, 'CRESTIC_CONFIG_FILE', 'tests/config.ini')


def test_plain():
    crestic.main(["plain", "backup"])
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla ~',
        env=os.environ,
        shell=True
    )


def test_boolean():
    crestic.main(["boolean", "backup"])
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla --quiet ~',
        env=os.environ,
        shell=True
    )


def test_multivals():
    crestic.main(["multivals", "backup"])
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla --exclude config.py --exclude passwords.txt ~',
        env=os.environ,
        shell=True
    )


def test_overloaded():
    crestic.main(["overloaded", "backup"])
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file overloaded ~',
        env=os.environ,
        shell=True
    )


def test_overloaded2():
    crestic.main(["overloaded2", "backup"])
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file overloaded2 ~',
        env=os.environ,
        shell=True
    )


def test_overloadedargs():
    crestic.main(["plain", "backup", "--exclude-file", "foo"])
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file foo ~',
        env=os.environ,
        shell=True
    )


def test_extraargs():
    crestic.main(["plain", "backup", "--quiet"])
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla --quiet ~',
        env=os.environ,
        shell=True
    )


def test_environ():
    crestic.main(["environ", "backup"])

    environ = dict(os.environ)
    environ.update({
        'B2_ACCOUNT_ID': 'testid',
        'B2_ACCOUNT_KEY': 'testkey',
    })

    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla ~',
        env=environ,
        shell=True
    )


def test_dryrun(mock_print):
    os.environ['CRESTIC_DRYRUN'] = "1"

    crestic.main(["environ", "backup"])

    subprocess.call.assert_not_called()
    builtins.print.assert_called_with(
        'restic backup --exclude-file bla ~'
    )
    sys.exit.assert_called_once_with(1)
