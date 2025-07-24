from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject = db.Column(db.String(50), nullable=False)  # Mathematics, Science, etc.
    grade_level = db.Column(db.String(10), nullable=False)  # K-12
    content_type = db.Column(db.String(50), nullable=False)  # video, text, exercise, game
    difficulty_level = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    singapore_method_stage = db.Column(db.String(20), nullable=True)  # concrete, pictorial, abstract
    content_data = db.Column(db.JSON, nullable=True)  # Flexible JSON field for content specifics
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
    creator_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    progress_records = db.relationship('Progress', backref='content', lazy=True)
    
    def __repr__(self):
        return f'<Content {self.title} - {self.subject}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'subject': self.subject,
            'grade_level': self.grade_level,
            'content_type': self.content_type,
            'difficulty_level': self.difficulty_level,
            'singapore_method_stage': self.singapore_method_stage,
            'content_data': self.content_data,
            'tags': self.tags.split(',') if self.tags else [],
            'creator_id': self.creator_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

