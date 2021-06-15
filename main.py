import argparse
import sys

from src.InvalidProfileError import InvalidProfileError
from src.PsnProfilesScraper import PsnProfilesScraper

if __name__ == "__main__":
    # Initiate the parser
    parser = argparse.ArgumentParser(description='Scrape a PSN profile and return it in proper JSON.')
    parser.add_argument('username', type=str, help='PSN username to scrape')
    parser.add_argument('-d', '--detailed', action='store_true', help='Fetch detailed game info (takes longer to process)')
    # Read arguments from the command line
    args = parser.parse_args()

    try:
        scraper = PsnProfilesScraper(args.username)
        print(scraper.get_profile().to_json())
    except InvalidProfileError:
        print("\n\"%s\" is not a valid PSN profile" % args.username, file=sys.stderr)
