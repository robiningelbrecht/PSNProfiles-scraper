# Python PSNProfiles scraper
Scrape PSNProfiles pages using a Python CLI script

## Usage

Install Python3 then in a terminal:
1. Run `python -m pip install -r requirements.txt`
2. Run `python main.py`
3. Fill out PSN username (= case sensitive)

## Example JSON output

```json
{
  "name": "Your-UserName",
  "summary": {
    "level": 354,
    "trophies": {
      "total": 2577,
      "grade": {
        "platinum": 66,
        "gold": 576,
        "silver": 583,
        "bronze": 1352
      },
      "rarity": {
        "ultra_rare": 4,
        "very_rare": 10,
        "rare": 39,
        "uncommon": 406,
        "common": 2118
      }
    },
    "stats": {
      "games_played": 165,
      "completed_games": 61,
      "completion": "56.91%",
      "unearned_trophies": 2686,
      "trophies_per_day": "2.25",
      "views": 490,
      "world_rank": 112045,
      "country_rank": 1486
    }
  },
  "recent_trophies": [
    {
      "title": "Luna's Apprentice",
      "game": "Concrete Genie",
      "rarity_percentage": "90.93%",
      "rarity_label": "Common",
      "grade": "bronze"
    },
    {
      "title": "Path of the Stars",
      "game": "Shadow of the Tomb Raider",
      "rarity_percentage": "94.29%",
      "rarity_label": "Common",
      "grade": "bronze"
    }
  ],
  "milestones": [
    {
      "title": "Dragon Break Classic master",
      "game": "Dragon Break Classic",
      "description": "Latest Platinum",
      "date": "6 days ago"
    },
    {
      "title": "Projectile Pro",
      "game": "Immortals Fenyx Rising",
      "description": "2,500th Trophy",
      "date": "4 weeks ago"
    },
    {
      "title": "Platinum Paw",
      "game": "Thunder Paw",
      "description": "50th Platinum",
      "date": "8 months ago"
    },
    {
      "title": "Thank you Mr. Kitty!",
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
      "ranked": "B",
      "has_earned_platinum": false
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
      "ranked": "S",
      "has_earned_platinum": true
     }
  ],
    "trophy_cabinet": [
    {
      "title": "Be Yourself",
      "game": "Marvel's Spider-Man: Miles Morales",
      "rarity_percentage": "56.11%",
      "rarity_label": "Common",
      "grade": "platinum"
    },
    {
      "title": "Viking Legend",
      "game": "Assassin's Creed Valhalla",
      "rarity_percentage": "15.91%",
      "rarity_label": "Rare",
      "grade": "platinum"
    }
  ]    
}
```

## Disclaimer

This app and its creator have no affiliation with PSNProfiles or the PlayStation Network/PlayStation beyond the creator's use of both services.
