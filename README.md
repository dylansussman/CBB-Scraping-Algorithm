# README

# Table of Contents
1. [Running Options](#Running-Options)

## Running Options
To run the program to scrape for the current day's game stats, run the following command:

```$ python3 main.py```

To run the program to create a new teams abbreviation key before scraping, first make sure the constant `TEAMS_KEY_INPUT_FILE_NAME` in `main.py` is initialized to the correct path and file name where the key is being read in from.  
Then run the following command:

```$ python3 main.py create-teams-key```

To run the program to scrape for game stats starting from a specific date, run the following command:  

```$ python3 main.py --date=YYYY-MM-DD```


