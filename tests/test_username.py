import pytest

from src.PsnProfileScraper import PsnProfileScraper
from src.InvalidProfileError import InvalidProfileError


def test_valid_username():
    scraper = PsnProfileScraper("Fluttezuhher")
    profile = scraper.get_profile()

    assert profile.get_name() == "Fluttezuhher"


def test_invalid_username():
    with pytest.raises(InvalidProfileError):
        PsnProfileScraper("InvalidUsernameFoSho")
