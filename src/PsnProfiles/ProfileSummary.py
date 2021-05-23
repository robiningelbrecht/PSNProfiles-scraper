from __future__ import annotations
import json
from bs4 import BeautifulSoup

from src.Utils import to_int
from src.PsnProfileObjectInterface import PsnProfileObjectInterface


class ProfileSummary(PsnProfileObjectInterface):
    def __init__(self, level: int, trophies: dict, points: dict, games: dict, stats: dict):
        self.level = level
        self.trophies = trophies
        self.points = points
        self.games = games
        self.stats = stats

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)

    def create_from_soup(soup: BeautifulSoup) -> ProfileSummary:
        profile_bar = soup.find("ul", class_="profile-bar")
        stats = soup.select("div.stats.flex")[0]

        level = to_int(profile_bar.select("#bar-level li.icon-sprite.level")[0].text) if profile_bar.select(
            "#bar-level li.icon-sprite.level") else 0
        trophies = {
            'total': to_int(profile_bar.find("li", class_="total").text) if profile_bar.find("li",
                                                                                             class_="total") else 0,
            'grade': {
                'platinum': to_int(profile_bar.find("li", class_="platinum").text) if profile_bar.find("li",
                                                                                                       class_="platinum") else 0,
                'gold': to_int(profile_bar.find("li", class_="gold").text) if profile_bar.find("li",
                                                                                               class_="gold") else 0,
                'silver': to_int(profile_bar.find("li", class_="silver").text) if profile_bar.find("li",
                                                                                                   class_="silver") else 0,
                'bronze': to_int(profile_bar.find("li", class_="bronze").text) if profile_bar.find("li",
                                                                                                   class_="bronze") else 0,
            },
            'rarity': {}
        }

        if soup.select("div.sidebar div.box.no-top-border div.row.lg-hide"):
            for trophy_rarity in soup.select("div.box.no-top-border div.row.lg-hide")[0].find_all('div',
                                                                                                  class_="col-lg"):
                if not trophy_rarity.find("span", class_="typo-top"):
                    continue
                if not trophy_rarity.find("span", class_="typo-bottom"):
                    continue
                trophies["rarity"][
                    trophy_rarity.find("span", class_="typo-bottom").text.lower().replace(" ", "_")] = to_int(
                    trophy_rarity.find("span", class_="typo-top").text)

        games = {
            'played': to_int(stats.find("span", text="Games Played").parent.contents[0]) if stats.find("span",
                                                                                                       text="Games Played") else 0,
            'completed': to_int(stats.find("span", text="Completed Games").parent.contents[0]) if stats.find(
                "span", text="Completed Games") else 0,
            'platforms': {},
            'ranks': {}
        }

        stats = {
            'completion': {
                'average': stats.find("span", text="Completion").parent.contents[0] if stats.find("span",
                                                                                                  text="Completion") else 0,
            },
            'unearned_trophies': to_int(stats.find("span", text="Unearned Trophies").parent.contents[0]) if stats.find(
                "span", text="Unearned Trophies") else 0,
            'trophies_per_day': stats.find("span", text="Trophies Per Day").parent.contents[0] if stats.find("span",
                                                                                                             text="Trophies Per Day") else 0,
            'views': to_int(stats.find("span", text="Views").parent.contents[0]) if stats.find("span",
                                                                                               text="Views") else 0,
            'world_rank': to_int(stats.find("span", text="World Rank").parent.contents[0]) if stats.find("span",
                                                                                                         text="World Rank") else 0,
            'country_rank': to_int(stats.find("span", text="Country Rank").parent.contents[0]) if stats.find("span",
                                                                                                             text="Country Rank") else 0,
        }

        detailed_stats = list(soup.select('div.col-xs-4 > div.box > div.row > div.col-xs-6 > table'))

        points = {}
        if len(detailed_stats) >= 6:
            for stat in detailed_stats[0].find_all("li"):
                (platform, count) = list(stat.stripped_strings)
                games["platforms"][platform] = to_int(count)

            for stat in detailed_stats[5].find_all("li"):
                (rank, count) = list(stat.stripped_strings)
                games["ranks"][rank] = to_int(count)

            total_points = 0
            for stat in detailed_stats[2].find_all("li"):
                (grade, count) = list(stat.stripped_strings)
                points[grade.lower()] = to_int(count)
                total_points += points[grade.lower()]
            points["total"] = total_points

            for stat in detailed_stats[4].find_all("li"):
                (completion, count) = list(stat.stripped_strings)
                stats["completion"][completion] = to_int(count)

        return ProfileSummary(level, trophies, points, games, stats)
