import json
from src.PsnProfiles.ProfileSummary import ProfileSummary


class Profile:
    def __init__(self, name: str, summary: ProfileSummary, recent_trophies: list, milestones: list, games: list):
        self.name = name
        self.summary = summary
        self.recent_trophies = recent_trophies
        self.milestones = milestones
        self.games = games

    def get_name(self) -> str:
        return self.name

    def get_summary(self) -> ProfileSummary:
        return self.summary

    def get_recent_trophies(self) -> list:
        return self.recent_trophies

    def get_milestones(self) -> list:
        return self.milestones

    def get_games(self) -> list:
        return self.games

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)
