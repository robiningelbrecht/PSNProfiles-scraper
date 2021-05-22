import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

from src.InvalidProfileError import InvalidProfileError


class BeautifulSoupFactory:

    # Creates soup object by given string
    def create_soup_by_content(content: str) -> BeautifulSoup:
        return BeautifulSoup(content.replace("\r", "").replace("\t", "").replace("\n", ""), "html.parser")

    # Creates soup object for the general profile.
    def create_profile_soup(psn_name: str) -> BeautifulSoup:
        page = urlopen("https://psnprofiles.com/" + psn_name)
        return BeautifulSoupFactory.create_soup_by_content(page.read().decode("utf-8"))

    # Creates as oup object for all the games.
    def create_games_soup(psn_name: str) -> BeautifulSoup:
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

        return BeautifulSoupFactory.create_soup_by_content(content_games)
