import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Textarea } from '@/components/ui/textarea.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Loader2, CheckCircle, XCircle, Lightbulb } from 'lucide-react';

const API_BASE_URL = 'https://curio-backend-1.onrender.com/api';

const ProblemOfTheDay = () => {
  const [problem, setProblem] = useState(null);
  const [answer, setAnswer] = useState('');
  const [submissionResult, setSubmissionResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [hint, setHint] = useState(null);
  const [showingHint, setShowingHint] = useState(false);

  useEffect(() => {
    fetchProblem();
  }, []);

  const fetchProblem = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/problems/today`);
      const data = await response.json();
      if (data.success) {
        setProblem(data.problem);
        setAnswer('');
        setSubmissionResult(null);
        setHint(null);
        setShowingHint(false);
      } else {
        console.error('Erro ao buscar problema:', data.error);
      }
    } catch (error) {
      console.error('Erro de rede ao buscar problema:', error);
      useFallbackProblem();
    } finally {
      setLoading(false);
    }
  };

  const useFallbackProblem = () => {
    const fallbackProblem = {
      id: 'fallback-1',
      title: 'Divisão de Frutas',
      description: 'Maria tem 24 maçãs e quer dividir igualmente entre seus 6 amigos. Quantas maçãs cada amigo receberá?',
      category: 'Divisão',
      difficulty: 'Fácil',
      resources: JSON.stringify(['Use a divisão', 'Pense em distribuir igualmente']),
      answer: '4' // Resposta para verificação local
    };
    setProblem(fallbackProblem);
  };

  
  const handleSubmit = async () => {
    if (!problem || !answer.trim()) return;

    setSubmitting(true);

  if (problem.id && problem.id.toString().startsWith('fallback')) {
    // Verificação local
    const isCorrect = answer.trim() === problem.answer;
    setSubmissionResult({
      success: true,
      is_correct: isCorrect,
      feedback: isCorrect ? 
        'Parabéns! Você acertou! Cada amigo receberá 4 maçãs.' : 
        'Tente novamente. Lembre-se: dividir é distribuir igualmente.'
    });
    setSubmitting(false);
    return;
  }
      
    try {
      const response = await fetch(`${API_BASE_URL}/problems/${problem.id}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          student_id: 1, // Hardcoded for demo, replace with actual student ID
          answer: answer,
          time_spent: 0, // Placeholder, could be calculated
        }),
      });
      const data = await response.json();
      if (data.success) {
        setSubmissionResult(data);
      } else {
        console.error('Erro ao submeter resposta:', data.error);
      }
    } catch (error) {
      console.error('Erro de rede ao submeter resposta:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const fetchHint = async () => {
    if (!problem) return;
    if (problem.id && problem.id.toString().startsWith('fallback')) {
    setHint('Pense assim: Se Maria tem 24 maçãs e 6 amigos, quantas maçãs cada um recebe? É só dividir 24 por 6!');
    setShowingHint(true);
    return;
  }    
    setShowingHint(true);
    try {
      const response = await fetch(`${API_BASE_URL}/problems/${problem.id}/hint`);
      const data = await response.json();
      if (data.success) {
        setHint(data.hint);
      } else {
        console.error('Erro ao buscar dica:', data.error);
      }
    } catch (error) {
      console.error('Erro de rede ao buscar dica:', error);
    } 
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-50">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-700">Carregando problema do dia...</span>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen bg-gray-50 text-red-600">
        <XCircle className="h-12 w-12 mb-4" />
        <p className="text-lg">Não foi possível carregar o problema do dia. Tente novamente mais tarde.</p>
        <Button onClick={fetchProblem} className="mt-4">Tentar Novamente</Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-3xl font-bold text-gray-900 mb-2">
              Problema do Dia: {problem.title}
            </CardTitle>
            <CardDescription className="text-lg text-gray-600">
              <Badge variant="secondary" className="mr-2">{problem.category}</Badge>
              <Badge variant="outline">Dificuldade: {problem.difficulty}</Badge>
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-gray-800 whitespace-pre-line leading-relaxed">
              {problem.description}
            </p>
            
            {problem.resources && (
              <div className="mt-4">
                <h4 className="font-semibold text-gray-700">Recursos Sugeridos:</h4>
                <ul className="list-disc list-inside text-gray-600">
                  {JSON.parse(problem.resources).map((res, index) => (
                    <li key={index}>{res}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="mt-6">
              <h4 className="font-semibold text-gray-700 mb-2">Sua Resposta:</h4>
              <Textarea
                placeholder="Digite sua solução aqui..."
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                rows={8}
                className="w-full"
                disabled={submitting || (submissionResult && submissionResult.success)}
              />
              <div className="flex justify-between items-center mt-4">
                <Button 
                  onClick={handleSubmit} 
                  disabled={submitting || !answer.trim() || (submissionResult && submissionResult.success)}
                >
                  {submitting ? (
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  ) : (
                    <CheckCircle className="h-4 w-4 mr-2" />
                  )}
                  {submitting ? 'Enviando...' : 'Enviar Resposta'}
                </Button>
                <Button 
                  variant="outline" 
                  onClick={fetchHint} 
                  disabled={showingHint || (submissionResult && submissionResult.success)}
                >
                  <Lightbulb className="h-4 w-4 mr-2" />
                  {showingHint ? 'Dica Carregada' : 'Pedir Dica'}
                </Button>
              </div>
            </div>

            {hint && (
              <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 className="font-semibold text-yellow-800 flex items-center">
                  <Lightbulb className="h-5 w-5 mr-2" /> Dica:
                </h4>
                <p className="text-yellow-700 mt-2">{hint}</p>
              </div>
            )}

            {submissionResult && submissionResult.success && (
              <div className={`mt-4 p-4 rounded-lg ${submissionResult.is_correct ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                <h4 className="font-semibold flex items-center mb-2">
                  {submissionResult.is_correct ? (
                    <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                  ) : (
                    <XCircle className="h-5 w-5 text-red-600 mr-2" />
                  )}
                  Sua resposta está {submissionResult.is_correct ? 'correta!' : 'incorreta.'}
                </h4>
                <p className="text-gray-800">{submissionResult.feedback}</p>
              </div>
            )}

            {submissionResult && !submissionResult.success && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <h4 className="font-semibold text-red-800">Erro na Submissão:</h4>
                <p className="text-red-700">{submissionResult.error}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProblemOfTheDay;


