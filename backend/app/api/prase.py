import gzip
from lxml import etree
from flask_restful import Api, Resource
import os
from flask import Flask

app = Flask(__name__)
replay_api = Api(app)

class ParseAPI(Resource):
    def get(self, filename):
        try:
            file_path = os.path.join('uploads', filename)
            with gzip.open(file_path, 'rb') as f:
                tree = etree.parse(f)
                root = tree.getroot()
                game_info = {'players': [elem.get('name') for elem in root.findall('.//UN')]}
            return {'message': 'Parse successful', 'data': game_info}, 200
        except Exception as e:
            return {'error': str(e)}, 400

replay_api.add_resource(ParseAPI, '/parse/<string:filename>')