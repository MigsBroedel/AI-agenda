# Assistente de Agendamento com Google Calendar + LangChain

Um assistente inteligente que integra IA conversacional (LangChain + LangGraph) com o Google Calendar, permitindo consultar, criar e gerenciar eventos da sua agenda por comandos em linguagem natural.

---

## 🧠 O que é este projeto?

Este projeto é um assistente virtual que:
- Consulta sua agenda do Google Calendar
- Cria reuniões e eventos com data, hora e título
- Testa a conexão com sua conta Google
- Interage em linguagem natural usando IA (ReAct Agent)

Ideal para automatizar tarefas de agendamento e facilitar o gerenciamento de compromissos via comandos simples.

---

## 🚀 Funcionalidades

- **Consultar agenda**: Pergunte "ver agenda", "consultar agenda", "meus eventos" para listar seus próximos compromissos.
- **Marcar reuniões**: Comandos como "marcar reunião amanhã às 14h" ou "criar evento dia 20" criam eventos automaticamente.
- **Testar conexão**: Use "testar conexão" para verificar se a integração com o Google está funcionando.
- **Conversar com a IA**: Interaja livremente para tirar dúvidas ou pedir ações relacionadas à agenda.

---

## 📦 Tecnologias Utilizadas

- Python 3.10+
- LangChain (OpenAI)
- LangGraph
- Google Calendar API
- OAuth2
- python-dotenv

---

## 🔧 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/MigsBroedel/AI-agenda.git
cd AI-agenda
```

### 2. Crie o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte modelo:

```env
PPLX_API_KEY_API_KEY="sua_perplexity_api_key"

GOOGLE_CREDENTIALS_JSON='{
  "installed": {
    "client_id": "SEU_CLIENT_ID",
    "project_id": "SEU_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "SEU_CLIENT_SECRET",
    "redirect_uris": ["http://localhost"]
  }
}'
```


- **GOOGLE_CREDENTIALS_JSON**: Copie o JSON de credenciais do Google Cloud Console (OAuth2) para acesso ao Google Calendar.

### 3. Instale as dependências

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## ▶️ Como usar

1. Execute o assistente:

```bash
python main.py
```

2. Interaja pelo terminal, por exemplo:
   - "ver agenda"
   - "marcar reunião amanhã às 10h com João"
   - "testar conexão"

3. O assistente irá autenticar sua conta Google na primeira execução (abra o link e cole o código de autorização quando solicitado).

---

## 💡 Exemplos de comandos

- "Quais meus eventos amanhã?"
- "Criar evento dia 20 às 15h: Revisão de projeto"
- "Testar conexão"
- "Adicionar reunião com Maria na sexta às 9h"

---

## 🛠️ Para desenvolvedores

- O código principal está em `main.py`, com módulos auxiliares para autenticação (`auth.py`), integração com o Calendar (`calendar_agent.py`) e orquestração de fluxos (`orchestrator.py`).
- As credenciais são carregadas automaticamente do `.env`.
- O projeto utiliza LangChain para processamento de linguagem natural e integração com IA.

---
