import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

@dataclass
class LearningProfile:
    """Perfil de aprendizagem do estudante"""
    student_id: int
    learning_style: str  # visual, auditory, kinesthetic, mixed
    difficulty_preference: str  # easy, medium, hard, adaptive
    pace_preference: str  # slow, normal, fast, adaptive
    attention_span: int  # em minutos
    preferred_content_types: List[str]
    strong_subjects: List[str]
    weak_subjects: List[str]
    engagement_score: float  # 0-1
    confidence_level: float  # 0-1

@dataclass
class ContentRecommendation:
    """Recomendação de conteúdo personalizada"""
    content_id: int
    title: str
    subject: str
    difficulty_level: str
    content_type: str
    singapore_stage: Optional[str]
    confidence_score: float  # 0-1
    reasoning: str
    estimated_time: int  # em minutos
    prerequisite_concepts: List[str]

class AIPersonalizationEngine:
    """Motor de IA para personalização educacional"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.learning_style_classifier = None
        self.content_recommender = None
        self.performance_predictor = None
        
    def analyze_student_behavior(self, student_data: Dict) -> LearningProfile:
        """
        Analisa o comportamento do estudante e cria um perfil de aprendizagem
        """
        student_id = student_data['student_id']
        progress_records = student_data.get('progress_records', [])
        interaction_data = student_data.get('interactions', [])
        
        # Análise do estilo de aprendizagem
        learning_style = self._detect_learning_style(progress_records, interaction_data)
        
        # Análise de preferência de dificuldade
        difficulty_preference = self._analyze_difficulty_preference(progress_records)
        
        # Análise de ritmo de aprendizagem
        pace_preference = self._analyze_learning_pace(progress_records)
        
        # Análise de span de atenção
        attention_span = self._estimate_attention_span(interaction_data)
        
        # Identificação de tipos de conteúdo preferidos
        preferred_content_types = self._identify_preferred_content_types(progress_records)
        
        # Identificação de matérias fortes e fracas
        strong_subjects, weak_subjects = self._analyze_subject_performance(progress_records)
        
        # Cálculo de engajamento e confiança
        engagement_score = self._calculate_engagement_score(interaction_data)
        confidence_level = self._calculate_confidence_level(progress_records)
        
        return LearningProfile(
            student_id=student_id,
            learning_style=learning_style,
            difficulty_preference=difficulty_preference,
            pace_preference=pace_preference,
            attention_span=attention_span,
            preferred_content_types=preferred_content_types,
            strong_subjects=strong_subjects,
            weak_subjects=weak_subjects,
            engagement_score=engagement_score,
            confidence_level=confidence_level
        )
    
    def _detect_learning_style(self, progress_records: List, interaction_data: List) -> str:
        """Detecta o estilo de aprendizagem baseado no desempenho por tipo de conteúdo"""
        content_performance = {}
        
        for record in progress_records:
            if record.get('content') and record.get('score'):
                content_type = record['content'].get('content_type', 'unknown')
                score = record['score']
                
                if content_type not in content_performance:
                    content_performance[content_type] = []
                content_performance[content_type].append(score)
        
        # Calcular média de desempenho por tipo de conteúdo
        avg_performance = {}
        for content_type, scores in content_performance.items():
            avg_performance[content_type] = np.mean(scores)
        
        # Mapear tipos de conteúdo para estilos de aprendizagem
        style_mapping = {
            'video': 'visual',
            'image': 'visual',
            'audio': 'auditory',
            'game': 'kinesthetic',
            'simulation': 'kinesthetic',
            'text': 'mixed'
        }
        
        # Encontrar o estilo com melhor desempenho
        best_style_score = 0
        best_style = 'mixed'
        
        for content_type, score in avg_performance.items():
            style = style_mapping.get(content_type, 'mixed')
            if score > best_style_score:
                best_style_score = score
                best_style = style
        
        return best_style
    
    def _analyze_difficulty_preference(self, progress_records: List) -> str:
        """Analisa a preferência de dificuldade baseada no desempenho"""
        difficulty_performance = {'easy': [], 'medium': [], 'hard': []}
        
        for record in progress_records:
            if record.get('content') and record.get('score'):
                difficulty = record['content'].get('difficulty_level', 'medium')
                score = record['score']
                
                if difficulty in difficulty_performance:
                    difficulty_performance[difficulty].append(score)
        
        # Calcular performance média por dificuldade
        avg_scores = {}
        for difficulty, scores in difficulty_performance.items():
            if scores:
                avg_scores[difficulty] = np.mean(scores)
        
        if not avg_scores:
            return 'medium'
        
        # Avaliar desempenho por dificuldade e ajustar recomendação
        best_difficulty = max(avg_scores, key=avg_scores.get)
        
        # Se a performance em 'hard' for boa (>80), recomendar 'hard'
        if avg_scores.get('hard', 0) > 80:
            return 'hard'
        elif avg_scores.get('medium', 0) > 70:
            return 'medium'
        else:
            return 'easy'
    
    def _analyze_learning_pace(self, progress_records: List) -> str:
        """Analisa o ritmo de aprendizagem baseado no tempo gasto"""
        times = []
        
        for record in progress_records:
            if record.get('time_spent'):
                times.append(record['time_spent'])
        
        if not times:
            return 'normal'
        
        avg_time = np.mean(times)
        
        # Classificar ritmo baseado no tempo médio
        if avg_time < 15:  # menos de 15 minutos
            return 'fast'
        elif avg_time > 45:  # mais de 45 minutos
            return 'slow'
        else:
            return 'normal'
    
    def _estimate_attention_span(self, interaction_data: List) -> int:
        """Estima o span de atenção baseado nos dados de interação"""
        session_durations = []
        
        for interaction in interaction_data:
            if interaction.get('session_duration'):
                session_durations.append(interaction['session_duration'])
        
        if not session_durations:
            return 30  # padrão de 30 minutos
        
        # Usar a mediana para evitar outliers
        median_duration = np.median(session_durations)
        return int(min(max(median_duration, 10), 60))  # entre 10 e 60 minutos
    
    def _identify_preferred_content_types(self, progress_records: List) -> List[str]:
        """Identifica tipos de conteúdo preferidos baseado no engajamento"""
        content_engagement = {}
        
        for record in progress_records:
            if record.get('content') and record.get('score') and record.get('time_spent'):
                content_type = record['content'].get('content_type', 'unknown')
                score = record['score']
                time_spent = record['time_spent']
                
                # Calcular engajamento como combinação de score e tempo
                engagement = (score / 100) * min(time_spent / 30, 1)  # normalizar tempo para 30 min
                
                if content_type not in content_engagement:
                    content_engagement[content_type] = []
                content_engagement[content_type].append(engagement)
        
        # Calcular engajamento médio por tipo
        avg_engagement = {}
        for content_type, engagements in content_engagement.items():
            avg_engagement[content_type] = np.mean(engagements)
        
        # Retornar tipos com engajamento acima da média
        if not avg_engagement:
            return ['mixed']
        
        overall_avg = np.mean(list(avg_engagement.values()))
        preferred_types = [ct for ct, eng in avg_engagement.items() if eng > overall_avg]
        
        return preferred_types if preferred_types else ['mixed']
    
    def _analyze_subject_performance(self, progress_records: List) -> Tuple[List[str], List[str]]:
        """Analisa performance por matéria para identificar pontos fortes e fracos"""
        subject_performance = {}
        
        for record in progress_records:
            if record.get('content') and record.get('score'):
                subject = record['content'].get('subject', 'unknown')
                score = record['score']
                
                if subject not in subject_performance:
                    subject_performance[subject] = []
                subject_performance[subject].append(score)
        
        # Calcular média por matéria
        avg_scores = {}
        for subject, scores in subject_performance.items():
            avg_scores[subject] = np.mean(scores)
        
        if not avg_scores:
            return [], []
        
        # Classificar como forte (>75) ou fraco (<60)
        strong_subjects = [subj for subj, score in avg_scores.items() if score > 75]
        weak_subjects = [subj for subj, score in avg_scores.items() if score < 60]
        
        return strong_subjects, weak_subjects
    
    def _calculate_engagement_score(self, interaction_data: List) -> float:
        """Calcula score de engajamento baseado nas interações"""
        if not interaction_data:
            return 0.5  # neutro
        
        # Fatores de engajamento
        total_sessions = len(interaction_data)
        avg_session_duration = np.mean([i.get('session_duration', 0) for i in interaction_data])
        interaction_frequency = total_sessions / max(len(set([i.get('date', '') for i in interaction_data])), 1)
        
        # Normalizar e combinar fatores
        duration_score = min(avg_session_duration / 45, 1)  # normalizar para 45 min
        frequency_score = min(interaction_frequency / 3, 1)  # normalizar para 3 sessões/dia
        
        engagement_score = (duration_score + frequency_score) / 2
        return min(max(engagement_score, 0), 1)
    
    def _calculate_confidence_level(self, progress_records: List) -> float:
        """Calcula nível de confiança baseado no histórico de performance"""
        if not progress_records:
            return 0.5
        
        recent_scores = []
        for record in progress_records[-10:]:  # últimos 10 registros
            if record.get('score'):
                recent_scores.append(record['score'])
        
        if not recent_scores:
            return 0.5
        
        avg_score = np.mean(recent_scores)
        score_consistency = 1 - (np.std(recent_scores) / 100)  # penalizar inconsistência
        
        confidence = (avg_score / 100) * score_consistency
        return min(max(confidence, 0), 1)
    
    def generate_personalized_recommendations(self, 
                                            learning_profile: LearningProfile, 
                                            available_content: List[Dict],
                                            num_recommendations: int = 5) -> List[ContentRecommendation]:
        """
        Gera recomendações personalizadas de conteúdo baseadas no perfil de aprendizagem
        """
        recommendations = []
        
        # Filtrar conteúdo baseado no perfil
        filtered_content = self._filter_content_by_profile(available_content, learning_profile)
        
        # Calcular scores de recomendação
        content_scores = []
        for content in filtered_content:
            score = self._calculate_recommendation_score(content, learning_profile)
            content_scores.append((content, score))
        
        # Ordenar por score e pegar os melhores
        content_scores.sort(key=lambda x: x[1], reverse=True)
        top_content = content_scores[:num_recommendations]
        
        # Criar objetos de recomendação
        for content, score in top_content:
            reasoning = self._generate_recommendation_reasoning(content, learning_profile)
            estimated_time = self._estimate_completion_time(content, learning_profile)
            
            recommendation = ContentRecommendation(
                content_id=content['id'],
                title=content['title'],
                subject=content['subject'],
                difficulty_level=content['difficulty_level'],
                content_type=content['content_type'],
                singapore_stage=content.get('singapore_method_stage'),
                confidence_score=score,
                reasoning=reasoning,
                estimated_time=estimated_time,
                prerequisite_concepts=content.get('prerequisites', [])
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _filter_content_by_profile(self, content_list: List[Dict], profile: LearningProfile) -> List[Dict]:
        """Filtra conteúdo baseado no perfil do estudante"""
        filtered = []
        
        for content in content_list:
            # Filtrar por tipo de conteúdo preferido
            if content.get('content_type') in profile.preferred_content_types:
                filtered.append(content)
                continue
            
            # Incluir conteúdo de matérias fracas (para reforço)
            if content.get('subject') in profile.weak_subjects:
                filtered.append(content)
                continue
            
            # Incluir conteúdo de dificuldade apropriada
            if content.get('difficulty_level') == profile.difficulty_preference:
                filtered.append(content)
                continue
        
        # Se filtro muito restritivo, incluir mais conteúdo
        if len(filtered) < 10:
            filtered.extend([c for c in content_list if c not in filtered][:20])
        
        return filtered
    
    def _calculate_recommendation_score(self, content: Dict, profile: LearningProfile) -> float:
        """Calcula score de recomendação para um conteúdo específico"""
        score = 0.0
        
        # Score por tipo de conteúdo preferido
        if content.get('content_type') in profile.preferred_content_types:
            score += 0.3
        
        # Score por matéria fraca (reforço necessário)
        if content.get('subject') in profile.weak_subjects:
            score += 0.4
        
        # Score por matéria forte (manter momentum)
        if content.get('subject') in profile.strong_subjects:
            score += 0.2
        
        # Score por dificuldade apropriada
        if content.get('difficulty_level') == profile.difficulty_preference:
            score += 0.3
        
        # Bonus para Método de Singapura em matemática
        if content.get('subject') == 'Mathematics' and content.get('singapore_method_stage'):
            score += 0.2
        
        # Ajustar por nível de confiança
        score *= profile.confidence_level
        
        return min(score, 1.0)
    
    def _generate_recommendation_reasoning(self, content: Dict, profile: LearningProfile) -> str:
        """Gera explicação para a recomendação"""
        reasons = []
        
        if content.get('content_type') in profile.preferred_content_types:
            reasons.append(f"Tipo de conteúdo preferido: {content['content_type']}")
        
        if content.get('subject') in profile.weak_subjects:
            reasons.append(f"Reforço necessário em {content['subject']}")
        
        if content.get('difficulty_level') == profile.difficulty_preference:
            reasons.append(f"Nível de dificuldade adequado: {content['difficulty_level']}")
        
        if content.get('singapore_method_stage'):
            reasons.append(f"Método de Singapura - Estágio: {content['singapore_method_stage']}")
        
        if profile.learning_style == 'visual' and content.get('content_type') in ['video', 'image']:
            reasons.append("Adequado para aprendizagem visual")
        
        return "; ".join(reasons) if reasons else "Conteúdo adequado para seu perfil"
    
    def _estimate_completion_time(self, content: Dict, profile: LearningProfile) -> int:
        """Estima tempo de conclusão baseado no perfil"""
        base_time = 30  # tempo base em minutos
        
        # Ajustar por ritmo de aprendizagem
        pace_multipliers = {
            'slow': 1.5,
            'normal': 1.0,
            'fast': 0.7
        }
        
        multiplier = pace_multipliers.get(profile.pace_preference, 1.0)
        
        # Ajustar por dificuldade
        difficulty_multipliers = {
            'easy': 0.8,
            'medium': 1.0,
            'hard': 1.3
        }
        
        difficulty_mult = difficulty_multipliers.get(content.get('difficulty_level', 'medium'), 1.0)
        
        estimated_time = int(base_time * multiplier * difficulty_mult)
        
        # Limitar ao span de atenção
        return min(estimated_time, profile.attention_span)
    
    def predict_performance(self, student_profile: LearningProfile, content: Dict) -> Dict:
        """Prediz performance do estudante em um conteúdo específico"""
        base_score = 70  # score base
        
        # Ajustar baseado no perfil
        if content.get('subject') in student_profile.strong_subjects:
            base_score += 15
        elif content.get('subject') in student_profile.weak_subjects:
            base_score -= 10
        
        # Ajustar por tipo de conteúdo
        if content.get('content_type') in student_profile.preferred_content_types:
            base_score += 10
        
        # Ajustar por dificuldade
        difficulty_adjustments = {
            'easy': 10,
            'medium': 0,
            'hard': -5
        }
        
        base_score += difficulty_adjustments.get(content.get('difficulty_level', 'medium'), 0)
        
        # Ajustar por confiança
        base_score *= student_profile.confidence_level
        
        predicted_score = min(max(base_score, 0), 100)
        
        return {
            'predicted_score': predicted_score,
            'confidence': student_profile.confidence_level,
            'estimated_attempts': 1 if predicted_score > 80 else 2,
            'success_probability': predicted_score / 100
        }
    
    def generate_learning_path(self, 
                             student_profile: LearningProfile, 
                             target_subject: str,
                             available_content: List[Dict]) -> Dict:
        """
        Gera um caminho de aprendizagem personalizado para uma matéria específica
        """
        # Filtrar conteúdo da matéria
        subject_content = [c for c in available_content if c.get('subject') == target_subject]
        
        if target_subject == 'Mathematics':
            return self._generate_singapore_method_path(student_profile, subject_content)
        else:
            return self._generate_general_learning_path(student_profile, subject_content)
    
    def _generate_singapore_method_path(self, profile: LearningProfile, math_content: List[Dict]) -> Dict:
        """Gera caminho baseado no Método de Singapura"""
        # Organizar conteúdo por estágio CPA
        concrete_content = [c for c in math_content if c.get('singapore_method_stage') == 'concrete']
        pictorial_content = [c for c in math_content if c.get('singapore_method_stage') == 'pictorial']
        abstract_content = [c for c in math_content if c.get('singapore_method_stage') == 'abstract']
        
        # Personalizar cada estágio
        path = {
            'subject': 'Mathematics',
            'method': 'Singapore Method (CPA)',
            'total_estimated_time': 0,
            'stages': []
        }
        
        # Estágio Concreto
        concrete_recs = self.generate_personalized_recommendations(profile, concrete_content, 3)
        concrete_stage = {
            'stage': 'concrete',
            'title': 'Concreto - Manipulação de Objetos',
            'description': 'Aprendizagem através de objetos físicos e manipuláveis',
            'content': [self._recommendation_to_dict(rec) for rec in concrete_recs],
            'estimated_duration_days': 7,
            'learning_objectives': [
                'Compreender conceitos através da manipulação física',
                'Desenvolver intuição matemática',
                'Construir base sólida para abstração'
            ]
        }
        path['stages'].append(concrete_stage)
        
        # Estágio Pictórico
        pictorial_recs = self.generate_personalized_recommendations(profile, pictorial_content, 3)
        pictorial_stage = {
            'stage': 'pictorial',
            'title': 'Pictórico - Representação Visual',
            'description': 'Representação visual dos conceitos através de desenhos e diagramas',
            'content': [self._recommendation_to_dict(rec) for rec in pictorial_recs],
            'estimated_duration_days': 7,
            'learning_objectives': [
                'Traduzir conceitos concretos em representações visuais',
                'Usar modelos de barras e diagramas',
                'Preparar para abstração simbólica'
            ]
        }
        path['stages'].append(pictorial_stage)
        
        # Estágio Abstrato
        abstract_recs = self.generate_personalized_recommendations(profile, abstract_content, 3)
        abstract_stage = {
            'stage': 'abstract',
            'title': 'Abstrato - Símbolos Matemáticos',
            'description': 'Uso de símbolos e equações matemáticas',
            'content': [self._recommendation_to_dict(rec) for rec in abstract_recs],
            'estimated_duration_days': 10,
            'learning_objectives': [
                'Dominar símbolos e notações matemáticas',
                'Resolver problemas usando equações',
                'Aplicar conceitos em contextos diversos'
            ]
        }
        path['stages'].append(abstract_stage)
        
        path['total_estimated_time'] = sum([stage['estimated_duration_days'] for stage in path['stages']])
        
        return path
    
    def _generate_general_learning_path(self, profile: LearningProfile, content: List[Dict]) -> Dict:
        """Gera caminho de aprendizagem geral para outras matérias"""
        # Organizar por dificuldade
        easy_content = [c for c in content if c.get('difficulty_level') == 'easy']
        medium_content = [c for c in content if c.get('difficulty_level') == 'medium']
        hard_content = [c for c in content if c.get('difficulty_level') == 'hard']
        
        path = {
            'subject': content[0].get('subject', 'General') if content else 'General',
            'method': 'Progressive Difficulty',
            'total_estimated_time': 0,
            'stages': []
        }
        
        # Estágio Básico
        basic_recs = self.generate_personalized_recommendations(profile, easy_content, 3)
        basic_stage = {
            'stage': 'basic',
            'title': 'Fundamentos',
            'description': 'Conceitos básicos e fundamentais',
            'content': [self._recommendation_to_dict(rec) for rec in basic_recs],
            'estimated_duration_days': 5
        }
        path['stages'].append(basic_stage)
        
        # Estágio Intermediário
        intermediate_recs = self.generate_personalized_recommendations(profile, medium_content, 4)
        intermediate_stage = {
            'stage': 'intermediate',
            'title': 'Desenvolvimento',
            'description': 'Aprofundamento dos conceitos',
            'content': [self._recommendation_to_dict(rec) for rec in intermediate_recs],
            'estimated_duration_days': 8
        }
        path['stages'].append(intermediate_stage)
        
        # Estágio Avançado
        advanced_recs = self.generate_personalized_recommendations(profile, hard_content, 3)
        advanced_stage = {
            'stage': 'advanced',
            'title': 'Domínio',
            'description': 'Aplicação avançada e síntese',
            'content': [self._recommendation_to_dict(rec) for rec in advanced_recs],
            'estimated_duration_days': 7
        }
        path['stages'].append(advanced_stage)
        
        path['total_estimated_time'] = sum([stage['estimated_duration_days'] for stage in path['stages']])
        
        return path
    
    def _recommendation_to_dict(self, rec: ContentRecommendation) -> Dict:
        """Converte recomendação para dicionário"""
        return {
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
        }

