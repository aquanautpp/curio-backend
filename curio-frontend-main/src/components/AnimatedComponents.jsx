import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  CheckCircle, 
  Star, 
  Trophy, 
  Zap, 
  TrendingUp,
  ArrowRight,
  Sparkles,
  Target
} from 'lucide-react'

// Hook para animações de entrada
const useInView = (threshold = 0.1) => {
  const [isInView, setIsInView] = useState(false)
  const [ref, setRef] = useState(null)

  useEffect(() => {
    if (!ref) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true)
        }
      },
      { threshold }
    )

    observer.observe(ref)
    return () => observer.disconnect()
  }, [ref, threshold])

  return [setRef, isInView]
}

// Componente de card animado
export const AnimatedCard = ({ 
  children, 
  delay = 0, 
  direction = 'up',
  className = '',
  hover = true,
  ...props 
}) => {
  const [ref, isInView] = useInView()
  
  const directions = {
    up: 'translate-y-8',
    down: 'translate-y-[-32px]',
    left: 'translate-x-[-32px]',
    right: 'translate-x-8'
  }

  return (
    <Card
      ref={ref}
      className={`
        transition-all duration-700 ease-out
        ${isInView 
          ? 'opacity-100 translate-x-0 translate-y-0' 
          : `opacity-0 ${directions[direction]}`
        }
        ${hover ? 'hover:shadow-lg hover:scale-[1.02] hover:-translate-y-1' : ''}
        ${className}
      `}
      style={{ transitionDelay: `${delay}ms` }}
      {...props}
    >
      {children}
    </Card>
  )
}

// Progresso animado
export const AnimatedProgress = ({ value, max = 100, duration = 1000, delay = 0 }) => {
  const [animatedValue, setAnimatedValue] = useState(0)
  const [ref, isInView] = useInView()

  useEffect(() => {
    if (!isInView) return

    const timer = setTimeout(() => {
      const increment = value / (duration / 16) // 60fps
      let current = 0
      
      const animate = () => {
        current += increment
        if (current >= value) {
          setAnimatedValue(value)
        } else {
          setAnimatedValue(Math.floor(current))
          requestAnimationFrame(animate)
        }
      }
      
      animate()
    }, delay)

    return () => clearTimeout(timer)
  }, [isInView, value, duration, delay])

  return (
    <div ref={ref} className="space-y-2">
      <div className="flex justify-between text-sm">
        <span>Progresso</span>
        <span className="font-medium">{animatedValue}%</span>
      </div>
      <Progress 
        value={animatedValue} 
        className="transition-all duration-300"
      />
    </div>
  )
}

// Contador animado
export const AnimatedCounter = ({ 
  end, 
  start = 0, 
  duration = 2000, 
  delay = 0,
  suffix = '',
  prefix = '',
  className = ''
}) => {
  const [count, setCount] = useState(start)
  const [ref, isInView] = useInView()

  useEffect(() => {
    if (!isInView) return

    const timer = setTimeout(() => {
      const increment = (end - start) / (duration / 16)
      let current = start
      
      const animate = () => {
        current += increment
        if (current >= end) {
          setCount(end)
        } else {
          setCount(Math.floor(current))
          requestAnimationFrame(animate)
        }
      }
      
      animate()
    }, delay)

    return () => clearTimeout(timer)
  }, [isInView, end, start, duration, delay])

  return (
    <span ref={ref} className={`font-bold ${className}`}>
      {prefix}{count}{suffix}
    </span>
  )
}

// Badge com animação de pulso
export const PulseBadge = ({ children, variant = 'default', pulse = true, ...props }) => (
  <Badge 
    variant={variant}
    className={`
      transition-all duration-300
      ${pulse ? 'animate-pulse hover:animate-none' : ''}
    `}
    {...props}
  >
    {children}
  </Badge>
)

// Botão com efeitos de hover avançados
export const AnimatedButton = ({ 
  children, 
  variant = 'default',
  size = 'default',
  loading = false,
  success = false,
  className = '',
  ...props 
}) => {
  const [isClicked, setIsClicked] = useState(false)

  const handleClick = (e) => {
    setIsClicked(true)
    setTimeout(() => setIsClicked(false), 200)
    props.onClick?.(e)
  }

  return (
    <Button
      variant={variant}
      size={size}
      className={`
        transition-all duration-300 ease-out
        hover:shadow-md hover:scale-105
        active:scale-95
        ${isClicked ? 'scale-95' : ''}
        ${success ? 'bg-green-500 hover:bg-green-600' : ''}
        ${className}
      `}
      onClick={handleClick}
      disabled={loading}
      {...props}
    >
      <div className={`flex items-center gap-2 transition-all duration-300 ${loading ? 'opacity-70' : ''}`}>
        {loading && (
          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
        )}
        {success && <CheckCircle className="w-4 h-4" />}
        {children}
      </div>
    </Button>
  )
}

// Card de conquista com animação especial
export const AchievementCard = ({ 
  achievement, 
  delay = 0,
  onUnlock = () => {} 
}) => {
  const [ref, isInView] = useInView()
  const [isUnlocking, setIsUnlocking] = useState(false)

  const handleUnlock = () => {
    setIsUnlocking(true)
    setTimeout(() => {
      onUnlock(achievement)
      setIsUnlocking(false)
    }, 1000)
  }

  const IconComponent = achievement.icon

  return (
    <Card
      ref={ref}
      className={`
        transition-all duration-700 ease-out
        ${isInView 
          ? 'opacity-100 translate-y-0' 
          : 'opacity-0 translate-y-8'
        }
        ${achievement.earned 
          ? 'border-yellow-200 bg-gradient-to-br from-yellow-50 to-orange-50 shadow-lg' 
          : 'hover:shadow-md'
        }
        ${isUnlocking ? 'animate-pulse scale-105' : ''}
      `}
      style={{ transitionDelay: `${delay}ms` }}
    >
      <CardHeader>
        <div className="flex items-center gap-3">
          <div className={`
            p-2 rounded-full transition-all duration-500
            ${achievement.earned 
              ? 'bg-yellow-100 text-yellow-600 animate-bounce' 
              : 'bg-gray-100 text-gray-400'
            }
          `}>
            <IconComponent className="w-6 h-6" />
          </div>
          <div>
            <CardTitle className={`
              transition-colors duration-300
              ${achievement.earned ? 'text-gray-900' : 'text-gray-500'}
            `}>
              {achievement.title}
              {achievement.earned && (
                <Sparkles className="inline w-4 h-4 ml-2 text-yellow-500 animate-pulse" />
              )}
            </CardTitle>
            <CardDescription>{achievement.description}</CardDescription>
          </div>
          {achievement.earned && (
            <CheckCircle className="w-6 h-6 text-green-500 ml-auto animate-bounce" />
          )}
        </div>
      </CardHeader>
      {!achievement.earned && (
        <CardContent>
          <p className="text-sm text-gray-600 mb-3">
            Requisito: {achievement.requirement}
          </p>
          <Progress value={achievement.progress || 0} className="h-2" />
        </CardContent>
      )}
    </Card>
  )
}

// Seção de estatísticas animadas
export const AnimatedStats = ({ stats, delay = 0 }) => {
  const [ref, isInView] = useInView()

  return (
    <div 
      ref={ref}
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
    >
      {stats.map((stat, index) => (
        <Card
          key={stat.id || index}
          className={`
            transition-all duration-700 ease-out
            hover:shadow-lg hover:scale-105
            ${isInView 
              ? 'opacity-100 translate-y-0' 
              : 'opacity-0 translate-y-8'
            }
          `}
          style={{ transitionDelay: `${delay + (index * 100)}ms` }}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
            {stat.icon && (
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            )}
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              <AnimatedCounter 
                end={stat.value} 
                suffix={stat.suffix || ''}
                prefix={stat.prefix || ''}
                delay={delay + (index * 100)}
              />
            </div>
            {stat.change && (
              <div className={`
                flex items-center text-xs mt-1
                ${stat.change > 0 ? 'text-green-600' : 'text-red-600'}
              `}>
                <TrendingUp className="w-3 h-3 mr-1" />
                {stat.change > 0 ? '+' : ''}{stat.change}%
              </div>
            )}
            {stat.progress !== undefined && (
              <div className="mt-2">
                <AnimatedProgress 
                  value={stat.progress} 
                  delay={delay + (index * 100) + 200}
                />
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

// Lista animada de atividades
export const AnimatedActivityList = ({ activities, delay = 0 }) => {
  const [ref, isInView] = useInView()

  return (
    <div ref={ref} className="space-y-4">
      {activities.map((activity, index) => (
        <Card
          key={activity.id}
          className={`
            transition-all duration-500 ease-out
            hover:shadow-md hover:scale-[1.01]
            ${isInView 
              ? 'opacity-100 translate-x-0' 
              : 'opacity-0 translate-x-[-20px]'
            }
          `}
          style={{ transitionDelay: `${delay + (index * 100)}ms` }}
        >
          <CardContent className="p-4">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                {activity.icon && (
                  <activity.icon className="w-8 h-8 text-blue-500" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-900">
                    {activity.subject}
                  </p>
                  <Badge 
                    variant={activity.status === 'completed' ? 'default' : 'secondary'}
                    className="transition-colors duration-300"
                  >
                    {activity.status === 'completed' ? 'Concluído' : 'Em Progresso'}
                  </Badge>
                </div>
                <p className="text-sm text-gray-600 mb-2">
                  {activity.topic}
                </p>
                <div className="flex items-center space-x-4">
                  <AnimatedProgress 
                    value={activity.progress} 
                    delay={delay + (index * 100) + 200}
                  />
                  <span className="text-xs text-gray-500">
                    {activity.timeSpent}min
                  </span>
                </div>
                {activity.aiRecommendation && (
                  <div className="mt-2 p-2 bg-blue-50 rounded text-xs text-blue-800 animate-fade-in">
                    💡 {activity.aiRecommendation}
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

// Componente de feedback animado
export const AnimatedFeedback = ({ 
  feedback, 
  onClose = () => {},
  autoClose = true,
  duration = 3000 
}) => {
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    if (autoClose) {
      const timer = setTimeout(() => {
        setIsVisible(false)
        setTimeout(onClose, 300)
      }, duration)
      
      return () => clearTimeout(timer)
    }
  }, [autoClose, duration, onClose])

  if (!feedback) return null

  return (
    <div className={`
      fixed top-4 right-4 z-50
      transition-all duration-300 ease-out
      ${isVisible 
        ? 'opacity-100 translate-x-0' 
        : 'opacity-0 translate-x-full'
      }
    `}>
      <Card className={`
        max-w-sm shadow-lg border-l-4
        ${feedback.is_correct 
          ? 'border-l-green-500 bg-green-50' 
          : 'border-l-yellow-500 bg-yellow-50'
        }
      `}>
        <CardContent className="p-4">
          <div className="flex items-start gap-2">
            {feedback.is_correct ? (
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
            ) : (
              <Target className="w-5 h-5 text-yellow-600 mt-0.5" />
            )}
            <div>
              <p className="font-medium text-sm">{feedback.message}</p>
              {feedback.explanation && (
                <p className="text-xs mt-1 text-gray-600">
                  {feedback.explanation}
                </p>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Componente de transição de página
export const PageTransition = ({ children, isLoading = false }) => {
  return (
    <div className={`
      transition-all duration-500 ease-out
      ${isLoading 
        ? 'opacity-0 translate-y-4' 
        : 'opacity-100 translate-y-0'
      }
    `}>
      {children}
    </div>
  )
}

// CSS personalizado para animações adicionais
export const AnimationStyles = () => (
  <style jsx global>{`
    @keyframes fade-in {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    
    @keyframes slide-up {
      from { 
        opacity: 0; 
        transform: translateY(20px); 
      }
      to { 
        opacity: 1; 
        transform: translateY(0); 
      }
    }
    
    @keyframes bounce-in {
      0% { 
        opacity: 0; 
        transform: scale(0.3); 
      }
      50% { 
        opacity: 1; 
        transform: scale(1.05); 
      }
      70% { 
        transform: scale(0.9); 
      }
      100% { 
        opacity: 1; 
        transform: scale(1); 
      }
    }
    
    .animate-fade-in {
      animation: fade-in 0.5s ease-out;
    }
    
    .animate-slide-up {
      animation: slide-up 0.6s ease-out;
    }
    
    .animate-bounce-in {
      animation: bounce-in 0.8s ease-out;
    }
    
    .hover-lift {
      transition: transform 0.2s ease-out;
    }
    
    .hover-lift:hover {
      transform: translateY(-2px);
    }
    
    .glass-effect {
      backdrop-filter: blur(10px);
      background: rgba(255, 255, 255, 0.8);
    }
  `}</style>
)

export default {
  AnimatedCard,
  AnimatedProgress,
  AnimatedCounter,
  PulseBadge,
  AnimatedButton,
  AchievementCard,
  AnimatedStats,
  AnimatedActivityList,
  AnimatedFeedback,
  PageTransition,
  AnimationStyles
}

