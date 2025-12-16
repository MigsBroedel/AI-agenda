# calendar_agent.py
from datetime import datetime, timedelta
from langchain_google_community import CalendarToolkit
from langchain_google_community.calendar.utils import (
    get_google_credentials,
    build_resouce_service,
)
from datetime import datetime, timedelta
from typing import Dict, Any

creds = get_google_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/calendar"],
    client_secrets_file="credentials.json",
)
api_resource = build_resouce_service(credentials=creds)
toolkit = CalendarToolkit(api_resource=api_resource)
calendar_tools = toolkit.get_tools()  # [0]=CreateEvent, [1]=SearchEvents etc. [web:9]

create_event_tool = calendar_tools[0]
search_events_tool = calendar_tools[1]

def buscar_horarios(data: str, duracao_min: int = 30) -> str:
    """Retorna alguns horários livres em data YYYY-MM-DD (placeholder)."""
    # TODO: usar search_events_tool para checar conflitos reais [web:18]
    return f"Tenho alguns horários em {data}: 09:00, 10:30 e 14:00. Qual prefere?"

def criar_evento(nome: str, data: str, hora: str, duracao_min: int, servico: str) -> str:
    """Cria um evento no Google Calendar para o paciente."""
    # data = "2025-12-17", hora = "09:00"
    start_dt = datetime.fromisoformat(f"{data}T{hora}:00")
    end_dt = start_dt + timedelta(minutes=duracao_min)

    # Formato exigido pelo CreateEvent: "%Y-%m-%d %H:%M:%S" [web:18]
    start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

    _ = create_event_tool.invoke(
        {
            "summary": f"Consulta - {servico} - {nome}",
            "start_datetime": start_str,
            "end_datetime": end_str,
            "timezone": "America/Sao_Paulo",
        }
    )

    return f"✅ Agendei {servico} para {nome} em {data} às {hora}."

async def executar_acao(acao: str, dados: Dict[str, Any]) -> str:
    if acao == "consultar_horarios":
        return buscar_horarios(dados["data"], dados.get("duracao_min", 30))
    elif acao == "criar_agendamento":
        return criar_evento(
            nome=dados["nome"],
            data=dados["data"],
            hora=dados["hora"],
            duracao_min=dados.get("duracao_min", 30),
            servico=dados["servico"],
        )
    else:
        return "Nenhuma ação na agenda foi executada."
