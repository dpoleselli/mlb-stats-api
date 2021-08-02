from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import requests


app = Flask(__name__)
api = Api(app)
CORS(app, origins="http://localhost:3000")

class Stats(Resource):
    def get(self):
        runs_scored = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        runs_allowed = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        total_scored = 0
        total_allowed = 0
        team_id = request.args.get("teamId")
        team_id = int(team_id)
        start_date = request.args.get("startDate")
        end_date = request.args.get("endDate")

        schedule = requests.get(f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={start_date}&endDate={end_date}&teamId={team_id}&gameType=R")
        schedule = schedule.json()

        for date in schedule["dates"]:
            for game in date["games"]:
                home_away = "home" if game["teams"]["home"]["team"]["id"] == team_id else "away"
                home_away_opposite = "home" if home_away == "away" else "away"
                
                data = requests.get("https://statsapi.mlb.com" + game["link"])
                data = data.json()

                for inning in data["liveData"]["linescore"]["innings"]:
                    # runs scored
                    if "runs" in inning[home_away]:
                        # handle extra innings if necessary
                        if inning["num"] not in runs_scored:
                            runs_scored[inning["num"]] = 0

                        runs_scored[inning["num"]] = runs_scored[inning["num"]] + inning[home_away]["runs"]
                        total_scored = total_scored + inning[home_away]["runs"]
                    
                    # runs allowed
                    if "runs" in inning[home_away_opposite]:
                        # handle extra innings if necessary
                        if inning["num"] not in runs_allowed:
                            runs_allowed[inning["num"]] = 0

                        runs_allowed[inning["num"]] = runs_allowed[inning["num"]] + inning[home_away_opposite]["runs"]
                        total_allowed = total_allowed + inning[home_away_opposite]["runs"]
        return {"scored": runs_scored, "allowed": runs_allowed, "total_scored": total_scored, "total_allowed": total_allowed}, 200 

api.add_resource(Stats, '/stats')


if __name__ == '__main__':
    app.run()  # run our Flask app