import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import {
  Calculator,
  BookOpen,
  Play,
  CheckCircle,
  XCircle,
  Lightbulb,
  Trophy,
  Clock,
  Target,
  Brain,
  Zap,
  RefreshCw,
  ArrowRight,
  Star,
  Award
} from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const MathematicsSection = () => {
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('singapore')
  const [currentExercise, setCurrentExercise] = useState(null)
  const [userAnswer, setUserAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [progress, setProgress] = useState({
    concrete: 25,
    pictorial: 15,
    abstract: 5,
    overall: 15
  })
  
  // Estados para diferentes tipos de exercícios
  const [singaporeExercises, setSingaporeExercises] = useState([])
  const [practiceProblems, setPracticeProblems] = useState([])
  const [achievements, setAchievements] = useState([])

  useEffect(() => {
    loadMathematicsData()
  }, [])

  const loadMathematicsData = async () => {
    setLoading(true)
    try {
      // Carrega dados de matemática
      const [exercisesRes, problemsRes, progressRes] = await Promise.allSettled([
        fetch(`${API_BASE_URL}/content/mathematics/singapore`),
        fetch(`${API_BASE_URL}/content/mathematics/problems`),
        fetch(`${API_BASE_URL}/students/1/progress/mathematics`)
      ])

      // Processa exercícios do método de Singapura
      if (exercisesRes.status === 'fulfilled' && exercisesRes.value.ok) {
        const data = await exercisesRes.value.json()
        setSingaporeExercises(data.exercises || createDefaultSingaporeExercises())
      } else {
        setSingaporeExercises(createDefaultSingaporeExercises())
      }

      // Processa problemas de prática
      if (problemsRes.status === 'fulfilled' && problemsRes.value.ok) {
        const data = await problemsRes.value.json()
        setPracticeProblems(data.problems || createDefaultPracticeProblems())
      } else {
        setPracticeProblems(createDefaultPracticeProblems())
      }

      // Processa progresso
      if (progressRes.status === 'fulfilled' && progressRes.value.ok) {
        const data = await progressRes.value.json()
        setProgress(data.progress || progress)
      }

      generateMathAchievements()

    } catch (error) {
      console.error('Erro ao carregar dados de matemática:', error)
    } finally {
      setLoading(false)
    }
  }

  const createDefaultSingaporeExercises = () => [
    {
      id: 1,
      title: "Adição com Objetos Concretos",
      phase: "concrete",
      difficulty: "easy",
      description: "Use blocos ou objetos para somar números",
      problem: "Maria tem 3 maçãs. João deu mais 2 maçãs para ela. Quantas maçãs Maria tem agora?",
      visual_aid: "🍎🍎🍎 + 🍎🍎 = ?",
      correct_answer: "5",
      hints: [
        "Conte as maçãs de Maria primeiro",
        "Depois conte as maçãs que João deu",
        "Junte todas as maçãs e conte o total"
      ],
      completed: false
    },
    {
      id: 2,
      title: "Subtração com Desenhos",
      phase: "pictorial",
      difficulty: "easy",
      description: "Use desenhos para resolver problemas de subtração",
      problem: "Havia 8 pássaros no galho. 3 voaram. Quantos pássaros ficaram?",
      visual_aid: "🐦🐦🐦🐦🐦🐦🐦🐦 - 🐦🐦🐦 = ?",
      correct_answer: "5",
      hints: [
        "Desenhe 8 pássaros",
        "Risque 3 pássaros que voaram",
        "Conte quantos sobraram"
      ],
      completed: false
    },
    {
      id: 3,
      title: "Multiplicação Abstrata",
      phase: "abstract",
      difficulty: "intermediate",
      description: "Resolva multiplicação usando números",
      problem: "Se cada caixa tem 4 lápis e você tem 3 caixas, quantos lápis você tem no total?",
      visual_aid: "3 × 4 = ?",
      correct_answer: "12",
      hints: [
        "Multiplique o número de caixas pelo número de lápis por caixa",
        "3 × 4 significa 4 + 4 + 4",
        "Ou pense: 3 grupos de 4"
      ],
      completed: false
    }
  ]

  const createDefaultPracticeProblems = () => [
    {
      id: 1,
      title: "Problema dos Doces",
      difficulty: "easy",
      category: "word_problem",
      problem: "Ana comprou 15 doces. Ela deu 6 doces para seus amigos. Quantos doces sobraram para Ana?",
      correct_answer: "9",
      explanation: "15 - 6 = 9 doces sobraram para Ana",
      points: 10
    },
    {
      id: 2,
      title: "Desafio das Frutas",
      difficulty: "intermediate",
      category: "word_problem",
      problem: "Em uma fruteira há 24 maçãs. Se elas forem divididas igualmente em 6 cestas, quantas maçãs terá cada cesta?",
      correct_answer: "4",
      explanation: "24 ÷ 6 = 4 maçãs por cesta",
      points: 15
    },
    {
      id: 3,
      title: "Problema do Tempo",
      difficulty: "hard",
      category: "logic",
      problem: "Se um relógio atrasa 2 minutos a cada hora, quanto tempo ele atrasará em 6 horas?",
      correct_answer: "12",
      explanation: "2 minutos × 6 horas = 12 minutos de atraso",
      points: 20
    }
  ]

  const generateMathAchievements = () => {
    const newAchievements = [
      {
        id: 1,
        title: "Primeiro Passo",
        description: "Completou seu primeiro exercício de matemática",
        icon: Play,
        color: "text-green-500",
        earned: progress.overall > 0,
        requirement: "Completar 1 exercício"
      },
      {
        id: 2,
        title: "Explorador Concreto",
        description: "Dominou a fase concreta do método de Singapura",
        icon: Trophy,
        color: "text-blue-500",
        earned: progress.concrete >= 50,
        requirement: "50% de progresso na fase concreta"
      },
      {
        id: 3,
        title: "Artista Pictórico",
        description: "Excelente uso de representações visuais",
        icon: Star,
        color: "text-purple-500",
        earned: progress.pictorial >= 50,
        requirement: "50% de progresso na fase pictórica"
      },
      {
        id: 4,
        title: "Mestre Abstrato",
        description: "Dominou cálculos abstratos",
        icon: Brain,
        color: "text-yellow-500",
        earned: progress.abstract >= 50,
        requirement: "50% de progresso na fase abstrata"
      }
    ]
    setAchievements(newAchievements)
  }

  const startExercise = (exercise) => {
    setCurrentExercise(exercise)
    setUserAnswer('')
    setFeedback(null)
  }

  const submitAnswer = async () => {
    if (!userAnswer.trim()) return

    setLoading(true)
    
    try {
      const response = await fetch(`${API_BASE_URL}/content/mathematics/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          exercise_id: currentExercise.id,
          answer: userAnswer.trim(),
          student_id: 1
        })
      })

      if (response.ok) {
        const result = await response.json()
        setFeedback(result)
        
        // Atualiza progresso se correto
        if (result.is_correct) {
          updateProgress(currentExercise.phase)
        }
      } else {
        // Avaliação local se API não disponível
        const isCorrect = userAnswer.trim().toLowerCase() === currentExercise.correct_answer.toLowerCase()
        setFeedback({
          is_correct: isCorrect,
          message: isCorrect 
            ? "🎉 Parabéns! Resposta correta!" 
            : "🤔 Não foi dessa vez. Tente novamente!",
          explanation: isCorrect ? "Excelente raciocínio!" : "Dica: " + currentExercise.hints[0]
        })
        
        if (isCorrect) {
          updateProgress(currentExercise.phase)
        }
      }
    } catch (error) {
      console.error('Erro ao submeter resposta:', error)
      // Fallback para avaliação local
      const isCorrect = userAnswer.trim().toLowerCase() === currentExercise.correct_answer.toLowerCase()
      setFeedback({
        is_correct: isCorrect,
        message: isCorrect 
          ? "🎉 Parabéns! Resposta correta!" 
          : "🤔 Não foi dessa vez. Tente novamente!",
        explanation: isCorrect ? "Excelente raciocínio!" : "Dica: " + currentExercise.hints[0]
      })
    } finally {
      setLoading(false)
    }
  }

  const updateProgress = (phase) => {
    setProgress(prev => {
      const newProgress = { ...prev }
      newProgress[phase] = Math.min(newProgress[phase] + 10, 100)
      newProgress.overall = Math.round((newProgress.concrete + newProgress.pictorial + newProgress.abstract) / 3)
      return newProgress
    })
    
    // Regenera conquistas
    setTimeout(() => generateMathAchievements(), 500)
  }

  const getHint = () => {
    if (currentExercise && currentExercise.hints.length > 0) {
      const randomHint = currentExercise.hints[Math.floor(Math.random() * currentExercise.hints.length)]
      setFeedback({
        is_hint: true,
        message: "💡 Dica",
        explanation: randomHint
      })
    }
  }

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: 'bg-green-100 text-green-800',
      intermediate: 'bg-yellow-100 text-yellow-800',
      hard: 'bg-red-100 text-red-800'
    }
    return colors[difficulty] || colors.easy
  }

  const getPhaseIcon = (phase) => {
    const icons = {
      concrete: Calculator,
      pictorial: BookOpen,
      abstract: Brain
    }
    return icons[phase] || Calculator
  }

  if (loading && !currentExercise) {
    return (
      <div className="space-y-6">
        <div className="text-center py-12">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4" />
          <p>Carregando exercícios de matemática...</p>
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
            <Calculator className="w-8 h-8 text-blue-500" />
            Matemática
          </h1>
          <p className="text-gray-600 mt-1">
            Aprenda matemática com o Método de Singapura
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <Badge variant="outline">
            Progresso Geral: {progress.overall}%
          </Badge>
          <Button onClick={loadMathematicsData} variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
        </div>
      </div>

      {/* Progress Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              <Calculator className="w-4 h-4" />
              Concreto
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold mb-2">{progress.concrete}%</div>
            <Progress value={progress.concrete} />
            <p className="text-xs text-gray-500 mt-1">Manipulação de objetos</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              <BookOpen className="w-4 h-4" />
              Pictórico
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold mb-2">{progress.pictorial}%</div>
            <Progress value={progress.pictorial} />
            <p className="text-xs text-gray-500 mt-1">Representações visuais</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              <Brain className="w-4 h-4" />
              Abstrato
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold mb-2">{progress.abstract}%</div>
            <Progress value={progress.abstract} />
            <p className="text-xs text-gray-500 mt-1">Símbolos e números</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="singapore">Método Singapura</TabsTrigger>
          <TabsTrigger value="practice">Prática</TabsTrigger>
          <TabsTrigger value="achievements">Conquistas</TabsTrigger>
        </TabsList>

        {/* Método de Singapura */}
        <TabsContent value="singapore" className="space-y-6">
          {currentExercise ? (
            <Card>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      {React.createElement(getPhaseIcon(currentExercise.phase), { className: "w-5 h-5" })}
                      {currentExercise.title}
                    </CardTitle>
                    <CardDescription>{currentExercise.description}</CardDescription>
                  </div>
                  <Badge className={getDifficultyColor(currentExercise.difficulty)}>
                    {currentExercise.difficulty}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h4 className="font-medium mb-2">Problema:</h4>
                  <p className="text-gray-700">{currentExercise.problem}</p>
                  {currentExercise.visual_aid && (
                    <div className="mt-3 text-2xl text-center">
                      {currentExercise.visual_aid}
                    </div>
                  )}
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Sua resposta:</label>
                  <Input
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="Digite sua resposta..."
                    disabled={loading}
                  />
                </div>

                <div className="flex gap-2">
                  <Button onClick={submitAnswer} disabled={loading || !userAnswer.trim()}>
                    {loading ? (
                      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <CheckCircle className="w-4 h-4 mr-2" />
                    )}
                    Verificar Resposta
                  </Button>
                  <Button variant="outline" onClick={getHint}>
                    <Lightbulb className="w-4 h-4 mr-2" />
                    Dica
                  </Button>
                  <Button variant="outline" onClick={() => setCurrentExercise(null)}>
                    Voltar
                  </Button>
                </div>

                {feedback && (
                  <Alert className={feedback.is_correct ? "border-green-200 bg-green-50" : feedback.is_hint ? "border-blue-200 bg-blue-50" : "border-yellow-200 bg-yellow-50"}>
                    <div className="flex items-start gap-2">
                      {feedback.is_correct ? (
                        <CheckCircle className="w-4 h-4 text-green-600 mt-0.5" />
                      ) : feedback.is_hint ? (
                        <Lightbulb className="w-4 h-4 text-blue-600 mt-0.5" />
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
              {singaporeExercises.map((exercise) => {
                const IconComponent = getPhaseIcon(exercise.phase)
                return (
                  <Card key={exercise.id} className="hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <CardTitle className="text-lg flex items-center gap-2">
                          <IconComponent className="w-5 h-5" />
                          {exercise.title}
                        </CardTitle>
                        <Badge className={getDifficultyColor(exercise.difficulty)}>
                          {exercise.difficulty}
                        </Badge>
                      </div>
                      <CardDescription>{exercise.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-500">Fase: {exercise.phase}</span>
                          {exercise.completed && (
                            <CheckCircle className="w-4 h-4 text-green-500" />
                          )}
                        </div>
                        <Button 
                          onClick={() => startExercise(exercise)} 
                          className="w-full"
                          variant={exercise.completed ? "outline" : "default"}
                        >
                          <Play className="w-4 h-4 mr-2" />
                          {exercise.completed ? "Revisar" : "Começar"}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          )}
        </TabsContent>

        {/* Prática */}
        <TabsContent value="practice" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {practiceProblems.map((problem) => (
              <Card key={problem.id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-lg">{problem.title}</CardTitle>
                    <div className="flex items-center gap-2">
                      <Badge className={getDifficultyColor(problem.difficulty)}>
                        {problem.difficulty}
                      </Badge>
                      <Badge variant="outline">
                        {problem.points} pts
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 mb-4">{problem.problem}</p>
                  <Button onClick={() => startExercise(problem)} className="w-full">
                    <Target className="w-4 h-4 mr-2" />
                    Resolver Problema
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Conquistas */}
        <TabsContent value="achievements" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {achievements.map((achievement) => {
              const IconComponent = achievement.icon
              return (
                <Card key={achievement.id} className={achievement.earned ? "border-yellow-200 bg-yellow-50" : ""}>
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

export default MathematicsSection

