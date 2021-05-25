import pytest

from src.PsnProfilesScraper import PsnProfilesScraper
from src.InvalidProfileError import InvalidProfileError


def test_valid_username():
    scraper = PsnProfilesScraper("Fluttezuhher")
    profile = scraper.get_profile()

    assert profile.get_name() == "Fluttezuhher"


def test_invalid_username():
    with pytest.raises(InvalidProfileError):
        PsnProfilesScraper("InvalidUsernameFoSho")
