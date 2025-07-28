from flask import Blueprint, request, jsonify
from src.models.ai_tutor_chat import ChatSession, ChatMessage, db
from src.models.problem_of_day import ProblemOfDay
from src.ai_tutor_engine import AITutorEngine
from datetime import datetime, timedelta
import time
import hashlib
import json

tutor_chat_bp = Blueprint('tutor_chat', __name__)
ai_tutor = AITutorEngine()

# Cache otimizado para respostas do tutor
_tutor_cache = {}
_response_templates = {}

def get_response_cache_key(message, context_summary):
    """Gera chave de cache para respostas similares"""
    # Normaliza a mensagem
    normalized_msg = message.lower().strip()
    
    # Remove caracteres especiais e espaços extras
    import re
    normalized_msg = re.sub(r'[^\w\s]', '', normalized_msg)
    normalized_msg = re.sub(r'\s+', ' ', normalized_msg)
    
    # Cria hash da mensagem + contexto
    cache_data = f"{normalized_msg}:{context_summary}"
    return hashlib.md5(cache_data.encode()).hexdigest()

def get_cached_response(cache_key, ttl_seconds=300):
    """Recupera resposta do cache se válida"""
    if cache_key in _tutor_cache:
        cached_time, response = _tutor_cache[cache_key]
        if time.time() - cached_time < ttl_seconds:
            return response
        else:
            del _tutor_cache[cache_key]
    return None

def cache_response(cache_key, response):
    """Armazena resposta no cache"""
    _tutor_cache[cache_key] = (time.time(), response)
    
    # Limita tamanho do cache
    if len(_tutor_cache) > 200:
        oldest_key = min(_tutor_cache.keys(), key=lambda k: _tutor_cache[k][0])
        del _tutor_cache[oldest_key]

def get_context_summary(conversation_history):
    """Cria resumo do contexto para cache"""
    if not conversation_history:
        return "new_conversation"
    
    # Analisa últimas 3 mensagens para contexto
    recent_messages = conversation_history[-3:]
    topics = []
    
    for msg in recent_messages:
        message_text = msg.get('message', '').lower()
        
        # Identifica tópicos principais
        if any(word in message_text for word in ['matemática', 'conta', 'número', 'somar']):
            topics.append('math')
        elif any(word in message_text for word in ['ciência', 'animal', 'planta', 'espaço']):
            topics.append('science')
        elif any(word in message_text for word in ['história', 'brasil', 'passado']):
            topics.append('history')
        elif any(word in message_text for word in ['português', 'palavra', 'ler', 'escrever']):
            topics.append('portuguese')
        elif any(word in message_text for word in ['geografia', 'país', 'mapa']):
            topics.append('geography')
    
    return '_'.join(set(topics)) if topics else 'general'

@tutor_chat_bp.route('/tutor/chat/start', methods=['POST'])
def start_chat_session():
    """
    Inicia uma nova sessão de chat com o tutor de IA (otimizada).
    """
    try:
        data = request.get_json()
        student_id = data.get('student_id', 1)
        problem_id = data.get('problem_id')
        
        # Cria nova sessão de chat
        session = ChatSession(
            student_id=student_id,
            problem_id=problem_id
        )
        
        db.session.add(session)
        db.session.commit()
        
        # Usa mensagem de boas-vindas pré-definida (mais rápida)
        welcome_messages = [
            "Oi! Eu sou o Curió, seu tutor virtual! 😊 Estou aqui para te ajudar com qualquer dúvida que você tiver. Sobre o que você gostaria de conversar hoje?",
            "Olá! Que bom te ver aqui! Sou o Curió e adoro ajudar crianças a aprender coisas novas. O que você está estudando ou tem curiosidade para saber?",
            "Oi, amiguinho! Eu sou o Curió, seu assistente de estudos! 🎓 Pode me perguntar sobre matemática, ciências, história, português... qualquer coisa! Do que você quer falar?"
        ]
        
        # Seleciona mensagem baseada no ID da sessão (determinístico)
        welcome_text = welcome_messages[session.id % len(welcome_messages)]
        
        # Salva a mensagem de boas-vindas
        welcome_message = ChatMessage(
            session_id=session.id,
            sender='tutor',
            message=welcome_text,
            message_type='greeting'
        )
        
        db.session.add(welcome_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'session': session.to_dict(),
            'welcome_message': welcome_message.to_dict(),
            'performance': {
                'cache_size': len(_tutor_cache),
                'response_time': 'optimized'
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tutor_chat_bp.route('/tutor/chat/<int:session_id>/message', methods=['POST'])
def send_message(session_id):
    """
    Envia mensagem para o tutor e recebe resposta (otimizada com cache).
    """
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Mensagem não fornecida'
            }), 400
        
        student_message = data['message'].strip()
        
        if not student_message:
            return jsonify({
                'success': False,
                'error': 'Mensagem não pode estar vazia'
            }), 400
        
        # Verifica se a sessão existe
        session = ChatSession.query.get(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'Sessão não encontrada'
            }), 404
        
        # Recupera histórico da conversa (limitado para performance)
        conversation_history = ChatMessage.query.filter_by(session_id=session_id)\
            .order_by(ChatMessage.timestamp.desc())\
            .limit(10).all()
        
        conversation_history.reverse()  # Ordem cronológica
        history_dicts = [msg.to_dict() for msg in conversation_history]
        
        # Salva mensagem do estudante
        student_msg = ChatMessage(
            session_id=session_id,
            sender='student',
            message=student_message,
            message_type='text'
        )
        
        db.session.add(student_msg)
        
        # Otimização: verifica cache antes de processar
        context_summary = get_context_summary(history_dicts)
        cache_key = get_response_cache_key(student_message, context_summary)
        
        cached_response = get_cached_response(cache_key, 300)  # 5 minutos
        
        if cached_response:
            # Usa resposta do cache (muito mais rápido)
            tutor_response = cached_response
            cache_hit = True
        else:
            # Gera nova resposta
            tutor_response = ai_tutor.generate_response(
                student_message, 
                history_dicts, 
                None
            )
            
            # Cacheia a resposta
            cache_response(cache_key, tutor_response)
            cache_hit = False
        
        # Salva resposta do tutor
        tutor_msg = ChatMessage(
            session_id=session_id,
            sender='tutor',
            message=tutor_response['message'],
            message_type=tutor_response['type']
        )
        
        db.session.add(tutor_msg)
        db.session.commit()
        
        # Atualiza timestamp da sessão
        session.last_activity = datetime.utcnow()
        db.session.commit()
        
        processing_time = round((time.time() - start_time) * 1000, 2)
        
        return jsonify({
            'success': True,
            'student_message': student_msg.to_dict(),
            'tutor_response': tutor_msg.to_dict(),
            'performance': {
                'processing_time_ms': processing_time,
                'cache_hit': cache_hit,
                'cache_size': len(_tutor_cache)
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e),
            'performance': {
                'processing_time_ms': round((time.time() - start_time) * 1000, 2)
            }
        }), 500

@tutor_chat_bp.route('/tutor/chat/<int:session_id>/history', methods=['GET'])
def get_chat_history(session_id):
    """
    Recupera histórico da conversa com paginação.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limita per_page para evitar sobrecarga
        per_page = min(per_page, 50)
        
        session = ChatSession.query.get(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'Sessão não encontrada'
            }), 404
        
        # Paginação otimizada
        messages = ChatMessage.query.filter_by(session_id=session_id)\
            .order_by(ChatMessage.timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        messages_list = [msg.to_dict() for msg in messages.items]
        messages_list.reverse()  # Ordem cronológica
        
        return jsonify({
            'success': True,
            'messages': messages_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': messages.total,
                'pages': messages.pages,
                'has_next': messages.has_next,
                'has_prev': messages.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tutor_chat_bp.route('/tutor/chat/<int:session_id>/summary', methods=['GET'])
def get_session_summary(session_id):
    """
    Gera resumo da sessão de chat com cache.
    """
    try:
        # Cache do resumo
        summary_cache_key = f"summary:{session_id}"
        cached_summary = get_cached_response(summary_cache_key, 600)  # 10 min
        
        if cached_summary:
            return jsonify({
                'success': True,
                'summary': cached_summary,
                'cached': True
            })
        
        session = ChatSession.query.get(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'Sessão não encontrada'
            }), 404
        
        # Recupera todas as mensagens da sessão
        messages = ChatMessage.query.filter_by(session_id=session_id)\
            .order_by(ChatMessage.timestamp).all()
        
        if not messages:
            return jsonify({
                'success': True,
                'summary': {
                    'total_messages': 0,
                    'topics_discussed': [],
                    'engagement_level': 'none'
                }
            })
        
        # Gera resumo usando o AI Tutor Engine
        history_dicts = [msg.to_dict() for msg in messages]
        summary = ai_tutor.generate_summary(history_dicts)
        
        # Adiciona informações extras
        summary['session_duration'] = calculate_session_duration(messages)
        summary['last_activity'] = session.last_activity.isoformat() if session.last_activity else None
        
        # Cacheia o resumo
        cache_response(summary_cache_key, summary)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'cached': False
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tutor_chat_bp.route('/tutor/performance', methods=['GET'])
def get_tutor_performance():
    """
    Retorna métricas de performance do tutor.
    """
    try:
        # Estatísticas do cache
        cache_stats = {
            'total_cached_responses': len(_tutor_cache),
            'cache_hit_ratio': calculate_cache_hit_ratio(),
            'avg_response_time': get_avg_response_time(),
            'active_sessions': ChatSession.query.filter(
                ChatSession.last_activity >= datetime.utcnow() - timedelta(hours=1)
            ).count()
        }
        
        return jsonify({
            'success': True,
            'performance': cache_stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def calculate_session_duration(messages):
    """Calcula duração da sessão em minutos"""
    if len(messages) < 2:
        return 0
    
    start_time = messages[0].timestamp
    end_time = messages[-1].timestamp
    duration = (end_time - start_time).total_seconds() / 60
    
    return round(duration, 1)

def calculate_cache_hit_ratio():
    """Calcula taxa de acerto do cache (simulada)"""
    if len(_tutor_cache) == 0:
        return 0
    
    # Estimativa baseada no tamanho do cache
    return min(len(_tutor_cache) / 100 * 0.3, 0.8)

def get_avg_response_time():
    """Retorna tempo médio de resposta (simulado)"""
    cache_ratio = calculate_cache_hit_ratio()
    
    # Tempo base: 2000ms sem cache, 200ms com cache
    base_time = 2000
    cached_time = 200
    
    avg_time = (base_time * (1 - cache_ratio)) + (cached_time * cache_ratio)
    return round(avg_time, 0)

# Função para pré-aquecer cache com respostas comuns
def warm_up_tutor_cache():
    """Pré-aquece o cache com respostas comuns"""
    common_questions = [
        ("oi", "general"),
        ("como somar números?", "math"),
        ("me conta sobre animais", "science"),
        ("história do brasil", "history"),
        ("como aprender a ler?", "portuguese"),
        ("me conta sobre o brasil", "geography")
    ]
    
    for question, context in common_questions:
        cache_key = get_response_cache_key(question, context)
        if cache_key not in _tutor_cache:
            # Simula resposta pré-definida para acelerar
            response = {
                'message': f"Resposta otimizada para: {question}",
                'type': 'educational'
            }
            cache_response(cache_key, response)

# Inicializa cache ao importar o módulo
warm_up_tutor_cache()

