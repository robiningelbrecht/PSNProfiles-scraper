from __future__ import annotations
import json
from bs4 import BeautifulSoup

from src.Utils import to_int
from src.Utils import extract_game_from_uri
from src.PsnProfiles.PsnProfilesObjectInterface import PsnProfilesObjectInterface


class Level(PsnProfilesObjectInterface):

    def __init__(self, level: int, game: str, game_thumbnail_uri: str, trophy_title: str, trophy_description: str,
                 trophy_icon_uri: str, date: str):
        self.level = level
        self.game = {
            "title": game,
            "thumbnail_uri": game_thumbnail_uri
        }
        self.trophy = {
            "title": trophy_title,
            "description": trophy_description,
            "icon_uri": trophy_icon_uri
        }
        self.date = date

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)

    def create_from_soup(soup: BeautifulSoup) -> Level:
        return Level(
            to_int(list(soup.stripped_strings)[2]),
            extract_game_from_uri(soup.find("a")["href"]),
            soup.select("picture.game img")[0]["src"] if soup.select("picture.game img") else "",
            list(soup.stripped_strings)[0],
            list(soup.stripped_strings)[1],
            soup.select("picture.trophy img")[0]["src"] if soup.select("picture.trophy img") else "",
            soup.select("span.typo-top-date nobr")[0].text + " " + soup.select("span.typo-bottom-date nobr")[
                0].text
        )
