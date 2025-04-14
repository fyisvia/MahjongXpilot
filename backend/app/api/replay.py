from flask import Blueprint
from flask_restful import Resource, Api

replay_bp = Blueprint('replay', __name__)
replay_api = Api(replay_bp)

class ReplayAPI(Resource):
    def get(self):
        return {'message': 'Welcome to Mahjong Replay API'}, 200

replay_api.add_resource(ReplayAPI, '/replay')