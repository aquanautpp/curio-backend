from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.gamification import (
    db, StudentProgress, Achievement, StudentAchievement, 
    StudyStreak, StudentPoints, ActivityLog, GamificationEngine
)

gamification_bp = Blueprint('gamification', __name__)

@gamification_bp.route('/students/<int:student_id>/progress', methods=['GET'])
def get_student_progress(student_id):
    """Retorna progresso completo do estudante"""
    try:
        summary = GamificationEngine.get_student_summary(student_id)
        return jsonify({
            'success': True,
            'progress': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/students/<int:student_id>/progress/<subject>', methods=['GET'])
def get_subject_progress(student_id, subject):
    """Retorna progresso específico de uma matéria"""
    try:
        progress_records = StudentProgress.query.filter_by(
            student_id=student_id,
            subject=subject
        ).all()
        
        return jsonify({
            'success': True,
            'subject': subject,
            'progress': [record.to_dict() for record in progress_records]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/students/<int:student_id>/progress', methods=['POST'])
def update_progress(student_id):
    """Atualiza progresso do estudante"""
    try:
        data = request.get_json()
        
        # Busca ou cria registro de progresso
        progress = StudentProgress.query.filter_by(
            student_id=student_id,
            subject=data.get('subject'),
            topic=data.get('topic')
        ).first()
        
        if not progress:
            progress = StudentProgress(
                student_id=student_id,
                subject=data.get('subject'),
                topic=data.get('topic')
            )
            db.session.add(progress)
        
        # Atualiza dados
        if 'progress_percentage' in data:
            progress.progress_percentage = min(data['progress_percentage'], 100)
        
        if 'time_spent_minutes' in data:
            progress.time_spent_minutes += data['time_spent_minutes']
        
        if 'exercises_completed' in data:
            progress.exercises_completed += data['exercises_completed']
        
        if 'exercises_correct' in data:
            progress.exercises_correct += data['exercises_correct']
        
        progress.last_activity = datetime.utcnow()
        progress.updated_at = datetime.utcnow()
        
        # Atualiza sequência de estudos
        streak = StudyStreak.query.filter_by(student_id=student_id).first()
        if not streak:
            streak = StudyStreak(student_id=student_id)
            db.session.add(streak)
        
        streak.update_streak()
        
        # Adiciona pontos
        points_earned = GamificationEngine.calculate_points(
            activity_type=data.get('activity_type', 'exercise'),
            success_rate=data.get('success_rate', 100),
            time_spent=data.get('time_spent_minutes', 0),
            difficulty=data.get('difficulty', 'easy')
        )
        
        student_points = StudentPoints.query.filter_by(student_id=student_id).first()
        if not student_points:
            student_points = StudentPoints(student_id=student_id)
            db.session.add(student_points)
        
        student_points.add_points(points_earned, data.get('activity_type', 'exercise'))
        
        # Registra atividade
        activity_log = ActivityLog(
            student_id=student_id,
            activity_type=data.get('activity_type', 'exercise'),
            subject=data.get('subject'),
            topic=data.get('topic'),
            points_earned=points_earned,
            time_spent_minutes=data.get('time_spent_minutes', 0),
            success_rate=data.get('success_rate')
        )
        activity_log.set_metadata(data.get('metadata', {}))
        db.session.add(activity_log)
        
        db.session.commit()
        
        # Verifica novas conquistas
        new_achievements = GamificationEngine.check_achievements(student_id)
        
        return jsonify({
            'success': True,
            'progress': progress.to_dict(),
            'points_earned': points_earned,
            'new_achievements': [achievement.to_dict() for achievement in new_achievements],
            'streak': streak.to_dict(),
            'student_points': student_points.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/students/<int:student_id>/achievements', methods=['GET'])
def get_student_achievements(student_id):
    """Retorna conquistas do estudante"""
    try:
        # Conquistas obtidas
        earned_achievements = db.session.query(StudentAchievement, Achievement).join(
            Achievement, StudentAchievement.achievement_id == Achievement.id
        ).filter(
            StudentAchievement.student_id == student_id,
            StudentAchievement.earned_at.isnot(None)
        ).all()
        
        # Conquistas em progresso
        progress_achievements = db.session.query(StudentAchievement, Achievement).join(
            Achievement, StudentAchievement.achievement_id == Achievement.id
        ).filter(
            StudentAchievement.student_id == student_id,
            StudentAchievement.earned_at.is_(None),
            StudentAchievement.progress > 0
        ).all()
        
        # Conquistas disponíveis (não iniciadas)
        available_achievements = db.session.query(Achievement).filter(
            Achievement.is_active == True,
            ~Achievement.id.in_(
                db.session.query(StudentAchievement.achievement_id).filter(
                    StudentAchievement.student_id == student_id
                )
            )
        ).all()
        
        return jsonify({
            'success': True,
            'earned': [
                {
                    'student_achievement': sa.to_dict(),
                    'achievement': achievement.to_dict()
                }
                for sa, achievement in earned_achievements
            ],
            'in_progress': [
                {
                    'student_achievement': sa.to_dict(),
                    'achievement': achievement.to_dict()
                }
                for sa, achievement in progress_achievements
            ],
            'available': [achievement.to_dict() for achievement in available_achievements]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/students/<int:student_id>/streak', methods=['GET'])
def get_study_streak(student_id):
    """Retorna sequência de estudos do estudante"""
    try:
        streak = StudyStreak.query.filter_by(student_id=student_id).first()
        
        if not streak:
            streak = StudyStreak(student_id=student_id)
            db.session.add(streak)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'streak': streak.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/students/<int:student_id>/points', methods=['GET'])
def get_student_points(student_id):
    """Retorna pontos e level do estudante"""
    try:
        points = StudentPoints.query.filter_by(student_id=student_id).first()
        
        if not points:
            points = StudentPoints(student_id=student_id)
            db.session.add(points)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'points': points.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/students/<int:student_id>/activities', methods=['GET'])
def get_activity_history(student_id):
    """Retorna histórico de atividades do estudante"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        activities = ActivityLog.query.filter_by(student_id=student_id)\
            .order_by(ActivityLog.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'activities': [activity.to_dict() for activity in activities.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': activities.total,
                'pages': activities.pages,
                'has_next': activities.has_next,
                'has_prev': activities.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Retorna ranking de estudantes"""
    try:
        leaderboard_type = request.args.get('type', 'points')  # points, streak, time
        limit = request.args.get('limit', 10, type=int)
        
        if leaderboard_type == 'points':
            # Ranking por pontos totais
            top_students = db.session.query(StudentPoints)\
                .order_by(StudentPoints.total_points.desc())\
                .limit(limit).all()
            
            leaderboard = [
                {
                    'rank': idx + 1,
                    'student_id': student.student_id,
                    'total_points': student.total_points,
                    'level': student.level
                }
                for idx, student in enumerate(top_students)
            ]
            
        elif leaderboard_type == 'streak':
            # Ranking por sequência atual
            top_students = db.session.query(StudyStreak)\
                .order_by(StudyStreak.current_streak.desc())\
                .limit(limit).all()
            
            leaderboard = [
                {
                    'rank': idx + 1,
                    'student_id': student.student_id,
                    'current_streak': student.current_streak,
                    'longest_streak': student.longest_streak
                }
                for idx, student in enumerate(top_students)
            ]
            
        elif leaderboard_type == 'time':
            # Ranking por tempo de estudo
            from sqlalchemy import func
            top_students = db.session.query(
                StudentProgress.student_id,
                func.sum(StudentProgress.time_spent_minutes).label('total_time')
            ).group_by(StudentProgress.student_id)\
             .order_by(func.sum(StudentProgress.time_spent_minutes).desc())\
             .limit(limit).all()
            
            leaderboard = [
                {
                    'rank': idx + 1,
                    'student_id': student.student_id,
                    'total_time_minutes': student.total_time
                }
                for idx, student in enumerate(top_students)
            ]
        
        return jsonify({
            'success': True,
            'leaderboard_type': leaderboard_type,
            'leaderboard': leaderboard
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/achievements', methods=['GET'])
def get_all_achievements():
    """Retorna todas as conquistas disponíveis"""
    try:
        achievements = Achievement.query.filter_by(is_active=True).all()
        
        # Agrupa por categoria
        by_category = {}
        for achievement in achievements:
            category = achievement.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(achievement.to_dict())
        
        return jsonify({
            'success': True,
            'achievements': [achievement.to_dict() for achievement in achievements],
            'by_category': by_category
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@gamification_bp.route('/achievements/seed', methods=['POST'])
def seed_achievements():
    """Popula banco com conquistas padrão"""
    try:
        # Conquistas básicas
        default_achievements = [
            {
                'name': 'Primeiro Passo',
                'description': 'Complete seu primeiro exercício',
                'icon': 'play',
                'category': 'progress',
                'requirement_type': 'exercises_completed',
                'requirement_value': 1,
                'points': 10,
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
                'description': 'Estude por 7 dias consecutivos',
                'icon': 'target',
                'category': 'streak',
                'requirement_type': 'streak_days',
                'requirement_value': 7,
                'points': 50,
                'rarity': 'rare'
            },
            {
                'name': 'Maratonista',
                'description': 'Estude por 30 dias consecutivos',
                'icon': 'trophy',
                'category': 'streak',
                'requirement_type': 'streak_days',
                'requirement_value': 30,
                'points': 200,
                'rarity': 'legendary'
            },
            {
                'name': 'Praticante',
                'description': 'Complete 10 exercícios',
                'icon': 'book-open',
                'category': 'progress',
                'requirement_type': 'exercises_completed',
                'requirement_value': 10,
                'points': 30,
                'rarity': 'common'
            },
            {
                'name': 'Estudioso',
                'description': 'Complete 50 exercícios',
                'icon': 'brain',
                'category': 'progress',
                'requirement_type': 'exercises_completed',
                'requirement_value': 50,
                'points': 100,
                'rarity': 'rare'
            },
            {
                'name': 'Mestre',
                'description': 'Complete 100 exercícios',
                'icon': 'star',
                'category': 'progress',
                'requirement_type': 'exercises_completed',
                'requirement_value': 100,
                'points': 250,
                'rarity': 'epic'
            },
            {
                'name': 'Colecionador de Pontos',
                'description': 'Acumule 1000 pontos',
                'icon': 'zap',
                'category': 'points',
                'requirement_type': 'total_points',
                'requirement_value': 1000,
                'points': 100,
                'rarity': 'rare'
            },
            {
                'name': 'Milionário',
                'description': 'Acumule 10000 pontos',
                'icon': 'crown',
                'category': 'points',
                'requirement_type': 'total_points',
                'requirement_value': 10000,
                'points': 500,
                'rarity': 'legendary'
            },
            {
                'name': 'Tempo é Ouro',
                'description': 'Estude por 10 horas no total',
                'icon': 'clock',
                'category': 'time',
                'requirement_type': 'study_time_hours',
                'requirement_value': 10,
                'points': 75,
                'rarity': 'rare'
            }
        ]
        
        for achievement_data in default_achievements:
            # Verifica se já existe
            existing = Achievement.query.filter_by(name=achievement_data['name']).first()
            if not existing:
                achievement = Achievement(**achievement_data)
                db.session.add(achievement)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Conquistas padrão criadas com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

