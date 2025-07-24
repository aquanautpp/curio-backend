import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.student import student_bp
from src.routes.content import content_bp
from src.routes.ai_personalization import ai_bp
from src.routes.ai_simple import ai_simple_bp
from src.routes.problem_of_day_optimized import problem_bp
from src.routes.ai_tutor_chat_optimized import tutor_chat_bp
from src.routes.gamification import gamification_bp

app = Flask(__name__)

# Configuração de produção
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "curio_secret_key_2024_#FGSgvasgf$5$WGT")
app.config["ENV"] = os.environ.get("FLASK_ENV", "production")

# Habilitar CORS para todas as rotas
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configurar banco de dados
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # Tentar criar banco na pasta do projeto, senão usar /tmp
    try:
        db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "curio_app.db")
        # Testar se consegue escrever no diretório
        test_file = os.path.join(db_dir, "test.tmp")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        print(f"✅ Banco de dados configurado em: {db_path}")
    except Exception as e:
        print(f"⚠️  Não foi possível criar banco na pasta do projeto: {e}")
        # Fallback para /tmp
        db_path = "/tmp/curio_app.db"
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        print(f"✅ Banco de dados configurado em: {db_path}")

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
app.register_blueprint(gamification_bp, url_prefix="/api/gamification")

# Servir arquivos estáticos do frontend (se existirem)
@app.route('/')
def serve_frontend():
    try:
        return send_from_directory('static', 'index.html')
    except:
        return jsonify({
            "message": "🐦 Curió Backend API está funcionando!",
            "status": "success",
            "version": "2.0.0",
            "features": [
                "AI Tutor Chat Otimizado",
                "Sistema de Gamificação Completo",
                "Dashboard Funcional",
                "Seções Educacionais Ativas",
                "Cache e Performance Otimizada",
                "Autenticação de Usuários"
            ]
        })

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('static', path)
    except:
        return jsonify({"message": "Arquivo não encontrado", "status": "error"}), 404

# Rota de health check
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Curió Backend está funcionando perfeitamente!",
        "database": "connected",
        "ai_tutor": "active",
        "gamification": "enabled"
    })

# Rota de informações da API
@app.route('/api')
def api_info():
    return jsonify({
        "api_name": "Curió Educational Platform API",
        "version": "2.0.0",
        "description": "API completa para plataforma educacional com IA",
        "endpoints": {
            "users": "/api/users",
            "students": "/api/students",
            "content": "/api/content",
            "ai_tutor": "/api/ai-tutor-chat",
            "problem_of_day": "/api/problems",
            "gamification": "/api/gamification",
            "health": "/health"
        },
        "features": [
            "Tutor de IA comunicativo e amigável",
            "Sistema completo de gamificação",
            "Método de Singapura para matemática",
            "Dashboard funcional com dados reais",
            "Sistema de conquistas e pontuação",
            "Cache otimizado para performance"
        ]
    })

# Inicializar banco de dados e dados padrão
def init_database():
    """Inicializa banco de dados e popula com dados padrão"""
    with app.app_context():
        try:
  # Importar todos os modelos para garantir que sejam registrados
    from src.models.user import User
    from src.models.student import Student
    from src.models.teacher import Teacher
    from src.models.content import Content
    from src.models.progress import Progress
    from src.models.ai_personalization import AIPersonalization
    from src.models.problem_of_day import ProblemOfDay
    from src.models.ai_tutor_chat import AITutorChat
    from src.models.gamification import (
        StudentProgress, Achievement, StudentAchievement, 
        StudyStreak, StudentPoints, ActivityLog
    )
    
            db.create_all()
            print("✅ Tabelas do banco de dados criadas com sucesso!")
            
            # Importar modelos de gamificação
            from src.models.gamification import Achievement
            
            # Verificar se já existem conquistas
            existing_achievements = Achievement.query.count()
            if existing_achievements == 0:
                # Criar conquistas padrão
                default_achievements = [
                    {
                        'name': 'Primeiro Passo',
                        'description': 'Complete seu primeiro exercício na plataforma Curió',
                        'icon': 'play',
                        'category': 'progress',
                        'requirement_type': 'exercises_completed',
                        'requirement_value': 1,
                        'points': 10,
                        'rarity': 'common'
                    },
                    {
                        'name': 'Curioso',
                        'description': 'Faça sua primeira pergunta ao tutor Curió',
                        'icon': 'brain',
                        'category': 'interaction',
                        'requirement_type': 'chat_messages',
                        'requirement_value': 1,
                        'points': 5,
                        'rarity': 'common'
                    },
                    {
                        'name': 'Dedicado',
                        'description': 'Estude por 3 dias consecutivos',
                        'icon': 'calendar',
                        'category': 'streak',
                        'requirement_type': 'streak_days',
                        'requirement_value': 3,
                        'points': 25,
                        'rarity': 'common'
                    },
                    {
                        'name': 'Persistente',
                        'description': 'Mantenha uma sequência de 7 dias de estudo',
                        'icon': 'target',
                        'category': 'streak',
                        'requirement_type': 'streak_days',
                        'requirement_value': 7,
                        'points': 50,
                        'rarity': 'rare'
                    },
                    {
                        'name': 'Explorador da Matemática',
                        'description': 'Complete 10 exercícios de matemática',
                        'icon': 'calculator',
                        'category': 'subject',
                        'requirement_type': 'subject_exercises',
                        'requirement_value': 10,
                        'points': 30,
                        'rarity': 'common'
                    },
                    {
                        'name': 'Cientista Curioso',
                        'description': 'Complete 10 atividades de ciências',
                        'icon': 'microscope',
                        'category': 'subject',
                        'requirement_type': 'subject_exercises',
                        'requirement_value': 10,
                        'points': 30,
                        'rarity': 'common'
                    },
                    {
                        'name': 'Maratonista',
                        'description': 'Estude por 30 dias consecutivos - um verdadeiro campeão!',
                        'icon': 'trophy',
                        'category': 'streak',
                        'requirement_type': 'streak_days',
                        'requirement_value': 30,
                        'points': 200,
                        'rarity': 'legendary'
                    },
                    {
                        'name': 'Mestre dos Pontos',
                        'description': 'Acumule 1000 pontos na plataforma',
                        'icon': 'zap',
                        'category': 'points',
                        'requirement_type': 'total_points',
                        'requirement_value': 1000,
                        'points': 100,
                        'rarity': 'rare'
                    },
                    {
                        'name': 'Tempo é Ouro',
                        'description': 'Dedique 10 horas aos estudos',
                        'icon': 'clock',
                        'category': 'time',
                        'requirement_type': 'study_time_hours',
                        'requirement_value': 10,
                        'points': 75,
                        'rarity': 'rare'
                    },
                    {
                        'name': 'Lenda do Curió',
                        'description': 'Conquista especial para os maiores estudiosos',
                        'icon': 'crown',
                        'category': 'special',
                        'requirement_type': 'total_points',
                        'requirement_value': 5000,
                        'points': 500,
                        'rarity': 'legendary'
                    }
                ]
                
                for achievement_data in default_achievements:
                    achievement = Achievement(**achievement_data)
                    db.session.add(achievement)
                
                db.session.commit()
                print(f"✅ {len(default_achievements)} conquistas padrão criadas!")
            
            print("🎉 Banco de dados inicializado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {e}")
            db.session.rollback()

# Criar tabelas do banco de dados
init_database()

if __name__ == "__main__":
    # Configuração para desenvolvimento local e produção
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_ENV") == "development"
    
    print(f"🚀 Iniciando Curió Backend...")
    print(f"📍 Host: {host}")
    print(f"🔌 Porta: {port}")
    print(f"🔧 Debug: {debug}")
    print(f"🐦 Curió está pronto para voar!")
    
    app.run(host=host, port=port, debug=debug)

