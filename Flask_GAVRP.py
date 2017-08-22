
from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
from io import StringIO
from dataProcess import MainProcess
from algorithmModel import optimization


app = Flask(__name__)
api = Api(app)



class SchedulingSolution(Resource):
    def __init__(self):
        pass

    def post(self):
        dataProcessed = MainProcess(request)
        result = optimization(dataProcessed)
        return result




api.add_resource(SchedulingSolution, '/dynamic_scheduling')

if __name__ == '__main__':
    app.run(debug=True)
