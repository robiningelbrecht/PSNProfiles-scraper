def to_int(a: str) -> int:
    try:
        return int(a.replace(",", "").replace("(", "").replace(")", ""))
    except ValueError:
        return 0


def extract_game_from_uri(uri: str) -> str:
    # /trophies/10034-foxyland/PSNname
    game_unfiltered = uri.split('/')[2]
    return game_unfiltered.replace(game_unfiltered.split('-')[0] + "-", "").replace("-", " ").title()
