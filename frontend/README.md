# Curió Frontend - React App

Interface de usuário da plataforma educacional adaptativa Curió, construída com React, Tailwind CSS e shadcn/ui.

## 🚀 Deploy no Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 📋 Características

- **Interface moderna e responsiva** com React 18
- **Design mobile-first** com Tailwind CSS
- **Componentes UI** com shadcn/ui
- **Navegação intuitiva** e experiência de usuário otimizada
- **Integração** com a API do backend Curió

## 🛠️ Instalação Local

### Pré-requisitos
- Node.js (versão 18 ou superior)
- pnpm (recomendado)

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/curio-frontend.git
cd curio-frontend
```

2. **Instale as dependências**
```bash
pnpm install
# ou npm install
# ou yarn install
```

3. **Execute a aplicação em modo de desenvolvimento**
```bash
pnpm run dev
# ou npm run dev
# ou yarn dev
```

A aplicação estará disponível em `http://localhost:5173` (ou outra porta, se 5173 estiver em uso).

## 🌐 Deploy no Render

### Configuração Automática

1. **Fork este repositório** para sua conta GitHub
2. **Conecte ao Render**: https://render.com
3. **Crie um novo Static Site**
4. **Conecte seu repositório GitHub**
5. **Configure as variáveis**:
   - **Build Command**: `pnpm install && pnpm run build`
   - **Publish Directory**: `dist`
   - **Root Directory**: (deixe em branco se o projeto estiver na raiz do repositório)

### Variáveis de Ambiente (Opcional)

Se o seu backend estiver hospedado em um URL diferente, você pode configurar a variável de ambiente `VITE_API_BASE_URL` no Render:

```bash
VITE_API_BASE_URL=https://curio-backend-1.onrender.com/api
```

## 🏗️ Estrutura do Projeto

```
curio-frontend/
├── public/                  # Arquivos estáticos públicos
├── src/
│   ├── assets/              # Imagens e outros assets
│   ├── components/          # Componentes React reutilizáveis
│   │   ├── Header.jsx
│   │   ├── Hero.jsx
│   │   ├── Dashboard.jsx
│   │   └── SingaporeMethod.jsx
│   ├── App.jsx              # Componente principal da aplicação
│   ├── main.jsx             # Ponto de entrada da aplicação
│   └── index.css            # Estilos globais
├── index.html               # Arquivo HTML principal
├── package.json             # Dependências e scripts do projeto
├── pnpm-lock.yaml           # Lock file do pnpm
├── tailwind.config.js       # Configuração do Tailwind CSS
├── vite.config.js           # Configuração do Vite
└── README.md               # Este arquivo
```

## 🔧 Desenvolvimento

### Adicionando Novos Componentes

1. Crie um novo arquivo `.jsx` em `src/components/`
2. Importe e use o componente em `src/App.jsx` ou em outros componentes

### Estilização

Utilizamos Tailwind CSS para estilização. Você pode adicionar classes diretamente no JSX ou criar arquivos CSS modulares.

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de dependências**: Execute `pnpm install` novamente
2. **API não conectada**: Verifique se o backend está rodando e se `VITE_API_BASE_URL` está configurado corretamente
3. **Página em branco**: Verifique os logs do navegador (F12) para erros JavaScript

### Logs

Os logs da aplicação em desenvolvimento são exibidos no terminal. No Render, acesse a aba "Logs" do seu serviço.

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
- Consulte a documentação da API do backend

---

**Curió** - O futuro da educação adaptativa no Brasil. 🇧🇷✨
