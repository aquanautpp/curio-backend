from flask import Blueprint, jsonify
from src.models.user import User, db
from src.models.student import Student
from src.models.progress import Progress
from src.models.gamification import StudentProgress, StudentPoints, StudyStreak, StudentAchievement, Achievement
from datetime import datetime, timedelta
import random

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Retorna estatísticas para o dashboard"""
    try:
        # Dados simulados para demonstração (baseados no usuário Victor Pires)
        user_stats = {
            'user': {
                'name': 'Victor Pires',
                'grade': '7º Ano',
                'level': 13,
                'points': 1250,
                'streak': 7
            },
            'progress': {
                'exercises_completed': 47,
                'total_study_time': 12.5,  # horas
                'subjects_studied': 4,
                'current_streak': 7,
                'best_streak': 12,
                'weekly_goal': 5,  # horas
                'weekly_progress': 3.2  # horas completadas esta semana
            },
            'recent_activities': [
                {
                    'id': 1,
                    'type': 'exercise',
                    'subject': 'Matemática',
                    'title': 'Frações Equivalentes',
                    'points': 15,
                    'completed_at': '2025-01-24T10:30:00Z',
                    'status': 'completed'
                },
                {
                    'id': 2,
                    'type': 'chat',
                    'subject': 'Ciências',
                    'title': 'Pergunta sobre fotossíntese',
                    'points': 5,
                    'completed_at': '2025-01-24T09:15:00Z',
                    'status': 'completed'
                },
                {
                    'id': 3,
                    'type': 'problem',
                    'subject': 'Matemática',
                    'title': 'Problema do Dia - Geometria',
                    'points': 25,
                    'completed_at': '2025-01-23T16:45:00Z',
                    'status': 'completed'
                },
                {
                    'id': 4,
                    'type': 'achievement',
                    'subject': 'Geral',
                    'title': 'Conquistou: Dedicado',
                    'points': 25,
                    'completed_at': '2025-01-23T16:45:00Z',
                    'status': 'unlocked'
                }
            ],
            'subjects': {
                'matematica': {
                    'name': 'Matemática',
                    'progress': 68,
                    'exercises_completed': 23,
                    'last_activity': '2025-01-24T10:30:00Z',
                    'color': '#3B82F6'
                },
                'ciencias': {
                    'name': 'Ciências',
                    'progress': 45,
                    'exercises_completed': 12,
                    'last_activity': '2025-01-24T09:15:00Z',
                    'color': '#10B981'
                },
                'historia': {
                    'name': 'História',
                    'progress': 32,
                    'exercises_completed': 8,
                    'last_activity': '2025-01-22T14:20:00Z',
                    'color': '#F59E0B'
                },
                'portugues': {
                    'name': 'Português',
                    'progress': 55,
                    'exercises_completed': 15,
                    'last_activity': '2025-01-23T11:10:00Z',
                    'color': '#EF4444'
                }
            },
            'achievements': {
                'total': 8,
                'recent': [
                    {
                        'name': 'Dedicado',
                        'description': 'Estude por 3 dias consecutivos',
                        'icon': 'calendar',
                        'unlocked_at': '2025-01-23T16:45:00Z',
                        'rarity': 'common'
                    },
                    {
                        'name': 'Explorador da Matemática',
                        'description': 'Complete 10 exercícios de matemática',
                        'icon': 'calculator',
                        'unlocked_at': '2025-01-22T18:30:00Z',
                        'rarity': 'common'
                    }
                ]
            },
            'weekly_chart': [
                {'day': 'Seg', 'hours': 1.5, 'exercises': 3},
                {'day': 'Ter', 'hours': 2.0, 'exercises': 5},
                {'day': 'Qua', 'hours': 1.8, 'exercises': 4},
                {'day': 'Qui', 'hours': 2.2, 'exercises': 6},
                {'day': 'Sex', 'hours': 1.9, 'exercises': 4},
                {'day': 'Sáb', 'hours': 1.2, 'exercises': 2},
                {'day': 'Dom', 'hours': 0.8, 'exercises': 1}
            ]
        }
        
        return jsonify({
            'status': 'success',
            'data': user_stats
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao buscar estatísticas: {str(e)}'
        }), 500

@dashboard_bp.route('/dashboard/quick-actions', methods=['GET'])
def get_quick_actions():
    """Retorna ações rápidas para o dashboard"""
    try:
        quick_actions = [
            {
                'id': 'tutor',
                'title': 'Conversar com Curió',
                'description': 'Tire suas dúvidas com o tutor de IA',
                'icon': 'message-circle',
                'color': 'blue',
                'action': 'navigate',
                'target': '/tutor'
            },
            {
                'id': 'problem',
                'title': 'Problema do Dia',
                'description': 'Resolva o desafio diário',
                'icon': 'target',
                'color': 'green',
                'action': 'navigate',
                'target': '/problem'
            },
            {
                'id': 'mathematics',
                'title': 'Estudar Matemática',
                'description': 'Continue seus exercícios',
                'icon': 'calculator',
                'color': 'purple',
                'action': 'navigate',
                'target': '/mathematics'
            },
            {
                'id': 'science',
                'title': 'Explorar Ciências',
                'description': 'Descubra o mundo científico',
                'icon': 'microscope',
                'color': 'teal',
                'action': 'navigate',
                'target': '/science'
            }
        ]
        
        return jsonify({
            'status': 'success',
            'data': quick_actions
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao buscar ações rápidas: {str(e)}'
        }), 500

@dashboard_bp.route('/dashboard/notifications', methods=['GET'])
def get_notifications():
    """Retorna notificações para o usuário"""
    try:
        notifications = [
            {
                'id': 1,
                'type': 'achievement',
                'title': 'Nova conquista desbloqueada!',
                'message': 'Parabéns! Você conquistou "Dedicado" por estudar 3 dias seguidos!',
                'icon': 'trophy',
                'color': 'yellow',
                'timestamp': '2025-01-24T10:30:00Z',
                'read': False
            },
            {
                'id': 2,
                'type': 'reminder',
                'title': 'Hora de estudar!',
                'message': 'Que tal resolver o problema do dia? Você ainda não tentou hoje!',
                'icon': 'clock',
                'color': 'blue',
                'timestamp': '2025-01-24T09:00:00Z',
                'read': False
            },
            {
                'id': 3,
                'type': 'tip',
                'title': 'Dica do Curió',
                'message': 'Sabia que estudar um pouco todo dia é melhor que estudar muito de uma vez?',
                'icon': 'lightbulb',
                'color': 'green',
                'timestamp': '2025-01-23T20:00:00Z',
                'read': True
            }
        ]
        
        return jsonify({
            'status': 'success',
            'data': notifications
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao buscar notificações: {str(e)}'
        }), 500

