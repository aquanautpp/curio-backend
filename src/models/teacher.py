from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialization = db.Column(db.String(100), nullable=True)  # Mathematics, Science, etc.
    experience_years = db.Column(db.Integer, nullable=True)
    certification = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    content_created = db.relationship('Content', backref='creator', lazy=True)
    
    def __repr__(self):
        return f'<Teacher {self.id} - {self.specialization}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'specialization': self.specialization,
            'experience_years': self.experience_years,
            'certification': self.certification,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

