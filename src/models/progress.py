from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # not_started, in_progress, completed, mastered
    score = db.Column(db.Float, nullable=True)  # 0-100 score
    time_spent = db.Column(db.Integer, nullable=True)  # Time in minutes
    attempts = db.Column(db.Integer, default=1)
    completion_date = db.Column(db.DateTime, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Progress Student:{self.student_id} Content:{self.content_id} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'content_id': self.content_id,
            'status': self.status,
            'score': self.score,
            'time_spent': self.time_spent,
            'attempts': self.attempts,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

