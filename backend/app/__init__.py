from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from dotenv import load_dotenv
import os

db = SQLAlchemy()
api = Api()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # 配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化扩展
    db.init_app(app)
    api.init_app(app)

    # 注册蓝图（后续添加）
    from .api.replay import replay_bp
    app.register_blueprint(replay_bp, url_prefix='/api')

    # 创建数据库
    with app.app_context():
        db.create_all()

    return app