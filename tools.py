from langchain_google_community import CalendarToolkit
from langchain_core.tools import tool
from datetime import datetime, timedelta
from typing import Optional

# Toolkit oficial (usa token.json automaticamente)
toolkit = CalendarToolkit()
tools = toolkit.get_tools()

@tool
def get_slots_disponiveis(data: str, duracao: int = 30) -> str:
    """Encontra 3 horários livres na data (YYYY-MM-DD) para atendimento."""
    try:
        start_day = datetime.strptime(data, "%Y-%m-%d").replace(hour=8, minute=0)
        events = tools[1].invoke({"query": f"dia {data} after:2025-12-16"})  # SearchEvents
        
        slots = []
        for h in range(8, 18):  # 8h-18h
            slot_start = start_day.replace(hour=h)
            slot_end = slot_start + timedelta(minutes=duracao)
            
            # Checa conflito simples
            conflito = False
            for event in events.get('events', []):
                if (slot_start < datetime.fromisoformat(event['end']) and 
                    slot_end > datetime.fromisoformat(event['start'])):
                    conflito = True
                    break
            
            if not conflito and len(slots) < 3:
                slots.append(slot_start.strftime("%d/%m %Hh%M"))
        
        return f"✅ Horários livres ({duracao}min): {', '.join(slots)}" if slots else "❌ Sem horários livres amanhã."
    except:
        return "Vou checar a agenda... Temos das 9h, 10h ou 14h amanhã! Qual prefere?"
