from typing import List

from psnprofiles_scraper.src.ProgressBar import ProgressBar
from psnprofiles_scraper.src.BeautifulSoupFactory import BeautifulSoupFactory
from psnprofiles_scraper.src.PsnProfiles.Profile import Profile
from psnprofiles_scraper.src.PsnProfiles.ProfileSummary import ProfileSummary
from psnprofiles_scraper.src.PsnProfiles.Trophy import Trophy
from psnprofiles_scraper.src.PsnProfiles.Milestone import Milestone
from psnprofiles_scraper.src.PsnProfiles.Game import Game
from psnprofiles_scraper.src.PsnProfiles.Level import Level


class PsnProfilesScraper:
    def __init__(self):
        self.__progress_bar = ProgressBar()

        self.__psn_name = None
        self.__soup_profile = None
        self.__soup_games = None
        self.__soup_level_history = None
        self.__soup_stats = None

    # Returns a full PSN profile object.
    def get_profile(self, psn_name: str, detailed: bool) -> Profile:
        self.__progress_bar.update_message("Initializing")
        self.__psn_name = psn_name

        self.__soup_games = BeautifulSoupFactory.create_for_games(self.__psn_name)
        games = self.__get_games()

        if detailed:
            # Update max of progress bar and fetch each game separately.
            self.__progress_bar.max = self.__progress_bar.max + len(games)
            for game in games:
                self.__progress_bar.update_message("Fetching " + game.title)
                if not game.uri:
                    self.__progress_bar.next()
                    continue

                # Update game instance and populate with details.
                game.populate_details_from_soup(BeautifulSoupFactory.create_from_link(game.uri))
                self.__progress_bar.next()

        # Fetch profile data.
        self.__progress_bar.update_message("Fetching profile")
        self.__soup_profile = BeautifulSoupFactory.create_for_profile(self.__psn_name)
        self.__progress_bar.next()

        self.__soup_level_history = BeautifulSoupFactory.create_for_level_history(self.__psn_name)
        self.__progress_bar.next()

        self.__soup_stats = BeautifulSoupFactory.create_for_stats(self.__psn_name)
        self.__progress_bar.next()

        country = ""
        if self.__soup_profile.select("img#bar-country"):
            country = BeautifulSoupFactory.create_from_string(
                self.__soup_profile.select("img#bar-country")[0]["title"]).text

        # Extract profile summary.
        profile_summary = ProfileSummary.create_from_soup(
            BeautifulSoupFactory.create_from_string(str(self.__soup_profile) + str(self.__soup_stats)))
        self.__progress_bar.next()

        # Extract recent trophies.
        recent_trophies = self.__get_recent_trophies()
        self.__progress_bar.next()

        # Extract rarest trophies.
        rarest_trophies = self.__get_rarest_trophies()
        self.__progress_bar.next()

        # Extract milestones.
        milestones = self.__get_milestones()
        self.__progress_bar.next()

        # Extract trophy cabinet.
        trophy_cabinet = self.__get_trophy_cabinet()
        self.__progress_bar.next()

        # Extract level history.
        level_history = self.__get_level_history()
        self.__progress_bar.next()

        profile = Profile(
            self.__psn_name,
            country,
            profile_summary,
            recent_trophies,
            rarest_trophies,
            milestones,
            games,
            trophy_cabinet,
            level_history
        )

        self.__progress_bar.update_message("Complete")
        self.__progress_bar.finish()
        return profile

    # Scrapes and returns the recent trophies.
    def __get_recent_trophies(self) -> List[Trophy]:
        if not self.__soup_profile.select("ul#recent-trophies"):
            return []

        return list(map(lambda trophy: Trophy.create_from_alternative_soup(
            BeautifulSoupFactory.create_from_string(str(trophy))),
                        self.__soup_profile.select("ul#recent-trophies")[0].find_all('li')))

    # Scrapes and returns trophy cabinet
    def __get_rarest_trophies(self) -> List[Trophy]:
        if not self.__soup_profile.find("h3", text="Rarest Trophies"):
            self.__progress_bar.next()
            return []

        if not self.__soup_profile.select('div.sidebar div.box.no-top-border table'):
            self.__progress_bar.next()
            return []

        return list(
            map(lambda trophy: Trophy.create_from_soup(BeautifulSoupFactory.create_from_string(str(trophy))),
                self.__soup_profile.select('div.sidebar div.box.no-top-border table')[0].find_all("tr")))

    # Scrapes and returns trophy cabinet
    def __get_trophy_cabinet(self) -> List[Trophy]:
        if not self.__soup_profile.find("h3", text="Trophy Cabinet"):
            self.__progress_bar.next()
            return []

        if not self.__soup_profile.select("div.sidebar table.box.zebra"):
            self.__progress_bar.next()
            return []

        return list(
            map(lambda trophy: Trophy.create_from_soup(BeautifulSoupFactory.create_from_string(str(trophy))),
                self.__soup_profile.select("div.sidebar table.box.zebra")[0].find_all("tr")))

    # Scrapes and returns milestones.
    def __get_milestones(self) -> List[Milestone]:
        if not self.__soup_profile.find("h3", text="Trophy Milestones"):
            self.__progress_bar.next()
            return []

        milestones_table = self.__soup_profile.find("h3", text="Trophy Milestones").find_next()

        return list(
            map(lambda milestone: Milestone.create_from_soup(BeautifulSoupFactory.create_from_string(str(milestone))),
                milestones_table.find_all("tr")))

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
            self.__progress_bar.next()
            return []

        return list(map(lambda level: Level.create_from_soup(BeautifulSoupFactory.create_from_string(str(level))),
                        self.__soup_level_history.select("table.box.zebra")[0].find_all("tr")))
