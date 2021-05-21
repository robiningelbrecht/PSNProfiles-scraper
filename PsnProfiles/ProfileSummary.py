import json


class ProfileSummary:
    def __init__(self, level: int, trophies: dict, stats: dict):
        self.level = level
        self.trophies = trophies
        self.stats = stats

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)
