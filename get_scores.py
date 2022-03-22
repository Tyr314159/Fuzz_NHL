import hockey_scraper as nhl
import datetime as dt
import sys


DATE = 1
HOME = 3
AWAY = 4
START_TIME = 5
HOME_SCORE = 6
AWAY_SCORE = 7
STATUS = 8  # Final, Preview and Live

if len(sys.argv) == 1:
    input_days = 1
else:
    input_days = int(sys.argv[1])

today_dt = dt.date.today()
date_check = today_dt + dt.timedelta(days=1)
xdays_dt = str(today_dt - dt.timedelta(days=input_days-1))
today_dt = str(today_dt)

df = nhl.scrape_schedule(xdays_dt, today_dt)
print()

Total_Games_In_Day = 0

#print(df)
#print(df[['date', 'home_team', 'away_team', 'start_time', 'home_score',  'away_score', 'status']])

for i,game in df.iterrows():
    if(game[STATUS] == "Final"):
        current_day = dt.datetime.fromisoformat(game[DATE])
        if(date_check != current_day):
            if(Total_Games_In_Day != 0):
                print("TOTAL GAMES = " + str(Total_Games_In_Day))
                Total_Games_In_Day = 0
            print()
            print("                           " + game[DATE] + "                           ")
            print()
            date_check = current_day
        print(game[DATE])
        print("Home Team = " + game[HOME] + " Away Team = " + game[AWAY])
        difference = int(game[HOME_SCORE]) - int(game[AWAY_SCORE])
        if(difference > 0):
            print(game[HOME] + " Wins " + str(game[HOME_SCORE]) + "-" + str(game[AWAY_SCORE]) + " over " + game[AWAY])
        else:
            print(game[AWAY] + " Wins " + str(game[HOME_SCORE]) + "-" + str(game[AWAY_SCORE]) + " over " + game[HOME])
        print()
    #else:
    #   print("Game not Complete")
    
   