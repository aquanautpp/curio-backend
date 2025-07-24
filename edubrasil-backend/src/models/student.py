from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grade_level = db.Column(db.String(10), nullable=False)  # K-12
    date_of_birth = db.Column(db.Date, nullable=True)
    learning_style = db.Column(db.String(50), nullable=True)  # visual, auditory, kinesthetic
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    progress_records = db.relationship('Progress', backref='student', lazy=True)
    ai_preferences = db.relationship('AIPersonalization', backref='student', lazy=True)
    
    def __repr__(self):
        return f'<Student {self.id} - Grade {self.grade_level}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'grade_level': self.grade_level,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'learning_style': self.learning_style,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

