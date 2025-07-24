from flask import Blueprint, jsonify, request
from src.models.student import Student, db
from src.models.progress import Progress
from src.models.content import Content
from src.models.ai_personalization import AIPersonalization
from datetime import datetime
import json
import random

ai_simple_bp = Blueprint('ai_simple', __name__)

@ai_simple_bp.route('/ai/simple/analyze/<int:student_id>', methods=['POST'])
def simple_student_analysis(student_id):
    """Análise simplificada do estudante sem dependências pesadas"""
    student = Student.query.get_or_404(student_id)
    
    # Coletar dados básicos do estudante
    progress_records = Progress.query.filter_by(student_id=student_id).all()
    
    # Análise simplificada
    total_activities = len(progress_records)
    if total_activities > 0:
        avg_score = sum([p.score for p in progress_records if p.score]) / max(len([p for p in progress_records if p.score]), 1)
        completion_rate = len([p for p in progress_records if p.status in ['completed', 'mastered']]) / total_activities
    else:
        avg_score = 0
        completion_rate = 0
    
    # Determinar estilo de aprendizagem baseado em padrões simples
    learning_style = 'visual' if avg_score > 80 else 'mixed'
    
    # Salvar análise no banco
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        personalization = AIPersonalization(student_id=student_id)
        db.session.add(personalization)
    
    personalization.learning_style_detected = learning_style
    personalization.preferred_content_types = json.dumps(['video', 'interactive'])
    personalization.difficulty_preference = 'medium' if avg_score < 70 else 'hard'
    personalization.pace_preference = 'normal'
    personalization.strengths = json.dumps(['Mathematics'] if avg_score > 75 else [])
    personalization.weaknesses = json.dumps(['Algebra'] if avg_score < 60 else [])
    personalization.ai_confidence_score = min(avg_score / 100, 1.0)
    personalization.last_analysis_date = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Simple analysis completed successfully',
        'learning_profile': {
            'student_id': student_id,
            'learning_style': learning_style,
            'difficulty_preference': personalization.difficulty_preference,
            'pace_preference': personalization.pace_preference,
            'average_score': avg_score,
            'completion_rate': completion_rate,
            'total_activities': total_activities,
            'confidence_level': personalization.ai_confidence_score
        },
        'insights': {
            'primary_learning_style': learning_style,
            'recommended_difficulty': personalization.difficulty_preference,
            'engagement_level': 'High' if completion_rate > 0.8 else 'Medium' if completion_rate > 0.5 else 'Low',
            'confidence_level': 'High' if avg_score > 80 else 'Medium' if avg_score > 60 else 'Low'
        }
    })

@ai_simple_bp.route('/ai/simple/recommend/<int:student_id>', methods=['GET'])
def simple_content_recommendations(student_id):
    """Recomendações simplificadas de conteúdo"""
    student = Student.query.get_or_404(student_id)
    
    # Obter perfil de aprendizagem
    personalization = AIPersonalization.query.filter_by(student_id=student_id).first()
    if not personalization:
        return jsonify({'error': 'No learning profile found. Please run analysis first.'}), 400
    
    # Obter conteúdo disponível
    available_content = Content.query.filter_by(
        grade_level=student.grade_level,
        is_active=True
    ).limit(10).all()
    
    # Gerar recomendações simples
    recommendations = []
    for content in available_content:
        confidence_score = random.uniform(0.6, 0.95)  # Simular score de confiança
        
        # Lógica simples de recomendação
        reasoning = f"Adequado para seu nível ({student.grade_level})"
        if content.subject == 'Mathematics':
            reasoning += " - Matéria forte identificada"
        
        recommendations.append({
            'content_id': content.id,
            'title': content.title,
            'subject': content.subject,
            'difficulty_level': content.difficulty_level,
            'content_type': content.content_type,
            'singapore_stage': content.singapore_method_stage,
            'confidence_score': confidence_score,
            'reasoning': reasoning,
            'estimated_time': 30,  # tempo padrão
            'prerequisite_concepts': []
        })
    
    return jsonify({
        'student_id': student_id,
        'recommendations': recommendations[:8],  # Top 8 recomendações
        'profile_summary': {
            'learning_style': personalization.learning_style_detected,
            'difficulty_preference': personalization.difficulty_preference,
            'pace_preference': personalization.pace_preference,
            'confidence_level': personalization.ai_confidence_score
        },
        'recommendation_strategy': 'Simplified AI-powered personalization'
    })

@ai_simple_bp.route('/ai/simple/learning-path/<int:student_id>/<subject>', methods=['GET'])
def generate_simple_learning_path(student_id, subject):
    """Gera caminho de aprendizagem simplificado"""
    student = Student.query.get_or_404(student_id)
    
    # Obter conteúdo da matéria
    subject_content = Content.query.filter_by(
        subject=subject,
        grade_level=student.grade_level,
        is_active=True
    ).all()
    
    # Organizar por dificuldade
    easy_content = [c for c in subject_content if c.difficulty_level == 'easy']
    medium_content = [c for c in subject_content if c.difficulty_level == 'medium']
    hard_content = [c for c in subject_content if c.difficulty_level == 'hard']
    
    # Criar caminho baseado no Método de Singapura se for matemática
    if subject == 'Mathematics':
        learning_path = {
            'subject': subject,
            'method': 'Singapore Method (CPA)',
            'total_estimated_time': 21,
            'stages': [
                {
                    'stage': 'concrete',
                    'title': 'Concreto - Manipulação de Objetos',
                    'description': 'Aprendizagem através de objetos físicos e manipuláveis',
                    'content': [{'title': c.title, 'content_id': c.id} for c in easy_content[:3]],
                    'estimated_duration_days': 7
                },
                {
                    'stage': 'pictorial',
                    'title': 'Pictórico - Representação Visual',
                    'description': 'Representação visual através de desenhos e diagramas',
                    'content': [{'title': c.title, 'content_id': c.id} for c in medium_content[:3]],
                    'estimated_duration_days': 7
                },
                {
                    'stage': 'abstract',
                    'title': 'Abstrato - Símbolos Matemáticos',
                    'description': 'Uso de símbolos e equações matemáticas',
                    'content': [{'title': c.title, 'content_id': c.id} for c in hard_content[:3]],
                    'estimated_duration_days': 7
                }
            ]
        }
    else:
        learning_path = {
            'subject': subject,
            'method': 'Progressive Difficulty',
            'total_estimated_time': 15,
            'stages': [
                {
                    'stage': 'basic',
                    'title': 'Fundamentos',
                    'description': 'Conceitos básicos e fundamentais',
                    'content': [{'title': c.title, 'content_id': c.id} for c in easy_content[:3]],
                    'estimated_duration_days': 5
                },
                {
                    'stage': 'intermediate',
                    'title': 'Desenvolvimento',
                    'description': 'Aprofundamento dos conceitos',
                    'content': [{'title': c.title, 'content_id': c.id} for c in medium_content[:3]],
                    'estimated_duration_days': 5
                },
                {
                    'stage': 'advanced',
                    'title': 'Domínio',
                    'description': 'Aplicação avançada e síntese',
                    'content': [{'title': c.title, 'content_id': c.id} for c in hard_content[:3]],
                    'estimated_duration_days': 5
                }
            ]
        }
    
    return jsonify({
        'student_id': student_id,
        'subject': subject,
        'learning_path': learning_path,
        'personalization_notes': {
            'adapted_for_grade': student.grade_level,
            'total_content_items': len(subject_content),
            'method_used': learning_path['method']
        }
    })

@ai_simple_bp.route('/ai/simple/dashboard-data/<int:student_id>', methods=['GET'])
def get_dashboard_data(student_id):
    """Fornece dados para o dashboard do estudante"""
    student = Student.query.get_or_404(student_id)
    progress_records = Progress.query.filter_by(student_id=student_id).order_by(Progress.created_at.desc()).limit(10).all()
    
    # Calcular métricas
    if progress_records:
        recent_scores = [p.score for p in progress_records if p.score is not None]
        avg_score = sum(recent_scores) / len(recent_scores) if recent_scores else 0
        completion_rate = len([p for p in progress_records if p.status in ['completed', 'mastered']]) / len(progress_records)
    else:
        avg_score = 0
        completion_rate = 0
    
    # Simular dados de streak e conquistas
    streak_days = random.randint(5, 20)
    weekly_goal = min(avg_score + random.randint(5, 15), 100)
    
    # Atividades recentes
    activities = []
    for record in progress_records[:5]:
        if record.content:
            activities.append({
                'id': record.id,
                'subject': record.content.subject,
                'topic': record.content.title,
                'progress': record.score or 0,
                'time_spent': record.time_spent or 25,
                'status': record.status,
                'ai_recommendation': _get_simple_recommendation(record.score or 0)
            })
    
    # Insights de IA simplificados
    ai_insights = {
        'learning_style': 'Visual' if avg_score > 75 else 'Mixed',
        'strong_subjects': ['Mathematics'] if avg_score > 80 else [],
        'needs_improvement': ['Algebra'] if avg_score < 60 else [],
        'recommended_next_steps': [
            'Continue praticando exercícios similares',
            'Explore conteúdo visual interativo',
            'Mantenha consistência nos estudos'
        ]
    }
    
    return jsonify({
        'student': {
            'name': student.name,
            'grade': student.grade_level,
            'total_progress': int(avg_score),
            'weekly_goal': int(weekly_goal),
            'streak_days': streak_days,
            'achievements': [
                {'title': 'Estudante Dedicado', 'icon': 'trophy'},
                {'title': 'Sequência de 7 dias', 'icon': 'fire'},
                {'title': 'Matemática em Dia', 'icon': 'star'}
            ]
        },
        'recent_activities': activities,
        'ai_insights': ai_insights,
        'progress_chart': {
            'labels': [f'Atividade {i+1}' for i in range(len(recent_scores))],
            'values': recent_scores
        }
    })

def _get_simple_recommendation(score):
    """Gera recomendação simples baseada no score"""
    if score >= 90:
        return "Excelente! Pronto para conteúdo mais desafiador."
    elif score >= 75:
        return "Bom trabalho! Continue praticando."
    elif score >= 60:
        return "No caminho certo. Foque nas áreas de dificuldade."
    else:
        return "Precisa de mais prática. Considere revisar conceitos básicos."

