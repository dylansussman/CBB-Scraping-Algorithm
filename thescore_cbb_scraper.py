from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
import openpyxl as xls

from game import Game

OUTPUT_FILE_NAME = "CBB_scores_and_data.xlsx"
OUTPUT_SHEET_NAME = "Game Data"

class thescoreCbbScraper:

  def __init__(self) -> None:
    self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    self._driver.get("https://www.thescore.com/ncaab/events")

  @property
  def driver(self):
    return self._driver

  @driver.setter
  def driver(self, value):
    self._driver = value

  def start_from_date(self, date: str):
    date_element: WebElement = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, f"//div[@id='{date}']")))
    while True:
      try:
        date_element.click()
        time.sleep(1)
      except:
        self.driver.find_element(By.XPATH, "//div[@class='ScrollMenu__scrollButton--1LXfu ScrollMenu__scrollLeft--JgF9U']").click()
        time.sleep(1)
      else:
        break

  # If there is another day of games to get, i.e., next day is not TODAY:
      # Click on the next day and return True
      # Otherwise return False
  def next_day(self, date: str) -> tuple[bool, str]:
    add_for_timedelta = 1
    year, month, day = date.split("-")
    actual_date = datetime.date(int(year), int(month), int(day))
    while True:
      next_day = (actual_date + datetime.timedelta(add_for_timedelta)).strftime("%Y-%m-%d")
      try:
        date_element: WebElement = self.driver.find_element(By.XPATH, f"//div[@id='{next_day}']")
      except:
        add_for_timedelta += 1
      else:
        break

    if date_element.accessible_name != "TODAY":
      date_element.click()
      return (True, next_day)
    else:
      return (False, "")

  def get_days_games(self, key: dict[str, str]) -> list[Game]:
    date_element: WebElement = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='Events__date--2cujl col-xs-6 col-md-6']")))
    date: str = date_element.text

    games_element: list[WebElement] = WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='Events__eventCardGrid--3NUse']/div[@class='Events__card--2w5uF']")))
    games: list[Game] = []
    original_tab = self.driver.current_window_handle
    for game in games_element:
      game_link: str = game.find_element(By.XPATH, ".//a").get_attribute("href")
      game_data: Game = None
      while game_data == None:
        self.driver.switch_to.new_window('tab')
        self.driver.get(game_link)
        game_data = self.get_game_data(key, date)
        self.driver.close()
        self.driver.switch_to.window(original_tab)
      # game_data == "" signifies a game was canceled; don't wanna add it then
      if game_data != "":
        games.append(game_data)
      time.sleep(1)
    return games

  def get_game_data(self, key: dict[str, str], date: str) -> Game:
    try:
      matchup_element: WebElement = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='MatchupSection__matchupSection--GJdi0']")))
    except:
      return None
    team_elements: list[WebElement] = matchup_element.find_elements(By.XPATH, "./div/div[last()]/span/a")
    home_team, home_score, away_team, away_score = "", "", "", ""
    for i, team_element in enumerate(team_elements):
      if i == 0:
        away_team, away_score = self.get_team_name_and_score(key, team_element)
      elif i == 1:
        home_team, home_score = self.get_team_name_and_score(key, team_element)
    # Accounts for canceled games
    if home_team == "" or away_team == "" or home_score == "" or away_score == "":
      return ""
    game_data: Game = Game(date, home_team, away_team)
    game_data.home_score = home_score
    game_data.away_score = away_score

    spread_column_element: WebElement = self.driver.find_element(By.XPATH, "//div[@class='NCAABMatchup__desktopView--2-nvq col-sm-4 NCAABMatchup__column--2MRi4']")
    
    # Account for games that don't have a spread
    try:
      closing_odds: str = spread_column_element.text[spread_column_element.text.index("Closing Odds"):]
      spread: str = ""
      if "o/u" in closing_odds:
        spread = closing_odds[closing_odds.index("\n")+1:closing_odds.index(",")]
      else:
        spread = closing_odds[closing_odds.index("\n")+1:]
        spread = spread[:spread.index("\n")]
      favorite_abbrev: str = spread[:spread.index(" ")]
      favorite_full: str = key.get(favorite_abbrev)
      underdog = game_data.away if favorite_full == game_data.home else game_data.home      
    except:
      game_data.spread = "N/A"
      game_data.favorite = "N/A"
      game_data.underdog = "N/A"
    else:
      try:
        game_data.spread = spread.replace(favorite_abbrev, favorite_full)
      except:
        game_data.spread = spread
        game_data.favorite = "No translation from spread abbreviation"
        game_data.underdog = "No translation from spread abbreviation"
      else:
        game_data.favorite = favorite_full
        game_data.underdog = underdog

    return game_data
        
  def get_team_name_and_score(self, key: dict[str, str], team_element: WebElement) -> tuple[str, str]:
    team_element_text: str = team_element.text
    team: str = team_element_text[:team_element_text.index("\n")]
    team = team[team.index(" ")+1:] if "(" in team else team
    team = key.get(team) if key.get(team) else team
    # Account for games that get canceled (no score present)
    try:
      team_score = int(team_element.find_element(By.XPATH, "./div/div[last()]").text)
    except:
      return ("", "")
    return (team, team_score)
  
  def print_days_games(self, games: Game):
    wb: Workbook = xls.load_workbook(OUTPUT_FILE_NAME)
    sheet: Worksheet = wb[OUTPUT_SHEET_NAME]
    for game in games:
      sheet.append(list(vars(game).values()))
    wb.save(OUTPUT_FILE_NAME)

  def change_to_all_conferences(self):
    dropdown_elemet: WebElement = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='EventsDropdown__dropdownButton--2k8XP']")))
    dropdown_elemet.click()
    self.driver.find_element(By.XPATH, "//ul[@class='EventsDropdown__dropdownList--Zij-i']/descendant::div[text()='All Conferences']").click()  