from __future__ import annotations
import json
import re
from bs4 import BeautifulSoup

from psnprofiles_scraper.src.Utils import to_int
from psnprofiles_scraper.src.PsnProfiles.PsnProfilesObjectInterface import PsnProfilesObjectInterface
from psnprofiles_scraper.src.BeautifulSoupFactory import BeautifulSoupFactory
from psnprofiles_scraper.src.PsnProfiles.Trophy import Trophy


class Game(PsnProfilesObjectInterface):
    def __init__(self, title: str, trophy_stats: dict, platform: str, rank: str, has_earned_platinum: bool,
                 thumbnail_uri: str, uri: str):
        self.title = title
        self.trophy_stats = trophy_stats
        self.platform = platform
        self.rank = rank
        self.has_earned_platinum = has_earned_platinum
        self.thumbnail_uri = thumbnail_uri
        self.uri = uri

        # Instance properties for detailed info.
        self.cover_uri = None
        self.background_uri = None
        self.trophies = []
        self.trophy_count = {
            "platinum": 0,
            "gold": 0,
            "silver": 0,
            "bronze": 0
        }
        self.developers = []
        self.publishers = []
        self.genres = []
        self.themes = []
        self.modes = []

    def populate_details_from_soup(self, soup: BeautifulSoup):
        self.cover_uri = soup.select("div.game-image-holder picture.game img")[0]["src"] if soup.select(
            "div.game-image-holder picture.game img") else ""
        self.background_uri = re.findall(r'url\(([^)]+)\)', soup.select("div#banner div.img")[1]["style"])[
            0] if soup.select("div#banner div.img") else ""
        self.developers = soup.find("td", text=re.compile("Developer.*")).find_next().text.split(', ') if soup.find(
            "td", text=re.compile("Developer.*")) else ""
        self.publishers = soup.find("td", text=re.compile("Publisher.*")).find_next().text.split(', ') if soup.find(
            "td", text=re.compile("Publisher.*")) else ""
        self.genres = soup.find("td", text=re.compile("Genre.*")).find_next().text.split(', ') if soup.find("td",
                                                                                                            text=re.compile(
                                                                                                                "Genre.*")) else ""
        self.themes = soup.find("td", text=re.compile("Theme.*")).find_next().text.split(', ') if soup.find("td",
                                                                                                            text=re.compile(
                                                                                                                "Theme.*")) else ""
        self.modes = soup.find("td", text=re.compile("Mode.*")).find_next().text.split(', ') if soup.find("td",
                                                                                                          text=re.compile(
                                                                                                              "Mode.*")) else ""

        self.trophy_count["platinum"] = soup.select("div.col-xs-4 div.trophy-count li.icon-sprite.platinum")[
            0].text if soup.select(
            "div.col-xs-4 div.trophy-count li.icon-sprite.platinum") else ""
        self.trophy_count["gold"] = soup.select("div.col-xs-4 div.trophy-count li.icon-sprite.gold")[
            0].text if soup.select(
            "div.col-xs-4 div.trophy-count li.icon-sprite.gold") else ""
        self.trophy_count["silver"] = soup.select("div.col-xs-4 div.trophy-count li.icon-sprite.silver")[
            0].text if soup.select(
            "div.col-xs-4 div.trophy-count li.icon-sprite.silver") else ""
        self.trophy_count["bronze"] = soup.select("div.col-xs-4 div.trophy-count li.icon-sprite.bronze")[
            0].text if soup.select(
            "div.col-xs-4 div.trophy-count li.icon-sprite.bronze") else ""

        if not soup.select("div.col-xs div.box.no-top-border table"):
            return

        # Append all trophy info to game.
        for table in soup.select("div.col-xs div.box.no-top-border table"):
            for row in table.find_all('tr'):
                if len(row.find_all('td')) < 6:
                    continue

                trophy = Trophy.create_from_game_detail_soup(BeautifulSoupFactory.create_from_string(str(row)))
                self.trophies.append(trophy)

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
                'completion': soup.select("div.progress-bar span")[0].text if soup.select(
                    "div.progress-bar span") else None,
            },
            soup.select("span.tag.platform")[0].text if soup.select("span.tag.platform") else "",
            soup.select("span.game-rank")[0].text if soup.select("span.game-rank") else "",
            len(soup.select("span.platinum.earned")) > 0,
            soup.select("picture.game img")[0]["src"] if soup.select("picture.game img") else "",
            "https://psnprofiles.com" + soup.find("a", class_="title")["href"] if soup.find("a",
                                                                                            class_="title") else "",
        )
