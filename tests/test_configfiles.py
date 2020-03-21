import pytest

import os
import sys
from crestic import config_files


@pytest.fixture
def no_appdirs(monkeypatch):
    monkeypatch.setitem(sys.modules, "appdirs", None)


def test_xdg_configfiles():
    paths = config_files()
    assert paths == [
        os.path.expanduser('~/.config/crestic/crestic.cfg'),
        '/etc/xdg/crestic/crestic.cfg',
    ]


def test_environ_config_paths():
    paths = config_files({'CRESTIC_CONFIG_PATHS': '/pathA:/pathB'})
    assert paths == ['/pathA/crestic.cfg', '/pathB/crestic.cfg']


def test_environ_config_file():
    paths = config_files({'CRESTIC_CONFIG_FILE': '/fileA/crestic.cfg'})
    assert paths == ['/fileA/crestic.cfg']


def test_default_configfiles(no_appdirs):
    paths = config_files()
    assert paths == [
        os.path.expanduser('~/.config/crestic/crestic.cfg'),
        '/etc/crestic/crestic.cfg'
    ]
