// src/App.jsx
import { useState } from 'react'
import Hero from './components/Hero.jsx'
import Dashboard from './components/Dashboard.jsx'
import SingaporeMethod from './components/SingaporeMethod.jsx'
import ProblemOfTheDay from './components/ProblemOfTheDay.jsx'
import AITutorChat from './components/AITutorChat.jsx'
import { Home, Trophy, Brain, Target, MessageCircle, X, Menu } from 'lucide-react'

function App () {
  // Seção ativa da aplicação (dashboard por padrão)
  const [activeSection, setActiveSection] = useState('dashboard')
  // Controlo da sidebar no mobile
  const [sidebarOpen, setSidebarOpen] = useState(false)

  // Definição das seções e ícones correspondentes
const sections = [
  {
    id: 'hero',
    name: 'Início',
    icon: Home,
    component: () => <Hero onNavigate={setActiveSection} />
  },
  {
    id: 'dashboard',
    name: 'Dashboard',
    icon: Trophy,
    component: () => <Dashboard onNavigate={setActiveSection} />
  },
  {
    id: 'singapore',
    name: 'Método Singapura',
    icon: Brain,
    component: () => <SingaporeMethod onNavigate={setActiveSection} />
  },
  {
    id: 'problem',
    name: 'Problema do Dia',
    icon: Target,
    component: ProblemOfTheDay
  },
  {
    id: 'tutor',
    name: 'Tutor de IA',
    icon: MessageCircle,
    component: AITutorChat
  }
]

  // Encontra o componente atual a partir da seção selecionada
  const CurrentComponent =
    sections.find(s => s.id === activeSection)?.component || Dashboard

  // Renderização principal
  return (
    <div className='flex h-screen'>
      {/* Sidebar visível em telas médias/grandes (≥640px) */}
      <aside className='hidden sm:flex flex-col w-60 bg-gray-100 border-r'>
        <div className='p-4 text-xl font-bold'>Curió</div>
        <nav className='flex-1 overflow-y-auto'>
          {sections.map(section => {
            const Icon = section.icon
            const active = activeSection === section.id
            return (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`flex items-center p-4 w-full text-left hover:bg-gray-200 ${
                  active ? 'bg-gray-200 font-semibold' : ''
                }`}
              >
                <Icon className='h-5 w-5 mr-2' />
                {section.name}
              </button>
            )
          })}
        </nav>
        {/* Informações básicas do usuário na base da sidebar */}
        <div className='p-4 border-t text-sm'>
          <div className='font-semibold'>Victor Pires</div>
          <div className='text-gray-500'>7º Ano</div>
        </div>
      </aside>

      {/* Overlay + sidebar para mobile */}
      {sidebarOpen && (
        <div className='fixed inset-0 z-40 sm:hidden flex'>
          {/* fundo escuro translúcido */}
          <div
            className='absolute inset-0 bg-black/50'
            onClick={() => setSidebarOpen(false)}
          />
          {/* painel lateral */}
          <aside className='relative z-50 w-60 bg-gray-100 h-full shadow-xl'>
            <div className='flex items-center justify-between p-4'>
              <span className='text-xl font-bold'>Curió</span>
              <button onClick={() => setSidebarOpen(false)}>
                <X className='h-5 w-5' />
              </button>
            </div>
            {sections.map(section => {
              const Icon = section.icon
              const active = activeSection === section.id
              return (
                <button
                  key={section.id}
                  onClick={() => {
                    setActiveSection(section.id)
                    setSidebarOpen(false)
                  }}
                  className={`flex items-center p-4 w-full text-left hover:bg-gray-200 ${
                    active ? 'bg-gray-200 font-semibold' : ''
                  }`}
                >
                  <Icon className='h-5 w-5 mr-2' />
                  {section.name}
                </button>
              )
            })}
          </aside>
        </div>
      )}

      {/* Conteúdo principal */}
      <main className='flex-1 flex flex-col overflow-y-auto'>
        {/* Cabeçalho com botão para abrir/fechar sidebar no mobile */}
        <header className='flex items-center justify-between px-4 py-3 border-b'>
          <button
            className='sm:hidden p-2'
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X className='h-5 w-5' /> : <Menu className='h-5 w-5' />}
          </button>
          <h1 className='text-lg font-semibold'>
            {sections.find(s => s.id === activeSection)?.name || 'Curió'}
          </h1>
          {/* Espaço reservado para possíveis ações do usuário (login, avatar etc.) */}
          <div className='flex items-center space-x-2'>
            <span className='hidden sm:inline'>Victor Pires</span>
          </div>
        </header>

        {/* Componente da seção ativa */}
        <div className='flex-1 p-4 overflow-y-auto'>
          <CurrentComponent />
        </div>
      </main>
    </div>
  )
}

export default App
