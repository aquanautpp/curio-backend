import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
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

# Habilitar CORS para todas as rotas, permitindo requisições de qualquer origem
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(student_bp, url_prefix="/api")
app.register_blueprint(content_bp, url_prefix="/api")
app.register_blueprint(ai_bp, url_prefix="/api")
app.register_blueprint(ai_simple_bp, url_prefix="/api")
app.register_blueprint(problem_bp, url_prefix="/api")
app.register_blueprint(tutor_chat_bp, url_prefix="/api")

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(os.path.dirname(__file__), "database", "app.db")}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Importar todos os modelos para criação das tabelas
from src.models.student import Student
from src.models.teacher import Teacher
from src.models.content import Content
from src.models.progress import Progress
from src.models.ai_personalization import AIPersonalization
from src.models.problem_of_day import ProblemOfDay, ProblemSubmission
from src.models.ai_tutor_chat import ChatSession, ChatMessage

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
