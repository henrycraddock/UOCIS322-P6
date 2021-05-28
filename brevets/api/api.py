import os
import flask
from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevetsdb


# Helper functions
def csv_form(l, k):
    headers = list(l[0].keys())
    values = []
    val_str = ""
    num = k if k > 0 else len(l)

    for i in range(num):
        values.append(list(l[i].values()))
    for j in range(len(values)):
        val_str += ",".join(values[j])
        val_str += "\n"
    return ",".join(headers) + "\n" + val_str


def json_form(l, k):
    if k > 0:
        new_l = []
        for i in range(k):
            new_l.append(dict(l[i]))
        return flask.jsonify(new_l)
    return flask.jsonify(l)


# Create resources
class listAll(Resource):
    def get(self, dtype='json'):
        topk = int(request.args.get('top', default=-1))
        items = list(db.timestable.find({}, {'_id': 0, 'index': 0, 'km': 0, 'miles': 0, 'location': 0}))
        if dtype == 'csv':
            return csv_form(items, topk)
        return json_form(items, topk)


class listOpenOnly(Resource):
    def get(self, dtype='json'):
        topk = int(request.args.get('top', default=-1))
        items = list(db.timestable.find({}, {'_id': 0, 'index': 0, 'km': 0, 'miles': 0, 'location': 0, 'close': 0}))
        if dtype == 'csv':
            return csv_form(items, topk)
        return json_form(items, topk)


class listCloseOnly(Resource):
    def get(self, dtype='json'):
        topk = int(request.args.get('top', default=-1))
        items = list(db.timestable.find({}, {'_id': 0, 'index': 0, 'km': 0, 'miles': 0, 'location': 0, 'open': 0}))
        if dtype == 'csv':
            return csv_form(items, topk)
        return json_form(items, topk)


# Create routes
api.add_resource(listAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:dtype>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
