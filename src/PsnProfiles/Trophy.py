import json


class Trophy:
    def __init__(self, title: str, game: str, rarity_percentage: str, rarity_label: str, grade: str):
        self.title = title
        self.game = game
        self.rarity_percentage = rarity_percentage
        self.rarity_label = rarity_label
        self.grade = grade

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)
