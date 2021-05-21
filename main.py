import sys
from InvalidProfileError import InvalidProfileError
from PsnScraper import PsnScraper

psn_username = input("Enter PSN username:")
scraper = PsnScraper(psn_username)

try:
    print(scraper.get_profile().to_json())
except InvalidProfileError:
    print("\"" + psn_username + "\" is not a valid psn profile", file=sys.stderr)
