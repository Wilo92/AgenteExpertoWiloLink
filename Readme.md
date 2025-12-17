# 🤖 Microservicio de Agentes Inteligentes (FastAPI + LangGraph)

Este es un microservicio diseñado para orquestar agentes inteligentes especializados en **Ciberseguridad** y **Arquitectura de Software**. Utiliza **LangGraph** para el flujo de trabajo, **Gemini 1.5 Flash** como motor de lenguaje y **FastAPI** para la exposición de la API.

## 🚀 Características

* **Orquestación de Agentes:** Flujo secuencial donde un experto en seguridad analiza la consulta y un arquitecto de software propone la solución técnica basándose en ese análisis.
* **Memoria Persistente:** Implementación de `MemorySaver` para que los agentes recuerden el contexto de la conversación utilizando un `thread_id` (ID de usuario).
* **Validación de Datos:** Uso de Pydantic para asegurar que las entradas y salidas de la API sean correctas.
* **Documentación Automática:** Acceso a Swagger UI para pruebas rápidas.

## 🛠️ Tecnologías Utilizadas

* **Python 3.10+**
* **FastAPI:** Framework web de alto rendimiento.
* **LangGraph:** Para la creación de grafos de estado y agentes.
* **LangChain Google GenAI:** Integración con Google Gemini.
* **Pydantic:** Gestión de esquemas de datos.

## 📋 Requisitos Previos

1.  **Python instalado** (Verificar con `python --version`).
2.  **Google Gemini API Key:** Obtenla en [Google AI Studio](https://aistudio.google.com/).

## 🔧 Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-de-tu-repositorio>
    cd Microservicio_Agentes_FastAPI
    ```

2.  **Crear y activar el entorno virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # En Windows
    source venv/bin/activate # En Linux/Mac
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz y añade tu clave:
    ```env
    GEMINI_API_KEY="TU_CLAVE_AQUI"
    ```

## 🏃 Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload