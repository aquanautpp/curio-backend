from flask import Blueprint, request, jsonify
from src.models.problem_of_day import ProblemOfDay, ProblemSubmission, db
from src.models.student import Student
from datetime import datetime, date
import json
import random

problem_bp = Blueprint('problem', __name__)

@problem_bp.route('/problems/today', methods=['GET'])
def get_problem_of_day():
    """
    Retorna o problema do dia atual.
    Por enquanto, seleciona um problema aleatório da base de dados.
    """
    try:
        # Busca todos os problemas ativos
        active_problems = ProblemOfDay.query.filter_by(is_active=True).all()
        
        if not active_problems:
            # Se não há problemas cadastrados, cria um problema exemplo
            sample_problem = create_sample_problem()
            return jsonify({
                'success': True,
                'problem': sample_problem.to_dict()
            })
        
        # Seleciona um problema aleatório (pode ser melhorado para considerar a data)
        today_problem = random.choice(active_problems)
        
        return jsonify({
            'success': True,
            'problem': today_problem.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@problem_bp.route('/problems/<int:problem_id>/submit', methods=['POST'])
def submit_answer(problem_id):
    """
    Submete a resposta de um estudante para um problema específico.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        student_id = data.get('student_id', 1)  # Default student for demo
        answer = data.get('answer', '')
        time_spent = data.get('time_spent', 0)
        
        if not answer:
            return jsonify({
                'success': False,
                'error': 'Resposta não pode estar vazia'
            }), 400
        
        # Verifica se o problema existe
        problem = ProblemOfDay.query.get(problem_id)
        if not problem:
            return jsonify({
                'success': False,
                'error': 'Problema não encontrado'
            }), 404
        
        # Cria a submissão
        submission = ProblemSubmission(
            student_id=student_id,
            problem_id=problem_id,
            answer=answer,
            time_spent=time_spent
        )
        
        # Avalia a resposta (lógica simples por enquanto)
        is_correct = evaluate_answer(problem, answer)
        submission.is_correct = is_correct
        
        # Gera feedback baseado na resposta
        feedback = generate_feedback(problem, answer, is_correct)
        submission.feedback = feedback
        
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'submission': submission.to_dict(),
            'is_correct': is_correct,
            'feedback': feedback
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@problem_bp.route('/problems/<int:problem_id>/hint', methods=['GET'])
def get_problem_hint(problem_id):
    """
    Retorna uma dica para o problema específico.
    """
    try:
        problem = ProblemOfDay.query.get(problem_id)
        if not problem:
            return jsonify({
                'success': False,
                'error': 'Problema não encontrado'
            }), 404
        
        hints = []
        if problem.solution_hints:
            try:
                hints = json.loads(problem.solution_hints)
            except:
                hints = [problem.solution_hints]
        
        # Retorna uma dica aleatória se houver múltiplas
        hint = random.choice(hints) if hints else "Pense no problema passo a passo. Que informações você tem disponíveis?"
        
        return jsonify({
            'success': True,
            'hint': hint
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def create_sample_problem():
    """
    Cria um problema exemplo para demonstração.
    """
    sample_problem = ProblemOfDay(
        title="Orçamento Familiar Inteligente",
        description="""
        A família Silva tem uma renda mensal de R$ 4.500. Eles querem organizar suas finanças de forma inteligente.
        
        Informações atuais:
        - Gastos fixos (aluguel, contas): R$ 2.200
        - Alimentação: R$ 800
        - Transporte: R$ 400
        - Lazer: R$ 300
        
        Eles querem economizar 20% da renda para emergências e sonham em fazer uma viagem que custa R$ 3.600 daqui a 8 meses.
        
        DESAFIO: Crie um plano financeiro para a família Silva. É possível atingir a meta de poupança E economizar para a viagem? Se não, que ajustes você sugere?
        """,
        category="personal_finance",
        difficulty="intermediate",
        expected_answer="Análise financeira com sugestões de ajustes no orçamento",
        solution_hints=json.dumps([
            "Calcule primeiro quanto sobra depois dos gastos atuais",
            "20% de R$ 4.500 = R$ 900 para emergências",
            "Para a viagem: R$ 3.600 ÷ 8 meses = R$ 450 por mês",
            "Some as metas: R$ 900 + R$ 450 = R$ 1.350 necessários para poupança",
            "Compare com o que sobra atualmente e veja se é viável"
        ]),
        resources=json.dumps([
            "Calculadora de orçamento familiar",
            "Dicas de economia doméstica",
            "Planilha de controle financeiro"
        ])
    )
    
    db.session.add(sample_problem)
    db.session.commit()
    
    return sample_problem

def evaluate_answer(problem, answer):
    """
    Avalia se a resposta está correta (lógica simples por enquanto).
    """
    # Para o problema exemplo, considera correto se a resposta menciona alguns pontos-chave
    if problem.category == "personal_finance":
        key_terms = ["900", "450", "1350", "deficit", "ajuste", "cortar", "economizar"]
        answer_lower = answer.lower()
        
        # Se menciona pelo menos 2 termos-chave, considera parcialmente correto
        matches = sum(1 for term in key_terms if term in answer_lower)
        return matches >= 2
    
    # Para outros tipos de problema, implementar lógicas específicas
    return len(answer.strip()) > 50  # Resposta mínima de 50 caracteres

def generate_feedback(problem, answer, is_correct):
    """
    Gera feedback personalizado baseado na resposta.
    """
    if is_correct:
        feedback_options = [
            "Excelente análise! Você demonstrou boa compreensão dos conceitos financeiros.",
            "Muito bem! Sua abordagem está no caminho certo.",
            "Parabéns! Você considerou os aspectos mais importantes do problema."
        ]
    else:
        feedback_options = [
            "Boa tentativa! Considere revisar os cálculos e pensar em todas as variáveis envolvidas.",
            "Você está no caminho certo, mas pode aprofundar mais a análise. Que tal usar as dicas?",
            "Interessante perspectiva! Tente incluir mais detalhes numéricos na sua resposta."
        ]
    
    return random.choice(feedback_options)

