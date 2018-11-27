#!/usr/bin/env python
from flask import Flask, Response, Blueprint
from flask_restful import reqparse
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app, version='1.0', title='Flask-RESTful',
          description='A simple demonstration of a Flask RestPlus powered API')

# Define expected arguments:
parser = reqparse.RequestParser()
parser.add_argument('id', type=str, help='Person ID to query')

ns = api.namespace('list', description='listdir operations')

PEOPLE = {1 : 'Roger',
          2 : 'Jessica',
          3 : 'Benny',
          4 : 'Bullet'}

@ns.route('/people/<int:id>')
class ListPeople(Resource):

    def get(self, id):
        return self._handle(id)

    def post(self, id):
        return self._handle(id)

    def _handle(self, id):
        # Return 400 response (Bad Request) if folder argument is missing.
        if not id in PEOPLE:
            return Response(response=dict(error='id {} not found'.format(id)), status=400)

        # Return default 200 response (OK)
        return PEOPLE[id]

if __name__ == '__main__':
    app.run(debug=True)
