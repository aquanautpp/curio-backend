from src.models.user import db
from datetime import datetime

class ProblemOfDay(db.Model):
    __tablename__ = 'problems_of_day'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # e.g., "personal_finance", "logic", "data_analysis"
    difficulty = db.Column(db.String(50), nullable=False)  # e.g., "beginner", "intermediate", "advanced"
    expected_answer = db.Column(db.Text, nullable=True)  # Optional expected answer
    solution_hints = db.Column(db.Text, nullable=True)  # JSON string with hints
    resources = db.Column(db.Text, nullable=True)  # JSON string with additional resources
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with student submissions
    submissions = db.relationship('ProblemSubmission', backref='problem', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'expected_answer': self.expected_answer,
            'solution_hints': self.solution_hints,
            'resources': self.resources,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'is_active': self.is_active
        }

class ProblemSubmission(db.Model):
    __tablename__ = 'problem_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems_of_day.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=True)  # Can be evaluated later
    time_spent = db.Column(db.Integer, nullable=True)  # Time in minutes
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Text, nullable=True)  # AI-generated feedback
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'problem_id': self.problem_id,
            'answer': self.answer,
            'is_correct': self.is_correct,
            'time_spent': self.time_spent,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'feedback': self.feedback
        }

