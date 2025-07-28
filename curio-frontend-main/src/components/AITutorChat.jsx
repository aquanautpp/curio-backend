import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Textarea } from '@/components/ui/textarea.jsx';
import { Loader2, Send, MessageSquare, User, Bot } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const AITutorChat = ({ studentId = 1, problemId = 1 }) => {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    startChatSession();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startChatSession = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/tutor/chat/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ student_id: studentId, problem_id: problemId }),
      });
      const data = await response.json();
      if (data.success) {
        setSessionId(data.session.id);
        setMessages([data.welcome_message]);
      } else {
        console.error('Erro ao iniciar sessão de chat:', data.error);
      }
    } catch (error) {
      console.error('Erro de rede ao iniciar sessão de chat:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !sessionId) return;

    setSending(true);
    const currentMessage = inputMessage;
    setInputMessage('');

    // Add student message to UI immediately
    setMessages(prevMessages => [...prevMessages, {
      sender: 'student',
      message: currentMessage,
      message_type: 'text',
      timestamp: new Date().toISOString(),
    }]);

    try {
      const response = await fetch(`${API_BASE_URL}/tutor/chat/${sessionId}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: currentMessage }),
      });
      const data = await response.json();
      if (data.success) {
        setMessages(prevMessages => [...prevMessages, data.tutor_response]);
      } else {
        console.error('Erro ao enviar mensagem:', data.error);
        // Revert student message or show error
        setMessages(prevMessages => prevMessages.filter(msg => msg.message !== currentMessage));
      }
    } catch (error) {
      console.error('Erro de rede ao enviar mensagem:', error);
      // Revert student message or show error
      setMessages(prevMessages => prevMessages.filter(msg => msg.message !== currentMessage));
    } finally {
      setSending(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-50">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-700">Iniciando chat com o tutor...</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-gray-900 flex items-center">
              <MessageSquare className="mr-2" /> Tutor de IA
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-96 overflow-y-auto border rounded-lg p-4 mb-4 bg-white flex flex-col space-y-4">
              {messages.map((msg, index) => (
                <div key={index} className={`flex ${msg.sender === 'student' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`flex items-start max-w-[70%] p-3 rounded-lg ${msg.sender === 'student' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}>
                    {msg.sender === 'tutor' && <Bot className="h-5 w-5 mr-2 flex-shrink-0" />}
                    <p className="break-words">{msg.message}</p>
                    {msg.sender === 'student' && <User className="h-5 w-5 ml-2 flex-shrink-0" />}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
            <div className="flex space-x-2">
              <Textarea
                placeholder="Digite sua mensagem..."
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                  }
                }}
                rows={1}
                className="flex-grow"
                disabled={sending}
              />
              <Button onClick={sendMessage} disabled={sending || !inputMessage.trim()}>
                {sending ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AITutorChat;


