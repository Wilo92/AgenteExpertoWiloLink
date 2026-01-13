from Agents.workflow import run_agents_workflow
import os
import requests
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import BaseModel
from typing import Dict, Any

load_dotenv()

app = FastAPI(
    title="Microservicio de Agentes con FastAPI",
    description="Microservicio con memoria persistente por sesión de usuario.",
)
security = HTTPBearer()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        
        "https://agent.wilolink.online"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ----------- SCHEMA ----------
class ConsultaInput(BaseModel):
    consulta: str

def obtener_usuario_laravel(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    # URL directa a la ruta de web.php que ya probamos
    url_validacion = "https://wilolink.online/user-check-test"

    try:
        response = requests.get(
            url_validacion,
            headers={
                # IMPORTANTE: Laravel en web.php a veces ignora el Bearer token
                # si no tiene la cookie de sesión. 
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            timeout=10
        )
        # Si Laravel responde 401, es porque no reconoce el token en la ruta web
        if response.status_code != 200:
            print(f"Laravel rechazó el token: {response.status_code}")
            raise HTTPException(status_code=401, detail="Sesión no reconocida")

        return response.json()

    except Exception as e:
        print(f"Error al validar token: {e}")
        raise HTTPException(
            status_code=401,
            detail="No se pudo validar el token con Laravel"
        )


# ----------- ENDPOINT ----------
@app.post("/api/v1/agentes/consulta", response_model=Dict[str, Any])
async def ejecutar_agentes(
    data: ConsultaInput,
    usuario: Dict = Depends(obtener_usuario_laravel)
):
    if not data.consulta:
        raise HTTPException(status_code=400, detail="La consulta está vacía")

    try:
        user_id_real = str(usuario["id"])
        user_name = usuario["name"]

        print(f"Usuario {user_name} (ID: {user_id_real}) consulta agentes")

        resultados = run_agents_workflow(
            data.consulta,
            user_id_real
        )

        return {
            "status": "success",
            "user": {
                "id": user_id_real,
                "name": user_name
            },
            "consulta_original": data.consulta,
            "ciberseguridad_reporte": resultados.get("ciberseguridad_reporte"),
            "software_reporte": resultados.get("software_reporte"),
        }

    except Exception as e:
        print(f"Error workflow agentes: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/api/v1/user-info")
async def info_usuario(
    usuario: Dict = Depends(obtener_usuario_laravel)
):
    return {
        "id": usuario["id"],
        "name": usuario["name"],
        "email": usuario["email"]
    }
