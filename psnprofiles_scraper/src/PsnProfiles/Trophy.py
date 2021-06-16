from __future__ import annotations
import json
from bs4 import BeautifulSoup

from psnprofiles_scraper.src.PsnProfiles.PsnProfilesObjectInterface import PsnProfilesObjectInterface


class Trophy(PsnProfilesObjectInterface):
    def __init__(self, title: str, description: str, rarity_percentage: str, rarity_label: str, grade: str,
                 icon_uri: str, obtained: bool = True):
        self.title = title
        self.description = description
        self.rarity_percentage = rarity_percentage
        self.rarity_label = rarity_label
        self.grade = grade.lower()
        self.icon_uri = icon_uri
        self.obtained = obtained

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)

    def create_from_soup(soup: BeautifulSoup) -> Trophy:
        return Trophy(
            soup.find("a", class_="small-title").text if soup.find("a", class_="small-title") else "",
            soup.find("a", rel="nofollow").text if soup.find("a", rel="nofollow") else "",
            soup.select("span.typo-top")[0].text if soup.select("span.typo-top") else "",
            soup.select("span.typo-bottom")[0].text if soup.select("span.typo-bottom") else "",
            soup.select("span.separator.left img")[0]["alt"] if soup.select("span.separator.left img") else "",
            soup.select("picture.trophy img")[0]["src"] if soup.select("picture.trophy img") else "",
        )

    def create_from_alternative_soup(soup: BeautifulSoup) -> Trophy:
        return Trophy(
            soup.find("a", class_="title").text if soup.find("a", class_="title") else "",
            soup.select("span.small_info_green a")[0].text if soup.select(
                "span.small_info_green a") else "",
            soup.select("span.separator span.typo-top")[0].text if soup.select(
                "span.separator span.typo-top") else "",
            soup.select("span.separator span.typo-bottom")[0].text if soup.select(
                "span.separator span.typo-bottom") else "",
            soup.select("span.separator.left img")[0]["title"] if soup.select(
                "span.separator.left img") else "",
            soup.select("picture.trophy img")[0]["src"] if soup.select(
                'picture.trophy img') else "",
        )

    def create_from_game_detail_soup(soup: BeautifulSoup) -> Trophy:
        title = soup.find("a", class_="title").text if soup.find("a", class_="title") else ""
        description = soup.find_all("td")[1].text.replace(title, "")

        return Trophy(
            title,
            description,
            soup.select("span.separator span.typo-top")[0].text if soup.select(
                "span.separator span.typo-top") else "",
            soup.select("span.separator span.typo-bottom")[0].text if soup.select(
                "span.separator span.typo-bottom") else "",
            soup.select("span.separator.left img")[0]["title"] if soup.select(
                "span.separator.left img") else "",
            soup.select("picture.trophy img")[0]["src"] if soup.select(
                'picture.trophy img') else "",
            True if soup.find('tr', class_="completed") else False
        )
