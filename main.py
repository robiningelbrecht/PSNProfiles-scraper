import sys
from src.InvalidProfileError import InvalidProfileError
from src.PsnProfilesScraper import PsnProfilesScraper

if __name__ == "__main__":
    psn_username = input("Enter PSN username:")

    try:
        scraper = PsnProfilesScraper(psn_username)
        print(scraper.get_profile().to_json())
    except InvalidProfileError:
        print("\"" + psn_username + "\" is not a valid psn profile", file=sys.stderr)
