# src/routes/metacognition.py
from flask import Blueprint, jsonify, request
from datetime import datetime

metacognition_bp = Blueprint('metacognition', __name__)

# Conjunto básico de perguntas de reflexão
PROMPTS = [
    {'id': 1, 'question': 'O que você achou mais fácil nesta atividade?'},
    {'id': 2, 'question': 'O que você achou mais difícil?'},
    {'id': 3, 'question': 'Qual estratégia de estudo funcionou melhor?'}
]

@metacognition_bp.route('/metacognition/prompts', methods=['GET'])
def get_prompts():
    """Lista de perguntas de metacognição para os alunos refletirem sobre seus estudos."""
    return jsonify({'prompts': PROMPTS})

@metacognition_bp.route('/metacognition/prompts/<int:student_id>', methods=['POST'])
def save_responses(student_id):
    """
    Recebe as respostas de um aluno às perguntas de metacognição.
    Espera um JSON com a chave "responses" contendo as respostas.
    """
    data = request.json or {}
    responses = data.get('responses', [])
    # Em um sistema completo, essas respostas seriam salvas no banco de dados.
    return jsonify({
        'message': 'Responses saved successfully',
        'student_id': student_id,
        'responses': responses,
        'timestamp': datetime.utcnow().isoformat()
    })
