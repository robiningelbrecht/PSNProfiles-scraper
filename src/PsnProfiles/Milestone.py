import json


class Milestone:
    def __init__(self, title: str, game: str, description: str, date: str):
        self.title = title
        self.game = game
        self.description = description
        self.date = date

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)
