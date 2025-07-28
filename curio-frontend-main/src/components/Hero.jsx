import React from 'react'
import { Button } from '@/components/ui/button.jsx'
import { ArrowRight, Brain, Target, Zap } from 'lucide-react'

const Hero = ({ onNavigate }) => {
  return (
    <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Educação Adaptativa
            <span className="text-blue-600 block">Powered by AI</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Plataforma educacional revolucionária que combina as melhores práticas da Holanda, 
            Estônia e Singapura com inteligência artificial para personalizar o aprendizado de cada estudante.
          </p>
          
      <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
        <Button
          size="lg"
          className="text-lg px-8 py-3"
          onClick={() => onNavigate('dashboard')}
        >
          Começar Agora
          <ArrowRight className="ml-2 h-5 w-5" />
        </Button>
        <Button
          variant="outline"
          size="lg"
          className="text-lg px-8 py-3"
          onClick={() => onNavigate('singapore')}
        >
          Ver Demo
        </Button>
      </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Brain className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">IA Personalizada</h3>
              <p className="text-gray-600">
                Algoritmos avançados adaptam o conteúdo, ritmo e estilo de aprendizagem 
                para cada estudante individualmente.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Target className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Método de Singapura</h3>
              <p className="text-gray-600">
                Ensino de matemática através da progressão Concreto-Pictórico-Abstrato, 
                comprovadamente eficaz.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Zap className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Autonomia & Metacognição</h3>
              <p className="text-gray-600">
                Desenvolve pensamento crítico e habilidades de "aprender a aprender", 
                inspirado no sistema holandês.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero
