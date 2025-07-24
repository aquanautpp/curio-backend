import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.student import student_bp
from src.routes.content import content_bp
from src.routes.ai_personalization import ai_bp
from src.routes.ai_simple import ai_simple_bp
from src.routes.problem_of_day import problem_bp
from src.routes.ai_tutor_chat import tutor_chat_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf#FGSgvasgf$5$WGT"

# Habilitar CORS para todas as rotas
CORS(app, resources={r"/api/*": {"origins": "*"}})