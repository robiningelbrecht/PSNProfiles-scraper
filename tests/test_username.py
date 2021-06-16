import pytest

from psnprofiles_scraper.src.PsnProfilesScraper import PsnProfilesScraper
from psnprofiles_scraper.src.InvalidProfileError import InvalidProfileError


def test_valid_username():
    scraper = PsnProfilesScraper()
    profile = scraper.get_profile("Fluttezuhher", False)

    assert profile.get_name() == "Fluttezuhher"


def test_invalid_username():
    with pytest.raises(InvalidProfileError):
        scraper = PsnProfilesScraper()
        scraper.get_profile("InvalidUsernameFoSho", False)
