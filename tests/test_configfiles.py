import pytest

import os
from crestic import config_files


def test_xdg_configfiles():
    paths = config_files()
    assert paths == [
        os.path.expanduser('~/.config/crestic/crestic.ini'),
        '/etc/xdg/crestic/crestic.ini',
    ]


def test_environ_config_paths():
    paths = config_files({'CRESTIC_CONFIG_PATHS': '/pathA:/pathB'})
    assert paths == ['/pathA/crestic.ini', '/pathB/crestic.ini']


def test_environ_config_file():
    paths = config_files({'CRESTIC_CONFIG_FILE': '/fileA/crestic.ini'})
    assert paths == ['/fileA/crestic.ini']


def test_default_configfiles(mocker):
    mocker.patch("appdirs.user_config_dir", side_effect=ImportError)
    mocker.patch("appdirs.site_config_dir", side_effect=ImportError)
    paths = config_files()
    assert paths == [
        os.path.expanduser('~/.config/crestic/crestic.ini'),
        '/etc/crestic.ini'
    ]
