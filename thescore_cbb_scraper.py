from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from game import Game

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
      except:
        self.driver.find_element(By.XPATH, "//div[@class='ScrollMenu__scrollButton--1LXfu ScrollMenu__scrollLeft--JgF9U']").click()
      else:
        break
  
  
  def get_days_games(self, key: dict[str, str]) -> list[Game]:
    action = ActionChains(self.driver)
    # TODO Get the date listed at the top of this page listed at dayOfWeek, MMM DD
    games_element: list[WebElement] = WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='Events__eventCardGrid--3NUse']/div[@class='Events__card--2w5uF']")))
    for game in games_element:
      action.move_to_element(game)
      game.click()
      game_data: Game = self.get_game_data(key)

  def get_game_data(self, key: dict[str, str], date: str) -> Game:
    matchup_element: WebElement = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='MatchupSection__matchupSection--GJdi0']")))
    team_elements: list[WebElement] = matchup_element.find_elements(By.XPATH, "./div/div[last()]/span/a")
    for i, team_element in enumerate(team_elements):
      if i == 0:
        away_team: str = team_element.accessible_name[:team_element.accessible_name.index(" ")]
      elif i == 1:
        home_team: str = team_element.accessible_name[:team_element.accessible_name.index(" ")]
    # TODO Create Game instance and then populate rest of the items
    
    