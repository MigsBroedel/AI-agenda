import os
import json
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS_JSON")

if not GOOGLE_CREDENTIALS:
    raise ValueError("❌ A variável GOOGLE_CREDENTIALS_JSON não está definida no .env")

# Salva o JSON em um arquivo físico que o Google usa
with open("credentials.json", "w") as f:
    json.dump(json.loads(GOOGLE_CREDENTIALS), f)

print("Credenciais carregadas do .env e salvas em credentials.json")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langgraph.prebuilt import create_react_agent

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import datetime
import pickle

llm = ChatOpenAI(
    model="openrouter/polaris-alpha",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
)

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0, open_browser=True)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


@tool("consultar_agenda_google")
def consultar_agenda_google(dias: int = 7):
    try:
        service = get_calendar_service()
        agora = datetime.datetime.utcnow()
        fim = agora + datetime.timedelta(days=dias)

        events_result = service.events().list(
            calendarId="primary",
            timeMin=agora.isoformat() + "Z",
            timeMax=fim.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        if not events:
            return f"📅 Nenhum evento encontrado nos próximos {dias} dias."

        texto = f"📅 Eventos nos próximos {dias} dias:\n\n"
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "Sem título")

            try:
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                data_formatada = dt.strftime("%d/%m/%Y %H:%M")
            except:
                data_formatada = start

            texto += f"📌 {summary}\n   🕐 {data_formatada}\n\n"

        return texto

    except Exception as e:
        return f"❌ Erro ao consultar agenda: {str(e)}"


@tool("marcar_reuniao_google")
def marcar_reuniao_google(data_hora: str, titulo: str = "Reunião", duracao_horas: int = 1):
    try:
        dt_inicio = datetime.datetime.strptime(data_hora, "%Y-%m-%d %H:%M")
        dt_fim = dt_inicio + datetime.timedelta(hours=duracao_horas)
    except Exception as e:
        return f"❌ Formato inválido. Use 'YYYY-MM-DD HH:MM'. Erro: {str(e)}"

    try:
        service = get_calendar_service()

        evento = {
            "summary": titulo,
            "start": {
                "dateTime": dt_inicio.isoformat(),
                "timeZone": "America/Sao_Paulo"
            },
            "end": {
                "dateTime": dt_fim.isoformat(),
                "timeZone": "America/Sao_Paulo"
            },
            "description": "Evento criado pelo assistente de agendamento"
        }

        evento_criado = service.events().insert(
            calendarId="primary",
            body=evento
        ).execute()

        return f"✅ Reunião marcada!\n📅 {titulo}\n🕐 {dt_inicio.strftime('%d/%m/%Y às %H:%M')}\n⏱️ {duracao_horas}h\n🔗 {evento_criado.get('htmlLink')}"

    except Exception as e:
        return f"❌ Erro ao marcar reunião: {str(e)}"


@tool("testar_conexao")
def testar_conexao():
    try:
        service = get_calendar_service()
        calendar = service.calendars().get(calendarId='primary').execute()
        return f"✅ Conexão OK!\n📧 Conta: {calendar.get('summary', 'N/A')}"
    except Exception as e:
        return f"❌ Erro na conexão: {str(e)}"


tools = [
    testar_conexao,
    consultar_agenda_google,
    marcar_reuniao_google
]

history = ChatMessageHistory()

prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente simpático que ajuda a marcar consultas e reuniões no Google Calendar.

Comandos:
- testar conexão
- ver agenda / consultar agenda
- marcar reunião

Sempre confirme os detalhes antes de marcar."""),
    ("placeholder", "{messages}"),
])

agent = create_react_agent(llm, tools, prompt=prompt)


def teste_rapido():
    print("🧪 Testando conexão...\n")
    print(testar_conexao.invoke({}))
    print("\n📅 Consultando agenda...\n")
    print(consultar_agenda_google.invoke({"dias": 7}))


def iniciar_assistente():
    print("🤖 Assistente iniciado!\n")

    while True:
        msg = input("Você: ")
        if msg.lower() in ["sair", "exit", "quit"]:
            print("👋 Até logo!")
            break

        try:
            result = agent.invoke({
                "messages": history.messages + [("user", msg)]
            })

            history.add_user_message(msg)
            history.add_ai_message(result["messages"][-1].content)

            print(f"\n🤖 IA: {result['messages'][-1].content}\n")

        except Exception as e:
            print(f"❌ Erro: {str(e)}\n")


print("\n" + "="*50)
teste_rapido()
