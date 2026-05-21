# Taller 5 — Integración Completa y Testing

---

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/0a31a068-2d29-4198-8667-923e74589427" />





# FASE 1. INTRODUCCIÓN A LA INTEGRACIÓN DEL SISTEMA

---

## 1.1 Objetivo de la Fase

En este taller se integrarán todos los componentes desarrollados anteriormente para construir un flujo funcional completo de ScrumDev AI. El objetivo es conectar frontend, backend, runtime de agentes, workflows y servicios externos en una arquitectura coherente y verificable.

A diferencia de los talleres anteriores, donde cada componente fue construido de forma independiente, aquí se validará el comportamiento end-to-end de la plataforma.

---

## 1.2 Comprender la Integración Completa

El flujo completo del sistema será:

```text
Humano
→ Frontend Conversacional
→ API Gateway
→ Conversation Service
→ Orchestrator Service
→ Temporal Workflow
→ Agent Runtime Service
→ CrewAI Agents
→ Jira / Git / Deploy
```

---

# FASE 2. INTEGRACIÓN FRONTEND ↔ API GATEWAY

---

## 2.1 Objetivo de la Fase

El frontend debe comunicarse correctamente con el backend distribuido utilizando el API Gateway como único punto de entrada.

---

## 2.2 Verificar Variables Frontend

Abrir:

```text
frontend/web-chat/.env.local
```

Verificar:

```env
NEXT_PUBLIC_API_GATEWAY_URL=http://localhost:8080
NEXT_PUBLIC_WS_URL=ws://localhost:8080/ws
```

---

## 2.3 Habilitar CORS en API Gateway

Editar:

```text
services/api-gateway/app/main.py
```

Agregar:

```python
from fastapi.middleware.cors import CORSMiddleware
```

Agregar configuración:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 2.4 Verificar Comunicación Frontend ↔ Backend

Ejecutar frontend:

```bash
npm run dev
```

Ejecutar API Gateway:

```bash
uvicorn services.api-gateway.app.main:app --reload --port 8080
```

Abrir:

```text
http://localhost:3000
```

Enviar mensaje desde el chat.

Resultado esperado:

```text
mensaje recibido backend
respuesta visible frontend
```

---

# FASE 3. INTEGRACIÓN CONVERSATION SERVICE ↔ ORCHESTRATOR

---

## 3.1 Objetivo de la Fase

El Conversation Service debe delegar workflows al Orchestrator Service.

---

## 3.2 Modificar Conversation Service

Editar:

```text
services/conversation-service/app/main.py
```

Agregar:

```python
import httpx
```

Modificar endpoint:

```python
@app.post("/messages")
async def receive_message(message: ChatMessage):

    async with httpx.AsyncClient() as client:

        workflow_response = await client.post(
            "http://localhost:8002/workflows/start",
            json={
                "project_key": message.project_key,
                "issue_key": message.issue_key,
                "user_id": message.user_id,
                "message": message.content
            }
        )

    return {
        "success": True,
        "workflow": workflow_response.json()
    }
```

---

## 3.3 Verificar Integración

Enviar mensaje desde frontend.

Resultado esperado:

```text
Conversation Service
→ llama Orchestrator Service
→ inicia workflow
```

---

# FASE 4. INTEGRACIÓN ORCHESTRATOR ↔ TEMPORAL

---

## 4.1 Objetivo de la Fase

El Orchestrator Service debe iniciar workflows reales en Temporal.

---

## 4.2 Conectar Temporal Client

Editar:

```text
services/orchestrator-service/app/main.py
```

Agregar:

```python
from temporalio.client import Client
```

---

## 4.3 Crear Cliente Temporal

Agregar:

```python
temporal_client = None


@app.on_event("startup")
async def startup():

    global temporal_client

    temporal_client = await Client.connect(
        "localhost:7233"
    )
```

---

## 4.4 Ejecutar Workflow Temporal

Modificar endpoint:

```python
workflow_handle = await temporal_client.start_workflow(
    "SoftwareDeliveryWorkflow.run",
    command.model_dump(),
    id=f"workflow-{command.project_key}",
    task_queue="scrumdev-ai-task-queue"
)
```

---

## 4.5 Verificar Workflow

Abrir Temporal UI:

```text
http://localhost:8233
```

Resultado esperado:

```text
workflow visible
workflow ejecutándose
```

---

# FASE 5. INTEGRACIÓN AGENT RUNTIME ↔ ORCHESTRATOR

---

## 5.1 Objetivo de la Fase

El Orchestrator Service debe ejecutar agentes mediante el Agent Runtime Service.

---

## 5.2 Conectar Runtime Service

Editar workflow Temporal.

Agregar llamada:

```python
import httpx
```

---

## 5.3 Ejecutar Refinamiento

Agregar:

```python
async with httpx.AsyncClient() as client:

    response = await client.post(
        "http://localhost:8003/refinement",
        json={
            "story": command["message"]
        }
    )
```

---

## 5.4 Verificar Ejecución Agentes

Resultado esperado:

```text
workflow ejecuta agente
CrewAI responde
resultado visible
```

---

# FASE 6. INTEGRACIÓN CON JIRA

---

## 6.1 Objetivo de la Fase

Los agentes deben interactuar automáticamente con Jira.

---

## 6.2 Crear Cliente Jira

Crear archivo:

```bash
touch shared/clients/jira_client.py
```

Agregar:

```python
import httpx

from shared.config.settings import settings


class JiraClient:

    async def get_issue(self, issue_key: str):

        url = (
            f"{settings.scrumdev_jira_base_url}"
            f"/rest/api/3/issue/{issue_key}"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                auth=(
                    settings.scrumdev_jira_email,
                    settings.scrumdev_jira_api_token
                )
            )

        return response.json()
```

---

## 6.3 Verificar Jira

Ejecutar:

```bash
python
```

Probar:

```python
from shared.clients.jira_client import JiraClient

client = JiraClient()
```

---

# FASE 7. INTEGRACIÓN CON GITHUB

---

## 7.1 Objetivo de la Fase

Los agentes deben poder crear ramas, commits y pull requests.

---

## 7.2 Crear Cliente GitHub

Crear archivo:

```bash
touch shared/clients/github_client.py
```

Agregar:

```python
import httpx

from shared.config.settings import settings


class GitHubClient:

    async def get_repo(self):

        url = (
            f"https://api.github.com/repos/"
            f"{settings.scrumdev_git_owner}/"
            f"{settings.scrumdev_git_repo}"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers={
                    "Authorization":
                    f"Bearer {settings.scrumdev_git_token}"
                }
            )

        return response.json()
```

---

## 7.3 Verificar GitHub

Probar cliente.

Resultado esperado:

```text
información repositorio obtenida
```

---

# FASE 8. INTEGRACIÓN MEMORIA SEMÁNTICA

---

## 8.1 Objetivo de la Fase

Los agentes deben mantener contexto persistente.

---

## 8.2 Guardar Conversaciones

Agregar al workflow:

```python
save_memory(
    memory_id="story-1",
    content=command["message"]
)
```

---

## 8.3 Verificar Memoria

Probar:

```python
search_memory("login usuario")
```

Resultado esperado:

```text
resultados relacionados
```

---

# FASE 9. IMPLEMENTACIÓN DE LOGGING

---

## 9.1 Objetivo de la Fase

La observabilidad es fundamental en sistemas distribuidos.

---

## 9.2 Crear Logger Compartido

Crear archivo:

```bash
touch shared/observability/logger.py
```

Agregar:

```python
import structlog

logger = structlog.get_logger()
```

---

## 9.3 Usar Logging

Agregar:

```python
logger.info(
    "workflow_started",
    workflow_id="wf-1"
)
```

---

## 9.4 Comprender Logging Estructurado

Permite:

```text
trazabilidad
debugging
monitoring
auditoría
```

---

# FASE 10. TESTING UNITARIO

---

## 10.1 Objetivo de la Fase

Validar componentes individualmente.

---

## 10.2 Crear Carpeta Tests

Ejecutar:

```bash
mkdir tests
mkdir tests/unit
```

---

## 10.3 Crear Test API Gateway

Crear archivo:

```bash
touch tests/unit/test_gateway.py
```

Agregar:

```python
from fastapi.testclient import TestClient

from services.api-gateway.app.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200
```

---

## 10.4 Ejecutar Tests

Ejecutar:

```bash
pytest
```

---

# FASE 11. TESTING DE INTEGRACIÓN

---

## 11.1 Objetivo de la Fase

Validar comunicación entre microservicios.

---

## 11.2 Crear Test Integración

Crear archivo:

```bash
touch tests/test_integration.py
```

Agregar:

```python
import httpx
import pytest


@pytest.mark.asyncio
async def test_conversation_service():

    async with httpx.AsyncClient() as client:

        response = await client.post(
            "http://localhost:8001/messages",
            json={
                "user_id": "u1",
                "project_key": "SDAI",
                "content": "Hola"
            }
        )

    assert response.status_code == 200
```

---

## 11.3 Ejecutar Tests Integración

Ejecutar:

```bash
pytest
```

---

# FASE 12. TESTING END-TO-END

---

## 12.1 Objetivo de la Fase

Validar flujo completo frontend ↔ backend ↔ agentes.

---

## 12.2 Flujo a Validar

El sistema debe permitir:

```text
usuario escribe mensaje
workflow inicia
agente responde
frontend actualiza
```

---

## 12.3 Ejecutar Todos los Servicios

Ejecutar:

```bash
docker compose -f infra/docker-compose.yml up -d
```

Ejecutar:

```bash
API Gateway
Conversation Service
Orchestrator Service
Agent Runtime Service
Frontend
Temporal Worker
```

---

## 12.4 Validar Flujo Completo

Desde frontend:

```text
crear historia
refinar historia
generar arquitectura
```

Resultado esperado:

```text
workflow ejecutado
agentes responden
frontend actualizado
```

---

# FASE 13. OBSERVABILIDAD Y MONITOREO

---

## 13.1 Objetivo de la Fase

La plataforma debe permitir monitoreo y diagnóstico.

---

## 13.2 Verificar Temporal UI

Abrir:

```text
http://localhost:8233
```

---

## 13.3 Verificar RabbitMQ UI

Abrir:

```text
http://localhost:15672
```

---

## 13.4 Comprender Observabilidad

Permite:

```text
rastrear workflows
visualizar errores
monitorear eventos
analizar rendimiento
```

---

# FASE 14. VALIDACIÓN FINAL

---

## 14.1 Objetivo de la Fase

Validar funcionamiento completo de ScrumDev AI.

---

## 14.2 Verificar Integración General

Verificar:

```text
frontend conectado
API Gateway funcionando
Temporal workflows activos
CrewAI funcionando
Jira integrado
GitHub integrado
memoria funcionando
tests exitosos
```

---

## 14.3 Resultado Esperado

Al finalizar este taller el estudiante tendrá:

```text
frontend integrado
backend integrado
Temporal funcionando
agentes ejecutándose
Jira integrado
GitHub integrado
testing implementado
observabilidad configurada
flujo end-to-end validado
```

El sistema quedará preparado para automatizar despliegues y ambientes productivos en el siguiente taller.
