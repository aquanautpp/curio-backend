from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class StudentProgress(db.Model):
    __tablename__ = 'student_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)  # mathematics, science, history, etc.
    topic = db.Column(db.String(100), nullable=False)
    progress_percentage = db.Column(db.Float, default=0.0)
    time_spent_minutes = db.Column(db.Integer, default=0)
    exercises_completed = db.Column(db.Integer, default=0)
    exercises_correct = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'topic': self.topic,
            'progress_percentage': self.progress_percentage,
            'time_spent_minutes': self.time_spent_minutes,
            'exercises_completed': self.exercises_completed,
            'exercises_correct': self.exercises_correct,
            'accuracy': round((self.exercises_correct / max(self.exercises_completed, 1)) * 100, 1),
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Achievement(db.Model):
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='trophy')
    category = db.Column(db.String(50), nullable=False)  # progress, streak, mastery, etc.
    requirement_type = db.Column(db.String(50), nullable=False)  # exercises_completed, streak_days, etc.
    requirement_value = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, default=10)
    rarity = db.Column(db.String(20), default='common')  # common, rare, epic, legendary
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'requirement_type': self.requirement_type,
            'requirement_value': self.requirement_value,
            'points': self.points,
            'rarity': self.rarity,
            'is_active': self.is_active
        }

class StudentAchievement(db.Model):
    __tablename__ = 'student_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Float, default=0.0)  # For tracking progress towards achievement
    
    # Relacionamentos
    achievement = db.relationship('Achievement', backref='student_achievements')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'achievement_id': self.achievement_id,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None,
            'progress': self.progress,
            'achievement': self.achievement.to_dict() if self.achievement else None
        }

class StudyStreak(db.Model):
    __tablename__ = 'study_streaks'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_study_date = db.Column(db.Date)
    total_study_days = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def update_streak(self):
        """Atualiza a sequência de estudos baseada na data atual"""
        today = datetime.utcnow().date()
        
        if not self.last_study_date:
            # Primeiro dia de estudo
            self.current_streak = 1
            self.longest_streak = 1
            self.total_study_days = 1
            self.last_study_date = today
        elif self.last_study_date == today:
            # Já estudou hoje, não muda nada
            return
        elif self.last_study_date == today - timedelta(days=1):
            # Estudou ontem, continua a sequência
            self.current_streak += 1
            self.longest_streak = max(self.longest_streak, self.current_streak)
            self.total_study_days += 1
            self.last_study_date = today
        else:
            # Quebrou a sequência
            self.current_streak = 1
            self.total_study_days += 1
            self.last_study_date = today
        
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_study_date': self.last_study_date.isoformat() if self.last_study_date else None,
            'total_study_days': self.total_study_days
        }

class StudentPoints(db.Model):
    __tablename__ = 'student_points'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    total_points = db.Column(db.Integer, default=0)
    points_this_week = db.Column(db.Integer, default=0)
    points_this_month = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    experience_points = db.Column(db.Integer, default=0)
    week_start = db.Column(db.Date)
    month_start = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def add_points(self, points, source='general'):
        """Adiciona pontos e atualiza level"""
        self.total_points += points
        self.experience_points += points
        
        # Atualiza pontos semanais
        today = datetime.utcnow().date()
        if not self.week_start or today >= self.week_start + timedelta(days=7):
            self.week_start = today - timedelta(days=today.weekday())
            self.points_this_week = points
        else:
            self.points_this_week += points
        
        # Atualiza pontos mensais
        if not self.month_start or today.month != self.month_start.month:
            self.month_start = today.replace(day=1)
            self.points_this_month = points
        else:
            self.points_this_month += points
        
        # Calcula novo level (100 XP por level)
        new_level = (self.experience_points // 100) + 1
        if new_level > self.level:
            self.level = new_level
            # Aqui poderia disparar evento de level up
        
        self.updated_at = datetime.utcnow()
    
    def get_level_progress(self):
        """Retorna progresso para o próximo level"""
        current_level_xp = (self.level - 1) * 100
        next_level_xp = self.level * 100
        progress = ((self.experience_points - current_level_xp) / 100) * 100
        return min(progress, 100)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'total_points': self.total_points,
            'points_this_week': self.points_this_week,
            'points_this_month': self.points_this_month,
            'level': self.level,
            'experience_points': self.experience_points,
            'level_progress': self.get_level_progress(),
            'points_to_next_level': (self.level * 100) - self.experience_points
        }

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # exercise, chat, problem_of_day, etc.
    subject = db.Column(db.String(50))
    topic = db.Column(db.String(100))
    points_earned = db.Column(db.Integer, default=0)
    time_spent_minutes = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float)  # Percentage of correct answers
    metadata = db.Column(db.Text)  # JSON string for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_metadata(self, data):
        """Converte dict para JSON string"""
        self.metadata = json.dumps(data) if data else None
    
    def get_metadata(self):
        """Converte JSON string para dict"""
        return json.loads(self.metadata) if self.metadata else {}
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'activity_type': self.activity_type,
            'subject': self.subject,
            'topic': self.topic,
            'points_earned': self.points_earned,
            'time_spent_minutes': self.time_spent_minutes,
            'success_rate': self.success_rate,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Funções utilitárias para gamificação
class GamificationEngine:
    
    @staticmethod
    def calculate_points(activity_type, success_rate=100, time_spent=0, difficulty='easy'):
        """Calcula pontos baseado na atividade"""
        base_points = {
            'exercise': 10,
            'chat': 5,
            'problem_of_day': 20,
            'singapore_method': 15,
            'experiment': 25
        }
        
        difficulty_multiplier = {
            'easy': 1.0,
            'intermediate': 1.5,
            'hard': 2.0
        }
        
        points = base_points.get(activity_type, 5)
        points *= difficulty_multiplier.get(difficulty, 1.0)
        points *= (success_rate / 100)
        
        # Bonus por tempo gasto (máximo 50% bonus)
        if time_spent > 0:
            time_bonus = min(time_spent / 30, 0.5)  # 30 min = 50% bonus
            points *= (1 + time_bonus)
        
        return int(points)
    
    @staticmethod
    def check_achievements(student_id):
        """Verifica se o estudante desbloqueou novas conquistas"""
        from sqlalchemy import func
        
        # Busca dados do estudante
        progress_data = db.session.query(
            func.sum(StudentProgress.exercises_completed).label('total_exercises'),
            func.sum(StudentProgress.exercises_correct).label('total_correct'),
            func.sum(StudentProgress.time_spent_minutes).label('total_time')
        ).filter(StudentProgress.student_id == student_id).first()
        
        streak_data = StudyStreak.query.filter_by(student_id=student_id).first()
        points_data = StudentPoints.query.filter_by(student_id=student_id).first()
        
        # Lista de conquistas para verificar
        achievements_to_check = Achievement.query.filter_by(is_active=True).all()
        new_achievements = []
        
        for achievement in achievements_to_check:
            # Verifica se já possui a conquista
            existing = StudentAchievement.query.filter_by(
                student_id=student_id,
                achievement_id=achievement.id
            ).first()
            
            if existing:
                continue
            
            earned = False
            progress = 0
            
            # Verifica diferentes tipos de requisitos
            if achievement.requirement_type == 'exercises_completed':
                current_value = progress_data.total_exercises or 0
                earned = current_value >= achievement.requirement_value
                progress = min((current_value / achievement.requirement_value) * 100, 100)
            
            elif achievement.requirement_type == 'streak_days':
                current_value = streak_data.current_streak if streak_data else 0
                earned = current_value >= achievement.requirement_value
                progress = min((current_value / achievement.requirement_value) * 100, 100)
            
            elif achievement.requirement_type == 'total_points':
                current_value = points_data.total_points if points_data else 0
                earned = current_value >= achievement.requirement_value
                progress = min((current_value / achievement.requirement_value) * 100, 100)
            
            elif achievement.requirement_type == 'study_time_hours':
                current_value = (progress_data.total_time or 0) / 60  # Convert to hours
                earned = current_value >= achievement.requirement_value
                progress = min((current_value / achievement.requirement_value) * 100, 100)
            
            # Cria ou atualiza registro de conquista
            student_achievement = StudentAchievement.query.filter_by(
                student_id=student_id,
                achievement_id=achievement.id
            ).first()
            
            if not student_achievement:
                student_achievement = StudentAchievement(
                    student_id=student_id,
                    achievement_id=achievement.id,
                    progress=progress
                )
                db.session.add(student_achievement)
            else:
                student_achievement.progress = progress
            
            if earned and not student_achievement.earned_at:
                student_achievement.earned_at = datetime.utcnow()
                new_achievements.append(achievement)
                
                # Adiciona pontos pela conquista
                if points_data:
                    points_data.add_points(achievement.points, 'achievement')
        
        db.session.commit()
        return new_achievements
    
    @staticmethod
    def get_student_summary(student_id):
        """Retorna resumo completo de gamificação do estudante"""
        from sqlalchemy import func
        
        # Progresso geral
        progress_summary = db.session.query(
            func.avg(StudentProgress.progress_percentage).label('avg_progress'),
            func.sum(StudentProgress.time_spent_minutes).label('total_time'),
            func.sum(StudentProgress.exercises_completed).label('total_exercises'),
            func.sum(StudentProgress.exercises_correct).label('total_correct')
        ).filter(StudentProgress.student_id == student_id).first()
        
        # Progresso por matéria
        subject_progress = db.session.query(
            StudentProgress.subject,
            func.avg(StudentProgress.progress_percentage).label('avg_progress'),
            func.sum(StudentProgress.time_spent_minutes).label('time_spent')
        ).filter(StudentProgress.student_id == student_id).group_by(StudentProgress.subject).all()
        
        # Sequência de estudos
        streak = StudyStreak.query.filter_by(student_id=student_id).first()
        
        # Pontos e level
        points = StudentPoints.query.filter_by(student_id=student_id).first()
        
        # Conquistas
        achievements = db.session.query(StudentAchievement, Achievement).join(
            Achievement, StudentAchievement.achievement_id == Achievement.id
        ).filter(StudentAchievement.student_id == student_id).all()
        
        return {
            'overall_progress': round(progress_summary.avg_progress or 0, 1),
            'total_time_minutes': progress_summary.total_time or 0,
            'total_exercises': progress_summary.total_exercises or 0,
            'total_correct': progress_summary.total_correct or 0,
            'accuracy': round(((progress_summary.total_correct or 0) / max(progress_summary.total_exercises or 1, 1)) * 100, 1),
            'subject_progress': {
                subject: {
                    'progress': round(avg_progress, 1),
                    'time_spent': time_spent
                }
                for subject, avg_progress, time_spent in subject_progress
            },
            'streak': streak.to_dict() if streak else None,
            'points': points.to_dict() if points else None,
            'achievements': [
                {
                    'student_achievement': sa.to_dict(),
                    'achievement': achievement.to_dict()
                }
                for sa, achievement in achievements
            ]
        }

