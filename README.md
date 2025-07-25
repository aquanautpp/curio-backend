# Curió Backend - API Flask

Plataforma educacional adaptativa K-12 com inteligência artificial e implementação do Método de Singapura.

## 🚀 Deploy no Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 📋 Características

- **API RESTful completa** com Flask
- **Sistema de IA** para personalização de aprendizagem
- **Método de Singapura** (CPA - Concreto-Pictórico-Abstrato)
- **Banco de dados** SQLite/PostgreSQL
- **Autenticação** preparada para JWT
- **CORS** configurado para frontend

## 🛠️ Instalação Local

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/curio-backend.git
cd curio-backend
```

2. **Crie ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python src/main.py
```

A API estará disponível em `http://localhost:5000`

## 🌐 Deploy no Render

### Configuração Automática

1. **Fork este repositório** para sua conta GitHub
2. **Conecte ao Render**: https://render.com
3. **Crie um novo Web Service**
4. **Conecte seu repositório GitHub**
5. **Configure as variáveis**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Environment**: `Python 3`

### Variáveis de Ambiente (Opcional)

```bash
# Para produção com PostgreSQL
DATABASE_URL=postgresql://usuario:senha@host:porta/database
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_aqui
```

## 📚 Endpoints da API

### Usuários
- `GET /api/users` - Listar usuários
- `POST /api/users` - Criar usuário
- `GET /api/users/<id>` - Obter usuário específico

### Estudantes
- `GET /api/students` - Listar estudantes
- `POST /api/students` - Criar estudante
- `GET /api/students/<id>` - Obter estudante específico

### Conteúdo Educacional
- `GET /api/content` - Listar conteúdo
- `POST /api/content` - Criar conteúdo
- `GET /api/content/<id>` - Obter conteúdo específico

### IA e Personalização
- `POST /api/ai/simple/analyze/<student_id>` - Análise de perfil do estudante
- `GET /api/ai/simple/recommend/<student_id>` - Recomendações personalizadas
- `GET /api/ai/simple/learning-path/<student_id>/<subject>` - Caminho de aprendizagem
- `GET /api/ai/simple/dashboard-data/<student_id>` - Dados para dashboard

## 🏗️ Estrutura do Projeto

```
curio-backend/
├── src/
│   ├── main.py              # Aplicação principal
│   ├── models/              # Modelos de dados
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── teacher.py
│   │   ├── content.py
│   │   ├── progress.py
│   │   └── ai_personalization.py
│   ├── routes/              # Rotas da API
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── content.py
│   │   ├── ai_personalization.py
│   │   └── ai_simple.py
│   ├── static/              # Arquivos estáticos (frontend build)
│   └── database/            # Banco de dados SQLite
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## 🤖 Sistema de IA

### Funcionalidades Implementadas

- **Análise de Perfil**: Detecta estilo de aprendizagem, ritmo e preferências
- **Personalização**: Adapta conteúdo baseado no perfil do estudante
- **Recomendações**: Sugere próximas atividades e recursos
- **Caminhos de Aprendizagem**: Gera sequências otimizadas de conteúdo
- **Método de Singapura**: Implementa progressão CPA automaticamente

### Algoritmos

- Análise comportamental de aprendizagem
- Detecção de padrões de performance
- Recomendação baseada em similaridade
- Predição de dificuldades
- Otimização de ritmo de aprendizagem

## 📖 Método de Singapura

A plataforma implementa o método CPA (Concreto-Pictórico-Abstrato):

1. **Concreto**: Manipulação de objetos físicos/virtuais
2. **Pictórico**: Representações visuais e diagramas
3. **Abstrato**: Símbolos e equações matemáticas

## 🔧 Desenvolvimento

### Adicionando Novos Endpoints

1. Crie o modelo em `src/models/`
2. Adicione as rotas em `src/routes/`
3. Registre o blueprint em `src/main.py`
4. Atualize a documentação

### Testando Localmente

```bash
# Testar endpoints
curl http://localhost:5000/api/users

# Testar IA
curl -X POST http://localhost:5000/api/ai/simple/analyze/1

# Testar recomendações
curl http://localhost:5000/api/ai/simple/recommend/1
```

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de importação**: Verifique se todas as dependências estão instaladas
2. **Banco não criado**: O banco SQLite é criado automaticamente na primeira execução
3. **CORS Error**: Verifique se o frontend está na lista de origens permitidas

### Logs

Os logs da aplicação são exibidos no console. No Render, acesse a aba "Logs" do seu serviço.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação da API
- Verifique os logs de erro

---

**Curió** - Transformando a educação brasileira através da tecnologia inteligente. 🇧🇷✨
