import chainlit as cl
from chainlit import Message
from langchain_core.messages import HumanMessage, AIMessage
from orchestrator import ana_conversa
from calendar_agent import executar_acao

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await Message(
        content="Oi! Sou a Ana, recepcionista da Clínica Saúde Total 😊 Como posso te ajudar hoje?"
    ).send()

@cl.on_message
async def main(message: Message):
    history = cl.user_session.get("history", [])

    # adiciona mensagem do usuário
    history.append(HumanMessage(content=message.content))
    cl.user_session.set("history", history)

    # chama Ana com histórico
    decisao = await ana_conversa(history)

    texto_paciente = decisao.get("mensagem_para_paciente", "")
    acao = decisao.get("acao", "nenhuma")
    dados = decisao.get("dados") or {}

    # resposta da Ana
    await Message(content=texto_paciente).send()
    history.append(AIMessage(content=texto_paciente))
    cl.user_session.set("history", history)

    # ação de agenda, se houver
    if acao != "nenhuma":
        resultado_agenda = await executar_acao(acao, dados)
        await Message(content=resultado_agenda).send()
        history.append(AIMessage(content=resultado_agenda))
        cl.user_session.set("history", history)
