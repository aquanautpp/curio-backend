from src.models.user import db
from datetime import datetime

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems_of_day.id'), nullable=True)
    session_start = db.Column(db.DateTime, default=datetime.utcnow)
    session_end = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with chat messages
    messages = db.relationship('ChatMessage', backref='session', lazy=True, order_by='ChatMessage.timestamp')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'problem_id': self.problem_id,
            'session_start': self.session_start.isoformat() if self.session_start else None,
            'session_end': self.session_end.isoformat() if self.session_end else None,
            'is_active': self.is_active,
            'message_count': len(self.messages)
        }

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    sender = db.Column(db.String(20), nullable=False)  # 'student' or 'tutor'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(50), default='text')  # 'text', 'hint', 'question', 'encouragement'
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'sender': self.sender,
            'message': self.message,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'message_type': self.message_type
        }

