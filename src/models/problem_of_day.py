# src/routes/problem_of_day.py
from flask import Blueprint, jsonify, request
from src.models.problem_of_day import ProblemOfDay, ProblemSubmission
from src.models.user import db
from datetime import datetime
import json
import random

problem_day_bp = Blueprint('problem_day', __name__)

@problem_day_bp.route('/problems/today', methods=['GET'])
def get_problem_of_day():
    """
    Retorna um problema do dia ativo. Seleciona aleatoriamente um entre os problemas ativos.
    """
    problems = ProblemOfDay.query.filter_by(is_active=True).all()
    if not problems:
        return jsonify({'success': False, 'error': 'No active problems available'}), 404
    problem = random.choice(problems)
    return jsonify({'success': True, 'problem': problem.to_dict()})

@problem_day_bp.route('/problems/<int:problem_id>/submit', methods=['POST'])
def submit_problem_answer(problem_id):
    """
    Recebe a resposta do aluno para um problema do dia.
    Se a resposta for igual à esperada (ignora maiúsculas/minúsculas e espaços), marca como correta.
    """
    data = request.json or {}
    student_id = data.get('student_id')
    answer = (data.get('answer') or '').strip()
    time_spent = data.get('time_spent')

    problem = ProblemOfDay.query.get_or_404(problem_id)

    # Avaliar resposta
    is_correct = False
    feedback = ''
    if problem.expected_answer:
        is_correct = answer.lower() == problem.expected_answer.strip().lower()
        feedback = 'Resposta correta! Parabéns!' if is_correct else 'Resposta incorreta. Continue tentando.'

    submission = ProblemSubmission(
        student_id=student_id,
        problem_id=problem_id,
        answer=answer,
        is_correct=is_correct,
        time_spent=time_spent,
        submitted_at=datetime.utcnow(),
        feedback=feedback
    )
    db.session.add(submission)
    db.session.commit()

    return jsonify({
        'success': True,
        'is_correct': is_correct,
        'feedback': feedback
    })

@problem_day_bp.route('/problems/<int:problem_id>/hint', methods=['GET'])
def get_problem_hint(problem_id):
    """
    Retorna uma dica do problema. As dicas estão armazenadas como JSON em solution_hints.
    Neste exemplo, devolvemos a primeira dica disponível.
    """
    problem = ProblemOfDay.query.get_or_404(problem_id)
    if not problem.solution_hints:
        return jsonify({'success': False, 'error': 'No hints available'}), 404
    try:
        hints = json.loads(problem.solution_hints)
    except Exception:
        hints = [problem.solution_hints]
    hint = hints[0] if hints else 'No hints found'
    return jsonify({'success': True, 'hint': hint})
