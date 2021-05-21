from PsnScraper import PsnScraper

scraper = PsnScraper("MyPsnName")

print(scraper.get_profile().to_json())
