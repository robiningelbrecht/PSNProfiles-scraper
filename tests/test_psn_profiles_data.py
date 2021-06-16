from psnprofiles_scraper.src.PsnProfilesScraper import PsnProfilesScraper

scraper = PsnProfilesScraper()
profile = scraper.get_profile("Fluttezuhher", False)


def test_json_structure():
    json = profile.to_json()
    assert "name" in json
    assert "country" in json
    assert "summary" in json
    assert "recent_trophies" in json
    assert "rarest_trophies" in json
    assert "milestones" in json
    assert "games" in json
    assert "trophy_cabinet" in json
    assert "level_history" in json


def test_trophy_count():
    summary = profile.get_summary()

    assert summary.trophies["total"] == sum(summary.trophies["grade"].values())
    assert summary.trophies["total"] == sum(summary.trophies["rarity"].values())


def test_game_count():
    summary = profile.get_summary()

    assert summary.games["played"] == sum(summary.games["platforms"].values())
    assert summary.games["played"] == sum(summary.games["ranks"].values())


def test_points_count():
    summary = profile.get_summary()

    total_points = summary.points["total"]
    summary.points["total"] = 0
    assert total_points == sum(summary.points.values())
