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

# Configuração de produção
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "asdf#FGSgvasgf$5$WGT")
app.config["ENV"] = os.environ.get("FLASK_ENV", "production")

# Habilitar CORS para todas as rotas
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configurar banco de dados
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///src/database/app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar banco de dados
db.init_app(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(student_bp, url_prefix="/api")
app.register_blueprint(content_bp, url_prefix="/api")
app.register_blueprint(ai_bp, url_prefix="/api")
app.register_blueprint(ai_simple_bp, url_prefix="/api")
app.register_blueprint(problem_bp, url_prefix="/api")
app.register_blueprint(tutor_chat_bp, url_prefix="/api")

# Servir arquivos estáticos do frontend (se existirem)
@app.route('/')
def serve_frontend():
    try:
        return send_from_directory('static', 'index.html')
    except:
        return {"message": "Curió Backend API is running!", "status": "success"}

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('static', path)
    except:
        return {"message": "File not found", "status": "error"}, 404

# Rota de health check
@app.route('/health')
def health_check():
    return {"status": "healthy", "message": "Curió Backend is running"}

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Configuração para desenvolvimento local
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_ENV") == "development"
    
    app.run(host=host, port=port, debug=debug)