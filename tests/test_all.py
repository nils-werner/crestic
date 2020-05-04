import os
import io
import sys
import subprocess

import pytest
import crestic

import builtins


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    try:
        monkeypatch.delitem(os.environ, 'CRESTIC_CONFIG_FILE')
    except KeyError:
        pass
    try:
        monkeypatch.delitem(os.environ, 'CRESTIC_DRYRUN')
    except KeyError:
        pass


@pytest.fixture(autouse=True)
def mock_call(mocker):
    mocker.patch('subprocess.call')


@pytest.fixture
def mock_print(mocker):
    mocker.patch('builtins.print')


@pytest.fixture(params=[True, False])
def conffile(monkeypatch, clean_env, request):
    val = 'tests/config.ini'

    if request.param:
        monkeypatch.setitem(os.environ, 'CRESTIC_CONFIG_FILE', val)
        return None
    else:
        return val


@pytest.fixture(params=[True, False])
def dryrun(monkeypatch, clean_env, request):
    if request.param:
        monkeypatch.setitem(os.environ, 'CRESTIC_DRYRUN', "1")
        return None
    else:
        return True


@pytest.fixture(params=[True, False])
def environ(monkeypatch, request):
    if request.param:
        return None
    else:
        return os.environ


def test_plain_backup(conffile, environ):
    crestic.main(["plain", "backup"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla ~',
        env=os.environ,
        shell=True
    )


def test_plain_forget(conffile, environ):
    crestic.main(["plain", "forget"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic forget --exclude-file bla',
        env=os.environ,
        shell=True
    )


def test_boolean(conffile, environ):
    crestic.main(["boolean", "backup"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla --quiet ~',
        env=os.environ,
        shell=True
    )


def test_multivals(conffile, environ):
    crestic.main(["multivals", "backup"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla --exclude config.py --exclude passwords.txt ~',
        env=os.environ,
        shell=True
    )


def test_overloaded(conffile, environ):
    crestic.main(["overloaded", "backup"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file overloaded ~',
        env=os.environ,
        shell=True
    )


def test_overloaded2(conffile, environ):
    crestic.main(["overloaded2", "backup"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file overloaded2 ~',
        env=os.environ,
        shell=True
    )


def test_overloadedargs(conffile, environ):
    crestic.main(["plain", "backup", "--exclude-file", "foo"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file foo ~',
        env=os.environ,
        shell=True
    )


def test_multipleargs(conffile, environ):
    crestic.main(["plain", "backup", "--exclude-file", "foo", "--exclude-file", "bar"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file foo --exclude-file bar ~',
        env=os.environ,
        shell=True
    )


def test_extraargs(conffile, environ):
    crestic.main(["plain", "backup", "--quiet"], conffile=conffile, environ=environ)
    subprocess.call.assert_called_once_with(
        'restic backup --exclude-file bla --quiet ~',
        env=os.environ,
        shell=True
    )


def test_environ(conffile, environ):
    crestic.main(["environ", "backup"], conffile=conffile, environ=environ)

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


def test_dryrun(mock_print, dryrun, conffile, environ):
    retval = crestic.main(["environ", "backup"], dryrun=dryrun, conffile=conffile, environ=environ)

    subprocess.call.assert_not_called()
    builtins.print.assert_called_with(
        '    Expanded command:',
        'restic backup --exclude-file bla ~'
    )
    assert retval == 1
