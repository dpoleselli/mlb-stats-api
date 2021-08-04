from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from dateutil.parser import parse
from db import db

app = Flask(__name__)
api = Api(app)
CORS(app, origins=["http://localhost:3000", "http://mlb-stats.s3-website.us-east-2.amazonaws.com"])


class Stats(Resource):
    def get(self):
        team_id = request.args.get("teamId")
        start_date = parse(request.args.get("startDate"))
        end_date = parse(request.args.get("endDate"))

        runs = db[team_id].aggregate(
            [
                {
                    '$match': {
                        'date': { '$gte': start_date, '$lte': end_date}
                    }
                }, {
                    '$group': {
                        '_id': '$allowed', 
                        '1': {
                            '$sum': '$1'
                        }, 
                        '2': {
                            '$sum': '$2'
                        }, 
                        '3': {
                            '$sum': '$3'
                        }, 
                        '4': {
                            '$sum': '$4'
                        }, 
                        '5': {
                            '$sum': '$5'
                        }, 
                        '6': {
                            '$sum': '$6'
                        }, 
                        '7': {
                            '$sum': '$7'
                        }, 
                        '8': {
                            '$sum': '$8'
                        }, 
                        '9': {
                            '$sum': '$9'
                        }, 
                        '10': {
                            '$sum': '$10'
                        }, 
                        '11': {
                            '$sum': '$11'
                        }, 
                        '12': {
                            '$sum': '$12'
                        }, 
                        '13': {
                            '$sum': '$13'
                        }, 
                        '14': {
                            '$sum': '$14'
                        }, 
                        '15': {
                            '$sum': '$15'
                        }
                    }
                },
                {
                    '$sort': {
                        '_id': 1 # will return runs scored first
                    }
                }
            ]
        )
        runs = list(runs)
       
        if len(runs) > 0:
            runs[0].pop("_id")

            # remove unnecessary extra innings from runs_scored
            for i in range(20, 9, -1):
                x = str(i)
                if x in runs[0]:
                    if runs[0][x] == 0:
                        runs[0].pop(x, None)
                    else:
                        break

        if len(runs) > 1:
            runs[1].pop("_id")

            # remove unnecessary extra innings from runs_allowed
            for i in range(20, 9, -1):
                x = str(i)
                if len(runs) > 1 and x in runs[1]:
                    if runs[1][x] == 0:
                        runs[1].pop(x, None)
                    else:
                        break

        return {"scored": runs[0] if len(runs) > 0 else None, "allowed": runs[1] if len(runs) > 1 else None}, 200 

api.add_resource(Stats, '/stats')


if __name__ == '__main__':
    app.run()  # run our Flask app