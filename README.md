# Assistente de Agendamento com Google Calendar + LangChain

Este projeto é um assistente inteligente capaz de:

- Consultar sua agenda do Google Calendar  
- Marcar reuniões com horário e título  
- Verificar conexão com sua conta Google  
- Interagir em linguagem natural usando LangChain + LangGraph  

As credenciais são carregadas automaticamente através do arquivo `.env` — **nenhum upload manual é necessário**.

---

## 🚀 Funcionalidades

- **Consultar agenda** → “ver agenda”, “consultar agenda”, “meus eventos”
- **Marcar reuniões** → “marcar reunião amanhã às 14h”, “criar evento dia 20”
- **Testar conexão** → “testar conexão”
- **Conversar com a IA** usando ReAct Agent

---

## 📦 Tecnologias

- Python 3.10+
- LangChain OpenAI
- LangGraph
- Google Calendar API
- OAuth2
- python-dotenv

---

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/seuprojeto.git
cd seuprojeto

```

### 2. Gere o .env nesse modelo

```bash

OPENAI_API_KEY="sua_openai_api_key"

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