# src/app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

# carrega .env (no dev)
load_dotenv()

db = SQLAlchemy()

def create_app():
    # static_folder aponta para src/static
    app = Flask(__name__,
                static_folder='static',
                static_url_path='')

    # escolhe config com base em FLASK_ENV
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('src.config.ProductionConfig')
    else:
        app.config.from_object('src.config.DevelopmentConfig')

    # inicializa DB e CORS apenas em /api/*
    db.init_app(app)
    CORS(app, resources={ r"/api/*": {"origins": app.config['CORS_ORIGINS']} })

    # registra seus blueprints (exemplo)
    from src.routes.users import users_bp
    from src.routes.problems import problems_bp
    app.register_blueprint(users_bp,   url_prefix='/api/users')
    app.register_blueprint(problems_bp, url_prefix='/api/problems')

    return app
