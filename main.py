import sys
from src.InvalidProfileError import InvalidProfileError
from src.PsnProfilesScraper import PsnProfilesScraper

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Required argument \"username\" is missing", file=sys.stderr)
        sys.exit(0)

    psn_username = sys.argv[1]
    try:
        scraper = PsnProfilesScraper(psn_username)
        print(scraper.get_profile().to_json())
    except InvalidProfileError:
        print("\"" + psn_username + "\" is not a valid psn profile", file=sys.stderr)
