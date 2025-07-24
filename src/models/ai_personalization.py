from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class AIPersonalization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    learning_style_detected = db.Column(db.String(50), nullable=True)  # visual, auditory, kinesthetic
    preferred_content_types = db.Column(db.String(200), nullable=True)  # JSON string of preferences
    difficulty_preference = db.Column(db.String(20), nullable=True)  # easy, medium, hard
    pace_preference = db.Column(db.String(20), nullable=True)  # slow, normal, fast
    strengths = db.Column(db.Text, nullable=True)  # JSON string of subject strengths
    weaknesses = db.Column(db.Text, nullable=True)  # JSON string of areas needing improvement
    recommended_next_content = db.Column(db.Text, nullable=True)  # JSON string of content IDs
    ai_confidence_score = db.Column(db.Float, nullable=True)  # 0-1 confidence in recommendations
    last_analysis_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIPersonalization Student:{self.student_id} - {self.learning_style_detected}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'learning_style_detected': self.learning_style_detected,
            'preferred_content_types': self.preferred_content_types,
            'difficulty_preference': self.difficulty_preference,
            'pace_preference': self.pace_preference,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'recommended_next_content': self.recommended_next_content,
            'ai_confidence_score': self.ai_confidence_score,
            'last_analysis_date': self.last_analysis_date.isoformat() if self.last_analysis_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

