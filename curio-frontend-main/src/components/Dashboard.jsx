import React, { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import {
  BookOpen,
  Trophy,
  Clock,
  TrendingUp,
  Play,
  CheckCircle,
  Star,
  Brain,
  Target
} from 'lucide-react'

const Dashboard = ({ onNavigate }) => {
  const [studentData] = useState({
    name: "Ana Silva",
    grade: "7º Ano",
    totalProgress: 68,
    weeklyGoal: 85,
    streakDays: 12,
    achievements: [
      { id: 1, title: "Mestre da Matemática", icon: Trophy, color: "text-yellow-500" },
      { id: 2, title: "Pensador Crítico", icon: Brain, color: "text-purple-500" },
      { id: 3, title: "Meta Semanal", icon: Target, color: "text-green-500" }
    ]
  })

  const [recentActivities] = useState([
    {
      id: 1,
      subject: "Matemática",
      topic: "Frações - Método Concreto",
      progress: 85,
      timeSpent: 25,
      status: "completed",
      aiRecommendation: "Excelente! Pronta para a fase pictórica."
    },
    {
      id: 2,
      subject: "Ciências",
      topic: "Sistema Solar",
      progress: 60,
      timeSpent: 18,
      status: "in_progress",
      aiRecommendation: "Continue explorando! Foque nos planetas gasosos."
    },
    {
      id: 3,
      subject: "Matemática",
      topic: "Geometria Básica",
      progress: 100,
      timeSpent: 30,
      status: "mastered",
      aiRecommendation: "Dominado! Vamos para geometria avançada."
    }
  ])

  const [aiInsights] = useState({
    learningStyle: "Visual",
    strongSubjects: ["Matemática", "Geometria"],
    needsImprovement: ["Álgebra", "Interpretação de Texto"],
    recommendedNextSteps: [
      "Praticar mais exercícios de álgebra básica",
      "Utilizar recursos visuais para interpretação de texto",
      "Continuar com o Método de Singapura em frações"
    ]
  })

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Olá, {studentData.name}! 👋
          </h1>
          <p className="text-gray-600 mt-2">
            {studentData.grade} • Vamos continuar sua jornada de aprendizado
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Progresso Geral</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{studentData.totalProgress}%</div>
              <Progress value={studentData.totalProgress} className="mt-2" />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Meta Semanal</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{studentData.weeklyGoal}%</div>
              <p className="text-xs text-muted-foreground">
                +12% desde ontem
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Sequência</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{studentData.streakDays} dias</div>
              <p className="text-xs text-muted-foreground">
                Continue assim! 🔥
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Conquistas</CardTitle>
              <Trophy className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{studentData.achievements.length}</div>
              <p className="text-xs text-muted-foreground">
                Novas esta semana
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Activities */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Atividades Recentes</CardTitle>
                <CardDescription>
                  Seu progresso nas últimas atividades
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentActivities.map((activity) => (
                    <div key={activity.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                          <BookOpen className="h-5 w-5 text-blue-600" />
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">{activity.topic}</h4>
                          <p className="text-sm text-gray-600">{activity.subject}</p>
                          <p className="text-xs text-blue-600 mt-1">{activity.aiRecommendation}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center space-x-2 mb-2">
                          {activity.status === 'completed' && (
                            <Badge variant="secondary">
                              <CheckCircle className="h-3 w-3 mr-1" />
                              Concluído
                            </Badge>
                          )}
                          {activity.status === 'mastered' && (
                            <Badge className="bg-green-100 text-green-800">
                              <Star className="h-3 w-3 mr-1" />
                              Dominado
                            </Badge>
                          )}
                          {activity.status === 'in_progress' && (
                            <Badge variant="outline">
                              <Play className="h-3 w-3 mr-1" />
                              Em Progresso
                            </Badge>
                          )}
                        </div>
                        <div className="text-sm text-gray-600">
                          {activity.progress}% • {activity.timeSpent}min
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* AI Insights */}
          <div>
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="h-5 w-5 mr-2 text-purple-600" />
                  Insights da IA
                </CardTitle>
                <CardDescription>
                  Análise personalizada do seu aprendizado
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Estilo de Aprendizagem</h4>
                    <Badge variant="secondary">{aiInsights.learningStyle}</Badge>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Pontos Fortes</h4>
                    <div className="flex flex-wrap gap-2">
                      {aiInsights.strongSubjects.map((subject, index) => (
                        <Badge key={index} className="bg-green-100 text-green-800">
                          {subject}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Áreas para Melhorar</h4>
                    <div className="flex flex-wrap gap-2">
                      {aiInsights.needsImprovement.map((subject, index) => (
                        <Badge key={index} variant="outline">
                          {subject}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Achievements */}
            <Card>
              <CardHeader>
                <CardTitle>Conquistas Recentes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {studentData.achievements.map((achievement) => (
                    <div key={achievement.id} className="flex items-center space-x-3">
                      <achievement.icon className={`h-6 w-6 ${achievement.color}`} />
                      <span className="text-sm font-medium">{achievement.title}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Recommended Next Steps */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Próximos Passos Recomendados</CardTitle>
            <CardDescription>
              Com base na sua análise de aprendizado personalizada
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {aiInsights.recommendedNextSteps.map((step, index) => (
                <div key={index} className="flex items-center justify-between py-2">
                  <span>{step}</span>
                  <Button onClick={() => {
                    if (step.includes('álgebra')) onNavigate('problem');
                    else if (step.includes('interpretação de texto')) onNavigate('tutor');
                    else if (step.includes('frações')) onNavigate('singapore');
                  }}>
                    Começar
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard

