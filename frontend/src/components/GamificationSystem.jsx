import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { 
  AnimatedCard, 
  AnimatedProgress, 
  AnimatedCounter,
  AchievementCard,
  AnimatedStats
} from './AnimatedComponents.jsx'
import {
  Trophy,
  Star,
  Zap,
  Target,
  Calendar,
  Clock,
  TrendingUp,
  Award,
  Crown,
  Flame,
  BookOpen,
  Brain,
  Play,
  CheckCircle,
  Medal,
  Sparkles,
  Users,
  BarChart3
} from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const GamificationSystem = ({ studentId = 1 }) => {
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [studentData, setStudentData] = useState(null)
  const [achievements, setAchievements] = useState({ earned: [], in_progress: [], available: [] })
  const [leaderboard, setLeaderboard] = useState([])
  const [recentActivities, setRecentActivities] = useState([])

  useEffect(() => {
    loadGamificationData()
  }, [studentId])

  const loadGamificationData = async () => {
    setLoading(true)
    try {
      // Carrega dados em paralelo
      const [progressRes, achievementsRes, activitiesRes] = await Promise.allSettled([
        fetch(`${API_BASE_URL}/gamification/students/${studentId}/progress`),
        fetch(`${API_BASE_URL}/gamification/students/${studentId}/achievements`),
        fetch(`${API_BASE_URL}/gamification/students/${studentId}/activities?per_page=10`)
      ])

      // Processa progresso
      if (progressRes.status === 'fulfilled' && progressRes.value.ok) {
        const data = await progressRes.value.json()
        setStudentData(data.progress)
      } else {
        setStudentData(createMockStudentData())
      }

      // Processa conquistas
      if (achievementsRes.status === 'fulfilled' && achievementsRes.value.ok) {
        const data = await achievementsRes.value.json()
        setAchievements(data)
      } else {
        setAchievements(createMockAchievements())
      }

      // Processa atividades
      if (activitiesRes.status === 'fulfilled' && activitiesRes.value.ok) {
        const data = await activitiesRes.value.json()
        setRecentActivities(data.activities || [])
      }

      // Carrega leaderboard
      loadLeaderboard()

    } catch (error) {
      console.error('Erro ao carregar dados de gamificação:', error)
      setStudentData(createMockStudentData())
      setAchievements(createMockAchievements())
    } finally {
      setLoading(false)
    }
  }

  const loadLeaderboard = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/gamification/leaderboard?type=points&limit=10`)
      if (response.ok) {
        const data = await response.json()
        setLeaderboard(data.leaderboard || [])
      }
    } catch (error) {
      console.error('Erro ao carregar leaderboard:', error)
    }
  }

  const createMockStudentData = () => ({
    overall_progress: 35,
    total_time_minutes: 480,
    total_exercises: 45,
    total_correct: 38,
    accuracy: 84.4,
    subject_progress: {
      mathematics: { progress: 45, time_spent: 180 },
      science: { progress: 30, time_spent: 120 },
      history: { progress: 25, time_spent: 90 },
      portuguese: { progress: 40, time_spent: 90 }
    },
    streak: {
      current_streak: 7,
      longest_streak: 12,
      total_study_days: 28
    },
    points: {
      total_points: 1250,
      points_this_week: 180,
      points_this_month: 720,
      level: 13,
      experience_points: 1250,
      level_progress: 50,
      points_to_next_level: 150
    }
  })

  const createMockAchievements = () => ({
    earned: [
      {
        achievement: {
          id: 1,
          name: 'Primeiro Passo',
          description: 'Complete seu primeiro exercício',
          icon: 'play',
          category: 'progress',
          points: 10,
          rarity: 'common'
        },
        student_achievement: {
          earned_at: new Date().toISOString(),
          progress: 100
        }
      },
      {
        achievement: {
          id: 2,
          name: 'Dedicado',
          description: 'Estude por 3 dias consecutivos',
          icon: 'calendar',
          category: 'streak',
          points: 25,
          rarity: 'common'
        },
        student_achievement: {
          earned_at: new Date().toISOString(),
          progress: 100
        }
      }
    ],
    in_progress: [
      {
        achievement: {
          id: 3,
          name: 'Persistente',
          description: 'Estude por 7 dias consecutivos',
          icon: 'target',
          category: 'streak',
          points: 50,
          rarity: 'rare'
        },
        student_achievement: {
          progress: 85
        }
      }
    ],
    available: [
      {
        id: 4,
        name: 'Maratonista',
        description: 'Estude por 30 dias consecutivos',
        icon: 'trophy',
        category: 'streak',
        points: 200,
        rarity: 'legendary'
      }
    ]
  })

  const getIconComponent = (iconName) => {
    const icons = {
      play: Play,
      calendar: Calendar,
      target: Target,
      trophy: Trophy,
      'book-open': BookOpen,
      brain: Brain,
      star: Star,
      zap: Zap,
      crown: Crown,
      clock: Clock
    }
    return icons[iconName] || Trophy
  }

  const getRarityColor = (rarity) => {
    const colors = {
      common: 'text-gray-600 bg-gray-100',
      rare: 'text-blue-600 bg-blue-100',
      epic: 'text-purple-600 bg-purple-100',
      legendary: 'text-yellow-600 bg-yellow-100'
    }
    return colors[rarity] || colors.common
  }

  const formatTime = (minutes) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    if (hours > 0) {
      return `${hours}h ${mins}min`
    }
    return `${mins}min`
  }

  const getSubjectIcon = (subject) => {
    const icons = {
      mathematics: Target,
      science: Brain,
      history: BookOpen,
      portuguese: BookOpen,
      geography: Target
    }
    return icons[subject] || BookOpen
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="text-center py-12">
          <Sparkles className="w-8 h-8 animate-spin mx-auto mb-4 text-yellow-500" />
          <p>Carregando seu progresso...</p>
        </div>
      </div>
    )
  }

  const statsData = [
    {
      title: 'Level',
      value: studentData?.points?.level || 1,
      icon: Crown,
      progress: studentData?.points?.level_progress || 0,
      change: 5
    },
    {
      title: 'Pontos Totais',
      value: studentData?.points?.total_points || 0,
      icon: Zap,
      change: 12
    },
    {
      title: 'Sequência Atual',
      value: studentData?.streak?.current_streak || 0,
      suffix: ' dias',
      icon: Flame,
      change: 8
    },
    {
      title: 'Tempo de Estudo',
      value: Math.floor((studentData?.total_time_minutes || 0) / 60),
      suffix: 'h',
      icon: Clock,
      change: 15
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 flex items-center justify-center gap-3">
          <Trophy className="w-8 h-8 text-yellow-500" />
          Seu Progresso
        </h1>
        <p className="text-gray-600 mt-2">
          Acompanhe suas conquistas e evolução nos estudos
        </p>
      </div>

      {/* Stats Overview */}
      <AnimatedStats stats={statsData} />

      {/* Level Progress */}
      <AnimatedCard delay={200}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Crown className="w-5 h-5 text-yellow-500" />
            Level {studentData?.points?.level || 1}
          </CardTitle>
          <CardDescription>
            Faltam {studentData?.points?.points_to_next_level || 0} pontos para o próximo level
          </CardDescription>
        </CardHeader>
        <CardContent>
          <AnimatedProgress 
            value={studentData?.points?.level_progress || 0} 
            delay={300}
          />
        </CardContent>
      </AnimatedCard>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Visão Geral</TabsTrigger>
          <TabsTrigger value="achievements">Conquistas</TabsTrigger>
          <TabsTrigger value="progress">Progresso</TabsTrigger>
          <TabsTrigger value="leaderboard">Ranking</TabsTrigger>
        </TabsList>

        {/* Visão Geral */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Streak Info */}
            <AnimatedCard delay={100}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Flame className="w-5 h-5 text-orange-500" />
                  Sequência de Estudos
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="text-4xl font-bold text-orange-500 mb-2">
                    <AnimatedCounter end={studentData?.streak?.current_streak || 0} />
                  </div>
                  <p className="text-gray-600 mb-4">dias consecutivos</p>
                  <div className="flex justify-between text-sm text-gray-500">
                    <span>Recorde: {studentData?.streak?.longest_streak || 0} dias</span>
                    <span>Total: {studentData?.streak?.total_study_days || 0} dias</span>
                  </div>
                </div>
              </CardContent>
            </AnimatedCard>

            {/* Weekly Progress */}
            <AnimatedCard delay={200}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-blue-500" />
                  Esta Semana
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>Pontos</span>
                    <span className="font-bold text-blue-500">
                      {studentData?.points?.points_this_week || 0}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Exercícios</span>
                    <span className="font-bold">
                      {Math.floor((studentData?.total_exercises || 0) * 0.3)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Tempo</span>
                    <span className="font-bold">
                      {formatTime(Math.floor((studentData?.total_time_minutes || 0) * 0.25))}
                    </span>
                  </div>
                </div>
              </CardContent>
            </AnimatedCard>

            {/* Subject Progress */}
            <AnimatedCard delay={300} className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-green-500" />
                  Progresso por Matéria
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(studentData?.subject_progress || {}).map(([subject, data], index) => {
                    const IconComponent = getSubjectIcon(subject)
                    return (
                      <div key={subject} className="space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <IconComponent className="w-4 h-4" />
                            <span className="capitalize text-sm">{subject}</span>
                          </div>
                          <span className="text-sm font-medium">{data.progress}%</span>
                        </div>
                        <AnimatedProgress 
                          value={data.progress} 
                          delay={400 + (index * 100)}
                        />
                        <p className="text-xs text-gray-500">
                          Tempo: {formatTime(data.time_spent)}
                        </p>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </AnimatedCard>
          </div>
        </TabsContent>

        {/* Conquistas */}
        <TabsContent value="achievements" className="space-y-6">
          
          {/* Conquistas Obtidas */}
          {achievements.earned.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Medal className="w-5 h-5 text-yellow-500" />
                Conquistas Obtidas ({achievements.earned.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {achievements.earned.map((item, index) => {
                  const IconComponent = getIconComponent(item.achievement.icon)
                  return (
                    <AchievementCard
                      key={item.achievement.id}
                      achievement={{
                        ...item.achievement,
                        icon: IconComponent,
                        earned: true,
                        progress: 100
                      }}
                      delay={index * 100}
                    />
                  )
                })}
              </div>
            </div>
          )}

          {/* Conquistas em Progresso */}
          {achievements.in_progress.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Target className="w-5 h-5 text-blue-500" />
                Em Progresso ({achievements.in_progress.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {achievements.in_progress.map((item, index) => {
                  const IconComponent = getIconComponent(item.achievement.icon)
                  return (
                    <AchievementCard
                      key={item.achievement.id}
                      achievement={{
                        ...item.achievement,
                        icon: IconComponent,
                        earned: false,
                        progress: item.student_achievement.progress,
                        requirement: `${Math.floor((item.student_achievement.progress / 100) * item.achievement.requirement_value)}/${item.achievement.requirement_value}`
                      }}
                      delay={index * 100}
                    />
                  )
                })}
              </div>
            </div>
          )}

          {/* Conquistas Disponíveis */}
          {achievements.available.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Star className="w-5 h-5 text-gray-500" />
                Disponíveis ({achievements.available.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {achievements.available.slice(0, 6).map((achievement, index) => {
                  const IconComponent = getIconComponent(achievement.icon)
                  return (
                    <AchievementCard
                      key={achievement.id}
                      achievement={{
                        ...achievement,
                        icon: IconComponent,
                        earned: false,
                        progress: 0,
                        requirement: `0/${achievement.requirement_value}`
                      }}
                      delay={index * 100}
                    />
                  )
                })}
              </div>
            </div>
          )}
        </TabsContent>

        {/* Progresso Detalhado */}
        <TabsContent value="progress" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Estatísticas Gerais */}
            <AnimatedCard>
              <CardHeader>
                <CardTitle>Estatísticas Gerais</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center">
                  <span>Progresso Geral</span>
                  <span className="font-bold text-green-500">
                    {studentData?.overall_progress || 0}%
                  </span>
                </div>
                <AnimatedProgress value={studentData?.overall_progress || 0} />
                
                <div className="grid grid-cols-2 gap-4 pt-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-500">
                      <AnimatedCounter end={studentData?.total_exercises || 0} />
                    </div>
                    <p className="text-sm text-gray-600">Exercícios</p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-500">
                      {studentData?.accuracy || 0}%
                    </div>
                    <p className="text-sm text-gray-600">Precisão</p>
                  </div>
                </div>
              </CardContent>
            </AnimatedCard>

            {/* Atividades Recentes */}
            <AnimatedCard delay={200}>
              <CardHeader>
                <CardTitle>Atividades Recentes</CardTitle>
              </CardHeader>
              <CardContent>
                {recentActivities.length > 0 ? (
                  <div className="space-y-3">
                    {recentActivities.slice(0, 5).map((activity, index) => (
                      <div key={activity.id} className="flex items-center justify-between p-2 rounded border">
                        <div>
                          <p className="text-sm font-medium">{activity.subject}</p>
                          <p className="text-xs text-gray-500">{activity.topic}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium text-green-500">
                            +{activity.points_earned} pts
                          </p>
                          <p className="text-xs text-gray-500">
                            {formatTime(activity.time_spent_minutes)}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <BookOpen className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                    <p>Nenhuma atividade recente</p>
                  </div>
                )}
              </CardContent>
            </AnimatedCard>
          </div>
        </TabsContent>

        {/* Leaderboard */}
        <TabsContent value="leaderboard" className="space-y-6">
          <AnimatedCard>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5 text-purple-500" />
                Ranking de Pontos
              </CardTitle>
              <CardDescription>
                Os estudantes com mais pontos da plataforma
              </CardDescription>
            </CardHeader>
            <CardContent>
              {leaderboard.length > 0 ? (
                <div className="space-y-3">
                  {leaderboard.map((student, index) => (
                    <div 
                      key={student.student_id} 
                      className={`
                        flex items-center justify-between p-3 rounded-lg
                        ${index < 3 ? 'bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200' : 'bg-gray-50'}
                        ${student.student_id === studentId ? 'ring-2 ring-blue-500' : ''}
                      `}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`
                          w-8 h-8 rounded-full flex items-center justify-center font-bold
                          ${index === 0 ? 'bg-yellow-500 text-white' : 
                            index === 1 ? 'bg-gray-400 text-white' :
                            index === 2 ? 'bg-orange-500 text-white' :
                            'bg-gray-200 text-gray-700'}
                        `}>
                          {student.rank}
                        </div>
                        <div>
                          <p className="font-medium">
                            {student.student_id === studentId ? 'Você' : `Estudante ${student.student_id}`}
                          </p>
                          <p className="text-sm text-gray-500">Level {student.level}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-lg">{student.total_points}</p>
                        <p className="text-sm text-gray-500">pontos</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <Users className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>Ranking não disponível</p>
                </div>
              )}
            </CardContent>
          </AnimatedCard>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default GamificationSystem

