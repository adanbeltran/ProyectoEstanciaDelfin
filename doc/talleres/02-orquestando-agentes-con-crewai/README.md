# ScrumDev AI

## Plataforma Multiagente para Desarrollo Ágil de Software

ScrumDev AI es una plataforma orientada a la automatización inteligente del ciclo de vida del desarrollo de software utilizando agentes de inteligencia artificial, microservicios, workflows durables y principios DevOps. El sistema integra agentes especializados capaces de colaborar entre sí para realizar refinamiento Scrum, generación de artefactos técnicos, generación de código, validación de calidad, revisión de seguridad y despliegue automatizado, manteniendo siempre al humano dentro del ciclo de decisión y aprobación. La plataforma utiliza una arquitectura desacoplada basada en FastAPI, Temporal y CrewAI, permitiendo construir sistemas extensibles, mantenibles y escalables.

La plataforma está diseñada especialmente para acelerar la construcción de Productos Mínimos Viables (PMV/MVP) reduciendo tiempos de análisis, desarrollo y despliegue sin sacrificar calidad técnica ni buenas prácticas de ingeniería. ScrumDev AI busca disminuir el tiempo entre la idea y la publicación funcional de un sistema, permitiendo iteraciones rápidas sobre requisitos funcionales y no funcionales. Gracias al uso de workflows distribuidos, microservicios y agentes especializados, la plataforma puede evolucionar progresivamente y adaptarse rápidamente a nuevos requerimientos, integraciones o arquitecturas tecnológicas sin necesidad de reconstruir completamente el sistema.

---

# Objetivos del Proyecto

ScrumDev AI busca construir una plataforma capaz de:

```text
automatizar parcialmente el SDLC
coordinar agentes especializados
integrar Scrum con IA
generar software basado en historias
mantener trazabilidad completa
automatizar despliegues
aplicar buenas prácticas arquitectónicas
permitir aprobación humana
facilitar construcción rápida de MVP
```

---

# Arquitectura General

```text
Frontend
→ API Gateway
→ Conversation Service
→ Orchestrator Service
→ Temporal Workflow
→ Agent Runtime Service
→ Connector Services
→ Jira / Git / Deploy
```

---

# Principios Arquitectónicos

La plataforma se construye bajo los siguientes principios:

```text
microservicios
desacoplamiento
workflows durables
arquitectura orientada a eventos
human-in-the-loop
12-factor app
observabilidad
escalabilidad
extensibilidad
```

---

# Stack Tecnológico

| Área | Tecnología |
|---|---|
| Frontend | Next.js |
| Backend | FastAPI |
| Orquestación | Temporal |
| Framework de agentes | CrewAI |
| Base de datos | PostgreSQL |
| Cache y locks | Redis |
| Broker de eventos | RabbitMQ |
| Memoria semántica | PGVector / ChromaDB |
| Infraestructura | Docker |
| Gestión Dependencias | Poetry |

---

# Organización Académica de los Talleres

El proyecto completo se encuentra dividido en seis talleres progresivos. Cada taller desarrolla una capa específica de ScrumDev AI y debe realizarse en el orden propuesto para mantener coherencia arquitectónica y pedagógica.

---

# Taller 1 — Configuración Inicial e Integraciones

Archivo:

```text
taller_1_configuracion_integraciones.md
```

## Objetivo

Preparar todas las integraciones externas necesarias para el funcionamiento de ScrumDev AI y construir la configuración inicial del entorno.

## Contenido principal

```text
visión general del sistema
obtención API Keys
integración Jira
integración Git
integración IA
integración despliegue
configuración PostgreSQL
construcción .env
separación variables entorno
12-factor app
```

## Acceso

[Taller 1 - Configuración Inicial e Integraciones](./taller_1_configuracion_integraciones.md)

---

# Taller 2 — Infraestructura y Backend Base

Archivo:

```text
taller_2_backend_base.md
```

## Objetivo

Construir la infraestructura distribuida y los servicios base del backend.

## Contenido principal

```text
Docker
Docker Compose
PostgreSQL
Redis
RabbitMQ
Temporal
FastAPI
API Gateway
Conversation Service
Orchestrator Service
```

## Acceso

[Taller 2 - Infraestructura y Backend Base](./taller_2_backend_base.md)

---

# Taller 3 — Runtime de Agentes y Orquestación

Archivo:

```text
taller_3_runtime_agentes.md
```

## Objetivo

Construir el núcleo inteligente de ScrumDev AI utilizando agentes IA y workflows durables.

## Contenido principal

```text
CrewAI
PO Agent
Architect Agent
Developer Agent
QA Agent
Temporal workflows
memoria semántica
policy service
audit service
eventos
```

## Acceso

[Taller 3 - Runtime de Agentes](./taller_3_runtime_agentes.md)

---

# Taller 4 — Frontend Conversacional

Archivo:

```text
taller_4_frontend.md
```

## Objetivo

Construir la interfaz humano ↔ agentes para interacción conversacional y monitoreo del sistema.

## Contenido principal

```text
Next.js
chat conversacional
formularios NFR
panel workflows
panel agentes
WebSockets
consumo APIs
autenticación frontend
```

## Acceso

[Taller 4 - Frontend Conversacional](./taller_4_frontend.md)

---

# Taller 5 — Integración Completa y Testing

Archivo:

```text
taller_5_integracion_testing.md
```

## Objetivo

Integrar todos los componentes y validar el funcionamiento end-to-end de la plataforma.

## Contenido principal

```text
integración frontend-backend
integración Jira
integración Git
testing unitario
testing integración
testing e2e
observabilidad
logs
métricas
tracing
```

## Acceso

[Taller 5 - Integración y Testing](./taller_5_integracion_testing.md)

---

# Taller 6 — DevOps y Despliegue

Archivo:

```text
taller_6_devops_despliegue.md
```

## Objetivo

Automatizar despliegues y preparar ScrumDev AI para ambientes productivos.

## Contenido principal

```text
CI/CD
GitHub Actions
deploy backend
deploy frontend
Docker producción
Render
Railway
AWS
rollback
monitoring
```

## Acceso

[Taller 6 - DevOps y Despliegue](./taller_6_devops_despliegue.md)

---

# Flujo General de Construcción

```text
1. Configurar integraciones y entornos
2. Construir infraestructura backend
3. Construir runtime de agentes
4. Construir frontend
5. Integrar y validar
6. Automatizar despliegues
```

---

# Resultado Esperado

Al finalizar todos los talleres se tendrá una plataforma capaz de:

```text
interactuar con humanos mediante conversación
coordinar agentes especializados
gestionar historias Scrum
generar código
validar calidad
crear pull requests
automatizar despliegues
mantener trazabilidad completa
```

---

# Licencia Recomendada

```text
MIT License
```

---

# Nombre del Proyecto

```text
ScrumDev AI
```
