import sys
import json

from create_teams_key import create_teams_key
from thescore_cbb_scraper import thescoreCbbScraper

# NOTE If a new key is being created make sure this relfects the correct path
TEAMS_KEY_INPUT_FILE_NAME = "../Desktop/Template Wid Scraping.csv"

def main(create_key: bool, date: str):
  if create_key:
    create_teams_key(TEAMS_KEY_INPUT_FILE_NAME)
  
  key: dict[str, str]
  with open("teams_key.json", "r") as file:
    key = json.loads(file.read())
  
  scraper: thescoreCbbScraper = thescoreCbbScraper()
  if date:
    scraper.start_from_date(date)
  scraper.get_days_games(key)

if __name__ == '__main__':
  create_key: bool = False
  date: str = ""
  if len(sys.argv) > 1:
    for i, arg in enumerate(sys.argv):
      if i > 0:
        if arg == "create-teams-key":
          create_key = True
        elif "--date" in arg:
          date = arg[arg.index("=") + 1:]
  main(create_key, date)