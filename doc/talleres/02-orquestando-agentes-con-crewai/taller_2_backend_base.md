# Taller 2- Infraestructura y Backend Base

---
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/56c7d9a1-7dfa-46b1-8fb5-6ca34c121c59" />


# FASE 1. PREPARACIÓN DEL PROYECTO BACKEND

---

## 1.1 Objetivo de la Fase

En esta fase se construirá la estructura inicial del backend de ScrumDev AI. El objetivo es preparar un proyecto organizado, versionado y listo para implementar microservicios usando FastAPI, Temporal, PostgreSQL, Redis y RabbitMQ.

El backend base no implementará todavía la inteligencia de agentes en profundidad. Esa parte se desarrollará en el Taller 3. Aquí se construye la infraestructura técnica mínima para que el sistema pueda recibir solicitudes, enrutar mensajes, iniciar workflows y preparar la comunicación entre servicios.

---

## 1.2 Crear Carpeta Principal del Proyecto

Crear una carpeta raíz para contener todos los componentes del sistema.

Ejecutar:

```bash
mkdir scrumdev-ai
cd scrumdev-ai
```

Verificar ubicación:

```bash
pwd
```

Resultado esperado:

```text
.../scrumdev-ai
```

---

## 1.3 Inicializar Repositorio Git

El proyecto debe versionarse desde el inicio para mantener trazabilidad de cambios y facilitar colaboración.

Ejecutar:

```bash
git init
```

Verificar:

```bash
git status
```

Resultado esperado:

```text
On branch main
```

---

## 1.4 Crear Archivo `.gitignore`

El archivo `.gitignore` evita subir al repositorio archivos sensibles o generados automáticamente.

Crear archivo:

```bash
touch .gitignore
```

Agregar:

```text
.env
.venv
__pycache__/
*.pyc
.DS_Store
.idea/
.vscode/
node_modules/
dist/
build/
```

---

## 1.5 Crear Estructura Base del Repositorio

La estructura del repositorio debe reflejar la arquitectura de microservicios. Cada servicio tendrá su propia carpeta, pero compartirá contratos y utilidades comunes mediante el módulo `shared`.

Ejecutar:

```bash
mkdir -p services/api-gateway/app
mkdir -p services/conversation-service/app
mkdir -p services/orchestrator-service/app
mkdir -p services/agent-runtime-service/app
mkdir -p services/jira-connector-service/app
mkdir -p services/git-connector-service/app
mkdir -p services/deploy-connector-service/app
mkdir -p services/policy-service/app
mkdir -p services/memory-service/app
mkdir -p services/audit-service/app

mkdir -p shared/config
mkdir -p shared/contracts
mkdir -p shared/events
mkdir -p shared/schemas
mkdir -p shared/clients
mkdir -p shared/security
mkdir -p shared/observability

mkdir -p temporal/workflows
mkdir -p temporal/activities
mkdir -p infra/postgres
mkdir -p infra/redis
mkdir -p infra/rabbitmq
mkdir -p infra/temporal
mkdir -p docs/architecture
mkdir -p docs/api
```

---

## 1.6 Verificar Estructura

Ejecutar:

```bash
tree -L 3
```

Si `tree` no está instalado, usar:

```bash
find . -maxdepth 3 -type d
```

Resultado esperado:

```text
services/
shared/
temporal/
infra/
docs/
```

---

# FASE 2. CONFIGURACIÓN DE POETRY Y DEPENDENCIAS

---

## 2.1 Objetivo de la Fase

En esta fase se configurará Poetry para administrar dependencias Python del backend. Poetry permite mantener un entorno reproducible, evitar conflictos entre librerías y separar dependencias de ejecución de dependencias de desarrollo.

Aunque el proyecto está organizado en microservicios, para este PMV se usará un archivo `pyproject.toml` raíz. Esto simplifica el aprendizaje y la replicación. En una fase posterior, cada microservicio podría tener su propio paquete independiente.

---

## 2.2 Inicializar Poetry

Ejecutar:

```bash
poetry init
```

Aceptar configuración interactiva básica.

Si se desea omitir la interacción:

```bash
poetry init --name scrumdev-ai --python "^3.11" --no-interaction
```

---

## 2.3 Instalar Dependencias Principales

Estas dependencias permiten construir APIs, conectar base de datos, manejar eventos, ejecutar workflows y preparar integración con agentes.

Ejecutar:

```bash
poetry add fastapi uvicorn pydantic pydantic-settings sqlalchemy asyncpg alembic redis aio-pika temporalio httpx python-jose passlib bcrypt structlog
```

---

## 2.4 Instalar Dependencias de Desarrollo

Estas herramientas permiten probar, formatear y validar el código antes de integrarlo.

Ejecutar:

```bash
poetry add --group dev pytest pytest-asyncio ruff black mypy
```

---

## 2.5 Explicación de Dependencias

| Librería | Función |
|---|---|
| `fastapi` | Framework para construir APIs HTTP. |
| `uvicorn` | Servidor ASGI para ejecutar FastAPI. |
| `pydantic` | Validación y serialización de datos. |
| `pydantic-settings` | Lectura de variables desde `.env`. |
| `sqlalchemy` | ORM y acceso a base de datos. |
| `asyncpg` | Driver asíncrono para PostgreSQL. |
| `alembic` | Migraciones de base de datos. |
| `redis` | Cache, sesiones y locks. |
| `aio-pika` | Cliente asíncrono para RabbitMQ. |
| `temporalio` | SDK Python para Temporal. |
| `httpx` | Cliente HTTP para comunicación entre servicios. |
| `python-jose` | Manejo de JWT. |
| `passlib` | Hashing seguro de contraseñas. |
| `bcrypt` | Algoritmo de hashing. |
| `structlog` | Logging estructurado. |
| `pytest` | Pruebas automatizadas. |
| `pytest-asyncio` | Pruebas de código asíncrono. |
| `ruff` | Linter rápido. |
| `black` | Formateador de código. |
| `mypy` | Verificación estática de tipos. |

---

## 2.6 Activar Entorno Virtual

Ejecutar:

```bash
poetry shell
```

Verificar Python usado por Poetry:

```bash
python --version
```

---

# FASE 3. CONFIGURACIÓN DE VARIABLES DE ENTORNO

---

## 3.1 Objetivo de la Fase

En esta fase se creará la configuración local del backend mediante variables de entorno. Esto permite separar configuración del código y mantener alineación con los principios 12-factor app.

El archivo `.env` contiene secretos reales y no debe subirse a Git. El archivo `.env.example` documenta las variables necesarias sin incluir credenciales.

---

## 3.2 Crear Archivo `.env.example`

Crear:

```bash
touch .env.example
```

Agregar:

```env
APP_ENV=local
APP_NAME=ScrumDev AI
APP_DEBUG=true

API_GATEWAY_HOST=0.0.0.0
API_GATEWAY_PORT=8080

CONVERSATION_SERVICE_URL=http://conversation-service:8001
ORCHESTRATOR_SERVICE_URL=http://orchestrator-service:8002
AGENT_RUNTIME_SERVICE_URL=http://agent-runtime-service:8003
JIRA_CONNECTOR_SERVICE_URL=http://jira-connector-service:8004
GIT_CONNECTOR_SERVICE_URL=http://git-connector-service:8005
DEPLOY_CONNECTOR_SERVICE_URL=http://deploy-connector-service:8006
POLICY_SERVICE_URL=http://policy-service:8007
MEMORY_SERVICE_URL=http://memory-service:8008
AUDIT_SERVICE_URL=http://audit-service:8009

DATABASE_URL=postgresql+asyncpg://scrumdev:scrumdev@postgres:5432/scrumdev_ai
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

TEMPORAL_HOST=temporal:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=scrumdev-ai-task-queue

SCRUMDEV_JIRA_BASE_URL=
SCRUMDEV_JIRA_EMAIL=
SCRUMDEV_JIRA_API_TOKEN=
SCRUMDEV_JIRA_PROJECT_KEY=

SCRUMDEV_GIT_PROVIDER=github
SCRUMDEV_GIT_TOKEN=
SCRUMDEV_GIT_OWNER=
SCRUMDEV_GIT_REPO=

SCRUMDEV_AI_PROVIDER=openai
SCRUMDEV_AI_API_KEY=
SCRUMDEV_AI_MODEL=gpt-5.5

SCRUMDEV_DEPLOY_PROVIDER=render
SCRUMDEV_DEPLOY_API_TOKEN=

JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
```

---

## 3.3 Crear Archivo `.env`

Crear una copia local:

```bash
cp .env.example .env
```

Editar `.env` y completar las credenciales obtenidas en el Taller 1.

---

## 3.4 Validar Seguridad del `.env`

Verificar que `.env` esté ignorado por Git:

```bash
git status
```

El archivo `.env` no debe aparecer como archivo listo para commit.

Si aparece, revisar `.gitignore`.

---

# FASE 4. CONFIGURACIÓN COMPARTIDA DEL BACKEND

---

## 4.1 Objetivo de la Fase

En esta fase se implementará una configuración centralizada para que todos los servicios lean variables de entorno de manera uniforme. Esto evita duplicación de código, reduce errores y permite cambiar configuración sin modificar la lógica del sistema.

---

## 4.2 Crear Archivo `shared/config/settings.py`

Crear archivo:

```bash
touch shared/config/settings.py
```

Agregar:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    app_name: str = "ScrumDev AI"
    app_debug: bool = True

    database_url: str
    redis_url: str
    rabbitmq_url: str

    temporal_host: str
    temporal_namespace: str = "default"
    temporal_task_queue: str

    conversation_service_url: str
    orchestrator_service_url: str
    agent_runtime_service_url: str
    jira_connector_service_url: str
    git_connector_service_url: str
    deploy_connector_service_url: str
    policy_service_url: str
    memory_service_url: str
    audit_service_url: str

    scrumdev_jira_base_url: str | None = None
    scrumdev_jira_email: str | None = None
    scrumdev_jira_api_token: str | None = None
    scrumdev_jira_project_key: str | None = None

    scrumdev_git_provider: str = "github"
    scrumdev_git_token: str | None = None
    scrumdev_git_owner: str | None = None
    scrumdev_git_repo: str | None = None

    scrumdev_ai_provider: str = "openai"
    scrumdev_ai_api_key: str | None = None
    scrumdev_ai_model: str = "gpt-5.5"

    scrumdev_deploy_provider: str | None = None
    scrumdev_deploy_api_token: str | None = None

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
```

---

## 4.3 Crear `__init__.py` en Módulos Compartidos

Ejecutar:

```bash
touch shared/__init__.py
touch shared/config/__init__.py
touch shared/contracts/__init__.py
touch shared/events/__init__.py
touch shared/schemas/__init__.py
```

---

## 4.4 Validar Carga de Configuración

Ejecutar:

```bash
python -c "from shared.config.settings import settings; print(settings.app_name)"
```

Resultado esperado:

```text
ScrumDev AI
```

---

# FASE 5. CONTRATOS Y EVENTOS BASE

---

## 5.1 Objetivo de la Fase

En esta fase se crearán contratos compartidos para que los microservicios puedan comunicarse de forma predecible. Los contratos son esenciales en microservicios porque reducen ambigüedad y permiten validar entradas y salidas.

---

## 5.2 Crear Contrato de Comando

Crear archivo:

```bash
touch shared/contracts/commands.py
```

Agregar:

```python
from pydantic import BaseModel
from typing import Optional, Dict, Any


class StartWorkflowCommand(BaseModel):
    project_key: str
    issue_key: Optional[str] = None
    user_id: str
    message: str
    correlation_id: Optional[str] = None


class AgentExecutionCommand(BaseModel):
    agent_name: str
    task_name: str
    input_data: Dict[str, Any]
    correlation_id: str
```

---

## 5.3 Crear Contrato de Respuesta

Crear archivo:

```bash
touch shared/contracts/responses.py
```

Agregar:

```python
from pydantic import BaseModel
from typing import Any, Optional


class ServiceResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    correlation_id: Optional[str] = None
```

---

## 5.4 Crear Modelo de Evento

Crear archivo:

```bash
touch shared/events/domain_events.py
```

Agregar:

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4


class DomainEvent(BaseModel):
    event_id: str = str(uuid4())
    event_type: str
    source_service: str
    correlation_id: str
    project_key: Optional[str] = None
    issue_key: Optional[str] = None
    payload: Dict[str, Any]
    occurred_at: datetime = datetime.utcnow()
```

---

## 5.5 Definir Eventos Iniciales

Crear archivo:

```bash
touch shared/events/event_types.py
```

Agregar:

```python
HUMAN_MESSAGE_RECEIVED = "HUMAN_MESSAGE_RECEIVED"
WORKFLOW_STARTED = "WORKFLOW_STARTED"
ISSUE_REFINEMENT_REQUESTED = "ISSUE_REFINEMENT_REQUESTED"
ARCHITECTURE_REQUESTED = "ARCHITECTURE_REQUESTED"
AGENT_EXECUTION_REQUESTED = "AGENT_EXECUTION_REQUESTED"
AGENT_EXECUTION_COMPLETED = "AGENT_EXECUTION_COMPLETED"
HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
```

---

# FASE 6. INFRAESTRUCTURA LOCAL CON DOCKER COMPOSE

---

## 6.1 Objetivo de la Fase

En esta fase se levantará la infraestructura local necesaria para que el backend funcione. PostgreSQL almacenará información persistente, Redis servirá para cache y locks, RabbitMQ gestionará eventos asíncronos y Temporal mantendrá workflows durables.

---

## 6.2 Crear Archivo `infra/docker-compose.yml`

Crear archivo:

```bash
touch infra/docker-compose.yml
```

Agregar:

```yaml
services:

  postgres:
    image: postgres:16
    container_name: scrumdev-postgres
    environment:
      POSTGRES_USER: scrumdev
      POSTGRES_PASSWORD: scrumdev
      POSTGRES_DB: scrumdev_ai
    ports:
      - "5432:5432"
    volumes:
      - scrumdev_postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    container_name: scrumdev-redis
    ports:
      - "6379:6379"

  rabbitmq:
    image: rabbitmq:3-management
    container_name: scrumdev-rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"

  temporal:
    image: temporalio/auto-setup:latest
    container_name: scrumdev-temporal
    ports:
      - "7233:7233"
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=scrumdev
      - POSTGRES_PWD=scrumdev
      - POSTGRES_SEEDS=postgres
    depends_on:
      - postgres

volumes:
  scrumdev_postgres_data:
```

---

## 6.3 Levantar Infraestructura

Ejecutar:

```bash
docker compose -f infra/docker-compose.yml up -d
```

---

## 6.4 Verificar Contenedores

Ejecutar:

```bash
docker ps
```

Resultado esperado:

```text
scrumdev-postgres
scrumdev-redis
scrumdev-rabbitmq
scrumdev-temporal
```

---

## 6.5 Verificar RabbitMQ

Abrir navegador:

```text
http://localhost:15672
```

Credenciales por defecto:

```text
usuario: guest
contraseña: guest
```

---

# FASE 7. SERVICIO API GATEWAY

---

## 7.1 Objetivo de la Fase

En esta fase se construirá el primer microservicio FastAPI: el API Gateway. Este servicio será la puerta de entrada del frontend hacia el backend y se encargará de enrutar solicitudes hacia otros servicios.

---

## 7.2 Crear Archivo Principal

Crear archivo:

```bash
touch services/api-gateway/app/main.py
```

Agregar:

```python
from fastapi import FastAPI

app = FastAPI(title="ScrumDev AI - API Gateway")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "api-gateway"
    }
```

---

## 7.3 Ejecutar API Gateway Localmente

Ejecutar desde la raíz del proyecto:

```bash
PYTHONPATH=. uvicorn services.api-gateway.app.main:app --reload --port 8080
```

Si el guion medio genera error de importación, usar ejecución desde la carpeta del servicio:

```bash
cd services/api-gateway
PYTHONPATH=../.. uvicorn app.main:app --reload --port 8080
```

---

## 7.4 Probar Healthcheck

Abrir:

```text
http://localhost:8080/health
```

Resultado esperado:

```json
{
  "status": "ok",
  "service": "api-gateway"
}
```

---

## 7.5 Nota de Nombres de Carpetas

Python no permite importar paquetes con guiones medios fácilmente. Para producción se recomienda usar nombres con guion bajo en módulos Python o ejecutar cada servicio desde su propia carpeta.

Ejemplo alternativo:

```text
api_gateway
conversation_service
orchestrator_service
```

En este taller se mantiene el nombre con guion medio porque es más claro visualmente para identificar microservicios.

---

# FASE 8. CONVERSATION SERVICE BASE

---

## 8.1 Objetivo de la Fase

En esta fase se construirá el servicio encargado de recibir mensajes del humano. Todavía no ejecutará agentes; solo recibirá mensajes y devolverá una respuesta controlada para validar el flujo básico.

---

## 8.2 Crear Modelo de Mensaje

Crear archivo:

```bash
mkdir -p services/conversation-service/app/models
touch services/conversation-service/app/models/chat_message.py
```

Agregar:

```python
from pydantic import BaseModel
from typing import Optional


class ChatMessage(BaseModel):
    user_id: str
    project_key: str
    issue_key: Optional[str] = None
    content: str
```

---

## 8.3 Crear Aplicación FastAPI

Crear archivo:

```bash
touch services/conversation-service/app/main.py
```

Agregar:

```python
from fastapi import FastAPI
from app.models.chat_message import ChatMessage

app = FastAPI(title="ScrumDev AI - Conversation Service")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "conversation-service"
    }


@app.post("/messages")
async def receive_message(message: ChatMessage):
    return {
        "success": True,
        "assistant_message": f"Mensaje recibido para el proyecto {message.project_key}",
        "received": message.model_dump()
    }
```

---

## 8.4 Ejecutar Conversation Service

Ejecutar:

```bash
cd services/conversation-service
PYTHONPATH=../.. uvicorn app.main:app --reload --port 8001
```

---

## 8.5 Probar Endpoint

Ejecutar:

```bash
curl -X POST http://localhost:8001/messages \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "project_key": "SDAI",
    "issue_key": "SDAI-1",
    "content": "Refina esta historia"
  }'
```

Resultado esperado:

```json
{
  "success": true,
  "assistant_message": "Mensaje recibido para el proyecto SDAI",
  "received": {
    "user_id": "u1",
    "project_key": "SDAI",
    "issue_key": "SDAI-1",
    "content": "Refina esta historia"
  }
}
```

---

# FASE 9. ORCHESTRATOR SERVICE BASE

---

## 9.1 Objetivo de la Fase

En esta fase se construirá el servicio orquestador base. Su función inicial será recibir comandos y preparar la futura conexión con Temporal. En este taller todavía no implementará workflows complejos; eso se profundizará en el Taller 3.

---

## 9.2 Crear Aplicación FastAPI

Crear archivo:

```bash
touch services/orchestrator-service/app/main.py
```

Agregar:

```python
from fastapi import FastAPI
from shared.contracts.commands import StartWorkflowCommand

app = FastAPI(title="ScrumDev AI - Orchestrator Service")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "orchestrator-service"
    }


@app.post("/workflows/start")
async def start_workflow(command: StartWorkflowCommand):
    return {
        "success": True,
        "workflow_id": f"wf-{command.project_key}-{command.issue_key or 'general'}",
        "command": command.model_dump()
    }
```

---

## 9.3 Ejecutar Orchestrator Service

Ejecutar:

```bash
cd services/orchestrator-service
PYTHONPATH=../.. uvicorn app.main:app --reload --port 8002
```

---

## 9.4 Probar Orchestrator

Ejecutar:

```bash
curl -X POST http://localhost:8002/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "project_key": "SDAI",
    "issue_key": "SDAI-1",
    "user_id": "u1",
    "message": "Iniciar refinamiento"
  }'
```

Resultado esperado:

```json
{
  "success": true,
  "workflow_id": "wf-SDAI-SDAI-1"
}
```

---

# FASE 10. TEMPORAL BASE

---

## 10.1 Objetivo de la Fase

En esta fase se preparará la estructura mínima de Temporal. Temporal será el motor de workflows durables que permitirá ejecutar procesos largos, esperar aprobaciones humanas y recuperarse ante fallos.

---

## 10.2 Crear Workflow Base

Crear archivo:

```bash
touch temporal/workflows/software_delivery_workflow.py
```

Agregar:

```python
from temporalio import workflow


@workflow.defn
class SoftwareDeliveryWorkflow:

    @workflow.run
    async def run(self, command: dict) -> dict:
        return {
            "status": "workflow_started",
            "command": command
        }
```

---

## 10.3 Crear Worker Base

Crear archivo:

```bash
touch temporal/worker.py
```

Agregar:

```python
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from shared.config.settings import settings
from temporal.workflows.software_delivery_workflow import SoftwareDeliveryWorkflow


async def main():
    client = await Client.connect(settings.temporal_host)

    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[SoftwareDeliveryWorkflow],
        activities=[]
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 10.4 Nota Técnica sobre Temporal

El workflow creado en esta fase es mínimo. En el Taller 3 se conectará con actividades reales, agentes CrewAI, aprobaciones humanas y estados de ScrumDev AI.

---

# FASE 11. DOCKERIZACIÓN BÁSICA DE SERVICIOS

---

## 11.1 Objetivo de la Fase

En esta fase se preparará la base para ejecutar los servicios mediante contenedores. La dockerización permite que cada microservicio se ejecute de forma aislada, reproducible y portable.

---

## 11.2 Crear Dockerfile para API Gateway

Crear archivo:

```bash
touch services/api-gateway/Dockerfile
```

Agregar:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-root

COPY . /app

CMD ["uvicorn", "services.api-gateway.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 11.3 Crear Dockerfile para Conversation Service

Crear archivo:

```bash
touch services/conversation-service/Dockerfile
```

Agregar:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-root

COPY . /app

CMD ["uvicorn", "services.conversation-service.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

## 11.4 Advertencia Técnica sobre Guiones Medios

Los nombres con guion medio pueden causar problemas al importar módulos en Python desde Docker. Si se encuentra ese problema, renombrar las carpetas internas de ejecución a:

```text
api_gateway
conversation_service
orchestrator_service
```

Para mantener claridad documental, los nombres de carpetas visibles se conservan como microservicios.

---

# FASE 12. VALIDACIÓN FINAL DEL TALLER

---

## 12.1 Objetivo de la Fase

En esta fase se verificará que la infraestructura y los servicios base funcionan correctamente antes de pasar al runtime de agentes.

---

## 12.2 Validar Infraestructura

Ejecutar:

```bash
docker ps
```

Verificar:

```text
PostgreSQL activo
Redis activo
RabbitMQ activo
Temporal activo
```

---

## 12.3 Validar API Gateway

Abrir:

```text
http://localhost:8080/health
```

Resultado esperado:

```json
{
  "status": "ok",
  "service": "api-gateway"
}
```

---

## 12.4 Validar Conversation Service

Ejecutar:

```bash
curl -X POST http://localhost:8001/messages \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "project_key": "SDAI",
    "issue_key": "SDAI-1",
    "content": "Hola"
  }'
```

Resultado esperado:

```json
{
  "success": true
}
```

---

## 12.5 Validar Orchestrator Service

Ejecutar:

```bash
curl -X POST http://localhost:8002/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "project_key": "SDAI",
    "issue_key": "SDAI-1",
    "user_id": "u1",
    "message": "Iniciar workflow"
  }'
```

Resultado esperado:

```json
{
  "success": true
}
```

---

## 12.6 Resultado Esperado

Al finalizar este taller el estudiante tendrá:

```text
repositorio backend organizado
dependencias instaladas
variables de entorno configuradas
infraestructura local funcionando
API Gateway base funcionando
Conversation Service base funcionando
Orchestrator Service base funcionando
estructura inicial de Temporal creada
contratos compartidos definidos
eventos base definidos
```

El sistema quedará preparado para el Taller 3, donde se construirá el runtime de agentes, workflows reales y orquestación inteligente.
