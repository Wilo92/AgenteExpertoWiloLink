from Agents.workflow import run_agents_workflow
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

load_dotenv()

app = FastAPI(
    title="Microservicio de Agentes con FastAPI",
    description="Microservicio con memoria persistente por sesión de usuario.",
)

# Esquema de entrada
class ConsultaInput(BaseModel):
    user_id: str = "usuario_por_defecto" 
    consulta: str

@app.post("/api/v1/agentes/consulta", response_model=Dict[str, Any])
async def ejecutar_agentes(data: ConsultaInput):
    if not data.consulta:
        raise HTTPException(status_code=400, detail="No existe una consulta")

    try:
        # Llamamos al workflow pasando el ID de usuario para la memoria
        resultados = run_agents_workflow(data.consulta, data.user_id)
        
        return {
            "status": "success",
            "ciberseguridad_reporte": resultados["ciberseguridad_reporte"],
            "software_reporte": resultados["software_reporte"],
            "user_id": data.user_id,
            "consulta_original": data.consulta
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))