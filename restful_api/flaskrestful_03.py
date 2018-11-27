#!/usr/bin/env python
from flask import Flask, Response
from flask_restful import Resource, Api
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)

# Define expected arguments:
parser = reqparse.RequestParser()
parser.add_argument('folder', type=str, help='Folder to query')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class ListDir(Resource):
    def get(self):
        return self._handle()

    def post(self):
        return self._handle()

    def _handle(self):
        import os

        args = parser.parse_args()

        # Return 400 response (Bad Request) if folder argument is missing.
        if not args.get('folder', None):
            return Response(response=dict(error='folder argument is missing'), status=400)

        # Return default 200 response (OK)
        return [i for i in os.listdir(args['folder'])]

api.add_resource(HelloWorld, '/')
api.add_resource(ListDir, '/listdir')

if __name__ == '__main__':
    app.run(debug=True)
