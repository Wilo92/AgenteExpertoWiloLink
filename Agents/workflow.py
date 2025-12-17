import os
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv
import operator 

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") 

# Configuración del Modelo
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.2, 
    google_api_key=GOOGLE_API_KEY, 
)

# 1. DEFINICIÓN DEL ESTADO CON MEMORIA
class AgentState(TypedDict):
    consulta: str 
    reporte_ciberseguridad: str
    reporte_software: str
    # 'messages' guardará todo el historial acumulado
    messages: Annotated[List[BaseMessage], operator.add]

# --- NODO 1: CIBERSEGURIDAD ---
def nodo_ciberseguridad(state: AgentState):
    print("--- EJECUTANDO AGENTE CIBERSEGURIDAD ---")
    consulta = state['consulta']
    historial = state.get('messages', [])
    
    prompt = [
        SystemMessage(content="Eres un Experto en Ciberseguridad. Analiza riesgos. Revisa el historial para dar continuidad.")
    ]
    prompt.extend(historial) # Inyectamos memoria
    prompt.append(HumanMessage(content=f"Análisis de seguridad para: {consulta}"))
    
    response = llm.invoke(prompt)
    
    return {
        "reporte_ciberseguridad": response.content,
        "messages": [HumanMessage(content=consulta), response] 
    }

# --- NODO 2: SOFTWARE ---
def nodo_software(state: AgentState):
    print("--- EJECUTANDO AGENTE ARQUITECTURA ---")
    consulta = state['consulta']
    reporte_seguridad = state['reporte_ciberseguridad']
    historial = state.get('messages', [])
    
    prompt = [
        SystemMessage(content="Eres un Arquitecto de Software. Diseña soluciones basadas en el análisis de seguridad previo.")
    ]
    prompt.extend(historial)
    prompt.append(HumanMessage(content=f"Diseño para: {consulta}. Contexto de seguridad: {reporte_seguridad}"))
    
    response = llm.invoke(prompt)
    
    return {
        "reporte_software": response.content,
        "messages": [response]
    }

# 2. CONSTRUCCIÓN DEL GRAFO
def build_langgraph_workflow():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("ciberseguridad", nodo_ciberseguridad)
    workflow.add_node("software", nodo_software)
    
    workflow.set_entry_point("ciberseguridad")
    workflow.add_edge("ciberseguridad", "software")
    workflow.add_edge("software", END)
    
    # Checkpointer para persistencia en RAM
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

langgraph_app = build_langgraph_workflow()

# 3. FUNCIÓN DE EJECUCIÓN
def run_agents_workflow(consulta_usuario: str, user_id: str):
    config = {"configurable": {"thread_id": user_id}}
    
    initial_state = {
        "consulta": consulta_usuario,
        "reporte_ciberseguridad": "",
        "reporte_software": "",
        "messages": []
    }
    
    final_state = langgraph_app.invoke(initial_state, config=config)
    
    return {
        "ciberseguridad_reporte": final_state["reporte_ciberseguridad"],
        "software_reporte": final_state["reporte_software"],
    }