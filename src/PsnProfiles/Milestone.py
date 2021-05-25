from __future__ import annotations
import json
from bs4 import BeautifulSoup

from src.PsnProfilesObjectInterface import PsnProfilesObjectInterface


class Milestone(PsnProfilesObjectInterface):
    def __init__(self, title: str, game: str, description: str, date: str):
        self.title = title
        self.game = game
        self.description = description
        self.date = date

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)

    def create_from_soup(soup: BeautifulSoup) -> Milestone:
        return Milestone(
            soup.find("a", class_="small-title").text if soup.find("a", class_="small-title") else "",
            soup.find("a", rel="nofollow").text if soup.find("a", rel="nofollow") else "",
            soup.select("span.typo-top-smaller.not-uppercase")[0].text if soup.select(
                "span.typo-top-smaller.not-uppercase") else "",
            soup.select("span.typo-bottom-date")[0].text if soup.select("span.typo-bottom-date") else "",
        )
