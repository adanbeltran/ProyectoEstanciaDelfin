# Taller replicable: plataforma conversacional multiagente para desarrollo de software con backend orientado a microservicios

**Versión:** 1.0  
**Propósito:** construir una plataforma reutilizable donde un Product Owner humano interactúa por una interfaz web conversacional con un PO Agent, y el sistema orquesta agentes especializados, Jira, Git, base de datos, despliegue, políticas de arquitectura y buenas prácticas.

---

## 0. Resultado esperado del taller

Al finalizar, tendrás una plataforma que permite:

1. Conectar un proyecto Jira existente o nuevo.
2. Conectar un repositorio Git existente o nuevo.
3. Conectar un proveedor de despliegue local, cloud o web.
4. Configurar credenciales y proveedores mediante `.env`.
5. Usar una interfaz web conversacional para que el humano interactúe con el PO Agent.
6. Capturar requerimientos no funcionales en un formulario web de preguntas simples.
7. Generar una propuesta de arquitectura con aprobación humana.
8. Generar políticas técnicas reutilizables: `architecture-policy.yaml`, `quality-gates.yaml` y ADR.
9. Orquestar agentes de desarrollo, arquitectura, QA, seguridad, DevOps y release.
10. Reemplazar o agregar servicios sin modificar todo el código.

---

## 1. Principio arquitectónico del sistema

La plataforma debe ser construida como un conjunto de microservicios. El orquestador no debe conectarse directamente a Jira, Git, despliegue ni base de datos mediante lógica fija. Debe comunicarse con servicios independientes a través de contratos HTTP, eventos o colas.

### 1.1 Arquitectura conceptual

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/5900c3cb-af27-4263-8ef3-545dee36b828" />




### 1.2 Regla central

El orquestador solo conoce **contratos**, no implementaciones concretas.

Incorrecto:

```text
Orchestrator → código específico de Jira
Orchestrator → código específico de GitHub
Orchestrator → código específico de Render
```

Correcto:

```text
Orchestrator → ProjectManagementService
Orchestrator → VersionControlService
Orchestrator → DeploymentService
```

Esto permite cambiar Jira por Azure DevOps, GitHub por GitLab, Render por AWS, o agregar nuevos agentes sin reescribir el núcleo.

---

## 2. Fuentes oficiales consultadas

Estas fuentes deben revisarse antes de una implementación productiva porque precios, límites y capacidades pueden cambiar:

- Jira Cloud REST API v3: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
- Jira Cloud Webhooks: https://developer.atlassian.com/cloud/jira/platform/webhooks/
- GitHub REST API: https://docs.github.com/en/rest
- GitHub repository webhooks: https://docs.github.com/en/rest/repos/webhooks
- GitHub pull requests API: https://docs.github.com/rest/pulls/pulls
- OpenAI API pricing: https://openai.com/api/pricing/
- CrewAI Flows: https://docs.crewai.com/en/concepts/flows

Jira permite usar REST API v3 y webhooks para integrar aplicaciones externas. GitHub permite webhooks para recibir eventos y REST API para administrar repositorios, pull requests y automatizaciones. CrewAI Flows permite estructurar workflows event-driven con estado.

---

# PARTE A. CONFIGURACIÓN BASE

---

## 3. Fase 1: Configuraciones básicas

### Objetivo

Configurar todos los servicios externos e internos para que la plataforma sea reutilizable mediante variables de entorno y no mediante código quemado.

---

## 3.1 Configuración de Jira

### Propósito

Jira será la interfaz de gestión del proyecto: historias, bugs, subtareas, estados, sprints, criterios de aceptación y evidencia.

### Licencia mínima

| Necesidad | Licencia sugerida |
|---|---|
| Prototipo pequeño | Jira Cloud Free |
| Proyecto serio con permisos, tableros y administración más controlada | Jira Cloud Standard |
| Organización con múltiples equipos, gobierno y escalamiento | Premium o Enterprise |

### Pasos

1. Crear un proyecto Scrum en Jira.
2. Crear un usuario técnico para la plataforma:

```text
agent-bot@tu-dominio.com
```

3. Asignar permisos mínimos:

```text
Browse Projects
Create Issues
Edit Issues
Transition Issues
Add Comments
Assign Issues
Manage Sprints, si el agente debe operar sprints
```

4. Crear un API token para el usuario técnico.
5. Registrar el proyecto y tablero en el archivo `.env`.

### Variables

```env
JIRA_BASE_URL=https://tu-dominio.atlassian.net
JIRA_EMAIL=agent-bot@tu-dominio.com
JIRA_API_TOKEN=xxxx
JIRA_PROJECT_KEY=DAS
JIRA_BOARD_ID=1
JIRA_DEFAULT_ISSUE_TYPE=Story
```

### Validación

Ejecutar una prueba de lectura:

```bash
curl -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search?jql=project=$JIRA_PROJECT_KEY"
```

Resultado esperado:

```text
Respuesta JSON con issues del proyecto o lista vacía sin error de autenticación.
```

---

## 3.2 Configuración de Git

### Propósito

El repositorio Git será la fuente técnica: código, ramas, pull requests, revisiones y trazabilidad.

### Licencia mínima

| Necesidad | Licencia sugerida |
|---|---|
| Repositorios públicos o prototipo | GitHub Free |
| Repositorios privados con colaboración y reglas de protección | GitHub Team |
| Organización con controles avanzados | Enterprise |

### Pasos

1. Crear repositorio:

```text
demo-agentic-software
```

2. Crear ramas base:

```text
main
develop
```

3. Activar protección de ramas:

```text
main:
- requiere pull request
- requiere checks exitosos
- restringe push directo
```

4. Crear token para el bot.

### Variables

```env
GIT_PROVIDER=github
GIT_API_BASE_URL=https://api.github.com
GIT_TOKEN=xxxx
GIT_OWNER=tu-org
GIT_REPO=demo-agentic-software
GIT_DEFAULT_BRANCH=develop
GIT_PRODUCTION_BRANCH=main
```

### Convenciones

```text
Rama: feature/DAS-1-registro-usuario
Commit: DAS-1 implement user registration
PR: DAS-1 Registro de usuario
```

### Validación

```bash
curl -H "Authorization: Bearer $GIT_TOKEN" \
  "$GIT_API_BASE_URL/repos/$GIT_OWNER/$GIT_REPO"
```

Resultado esperado:

```text
Respuesta JSON con información del repositorio.
```

---

## 3.3 Configuración de despliegue

### Propósito

Permitir que los agentes publiquen versiones en staging y producción con aprobación humana.

### Opciones

| Escenario | Opción |
|---|---|
| Local | Docker Compose |
| Web estática | Vercel, Netlify, GitHub Pages |
| Backend/API | Render, Railway, Fly.io |
| Cloud empresarial | AWS, Azure, GCP |

### Licencia mínima

| Necesidad | Licencia sugerida |
|---|---|
| Prueba local | Sin licencia, Docker local |
| Prototipo público | Free tier del proveedor |
| Producción | Plan pago con logs, dominios, secretos, escalamiento y rollback |

### Variables

```env
DEPLOY_PROVIDER=render
DEPLOY_API_BASE_URL=https://api.render.com
DEPLOY_API_TOKEN=xxxx
DEPLOY_STAGING_SERVICE_ID=xxxx
DEPLOY_PRODUCTION_SERVICE_ID=xxxx
DEPLOY_STAGING_URL=https://staging.demo.com
DEPLOY_PRODUCTION_URL=https://demo.com
```

### Validación

El conector de despliegue debe poder:

```text
1. Consultar estado del servicio.
2. Disparar despliegue en staging.
3. Consultar estado del despliegue.
4. Disparar despliegue a producción solo con aprobación humana.
5. Ejecutar rollback.
```

---

## 3.4 Configuración de base de datos

### Propósito

Guardar el estado operativo del sistema. Jira no debe usarse como base de datos interna de la plataforma.

### Componentes

```text
PostgreSQL:
- proyectos conectados
- usuarios
- conversaciones
- decisiones humanas
- ejecuciones de agentes
- estados del workflow
- correlación Jira/Git/deploy

Vector DB:
- memoria semántica
- arquitectura
- documentación técnica
- decisiones históricas
```

### Variables

```env
DATABASE_URL=postgresql://agent:password@localhost:5432/agent_platform
VECTOR_DB_PROVIDER=chroma
VECTOR_DB_URL=http://localhost:8000
```

### Tablas mínimas

```text
projects
conversations
messages
workflow_instances
workflow_events
human_decisions
agent_runs
external_references
architecture_decisions
quality_gate_results
```

---

## 3.5 Configuración de API de IA

### Propósito

Ejecutar agentes especializados.

### Licencia

Para usar modelos desde tu aplicación necesitas acceso a API. Un plan de ChatGPT para uso conversacional no equivale necesariamente a crédito o uso de API. Los costos de API se consultan en la página oficial de precios de OpenAI.

### Variables

```env
AI_PROVIDER=openai
AI_API_KEY=xxxx
AI_MODEL=gpt-5.5
AI_TEMPERATURE=0.2
AI_MAX_TOKENS=8000
```

---

## 3.6 Archivo `.env.example`

```env
# General
APP_ENV=local
APP_BASE_URL=http://localhost:8080
FRONTEND_URL=http://localhost:3000

# API Gateway
API_GATEWAY_PORT=8080

# Jira
JIRA_BASE_URL=
JIRA_EMAIL=
JIRA_API_TOKEN=
JIRA_PROJECT_KEY=
JIRA_BOARD_ID=
JIRA_DEFAULT_ISSUE_TYPE=Story

# Git
GIT_PROVIDER=github
GIT_API_BASE_URL=https://api.github.com
GIT_TOKEN=
GIT_OWNER=
GIT_REPO=
GIT_DEFAULT_BRANCH=develop
GIT_PRODUCTION_BRANCH=main

# Deploy
DEPLOY_PROVIDER=
DEPLOY_API_BASE_URL=
DEPLOY_API_TOKEN=
DEPLOY_STAGING_SERVICE_ID=
DEPLOY_PRODUCTION_SERVICE_ID=
DEPLOY_STAGING_URL=
DEPLOY_PRODUCTION_URL=

# Database
DATABASE_URL=
VECTOR_DB_PROVIDER=chroma
VECTOR_DB_URL=

# AI
AI_PROVIDER=openai
AI_API_KEY=
AI_MODEL=gpt-5.5
AI_TEMPERATURE=0.2
AI_MAX_TOKENS=8000

# Messaging
EVENT_BUS_PROVIDER=redis
REDIS_URL=redis://localhost:6379/0
```

---

# PARTE B. CONSTRUCCIÓN DEL BACKEND ORIENTADO A MICROSERVICIOS

---

## 4. Fase 2: Diseño de microservicios

### Objetivo

Construir servicios independientes, desplegables y reemplazables.

---

## 4.1 Microservicios mínimos

| Servicio | Responsabilidad | Puede cambiarse sin afectar todo |
|---|---|---|
| API Gateway | Exponer API única al frontend | Sí |
| Conversation Service | Manejar chat, sesiones y mensajes | Sí |
| Orchestrator Service | Coordinar workflows y eventos | Parcialmente |
| Agent Runtime Service | Ejecutar agentes CrewAI | Sí |
| Project Management Connector | Conectar con Jira u otro gestor | Sí |
| Version Control Connector | Conectar con GitHub/GitLab/Bitbucket | Sí |
| Deployment Connector | Conectar con Render/AWS/Azure/etc. | Sí |
| Policy Service | Validar arquitectura y buenas prácticas | Sí |
| Memory Service | Gestionar memoria semántica y contexto | Sí |
| Notification Service | Notificar resultados y aprobaciones | Sí |
| Identity/Auth Service | Autenticación y roles internos | Sí |

---

## 4.2 Comunicación recomendada

### Síncrona

Usar HTTP/REST para acciones que requieren respuesta inmediata:

```text
Frontend → API Gateway → Conversation Service
Orchestrator → Jira Connector
Orchestrator → Git Connector
```

### Asíncrona

Usar eventos para procesos largos:

```text
ISSUE_REFINED
ARCHITECTURE_APPROVED
DEVELOPMENT_STARTED
PULL_REQUEST_CREATED
QA_COMPLETED
RELEASE_APPROVED
DEPLOYMENT_COMPLETED
```

### Bus de eventos recomendado para prototipo

```text
Redis Streams
```

### Bus de eventos recomendado para producción

```text
Kafka, NATS o RabbitMQ
```

---

## 4.3 Contrato estándar de evento

```json
{
  "event_id": "evt_001",
  "event_type": "ISSUE_REFINED",
  "project_id": "DAS",
  "issue_key": "DAS-1",
  "correlation_id": "corr_abc123",
  "created_at": "2026-05-01T10:00:00Z",
  "source_service": "conversation-service",
  "payload": {
    "summary": "Historia refinada",
    "status": "READY_FOR_DEVELOPMENT"
  }
}
```

### Reglas

```text
event_id: único
correlation_id: agrupa todo lo relacionado con una historia o ejecución
source_service: servicio que emitió el evento
payload: contenido específico del evento
```

---

## 4.4 Contrato estándar de respuesta de servicio

```json
{
  "success": true,
  "data": {},
  "errors": [],
  "correlation_id": "corr_abc123"
}
```

---

## 4.5 Estructura de monorepo recomendada

Aunque uses microservicios, para un taller es más replicable iniciar con un monorepo.

```text
agentic-software-platform/
│
├── services/
│   ├── api-gateway/
│   ├── conversation-service/
│   ├── orchestrator-service/
│   ├── agent-runtime-service/
│   ├── jira-connector-service/
│   ├── git-connector-service/
│   ├── deploy-connector-service/
│   ├── policy-service/
│   ├── memory-service/
│   └── notification-service/
│
├── frontend/
│   └── web-chat/
│
├── shared/
│   ├── contracts/
│   ├── schemas/
│   └── clients/
│
├── infra/
│   ├── docker-compose.yml
│   ├── postgres/
│   ├── redis/
│   └── migrations/
│
├── docs/
│   ├── architecture/
│   ├── adr/
│   └── api/
│
├── .env.example
└── README.md
```

---

# PARTE C. CONSTRUCCIÓN DE CADA SERVICIO

---

## 5. API Gateway

### Propósito

Ser el único punto de entrada para el frontend.

### Responsabilidades

```text
- recibir mensajes del frontend
- enrutar al Conversation Service
- exponer decisiones pendientes
- consultar estado de workflows
- exponer eventos de progreso por WebSocket o SSE
```

### Endpoints mínimos

```text
POST /api/chat/message
GET  /api/projects
GET  /api/issues
GET  /api/workflows/{id}
POST /api/decisions/{id}/approve
POST /api/decisions/{id}/reject
GET  /api/events/stream
```

### Criterio de validación

El frontend nunca debe llamar directamente a Jira, Git, deploy o agentes. Siempre debe pasar por API Gateway.

---

## 6. Conversation Service

### Propósito

Gestionar la conversación humano ↔ PO Agent.

### Responsabilidades

```text
- guardar mensajes
- recuperar contexto
- identificar intención
- llamar al Orchestrator cuando una intención implique acción
- devolver respuesta conversacional
```

### Intenciones mínimas

```text
REFINE_ISSUE
ASK_PROJECT_STATUS
START_ARCHITECTURE_INCEPTION
APPROVE_ARCHITECTURE
START_DEVELOPMENT
REQUEST_QA
APPROVE_RELEASE
REQUEST_CHANGES
```

### Endpoint interno

```text
POST /conversation/message
```

### Request

```json
{
  "user_id": "u1",
  "project_key": "DAS",
  "issue_key": "DAS-1",
  "message": "Refina esta historia"
}
```

### Response

```json
{
  "assistant_message": "Necesito confirmar los campos obligatorios del registro.",
  "intent": "REFINE_ISSUE",
  "pending_decisions": [],
  "workflow_state": "REFINEMENT",
  "correlation_id": "corr_123"
}
```

---

## 7. Orchestrator Service

### Propósito

Coordinar el ciclo de vida del proyecto sin depender de proveedores específicos.

### Responsabilidades

```text
- ejecutar workflow
- emitir eventos
- llamar conectores
- llamar Agent Runtime
- aplicar gates humanos
- mantener estado
```

### Lo que NO debe hacer

```text
- no debe tener código específico de Jira
- no debe tener código específico de GitHub
- no debe tener código específico del proveedor cloud
- no debe contener prompts extensos
```

### Máquina de estados principal

```text
BACKLOG
→ REFINEMENT
→ NFR_CAPTURE
→ ARCHITECTURE_INCEPTION
→ ARCHITECTURE_APPROVAL_PENDING
→ READY_FOR_DEVELOPMENT
→ DEVELOPMENT
→ CODE_REVIEW
→ QA
→ PO_REVIEW
→ RELEASE_APPROVAL_PENDING
→ STAGING_DEPLOYMENT
→ PRODUCTION_DEPLOYMENT
→ RELEASED
```

### Endpoints internos

```text
POST /orchestrator/commands
GET  /orchestrator/workflows/{workflow_id}
POST /orchestrator/events
```

### Comando estándar

```json
{
  "command": "START_DEVELOPMENT",
  "project_key": "DAS",
  "issue_key": "DAS-1",
  "requested_by": "human",
  "correlation_id": "corr_123"
}
```

---

## 8. Agent Runtime Service

### Propósito

Ejecutar agentes CrewAI de manera desacoplada del orquestador.

### Agentes mínimos

```text
PO Agent
Scrum Master Agent
NFR Agent
Architecture Agent
Developer Agent
Code Review Agent
QA Agent
Security Agent
DevOps Agent
Release Agent
```

### Endpoint interno

```text
POST /agents/run
```

### Request

```json
{
  "agent_name": "architecture_agent",
  "task": "PROPOSE_ARCHITECTURE",
  "input": {
    "project_key": "DAS",
    "functional_requirements": [],
    "non_functional_requirements": {},
    "constraints": {}
  },
  "correlation_id": "corr_123"
}
```

### Response

```json
{
  "agent_name": "architecture_agent",
  "status": "completed",
  "output": {
    "recommended_architecture": "modular_monolith",
    "patterns": ["clean_architecture", "repository", "service_layer"],
    "risks": [],
    "artifacts": []
  }
}
```

### Justificación técnica

CrewAI Flows es útil para workflows estructurados con estado, pero en este diseño los Flows pueden vivir dentro del Agent Runtime o del Orchestrator. Para mantener escalabilidad, el orquestador debe invocar agentes por contrato y no importar directamente sus clases.

---

## 9. Project Management Connector Service

### Propósito

Aislar Jira detrás de un contrato genérico.

### Contrato genérico

```text
GET  /pm/projects
GET  /pm/issues/{issue_key}
POST /pm/issues
PATCH /pm/issues/{issue_key}
POST /pm/issues/{issue_key}/comments
POST /pm/issues/{issue_key}/transition
GET  /pm/sprints
```

### Implementación inicial

```text
JiraProjectManagementConnector
```

### Cambio futuro

Puedes reemplazarlo por:

```text
AzureDevOpsConnector
LinearConnector
TrelloConnector
```

Sin cambiar el Orchestrator.

---

## 10. Version Control Connector Service

### Propósito

Aislar GitHub, GitLab o Bitbucket detrás de un contrato común.

### Contrato genérico

```text
POST /vcs/branches
GET  /vcs/files
PUT  /vcs/files
POST /vcs/commits
POST /vcs/pull-requests
POST /vcs/pull-requests/{id}/comments
POST /vcs/pull-requests/{id}/merge
GET  /vcs/pull-requests/{id}/checks
```

### Implementación inicial

```text
GitHubConnector
```

### Cambio futuro

```text
GitLabConnector
BitbucketConnector
```

---

## 11. Deployment Connector Service

### Propósito

Aislar el proveedor de despliegue.

### Contrato genérico

```text
POST /deploy/staging
POST /deploy/production
POST /deploy/rollback
GET  /deploy/status/{deployment_id}
```

### Implementaciones posibles

```text
DockerLocalDeployConnector
RenderDeployConnector
RailwayDeployConnector
AWSDeployConnector
AzureDeployConnector
GCPDeployConnector
```

---

## 12. Policy Service

### Propósito

Convertir buenas prácticas en reglas verificables.

### Artefactos

```text
architecture-policy.yaml
quality-gates.yaml
security-policy.yaml
twelve-factor-policy.yaml
```

### Endpoint

```text
POST /policy/evaluate
```

### Request

```json
{
  "project_key": "DAS",
  "issue_key": "DAS-1",
  "artifact_type": "pull_request",
  "artifact_reference": "PR-12",
  "policies": [
    "architecture-policy",
    "quality-gates",
    "security-policy",
    "twelve-factor-policy"
  ]
}
```

### Response

```json
{
  "status": "failed",
  "violations": [
    {
      "policy": "architecture-policy",
      "rule": "business_logic_must_not_be_in_controller",
      "severity": "high",
      "message": "Se detectó lógica de negocio en el controlador."
    }
  ]
}
```

---

## 13. Memory Service

### Propósito

Centralizar memoria de proyecto y recuperación de contexto.

### Responsabilidades

```text
- guardar decisiones
- guardar ADR
- indexar documentación
- recuperar contexto relevante para agentes
- separar memoria por proyecto
```

### Endpoints

```text
POST /memory/documents
POST /memory/search
GET  /memory/projects/{project_key}/context
```

---

# PARTE D. INTERFAZ WEB CONVERSACIONAL Y FORMULARIO NFR

---

## 14. Fase 3: Construcción del frontend web

### Objetivo

Construir una interfaz web sencilla para que el humano pueda dirigir el proyecto sin conocer Jira API, Git API ni comandos técnicos.

---

## 14.1 Pantallas mínimas

```text
1. Login o identificación básica
2. Selector de proyecto
3. Chat conversacional
4. Formulario de requerimientos no funcionales
5. Panel de arquitectura propuesta
6. Panel de decisiones pendientes
7. Panel de estado de agentes
8. Panel de evidencias
```

---

## 14.2 Pantalla de chat

Debe permitir:

```text
- escribir mensajes
- seleccionar historia Jira
- ver respuesta del PO Agent
- ver acciones sugeridas
- activar refinamiento
- iniciar desarrollo
- solicitar estado
```

Diseño sugerido:

```text
┌──────────────────────────────────────────────┐
│ Proyecto: DAS        Historia: DAS-1         │
├──────────────────────────────────────────────┤
│ Chat                                         │
│ Humano: Refina DAS-1                         │
│ PO Agent: Necesito confirmar reglas...       │
├──────────────────────────────────────────────┤
│ Acciones                                     │
│ [Refinar] [Definir arquitectura] [Desarrollar]│
└──────────────────────────────────────────────┘
```

---

## 14.3 Formulario web de requerimientos no funcionales

### Propósito

El humano no tiene que saber arquitectura. Solo debe responder preguntas simples o escribir restricciones.

### Campos recomendados

#### Escalabilidad

```text
Usuarios esperados inicialmente:
[ texto ]

¿Debe soportar crecimiento alto?
[ Sí ] [ No ] [ No sé ]

Usuarios concurrentes estimados:
[ texto ]
```

#### Disponibilidad

```text
¿Debe funcionar 24/7?
[ Sí ] [ No ] [ No sé ]

Tiempo máximo tolerable de caída:
[ texto ]
```

#### Seguridad

```text
¿Maneja datos sensibles?
[ Sí ] [ No ] [ No sé ]

¿Requiere autenticación?
[ Sí ] [ No ]

¿Requiere roles/permisos?
[ Sí ] [ No ]

¿Requiere auditoría?
[ Sí ] [ No ]
```

#### Integraciones

```text
¿Debe integrarse con otros sistemas?
[ Sí ] [ No ]

¿Cuáles?
[ texto ]
```

#### Rendimiento

```text
Tiempo de respuesta esperado:
[ texto ]

¿Hay operaciones pesadas?
[ Sí ] [ No ] [ No sé ]
```

#### Despliegue

```text
Lugar preferido de despliegue:
[ Local ] [ Cloud ] [ Web estática ] [ No sé ]

Presupuesto aproximado:
[ texto ]
```

#### Mantenibilidad

```text
¿El sistema será mantenido por varios desarrolladores?
[ Sí ] [ No ] [ No sé ]

¿Debe ser fácil agregar módulos?
[ Sí ] [ No ]
```

---

## 14.4 JSON generado por el formulario

```json
{
  "project_key": "DAS",
  "scalability": {
    "expected_users": "1000 inicialmente",
    "high_growth": true,
    "concurrent_users": "100"
  },
  "availability": {
    "requires_24_7": false,
    "max_downtime": "4 horas mensuales"
  },
  "security": {
    "sensitive_data": true,
    "authentication_required": true,
    "roles_required": true,
    "audit_required": true
  },
  "integrations": {
    "required": true,
    "systems": ["Jira", "pasarela de pagos"]
  },
  "performance": {
    "expected_response_time": "menos de 2 segundos",
    "heavy_operations": false
  },
  "deployment": {
    "target": "cloud",
    "budget": "bajo"
  },
  "maintainability": {
    "multiple_developers": true,
    "easy_modules": true
  }
}
```

---

## 15. Fase 4: Definición de arquitectura asistida

### Objetivo

Usar requisitos funcionales, NFR y restricciones para que el Architecture Agent proponga una arquitectura.

---

## 15.1 Flujo

```text
Humano diligencia formulario NFR
→ Conversation Service guarda respuestas
→ Orchestrator emite NFR_CAPTURED
→ Agent Runtime ejecuta Architecture Agent
→ Architecture Agent propone arquitectura
→ Humano aprueba o solicita cambios
→ Policy Service genera reglas
→ Memory Service guarda ADR y políticas
```

---

## 15.2 Decisiones que debe proponer el Architecture Agent

```text
- estilo arquitectónico
- estructura del repositorio
- patrones de diseño
- base de datos
- estrategia de autenticación
- estrategia de logs
- estrategia de pruebas
- estrategia de despliegue
- riesgos
- costos aproximados
```

---

## 15.3 Ejemplo de salida

```json
{
  "architecture": {
    "style": "modular_monolith",
    "reason": "El proyecto requiere modularidad, pero aún no justifica microservicios en el software objetivo.",
    "patterns": [
      "clean_architecture",
      "repository_pattern",
      "service_layer",
      "dependency_injection"
    ],
    "database": "postgresql",
    "auth": "jwt_with_role_based_access_control",
    "deployment": "docker_to_cloud_staging_and_production"
  },
  "risks": [
    "Manejo de datos sensibles requiere auditoría y control de acceso."
  ],
  "human_approval_required": true
}
```

---

## 15.4 Artefactos generados

```text
/docs/architecture/overview.md
/docs/architecture/non-functional-requirements.md
/docs/adr/ADR-001-architecture-style.md
/docs/adr/ADR-002-database-choice.md
/docs/adr/ADR-003-authentication-strategy.md
architecture-policy.yaml
quality-gates.yaml
security-policy.yaml
twelve-factor-policy.yaml
```

---

# PARTE E. APLICACIÓN DE BUENAS PRÁCTICAS

---

## 16. Fase 5: Políticas ejecutables

### Objetivo

Evitar que las buenas prácticas dependan solo del prompt del agente.

---

## 16.1 `architecture-policy.yaml`

```yaml
architecture:
  style: modular_monolith
  layers:
    - presentation
    - application
    - domain
    - infrastructure

rules:
  - id: no_business_logic_in_controllers
    description: Los controladores no deben contener lógica de negocio.
    severity: high

  - id: repository_for_persistence
    description: El acceso a datos debe pasar por repositorios.
    severity: high

  - id: dependency_injection_required
    description: Las dependencias deben inyectarse, no instanciarse directamente en lógica de negocio.
    severity: medium
```

---

## 16.2 `twelve-factor-policy.yaml`

```yaml
twelve_factor:
  config:
    env_variables_required: true
    hardcoded_secrets_forbidden: true

  dependencies:
    explicit_manifest_required: true

  logs:
    stdout_required: true

  processes:
    stateless_required: true

  build_release_run:
    separated: true
```

Los 12 factores incluyen principios como configuración en el entorno, dependencias explícitas, separación build/release/run, procesos stateless y logs como flujos de eventos.

---

## 16.3 `quality-gates.yaml`

```yaml
quality_gates:
  pull_request:
    required:
      - architecture_policy_passed
      - unit_tests_passed
      - integration_tests_passed
      - security_review_passed
      - no_high_severity_violations

  release:
    required:
      - staging_deploy_successful
      - qa_validation_passed
      - human_approval
```

---

## 16.4 Flujo de validación

```text
Developer Agent genera código
→ Git Connector abre PR
→ Orchestrator emite PULL_REQUEST_CREATED
→ Policy Service evalúa PR
→ Code Review Agent revisa arquitectura
→ Security Agent revisa seguridad
→ QA Agent ejecuta pruebas
→ Quality Gate decide
```

---

# PARTE F. EJECUCIÓN DEL CICLO DE VIDA

---

## 17. Fase 6: Flujo operativo completo

### 17.1 Creación y refinamiento

```text
Humano crea historia en Jira
→ Jira webhook informa al Project Management Connector
→ Connector emite ISSUE_CREATED
→ Orchestrator registra workflow
→ Humano conversa con PO Agent
→ PO Agent refina la historia
→ Connector actualiza Jira
```

---

### 17.2 Captura NFR y arquitectura

```text
Humano diligencia formulario NFR
→ Architecture Agent propone arquitectura
→ Humano aprueba
→ Policy Service crea políticas
→ Memory Service guarda ADR
```

---

### 17.3 Desarrollo

```text
Humano indica: Iniciar desarrollo de DAS-1
→ Orchestrator verifica que existe arquitectura aprobada
→ Developer Agent genera cambios
→ Git Connector crea rama
→ Git Connector crea commit
→ Git Connector abre PR
→ Jira pasa a Code Review
```

---

### 17.4 Revisión

```text
PR creado
→ Policy Service evalúa arquitectura
→ Code Review Agent revisa patrones
→ Security Agent revisa seguridad
→ QA Agent valida criterios
→ resultados se comentan en PR y Jira
```

---

### 17.5 Aprobación humana

```text
PO Agent resume evidencia
→ humano acepta o solicita cambios
→ Orchestrator continúa o devuelve a desarrollo
```

---

### 17.6 Despliegue

```text
Humano aprueba release
→ Deploy Connector despliega staging
→ QA valida staging
→ humano aprueba producción
→ Deploy Connector despliega producción
→ Jira pasa a Released
```

---

# PARTE G. ESCALABILIDAD Y EXTENSIBILIDAD

---

## 18. Agregar un nuevo conector sin cambiar el núcleo

### Ejemplo: cambiar GitHub por GitLab

1. Crear nuevo servicio:

```text
gitlab-connector-service
```

2. Implementar el mismo contrato:

```text
POST /vcs/branches
POST /vcs/pull-requests
POST /vcs/pull-requests/{id}/merge
```

3. Cambiar configuración:

```env
GIT_PROVIDER=gitlab
GIT_CONNECTOR_URL=http://gitlab-connector-service:8010
```

4. No modificar:

```text
Conversation Service
Orchestrator Service
Agent Runtime Service
Frontend
Policy Service
```

---

## 19. Agregar un nuevo agente

### Ejemplo: Performance Agent

1. Crear agente en Agent Runtime:

```text
performance_agent
```

2. Registrar en configuración:

```yaml
agents:
  - name: performance_agent
    triggers:
      - PULL_REQUEST_CREATED
      - STAGING_DEPLOYED
```

3. Agregar política:

```yaml
performance:
  max_response_time_ms: 2000
  load_test_required: true
```

4. El orquestador solo emite eventos. No necesita conocer la lógica interna del agente.

---

## 20. Agregar un nuevo proveedor de despliegue

### Ejemplo: AWS

1. Crear `aws-deploy-connector-service`.
2. Implementar contrato genérico:

```text
POST /deploy/staging
POST /deploy/production
POST /deploy/rollback
GET /deploy/status/{deployment_id}
```

3. Cambiar `.env`:

```env
DEPLOY_PROVIDER=aws
DEPLOY_CONNECTOR_URL=http://aws-deploy-connector-service:8020
```

---

# PARTE H. DESPLIEGUE LOCAL DEL TALLER

---

## 21. Docker Compose mínimo

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: agent_platform
      POSTGRES_USER: agent
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8080:8080"
    env_file:
      - .env

  conversation-service:
    build: ./services/conversation-service
    env_file:
      - .env

  orchestrator-service:
    build: ./services/orchestrator-service
    env_file:
      - .env

  agent-runtime-service:
    build: ./services/agent-runtime-service
    env_file:
      - .env

  jira-connector-service:
    build: ./services/jira-connector-service
    env_file:
      - .env

  git-connector-service:
    build: ./services/git-connector-service
    env_file:
      - .env

  deploy-connector-service:
    build: ./services/deploy-connector-service
    env_file:
      - .env

  policy-service:
    build: ./services/policy-service
    env_file:
      - .env

  memory-service:
    build: ./services/memory-service
    env_file:
      - .env

  frontend:
    build: ./frontend/web-chat
    ports:
      - "3000:3000"
    env_file:
      - .env
```

---

## 22. Orden de ejecución

```bash
cp .env.example .env
docker compose up -d postgres redis
docker compose up --build
```

Validar:

```text
Frontend: http://localhost:3000
API Gateway: http://localhost:8080/health
```

---

# PARTE I. CRITERIOS DE VALIDACIÓN

---

## 23. Validación funcional

El sistema está correctamente construido si:

```text
1. El usuario puede escribir en el chat.
2. El PO Agent responde.
3. El usuario puede diligenciar NFR en formulario web.
4. Architecture Agent propone arquitectura.
5. El humano puede aprobar arquitectura.
6. Se generan ADR y políticas.
7. El sistema puede leer una historia de Jira.
8. El sistema puede actualizar Jira.
9. El sistema puede crear rama en Git.
10. El sistema puede abrir PR.
11. El Policy Service puede aprobar o rechazar un PR.
12. El sistema puede desplegar en staging.
13. El sistema pide aprobación humana antes de producción.
```

---

## 24. Validación de extensibilidad

El sistema es extensible si puedes:

```text
1. Cambiar GitHub por GitLab implementando solo un nuevo conector.
2. Cambiar Jira por otro gestor implementando solo otro Project Management Connector.
3. Agregar un nuevo agente registrándolo en configuración.
4. Agregar una nueva política sin modificar el orquestador.
5. Agregar un nuevo proveedor de despliegue sin cambiar frontend ni conversación.
```

---

## 25. Validación de seguridad mínima

```text
- No hay secretos en código fuente.
- Todo secreto está en variables de entorno o gestor de secretos.
- El usuario técnico de Jira tiene permisos mínimos.
- El token Git tiene permisos mínimos.
- Producción requiere aprobación humana.
- Rollback requiere aprobación humana.
- Las decisiones quedan auditadas.
```

---

# PARTE J. RESUMEN FINAL

---

## 26. Qué se construye

```text
Una plataforma conversacional multiagente para desarrollo de software,
con backend orientado a microservicios,
con conectores intercambiables,
con arquitectura definida por NFR,
con buenas prácticas convertidas en políticas,
y con Product Owner humano en decisiones críticas.
```

---

## 27. Qué no debe hacerse

```text
No conectar todos los agentes directamente a Jira.
No poner lógica de Jira dentro del orquestador.
No poner lógica de GitHub dentro del orquestador.
No depender solo de prompts para buenas prácticas.
No permitir despliegue a producción sin aprobación humana.
No guardar secretos en código.
```

---

## 28. Arquitectura final deseada

```text
Frontend conversacional
→ API Gateway
→ Conversation Service
→ Orchestrator Service
→ servicios conectores independientes
→ Agent Runtime Service
→ Policy Service
→ Memory Service
→ Jira / Git / Deploy
```

Este diseño permite que cada servicio evolucione, se reemplace o escale de forma independiente sin modificar todo el proyecto.
