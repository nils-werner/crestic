import pytest
import argparse

import crestic


def test_split():
    assert crestic.split("home") == ["home"]
    assert crestic.split("home@nas") == ["home@", "@nas"]
    assert crestic.split("home@") == ["home@", "@"]
    assert crestic.split("@nas") == ["@", "@nas"]
    assert crestic.split("home@nas-home") == ["home@", "@nas-home"]
    assert crestic.split("") == [""]


def test_valid_preset():
    assert crestic.valid_preset("home") == "home"
    assert crestic.valid_preset("home@nas") == "home@nas"
    assert crestic.valid_preset("home@nas-home") == "home@nas-home"

    with pytest.raises(argparse.ArgumentTypeError):
        crestic.valid_preset("@nas")
    with pytest.raises(argparse.ArgumentTypeError):
        crestic.valid_preset("home@")
    with pytest.raises(argparse.ArgumentTypeError):
        crestic.valid_preset("@")
