import hockey_scraper as nhl
import datetime as dt
import requests
import sys
import time


# From thesportsdb

TeamIDs = {"ANA": 134846, "ARI": 134847, "BOS": 134830, "BUF": 134831, "CAR": 134838, "CBJ": 134839, "CGY": 134848, "CHI": 134854, "COL": 134855, 
           "DAL": 134856, "DET": 134832, "EDM": 134849, "FLA": 134833, "L.A": 134852, "MIN": 134857, "MTL": 134834, "N.J": 134840, "NSH": 134858, 
           "NYI": 134841, "NYR": 134842, "OTT": 134835, "PHI": 134843, "PIT": 134844, "SEA": 140082, "S.J": 134853, "STL": 134859, "T.B": 134836, 
           "TOR": 134837, "VAN": 134850, "VGK": 135913, "WPG": 134851, "WSH": 134845}

TeamNames = {"ANA": "Anaheim Ducks", "ARI": "Arizona Coyotes", "BOS": "Boston Bruins", "BUF": "Buffalo Sabres", "CAR": "Carolina Hurricanes", 
             "CBJ": "Columbus Blue Jackets", "CGY": "Calgary Flames", "CHI": "Chicago Blackhawks", "COL": "Colorado Avalanche", 
             "DAL": "Dallas Stars", "DET": "Detroit Red Wings", "EDM": "Edmonton Oilers", "FLA": "Florida Panthers", "L.A": "Los Angeles Kings", 
             "MIN": "Minnesota Wild", "MTL": "Montreal Canadiens", "N.J": "New Jersey Devils", "NSH": "Nashville Predators", 
             "NYI": "New York Islanders", "NYR": "New York Rangers", "OTT": "Ottawa Senators", "PHI": "Philadelphia Flyers", 
             "PIT": "Pittsburgh Penguins", "SEA": "Seattle Kraken", "S.J": "San Jose Sharks", "STL": "St. Louis Blues", "T.B": "Tampa Bay Lightning", 
             "TOR": "Toronto Maple Leafs", "VAN": "Vancouver Canucks", "VGK": "Vegas Golden Knights", "WPG": "Winnipeg Jets", "WSH": "Washington Capitals"}

# Works!
# https://www.thesportsdb.com/api/v1/json/2/searchevents.php?e=Ottawa_Senators_vs_Chicago_Blackhawks

sdb_url_base = "https://www.thesportsdb.com/api/v1/json/2/searchevents.php?e="

DATE = 1
HOME = 3
AWAY = 4
START_TIME = 5
HOME_SCORE = 6
AWAY_SCORE = 7
STATUS = 8  # Final, Preview and Live

Time_Correction_Hours = 4
Time_Correction_Minutes = 0

def print_game(game):
    start_time = str(game[START_TIME] - dt.timedelta(hours=Time_Correction_Hours, minutes=Time_Correction_Minutes))
    if(game[STATUS] == "Preview"):
        print(f'{game[HOME]}  -  {game[AWAY]}')
        print("Home Team = " + game[HOME] + " Away Team = " + game[AWAY] + " Date = " + game[DATE] + " Start Time = " + start_time)
        event_url = sdb_url_base + str(TeamNames[game[HOME]] + " vs " + TeamNames[game[AWAY]])
        resp_check = False
        while(not resp_check):
            try:
                response = requests.get(event_url).json()
                resp_check = True
            except ValueError:
                time.sleep(0.5)


        event_id = response['event'][0]['idEvent']
        event_date = response['event'][0]['dateEvent']
        print("Event ID = " + str(event_id))
        print()
    elif(game[STATUS] == "Live"):
       print("Game is Live")
       print("Home Team = " + game[HOME] + " Away Team = " + game[AWAY] + " Date = " + game[DATE] + " Start Time = " + start_time)
       print()
    elif(game[STATUS] == "Final"):
       print("Game is Final")
       print("Home Team = " + game[HOME] + " Away Team = " + game[AWAY] + " Date = " + game[DATE] + " Start Time = " + start_time)
       print()


if len(sys.argv) == 1:
    input_days = 1
else:
    input_days = int(sys.argv[1])

today_dt = dt.date.today()
date_check = today_dt - dt.timedelta(days=1)
xdays_dt = str(today_dt + dt.timedelta(days=input_days-1))
today_dt = str(today_dt)


df = nhl.scrape_schedule(today_dt, xdays_dt)
print()

Total_Games_In_Day = 0

for i,game in df.iterrows():
    current_day = dt.datetime.fromisoformat(game[DATE])
    if(date_check != current_day):
        if(Total_Games_In_Day != 0):
            print("TOTAL GAMES = " + str(Total_Games_In_Day))
            Total_Games_In_Day = 0
        print()
        print("                           " + game[DATE] + "                           ")
        print()
        date_check = current_day
    print_game(game)
    
    Total_Games_In_Day += 1
print("TOTAL GAMES = " + str(Total_Games_In_Day))






#print(f'"Mikey moo: {home} ')