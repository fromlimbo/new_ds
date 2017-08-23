
from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
from io import StringIO
from dataProcess import GAVRP_Process
from algorithmModel import optimization


app = Flask(__name__)
api = Api(app)



class SchedulingSolution(Resource):
    def __init__(self):
        pass

    def post(self):
        var_dict = GAVRP_Process(request)
        result = optimization(var_dict)
        return result




api.add_resource(SchedulingSolution, '/dynamic_scheduling')

if __name__ == '__main__':
    app.run(debug=True)
