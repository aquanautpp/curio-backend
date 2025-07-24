import random
import re
from datetime import datetime

class AITutorEngine:
    """
    Engine de IA para o tutor virtual que guia estudantes através de perguntas
    e dicas, sem dar respostas diretas.
    """
    
    def __init__(self):
        self.conversation_starters = [
            "Olá! Estou aqui para te ajudar com o problema de hoje. Por onde você gostaria de começar?",
            "Oi! Vamos trabalhar juntos neste problema. Qual parte você achou mais interessante?",
            "Olá! Que bom te ver aqui. Já deu uma olhada no problema? O que você entendeu até agora?"
        ]
        
        self.encouragement_phrases = [
            "Você está no caminho certo!",
            "Boa reflexão!",
            "Interessante perspectiva!",
            "Continue pensando assim!",
            "Excelente raciocínio!"
        ]
        
        self.guiding_questions = {
            'financial': [
                "Que informações você tem sobre a renda da família?",
                "Quais são os gastos fixos que você identificou?",
                "Como você calcularia quanto sobra no orçamento atual?",
                "O que significa economizar 20% da renda?",
                "Como você dividiria o custo da viagem pelos meses disponíveis?"
            ],
            'math': [
                "Que operações matemáticas você precisa fazer aqui?",
                "Como você organizaria os números do problema?",
                "Qual é a primeira conta que você faria?",
                "Como você verificaria se sua resposta faz sentido?"
            ],
            'general': [
                "O que o problema está pedindo exatamente?",
                "Quais informações você tem disponíveis?",
                "Como você dividiria este problema em partes menores?",
                "Que estratégia você usaria para resolver isso?"
            ]
        }
        
        self.hint_patterns = {
            'calculation': [
                "Que tal fazer os cálculos passo a passo?",
                "Comece somando todos os gastos atuais.",
                "Lembre-se: renda total - gastos = sobra disponível.",
                "Para porcentagem: valor × (porcentagem ÷ 100)"
            ],
            'organization': [
                "Tente organizar as informações em uma lista.",
                "Que tal separar o que você sabe do que precisa descobrir?",
                "Faça uma tabela com receitas e despesas."
            ],
            'strategy': [
                "Pense em diferentes cenários possíveis.",
                "E se eles cortassem alguns gastos?",
                "Existem outras formas de aumentar a renda?",
                "Como outras famílias resolveriam isso?"
            ]
        }
    
    def generate_response(self, student_message, conversation_history, problem_context=None):
        """
        Gera uma resposta do tutor baseada na mensagem do estudante e no contexto.
        """
        student_message = student_message.lower().strip()
        
        # Primeira mensagem da conversa
        if len(conversation_history) == 0:
            return {
                'message': random.choice(self.conversation_starters),
                'type': 'greeting'
            }
        
        # Detecta o tipo de resposta necessária
        response_type = self._analyze_student_message(student_message)
        
        if response_type == 'needs_encouragement':
            return self._generate_encouragement(student_message)
        elif response_type == 'needs_guidance':
            return self._generate_guiding_question(student_message, problem_context)
        elif response_type == 'needs_hint':
            return self._generate_hint(student_message, problem_context)
        elif response_type == 'good_progress':
            return self._generate_progress_feedback(student_message)
        else:
            return self._generate_general_response(student_message)
    
    def _analyze_student_message(self, message):
        """
        Analisa a mensagem do estudante para determinar o tipo de resposta necessária.
        """
        # Palavras que indicam confusão ou dificuldade
        confusion_words = ['não entendo', 'confuso', 'difícil', 'não sei', 'ajuda', 'perdido']
        
        # Palavras que indicam progresso
        progress_words = ['calculei', 'descobri', 'acho que', 'resultado', 'resposta']
        
        # Palavras que pedem dicas
        hint_words = ['dica', 'hint', 'como', 'qual', 'onde']
        
        if any(word in message for word in confusion_words):
            return 'needs_encouragement'
        elif any(word in message for word in hint_words):
            return 'needs_hint'
        elif any(word in message for word in progress_words):
            return 'good_progress'
        else:
            return 'needs_guidance'
    
    def _generate_encouragement(self, message):
        """
        Gera uma mensagem de encorajamento.
        """
        encouragement = random.choice(self.encouragement_phrases)
        follow_up = random.choice([
            "Vamos tentar uma abordagem diferente.",
            "Que tal começarmos com algo mais simples?",
            "Não se preocupe, vamos resolver isso juntos.",
            "Todo mundo tem dificuldades às vezes. O importante é continuar tentando!"
        ])
        
        return {
            'message': f"{encouragement} {follow_up}",
            'type': 'encouragement'
        }
    
    def _generate_guiding_question(self, message, problem_context):
        """
        Gera uma pergunta para guiar o estudante.
        """
        # Determina o tipo de problema baseado no contexto
        if problem_context and 'category' in problem_context:
            category = problem_context['category']
            if category == 'personal_finance':
                questions = self.guiding_questions['financial']
            else:
                questions = self.guiding_questions['general']
        else:
            questions = self.guiding_questions['general']
        
        question = random.choice(questions)
        
        return {
            'message': question,
            'type': 'question'
        }
    
    def _generate_hint(self, message, problem_context):
        """
        Gera uma dica específica.
        """
        # Detecta que tipo de dica é necessária
        if 'calcul' in message or 'conta' in message or 'número' in message:
            hints = self.hint_patterns['calculation']
        elif 'organiz' in message or 'como' in message:
            hints = self.hint_patterns['organization']
        else:
            hints = self.hint_patterns['strategy']
        
        hint = random.choice(hints)
        
        return {
            'message': f"💡 Dica: {hint}",
            'type': 'hint'
        }
    
    def _generate_progress_feedback(self, message):
        """
        Gera feedback quando o estudante mostra progresso.
        """
        feedback_options = [
            "Muito bem! Você está pensando na direção certa.",
            "Excelente! Continue desenvolvendo essa ideia.",
            "Boa! Agora, como você pode verificar se isso está correto?",
            "Interessante! E o que mais você pode descobrir com essa informação?"
        ]
        
        feedback = random.choice(feedback_options)
        
        return {
            'message': feedback,
            'type': 'feedback'
        }
    
    def _generate_general_response(self, message):
        """
        Gera uma resposta geral quando não há padrão específico detectado.
        """
        responses = [
            "Entendi. Como você chegou a essa conclusão?",
            "Interessante. Pode me explicar seu raciocínio?",
            "Certo. Que tal verificarmos isso passo a passo?",
            "Ok. O que você faria em seguida?",
            "Compreendo. Como isso se relaciona com o problema?"
        ]
        
        return {
            'message': random.choice(responses),
            'type': 'general'
        }
    
    def should_provide_hint(self, conversation_history):
        """
        Determina se é hora de oferecer uma dica baseado no histórico da conversa.
        """
        if len(conversation_history) < 3:
            return False
        
        # Verifica se o estudante está lutando (muitas mensagens de confusão)
        recent_messages = conversation_history[-3:]
        confusion_count = sum(1 for msg in recent_messages 
                            if msg.get('sender') == 'student' and 
                            any(word in msg.get('message', '').lower() 
                                for word in ['não sei', 'difícil', 'confuso']))
        
        return confusion_count >= 2
    
    def generate_summary(self, conversation_history):
        """
        Gera um resumo da conversa para análise posterior.
        """
        student_messages = [msg for msg in conversation_history if msg.get('sender') == 'student']
        tutor_messages = [msg for msg in conversation_history if msg.get('sender') == 'tutor']
        
        return {
            'total_messages': len(conversation_history),
            'student_messages': len(student_messages),
            'tutor_messages': len(tutor_messages),
            'hints_given': len([msg for msg in tutor_messages if msg.get('type') == 'hint']),
            'encouragements_given': len([msg for msg in tutor_messages if msg.get('type') == 'encouragement']),
            'engagement_level': 'high' if len(student_messages) > 5 else 'medium' if len(student_messages) > 2 else 'low'
        }

