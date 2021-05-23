import json
from typing import List

from src.PsnProfiles.ProfileSummary import ProfileSummary
from src.PsnProfiles.Trophy import Trophy
from src.PsnProfiles.Milestone import Milestone
from src.PsnProfiles.Game import Game
from src.PsnProfiles.Level import Level


class Profile:
    def __init__(self, name: str, country: str, summary: ProfileSummary, recent_trophies: List[Trophy],
                 rarest_trophies: List[Trophy], milestones: List[Milestone], games: List[Game],
                 trophy_cabinet: List[Trophy], level_history: List[Level]):
        self.__name = name
        self.__country = country
        self.__summary = summary
        self.__recent_trophies = recent_trophies
        self.__rarest_trophies = rarest_trophies
        self.__milestones = milestones
        self.__games = games
        self.__trophy_cabinet = trophy_cabinet
        self.__level_history = level_history

    def get_name(self) -> str:
        return self.__name

    def get_country(self) -> str:
        return self.__country

    def get_summary(self) -> ProfileSummary:
        return self.__summary

    def get_recent_trophies(self) -> List[Trophy]:
        return self.__recent_trophies

    def get_rarest_trophies(self) -> List[Trophy]:
        return self.__rarest_trophies

    def get_milestones(self) -> List[Milestone]:
        return self.__milestones

    def get_games(self) -> List[Game]:
        return self.__games

    def get_trophy_cabinet(self) -> List[Trophy]:
        return self.__trophy_cabinet

    def get_level_history(self) -> List[Level]:
        return self.__level_history

    def to_json(self):
        return json.dumps({
            "name": self.get_name(),
            "country": self.get_country(),
            "summary": self.get_summary(),
            "recent_trophies": self.get_recent_trophies(),
            "rarest_trophies": self.get_rarest_trophies(),
            "milestones": self.get_milestones(),
            "games": self.get_games(),
            "trophy_cabinet": self.get_trophy_cabinet(),
            "level_history": self.get_level_history(),
        }, default=lambda o: o.__dict__,
            sort_keys=False, indent=2)
