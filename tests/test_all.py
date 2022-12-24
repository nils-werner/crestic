import os
import io
import sys
import subprocess

import pytest
import crestic

import builtins

testroot = os.path.dirname(__file__)


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    try:
        monkeypatch.delitem(os.environ, 'CRESTIC_CONFIG_FILE')
    except KeyError:
        pass
    try:
        monkeypatch.delitem(os.environ, 'CRESTIC_CONFIG_PATHS')
    except KeyError:
        pass
    try:
        monkeypatch.delitem(os.environ, 'CRESTIC_DRYRUN')
    except KeyError:
        pass


@pytest.fixture(autouse=True)
def mock_call(mocker):
    mocker.patch('os.execvpe')


@pytest.fixture
def mock_print(mocker):
    mocker.patch('builtins.print')


@pytest.fixture()
def conffile():
    return [testroot + '/config.ini', testroot + '/overloading_config.ini']


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


@pytest.fixture(params=[True, False], autouse=True)
def mock_parse_intermixed_args(request, monkeypatch):
    if request.param:
        if sys.version_info < (3, 7):
            pytest.skip("requires python3.7 or higher")

        import argparse
        monkeypatch.delattr(argparse.ArgumentParser, 'parse_intermixed_args')

    return request.param


def test_plain_backup(conffile, environ):
    crestic.main(["plain", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', '/home/user'],
        env=os.environ,
    )


def test_plain_forget(conffile, environ):
    crestic.main(["plain", "forget"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'forget', '--exclude-file', 'bla'],
        env=os.environ,
    )


def test_boolean(conffile, environ):
    crestic.main(["boolean", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', '--quiet', '/home/user'],
        env=os.environ,
    )


def test_emptystring(conffile, environ):
    with pytest.deprecated_call():
        crestic.main(["emptystring", "backup"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', '--empty', '--noval', '/home/user'],
        env=os.environ,
    )


def test_singlechar(conffile, environ):
    crestic.main(["singlechar", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', '-r', 'repo-url', '/home/user'],
        env=os.environ,
    )


def test_multivals(conffile, environ):
    crestic.main(["multivals", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', '--exclude', 'config.py', '--exclude', 'passwords.txt', '/home/user'],
        env=os.environ,
    )


def test_overloaded(conffile, environ):
    crestic.main(["overloaded", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'overloaded', '/home/user'],
        env=os.environ,
    )


def test_overloaded2(conffile, environ):
    crestic.main(["overloaded2", "backup"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'overloaded2', '/home/user'],
        env=os.environ,
    )


def test_overloadedargs(conffile, environ):
    crestic.main(["plain", "backup", "--exclude-file", "foo"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'foo', '/home/user'],
        env=os.environ,
    )


def test_multipleargs(conffile, environ):
    crestic.main(["plain", "backup", "--exclude-file", "foo", "--exclude-file", "bar"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'foo', '--exclude-file', 'bar', '/home/user'],
        env=os.environ,
    )


def test_extraargs(conffile, environ):
    crestic.main(["plain", "backup", "--quiet"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', '--quiet', '/home/user'],
        env=os.environ,
    )


def test_environ(conffile, environ):
    crestic.main(["environ", "backup"], conffile=conffile, environ=environ)

    environ = dict(os.environ)
    environ.update({
        'B2_ACCOUNT_ID': 'testid',
        'B2_ACCOUNT_KEY': 'testkey',
    })

    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', '/home/user'],
        env=environ,
    )


def test_dryrun(mock_print, dryrun, conffile, environ):
    retval = crestic.main(["environ", "backup"], dryrun=dryrun, conffile=conffile, environ=environ)

    os.execvpe.assert_not_called()
    builtins.print.assert_called_with(
        '    Expanded command:',
        'restic backup --exclude-file bla /home/user'
    )
    assert retval == 0


def test_invalid(mock_print):
    with pytest.raises(SystemExit):
        retval = crestic.main(["@nas", "backup"])

    os.execvpe.assert_not_called()


def test_expanded_tilde(conffile, environ):
    retval = crestic.main(["plain", "backup", "~"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', os.path.expanduser('~')],
        env=os.environ,
    )


def test_expanded_variable(conffile, environ):
    retval = crestic.main(["plain", "backup", "$HOME"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'bla', os.path.expandvars('$HOME')],
        env=os.environ,
    )


@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
def test_intermixed(conffile, environ, mock_parse_intermixed_args):
    if mock_parse_intermixed_args:
        pytest.skip()

    crestic.main(["plain", "restore", "--include", "path space", "--target", ".", "asd"], conffile=conffile, environ=environ)
    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'restore', '--exclude-file', 'bla', '--include', 'path space', '--target', '.', 'asd'],
        env=os.environ,
    )


def test_intermixed_error(conffile, environ, mock_parse_intermixed_args):
    if not mock_parse_intermixed_args:
        pytest.skip()

    with pytest.raises(SystemExit):
        crestic.main(
            ["plain", "restore", "--include", "path space", "--target", ".", "asd"],
            conffile=conffile,
            environ=environ
        )


def test_overloaded_config(conffile, environ):
    retval = crestic.main(["overloaded_config", "backup"], conffile=conffile, environ=environ)

    os.execvpe.assert_called_once_with(
        'restic',
        ['restic', 'backup', '--exclude-file', 'valid', '/home/user'],
        env=os.environ,
    )
