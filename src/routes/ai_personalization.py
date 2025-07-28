from flask import Blueprint, jsonify, request
from src.models.ai_personalization import AIPersonalization, db
from src.models.student import Student
from src.models.progress import Progress
from src.models.content import Content
from datetime import datetime
import json

ai_bp = Blueprint('ai_personalization', __name__)

@ai_bp.route('/ai/personalization/<int:student_id>', methods=['GET'])
def get_personalization(student_id):
    """Obter dados de personalização para um estudante"""
    student = Student.query.get_or_404(student_id)
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        return jsonify({'message': 'No personalization data found'}), 404
    return jsonify(personalization.to_dict())

@ai_bp.route('/simple/analyze/<int:student_id>', methods=['POST'])
def analyze_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    analysis = perform_ai_analysis(student)
    return jsonify(analysis)

    # Obter dados de progresso do estudante
    progress_records = Progress.query.filter_by(student_id=student_id).all()
    if not progress_records:
        return jsonify({'message': 'No progress data available for analysis'}), 400

    # Análise simples baseada no progresso
    analysis_result = _analyze_student_performance(progress_records)

    # Buscar ou criar registro de personalização
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        personalization = AIPersonalization(student_id=student_id)
        db.session.add(personalization)

    # Atualizar dados de personalização
    personalization.learning_style_detected = analysis_result['learning_style']
    personalization.preferred_content_types = json.dumps(analysis_result['preferred_content_types'])
    personalization.difficulty_preference = analysis_result['difficulty_preference']
    personalization.pace_preference = analysis_result['pace_preference']
    personalization.strengths = json.dumps(analysis_result['strengths'])
    personalization.weaknesses = json.dumps(analysis_result['weaknesses'])
    personalization.ai_confidence_score = analysis_result['confidence_score']
    personalization.last_analysis_date = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'message': 'Analysis completed successfully',
        'personalization': personalization.to_dict(),
        'analysis_summary': analysis_result
    })

@ai_bp.route('/ai/recommend/<int:student_id>', methods=['GET'])
def recommend_content(student_id):
    """Recomendar conteúdo personalizado para o estudante"""
    student = Student.query.get_or_404(student_id)
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        return jsonify({
            'message': 'No personalization data found. Please run analysis first.',
            'action_required': 'POST /ai/analyze/' + str(student_id)
        }), 400

    # Obter recomendações baseadas na personalização
    recommendations = _generate_content_recommendations(student, personalization)

    # Atualizar campo de recomendações
    personalization.recommended_next_content = json.dumps([rec['id'] for rec in recommendations])
    db.session.commit()

    return jsonify({
        'student_id': student_id,
        'recommendations': recommendations,
        'personalization_summary': {
            'learning_style': personalization.learning_style_detected,
            'difficulty_preference': personalization.difficulty_preference,
            'pace_preference': personalization.pace_preference
        }
    })

@ai_bp.route('/ai/adaptive-path/<int:student_id>', methods=['GET'])
def get_adaptive_learning_path(student_id):
    """Gerar caminho de aprendizagem adaptativo"""
    student = Student.query.get_or_404(student_id)
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        return jsonify({'message': 'No personalization data found'}), 400

    # Gerar caminho de aprendizagem baseado no Método de Singapura
    learning_path = _generate_singapore_method_path(student, personalization)

    return jsonify({
        'student_id': student_id,
        'learning_path': learning_path,
        'path_explanation': 'Adaptive learning path based on Singapore Method (CPA progression)'
    })

def _analyze_student_performance(progress_records):
    """Função auxiliar para analisar performance do estudante"""
    total_records = len(progress_records)
    completed_records = [p for p in progress_records if p.status == 'completed']
    mastered_records = [p for p in progress_records if p.status == 'mastered']

    # Calcular médias
    avg_score = (
        sum([p.score for p in progress_records if p.score]) /
        len([p for p in progress_records if p.score])
        if progress_records else 0
    )
    avg_time = (
        sum([p.time_spent for p in progress_records if p.time_spent]) /
        len([p for p in progress_records if p.time_spent])
        if progress_records else 0
    )

    # Análise de estilo de aprendizagem (simplificada)
    content_types = {}
    for record in progress_records:
        if record.content and record.score and record.score > 70:
            content_type = record.content.content_type
            content_types[content_type] = content_types.get(content_type, 0) + 1
    preferred_content_type = max(content_types, key=content_types.get) if content_types else 'mixed'

    # Determinar estilo de aprendizagem baseado no tipo de conteúdo preferido
    learning_style_map = {
        'video': 'visual',
        'audio': 'auditory',
        'game': 'kinesthetic',
        'text': 'visual',
        'exercise': 'kinesthetic'
    }
    learning_style = learning_style_map.get(preferred_content_type, 'mixed')

    # Análise de dificuldade
    if avg_score > 85:
        difficulty_preference = 'hard'
    elif avg_score > 70:
        difficulty_preference = 'medium'
    else:
        difficulty_preference = 'easy'

    # Análise de ritmo
    if avg_time < 15:  # menos de 15 minutos por conteúdo
        pace_preference = 'fast'
    elif avg_time > 45:  # mais de 45 minutos por conteúdo
        pace_preference = 'slow'
    else:
        pace_preference = 'normal'

    # Identificar pontos fortes e fracos por matéria
    subjects = {}
    for record in progress_records:
        if record.content and record.score:
            subject = record.content.subject
            subjects.setdefault(subject, []).append(record.score)

    strengths, weaknesses = [], []
    for subject, scores in subjects.items():
        avg_subject_score = sum(scores) / len(scores)
        if avg_subject_score > 80:
            strengths.append(subject)
        elif avg_subject_score < 60:
            weaknesses.append(subject)

    return {
        'learning_style': learning_style,
        'preferred_content_types': list(content_types.keys()),
        'difficulty_preference': difficulty_preference,
        'pace_preference': pace_preference,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'confidence_score': min(total_records / 10, 1.0),
        'performance_summary': {
            'avg_score': round(avg_score, 2),
            'completion_rate': len(completed_records) / total_records if total_records else 0,
            'mastery_rate': len(mastered_records) / total_records if total_records else 0
        }
    }

def _generate_content_recommendations(student, personalization):
    """Gerar recomendações de conteúdo baseadas na personalização"""
    weaknesses = json.loads(personalization.weaknesses) if personalization.weaknesses else []
    preferred_content_types = json.loads(personalization.preferred_content_types) if personalization.preferred_content_types else []

    # Buscar conteúdo relevante
    query = Content.query.filter_by(
        grade_level=student.grade_level,
        is_active=True
    )

    # Priorizar matérias fracas
    if weaknesses:
        query = query.filter(Content.subject.in_(weaknesses))

    # Filtrar por dificuldade preferida
    if personalization.difficulty_preference:
        query = query.filter_by(difficulty_level=personalization.difficulty_preference)

    # Filtrar por tipos de conteúdo preferidos
    if preferred_content_types:
        query = query.filter(Content.content_type.in_(preferred_content_types))

    content_list = query.limit(10).all()

    # Se não encontrou conteúdo suficiente, buscar mais geral
    if len(content_list) < 5:
        additional_content = Content.query.filter_by(
            grade_level=student.grade_level,
            is_active=True
        ).limit(10 - len(content_list)).all()
        content_list.extend(additional_content)

    recommendations = []
    for content in content_list:
        recommendations.append({
            'id': content.id,
            'title': content.title,
            'subject': content.subject,
            'content_type': content.content_type,
            'difficulty_level': content.difficulty_level,
            'singapore_method_stage': content.singapore_method_stage,
            'recommendation_reason': _get_recommendation_reason(content, personalization)
        })

    return recommendations

def _generate_singapore_method_path(student, personalization):
    """Gerar caminho de aprendizagem baseado no Método de Singapura (CPA)"""
    # Obter conteúdo de matemática para o nível do estudante
    math_content = Content.query.filter_by(
        subject='Mathematics',
        grade_level=student.grade_level,
        is_active=True
    ).all()

    # Organizar por estágio do Método de Singapura
    concrete_content = [c for c in math_content if c.singapore_method_stage == 'concrete']
    pictorial_content = [c for c in math_content if c.singapore_method_stage == 'pictorial']
    abstract_content = [c for c in math_content if c.singapore_method_stage == 'abstract']

    return {
        'stage_1_concrete': {
            'stage_name': 'Concreto - Manipulação de Objetos',
            'description': 'Aprendizagem através de objetos físicos e manipuláveis',
            'content': [c.to_dict() for c in concrete_content[:5]],
            'estimated_duration': '2-3 semanas'
        },
        'stage_2_pictorial': {
            'stage_name': 'Pictórico - Representação Visual',
            'description': 'Representação visual dos conceitos através de desenhos e diagramas',
            'content': [c.to_dict() for c in pictorial_content[:5]],
            'estimated_duration': '2-3 semanas'
        },
        'stage_3_abstract': {
            'stage_name': 'Abstrato - Símbolos Matemáticos',
            'description': 'Uso de símbolos e equações matemáticas',
            'content': [c.to_dict() for c in abstract_content[:5]],
            'estimated_duration': '3-4 semanas'
        }
    }

def _get_recommendation_reason(content, personalization):
    """Gerar razão para a recomendação"""
    reasons = []

    if personalization.weaknesses and content.subject in json.loads(personalization.weaknesses):
        reasons.append(f"Reforço em {content.subject}")
    if personalization.preferred_content_types and content.content_type in json.loads(personalization.preferred_content_types):
        reasons.append(f"Tipo de conteúdo preferido: {content.content_type}")
    if personalization.difficulty_preference == content.difficulty_level:
        reasons.append(f"Nível de dificuldade adequado: {content.difficulty_level}")
    if content.singapore_method_stage:
        reasons.append(f"Método de Singapura - Estágio: {content.singapore_method_stage}")

    return "; ".join(reasons) if reasons else "Conteúdo adequado para seu nível"
