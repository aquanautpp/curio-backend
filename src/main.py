import os
import sys
import logging
from datetime import datetime

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# Configurar logging para produção
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

app = Flask(__name__)

# Configuração de produção otimizada
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "curio-production-key-2025")
app.config["ENV"] = os.environ.get("FLASK_ENV", "production")
app.config["DEBUG"] = False
app.config["TESTING"] = False

# Configuração de segurança
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Middleware para proxy (Render)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Habilitar CORS para todas as rotas
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configurar banco de dados
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # Configuração robusta para SQLite
    try:
        db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "curio_production.db")
        
        # Testar permissões
        test_file = os.path.join(db_dir, "test.tmp")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        print(f"✅ Banco de dados configurado em: {db_path}")
        
    except Exception as e:
        # Fallback para /tmp
        db_path = "/tmp/curio_production.db"
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        print(f"⚠️ Usando banco temporário: {db_path}")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

# Importar modelos e rotas
from src.models.user import db
from src.routes.user import user_bp
from src.routes.student import student_bp
from src.routes.content import content_bp
from src.routes.ai_personalization import ai_bp
from src.routes.ai_simple import ai_simple_bp
from src.routes.problem_of_day import problem_bp
from src.routes.ai_tutor_chat import tutor_chat_bp
from src.routes.gamification import gamification_bp

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(student_bp, url_prefix="/api")
app.register_blueprint(content_bp, url_prefix="/api")
app.register_blueprint(ai_bp, url_prefix="/api")
app.register_blueprint(ai_simple_bp, url_prefix="/api")
app.register_blueprint(problem_bp, url_prefix="/api")
app.register_blueprint(tutor_chat_bp, url_prefix="/api")
app.register_blueprint(gamification_bp, url_prefix="/api")

# Servir arquivos estáticos do frontend (se existirem)
@app.route('/')
def serve_frontend():
    try:
        return send_from_directory('static', 'index.html')
    except:
        return {
            "message": "🐦 Curió Backend API está funcionando!",
            "status": "success",
            "version": "2.0.0",
            "timestamp": datetime.utcnow().isoformat()
        }

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('static', path)
    except:
        return {"message": "Arquivo não encontrado", "status": "error"}, 404

# Rotas de sistema
@app.route('/health')
def health_check():
    try:
        # Testar conexão com banco
        db.session.execute('SELECT 1')
        db_status = "connected"
    except:
        db_status = "error"
    
    return {
        "status": "healthy",
        "message": "Curió Backend está funcionando perfeitamente!",
        "database": db_status,
        "ai_tutor": "active",
        "gamification": "enabled",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.route('/api')
def api_info():
    return {
        "name": "Curió API",
        "version": "2.0.0",
        "description": "API da Plataforma Educacional Curió",
        "endpoints": {
            "health": "/health",
            "users": "/api/users",
            "students": "/api/students",
            "content": "/api/content",
            "ai_tutor": "/api/ai-tutor-chat",
            "problem_of_day": "/api/problem-of-day",
            "gamification": "/api/gamification"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint não encontrado", "status": 404}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Erro interno do servidor", "status": 500}, 500

@app.errorhandler(403)
def forbidden(error):
    return {"error": "Acesso negado", "status": 403}, 403

# Inicializar banco de dados e dados padrão
def init_database():
    """Inicializa banco de dados e popula com dados padrão"""
    with app.app_context():
        try:
            # Importar todos os modelos para garantir que sejam registrados
            from src.models.user import User
            from src.models.teacher import Teacher
            from src.models.student import Student
            from src.models.content import Content
            from src.models.progress import Progress
            from src.models.ai_personalization import AIPersonalization
            from src.models.problem_of_day import ProblemOfDay
            from src.models.ai_tutor_chat import ChatMessage
            from src.models.gamification import (
                StudentProgress, Achievement, StudentAchievement, 
                StudyStreak, StudentPoints, ActivityLog
            )
            
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas do banco de dados criadas com sucesso!")
            
            # Criar dados padrão se não existirem
            create_default_data()
            
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {e}")

def create_default_data():
    """Cria dados padrão para demonstração"""
    try:
        from src.models.user import User
        from src.models.student import Student
        from src.models.gamification import Achievement
        
        # Criar usuário demo se não existir
        demo_user = User.query.filter_by(email="demo@curio.com").first()
        if not demo_user:
            demo_user = User(
                username="demo_student",
                email="demo@curio.com"
            )
            demo_user.set_password("demo123")
            db.session.add(demo_user)
            db.session.commit()
            print("✅ Usuário demo criado")
        
        # Criar estudante demo se não existir
        demo_student = Student.query.filter_by(user_id=demo_user.id).first()
        if not demo_student:
            demo_student = Student(
                user_id=demo_user.id,
                name="Victor Pires",
                grade_level=7,
                learning_preferences={"visual": True, "interactive": True}
            )
            db.session.add(demo_student)
            db.session.commit()
            print("✅ Estudante demo criado")
        
        # Criar conquistas padrão se não existirem
        achievements = [
            {"name": "Primeiro Passo", "description": "Complete seu primeiro exercício", "icon": "🎯", "points": 10},
            {"name": "Curioso", "description": "Faça 10 perguntas ao tutor", "icon": "🧠", "points": 25},
            {"name": "Dedicado", "description": "Estude por 7 dias consecutivos", "icon": "📅", "points": 50},
            {"name": "Explorador", "description": "Complete 5 experimentos", "icon": "🔬", "points": 30},
            {"name": "Matemático", "description": "Complete 20 exercícios de matemática", "icon": "🧮", "points": 40},
            {"name": "Cientista", "description": "Complete 15 experimentos de ciências", "icon": "⚗️", "points": 35}
        ]
        
        for ach_data in achievements:
            existing = Achievement.query.filter_by(name=ach_data["name"]).first()
            if not existing:
                achievement = Achievement(**ach_data)
                db.session.add(achievement)
        
        db.session.commit()
        print("✅ Dados padrão criados com sucesso!")
        
    except Exception as e:
        print(f"⚠️ Erro ao criar dados padrão: {e}")

# Criar tabelas do banco de dados
init_database()

if __name__ == "__main__":
    # Configuração para desenvolvimento local e produção
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_ENV") == "development"
    
    print(f"🚀 Iniciando Curió Backend v2.0...")
    print(f"📍 Host: {host}")
    print(f"🔌 Porta: {port}")
    print(f"🔧 Debug: {debug}")
    print(f"🐦 Curió está pronto para voar!")
    
    app.run(host=host, port=port, debug=debug, threaded=True)

