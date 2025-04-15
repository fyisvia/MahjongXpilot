from flask import Blueprint, request
from flask_restful import Resource, Api
from lxml import etree
import os
import gzip

replay_bp = Blueprint('replay', __name__)
replay_api = Api(replay_bp)

class ReplayAPI(Resource):
    def get(self):
        return {'message': 'Welcome to Mahjong Replay API'}, 200

class UploadAPI(Resource):
    def post(self):
        file = request.files.get('file')
        if file and file.filename.endswith(('.mjlog', '.xml')):
            os.makedirs('uploads', exist_ok=True)
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            return {'message': 'File uploaded successfully', 'filename': file.filename}, 200
        return {'error': 'Invalid file or no file provided'}, 400

class ParseAPI(Resource):
    def get(self, filename):
        try:
            file_path = os.path.join('uploads', filename)
            with gzip.open(file_path, 'rb') as f:
                tree = etree.parse(f)
                root = tree.getroot()
                # 示例：提取对局信息
                game_info = {'players': [elem.get('name') for elem in root.findall('.//UN')] }
            return {'message': 'Parse successful', 'data': game_info}, 200
        except Exception as e:
            return {'error': str(e)}, 400

replay_api.add_resource(ParseAPI, '/parse/<string:filename>')
replay_api.add_resource(ReplayAPI, '/replay')
replay_api.add_resource(UploadAPI, '/upload')