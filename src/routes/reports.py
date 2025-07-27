# src/routes/reports.py
from flask import Blueprint, jsonify
from src.models.student import Student
from src.models.progress import Progress
from src.models.gamification import Achievement

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/overview', methods=['GET'])
def overview():
    """
    Retorna estatísticas agregadas:
    - número total de alunos
    - número total de conquistas cadastradas
    - total de registros de progresso
    - média de progresso (se disponível)
    """
    total_students = Student.query.count()
    total_achievements = Achievement.query.count()
    total_progress_records = Progress.query.count()

    # Calcular média de progresso, se houver campo progress_percentage
    avg_progress = 0
    progress_list = Progress.query.all()
    percentages = []
    for record in progress_list:
        # Caso exista o atributo 'progress_percentage' no modelo de progresso
        if hasattr(record, 'progress_percentage') and record.progress_percentage is not None:
            percentages.append(record.progress_percentage)
    if percentages:
        avg_progress = sum(percentages) / len(percentages)

    return jsonify({
        'total_students': total_students,
        'total_achievements': total_achievements,
        'total_progress_records': total_progress_records,
        'avg_progress_percentage': avg_progress
    })
