from flask import Blueprint, request
from flask_restful import Resource, Api
import os
import gzip
from lxml import etree

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
            try:
                file.save(file_path)
                return {'message': 'File uploaded successfully', 'filename': file.filename}, 200
            except Exception as e:
                return {'error': f'Failed to save file: {str(e)}'}, 400
        return {'error': 'Invalid file or no file provided'}, 400

class ParseAPI(Resource):
    def get(self, filename):
        try:
            file_path = os.path.join('uploads', filename)
            if not os.path.exists(file_path):
                return {'error': f'File not found: {file_path}'}, 404
            with gzip.open(file_path, 'rb') as f:
                try:
                    tree = etree.parse(f)
                except Exception as e:
                    return {'error': f'XML parsing failed: {str(e)}'}, 400
                root = tree.getroot()
                players = [elem.get('n0') or elem.get('name') for elem in root.findall('.//UN')]
                scores = []
                for elem in root.findall('.//AGARI') + root.findall('.//RYUUKYOKU'):
                    if elem.get('sc'):
                        scores.append(elem.get('sc').split(','))
                tile_map = {
                    '0': '1m', '1': '2m', '2': '3m', '3': '4m', '4': '5m', '5': '6m', '6': '7m', '7': '8m', '8': '9m',
                    '16': '1p', '17': '2p', '18': '3p', '19': '4p', '20': '5p', '21': '6p', '22': '7p', '23': '8p', '24': '9p',
                    '32': '1s', '33': '2s', '34': '3s', '35': '4s', '36': '5s', '37': '6s', '38': '7s', '39': '8s', '40': '9s',
                    '48': 'Haku', '49': 'Hatsu', '50': 'Chun', '51': 'Ton', '52': 'Nan', '53': 'Shaa', '54': 'Pei'
                }
                actions = []
                for elem in root.findall('.//T') + root.findall('.//D') + root.findall('.//REACH'):
                    hai = elem.get('hai')
                    tile = tile_map.get(hai, 'REACH') if elem.tag != 'REACH' else 'REACH'
                    if hai and hai not in tile_map and elem.tag != 'REACH':
                        print(f"Unknown hai: {hai}")  # 调试输出
                    actions.append({'type': elem.tag, 'tile': tile})
                tiles = []
                for elem in root.findall('.//T') + root.findall('.//D'):
                    hai = elem.get('hai')
                    tile = tile_map.get(hai, elem.tag)
                    if hai and hai not in tile_map:
                        print(f"Unknown tile hai: {hai}")  # 调试输出
                    tiles.append(tile)
                game_info = {
                    'players': players[:4],
                    'scores': scores,
                    'tiles': tiles,
                    'actions': actions
                }
            return {'message': 'Parse successful', 'data': game_info}, 200
        except Exception as e:
            return {'error': f'Parsing failed: {str(e)}'}, 400

replay_api.add_resource(ReplayAPI, '/replay')
replay_api.add_resource(UploadAPI, '/upload')
replay_api.add_resource(ParseAPI, '/parse/<string:filename>')