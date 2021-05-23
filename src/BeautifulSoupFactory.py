import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

from src.InvalidProfileError import InvalidProfileError


class BeautifulSoupFactory:

    # Creates soup object by given string
    def create_from_string(string: str) -> BeautifulSoup:
        return BeautifulSoup(string.replace("\r", "").replace("\t", "").replace("\n", ""), "html.parser")

    # Creates soup object for the general profile.
    def create_from_link(link: str) -> BeautifulSoup:
        page = urlopen(link)
        return BeautifulSoupFactory.create_from_string(page.read().decode("utf-8"))

    # Creates soup object for the general profile.
    def create_for_profile(psn_name: str) -> BeautifulSoup:
        return BeautifulSoupFactory.create_from_link("https://psnprofiles.com/" + psn_name)

    # Creates as soup object for level history.
    def create_for_level_history(psn_name: str) -> BeautifulSoup:
        return BeautifulSoupFactory.create_from_link("https://psnprofiles.com/" + psn_name + "/levels")

    # Creates as soup object for stats.
    def create_for_stats(psn_name: str) -> BeautifulSoup:
        return BeautifulSoupFactory.create_from_link("https://psnprofiles.com/" + psn_name + "/stats")

    # Creates as soup object for all the games.
    def create_for_games(psn_name: str) -> BeautifulSoup:
        content_games = ""
        current_page = 1
        while "nextPage = 0" not in content_games:
            page = urlopen("https://psnprofiles.com/" + psn_name + "?ajax=1&page=" + str(current_page))

            try:
                content_games += json.loads(page.read().decode("utf-8"))["html"]
            except json.decoder.JSONDecodeError:
                # This is most likely an invalid psn name.
                break
            current_page += 1

        if not content_games:
            raise InvalidProfileError(psn_name + " is not a valid psn profile")

        return BeautifulSoupFactory.create_from_string(content_games)
