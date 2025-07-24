from flask import Blueprint, jsonify, request
from src.models.student import Student, db
from src.models.user import User
from datetime import datetime

student_bp = Blueprint('student', __name__)

@student_bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@student_bp.route('/students', methods=['POST'])
def create_student():
    data = request.json
    
    # Validar se o usuário existe
    user = User.query.get(data.get('user_id'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    student = Student(
        user_id=data['user_id'],
        grade_level=data['grade_level'],
        date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
        learning_style=data.get('learning_style')
    )
    
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201

@student_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict())

@student_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.json
    
    student.grade_level = data.get('grade_level', student.grade_level)
    student.learning_style = data.get('learning_style', student.learning_style)
    
    if data.get('date_of_birth'):
        student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
    
    db.session.commit()
    return jsonify(student.to_dict())

@student_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return '', 204

@student_bp.route('/students/<int:student_id>/progress', methods=['GET'])
def get_student_progress(student_id):
    student = Student.query.get_or_404(student_id)
    progress_data = [progress.to_dict() for progress in student.progress_records]
    return jsonify(progress_data)

@student_bp.route('/students/<int:student_id>/ai-personalization', methods=['GET'])
def get_student_ai_personalization(student_id):
    student = Student.query.get_or_404(student_id)
    ai_data = [ai.to_dict() for ai in student.ai_preferences]
    return jsonify(ai_data)

