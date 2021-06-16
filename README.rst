|pypi| |unit-tests|

Python PSNProfiles scraper
===========================
Scrape PSNProfiles profile pages using a Python CLI script

.. |pypi| image:: https://img.shields.io/pypi/v/psnprofiles_scraper.svg
   :target: https://pypi.org/project/psnprofiles_scraper/

.. |unit-tests| image:: https://github.com/robiningelbrecht/psnprofiles-scraper/actions/workflows/python-app.yml/badge.svg
   :target: https://github.com/robiningelbrecht/psnprofiles-scraper

Installation
-------------

Install Python3 then in a terminal:

- Run ``git clone https://github.com/robiningelbrecht/psnprofiles-scraper``
- Run ``python -m pip install -r requirements.txt``
- Run ``python main.py YourUserName (-d)``

Or install from PyPi

.. code-block:: shell

    pip install psnprofiles_scraper

Usage
------

.. code-block:: python

    from psnprofiles_scraper.src.PsnProfilesScraper import PsnProfilesScraper

    scraper = PsnProfilesScraper()
    print(scraper.get_profile("YourUsername", False).to_json())

Example JSON output
-------------------

.. code-block:: json

    {
      "name": "YourUserName",
      "country": "Belgium",
      "summary": {
        "level": 354,
        "trophies": {
          "total": 2578,
          "grade": {
            "platinum": 66,
            "gold": 576,
            "silver": 583,
            "bronze": 1353
          },
          "rarity": {
            "ultra_rare": 4,
            "very_rare": 10,
            "rare": 39,
            "uncommon": 406,
            "common": 2119
          }
        },
        "points": {
          "platinum": 19800,
          "gold": 51840,
          "silver": 17490,
          "bronze": 20295,
          "total": 109425
        },
        "games": {
          "played": 165,
          "completed": 61,
          "platforms": {
            "PS5": 4,
            "PS4": 157,
            "PS3": 0,
            "PS Vita": 0,
            "Multiplatform": 4
          },
          "ranks": {
            "S": 61,
            "A": 12,
            "B": 11,
            "C": 14,
            "D": 12,
            "E": 36,
            "F": 19
          }
        },
        "stats": {
          "completion": {
            "average": "56.92%",
            "80% - 100%": 66,
            "60% - 79.99%": 15,
            "40% - 59.99%": 12,
            "20% - 39.99%": 14,
            "0% - 19.99%": 58
          },
          "unearned_trophies": 2685,
          "trophies_per_day": "2.25",
          "views": 501,
          "world_rank": 112163,
          "country_rank": 1486
        }
      },
      "recent_trophies": [
        {
          "title": "Luna's Apprentice",
          "game": "Concrete Genie",
          "rarity_percentage": "90.93%",
          "rarity_label": "Common",
          "grade": "bronze",
          "icon_uri": "https://i.psnprofiles.com/games/e17609/trophies/2Se1a8c6.png"
        },
        {
          "title": "Path of the Stars",
          "game": "Shadow of the Tomb Raider",
          "rarity_percentage": "94.29%",
          "rarity_label": "Common",
          "grade": "bronze",
          "icon_uri": "https://i.psnprofiles.com/games/e17609/trophies/2Se1a8c6.png"
        }
      ],
      "rarest_trophies": [
        {
          "title": "Blue Series clear",
          "game": "Trackmania Turbo",
          "rarity_percentage": "3.28%",
          "rarity_label": "Ultra Rare",
          "grade": "silver",
          "icon_uri": "https://i.psnprofiles.com/games/4d4c0b/trophies/17S023638.png"
        },
        {
          "title": "Stadium Blue clear",
          "game": "Trackmania Turbo",
          "rarity_percentage": "3.45%",
          "rarity_label": "Ultra Rare",
          "grade": "bronze",
          "icon_uri": "https://i.psnprofiles.com/games/4d4c0b/trophies/33Sd54d43.png"
        }
      ],
      "milestones": [
        {
          "trophy": "Dragon Break Classic master",
          "game": "Dragon Break Classic",
          "description": "Latest Platinum",
          "date": "6 days ago"
        },
        {
          "trophy": "Projectile Pro",
          "game": "Immortals Fenyx Rising",
          "description": "2,500th Trophy",
          "date": "4 weeks ago"
        },
        {
          "trophy": "Platinum Paw",
          "game": "Thunder Paw",
          "description": "50th Platinum",
          "date": "8 months ago"
        },
        {
          "trophy": "Thank you Mr. Kitty!",
          "game": "Red Bow",
          "description": "2,000th Trophy",
          "date": "8 months ago"
        }
      ],
      "games": [
        {
          "title": "Assassin's Creed Syndicate",
          "trophy_stats": {
            "obtained": "32",
            "total": "57",
            "gold": "2",
            "silver": "5",
            "bronze": "25",
            "completion": "56%"
          },
          "platform": "PS4",
          "rank": "B",
          "has_earned_platinum": false,
          "thumbnail_uri": "https://i.psnprofiles.com/games/79c5a1/Sd24d1d.png"
        },
        {
          "title": "My Name is Mayo",
          "trophy_stats": {
            "obtained": "51",
            "total": "51",
            "gold": "4",
            "silver": "0",
            "bronze": "46",
            "completion": "100%"
          },
          "platform": "PS4",
          "rank": "S",
          "has_earned_platinum": true,
          "thumbnail_uri": "https://i.psnprofiles.com/games/79c5a1/Sd24d1d.png"
         }
      ],
      "trophy_cabinet": [
        {
          "title": "Be Yourself",
          "game": "Marvel's Spider-Man: Miles Morales",
          "rarity_percentage": "56.11%",
          "rarity_label": "Common",
          "grade": "platinum",
          "icon_uri": "https://i.psnprofiles.com/games/e17609/trophies/2Se1a8c6.png"
        },
        {
          "title": "Viking Legend",
          "game": "Assassin's Creed Valhalla",
          "rarity_percentage": "15.91%",
          "rarity_label": "Rare",
          "grade": "platinum",
          "icon_uri": "https://i.psnprofiles.com/games/e17609/trophies/2Se1a8c6.png"
        }
      ],
      "level_history": [
        {
          "level": 20,
          "game": {
            "title": "Assassins Creed Syndicate",
            "thumbnail_uri": "https://i.psnprofiles.com/games/c2af51/S7d1b26.png"
          },
          "trophy": {
            "title": "Bare-Knuckle Champion",
            "description": "Win three different Fight Clubs.",
            "icon_uri": "https://i.psnprofiles.com/games/c2af51/trophies/16Sa76145.png"
          },
          "date": "12th May 2018 10:54:10 AM"
        },
        {
          "level": 10,
          "game": {
            "title": "Assassins Creed Iv Black Flag",
            "thumbnail_uri": "https://i.psnprofiles.com/games/cc3b08/S359338.png"
          },
          "trophy": {
            "title": "Barfly",
            "description": "Unlock all taverns.",
            "icon_uri": "https://i.psnprofiles.com/games/cc3b08/trophies/36Sbcace5.png"
          },
          "date": "29th Apr 2018 9:12:16 AM"
        }
      ]
    }

Disclaimer
----------

This app and its creator have no affiliation with PSNProfiles or the PlayStation Network/PlayStation beyond the creator's use of both services.
