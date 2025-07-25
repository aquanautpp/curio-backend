from flask import Blueprint, request, jsonify
from src.models.ai_tutor_chat import ChatSession, ChatMessage, db
from src.models.problem_of_day import ProblemOfDay
from src.ai_tutor_engine import AITutorEngine
from datetime import datetime

tutor_chat_bp = Blueprint('tutor_chat', __name__)
ai_tutor = AITutorEngine()

@tutor_chat_bp.route('/tutor/chat/start', methods=['POST'])
def start_chat_session():
    """
    Inicia uma nova sessão de chat com o tutor de IA.
    """
    try:
        data = request.get_json()
        student_id = data.get('student_id', 1)  # Default student for demo
        problem_id = data.get('problem_id')
        
        # Cria nova sessão de chat
        session = ChatSession(
            student_id=student_id,
            problem_id=problem_id
        )
        
        db.session.add(session)
        db.session.commit()
        
        # Gera mensagem de boas-vindas do tutor
        welcome_response = ai_tutor.generate_response("", [], None)
        
        # Salva a mensagem de boas-vindas
        welcome_message = ChatMessage(
            session_id=session.id,
            sender='tutor',
            message=welcome_response['message'],
            message_type=welcome_response['type']
        )
        
        db.session.add(welcome_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'session': session.to_dict(),
            'welcome_message': welcome_message.to_dict()
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
    Envia uma mensagem do estudante e recebe resposta do tutor.
    """
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
                'error': 'Sessão de chat não encontrada'
            }), 404
        
        if not session.is_active:
            return jsonify({
                'success': False,
                'error': 'Sessão de chat não está ativa'
            }), 400
        
        # Salva a mensagem do estudante
        student_msg = ChatMessage(
            session_id=session_id,
            sender='student',
            message=student_message,
            message_type='text'
        )
        
        db.session.add(student_msg)
        db.session.commit()
        
        # Busca o histórico da conversa
        conversation_history = []
        for msg in session.messages:
            conversation_history.append({
                'sender': msg.sender,
                'message': msg.message,
                'type': msg.message_type,
                'timestamp': msg.timestamp
            })
        
        # Busca contexto do problema se disponível
        problem_context = None
        if session.problem_id:
            problem = ProblemOfDay.query.get(session.problem_id)
            if problem:
                problem_context = {
                    'category': problem.category,
                    'difficulty': problem.difficulty,
                    'title': problem.title
                }
        
        # Gera resposta do tutor
        tutor_response = ai_tutor.generate_response(
            student_message, 
            conversation_history[:-1],  # Exclui a mensagem atual
            problem_context
        )
        
        # Salva a resposta do tutor
        tutor_msg = ChatMessage(
            session_id=session_id,
            sender='tutor',
            message=tutor_response['message'],
            message_type=tutor_response['type']
        )
        
        db.session.add(tutor_msg)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'student_message': student_msg.to_dict(),
            'tutor_response': tutor_msg.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tutor_chat_bp.route('/tutor/chat/<int:session_id>/history', methods=['GET'])
def get_chat_history(session_id):
    """
    Retorna o histórico completo de uma sessão de chat.
    """
    try:
        session = ChatSession.query.get(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'Sessão de chat não encontrada'
            }), 404
        
        messages = [msg.to_dict() for msg in session.messages]
        
        return jsonify({
            'success': True,
            'session': session.to_dict(),
            'messages': messages
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tutor_chat_bp.route('/tutor/chat/<int:session_id>/end', methods=['POST'])
def end_chat_session(session_id):
    """
    Encerra uma sessão de chat.
    """
    try:
        session = ChatSession.query.get(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'Sessão de chat não encontrada'
            }), 404
        
        session.is_active = False
        session.session_end = datetime.utcnow()
        
        db.session.commit()
        
        # Gera resumo da conversa
        conversation_history = [msg.to_dict() for msg in session.messages]
        summary = ai_tutor.generate_summary(conversation_history)
        
        return jsonify({
            'success': True,
            'session': session.to_dict(),
            'summary': summary
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@tutor_chat_bp.route('/tutor/chat/student/<int:student_id>/sessions', methods=['GET'])
def get_student_chat_sessions(student_id):
    """
    Retorna todas as sessões de chat de um estudante.
    """
    try:
        sessions = ChatSession.query.filter_by(student_id=student_id).order_by(ChatSession.session_start.desc()).all()
        
        sessions_data = []
        for session in sessions:
            session_dict = session.to_dict()
            # Adiciona informação do problema se disponível
            if session.problem_id:
                problem = ProblemOfDay.query.get(session.problem_id)
                if problem:
                    session_dict['problem_title'] = problem.title
            sessions_data.append(session_dict)
        
        return jsonify({
            'success': True,
            'sessions': sessions_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

