from typing import List

from src.Utils import to_int

from src.BeautifulSoupFactory import BeautifulSoupFactory
from src.PsnProfiles.Profile import Profile
from src.PsnProfiles.ProfileSummary import ProfileSummary
from src.PsnProfiles.Trophy import Trophy
from src.PsnProfiles.Milestone import Milestone
from src.PsnProfiles.Game import Game
from src.PsnProfiles.Level import Level


class PsnProfileScraper:
    def __init__(self, psn_name=""):
        self.__psn_name = psn_name

        self.__soup_profile = BeautifulSoupFactory.create_profile_soup(self.__psn_name)
        self.__soup_games = BeautifulSoupFactory.create_from_games(self.__psn_name)
        self.__soup_level_history = BeautifulSoupFactory.create_from_level_history(self.__psn_name)
        self.__soup_stats = BeautifulSoupFactory.create_from_stats(self.__psn_name)

    # Returns a full PSN profile object.
    def get_profile(self) -> Profile:
        country = ""
        if self.__soup_profile.select("img#bar-country"):
            country = BeautifulSoupFactory.create_from_string(
                self.__soup_profile.select("img#bar-country")[0]["title"]).text

        return Profile(
            self.__psn_name,
            country,
            ProfileSummary.create_from_soup(BeautifulSoupFactory.create_from_string(str(self.__soup_profile) + str(self.__soup_stats))),
            self.__get_recent_trophies(),
            self.__get_rarest_trophies(),
            self.__get_milestones(),
            self.__get_games(),
            self.__get_trophy_cabinet(),
            self.__get_level_history()
        )

    # Scrapes and returns the recent trophies.
    def __get_recent_trophies(self) -> List[Trophy]:
        if not self.__soup_profile.select("ul#recent-trophies"):
            return []

        recent_trophies = []
        for recent_trophy in self.__soup_profile.select("ul#recent-trophies")[0].find_all('li'):
            recent_trophies.append(Trophy.create_from_alternative_soup(BeautifulSoupFactory.create_from_string(str(recent_trophy))))

        return recent_trophies

    # Scrapes and returns trophy cabinet
    def __get_rarest_trophies(self) -> List[Trophy]:
        if not self.__soup_profile.find("h3", text="Rarest Trophies"):
            return []

        if not self.__soup_profile.select('div.sidebar div.box.no-top-border table'):
            return []

        rarest_trophies = self.__soup_profile.select('div.sidebar div.box.no-top-border table')[0]

        trophies = []
        for trophy in rarest_trophies.find_all("tr"):
            trophies.append(Trophy.create_from_soup(BeautifulSoupFactory.create_from_string(str(trophy))))

        return trophies

    # Scrapes and returns trophy cabinet
    def __get_trophy_cabinet(self) -> List[Trophy]:
        if not self.__soup_profile.find("h3", text="Trophy Cabinet"):
            return []

        if not self.__soup_profile.select("div.sidebar table.box.zebra"):
            return []

        trophy_cabinet = self.__soup_profile.select("div.sidebar table.box.zebra")[0]

        trophies = []
        for trophy in trophy_cabinet.find_all("tr"):
            trophies.append(Trophy.create_from_soup(BeautifulSoupFactory.create_from_string(str(trophy))))

        return trophies

    # Scrapes and returns milestones.
    def __get_milestones(self) -> List[Milestone]:
        if not self.__soup_profile.find("h3", text="Trophy Milestones"):
            return []

        milestones_table = self.__soup_profile.find("h3", text="Trophy Milestones").find_next()

        milestones = []
        for milestone in milestones_table.find_all("tr"):
            milestones.append(Milestone.create_from_soup(BeautifulSoupFactory.create_from_string(str(milestone))))

        return milestones

    # Scrapes and returns games.
    def __get_games(self) -> List[Game]:
        if not self.__soup_games.find("tr"):
            return []

        games = []
        for game in self.__soup_games.find_all("tr"):
            if not game.find("div", class_="small-info"):
                continue

            if len(game.find_all("div", class_="small-info")) != 2:
                continue

            games.append(Game.create_from_soup(BeautifulSoupFactory.create_from_string(str(game))))
        return games

    # Scrapes and returns level history.
    def __get_level_history(self) -> List[Level]:
        if not self.__soup_level_history.select("table.box.zebra"):
            return []

        levels = []
        for level in self.__soup_level_history.select("table.box.zebra")[0].find_all("tr"):
            levels.append(Level.create_from_soup(BeautifulSoupFactory.create_from_string(str(level))))

        return levels
