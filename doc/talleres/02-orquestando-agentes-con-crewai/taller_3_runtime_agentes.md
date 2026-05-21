# Taller 3 — Runtime de Agentes y Workflows

---
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/73a0a128-4902-4f91-a503-42484e97a69b" />



# FASE 1. INTRODUCCIÓN AL RUNTIME DE AGENTES

---

## 1.1 Objetivo de la Fase

En este taller se construirá el núcleo inteligente de ScrumDev AI. El objetivo es implementar el runtime de agentes, la ejecución coordinada mediante CrewAI y los workflows durables utilizando Temporal.

Mientras el Taller 2 construyó la infraestructura técnica y los servicios base, este taller incorporará la capa de inteligencia encargada de analizar historias, coordinar agentes especializados, mantener trazabilidad y ejecutar procesos automatizados del ciclo de vida del desarrollo de software.

---

## 1.2 Comprender el Runtime de Agentes

El runtime de agentes es el componente encargado de:

```text
registrar agentes
ejecutar agentes
coordinar tareas
mantener contexto
administrar memoria
ejecutar workflows
```

Arquitectura conceptual:

```text
Humano
→ Conversation Service
→ Orchestrator Service
→ Temporal Workflow
→ Agent Runtime Service
→ CrewAI Agents
```

---

# FASE 2. INSTALACIÓN DE DEPENDENCIAS IA

---

## 2.1 Objetivo de la Fase

En esta fase se instalarán las dependencias necesarias para ejecutar agentes IA, administrar memoria semántica y conectar CrewAI con los modelos de lenguaje configurados en el Taller 1.

---

## 2.2 Instalar CrewAI y Dependencias IA

Desde la raíz del proyecto ejecutar:

```bash
poetry add crewai langchain chromadb tiktoken openai sentence-transformers
```

---

## 2.3 Explicación de Dependencias

| Librería | Función |
|---|---|
| `crewai` | Orquestación de agentes IA |
| `langchain` | Integración LLM y herramientas |
| `chromadb` | Base vectorial para memoria |
| `tiktoken` | Conteo tokens OpenAI |
| `openai` | Cliente oficial OpenAI |
| `sentence-transformers` | Embeddings locales |

---

## 2.4 Verificar Instalación

Ejecutar:

```bash
poetry show
```

Verificar presencia de:

```text
crewai
langchain
chromadb
openai
```

---

# FASE 3. ESTRUCTURA DEL AGENT RUNTIME SERVICE

---

## 3.1 Objetivo de la Fase

En esta fase se construirá la estructura interna del servicio encargado de ejecutar agentes IA.

El runtime debe ser desacoplado para permitir agregar nuevos agentes sin modificar el orquestador principal.

---

## 3.2 Crear Estructura del Runtime

Ejecutar:

```bash
mkdir -p services/agent-runtime-service/app/agents
mkdir -p services/agent-runtime-service/app/runtime
mkdir -p services/agent-runtime-service/app/memory
mkdir -p services/agent-runtime-service/app/tools
mkdir -p services/agent-runtime-service/app/crews
mkdir -p services/agent-runtime-service/app/workflows
```

---

## 3.3 Crear Archivos Base

Ejecutar:

```bash
touch services/agent-runtime-service/app/main.py
touch services/agent-runtime-service/app/runtime/agent_registry.py
touch services/agent-runtime-service/app/runtime/agent_executor.py
touch services/agent-runtime-service/app/memory/vector_store.py
```

---

## 3.4 Comprender la Separación del Runtime

| Componente | Responsabilidad |
|---|---|
| `agents/` | Definición agentes |
| `runtime/` | Ejecución agentes |
| `memory/` | Memoria semántica |
| `tools/` | Herramientas externas |
| `crews/` | Coordinación CrewAI |
| `workflows/` | Integración workflows |

---

# FASE 4. CONFIGURACIÓN DEL MODELO IA

---

## 4.1 Objetivo de la Fase

En esta fase se configurará el proveedor LLM que utilizarán los agentes.

---

## 4.2 Crear Configuración LLM

Crear archivo:

```bash
touch services/agent-runtime-service/app/runtime/llm.py
```

Agregar:

```python
from crewai import LLM

from shared.config.settings import settings


llm = LLM(
    model=settings.scrumdev_ai_model,
    api_key=settings.scrumdev_ai_api_key
)
```

---

## 4.3 Verificar Variables de Entorno

Verificar `.env`:

```env
SCRUMDEV_AI_PROVIDER=openai
SCRUMDEV_AI_API_KEY=
SCRUMDEV_AI_MODEL=gpt-5.5
```

---

# FASE 5. CREACIÓN DE AGENTES BASE

---

## 5.1 Objetivo de la Fase

En esta fase se implementarán los agentes principales de ScrumDev AI.

Cada agente tendrá una responsabilidad específica siguiendo separación de roles Scrum y SDLC.

---

## 5.2 Crear PO Agent

Crear archivo:

```bash
touch services/agent-runtime-service/app/agents/po_agent.py
```

Agregar:

```python
from crewai import Agent

from app.runtime.llm import llm


po_agent = Agent(
    role="Product Owner Agent",
    goal="Refinar historias Scrum y clarificar requerimientos",
    backstory="Especialista en refinamiento Scrum y análisis funcional.",
    llm=llm,
    verbose=True
)
```

---

## 5.3 Crear Architect Agent

Crear archivo:

```bash
touch services/agent-runtime-service/app/agents/architect_agent.py
```

Agregar:

```python
from crewai import Agent

from app.runtime.llm import llm


architect_agent = Agent(
    role="Software Architect Agent",
    goal="Definir arquitecturas escalables y desacopladas",
    backstory="Arquitecto experto en microservicios y cloud-native.",
    llm=llm,
    verbose=True
)
```

---

## 5.4 Crear Developer Agent

Crear archivo:

```bash
touch services/agent-runtime-service/app/agents/developer_agent.py
```

Agregar:

```python
from crewai import Agent

from app.runtime.llm import llm


developer_agent = Agent(
    role="Software Developer Agent",
    goal="Construir software limpio y mantenible",
    backstory="Desarrollador experto en backend y buenas prácticas.",
    llm=llm,
    verbose=True
)
```

---

## 5.5 Crear QA Agent

Crear archivo:

```bash
touch services/agent-runtime-service/app/agents/qa_agent.py
```

Agregar:

```python
from crewai import Agent

from app.runtime.llm import llm


qa_agent = Agent(
    role="QA Agent",
    goal="Validar calidad funcional y técnica",
    backstory="Especialista en testing y aseguramiento calidad.",
    llm=llm,
    verbose=True
)
```

---

## 5.6 Crear Security Agent

Crear archivo:

```bash
touch services/agent-runtime-service/app/agents/security_agent.py
```

Agregar:

```python
from crewai import Agent

from app.runtime.llm import llm


security_agent = Agent(
    role="Security Agent",
    goal="Validar vulnerabilidades y riesgos",
    backstory="Especialista DevSecOps y seguridad cloud.",
    llm=llm,
    verbose=True
)
```

---

# FASE 6. REGISTRO CENTRALIZADO DE AGENTES

---

## 6.1 Objetivo de la Fase

El runtime necesita un mecanismo centralizado para registrar y recuperar agentes dinámicamente.

Esto permitirá agregar nuevos agentes sin modificar el núcleo del sistema.

---

## 6.2 Implementar Agent Registry

Editar:

```text
services/agent-runtime-service/app/runtime/agent_registry.py
```

Agregar:

```python
class AgentRegistry:

    def __init__(self):
        self.agents = {}

    def register(self, name, agent):
        self.agents[name] = agent

    def get(self, name):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())
```

---

## 6.3 Registrar Agentes

Crear archivo:

```bash
touch services/agent-runtime-service/app/runtime/bootstrap.py
```

Agregar:

```python
from app.runtime.agent_registry import AgentRegistry

from app.agents.po_agent import po_agent
from app.agents.architect_agent import architect_agent
from app.agents.developer_agent import developer_agent
from app.agents.qa_agent import qa_agent
from app.agents.security_agent import security_agent


registry = AgentRegistry()

registry.register("po_agent", po_agent)
registry.register("architect_agent", architect_agent)
registry.register("developer_agent", developer_agent)
registry.register("qa_agent", qa_agent)
registry.register("security_agent", security_agent)
```

---

# FASE 7. MEMORIA SEMÁNTICA

---

## 7.1 Objetivo de la Fase

Los agentes necesitan memoria para mantener contexto entre conversaciones y workflows.

La memoria semántica permitirá almacenar:

```text
historias
decisiones
arquitecturas
conversaciones
artefactos
```

---

## 7.2 Configurar ChromaDB

Editar:

```text
services/agent-runtime-service/app/memory/vector_store.py
```

Agregar:

```python
import chromadb


client = chromadb.Client()

collection = client.create_collection(
    name="scrumdev_memory"
)
```

---

## 7.3 Crear Funciones de Memoria

Agregar:

```python
def save_memory(memory_id: str, content: str):

    collection.add(
        ids=[memory_id],
        documents=[content]
    )


def search_memory(query: str):

    return collection.query(
        query_texts=[query],
        n_results=5
    )
```

---

## 7.4 Comprender la Memoria Semántica

La memoria permitirá:

```text
persistencia contexto
RAG
trazabilidad
aprendizaje contextual
```

---

# FASE 8. CREACIÓN DE CREWS

---

## 8.1 Objetivo de la Fase

CrewAI utiliza crews para coordinar múltiples agentes trabajando colaborativamente.

---

## 8.2 Crear Crew de Refinamiento

Crear archivo:

```bash
touch services/agent-runtime-service/app/crews/refinement_crew.py
```

Agregar:

```python
from crewai import Crew, Task

from app.agents.po_agent import po_agent


def create_refinement_crew(user_story: str):

    task = Task(
        description=f"Refina la historia: {user_story}",
        expected_output="Historia refinada",
        agent=po_agent
    )

    crew = Crew(
        agents=[po_agent],
        tasks=[task],
        verbose=True
    )

    return crew
```

---

## 8.3 Crear Crew Arquitectura

Crear archivo:

```bash
touch services/agent-runtime-service/app/crews/architecture_crew.py
```

Agregar:

```python
from crewai import Crew, Task

from app.agents.architect_agent import architect_agent


def create_architecture_crew(requirements: str):

    task = Task(
        description=f"Definir arquitectura para: {requirements}",
        expected_output="Arquitectura propuesta",
        agent=architect_agent
    )

    crew = Crew(
        agents=[architect_agent],
        tasks=[task],
        verbose=True
    )

    return crew
```

---

# FASE 9. EJECUTOR DE AGENTES

---

## 9.1 Objetivo de la Fase

El ejecutor será responsable de iniciar crews y retornar resultados al orquestador.

---

## 9.2 Implementar Agent Executor

Editar:

```text
services/agent-runtime-service/app/runtime/agent_executor.py
```

Agregar:

```python
from app.crews.refinement_crew import create_refinement_crew
from app.crews.architecture_crew import create_architecture_crew


class AgentExecutor:

    async def execute_refinement(self, story: str):

        crew = create_refinement_crew(story)

        return crew.kickoff()

    async def execute_architecture(self, requirements: str):

        crew = create_architecture_crew(requirements)

        return crew.kickoff()
```

---

# FASE 10. API DEL AGENT RUNTIME SERVICE

---

## 10.1 Objetivo de la Fase

En esta fase se expondrán endpoints HTTP para que otros servicios puedan ejecutar agentes.

---

## 10.2 Implementar FastAPI Runtime Service

Editar:

```text
services/agent-runtime-service/app/main.py
```

Agregar:

```python
from fastapi import FastAPI
from pydantic import BaseModel

from app.runtime.agent_executor import AgentExecutor


app = FastAPI(title="ScrumDev AI - Agent Runtime")

executor = AgentExecutor()


class RefinementRequest(BaseModel):
    story: str


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "agent-runtime-service"
    }


@app.post("/refinement")
async def refinement(request: RefinementRequest):

    result = await executor.execute_refinement(
        request.story
    )

    return {
        "success": True,
        "result": str(result)
    }
```

---

## 10.3 Ejecutar Agent Runtime Service

Ejecutar:

```bash
cd services/agent-runtime-service
PYTHONPATH=../.. uvicorn app.main:app --reload --port 8003
```

---

## 10.4 Probar Endpoint Refinement

Ejecutar:

```bash
curl -X POST http://localhost:8003/refinement \
-H "Content-Type: application/json" \
-d '{
  "story": "Como usuario quiero iniciar sesión"
}'
```

---

# FASE 11. WORKFLOWS TEMPORAL

---

## 11.1 Objetivo de la Fase

Temporal permitirá ejecutar workflows durables que coordinen agentes y esperen aprobaciones humanas.

---

## 11.2 Crear Workflow Refinamiento

Editar:

```text
temporal/workflows/software_delivery_workflow.py
```

Agregar:

```python
from temporalio import workflow


@workflow.defn
class SoftwareDeliveryWorkflow:

    @workflow.run
    async def run(self, command: dict):

        return {
            "workflow": "started",
            "command": command
        }
```

---

## 11.3 Comprender Workflows Durables

Temporal permitirá:

```text
persistir estado
reintentos automáticos
esperar aprobaciones humanas
recuperación fallos
workflows largos
```

---

# FASE 12. POLICY SERVICE

---

## 12.1 Objetivo de la Fase

El sistema debe aplicar buenas prácticas automáticamente durante generación de software.

---

## 12.2 Crear Política Arquitectónica

Crear archivo:

```bash
mkdir -p docs/policies
touch docs/policies/architecture-policy.yaml
```

Agregar:

```yaml
architecture:
  style: microservices

patterns:
  required:
    - repository
    - dependency_injection

quality:
  tests_required: true

security:
  auth_required: true
```

---

## 12.3 Comprender el Policy Service

Las políticas permitirán validar automáticamente:

```text
arquitectura
seguridad
testing
patrones diseño
```

---

# FASE 13. EVENTOS Y AUDITORÍA

---

## 13.1 Objetivo de la Fase

Los eventos permitirán desacoplar servicios y mantener trazabilidad.

---

## 13.2 Crear Eventos Nuevos

Agregar eventos:

```text
AGENT_EXECUTION_STARTED
AGENT_EXECUTION_COMPLETED
HUMAN_APPROVAL_REQUIRED
WORKFLOW_COMPLETED
```

---

## 13.3 Comprender la Auditoría

La auditoría permitirá rastrear:

```text
acciones agentes
decisiones humanas
errores
workflow
despliegues
```

---

# FASE 14. VALIDACIÓN FINAL

---

## 14.1 Objetivo de la Fase

Verificar funcionamiento del runtime de agentes y workflows.

---

## 14.2 Validar Agent Runtime Service

Abrir:

```text
http://localhost:8003/health
```

Resultado esperado:

```json
{
  "status": "ok",
  "service": "agent-runtime-service"
}
```

---

## 14.3 Validar Endpoint Refinement

Ejecutar:

```bash
curl -X POST http://localhost:8003/refinement \
-H "Content-Type: application/json" \
-d '{
  "story": "Como usuario quiero registrarme"
}'
```

---

## 14.4 Resultado Esperado

Al finalizar este taller el estudiante tendrá:

```text
CrewAI configurado
runtime agentes funcionando
agentes especializados creados
registry agentes implementado
memoria semántica configurada
crews funcionando
Temporal configurado
workflows base funcionando
policy service inicial
eventos y auditoría preparados
```

El sistema quedará listo para construir el frontend conversacional en el siguiente taller.
