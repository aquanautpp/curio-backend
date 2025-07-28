import { Skeleton } from '@/components/ui/skeleton.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { 
  Loader2, 
  RefreshCw, 
  BookOpen, 
  Brain, 
  Calculator,
  Microscope,
  Globe,
  Zap
} from 'lucide-react'

// Loading para Dashboard
export const DashboardSkeleton = () => (
  <div className="space-y-6 animate-pulse">
    {/* Header */}
    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <Skeleton className="h-8 w-64 mb-2" />
        <Skeleton className="h-4 w-48" />
      </div>
      <Skeleton className="h-10 w-32" />
    </div>

    {/* Stats Cards */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {[...Array(4)].map((_, i) => (
        <Card key={i}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-4 w-4 rounded" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-8 w-16 mb-2" />
            <Skeleton className="h-2 w-full" />
          </CardContent>
        </Card>
      ))}
    </div>

    {/* Main Content */}
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <Card className="lg:col-span-2">
        <CardHeader>
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-64" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="flex items-start space-x-4 p-4 rounded-lg border">
                <Skeleton className="w-8 h-8 rounded" />
                <div className="flex-1 space-y-2">
                  <Skeleton className="h-4 w-32" />
                  <Skeleton className="h-4 w-48" />
                  <div className="flex items-center space-x-4">
                    <Skeleton className="h-2 w-20" />
                    <Skeleton className="h-3 w-12" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="space-y-6">
        {[...Array(2)].map((_, i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-6 w-32" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-32 w-full" />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  </div>
)

// Loading para seções educacionais
export const SectionSkeleton = ({ title, icon: Icon }) => (
  <div className="space-y-6 animate-pulse">
    {/* Header */}
    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <div className="flex items-center gap-3 mb-2">
          <Icon className="w-8 h-8 text-gray-300" />
          <Skeleton className="h-8 w-48" />
        </div>
        <Skeleton className="h-4 w-64" />
      </div>
      <div className="flex items-center gap-2">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-10 w-24" />
      </div>
    </div>

    {/* Progress Cards */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {[...Array(3)].map((_, i) => (
        <Card key={i}>
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <Skeleton className="w-4 h-4 rounded" />
              <Skeleton className="h-4 w-20" />
            </div>
          </CardHeader>
          <CardContent>
            <Skeleton className="h-8 w-12 mb-2" />
            <Skeleton className="h-2 w-full" />
          </CardContent>
        </Card>
      ))}
    </div>

    {/* Content Grid */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {[...Array(6)].map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <div className="flex justify-between items-start">
              <div className="flex items-center gap-2">
                <Skeleton className="w-5 h-5 rounded" />
                <Skeleton className="h-5 w-32" />
              </div>
              <Skeleton className="h-5 w-16 rounded-full" />
            </div>
            <Skeleton className="h-4 w-full mt-2" />
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <Skeleton className="h-3 w-20" />
                <Skeleton className="h-3 w-12" />
              </div>
              <Skeleton className="h-10 w-full" />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  </div>
)

// Loading para exercícios/atividades
export const ExerciseSkeleton = () => (
  <Card className="animate-pulse">
    <CardHeader>
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Skeleton className="w-5 h-5 rounded" />
            <Skeleton className="h-6 w-48" />
          </div>
          <Skeleton className="h-4 w-64" />
        </div>
        <Skeleton className="h-5 w-20 rounded-full" />
      </div>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="p-4 bg-gray-50 rounded-lg">
        <Skeleton className="h-4 w-20 mb-2" />
        <Skeleton className="h-4 w-full mb-2" />
        <Skeleton className="h-4 w-3/4 mb-3" />
        <Skeleton className="h-12 w-32 mx-auto" />
      </div>

      <div className="space-y-2">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-10 w-full" />
      </div>

      <div className="flex gap-2">
        <Skeleton className="h-10 w-32" />
        <Skeleton className="h-10 w-20" />
        <Skeleton className="h-10 w-16" />
      </div>
    </CardContent>
  </Card>
)

// Loading para chat do tutor
export const ChatSkeleton = () => (
  <div className="space-y-4 animate-pulse">
    {[...Array(3)].map((_, i) => (
      <div key={i} className={`flex ${i % 2 === 0 ? 'justify-start' : 'justify-end'}`}>
        <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
          i % 2 === 0 ? 'bg-gray-100' : 'bg-blue-100'
        }`}>
          <Skeleton className="h-4 w-full mb-1" />
          <Skeleton className="h-4 w-3/4" />
        </div>
      </div>
    ))}
    
    {/* Typing indicator */}
    <div className="flex justify-start">
      <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-100">
        <div className="flex space-x-1">
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
        </div>
      </div>
    </div>
  </div>
)

// Loading para problema do dia
export const ProblemSkeleton = () => (
  <Card className="animate-pulse">
    <CardHeader>
      <div className="flex items-center gap-2 mb-2">
        <Brain className="w-5 h-5 text-gray-300" />
        <Skeleton className="h-6 w-40" />
      </div>
    </CardHeader>
    <CardContent>
      <Skeleton className="h-4 w-full mb-2" />
      <Skeleton className="h-4 w-3/4 mb-4" />
      <Skeleton className="h-10 w-full" />
    </CardContent>
  </Card>
)

// Loading states com animações personalizadas
export const SpinnerLoader = ({ size = 'md', text = 'Carregando...' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  }

  return (
    <div className="flex flex-col items-center justify-center py-8">
      <Loader2 className={`${sizeClasses[size]} animate-spin text-blue-500 mb-2`} />
      <p className="text-sm text-gray-600">{text}</p>
    </div>
  )
}

export const PulseLoader = ({ text = 'Processando...' }) => (
  <div className="flex flex-col items-center justify-center py-8">
    <div className="flex space-x-2 mb-4">
      <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
      <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
      <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
    </div>
    <p className="text-sm text-gray-600">{text}</p>
  </div>
)

export const DotsLoader = ({ text = 'Aguarde...' }) => (
  <div className="flex flex-col items-center justify-center py-8">
    <div className="flex space-x-1 mb-4">
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
    </div>
    <p className="text-sm text-gray-600">{text}</p>
  </div>
)

// Loading para diferentes seções
export const MathSkeleton = () => <SectionSkeleton title="Matemática" icon={Calculator} />
export const ScienceSkeleton = () => <SectionSkeleton title="Ciências" icon={Microscope} />
export const HistorySkeleton = () => <SectionSkeleton title="História" icon={BookOpen} />
export const GeographySkeleton = () => <SectionSkeleton title="Geografia" icon={Globe} />

// Loading overlay para operações
export const LoadingOverlay = ({ isLoading, text = 'Carregando...', children }) => (
  <div className="relative">
    {children}
    {isLoading && (
      <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center z-50">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-blue-500 mx-auto mb-2" />
          <p className="text-sm text-gray-600">{text}</p>
        </div>
      </div>
    )}
  </div>
)

// Loading para listas
export const ListSkeleton = ({ items = 5, showAvatar = false }) => (
  <div className="space-y-3">
    {[...Array(items)].map((_, i) => (
      <div key={i} className="flex items-center space-x-3 p-3 rounded-lg border animate-pulse">
        {showAvatar && <Skeleton className="w-10 h-10 rounded-full" />}
        <div className="flex-1 space-y-2">
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-3 w-1/2" />
        </div>
        <Skeleton className="h-8 w-20" />
      </div>
    ))}
  </div>
)

// Loading para formulários
export const FormSkeleton = () => (
  <div className="space-y-4 animate-pulse">
    {[...Array(4)].map((_, i) => (
      <div key={i} className="space-y-2">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-10 w-full" />
      </div>
    ))}
    <Skeleton className="h-10 w-32" />
  </div>
)

export default {
  DashboardSkeleton,
  SectionSkeleton,
  ExerciseSkeleton,
  ChatSkeleton,
  ProblemSkeleton,
  SpinnerLoader,
  PulseLoader,
  DotsLoader,
  MathSkeleton,
  ScienceSkeleton,
  HistorySkeleton,
  GeographySkeleton,
  LoadingOverlay,
  ListSkeleton,
  FormSkeleton
}

