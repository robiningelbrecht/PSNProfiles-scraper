import json


class Game:
    def __init__(self, title: str, trophy_stats: dict, platform: str, ranked: str, has_earned_platinum: bool, thumbnail_uri: str):
        self.title = title
        self.trophy_stats = trophy_stats
        self.platform = platform
        self.ranked = ranked
        self.has_earned_platinum = has_earned_platinum
        self.thumbnail_uri = thumbnail_uri

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)
