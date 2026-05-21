# ScrumDev AI

## Plataforma Multiagente para Desarrollo Ágil de Software

ScrumDev AI es una plataforma basada en agentes de inteligencia artificial orientada a automatizar y acelerar el ciclo de vida del desarrollo de software utilizando Scrum, microservicios y workflows durables. El sistema integra agentes especializados capaces de colaborar para realizar refinamiento de historias, generación de código, validación técnica y despliegue automatizado, manteniendo siempre al humano dentro del proceso de decisión.

La plataforma está diseñada para facilitar la construcción rápida de Productos Mínimos Viables (PMV/MVP) mediante una arquitectura desacoplada y extensible basada en FastAPI, Temporal y CrewAI. Gracias al uso de microservicios y agentes especializados, ScrumDev AI permite iterar rápidamente sobre requisitos, integrar nuevas tecnologías y evolucionar el sistema sin necesidad de reconstruir toda la arquitectura.

---

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/aedde8eb-acff-48a2-a072-8f58edea0ef1" />


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

# Stack Tecnológico

| Área | Tecnología |
|---|---|
| Frontend | Next.js |
| Backend | FastAPI |
| Orquestación | Temporal |
| Agentes IA | CrewAI |
| Base de datos | PostgreSQL |
| Cache | Redis |
| Eventos | RabbitMQ |
| Infraestructura | Docker |

---

# Ruta de Construcción

| Taller | Objetivo |
|---|---|
| [Taller 1](./taller_1_configuracion_integraciones.md) | Configuración inicial e integraciones |
| [Taller 2](./taller_2_backend_base.md) | Infraestructura y backend base |
| [Taller 3](./taller_3_runtime_agentes.md) | Runtime de agentes y workflows |
| [Taller 4](./taller_4_frontend.md) | Frontend conversacional |
| [Taller 5](./taller_5_integracion_testing.md) | Integración y pruebas |
| [Taller 6](./taller_6_devops_despliegue.md) | DevOps y despliegue |

---

# Principios Arquitectónicos

```text
microservicios
desacoplamiento
workflows durables
arquitectura orientada a eventos
human-in-the-loop
12-factor app
escalabilidad
extensibilidad
```

---

# Resultado Esperado

Al finalizar los talleres se tendrá una plataforma capaz de:

```text
coordinar agentes especializados
gestionar historias Scrum
generar software automáticamente
validar calidad
automatizar despliegues
mantener trazabilidad completa
```



