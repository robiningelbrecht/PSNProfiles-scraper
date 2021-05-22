import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

from src.Utils import to_int
from src.InvalidProfileError import InvalidProfileError
from src.PsnProfiles.Profile import Profile
from src.PsnProfiles.ProfileSummary import ProfileSummary
from src.PsnProfiles.Trophy import Trophy
from src.PsnProfiles.Milestone import Milestone
from src.PsnProfiles.Game import Game


class PsnScraper:
    def __init__(self, psn_name=""):
        self.psn_name = psn_name

        page = urlopen("https://psnprofiles.com/" + self.psn_name)
        content = page.read().decode("utf-8")
        self.parser = BeautifulSoup(content.replace("\r", "").replace("\t", "").replace("\n", ""), "html.parser")

        content_games = ""
        current_page = 1
        while "nextPage = 0" not in content_games:
            page = urlopen("https://psnprofiles.com/" + self.psn_name + "?ajax=1&page=" + str(current_page))

            try:
                content_games += json.loads(page.read().decode("utf-8"))["html"]
            except json.decoder.JSONDecodeError:
                # This is most likely an invalid psn name.
                break
            current_page += 1

        if content_games:
            self.parser_games = BeautifulSoup(content_games.replace("\r", "").replace("\t", "").replace("\n", ""),
                                              "html.parser")

    # Returns the full PSN profile object.
    def get_profile(self) -> Profile:
        if not hasattr(self, "parser_games"):
            raise InvalidProfileError(self.psn_name + " is not a valid psn profile")

        return Profile(self.psn_name, self.get_profile_summary(), self.get_recent_trophies(),
                       self.get_rarest_trophies(), self.get_milestones(), self.get_games(), self.get_trophy_cabinet())

    # Scrapes and returns the profile summary.
    def get_profile_summary(self) -> ProfileSummary:
        profile_bar = self.parser.find("ul", class_="profile-bar")
        stats = self.parser.select("div.stats.flex")[0]

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

        if self.parser.select("div.sidebar div.box.no-top-border div.row.lg-hide"):
            for trophy_rarity in self.parser.select("div.box.no-top-border div.row.lg-hide")[0].find_all('div',
                                                                                                         class_="col-lg"):
                if not trophy_rarity.find("span", class_="typo-top"):
                    continue
                if not trophy_rarity.find("span", class_="typo-bottom"):
                    continue
                trophies["rarity"][
                    trophy_rarity.find("span", class_="typo-bottom").text.lower().replace(" ", "_")] = to_int(
                    trophy_rarity.find("span", class_="typo-top").text)

        stats = {
            'games_played': to_int(stats.find("span", text="Games Played").parent.contents[0]) if stats.find("span",
                                                                                                             text="Games Played") else 0,
            'completed_games': to_int(stats.find("span", text="Completed Games").parent.contents[0]) if stats.find(
                "span", text="Completed Games") else 0,
            'completion': stats.find("span", text="Completion").parent.contents[0] if stats.find("span",
                                                                                                 text="Completion") else 0,
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

        return ProfileSummary(level, trophies, stats)

    # Scrapes and returns the recent trophies.
    def get_recent_trophies(self) -> list:
        if not self.parser.select("ul#recent-trophies"):
            return []

        recent_trophies = []
        for recent_trophy in self.parser.select("ul#recent-trophies")[0].find_all('li'):
            recent_trophies.append(Trophy(
                recent_trophy.find("a", class_="title").text if recent_trophy.find("a", class_="title") else "",
                recent_trophy.select("span.small_info_green a")[0].text if recent_trophy.select(
                    "span.small_info_green a") else "",
                recent_trophy.select("span.separator span.typo-top")[0].text if recent_trophy.select(
                    "span.separator span.typo-top") else "",
                recent_trophy.select("span.separator span.typo-bottom")[0].text if recent_trophy.select(
                    "span.separator span.typo-bottom") else "",
                recent_trophy.select("span.separator.left img")[0]["alt"] if recent_trophy.select(
                    "span.separator.left img") else "",
                recent_trophy.select("picture.trophy img")[0]["src"] if recent_trophy.select(
                    'picture.trophy img') else "",
            ))

        return recent_trophies

    # Scrapes and returns trophy cabinet
    def get_rarest_trophies(self) -> list:
        if not self.parser.find("h3", text="Rarest Trophies"):
            return []

        if not self.parser.select('div.sidebar div.box.no-top-border table'):
            return []

        rarest_trophies = self.parser.select('div.sidebar div.box.no-top-border table')[0]

        trophies = []
        for trophy in rarest_trophies.find_all("tr"):
            trophies.append(Trophy(
                trophy.find("a", class_="small-title").text if trophy.find("a", class_="small-title") else "",
                trophy.find("a", rel="nofollow").text if trophy.find("a", rel="nofollow") else "",
                trophy.select("span.typo-top")[0].text if trophy.select("span.typo-top") else "",
                trophy.select("span.typo-bottom")[0].text if trophy.select("span.typo-bottom") else "",
                trophy.select("span.separator.left img")[0]["alt"] if trophy.select("span.separator.left img") else "",
                trophy.select("picture.trophy img")[0]["src"] if trophy.select("picture.trophy img") else "",
            ))

        return trophies

    # Scrapes and returns trophy cabinet
    def get_trophy_cabinet(self) -> list:
        if not self.parser.find("h3", text="Trophy Cabinet"):
            return []

        if not self.parser.select("div.sidebar table.box.zebra"):
            return []

        trophy_cabinet = self.parser.select("div.sidebar table.box.zebra")[0]

        trophies = []
        for trophy in trophy_cabinet.find_all("tr"):
            trophies.append(Trophy(
                trophy.find("a", class_="small-title").text if trophy.find("a", class_="small-title") else "",
                trophy.find("a", rel="nofollow").text if trophy.find("a", rel="nofollow") else "",
                trophy.select("span.typo-top")[0].text if trophy.select("span.typo-top") else "",
                trophy.select("span.typo-bottom")[0].text if trophy.select("span.typo-bottom") else "",
                trophy.select("span.separator.left img")[0]["alt"] if trophy.select("span.separator.left img") else "",
                trophy.select("picture.trophy img")[0]["src"] if trophy.select("picture.trophy img") else "",
            ))

        return trophies

    # Scrapes and returns milestones.
    def get_milestones(self) -> list:
        if not self.parser.find("h3", text="Trophy Milestones"):
            return []

        milestones_table = self.parser.find("h3", text="Trophy Milestones").find_next()

        milestones = []
        for milestone in milestones_table.find_all("tr"):
            milestones.append(Milestone(
                milestone.find("a", class_="small-title").text if milestone.find("a", class_="small-title") else "",
                milestone.find("a", rel="nofollow").text if milestone.find("a", rel="nofollow") else "",
                milestone.select("span.typo-top-smaller.not-uppercase")[0].text if milestone.select(
                    "span.typo-top-smaller.not-uppercase") else "",
                milestone.select("span.typo-bottom-date")[0].text if milestone.select("span.typo-bottom-date") else "",
            ))

        return milestones

    # Scrapes and returns games.
    def get_games(self) -> list:
        if not self.parser_games.find("tr"):
            return []

        games = []
        for game in self.parser_games.find_all("tr"):
            if not game.find("div", class_="small-info"):
                continue

            if len(game.find_all("div", class_="small-info")) != 2:
                continue

            trophies = game.find("div", class_="small-info")

            trophies_obtained = trophies.find_all("b")[0].text if trophies.find_all("b") else 0
            trophies_total = trophies.find_all("b")[0].text if trophies.find_all("b") else 0
            if len(trophies.find_all("b")) == 2:
                trophies_total = trophies.find_all("b")[1].text

            games.append(Game(
                game.find("a", class_="title").text if game.find("a", class_="title") else "",
                {
                    'obtained': trophies_obtained,
                    'total': trophies_total,
                    'gold': game.select("span.icon-sprite.gold")[0].find_next().text if game.select(
                        "span.icon-sprite.gold") else 0,
                    'silver': game.select("span.icon-sprite.silver")[0].find_next().text if game.select(
                        "span.icon-sprite.silver") else 0,
                    'bronze': game.select("span.icon-sprite.bronze")[0].find_next().text if game.select(
                        "span.icon-sprite.bronze") else 0,
                    'completion': game.select("div.progress-bar span")[0].text if game.select(
                        "div.progress-bar span") else 0,
                },
                game.select("span.tag.platform")[0].text if game.select("span.tag.platform") else "",
                game.select("span.game-rank")[0].text if game.select("span.game-rank") else "",
                len(game.select("span.platinum.earned")) > 0,
                game.select("picture.game img")[0]["src"] if game.select("picture.game img") else "",
            ))
        return games
