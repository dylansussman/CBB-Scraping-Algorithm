import csv
import json

def create_teams_key(file_name: str) -> dict[str, str]:
  key: dict[str, str] = {}
  with open(file_name, "r") as file:
    reader = csv.reader(file)
    for i, line in enumerate(reader):
      if i > 0:
        key.update({line[1]:line[0]})
  with open("teams_key.json", "w") as file:
    file.write(json.dumps(key))