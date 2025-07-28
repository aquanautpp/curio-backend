import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Skeleton } from '@/components/ui/skeleton.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import {
  BookOpen,
  Trophy,
  Clock,
  TrendingUp,
  Play,
  CheckCircle,
  Star,
  Brain,
  Target,
  Users,
  Calendar,
  Award,
  Zap,
  RefreshCw,
  AlertCircle
} from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const DashboardFunctional = () => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [refreshing, setRefreshing] = useState(false)
  
  // Estados dos dados
  const [studentData, setStudentData] = useState(null)
  const [progressData, setProgressData] = useState(null)
  const [recentActivities, setRecentActivities] = useState([])
  const [achievements, setAchievements] = useState([])
  const [todayProblem, setTodayProblem] = useState(null)
  const [chatSessions, setChatSessions] = useState([])

  // Carrega dados iniciais
  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      // Carrega dados em paralelo para melhor performance
      const [
        studentResponse,
        progressResponse,
        problemResponse,
        activitiesResponse
      ] = await Promise.allSettled([
        fetch(`${API_BASE_URL}/students/1`),
        fetch(`${API_BASE_URL}/students/1/progress`),
        fetch(`${API_BASE_URL}/problems/today`),
        fetch(`${API_BASE_URL}/students/1/activities`)
      ])

      // Processa dados do estudante
      if (studentResponse.status === 'fulfilled' && studentResponse.value.ok) {
        const studentData = await studentResponse.value.json()
        setStudentData(studentData.student || createDefaultStudent())
      } else {
        setStudentData(createDefaultStudent())
      }

      // Processa dados de progresso
      if (progressResponse.status === 'fulfilled' && progressResponse.value.ok) {
        const progressData = await progressResponse.value.json()
        setProgressData(progressData.progress || createDefaultProgress())
      } else {
        setProgressData(createDefaultProgress())
      }

      // Processa problema do dia
      if (problemResponse.status === 'fulfilled' && problemResponse.value.ok) {
        const problemData = await problemResponse.value.json()
        setTodayProblem(problemData.problem)
      }

      // Processa atividades recentes
      if (activitiesResponse.status === 'fulfilled' && activitiesResponse.value.ok) {
        const activitiesData = await activitiesResponse.value.json()
        setRecentActivities(activitiesData.activities || createDefaultActivities())
      } else {
        setRecentActivities(createDefaultActivities())
      }

      // Gera conquistas baseadas nos dados
      generateAchievements()

    } catch (err) {
      console.error('Erro ao carregar dashboard:', err)
      setError('Erro ao carregar dados do dashboard')
      
      // Usa dados padrão em caso de erro
      setStudentData(createDefaultStudent())
      setProgressData(createDefaultProgress())
      setRecentActivities(createDefaultActivities())
    } finally {
      setLoading(false)
    }
  }

  const refreshDashboard = async () => {
    setRefreshing(true)
    await loadDashboardData()
    setRefreshing(false)
  }

  const createDefaultStudent = () => ({
    id: 1,
    name: "Estudante Curió",
    grade: "Ensino Fundamental",
    avatar: null,
    joined_date: new Date().toISOString(),
    total_study_time: 0,
    streak_days: 0
  })

  const createDefaultProgress = () => ({
    overall_progress: 15,
    weekly_goal: 100,
    weekly_progress: 25,
    subjects: {
      mathematics: { progress: 20, last_activity: new Date().toISOString() },
      science: { progress: 15, last_activity: new Date().toISOString() },
      history: { progress: 10, last_activity: new Date().toISOString() },
      portuguese: { progress: 18, last_activity: new Date().toISOString() },
      geography: { progress: 12, last_activity: new Date().toISOString() }
    },
    total_sessions: 0,
    total_time_minutes: 0
  })

  const createDefaultActivities = () => [
    {
      id: 1,
      subject: "Matemática",
      topic: "Explorando o Método de Singapura",
      progress: 25,
      timeSpent: 15,
      status: "in_progress",
      aiRecommendation: "Continue praticando! Você está indo muito bem.",
      timestamp: new Date().toISOString()
    },
    {
      id: 2,
      subject: "Tutor de IA",
      topic: "Conversa sobre ciências",
      progress: 100,
      timeSpent: 10,
      status: "completed",
      aiRecommendation: "Ótimas perguntas! Continue curioso.",
      timestamp: new Date(Date.now() - 3600000).toISOString()
    }
  ]

  const generateAchievements = () => {
    const newAchievements = []
    
    if (progressData?.total_sessions > 0) {
      newAchievements.push({
        id: 1,
        title: "Primeiro Passo",
        description: "Completou sua primeira atividade",
        icon: Play,
        color: "text-green-500",
        earned: true
      })
    }

    if (studentData?.streak_days >= 3) {
      newAchievements.push({
        id: 2,
        title: "Dedicação",
        description: "3 dias consecutivos de estudo",
        icon: Calendar,
        color: "text-blue-500",
        earned: true
      })
    }

    if (progressData?.subjects?.mathematics?.progress >= 20) {
      newAchievements.push({
        id: 3,
        title: "Explorador da Matemática",
        description: "20% de progresso em matemática",
        icon: Trophy,
        color: "text-yellow-500",
        earned: true
      })
    }

    // Conquistas futuras
    newAchievements.push({
      id: 4,
      title: "Pensador Crítico",
      description: "Complete 10 problemas do dia",
      icon: Brain,
      color: "text-purple-500",
      earned: false
    })

    setAchievements(newAchievements)
  }

  const getSubjectIcon = (subject) => {
    const icons = {
      'Matemática': BookOpen,
      'Ciências': Brain,
      'História': Clock,
      'Português': BookOpen,
      'Geografia': Target,
      'Tutor de IA': Zap
    }
    return icons[subject] || BookOpen
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      completed: { label: 'Concluído', variant: 'default', color: 'bg-green-100 text-green-800' },
      in_progress: { label: 'Em Progresso', variant: 'secondary', color: 'bg-blue-100 text-blue-800' },
      not_started: { label: 'Não Iniciado', variant: 'outline', color: 'bg-gray-100 text-gray-800' }
    }
    
    const config = statusConfig[status] || statusConfig.not_started
    return (
      <Badge className={config.color}>
        {config.label}
      </Badge>
    )
  }

  const formatTimeSpent = (minutes) => {
    if (minutes < 60) return `${minutes}min`
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return `${hours}h ${mins}min`
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-10 w-32" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-8 w-16" />
              </CardHeader>
            </Card>
          ))}
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <Skeleton className="h-6 w-48" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-32 w-full" />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <Skeleton className="h-6 w-48" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-32 w-full" />
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Olá, {studentData?.name || 'Estudante'}! 👋
          </h1>
          <p className="text-gray-600 mt-1">
            Bem-vindo de volta à sua jornada de aprendizado
          </p>
        </div>
        
        <Button 
          onClick={refreshDashboard} 
          disabled={refreshing}
          variant="outline"
          size="sm"
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
          Atualizar
        </Button>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Progresso Geral</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progressData?.overall_progress || 0}%</div>
            <Progress value={progressData?.overall_progress || 0} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Meta Semanal</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{progressData?.weekly_progress || 0}%</div>
            <Progress value={progressData?.weekly_progress || 0} className="mt-2" />
            <p className="text-xs text-muted-foreground mt-2">
              Meta: {progressData?.weekly_goal || 100}% por semana
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Sequência</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{studentData?.streak_days || 0}</div>
            <p className="text-xs text-muted-foreground">dias consecutivos</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tempo Total</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatTimeSpent(progressData?.total_time_minutes || 0)}
            </div>
            <p className="text-xs text-muted-foreground">tempo de estudo</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Recent Activities */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="w-5 h-5" />
              Atividades Recentes
            </CardTitle>
            <CardDescription>
              Suas últimas interações com a plataforma
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivities.length > 0 ? (
                recentActivities.map((activity) => {
                  const IconComponent = getSubjectIcon(activity.subject)
                  return (
                    <div key={activity.id} className="flex items-start space-x-4 p-4 rounded-lg border">
                      <div className="flex-shrink-0">
                        <IconComponent className="w-8 h-8 text-blue-500" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-gray-900">
                            {activity.subject}
                          </p>
                          {getStatusBadge(activity.status)}
                        </div>
                        <p className="text-sm text-gray-600 mt-1">
                          {activity.topic}
                        </p>
                        <div className="flex items-center space-x-4 mt-2">
                          <div className="flex items-center space-x-2">
                            <Progress value={activity.progress} className="w-20" />
                            <span className="text-xs text-gray-500">
                              {activity.progress}%
                            </span>
                          </div>
                          <span className="text-xs text-gray-500">
                            {formatTimeSpent(activity.timeSpent)}
                          </span>
                        </div>
                        {activity.aiRecommendation && (
                          <div className="mt-2 p-2 bg-blue-50 rounded text-xs text-blue-800">
                            💡 {activity.aiRecommendation}
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <BookOpen className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>Nenhuma atividade recente</p>
                  <p className="text-sm">Comece explorando a plataforma!</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Sidebar */}
        <div className="space-y-6">
          
          {/* Today's Problem */}
          {todayProblem && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="w-5 h-5" />
                  Problema do Dia
                </CardTitle>
              </CardHeader>
              <CardContent>
                <h4 className="font-medium mb-2">{todayProblem.title}</h4>
                <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                  {todayProblem.description?.substring(0, 100)}...
                </p>
                <Button size="sm" className="w-full">
                  <Play className="w-4 h-4 mr-2" />
                  Resolver Agora
                </Button>
              </CardContent>
            </Card>
          )}

          {/* Achievements */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Trophy className="w-5 h-5" />
                Conquistas
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {achievements.length > 0 ? (
                  achievements.map((achievement) => {
                    const IconComponent = achievement.icon
                    return (
                      <div 
                        key={achievement.id} 
                        className={`flex items-center space-x-3 p-2 rounded ${
                          achievement.earned ? 'bg-yellow-50' : 'bg-gray-50'
                        }`}
                      >
                        <IconComponent 
                          className={`w-6 h-6 ${
                            achievement.earned ? achievement.color : 'text-gray-400'
                          }`} 
                        />
                        <div className="flex-1">
                          <p className={`text-sm font-medium ${
                            achievement.earned ? 'text-gray-900' : 'text-gray-500'
                          }`}>
                            {achievement.title}
                          </p>
                          <p className="text-xs text-gray-500">
                            {achievement.description}
                          </p>
                        </div>
                        {achievement.earned && (
                          <CheckCircle className="w-4 h-4 text-green-500" />
                        )}
                      </div>
                    )
                  })
                ) : (
                  <div className="text-center py-4 text-gray-500">
                    <Trophy className="w-8 h-8 mx-auto mb-2 text-gray-300" />
                    <p className="text-sm">Continue estudando para conquistar badges!</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Subject Progress */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="w-5 h-5" />
                Progresso por Matéria
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {progressData?.subjects && Object.entries(progressData.subjects).map(([subject, data]) => (
                  <div key={subject} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="capitalize">{subject}</span>
                      <span>{data.progress}%</span>
                    </div>
                    <Progress value={data.progress} />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default DashboardFunctional

