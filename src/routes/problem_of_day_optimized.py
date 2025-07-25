from flask import Blueprint, request, jsonify
from src.models.problem_of_day import ProblemOfDay, ProblemSubmission, db
from src.models.student import Student
from datetime import datetime, date
import json
import random
import time
import hashlib

problem_bp = Blueprint('problem', __name__)

# Cache simples em memória
_cache = {}
_cache_ttl = {}

def get_cache_key(prefix, data=None):
    """Gera chave única para cache"""
    if data:
        data_str = json.dumps(data, sort_keys=True) if isinstance(data, dict) else str(data)
        hash_obj = hashlib.md5(data_str.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"
    else:
        # Para problema do dia, usa a data atual
        date_str = datetime.now().strftime("%Y-%m-%d")
        return f"{prefix}:{date_str}"

def get_from_cache(key, ttl_seconds=3600):
    """Recupera item do cache se ainda válido"""
    if key in _cache:
        cached_time, data = _cache[key]
        if time.time() - cached_time < ttl_seconds:
            return data
        else:
            # Remove item expirado
            del _cache[key]
    return None

def set_cache(key, data):
    """Armazena item no cache"""
    _cache[key] = (time.time(), data)
    
    # Limpa cache antigo se necessário (máximo 100 itens)
    if len(_cache) > 100:
        oldest_key = min(_cache.keys(), key=lambda k: _cache[k][0])
        del _cache[oldest_key]

@problem_bp.route('/problems/today', methods=['GET'])
def get_problem_of_day():
    """
    Retorna o problema do dia atual com cache otimizado.
    """
    try:
        # Verifica cache primeiro (válido por 1 hora)
        cache_key = get_cache_key("problem_of_day")
        cached_problem = get_from_cache(cache_key, 3600)
        
        if cached_problem:
            return jsonify({
                'success': True,
                'problem': cached_problem,
                'cached': True
            })
        
        # Busca todos os problemas ativos
        active_problems = ProblemOfDay.query.filter_by(is_active=True).all()
        
        if not active_problems:
            # Se não há problemas cadastrados, cria um problema exemplo
            sample_problem = create_sample_problem()
            problem_data = sample_problem.to_dict()
        else:
            # Seleciona problema baseado na data (determinístico para o dia)
            today_seed = int(datetime.now().strftime("%Y%m%d"))
            random.seed(today_seed)
            today_problem = random.choice(active_problems)
            problem_data = today_problem.to_dict()
        
        # Adiciona informações extras para melhor UX
        problem_data['estimated_time'] = estimate_problem_time(problem_data)
        problem_data['difficulty_level'] = get_difficulty_description(problem_data.get('difficulty', 'intermediate'))
        
        # Cacheia o resultado
        set_cache(cache_key, problem_data)
        
        return jsonify({
            'success': True,
            'problem': problem_data,
            'cached': False
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
    Otimizado com validações mais rápidas.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        student_id = data.get('student_id', 1)
        answer = data.get('answer', '').strip()
        time_spent = data.get('time_spent', 0)
        
        # Validações rápidas
        if not answer:
            return jsonify({
                'success': False,
                'error': 'Resposta não pode estar vazia'
            }), 400
        
        if len(answer) < 10:
            return jsonify({
                'success': False,
                'error': 'Resposta muito curta. Mínimo 10 caracteres.'
            }), 400
        
        # Verifica cache do problema primeiro
        problem_cache_key = f"problem:{problem_id}"
        problem_data = get_from_cache(problem_cache_key, 1800)  # 30 min
        
        if not problem_data:
            problem = ProblemOfDay.query.get(problem_id)
            if not problem:
                return jsonify({
                    'success': False,
                    'error': 'Problema não encontrado'
                }), 404
            problem_data = problem.to_dict()
            set_cache(problem_cache_key, problem_data)
        
        # Avaliação otimizada da resposta
        is_correct, confidence = evaluate_answer_optimized(problem_data, answer)
        
        # Gera feedback inteligente
        feedback = generate_smart_feedback(problem_data, answer, is_correct, confidence)
        
        # Cria a submissão
        submission = ProblemSubmission(
            student_id=student_id,
            problem_id=problem_id,
            answer=answer,
            time_spent=time_spent,
            is_correct=is_correct,
            feedback=feedback
        )
        
        db.session.add(submission)
        db.session.commit()
        
        # Resposta otimizada
        response_data = {
            'success': True,
            'submission_id': submission.id,
            'is_correct': is_correct,
            'confidence': confidence,
            'feedback': feedback,
            'points_earned': calculate_points(is_correct, time_spent, confidence),
            'next_suggestion': get_next_suggestion(is_correct, problem_data)
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@problem_bp.route('/problems/<int:problem_id>/hint', methods=['GET'])
def get_problem_hint(problem_id):
    """
    Retorna uma dica para o problema específico com cache.
    """
    try:
        # Cache de dicas
        hint_cache_key = f"hint:{problem_id}"
        cached_hint = get_from_cache(hint_cache_key, 1800)  # 30 min
        
        if cached_hint:
            return jsonify({
                'success': True,
                'hint': cached_hint,
                'cached': True
            })
        
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
        
        # Seleciona dica baseada no horário (determinístico)
        if hints:
            hint_index = (int(time.time()) // 300) % len(hints)  # Muda a cada 5 min
            hint = hints[hint_index]
        else:
            hint = "Pense no problema passo a passo. Que informações você tem disponíveis?"
        
        # Cacheia a dica
        set_cache(hint_cache_key, hint)
        
        return jsonify({
            'success': True,
            'hint': hint,
            'cached': False
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@problem_bp.route('/problems/stats', methods=['GET'])
def get_problem_stats():
    """
    Retorna estatísticas dos problemas com cache.
    """
    try:
        stats_cache_key = "problem_stats"
        cached_stats = get_from_cache(stats_cache_key, 600)  # 10 min
        
        if cached_stats:
            return jsonify({
                'success': True,
                'stats': cached_stats,
                'cached': True
            })
        
        # Calcula estatísticas
        total_problems = ProblemOfDay.query.filter_by(is_active=True).count()
        total_submissions = ProblemSubmission.query.count()
        correct_submissions = ProblemSubmission.query.filter_by(is_correct=True).count()
        
        success_rate = (correct_submissions / total_submissions * 100) if total_submissions > 0 else 0
        
        stats = {
            'total_problems': total_problems,
            'total_submissions': total_submissions,
            'success_rate': round(success_rate, 1),
            'cache_info': {
                'cached_items': len(_cache),
                'cache_hits_today': get_cache_hits_today()
            }
        }
        
        set_cache(stats_cache_key, stats)
        
        return jsonify({
            'success': True,
            'stats': stats,
            'cached': False
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def create_sample_problem():
    """
    Cria um problema exemplo otimizado para demonstração.
    """
    sample_problem = ProblemOfDay(
        title="Orçamento Familiar Inteligente",
        description="""
        A família Silva tem uma renda mensal de R$ 4.500. Eles querem organizar suas finanças de forma inteligente.
        
        📊 Informações atuais:
        • Gastos fixos (aluguel, contas): R$ 2.200
        • Alimentação: R$ 800
        • Transporte: R$ 400
        • Lazer: R$ 300
        
        🎯 Objetivos:
        • Economizar 20% da renda para emergências
        • Juntar R$ 3.600 para uma viagem em 8 meses
        
        💡 DESAFIO: Crie um plano financeiro completo. É possível atingir ambas as metas? Se não, que ajustes você sugere?
        """,
        category="personal_finance",
        difficulty="intermediate",
        expected_answer="Análise financeira com sugestões de ajustes no orçamento",
        solution_hints=json.dumps([
            "💰 Calcule quanto sobra: R$ 4.500 - R$ 3.700 = R$ 800",
            "🎯 Meta emergência: 20% de R$ 4.500 = R$ 900/mês",
            "✈️ Meta viagem: R$ 3.600 ÷ 8 meses = R$ 450/mês",
            "📊 Total necessário: R$ 900 + R$ 450 = R$ 1.350/mês",
            "⚠️ Déficit: R$ 1.350 - R$ 800 = R$ 550/mês",
            "🔧 Sugestão: Reduzir lazer para R$ 150 e otimizar outros gastos"
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

def evaluate_answer_optimized(problem_data, answer):
    """
    Avalia a resposta de forma otimizada com nível de confiança.
    """
    answer_lower = answer.lower()
    
    if problem_data.get('category') == "personal_finance":
        # Palavras-chave importantes
        key_terms = {
            'calculations': ['900', '450', '1350', '800', '550'],
            'concepts': ['deficit', 'sobra', 'economizar', 'cortar', 'ajuste', 'reduzir'],
            'solutions': ['lazer', 'transporte', 'alimentação', 'plano', 'orçamento']
        }
        
        scores = {}
        for category, terms in key_terms.items():
            matches = sum(1 for term in terms if term in answer_lower)
            scores[category] = matches / len(terms)
        
        # Calcula score geral
        overall_score = sum(scores.values()) / len(scores)
        
        # Determina se está correto e confiança
        is_correct = overall_score >= 0.4  # 40% dos termos-chave
        confidence = min(overall_score * 2, 1.0)  # Normaliza para 0-1
        
        return is_correct, round(confidence, 2)
    
    # Para outros tipos de problema
    word_count = len(answer.split())
    is_correct = word_count >= 20  # Resposta mínima de 20 palavras
    confidence = min(word_count / 50, 1.0)  # Confiança baseada no tamanho
    
    return is_correct, round(confidence, 2)

def generate_smart_feedback(problem_data, answer, is_correct, confidence):
    """
    Gera feedback inteligente baseado na análise da resposta.
    """
    if is_correct:
        if confidence > 0.8:
            return "🎉 Excelente! Sua análise está muito completa e demonstra ótima compreensão dos conceitos financeiros."
        elif confidence > 0.6:
            return "👏 Muito bem! Você captou os pontos principais. Sua abordagem está correta."
        else:
            return "✅ Bom trabalho! Você está no caminho certo, mas pode detalhar mais alguns aspectos."
    else:
        if confidence > 0.3:
            return "🤔 Boa tentativa! Você tocou em alguns pontos importantes, mas considere revisar os cálculos e usar as dicas."
        else:
            return "💡 Continue tentando! Que tal começar calculando quanto a família gasta atualmente? Use as dicas para te guiar."

def estimate_problem_time(problem_data):
    """
    Estima tempo necessário para resolver o problema.
    """
    difficulty = problem_data.get('difficulty', 'intermediate')
    description_length = len(problem_data.get('description', ''))
    
    base_times = {
        'easy': 5,
        'intermediate': 10,
        'hard': 20
    }
    
    base_time = base_times.get(difficulty, 10)
    
    # Ajusta baseado no tamanho da descrição
    if description_length > 500:
        base_time += 5
    
    return f"{base_time}-{base_time + 5} minutos"

def get_difficulty_description(difficulty):
    """
    Retorna descrição amigável da dificuldade.
    """
    descriptions = {
        'easy': '🟢 Fácil - Conceitos básicos',
        'intermediate': '🟡 Intermediário - Requer análise',
        'hard': '🔴 Difícil - Pensamento crítico'
    }
    return descriptions.get(difficulty, '🟡 Intermediário')

def calculate_points(is_correct, time_spent, confidence):
    """
    Calcula pontos baseado na performance.
    """
    if not is_correct:
        return 10  # Pontos de participação
    
    base_points = 100
    
    # Bônus por confiança
    confidence_bonus = int(confidence * 50)
    
    # Bônus por velocidade (se resolveu em menos de 10 min)
    speed_bonus = max(0, 30 - (time_spent // 60)) if time_spent < 600 else 0
    
    return base_points + confidence_bonus + speed_bonus

def get_next_suggestion(is_correct, problem_data):
    """
    Sugere próxima ação baseada na performance.
    """
    if is_correct:
        return "🚀 Parabéns! Que tal tentar um problema mais desafiador amanhã?"
    else:
        return "📚 Revise os conceitos de orçamento familiar e tente novamente!"

def get_cache_hits_today():
    """
    Conta hits de cache do dia (simulado).
    """
    return len(_cache) * 3  # Estimativa simples

