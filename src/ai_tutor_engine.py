import random
import re
from datetime import datetime

class AITutorEngine:
    """
    Engine de IA para o tutor virtual educacional que funciona como um ChatGPT
    amigável e comunicativo, especialmente adaptado para crianças.
    """
    
    def __init__(self):
        self.tutor_name = "Curió"
        self.conversation_starters = [
            f"Oi! Eu sou o {self.tutor_name}, seu tutor virtual! 😊 Estou aqui para te ajudar com qualquer dúvida que você tiver. Sobre o que você gostaria de conversar hoje?",
            f"Olá! Que bom te ver aqui! Sou o {self.tutor_name} e adoro ajudar crianças a aprender coisas novas. O que você está estudando ou tem curiosidade para saber?",
            f"Oi, amiguinho! Eu sou o {self.tutor_name}, seu assistente de estudos! 🎓 Pode me perguntar sobre matemática, ciências, história, português... qualquer coisa! Do que você quer falar?"
        ]
        
        self.encouragement_phrases = [
            "Que pergunta interessante! 🤔",
            "Adorei sua curiosidade! 🌟",
            "Você está pensando muito bem! 👏",
            "Excelente pergunta! 💡",
            "Que legal que você quer aprender isso! 🎉",
            "Muito bem! Continue assim! ⭐",
            "Você é muito esperto! 🧠",
            "Que raciocínio incrível! 🚀"
        ]
        
        # Base de conhecimento educacional para crianças
        self.educational_knowledge = {
            'matematica': {
                'adicao': {
                    'explanation': "A adição é quando juntamos números! É como juntar brinquedos: se você tem 3 carrinhos e ganha mais 2, fica com 5 carrinhos no total! 🚗",
                    'examples': ["2 + 3 = 5 (como juntar 2 maçãs com 3 maçãs)", "10 + 5 = 15 (como somar seus dedos!)"],
                    'tips': "Uma dica legal: você pode usar os dedos para contar, ou imaginar objetos que você gosta!"
                },
                'subtracao': {
                    'explanation': "A subtração é quando tiramos algo! É como comer biscoitos: se você tinha 8 biscoitos e comeu 3, sobraram 5! 🍪",
                    'examples': ["8 - 3 = 5 (como comer biscoitos)", "10 - 4 = 6 (como dar brinquedos para amigos)"],
                    'tips': "Imagine que você está dando ou perdendo coisas para entender melhor!"
                },
                'multiplicacao': {
                    'explanation': "A multiplicação é uma forma rápida de somar números iguais! É como ter grupos de coisas: 3 × 4 significa 3 grupos com 4 coisas cada! 📦",
                    'examples': ["3 × 4 = 12 (3 caixas com 4 bolas cada)", "2 × 5 = 10 (2 mãos com 5 dedos cada)"],
                    'tips': "Pense em grupos ou fileiras de objetos iguais!"
                },
                'divisao': {
                    'explanation': "A divisão é quando dividimos coisas igualmente! É como repartir doces entre amigos: 12 ÷ 3 = 4 significa que cada um dos 3 amigos ganha 4 doces! 🍬",
                    'examples': ["12 ÷ 3 = 4 (dividir 12 doces para 3 amigos)", "20 ÷ 4 = 5 (dividir 20 brinquedos em 4 grupos)"],
                    'tips': "Imagine que você está repartindo coisas de forma justa!"
                },
                'fracao': {
                    'explanation': "Frações são partes de um todo! É como dividir uma pizza: se você corta uma pizza em 4 pedaços e come 1, você comeu 1/4 da pizza! 🍕",
                    'examples': ["1/2 = metade (como meio sanduíche)", "1/4 = um quarto (como um pedaço de pizza)", "3/4 = três quartos (como 3 pedaços de uma pizza de 4)"],
                    'tips': "Pense em coisas que você pode dividir, como chocolates, pizzas ou bolos!"
                },
                'geometria': {
                    'explanation': "Geometria é o estudo das formas! Olhe ao seu redor - tudo tem uma forma: círculos, quadrados, triângulos! 🔺⭕🟩",
                    'examples': ["Círculo: bola, roda, moeda", "Quadrado: janela, dado, caixa", "Triângulo: fatia de pizza, telhado, cone de trânsito"],
                    'tips': "Procure formas geométricas nos objetos ao seu redor!"
                }
            },
            'ciencias': {
                'animais': {
                    'explanation': "Os animais são seres vivos incríveis! Eles respiram, se movem, comem e têm filhotes. Cada animal é especial e tem características únicas! 🐾",
                    'examples': ["Mamíferos: gatos, cachorros, elefantes", "Aves: papagaios, águias, pinguins", "Peixes: tubarões, peixe-palhaço, salmão"],
                    'tips': "Observe os animais ao seu redor e veja como eles são diferentes!"
                },
                'plantas': {
                    'explanation': "As plantas são seres vivos que fazem sua própria comida usando a luz do sol! Elas são super importantes porque nos dão oxigênio para respirar! 🌱",
                    'examples': ["Árvores: carvalho, pinheiro, mangueira", "Flores: rosa, girassol, margarida", "Vegetais: alface, cenoura, tomate"],
                    'tips': "Plante uma sementinha e observe ela crescer!"
                },
                'corpo_humano': {
                    'explanation': "Nosso corpo é uma máquina incrível! Cada parte tem uma função especial para nos manter vivos e saudáveis! ❤️",
                    'examples': ["Coração: bombeia sangue", "Pulmões: nos ajudam a respirar", "Cérebro: controla tudo"],
                    'tips': "Cuide bem do seu corpo comendo bem, bebendo água e se exercitando!"
                },
                'espaco': {
                    'explanation': "O espaço é gigantesco e cheio de mistérios! Lá existem planetas, estrelas, a Lua e muito mais! É como um oceano infinito de aventuras! 🚀",
                    'examples': ["Planetas: Terra, Marte, Júpiter", "Estrelas: Sol, Sirius, Polaris", "Outros: Lua, cometas, asteroides"],
                    'tips': "Olhe para o céu à noite e tente encontrar as estrelas e a Lua!"
                },
                'agua': {
                    'explanation': "A água é super importante para a vida! Ela pode ser líquida (como na torneira), sólida (gelo) ou gasosa (vapor)! 💧",
                    'examples': ["Líquida: chuva, rios, oceanos", "Sólida: gelo, neve, granizo", "Gasosa: vapor, nuvens"],
                    'tips': "Observe como a água muda de forma quando esquenta ou esfria!"
                },
                'dinossauros': {
                    'explanation': "Os dinossauros eram animais gigantes que viveram há muito, muito tempo! Alguns eram enormes, outros pequenos, alguns comiam plantas e outros comiam carne! 🦕",
                    'examples': ["Herbívoros: Brontossauro, Triceratops", "Carnívoros: Tiranossauro Rex, Velociraptor", "Voadores: Pterodáctilo"],
                    'tips': "Visite um museu para ver esqueletos de dinossauros de verdade!"
                }
            },
            'historia': {
                'brasil': {
                    'explanation': "O Brasil tem uma história muito rica e interessante! Nosso país foi formado por muitos povos diferentes: indígenas, africanos e europeus! 🇧🇷",
                    'examples': ["Povos indígenas viviam aqui primeiro", "Portugueses chegaram em 1500", "Pessoas da África vieram trabalhar aqui"],
                    'tips': "Cada região do Brasil tem suas próprias tradições especiais!"
                },
                'descobrimentos': {
                    'explanation': "Ao longo da história, pessoas corajosas fizeram descobertas incríveis que mudaram o mundo! 🗺️",
                    'examples': ["Cristóvão Colombo descobriu a América", "Pedro Álvares Cabral chegou ao Brasil", "Santos Dumont inventou o avião"],
                    'tips': "Você também pode ser um descobridor! Sempre faça perguntas e explore!"
                },
                'inventos': {
                    'explanation': "As pessoas sempre inventaram coisas para tornar a vida mais fácil! Muitas coisas que usamos hoje foram inventadas há muito tempo! 💡",
                    'examples': ["Roda: para transportar coisas", "Escrita: para guardar informações", "Telefone: para falar com pessoas longe"],
                    'tips': "Pense em como seria sua vida sem essas invenções!"
                }
            },
            'portugues': {
                'alfabeto': {
                    'explanation': "O alfabeto é formado por 26 letras que usamos para escrever todas as palavras! Cada letra tem um som especial! 📝",
                    'examples': ["Vogais: A, E, I, O, U", "Consoantes: B, C, D, F, G...", "Juntas formam palavras como CASA, BOLA, GATO"],
                    'tips': "Pratique escrevendo seu nome e palavras que você gosta!"
                },
                'leitura': {
                    'explanation': "Ler é como viajar para mundos mágicos! Cada livro é uma aventura nova esperando por você! 📚",
                    'examples': ["Histórias de aventura", "Contos de fadas", "Livros sobre animais"],
                    'tips': "Comece com livros que tenham figuras bonitas e histórias curtas!"
                },
                'escrita': {
                    'explanation': "Escrever é uma forma de expressar seus pensamentos e sentimentos! É como pintar com palavras! ✍️",
                    'examples': ["Cartas para amigos", "Histórias inventadas", "Diário pessoal"],
                    'tips': "Comece escrevendo sobre coisas que você gosta!"
                }
            },
            'geografia': {
                'brasil': {
                    'explanation': "O Brasil é um país enorme e cheio de lugares diferentes! Temos praias, florestas, montanhas e muito mais! 🏞️",
                    'examples': ["Regiões: Norte, Nordeste, Centro-Oeste, Sudeste, Sul", "Biomas: Amazônia, Cerrado, Mata Atlântica", "Cidades: São Paulo, Rio de Janeiro, Brasília"],
                    'tips': "Olhe um mapa do Brasil e encontre onde você mora!"
                },
                'mundo': {
                    'explanation': "Nosso planeta Terra é incrível! Existem muitos países diferentes, cada um com suas próprias culturas e tradições! 🌍",
                    'examples': ["Continentes: América, Europa, Ásia, África, Oceania, Antártida", "Oceanos: Atlântico, Pacífico, Índico", "Países: França, Japão, Egito"],
                    'tips': "Use um globo ou mapa-múndi para explorar o mundo!"
                },
                'natureza': {
                    'explanation': "A natureza é cheia de maravilhas! Rios, montanhas, florestas e oceanos formam nosso belo planeta! 🏔️",
                    'examples': ["Rios: Amazonas, Nilo, Mississippi", "Montanhas: Everest, Andes, Alpes", "Florestas: Amazônia, Taiga, Mata Atlântica"],
                    'tips': "Explore a natureza perto de você e observe sua beleza!"
                }
            }
        }
        
        # Respostas para perguntas comuns de crianças
        self.common_questions = {
            'por que': [
                "Que pergunta curiosa! Vou te explicar de um jeito fácil de entender...",
                "Adorei sua pergunta! É assim que aprendemos coisas novas...",
                "Excelente pergunta! Deixe-me te contar..."
            ],
            'como': [
                "Vou te ensinar passo a passo!",
                "É mais fácil do que parece! Vamos ver...",
                "Que legal que você quer aprender como fazer isso!"
            ],
            'o que é': [
                "Vou te explicar de um jeito bem simples!",
                "É uma ótima pergunta! Deixe-me te contar...",
                "Vou te dar uma explicação que você vai entender facilmente!"
            ]
        }
        
        # Tópicos que o tutor pode abordar
        self.supported_topics = [
            'matemática', 'ciências', 'história', 'português', 'geografia',
            'animais', 'plantas', 'espaço', 'dinossauros', 'corpo humano',
            'países', 'culturas', 'invenções', 'arte', 'música', 'frações',
            'geometria', 'água', 'brasil', 'mundo', 'natureza', 'escrita', 'leitura'
        ]
        
        # Palavras-chave expandidas para melhor reconhecimento
        self.topic_keywords = {
            'matematica': [
                'matemática', 'conta', 'número', 'somar', 'subtrair', 'multiplicar', 'dividir', 
                'adição', 'subtração', 'multiplicação', 'divisão', 'calcular', 'soma', 'menos',
                'vezes', 'fração', 'metade', 'geometria', 'forma', 'círculo', 'quadrado', 
                'triângulo', 'retângulo', 'tabuada', 'problema', 'resolver'
            ],
            'ciencias': [
                'ciência', 'animal', 'planta', 'corpo', 'natureza', 'experimento', 'biologia', 
                'física', 'química', 'espaço', 'planeta', 'estrela', 'lua', 'sol', 'dinossauro',
                'água', 'ar', 'terra', 'fogo', 'mamífero', 'pássaro', 'peixe', 'inseto',
                'árvore', 'flor', 'folha', 'raiz', 'coração', 'pulmão', 'cérebro', 'sangue'
            ],
            'historia': [
                'história', 'brasil', 'descobrimento', 'passado', 'antigo', 'guerra', 'rei', 
                'presidente', 'índio', 'indígena', 'português', 'africano', 'escravidão',
                'independência', 'cabral', 'colombo', 'invenção', 'inventor', 'santos dumont'
            ],
            'portugues': [
                'português', 'palavra', 'letra', 'escrever', 'ler', 'alfabeto', 'texto', 
                'história', 'livro', 'frase', 'vogal', 'consoante', 'sílaba', 'rima',
                'poesia', 'conto', 'fábula', 'redação', 'gramática', 'leitura', 'escrita'
            ],
            'geografia': [
                'geografia', 'mapa', 'país', 'cidade', 'estado', 'região', 'continente',
                'oceano', 'rio', 'montanha', 'floresta', 'praia', 'clima', 'cultura',
                'população', 'capital', 'bandeira', 'mundo', 'terra', 'globo'
            ]
        }
    
    def generate_response(self, student_message, conversation_history, problem_context=None):
        """
        Gera uma resposta do tutor baseada na mensagem do estudante.
        Agora funciona como um ChatGPT educacional amigável para crianças.
        """
        student_message = student_message.lower().strip()
        
        # Primeira mensagem da conversa
        if len(conversation_history) == 0:
            return {
                'message': random.choice(self.conversation_starters),
                'type': 'greeting'
            }
        
        # Detecta o tipo de pergunta/mensagem
        response_type = self._analyze_student_message(student_message)
        
        if response_type == 'math_question':
            return self._handle_math_question(student_message)
        elif response_type == 'science_question':
            return self._handle_science_question(student_message)
        elif response_type == 'history_question':
            return self._handle_history_question(student_message)
        elif response_type == 'portuguese_question':
            return self._handle_portuguese_question(student_message)
        elif response_type == 'geography_question':
            return self._handle_geography_question(student_message)
        elif response_type == 'general_curiosity':
            return self._handle_general_curiosity(student_message)
        elif response_type == 'needs_encouragement':
            return self._generate_encouragement(student_message)
        elif response_type == 'greeting':
            return self._handle_greeting(student_message)
        else:
            return self._generate_educational_response(student_message)
    
    def _analyze_student_message(self, message):
        """
        Analisa a mensagem do estudante para determinar o tipo de resposta.
        Agora usa o sistema expandido de palavras-chave.
        """
        # Palavras que indicam confusão ou dificuldade
        confusion_words = ['não entendo', 'confuso', 'difícil', 'não sei', 'ajuda', 'perdido', 'complicado']
        
        # Saudações
        greeting_words = ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'tchau', 'obrigado']
        
        # Verifica confusão primeiro
        if any(word in message for word in confusion_words):
            return 'needs_encouragement'
        
        # Verifica saudações
        if any(word in message for word in greeting_words):
            return 'greeting'
        
        # Verifica tópicos educacionais usando as palavras-chave expandidas
        if any(word in message for word in self.topic_keywords['matematica']):
            return 'math_question'
        elif any(word in message for word in self.topic_keywords['ciencias']):
            return 'science_question'
        elif any(word in message for word in self.topic_keywords['historia']):
            return 'history_question'
        elif any(word in message for word in self.topic_keywords['portugues']):
            return 'portuguese_question'
        elif any(word in message for word in self.topic_keywords['geografia']):
            return 'geography_question'
        else:
            return 'general_curiosity'
    
    def _handle_math_question(self, message):
        """
        Responde perguntas sobre matemática de forma didática e amigável.
        """
        encouragement = random.choice(self.encouragement_phrases)
        
        # Detecta o tópico específico de matemática
        if any(word in message for word in ['somar', 'adição', 'mais', 'soma']):
            topic_info = self.educational_knowledge['matematica']['adicao']
        elif any(word in message for word in ['subtrair', 'subtração', 'menos']):
            topic_info = self.educational_knowledge['matematica']['subtracao']
        elif any(word in message for word in ['multiplicar', 'multiplicação', 'vezes', 'tabuada']):
            topic_info = self.educational_knowledge['matematica']['multiplicacao']
        elif any(word in message for word in ['dividir', 'divisão']):
            topic_info = self.educational_knowledge['matematica']['divisao']
        elif any(word in message for word in ['fração', 'metade', 'quarto', 'terço']):
            topic_info = self.educational_knowledge['matematica']['fracao']
        elif any(word in message for word in ['geometria', 'forma', 'círculo', 'quadrado', 'triângulo']):
            topic_info = self.educational_knowledge['matematica']['geometria']
        else:
            # Resposta geral sobre matemática
            return {
                'message': f"{encouragement} A matemática é super divertida! É como um jogo de números! 🔢 Você pode me perguntar sobre somar, subtrair, multiplicar, dividir, frações, formas geométricas... Qual operação ou conceito você quer aprender?",
                'type': 'educational'
            }
        
        response = f"{encouragement}\n\n{topic_info['explanation']}\n\n📚 **Exemplos:**\n"
        for example in topic_info['examples']:
            response += f"• {example}\n"
        response += f"\n💡 **Dica:** {topic_info['tips']}\n\nTem alguma conta específica que você quer que eu te ajude a resolver?"
        
        return {
            'message': response,
            'type': 'educational'
        }
    
    def _handle_science_question(self, message):
        """
        Responde perguntas sobre ciências de forma educativa e divertida.
        """
        encouragement = random.choice(self.encouragement_phrases)
        
        if any(word in message for word in ['animal', 'bicho', 'cachorro', 'gato', 'pássaro', 'mamífero', 'peixe']):
            topic_info = self.educational_knowledge['ciencias']['animais']
        elif any(word in message for word in ['planta', 'árvore', 'flor', 'folha', 'raiz']):
            topic_info = self.educational_knowledge['ciencias']['plantas']
        elif any(word in message for word in ['corpo', 'coração', 'pulmão', 'cérebro', 'sangue']):
            topic_info = self.educational_knowledge['ciencias']['corpo_humano']
        elif any(word in message for word in ['espaço', 'planeta', 'estrela', 'lua', 'sol']):
            topic_info = self.educational_knowledge['ciencias']['espaco']
        elif any(word in message for word in ['água', 'chuva', 'rio', 'oceano', 'gelo', 'vapor']):
            topic_info = self.educational_knowledge['ciencias']['agua']
        elif any(word in message for word in ['dinossauro', 'tiranossauro', 'brontossauro', 'pterodáctilo']):
            topic_info = self.educational_knowledge['ciencias']['dinossauros']
        else:
            return {
                'message': f"{encouragement} A ciência é incrível! Ela nos ajuda a entender o mundo ao nosso redor! 🔬 Posso te contar sobre animais, plantas, o corpo humano, o espaço, a água, dinossauros... Sobre o que você tem curiosidade?",
                'type': 'educational'
            }
        
        response = f"{encouragement}\n\n{topic_info['explanation']}\n\n📚 **Exemplos:**\n"
        for example in topic_info['examples']:
            response += f"• {example}\n"
        response += f"\n💡 **Dica:** {topic_info['tips']}\n\nQue mais você gostaria de saber sobre esse assunto?"
        
        return {
            'message': response,
            'type': 'educational'
        }
    
    def _handle_history_question(self, message):
        """
        Responde perguntas sobre história de forma interessante para crianças.
        """
        encouragement = random.choice(self.encouragement_phrases)
        
        if any(word in message for word in ['brasil', 'brasileiro', 'nosso país', 'indígena', 'português']):
            topic_info = self.educational_knowledge['historia']['brasil']
        elif any(word in message for word in ['descobrimento', 'descoberta', 'explorador', 'cabral', 'colombo']):
            topic_info = self.educational_knowledge['historia']['descobrimentos']
        elif any(word in message for word in ['invenção', 'inventor', 'santos dumont', 'telefone', 'roda']):
            topic_info = self.educational_knowledge['historia']['inventos']
        else:
            return {
                'message': f"{encouragement} A história é como uma coleção de aventuras reais que aconteceram no passado! 📜 Posso te contar sobre o Brasil, grandes descobrimentos, invenções incríveis, pessoas famosas... O que você quer saber?",
                'type': 'educational'
            }
        
        response = f"{encouragement}\n\n{topic_info['explanation']}\n\n📚 **Exemplos:**\n"
        for example in topic_info['examples']:
            response += f"• {example}\n"
        response += f"\n💡 **Dica:** {topic_info['tips']}\n\nQue período da história mais te interessa?"
        
        return {
            'message': response,
            'type': 'educational'
        }
    
    def _handle_portuguese_question(self, message):
        """
        Responde perguntas sobre português de forma didática.
        """
        encouragement = random.choice(self.encouragement_phrases)
        
        if any(word in message for word in ['alfabeto', 'letra', 'abc', 'vogal', 'consoante']):
            topic_info = self.educational_knowledge['portugues']['alfabeto']
        elif any(word in message for word in ['ler', 'leitura', 'livro', 'história', 'conto']):
            topic_info = self.educational_knowledge['portugues']['leitura']
        elif any(word in message for word in ['escrever', 'escrita', 'redação', 'texto', 'carta']):
            topic_info = self.educational_knowledge['portugues']['escrita']
        else:
            return {
                'message': f"{encouragement} O português é nossa língua! É com ela que nos comunicamos e expressamos nossos sentimentos! 📖 Posso te ajudar com o alfabeto, leitura, escrita, gramática... O que você quer aprender?",
                'type': 'educational'
            }
        
        response = f"{encouragement}\n\n{topic_info['explanation']}\n\n📚 **Exemplos:**\n"
        for example in topic_info['examples']:
            response += f"• {example}\n"
        response += f"\n💡 **Dica:** {topic_info['tips']}\n\nCom que parte do português você quer mais ajuda?"
        
        return {
            'message': response,
            'type': 'educational'
        }
    
    def _handle_geography_question(self, message):
        """
        Responde perguntas sobre geografia de forma educativa e interessante.
        """
        encouragement = random.choice(self.encouragement_phrases)
        
        if any(word in message for word in ['brasil', 'brasileiro', 'nosso país', 'região']):
            topic_info = self.educational_knowledge['geografia']['brasil']
        elif any(word in message for word in ['mundo', 'país', 'continente', 'oceano']):
            topic_info = self.educational_knowledge['geografia']['mundo']
        elif any(word in message for word in ['natureza', 'rio', 'montanha', 'floresta']):
            topic_info = self.educational_knowledge['geografia']['natureza']
        else:
            return {
                'message': f"{encouragement} A geografia é fascinante! Ela nos ensina sobre os lugares do mundo, as pessoas e a natureza! 🗺️ Posso te contar sobre o Brasil, outros países, rios, montanhas... O que você quer explorar?",
                'type': 'educational'
            }
        
        response = f"{encouragement}\n\n{topic_info['explanation']}\n\n📚 **Exemplos:**\n"
        for example in topic_info['examples']:
            response += f"• {example}\n"
        response += f"\n💡 **Dica:** {topic_info['tips']}\n\nQue lugar do mundo mais desperta sua curiosidade?"
        
        return {
            'message': response,
            'type': 'educational'
        }
    
    def _handle_general_curiosity(self, message):
        """
        Responde perguntas gerais com curiosidade e incentivo ao aprendizado.
        """
        encouragement = random.choice(self.encouragement_phrases)
        
        # Detecta palavras-chave para dar respostas mais específicas
        if 'por que' in message:
            starter = random.choice(self.common_questions['por que'])
        elif 'como' in message:
            starter = random.choice(self.common_questions['como'])
        elif 'o que é' in message or 'que é' in message:
            starter = random.choice(self.common_questions['o que é'])
        else:
            starter = "Que interessante!"
        
        # Respostas gerais educativas
        general_responses = [
            f"{starter} Essa é uma pergunta muito inteligente! Embora eu não tenha todas as respostas, posso te ajudar a pensar sobre isso. Que tal pesquisarmos juntos? 🤔",
            f"{encouragement} {starter} Adoro quando você faz perguntas assim! Isso mostra que você é muito curioso e quer aprender. Vamos explorar esse assunto! 🔍",
            f"{starter} Você sabe que pode me perguntar sobre matemática, ciências, história, português e muitas outras coisas? Estou aqui para te ajudar a aprender! 📚",
            f"{encouragement} {starter} Que tal me contar mais sobre o que você está pensando? Assim posso te ajudar melhor! 💭"
        ]
        
        return {
            'message': random.choice(general_responses),
            'type': 'educational'
        }
    
    def _handle_greeting(self, message):
        """
        Responde saudações de forma amigável.
        """
        if any(word in message for word in ['tchau', 'até logo', 'bye']):
            farewells = [
                f"Tchau! Foi muito legal conversar com você! Continue sempre curioso e estudando! 👋😊",
                f"Até logo! Lembre-se: nunca pare de fazer perguntas e aprender coisas novas! 🌟",
                f"Tchau, amiguinho! Volte sempre que quiser aprender algo novo! 📚✨"
            ]
            return {
                'message': random.choice(farewells),
                'type': 'farewell'
            }
        elif any(word in message for word in ['obrigado', 'obrigada', 'valeu']):
            thanks_responses = [
                "De nada! Fico muito feliz em poder te ajudar! 😊",
                "Foi um prazer! Estou sempre aqui quando você precisar! 🌟",
                "Que bom que consegui te ajudar! Continue sempre perguntando! 💡"
            ]
            return {
                'message': random.choice(thanks_responses),
                'type': 'thanks'
            }
        else:
            greetings = [
                f"Oi! Que bom te ver de novo! Como posso te ajudar hoje? 😊",
                f"Olá! Estou aqui e pronto para aprender junto com você! O que vamos descobrir hoje? 🎓",
                f"Oi, amiguinho! Que alegria! Sobre o que você quer conversar? 🌟"
            ]
            return {
                'message': random.choice(greetings),
                'type': 'greeting'
            }
    
    def _generate_encouragement(self, message):
        """
        Gera mensagens de encorajamento quando a criança está com dificuldades.
        """
        encouragement = random.choice(self.encouragement_phrases)
        
        supportive_messages = [
            f"{encouragement} Não se preocupe! Todo mundo tem dificuldades às vezes. O importante é não desistir! Vamos tentar de um jeito diferente? 💪",
            f"Ei, não fique triste! Aprender é como andar de bicicleta - no começo é difícil, mas depois fica fácil! Vou te ajudar passo a passo! 🚲",
            f"{encouragement} Você é muito inteligente! Às vezes as coisas parecem difíceis, mas com paciência e prática, você consegue! Vamos juntos? 🌈",
            f"Que bom que você me contou que está com dificuldade! Isso mostra que você quer aprender. Vou te explicar de um jeito mais fácil! 🤗"
        ]
        
        return {
            'message': random.choice(supportive_messages),
            'type': 'encouragement'
        }
    
    def _generate_educational_response(self, message):
        """
        Gera uma resposta educativa geral quando não há padrão específico.
        """
        encouragement = random.choice(self.encouragement_phrases)
        
        educational_responses = [
            f"{encouragement} Essa é uma pergunta muito boa! Embora eu não tenha uma resposta específica agora, posso te ajudar a pesquisar sobre isso. Que tal me contar mais detalhes? 🔍",
            f"Que interessante! Você me fez pensar em algo novo! Posso te ajudar com matemática, ciências, história, português... Qual dessas matérias te interessa mais? 📚",
            f"{encouragement} Adoro sua curiosidade! Isso é o que faz as pessoas aprenderem coisas incríveis! Me conte mais sobre o que você está pensando! 💭",
            f"Você sabe que pode me perguntar qualquer coisa sobre os estudos? Estou aqui para te ajudar a entender melhor o mundo! O que mais você quer saber? 🌍"
        ]
        
        return {
            'message': random.choice(educational_responses),
            'type': 'educational'
        }
    
    def should_provide_hint(self, conversation_history):
        """
        Determina se é hora de oferecer uma dica baseado no histórico da conversa.
        """
        if len(conversation_history) < 3:
            return False
        
        # Verifica se a criança está com dificuldades
        recent_messages = conversation_history[-3:]
        confusion_count = sum(1 for msg in recent_messages 
                            if msg.get('sender') == 'student' and 
                            any(word in msg.get('message', '').lower() 
                                for word in ['não sei', 'difícil', 'confuso', 'não entendo']))
        
        return confusion_count >= 2
    
    def generate_summary(self, conversation_history):
        """
        Gera um resumo da conversa para análise posterior.
        """
        student_messages = [msg for msg in conversation_history if msg.get('sender') == 'student']
        tutor_messages = [msg for msg in conversation_history if msg.get('sender') == 'tutor']
        
        # Analisa os tópicos discutidos
        topics_discussed = []
        for msg in student_messages:
            message_text = msg.get('message', '').lower()
            if any(word in message_text for word in ['matemática', 'conta', 'número']):
                topics_discussed.append('matemática')
            elif any(word in message_text for word in ['ciência', 'animal', 'planta']):
                topics_discussed.append('ciências')
            elif any(word in message_text for word in ['história', 'brasil']):
                topics_discussed.append('história')
            elif any(word in message_text for word in ['português', 'palavra', 'letra']):
                topics_discussed.append('português')
        
        return {
            'total_messages': len(conversation_history),
            'student_messages': len(student_messages),
            'tutor_messages': len(tutor_messages),
            'topics_discussed': list(set(topics_discussed)),
            'encouragements_given': len([msg for msg in tutor_messages if msg.get('type') == 'encouragement']),
            'educational_responses': len([msg for msg in tutor_messages if msg.get('type') == 'educational']),
            'engagement_level': 'high' if len(student_messages) > 5 else 'medium' if len(student_messages) > 2 else 'low',
            'learning_areas_covered': len(set(topics_discussed))
        }

