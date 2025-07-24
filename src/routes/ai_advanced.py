from flask import Blueprint, jsonify, request
from src.models.student import Student, db
from src.models.progress import Progress
from src.models.content import Content
from src.models.ai_personalization import AIPersonalization
from src.ai_engine import AIPersonalizationEngine, LearningProfile
from datetime import datetime
import json

ai_advanced_bp = Blueprint('ai_advanced', __name__)

# Instância global do motor de IA
ai_engine = AIPersonalizationEngine()

@ai_advanced_bp.route('/ai/advanced/analyze/<int:student_id>', methods=['POST'])
def advanced_student_analysis(student_id):
    """Análise avançada do estudante usando o motor de IA"""
    student = Student.query.get_or_404(student_id)
    
    # Coletar dados do estudante
    progress_records = Progress.query.filter_by(student_id=student_id).all()
    
    # Simular dados de interação (em produção, viria de logs reais)
    interaction_data = _generate_mock_interaction_data(student_id, len(progress_records))
    
    # Preparar dados para análise
    student_data = {
        'student_id': student_id,
        'progress_records': [
            {
                'content': {
                    'content_type': record.content.content_type if record.content else 'text',
                    'difficulty_level': record.content.difficulty_level if record.content else 'medium',
                    'subject': record.content.subject if record.content else 'General'
                },
                'score': record.score,
                'time_spent': record.time_spent,
                'status': record.status
            } for record in progress_records
        ],
        'interactions': interaction_data
    }
    
    # Executar análise avançada
    learning_profile = ai_engine.analyze_student_behavior(student_data)
    
    # Salvar perfil no banco de dados
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        personalization = AIPersonalization(student_id=student_id)
        db.session.add(personalization)
    
    # Atualizar com dados avançados
    personalization.learning_style_detected = learning_profile.learning_style
    personalization.preferred_content_types = json.dumps(learning_profile.preferred_content_types)
    personalization.difficulty_preference = learning_profile.difficulty_preference
    personalization.pace_preference = learning_profile.pace_preference
    personalization.strengths = json.dumps(learning_profile.strong_subjects)
    personalization.weaknesses = json.dumps(learning_profile.weak_subjects)
    personalization.ai_confidence_score = learning_profile.confidence_level
    personalization.last_analysis_date = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Advanced analysis completed successfully',
        'learning_profile': {
            'student_id': learning_profile.student_id,
            'learning_style': learning_profile.learning_style,
            'difficulty_preference': learning_profile.difficulty_preference,
            'pace_preference': learning_profile.pace_preference,
            'attention_span': learning_profile.attention_span,
            'preferred_content_types': learning_profile.preferred_content_types,
            'strong_subjects': learning_profile.strong_subjects,
            'weak_subjects': learning_profile.weak_subjects,
            'engagement_score': learning_profile.engagement_score,
            'confidence_level': learning_profile.confidence_level
        },
        'insights': {
            'primary_learning_style': learning_profile.learning_style,
            'optimal_session_duration': learning_profile.attention_span,
            'recommended_difficulty': learning_profile.difficulty_preference,
            'engagement_level': 'High' if learning_profile.engagement_score > 0.7 else 'Medium' if learning_profile.engagement_score > 0.4 else 'Low',
            'confidence_level': 'High' if learning_profile.confidence_level > 0.7 else 'Medium' if learning_profile.confidence_level > 0.4 else 'Low'
        }
    })

@ai_advanced_bp.route('/ai/advanced/recommend/<int:student_id>', methods=['GET'])
def advanced_content_recommendations(student_id):
    """Recomendações avançadas de conteúdo usando IA"""
    student = Student.query.get_or_404(student_id)
    
    # Obter perfil de aprendizagem
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        return jsonify({'error': 'No learning profile found. Please run advanced analysis first.'}), 400
    
    # Reconstruir perfil de aprendizagem
    learning_profile = LearningProfile(
        student_id=student_id,
        learning_style=personalization.learning_style_detected or 'mixed',
        difficulty_preference=personalization.difficulty_preference or 'medium',
        pace_preference=personalization.pace_preference or 'normal',
        attention_span=30,  # padrão
        preferred_content_types=json.loads(personalization.preferred_content_types) if personalization.preferred_content_types else ['mixed'],
        strong_subjects=json.loads(personalization.strengths) if personalization.strengths else [],
        weak_subjects=json.loads(personalization.weaknesses) if personalization.weaknesses else [],
        engagement_score=0.7,  # padrão
        confidence_level=personalization.ai_confidence_score or 0.5
    )
    
    # Obter conteúdo disponível
    available_content = Content.query.filter_by(
        grade_level=student.grade_level,
        is_active=True
    ).all()
    
    content_dicts = [content.to_dict() for content in available_content]
    
    # Gerar recomendações avançadas
    recommendations = ai_engine.generate_personalized_recommendations(
        learning_profile, 
        content_dicts, 
        num_recommendations=8
    )
    
    # Converter para formato JSON
    recommendations_json = []
    for rec in recommendations:
        recommendations_json.append({
            'content_id': rec.content_id,
            'title': rec.title,
            'subject': rec.subject,
            'difficulty_level': rec.difficulty_level,
            'content_type': rec.content_type,
            'singapore_stage': rec.singapore_stage,
            'confidence_score': rec.confidence_score,
            'reasoning': rec.reasoning,
            'estimated_time': rec.estimated_time,
            'prerequisite_concepts': rec.prerequisite_concepts
        })
    
    return jsonify({
        'student_id': student_id,
        'recommendations': recommendations_json,
        'profile_summary': {
            'learning_style': learning_profile.learning_style,
            'difficulty_preference': learning_profile.difficulty_preference,
            'pace_preference': learning_profile.pace_preference,
            'confidence_level': learning_profile.confidence_level
        },
        'recommendation_strategy': 'Advanced AI-powered personalization based on learning behavior analysis'
    })

@ai_advanced_bp.route('/ai/advanced/learning-path/<int:student_id>/<subject>', methods=['GET'])
def generate_advanced_learning_path(student_id, subject):
    """Gera caminho de aprendizagem avançado para uma matéria específica"""
    student = Student.query.get_or_404(student_id)
    
    # Obter perfil de aprendizagem
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        return jsonify({'error': 'No learning profile found. Please run advanced analysis first.'}), 400
    
    # Reconstruir perfil
    learning_profile = LearningProfile(
        student_id=student_id,
        learning_style=personalization.learning_style_detected or 'mixed',
        difficulty_preference=personalization.difficulty_preference or 'medium',
        pace_preference=personalization.pace_preference or 'normal',
        attention_span=30,
        preferred_content_types=json.loads(personalization.preferred_content_types) if personalization.preferred_content_types else ['mixed'],
        strong_subjects=json.loads(personalization.strengths) if personalization.strengths else [],
        weak_subjects=json.loads(personalization.weaknesses) if personalization.weaknesses else [],
        engagement_score=0.7,
        confidence_level=personalization.ai_confidence_score or 0.5
    )
    
    # Obter conteúdo da matéria
    subject_content = Content.query.filter_by(
        subject=subject,
        grade_level=student.grade_level,
        is_active=True
    ).all()
    
    content_dicts = [content.to_dict() for content in subject_content]
    
    # Gerar caminho de aprendizagem
    learning_path = ai_engine.generate_learning_path(
        learning_profile, 
        subject, 
        content_dicts
    )
    
    return jsonify({
        'student_id': student_id,
        'subject': subject,
        'learning_path': learning_path,
        'personalization_notes': {
            'adapted_for_style': learning_profile.learning_style,
            'difficulty_adjusted': learning_profile.difficulty_preference,
            'pace_optimized': learning_profile.pace_preference,
            'confidence_considered': learning_profile.confidence_level
        }
    })

@ai_advanced_bp.route('/ai/advanced/predict-performance/<int:student_id>/<int:content_id>', methods=['GET'])
def predict_student_performance(student_id, content_id):
    """Prediz performance do estudante em um conteúdo específico"""
    student = Student.query.get_or_404(student_id)
    content = Content.query.get_or_404(content_id)
    
    # Obter perfil de aprendizagem
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        return jsonify({'error': 'No learning profile found. Please run advanced analysis first.'}), 400
    
    # Reconstruir perfil
    learning_profile = LearningProfile(
        student_id=student_id,
        learning_style=personalization.learning_style_detected or 'mixed',
        difficulty_preference=personalization.difficulty_preference or 'medium',
        pace_preference=personalization.pace_preference or 'normal',
        attention_span=30,
        preferred_content_types=json.loads(personalization.preferred_content_types) if personalization.preferred_content_types else ['mixed'],
        strong_subjects=json.loads(personalization.strengths) if personalization.strengths else [],
        weak_subjects=json.loads(personalization.weaknesses) if personalization.weaknesses else [],
        engagement_score=0.7,
        confidence_level=personalization.ai_confidence_score or 0.5
    )
    
    # Predizer performance
    prediction = ai_engine.predict_performance(learning_profile, content.to_dict())
    
    return jsonify({
        'student_id': student_id,
        'content_id': content_id,
        'content_title': content.title,
        'prediction': prediction,
        'recommendations': {
            'study_approach': _get_study_approach_recommendation(learning_profile, content),
            'estimated_study_time': prediction.get('estimated_attempts', 1) * 30,
            'difficulty_adjustment': _get_difficulty_adjustment_recommendation(prediction['predicted_score']),
            'support_needed': 'High' if prediction['predicted_score'] < 60 else 'Medium' if prediction['predicted_score'] < 80 else 'Low'
        }
    })

@ai_advanced_bp.route('/ai/advanced/metacognition-tools/<int:student_id>', methods=['GET'])
def get_metacognition_tools(student_id):
    """Fornece ferramentas de metacognição personalizadas"""
    student = Student.query.get_or_404(student_id)
    
    # Obter dados de progresso recente
    recent_progress = Progress.query.filter_by(student_id=student_id).order_by(Progress.created_at.desc()).limit(10).all()
    
    # Analisar padrões de aprendizagem
    learning_patterns = _analyze_learning_patterns(recent_progress)
    
    # Gerar ferramentas de metacognição
    metacognition_tools = {
        'reflection_prompts': _generate_reflection_prompts(learning_patterns),
        'self_assessment_questions': _generate_self_assessment_questions(student.grade_level),
        'goal_setting_suggestions': _generate_goal_suggestions(learning_patterns),
        'learning_strategies': _suggest_learning_strategies(learning_patterns),
        'progress_visualization': _create_progress_visualization_data(recent_progress)
    }
    
    return jsonify({
        'student_id': student_id,
        'metacognition_tools': metacognition_tools,
        'learning_insights': learning_patterns,
        'next_steps': _generate_next_steps_recommendations(learning_patterns)
    })

def _generate_mock_interaction_data(student_id: int, num_records: int) -> list:
    """Gera dados de interação simulados para demonstração"""
    import random
    from datetime import datetime, timedelta
    
    interactions = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(min(num_records * 2, 20)):  # Simular interações
        interaction_date = base_date + timedelta(days=random.randint(0, 30))
        session_duration = random.randint(10, 60)  # 10-60 minutos
        
        interactions.append({
            'date': interaction_date.isoformat(),
            'session_duration': session_duration,
            'interactions_count': random.randint(5, 50),
            'completion_rate': random.uniform(0.6, 1.0)
        })
    
    return interactions

def _get_study_approach_recommendation(profile: LearningProfile, content) -> str:
    """Recomenda abordagem de estudo baseada no perfil"""
    if profile.learning_style == 'visual':
        return "Use diagramas, mapas mentais e recursos visuais. Faça anotações coloridas e organizadas."
    elif profile.learning_style == 'auditory':
        return "Leia em voz alta, use recursos de áudio e discuta o conteúdo. Grave resumos falados."
    elif profile.learning_style == 'kinesthetic':
        return "Use manipuláveis, faça experimentos práticos e tome pausas frequentes para movimento."
    else:
        return "Combine diferentes abordagens: visual, auditiva e prática para máxima efetividade."

def _get_difficulty_adjustment_recommendation(predicted_score: float) -> str:
    """Recomenda ajuste de dificuldade baseado na predição"""
    if predicted_score < 50:
        return "Considere começar com conteúdo mais básico ou usar recursos de apoio adicionais."
    elif predicted_score < 70:
        return "Conteúdo adequado, mas pode precisar de reforço e prática extra."
    elif predicted_score > 90:
        return "Considere conteúdo mais desafiador para manter o engajamento."
    else:
        return "Nível de dificuldade apropriado para seu perfil atual."

def _analyze_learning_patterns(progress_records) -> dict:
    """Analisa padrões de aprendizagem dos registros de progresso"""
    if not progress_records:
        return {'pattern': 'insufficient_data'}
    
    scores = [p.score for p in progress_records if p.score is not None]
    times = [p.time_spent for p in progress_records if p.time_spent is not None]
    
    patterns = {
        'average_score': sum(scores) / len(scores) if scores else 0,
        'score_trend': 'improving' if len(scores) > 1 and scores[-1] > scores[0] else 'stable',
        'average_time': sum(times) / len(times) if times else 0,
        'consistency': 'high' if len(scores) > 1 and max(scores) - min(scores) < 20 else 'variable',
        'completion_rate': len([p for p in progress_records if p.status in ['completed', 'mastered']]) / len(progress_records)
    }
    
    return patterns

def _generate_reflection_prompts(patterns) -> list:
    """Gera prompts de reflexão baseados nos padrões"""
    prompts = [
        "O que você aprendeu de mais importante hoje?",
        "Qual estratégia funcionou melhor para você?",
        "O que você faria diferente na próxima vez?",
        "Como você se sentiu durante o aprendizado?",
        "Que conexões você pode fazer com o que já sabia?"
    ]
    
    # Personalizar baseado nos padrões
    if patterns.get('score_trend') == 'improving':
        prompts.append("Você está melhorando! O que está contribuindo para esse progresso?")
    
    if patterns.get('consistency') == 'variable':
        prompts.append("Seus resultados variam. Que fatores podem estar influenciando isso?")
    
    return prompts

def _generate_self_assessment_questions(grade_level) -> list:
    """Gera questões de autoavaliação apropriadas para o nível"""
    base_questions = [
        "Em uma escala de 1-5, como você avalia sua compreensão do tópico?",
        "Você consegue explicar este conceito para um colega?",
        "Que partes ainda geram dúvidas?",
        "Como você aplicaria isso na vida real?"
    ]
    
    # Ajustar complexidade baseada no nível
    if grade_level in ['K', '1', '2', '3']:
        return [
            "Você entendeu bem? (😊 😐 😟)",
            "Consegue contar para alguém o que aprendeu?",
            "Do que você mais gostou?",
            "O que foi mais difícil?"
        ]
    
    return base_questions

def _generate_goal_suggestions(patterns) -> list:
    """Sugere metas baseadas nos padrões de aprendizagem"""
    suggestions = []
    
    avg_score = patterns.get('average_score', 0)
    
    if avg_score < 70:
        suggestions.append("Melhorar a pontuação média para acima de 75%")
        suggestions.append("Dedicar 15 minutos extras de estudo por dia")
    elif avg_score > 85:
        suggestions.append("Explorar conteúdo mais avançado")
        suggestions.append("Ajudar colegas com dificuldades")
    
    if patterns.get('consistency') == 'variable':
        suggestions.append("Manter consistência nos resultados")
        suggestions.append("Estabelecer rotina de estudos regular")
    
    return suggestions

def _suggest_learning_strategies(patterns) -> list:
    """Sugere estratégias de aprendizagem"""
    strategies = [
        "Técnica Pomodoro: 25 min de estudo + 5 min de pausa",
        "Mapas mentais para organizar informações",
        "Ensinar o conteúdo para alguém (técnica Feynman)",
        "Revisão espaçada: revisar após 1 dia, 3 dias, 1 semana"
    ]
    
    if patterns.get('average_time', 0) > 45:
        strategies.append("Quebrar sessões longas em períodos menores")
    
    if patterns.get('completion_rate', 0) < 0.8:
        strategies.append("Definir metas menores e mais alcançáveis")
    
    return strategies

def _create_progress_visualization_data(progress_records) -> dict:
    """Cria dados para visualização do progresso"""
    if not progress_records:
        return {'type': 'no_data'}
    
    # Preparar dados para gráfico de progresso
    dates = []
    scores = []
    
    for record in progress_records[-10:]:  # últimos 10 registros
        if record.score is not None:
            dates.append(record.created_at.strftime('%Y-%m-%d'))
            scores.append(record.score)
    
    return {
        'type': 'line_chart',
        'title': 'Progresso nas Últimas Atividades',
        'data': {
            'labels': dates,
            'values': scores
        },
        'insights': {
            'trend': 'improving' if len(scores) > 1 and scores[-1] > scores[0] else 'stable',
            'best_score': max(scores) if scores else 0,
            'average_score': sum(scores) / len(scores) if scores else 0
        }
    }

def _generate_next_steps_recommendations(patterns) -> list:
    """Gera recomendações de próximos passos"""
    recommendations = []
    
    avg_score = patterns.get('average_score', 0)
    
    if avg_score < 60:
        recommendations.append("Revisar conceitos fundamentais")
        recommendations.append("Buscar ajuda adicional ou tutoria")
    elif avg_score < 80:
        recommendations.append("Praticar exercícios adicionais")
        recommendations.append("Focar nas áreas de maior dificuldade")
    else:
        recommendations.append("Explorar tópicos avançados")
        recommendations.append("Aplicar conhecimentos em projetos práticos")
    
    if patterns.get('completion_rate', 0) < 0.7:
        recommendations.append("Melhorar consistência na conclusão de atividades")
    
    return recommendations

