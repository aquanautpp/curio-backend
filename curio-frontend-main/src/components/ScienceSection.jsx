import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Input } from '@/components/ui/input.jsx'
import {
  Microscope,
  Leaf,
  Globe,
  Zap,
  Play,
  CheckCircle,
  XCircle,
  Lightbulb,
  Trophy,
  Star,
  Brain,
  RefreshCw,
  BookOpen,
  Search,
  Atom,
  Heart,
  Rocket
} from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const ScienceSection = () => {
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('topics')
  const [currentActivity, setCurrentActivity] = useState(null)
  const [userAnswer, setUserAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [progress, setProgress] = useState({
    biology: 20,
    physics: 15,
    chemistry: 10,
    earth_science: 25,
    overall: 18
  })
  
  const [scienceTopics, setScienceTopics] = useState([])
  const [experiments, setExperiments] = useState([])
  const [achievements, setAchievements] = useState([])

  useEffect(() => {
    loadScienceData()
  }, [])

  const loadScienceData = async () => {
    setLoading(true)
    try {
      // Simula carregamento de dados
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      setScienceTopics(createDefaultScienceTopics())
      setExperiments(createDefaultExperiments())
      generateScienceAchievements()
      
    } catch (error) {
      console.error('Erro ao carregar dados de ciências:', error)
    } finally {
      setLoading(false)
    }
  }

  const createDefaultScienceTopics = () => [
    {
      id: 1,
      title: "Reino Animal",
      category: "biology",
      difficulty: "easy",
      description: "Explore a diversidade dos animais e suas características",
      content: "Os animais são seres vivos que se movem, respiram e se alimentam. Eles podem ser mamíferos, aves, peixes, répteis ou anfíbios.",
      visual_aid: "🐕🐱🐦🐠🦎🐸",
      questions: [
        {
          question: "Qual animal é um mamífero?",
          options: ["Peixe", "Cachorro", "Pássaro", "Cobra"],
          correct: 1,
          explanation: "O cachorro é um mamífero porque tem pelos, é de sangue quente e alimenta os filhotes com leite."
        }
      ],
      completed: false,
      points: 15
    },
    {
      id: 2,
      title: "Sistema Solar",
      category: "earth_science",
      difficulty: "intermediate",
      description: "Descubra os planetas e estrelas do nosso sistema solar",
      content: "O Sistema Solar é formado pelo Sol e todos os corpos celestes que orbitam ao seu redor, incluindo 8 planetas.",
      visual_aid: "☀️🌍🪐⭐",
      questions: [
        {
          question: "Quantos planetas existem no Sistema Solar?",
          options: ["7", "8", "9", "10"],
          correct: 1,
          explanation: "Existem 8 planetas no Sistema Solar: Mercúrio, Vênus, Terra, Marte, Júpiter, Saturno, Urano e Netuno."
        }
      ],
      completed: false,
      points: 20
    },
    {
      id: 3,
      title: "Estados da Matéria",
      category: "physics",
      difficulty: "easy",
      description: "Aprenda sobre sólido, líquido e gasoso",
      content: "A matéria pode existir em três estados principais: sólido (como gelo), líquido (como água) e gasoso (como vapor).",
      visual_aid: "🧊💧☁️",
      questions: [
        {
          question: "O que acontece com a água quando ela congela?",
          options: ["Vira vapor", "Vira gelo", "Desaparece", "Fica quente"],
          correct: 1,
          explanation: "Quando a água congela, ela muda do estado líquido para o estado sólido, virando gelo."
        }
      ],
      completed: false,
      points: 15
    },
    {
      id: 4,
      title: "Corpo Humano",
      category: "biology",
      difficulty: "intermediate",
      description: "Conheça os sistemas do nosso corpo",
      content: "O corpo humano é formado por vários sistemas que trabalham juntos: respiratório, circulatório, digestivo, nervoso e outros.",
      visual_aid: "🫁❤️🧠🦴",
      questions: [
        {
          question: "Qual órgão bombeia o sangue pelo corpo?",
          options: ["Pulmão", "Coração", "Estômago", "Cérebro"],
          correct: 1,
          explanation: "O coração é o órgão responsável por bombear o sangue para todo o corpo através dos vasos sanguíneos."
        }
      ],
      completed: false,
      points: 20
    },
    {
      id: 5,
      title: "Plantas e Fotossíntese",
      category: "biology",
      difficulty: "intermediate",
      description: "Como as plantas produzem seu próprio alimento",
      content: "As plantas fazem fotossíntese, usando luz solar, água e gás carbônico para produzir açúcar e oxigênio.",
      visual_aid: "🌱☀️💧🍃",
      questions: [
        {
          question: "O que as plantas precisam para fazer fotossíntese?",
          options: ["Só água", "Luz solar, água e gás carbônico", "Só luz solar", "Só gás carbônico"],
          correct: 1,
          explanation: "Para fazer fotossíntese, as plantas precisam de luz solar, água e gás carbônico do ar."
        }
      ],
      completed: false,
      points: 25
    }
  ]

  const createDefaultExperiments = () => [
    {
      id: 1,
      title: "Vulcão de Bicarbonato",
      category: "chemistry",
      difficulty: "easy",
      description: "Crie uma erupção vulcânica segura em casa",
      materials: ["Bicarbonato de sódio", "Vinagre", "Corante alimentar", "Detergente", "Garrafa pequena"],
      steps: [
        "Coloque 2 colheres de bicarbonato na garrafa",
        "Adicione algumas gotas de corante e detergente",
        "Despeje o vinagre rapidamente",
        "Observe a 'erupção'!"
      ],
      explanation: "A reação entre bicarbonato (base) e vinagre (ácido) produz gás carbônico, criando espuma.",
      safety_tips: ["Use óculos de proteção", "Faça em local ventilado", "Peça ajuda de um adulto"],
      completed: false,
      points: 30
    },
    {
      id: 2,
      title: "Jardim de Cristais",
      category: "chemistry",
      difficulty: "intermediate",
      description: "Cultive cristais coloridos",
      materials: ["Sal", "Água quente", "Barbante", "Corante", "Pote de vidro"],
      steps: [
        "Dissolva bastante sal em água quente",
        "Adicione corante à solução",
        "Amarre o barbante e mergulhe na solução",
        "Aguarde alguns dias para os cristais crescerem"
      ],
      explanation: "Quando a água evapora, o sal se cristaliza ao redor do barbante, formando cristais.",
      safety_tips: ["Cuidado com água quente", "Não beba a solução"],
      completed: false,
      points: 35
    },
    {
      id: 3,
      title: "Densidade dos Líquidos",
      category: "physics",
      difficulty: "easy",
      description: "Crie uma torre de líquidos coloridos",
      materials: ["Mel", "Óleo", "Água com corante", "Álcool", "Copo transparente"],
      steps: [
        "Despeje o mel no fundo do copo",
        "Adicione cuidadosamente a água colorida",
        "Despeje o óleo devagar",
        "Por último, adicione o álcool"
      ],
      explanation: "Líquidos com densidades diferentes não se misturam e formam camadas.",
      safety_tips: ["Despeje devagar", "Use álcool com supervisão"],
      completed: false,
      points: 25
    }
  ]

  const generateScienceAchievements = () => {
    const newAchievements = [
      {
        id: 1,
        title: "Primeiro Cientista",
        description: "Completou sua primeira atividade de ciências",
        icon: Microscope,
        color: "text-green-500",
        earned: progress.overall > 0,
        requirement: "Completar 1 atividade"
      },
      {
        id: 2,
        title: "Biólogo Junior",
        description: "Explorou o mundo dos seres vivos",
        icon: Leaf,
        color: "text-green-600",
        earned: progress.biology >= 30,
        requirement: "30% de progresso em Biologia"
      },
      {
        id: 3,
        title: "Físico Curioso",
        description: "Descobriu os segredos da física",
        icon: Zap,
        color: "text-blue-500",
        earned: progress.physics >= 30,
        requirement: "30% de progresso em Física"
      },
      {
        id: 4,
        title: "Químico Experimental",
        description: "Realizou experimentos químicos",
        icon: Atom,
        color: "text-purple-500",
        earned: progress.chemistry >= 30,
        requirement: "30% de progresso em Química"
      },
      {
        id: 5,
        title: "Explorador da Terra",
        description: "Conheceu nosso planeta e o espaço",
        icon: Globe,
        color: "text-blue-600",
        earned: progress.earth_science >= 40,
        requirement: "40% de progresso em Ciências da Terra"
      }
    ]
    setAchievements(newAchievements)
  }

  const startActivity = (topic) => {
    setCurrentActivity(topic)
    setUserAnswer('')
    setFeedback(null)
  }

  const submitAnswer = (questionIndex, selectedOption) => {
    const question = currentActivity.questions[questionIndex]
    const isCorrect = selectedOption === question.correct
    
    setFeedback({
      is_correct: isCorrect,
      message: isCorrect ? "🎉 Parabéns! Resposta correta!" : "🤔 Não foi dessa vez. Tente novamente!",
      explanation: question.explanation
    })
    
    if (isCorrect) {
      updateProgress(currentActivity.category, currentActivity.points)
    }
  }

  const updateProgress = (category, points) => {
    setProgress(prev => {
      const newProgress = { ...prev }
      newProgress[category] = Math.min(newProgress[category] + 5, 100)
      newProgress.overall = Math.round(
        (newProgress.biology + newProgress.physics + newProgress.chemistry + newProgress.earth_science) / 4
      )
      return newProgress
    })
    
    setTimeout(() => generateScienceAchievements(), 500)
  }

  const getCategoryIcon = (category) => {
    const icons = {
      biology: Leaf,
      physics: Zap,
      chemistry: Atom,
      earth_science: Globe
    }
    return icons[category] || Microscope
  }

  const getCategoryName = (category) => {
    const names = {
      biology: "Biologia",
      physics: "Física", 
      chemistry: "Química",
      earth_science: "Ciências da Terra"
    }
    return names[category] || category
  }

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: 'bg-green-100 text-green-800',
      intermediate: 'bg-yellow-100 text-yellow-800',
      hard: 'bg-red-100 text-red-800'
    }
    return colors[difficulty] || colors.easy
  }

  if (loading && !currentActivity) {
    return (
      <div className="space-y-6">
        <div className="text-center py-12">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4" />
          <p>Carregando atividades de ciências...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Microscope className="w-8 h-8 text-green-500" />
            Ciências
          </h1>
          <p className="text-gray-600 mt-1">
            Explore o mundo através da ciência
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <Badge variant="outline">
            Progresso Geral: {progress.overall}%
          </Badge>
          <Button onClick={loadScienceData} variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
        </div>
      </div>

      {/* Progress Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              <Leaf className="w-4 h-4" />
              Biologia
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold mb-2">{progress.biology}%</div>
            <Progress value={progress.biology} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              <Zap className="w-4 h-4" />
              Física
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold mb-2">{progress.physics}%</div>
            <Progress value={progress.physics} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              <Atom className="w-4 h-4" />
              Química
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold mb-2">{progress.chemistry}%</div>
            <Progress value={progress.chemistry} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              <Globe className="w-4 h-4" />
              Terra/Espaço
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold mb-2">{progress.earth_science}%</div>
            <Progress value={progress.earth_science} />
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="topics">Tópicos</TabsTrigger>
          <TabsTrigger value="experiments">Experimentos</TabsTrigger>
          <TabsTrigger value="achievements">Conquistas</TabsTrigger>
        </TabsList>

        {/* Tópicos */}
        <TabsContent value="topics" className="space-y-6">
          {currentActivity ? (
            <Card>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      {React.createElement(getCategoryIcon(currentActivity.category), { className: "w-5 h-5" })}
                      {currentActivity.title}
                    </CardTitle>
                    <CardDescription>{currentActivity.description}</CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Badge className={getDifficultyColor(currentActivity.difficulty)}>
                      {currentActivity.difficulty}
                    </Badge>
                    <Badge variant="outline">
                      {currentActivity.points} pts
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="p-4 bg-green-50 rounded-lg">
                  <h4 className="font-medium mb-2">Conteúdo:</h4>
                  <p className="text-gray-700 mb-3">{currentActivity.content}</p>
                  {currentActivity.visual_aid && (
                    <div className="text-3xl text-center">
                      {currentActivity.visual_aid}
                    </div>
                  )}
                </div>

                {currentActivity.questions.map((question, index) => (
                  <div key={index} className="p-4 border rounded-lg">
                    <h4 className="font-medium mb-3">{question.question}</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {question.options.map((option, optionIndex) => (
                        <Button
                          key={optionIndex}
                          variant="outline"
                          className="justify-start h-auto p-3"
                          onClick={() => submitAnswer(index, optionIndex)}
                        >
                          {option}
                        </Button>
                      ))}
                    </div>
                  </div>
                ))}

                <div className="flex gap-2">
                  <Button variant="outline" onClick={() => setCurrentActivity(null)}>
                    Voltar aos Tópicos
                  </Button>
                </div>

                {feedback && (
                  <Alert className={feedback.is_correct ? "border-green-200 bg-green-50" : "border-yellow-200 bg-yellow-50"}>
                    <div className="flex items-start gap-2">
                      {feedback.is_correct ? (
                        <CheckCircle className="w-4 h-4 text-green-600 mt-0.5" />
                      ) : (
                        <XCircle className="w-4 h-4 text-yellow-600 mt-0.5" />
                      )}
                      <div>
                        <p className="font-medium">{feedback.message}</p>
                        <p className="text-sm mt-1">{feedback.explanation}</p>
                      </div>
                    </div>
                  </Alert>
                )}
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {scienceTopics.map((topic) => {
                const IconComponent = getCategoryIcon(topic.category)
                return (
                  <Card key={topic.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <CardTitle className="text-lg flex items-center gap-2">
                          <IconComponent className="w-5 h-5" />
                          {topic.title}
                        </CardTitle>
                        <div className="flex gap-1">
                          <Badge className={getDifficultyColor(topic.difficulty)}>
                            {topic.difficulty}
                          </Badge>
                          {topic.completed && (
                            <CheckCircle className="w-4 h-4 text-green-500" />
                          )}
                        </div>
                      </div>
                      <CardDescription>{topic.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-500">
                            {getCategoryName(topic.category)}
                          </span>
                          <span className="text-gray-500">
                            {topic.points} pontos
                          </span>
                        </div>
                        <Button 
                          onClick={() => startActivity(topic)} 
                          className="w-full"
                          variant={topic.completed ? "outline" : "default"}
                        >
                          <Play className="w-4 h-4 mr-2" />
                          {topic.completed ? "Revisar" : "Estudar"}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          )}
        </TabsContent>

        {/* Experimentos */}
        <TabsContent value="experiments" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {experiments.map((experiment) => {
              const IconComponent = getCategoryIcon(experiment.category)
              return (
                <Card key={experiment.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-lg flex items-center gap-2">
                        <IconComponent className="w-5 h-5" />
                        {experiment.title}
                      </CardTitle>
                      <div className="flex gap-2">
                        <Badge className={getDifficultyColor(experiment.difficulty)}>
                          {experiment.difficulty}
                        </Badge>
                        <Badge variant="outline">
                          {experiment.points} pts
                        </Badge>
                      </div>
                    </div>
                    <CardDescription>{experiment.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <h4 className="font-medium mb-2">Materiais:</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {experiment.materials.map((material, index) => (
                          <li key={index}>• {material}</li>
                        ))}
                      </ul>
                    </div>
                    
                    <div>
                      <h4 className="font-medium mb-2">Passos:</h4>
                      <ol className="text-sm text-gray-600 space-y-1">
                        {experiment.steps.map((step, index) => (
                          <li key={index}>{index + 1}. {step}</li>
                        ))}
                      </ol>
                    </div>

                    <Alert>
                      <Lightbulb className="h-4 w-4" />
                      <AlertDescription>
                        <strong>Por que funciona:</strong> {experiment.explanation}
                      </AlertDescription>
                    </Alert>

                    <Alert variant="destructive">
                      <AlertDescription>
                        <strong>Segurança:</strong> {experiment.safety_tips.join(', ')}
                      </AlertDescription>
                    </Alert>

                    <Button className="w-full">
                      <CheckCircle className="w-4 h-4 mr-2" />
                      Marcar como Realizado
                    </Button>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>

        {/* Conquistas */}
        <TabsContent value="achievements" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {achievements.map((achievement) => {
              const IconComponent = achievement.icon
              return (
                <Card key={achievement.id} className={achievement.earned ? "border-green-200 bg-green-50" : ""}>
                  <CardHeader>
                    <div className="flex items-center gap-3">
                      <IconComponent 
                        className={`w-8 h-8 ${achievement.earned ? achievement.color : 'text-gray-400'}`} 
                      />
                      <div>
                        <CardTitle className={achievement.earned ? "text-gray-900" : "text-gray-500"}>
                          {achievement.title}
                        </CardTitle>
                        <CardDescription>{achievement.description}</CardDescription>
                      </div>
                      {achievement.earned && (
                        <CheckCircle className="w-6 h-6 text-green-500 ml-auto" />
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600">
                      Requisito: {achievement.requirement}
                    </p>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ScienceSection

