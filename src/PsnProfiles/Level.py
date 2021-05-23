import json


class Level:

    def __init__(self, level: int, game: str, game_thumbnail_uri: str, trophy_name: str, trophy_description: str, trophy_icon_uri: str, date: str):
        self.level = level
        self.game = game
        self.game_thumbnail_uri = game_thumbnail_uri
        self.trophy_name = trophy_name
        self.trophy_description = trophy_description
        self.trophy_icon_uri = trophy_icon_uri
        self.date = date

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)
