import React, { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { ArrowRight, CheckCircle, Play, RotateCcw } from 'lucide-react'
import { Blocks, Image, Calculator } from 'lucide-react'

const SingaporeMethod = ({ onNavigate }) => {
  // Gera um problema aleatório para o estágio concreto (soma de duas dezenas/unidades)
  const getConcreteProblem = () => {
    const tensA = Math.floor(Math.random() * 5) + 1 // entre 1 e 5 dezenas
    const unitsA = Math.floor(Math.random() * 9)     // entre 0 e 8 unidades
    const tensB = Math.floor(Math.random() * 4) + 1
    const unitsB = Math.floor(Math.random() * 9)
    const sumTens = tensA + tensB
    const sumUnits = unitsA + unitsB
    const carried = sumUnits >= 10 ? 1 : 0
    const finalUnits = sumUnits % 10
    const total = (tensA * 10 + unitsA) + (tensB * 10 + unitsB)
    return {
      a: tensA * 10 + unitsA,
      b: tensB * 10 + unitsB,
      tensA,
      unitsA,
      tensB,
      unitsB,
      sumTens,
      sumUnits,
      carried,
      finalUnits,
      total
    }
  }

  const [currentStage, setCurrentStage] = useState('concrete')
  const [problemConcrete] = useState(getConcreteProblem)
  const [problemSolved, setProblemSolved] = useState(false)
  const [showAnswer, setShowAnswer] = useState({
    concrete: false,
    pictorial: false,
    abstract: false
  })

  // Dados para o bar model (pictórico)
  const pictorialProblem = {
    ana: 24,
    difference: 8,
    bruno: 16
  }

  // Problema abstrato fixo
  const abstractProblem = { question: '4x + 6 = 26', answer: 'x = 5' }

  const stages = {
    concrete: {
      title: 'Concreto',
      description: 'Some dezenas e unidades usando blocos de base 10 e cubos.',
      icon: Blocks,
      color: 'bg-green-100 text-green-800'
    },
    pictorial: {
      title: 'Pictórico',
      description: 'Use modelos de barras (bar model) para visualizar relações.',
      icon: Image,
      color: 'bg-blue-100 text-blue-800'
    },
    abstract: {
      title: 'Abstrato',
      description: 'Resolva equações de forma simbólica.',
      icon: Calculator,
      color: 'bg-purple-100 text-purple-800'
    }
  }

  // Etapa Concreta
  const ConcreteStage = () => (
    <div className="space-y-4">
      <p className="text-sm text-gray-700">
        Problema: {problemConcrete.a} + {problemConcrete.b}. Represente com blocos.
      </p>
      {/* Mostrar dezenas como barras e unidades como cubos */}
      <div className="flex space-x-8">
        {/* Primeiro número */}
        <div>
          <div className="mb-2 text-sm font-medium">Número A</div>
          <div className="flex space-x-1 mb-1">
            {[...Array(problemConcrete.tensA)].map((_, i) => (
              <div key={i} className="w-6 h-12 bg-green-300 border border-green-500"></div>
            ))}
          </div>
          <div className="flex space-x-1">
            {[...Array(problemConcrete.unitsA)].map((_, i) => (
              <div key={i} className="w-6 h-6 bg-green-200 border border-green-400"></div>
            ))}
          </div>
        </div>
        {/* Segundo número */}
        <div>
          <div className="mb-2 text-sm font-medium">Número B</div>
          <div className="flex space-x-1 mb-1">
            {[...Array(problemConcrete.tensB)].map((_, i) => (
              <div key={i} className="w-6 h-12 bg-blue-300 border border-blue-500"></div>
            ))}
          </div>
          <div className="flex space-x-1">
            {[...Array(problemConcrete.unitsB)].map((_, i) => (
              <div key={i} className="w-6 h-6 bg-blue-200 border border-blue-400"></div>
            ))}
          </div>
        </div>
      </div>
      {/* Explicação de reagrupamento visível após resolver */}
      <div className="mt-4">
        {!problemSolved ? (
          <Button onClick={() => setProblemSolved(true)}>Mostrar Processo</Button>
        ) : (
          <div className="space-y-2">
            <p className="text-sm text-gray-700">
              Some as unidades: {problemConcrete.unitsA} + {problemConcrete.unitsB} = {problemConcrete.sumUnits}.
              {problemConcrete.carried
                ? ` Como é maior que 10, trocamos 10 unidades por 1 dezena (carregamos ${problemConcrete.carried}).`
                : ` É menor que 10, então não há reagrupamento.`}
            </p>
            <p className="text-sm text-gray-700">
              Some as dezenas: {problemConcrete.tensA} + {problemConcrete.tensB} + {problemConcrete.carried} ={' '}
              {problemConcrete.sumTens + problemConcrete.carried}.
            </p>
            {!showAnswer.concrete ? (
              <Button variant="outline" size="sm" onClick={() => setShowAnswer({ ...showAnswer, concrete: true })}>
                Ver Resposta
              </Button>
            ) : (
              <Badge className="bg-green-100 text-green-800">
                <CheckCircle className="h-4 w-4 mr-1" /> Resultado: {problemConcrete.total}
              </Badge>
            )}
          </div>
        )}
      </div>
    </div>
  )

  // Etapa Pictórica
  const PictorialStage = () => (
    <div className="space-y-4">
      <p className="text-sm text-gray-700">
        Problema: Ana tem {pictorialProblem.ana} adesivos. Ela tem {pictorialProblem.difference} a mais que Bruno.
        Quantos adesivos Bruno tem?
      </p>
      {/* Modelo de barras */}
      <div className="space-y-2">
      <div className="flex items-center">
        <span className="w-20 text-sm mr-2">Ana:</span>
        <div className="h-8 bg-blue-300 w-64 relative">
          <span className="absolute inset-0 flex items-center justify-center text-sm text-black">
            24
          </span>
        </div>
      </div>
      <div className="flex items-center">
        <span className="w-20 text-sm mr-2">Bruno:</span>
        <div className="h-8 bg-green-300 w-48 relative">
          <span className="absolute inset-0 flex items-center justify-center text-sm text-black">
            ?
          </span>
        </div>
        <span className="ml-2 text-sm">+ 8</span>
      </div>
      </div>
      {!showAnswer.pictorial ? (
        <Button variant="outline" size="sm" onClick={() => setShowAnswer({ ...showAnswer, pictorial: true })}>
          Ver Resposta
        </Button>
      ) : (
        <Badge className="bg-blue-100 text-blue-800 flex items-center">
          <CheckCircle className="h-4 w-4 mr-1" /> Bruno tem {pictorialProblem.bruno}
        </Badge>
      )}
    </div>
  )

  // Etapa Abstrata
  const AbstractStage = () => (
    <div className="space-y-4">
      <p className="text-sm text-gray-700">Resolva a equação: {abstractProblem.question}</p>
      {!showAnswer.abstract ? (
        <Button variant="outline" size="sm" onClick={() => setShowAnswer({ ...showAnswer, abstract: true })}>
          Ver Resposta
        </Button>
      ) : (
        <Badge className="bg-purple-100 text-purple-800 flex items-center">
          <CheckCircle className="h-4 w-4 mr-1" /> {abstractProblem.answer}
        </Badge>
      )}
      <div className="mt-4 text-sm text-gray-700">
        Explicação:  
        <pre>{`
4x + 6 = 26
4x + 6 - 6 = 26 - 6
4x = 20
4x ÷ 4 = 20 ÷ 4
x = 5
        `}</pre>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Cabeçalho */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-curio-dark mb-4">Método de Singapura</h1>
          <p className="text-xl text-curio-medium max-w-3xl mx-auto">
            Aprenda matemática com a progressão Concreto→Pictórico→Abstrato, baseada no método de Singapura.
          </p>
        </div>

        {/* Navegação entre etapas */}
        <div className="flex justify-center mb-8">
          <div className="flex items-center space-x-4 bg-white p-2 rounded-lg shadow-sm border">
            {Object.entries(stages).map(([key, stage], index) => (
              <div key={key} className="flex items-center">
                <Button
                  variant={currentStage === key ? 'default' : 'ghost'}
                  onClick={() => {
                    setCurrentStage(key)
                    setProblemSolved(false)
                    setShowAnswer({ ...showAnswer, [key]: false })
                  }}
                  className="flex items-center space-x-2"
                >
                  <stage.icon className="h-4 w-4" />
                  <span>{stage.title}</span>
                </Button>
                {index < Object.keys(stages).length - 1 && (
                  <ArrowRight className="h-4 w-4 text-gray-400 mx-2" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Conteúdo da etapa atual */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {React.createElement(stages[currentStage].icon, { className: 'h-6 w-6' })}
                <CardTitle className="text-2xl">Estágio {stages[currentStage].title}</CardTitle>
                <Badge className={stages[currentStage].color}>Ativo</Badge>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setProblemSolved(false)
                  setShowAnswer({ ...showAnswer, [currentStage]: false })
                }}
              >
                <RotateCcw className="h-4 w-4 mr-2" /> Reiniciar
              </Button>
            </div>
            <CardDescription className="text-lg">
              {stages[currentStage].description}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {currentStage === 'concrete' && <ConcreteStage />}
            {currentStage === 'pictorial' && <PictorialStage />}
            {currentStage === 'abstract' && <AbstractStage />}
          </CardContent>
        </Card>

        {/* Próximos Passos */}
        <Card>
          <CardHeader>
            <CardTitle>Pronto para Praticar?</CardTitle>
            <CardDescription>
              Continue sua jornada com exercícios personalizados baseados no Método de Singapura
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button size="lg" onClick={() => onNavigate('problem')}>
                <Play className="h-4 w-4 mr-2" /> Começar Exercícios
              </Button>
              <Button
                variant="outline"
                size="lg"
                onClick={() => {
                  setCurrentStage('pictorial')
                  setProblemSolved(false)
                  setShowAnswer({ ...showAnswer, pictorial: false })
                }}
              >
                Ver Mais Exemplos
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default SingaporeMethod
