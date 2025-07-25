import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'

// Componentes principais
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import LoadingScreen from './components/LoadingScreen'
import NotificationSystem from './components/NotificationSystem'

// Páginas/Seções
import Dashboard from './pages/Dashboard'
import Mathematics from './pages/Mathematics'
import Science from './pages/Science'
import SingaporeMethod from './pages/SingaporeMethod'
import ProblemOfDay from './pages/ProblemOfDay'
import AITutor from './pages/AITutor'
import Progress from './pages/Progress'
import ContentExplorer from './pages/ContentExplorer'

// Configuração da API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://curio-backend.onrender.com/api'

function App() {
  const [loading, setLoading] = useState(true)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [notifications, setNotifications] = useState([])
  const [currentUser] = useState({
    name: 'Victor Pires',
    grade: '7º Ano',
    level: 13,
    points: 1250,
    streak: 7
  })

  // Configuração das seções/páginas
  const sections = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      path: '/',
      component: Dashboard,
      icon: 'Home',
      description: 'Visão geral do progresso'
    },
    {
      id: 'mathematics',
      name: 'Matemática',
      path: '/matematica',
      component: Mathematics,
      icon: 'Calculator',
      description: 'Exercícios e método CPA'
    },
    {
      id: 'science',
      name: 'Ciências',
      path: '/ciencias',
      component: Science,
      icon: 'Microscope',
      description: 'Experimentos e descobertas'
    },
    {
      id: 'singapore',
      name: 'Método Singapura',
      path: '/singapura',
      component: SingaporeMethod,
      icon: 'Brain',
      description: 'Aprendizado estruturado'
    },
    {
      id: 'content',
      name: 'Explorar Conteúdo',
      path: '/conteudo',
      component: ContentExplorer,
      icon: 'BookOpen',
      description: 'Biblioteca educacional'
    },
    {
      id: 'problem',
      name: 'Problema do Dia',
      path: '/problema',
      component: ProblemOfDay,
      icon: 'Target',
      description: 'Desafio diário'
    },
    {
      id: 'tutor',
      name: 'Tutor de IA',
      path: '/tutor',
      component: AITutor,
      icon: 'MessageCircle',
      description: 'Converse com Curió'
    },
    {
      id: 'progress',
      name: 'Progresso',
      path: '/progresso',
      component: Progress,
      icon: 'Trophy',
      description: 'Conquistas e estatísticas'
    }
  ]

  // Sistema de notificações
  const addNotification = (message, type = 'info', duration = 5000) => {
    const id = Date.now() + Math.random()
    const notification = { id, message, type, timestamp: new Date() }
    
    setNotifications(prev => [...prev, notification])
    
    if (duration > 0) {
      setTimeout(() => {
        removeNotification(id)
      }, duration)
    }
  }

  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  // Inicialização da aplicação
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Simular carregamento inicial
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // Verificar conectividade com API
        try {
          const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`)
          if (response.ok) {
            console.log('✅ Conectado ao backend Curió')
          }
        } catch (error) {
          console.warn('⚠️ Backend não disponível, usando modo offline')
        }
        
        setLoading(false)
        
        // Notificação de boas-vindas
        setTimeout(() => {
          addNotification(`Bem-vindo de volta, ${currentUser.name}! 🐦`, 'success')
        }, 500)
        
      } catch (error) {
        console.error('Erro na inicialização:', error)
        setLoading(false)
        addNotification('Erro ao carregar a plataforma', 'error')
      }
    }

    initializeApp()
  }, [currentUser.name])

  // Controle do sidebar
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen)
  const closeSidebar = () => setSidebarOpen(false)

  if (loading) {
    return <LoadingScreen />
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex">
        {/* Sidebar */}
        <Sidebar
          sections={sections}
          isOpen={sidebarOpen}
          onClose={closeSidebar}
          currentUser={currentUser}
        />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col lg:ml-64">
          {/* Header */}
          <Header
            onMenuClick={toggleSidebar}
            currentUser={currentUser}
            onNotification={addNotification}
          />

          {/* Page Content */}
          <main className="flex-1 overflow-auto">
            <div className="container mx-auto px-4 py-6 max-w-7xl">
              <Routes>
                {sections.map(section => (
                  <Route
                    key={section.id}
                    path={section.path}
                    element={
                      <section.component
                        user={currentUser}
                        onNotification={addNotification}
                        apiBaseUrl={API_BASE_URL}
                      />
                    }
                  />
                ))}
                {/* Redirect para dashboard se rota não encontrada */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </div>
          </main>
        </div>

        {/* Overlay para mobile */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            onClick={closeSidebar}
          />
        )}

        {/* Sistema de Notificações */}
        <NotificationSystem
          notifications={notifications}
          onRemove={removeNotification}
        />
      </div>
    </Router>
  )
}

export default App

