import schedule
import sys
import time
from datetime import date, datetime
import requests
from db import db

scored_data = {}
allowed_data = {}

def print_out(value):
    print(value)
    sys.stdout.flush()

def put(which, team, date, inning, runs):
    if team not in which:
        which[team] = {date: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}}
    if date not in which[team]:
        which[team][date] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    if inning not in which[team][date]:
        which[team][date][inning] = 0
    
    which[team][date][inning] += runs

def process_game(game, date):
    data = requests.get("https://statsapi.mlb.com" + game["link"]).json()
    home_id = game["teams"]["home"]["team"]["id"]
    away_id = game["teams"]["away"]["team"]["id"]

    for inning in data["liveData"]["linescore"]["innings"]:
        if "runs" in inning["home"]:
            put(scored_data, home_id, date, inning["num"], inning["home"]["runs"])
            put(allowed_data, away_id, date, inning["num"], inning["home"]["runs"])

        if "runs" in inning["away"]:
            put(scored_data, away_id, date, inning["num"], inning["away"]["runs"])
            put(allowed_data, home_id, date, inning["num"], inning["away"]["runs"])



def process_dates(dates):
    print_out("processing dates")
    for date in dates:
        string_date = date["date"]
        print_out(f"processing games on {string_date}")

        for game in date["games"]:
            process_game(game, string_date)


def save_data():
    print_out("saving data to mongodb")
    for teamId, dates in scored_data.items():
        team_collection = db[str(teamId)]

        for date, innings in dates.items():
            replacement = {str(key): value for key, value in innings.items()}
            replacement["date"] = datetime.strptime(date, "%Y-%m-%d")

            team_collection.replace_one({"date": replacement["date"], "allowed": False}, replacement, True)

        if teamId in allowed_data:
            for date, innings in allowed_data[teamId].items():
                replacement = {str(key): value for key, value in innings.items()}
                replacement["date"] = datetime.strptime(date, "%Y-%m-%d")
                replacement["allowed"] = True

                team_collection.replace_one({"date": replacement["date"], "allowed": True}, replacement, True)


def get_all_data():
    print_out("getting all data")
    start_date = str(date(date.today().year, 1, 1))
    end_date = str(date.today())
    schedule = requests.get(f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={start_date}&endDate={end_date}&gameType=R").json()

    process_dates(schedule["dates"])
    save_data()
    print_out("done processing")


get_all_data()
schedule.every().day.at("01:38").do(get_all_data)

while True:
    schedule.run_pending()
    time.sleep(60)