import datetime

class Game:

  def __init__(self, date: str, home_team: str, away_team: str) -> None:
    self._date = date
    self._home = home_team
    self._away = away_team
    self._favorite = ""
    self._underdog = ""
    self._home_score = ""
    self._away_score = ""

  @property
  def date(self):
    return self._date

  @date.setter
  def date(self, value):
    self._date = value

  @property
  def home(self):
    return self._home

  @home.setter
  def home(self, value):
    self._home = value

  @property
  def away(self):
    return self._away

  @away.setter
  def away(self, value):
    self._away = value

  @property
  def favorite(self):
    return self._favorite

  @favorite.setter
  def favorite(self, value):
    self._favorite = value

  @property
  def underdog(self):
    return self._underdog

  @underdog.setter
  def underdog(self, value):
    self._underdog = value

  @property
  def home_score(self):
    return self._home_score

  @home_score.setter
  def home_score(self, value):
    self._home_score = value

  @property
  def away_score(self):
    return self._away_score

  @away_score.setter
  def away_score(self, value):
    self._away_score = value

