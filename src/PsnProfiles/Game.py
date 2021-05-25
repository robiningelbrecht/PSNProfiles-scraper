from __future__ import annotations
import json
from bs4 import BeautifulSoup

from src.Utils import to_int
from src.PsnProfilesObjectInterface import PsnProfilesObjectInterface


class Game(PsnProfilesObjectInterface):
    def __init__(self, title: str, trophy_stats: dict, platform: str, rank: str, has_earned_platinum: bool,
                 thumbnail_uri: str):
        self.title = title
        self.trophy_stats = trophy_stats
        self.platform = platform
        self.rank = rank
        self.has_earned_platinum = has_earned_platinum
        self.thumbnail_uri = thumbnail_uri

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)

    def create_from_soup(soup: BeautifulSoup) -> Game:
        trophies = soup.find("div", class_="small-info")

        trophies_obtained = to_int(trophies.find_all("b")[0].text) if trophies.find_all("b") else 0
        trophies_total = to_int(trophies.find_all("b")[0].text) if trophies.find_all("b") else 0
        if len(trophies.find_all("b")) == 2:
            trophies_total = to_int(trophies.find_all("b")[1].text)

        return Game(
            soup.find("a", class_="title").text if soup.find("a", class_="title") else "",
            {
                'obtained': trophies_obtained,
                'total': trophies_total,
                'gold': to_int(soup.select("span.icon-sprite.gold")[0].find_next().text) if soup.select(
                    "span.icon-sprite.gold") else 0,
                'silver': to_int(soup.select("span.icon-sprite.silver")[0].find_next().text) if soup.select(
                    "span.icon-sprite.silver") else 0,
                'bronze': to_int(soup.select("span.icon-sprite.bronze")[0].find_next().text) if soup.select(
                    "span.icon-sprite.bronze") else 0,
                'completion': to_int(soup.select("div.progress-bar span")[0].text) if soup.select(
                    "div.progress-bar span") else 0,
            },
            soup.select("span.tag.platform")[0].text if soup.select("span.tag.platform") else "",
            soup.select("span.game-rank")[0].text if soup.select("span.game-rank") else "",
            len(soup.select("span.platinum.earned")) > 0,
            soup.select("picture.game img")[0]["src"] if soup.select("picture.game img") else "",
        )
