import os
from flask import Flask, render_template, request
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from datetime import datetime
from flask_basicauth import BasicAuth
import config

app = Flask(__name__)
mysql = MySQL(app)
api = Api(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = config.mysql_user
app.config['MYSQL_PASSWORD'] = config.mysql_pass
app.config['MYSQL_DB'] = 'garden'

@app.route("/")
def main():
    return True

class Log(Resource):
    def get(self):
        return "Hello World!"

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str, required=True, location='json')
        parser.add_argument('pump', type=int, required=True, location='json')
        parser.add_argument('soil', type=int, required=True, location='json')
        parser.add_argument('temperature', type=int, required=True, location='json')
        parser.add_argument('humidity', type=int, required=True, location='json')
        parser.add_argument('rain', type=int, required=True, location='json')
        parser.add_argument('light', type=int, required=True, location='json')

        try:
            args = parser.parse_args(strict=True)
            print(args)
            cur = mysql.connection.cursor()
            query = "INSERT INTO garden.logs (datetime, pump, soil, temperature, humidity, rain, light) VALUES "
            query += "('" + args['datetime'] + "'," + str(args['pump']) + "," + str(args['soil']) + "," + str(args['temperature']) + "," + str(args['humidity']) + "," + str(args['rain']) + "," + str(args['light']) + ");"
            print(query)
            cur.execute(query)
            mysql.connection.commit()
            return 'ok!'
        except:
            pass
            return 'error!'

api.add_resource(Log, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
