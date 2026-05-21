# Taller 6 — DevOps y Despliegue

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/58364c74-7d3a-4dfd-9677-4d24e353e8db" />


---

# FASE 1. INTRODUCCIÓN A DEVOPS Y DESPLIEGUE

---

## 1.1 Objetivo de la Fase

En este taller se automatizará el despliegue de ScrumDev AI utilizando contenedores, pipelines CI/CD y ambientes cloud. El objetivo es preparar la plataforma para ambientes productivos manteniendo reproducibilidad, automatización y escalabilidad.

A diferencia de los talleres anteriores, donde el sistema se ejecutaba principalmente en ambiente local, aquí se preparará ScrumDev AI para operar en infraestructura cloud moderna.

---

## 1.2 Comprender el Flujo DevOps

El flujo DevOps del sistema será:

```text
GitHub
→ GitHub Actions
→ Docker Build
→ Testing
→ Deploy Automático
→ Ambiente Cloud
```

Arquitectura conceptual:

```text
Developer
→ GitHub Repository
→ CI/CD Pipeline
→ Docker Images
→ Cloud Provider
→ Frontend + Backend + Infraestructura
```

---

# FASE 2. DOCKERIZACIÓN COMPLETA DEL SISTEMA

---

## 2.1 Objetivo de la Fase

Todos los microservicios deben ejecutarse mediante contenedores Docker para garantizar portabilidad y despliegues consistentes.

---

## 2.2 Crear Dockerfile API Gateway

Crear archivo:

```bash
touch services/api-gateway/Dockerfile
```

Agregar:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

COPY . /app

CMD ["uvicorn", "services.api-gateway.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 2.3 Crear Dockerfile Conversation Service

Crear archivo:

```bash
touch services/conversation-service/Dockerfile
```

Agregar:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

COPY . /app

CMD ["uvicorn", "services.conversation-service.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

## 2.4 Dockerizar Frontend

Crear archivo:

```bash
touch frontend/web-chat/Dockerfile
```

Agregar:

```dockerfile
FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

CMD ["npm", "start"]
```

---

## 2.5 Comprender la Dockerización

Docker permitirá:

```text
aislamiento
portabilidad
consistencia
despliegue reproducible
```

---

# FASE 3. DOCKER COMPOSE DE PRODUCCIÓN

---

## 3.1 Objetivo de la Fase

Se construirá un ambiente integrado para ejecutar todos los servicios coordinadamente.

---

## 3.2 Crear Archivo `docker-compose.prod.yml`

Crear archivo:

```bash
touch docker-compose.prod.yml
```

Agregar:

```yaml
services:

  api-gateway:
    build:
      context: .
      dockerfile: services/api-gateway/Dockerfile
    ports:
      - "8080:8080"

  conversation-service:
    build:
      context: .
      dockerfile: services/conversation-service/Dockerfile
    ports:
      - "8001:8001"

  frontend:
    build:
      context: ./frontend/web-chat
    ports:
      - "3000:3000"

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: scrumdev
      POSTGRES_PASSWORD: scrumdev
      POSTGRES_DB: scrumdev_ai

  redis:
    image: redis:7

  rabbitmq:
    image: rabbitmq:3-management
```

---

## 3.3 Levantar Ambiente Completo

Ejecutar:

```bash
docker compose -f docker-compose.prod.yml up --build
```

---

## 3.4 Verificar Contenedores

Ejecutar:

```bash
docker ps
```

Verificar:

```text
frontend
api-gateway
conversation-service
postgres
redis
rabbitmq
```

---

# FASE 4. CONFIGURACIÓN DE GITHUB ACTIONS

---

## 4.1 Objetivo de la Fase

GitHub Actions automatizará testing, build y despliegues.

---

## 4.2 Crear Carpeta Workflows

Ejecutar:

```bash
mkdir -p .github/workflows
```

---

## 4.3 Crear Pipeline CI/CD

Crear archivo:

```bash
touch .github/workflows/ci-cd.yml
```

Agregar:

```yaml
name: ScrumDev AI CI/CD

on:
  push:
    branches:
      - main

jobs:

  test:

    runs-on: ubuntu-latest

    steps:

      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Poetry
        run: pip install poetry

      - name: Install Dependencies
        run: poetry install

      - name: Run Tests
        run: poetry run pytest

  docker-build:

    needs: test

    runs-on: ubuntu-latest

    steps:

      - name: Checkout
        uses: actions/checkout@v4

      - name: Build Containers
        run: docker compose -f docker-compose.prod.yml build
```

---

## 4.4 Comprender CI/CD

El pipeline permitirá:

```text
automatizar pruebas
validar código
generar imágenes
automatizar despliegues
```

---

# FASE 5. DESPLIEGUE DEL BACKEND EN RENDER

---

## 5.1 Objetivo de la Fase

Render será utilizado para desplegar los servicios backend cloud.

---

## 5.2 Crear Nuevo Web Service

Ingresar:

```text
https://render.com
```

Seleccionar:

```text
New
→ Web Service
```

---

## 5.3 Conectar GitHub

Seleccionar:

```text
Connect Repository
```

Seleccionar repositorio:

```text
scrumdev-ai
```

---

## 5.4 Configurar Servicio

Configurar:

```text
Environment: Docker
Branch: main
Root Directory: /
```

---

## 5.5 Agregar Variables Entorno

Agregar:

```env
SCRUMDEV_AI_API_KEY=
SCRUMDEV_DATABASE_URL=
SCRUMDEV_JIRA_API_TOKEN=
SCRUMDEV_GIT_TOKEN=
```

---

## 5.6 Ejecutar Deploy

Seleccionar:

```text
Create Web Service
```

Esperar despliegue.

---

# FASE 6. DESPLIEGUE DEL FRONTEND EN VERCEL

---

## 6.1 Objetivo de la Fase

Vercel permitirá desplegar el frontend Next.js.

---

## 6.2 Crear Cuenta Vercel

Ingresar:

```text
https://vercel.com
```

---

## 6.3 Importar Proyecto

Seleccionar:

```text
Add New Project
```

Importar:

```text
scrumdev-ai
```

---

## 6.4 Configurar Frontend

Seleccionar:

```text
Root Directory:
frontend/web-chat
```

---

## 6.5 Configurar Variables Entorno

Agregar:

```env
NEXT_PUBLIC_API_GATEWAY_URL=
NEXT_PUBLIC_WS_URL=
```

---

## 6.6 Ejecutar Deploy

Seleccionar:

```text
Deploy
```

---

# FASE 7. CONFIGURACIÓN DE DOMINIOS

---

## 7.1 Objetivo de la Fase

La plataforma debe poder exponerse mediante URLs públicas.

---

## 7.2 Configurar Dominio Frontend

Ejemplo:

```text
app.scrumdev-ai.com
```

---

## 7.3 Configurar Dominio API

Ejemplo:

```text
api.scrumdev-ai.com
```

---

## 7.4 Comprender Separación Dominios

Separar frontend y backend mejora:

```text
seguridad
escalabilidad
balanceo
mantenibilidad
```

---

# FASE 8. CONFIGURACIÓN DE HTTPS

---

## 8.1 Objetivo de la Fase

Toda comunicación debe realizarse utilizando HTTPS.

---

## 8.2 Activar HTTPS

Render y Vercel generan HTTPS automáticamente.

Verificar:

```text
https://
```

en URLs finales.

---

## 8.3 Comprender HTTPS

HTTPS protege:

```text
tokens
credenciales
cookies
mensajes
```

---

# FASE 9. CONFIGURACIÓN DE OBSERVABILIDAD

---

## 9.1 Objetivo de la Fase

La plataforma debe poder monitorearse en producción.

---

## 9.2 Configurar Logs Render

Dentro de Render abrir:

```text
Logs
```

Verificar:

```text
errores
warnings
requests
```

---

## 9.3 Configurar Métricas

Verificar:

```text
CPU
RAM
requests
latencia
```

---

## 9.4 Comprender Observabilidad

La observabilidad permitirá:

```text
debugging
monitoring
auditoría
detección fallos
```

---

# FASE 10. HARDENING BÁSICO

---

## 10.1 Objetivo de la Fase

Aplicar medidas mínimas de seguridad para ambientes productivos.

---

## 10.2 Deshabilitar Debug

Verificar:

```env
APP_DEBUG=false
```

---

## 10.3 Proteger Variables Sensibles

Nunca subir:

```text
.env
tokens
API keys
```

---

## 10.4 Rotar Credenciales

Rotar periódicamente:

```text
Jira Tokens
GitHub Tokens
OpenAI Keys
Deploy Tokens
```

---

## 10.5 Comprender Hardening

El hardening reduce:

```text
vulnerabilidades
filtraciones
riesgos cloud
```

---

# FASE 11. ESTRATEGIA DE AMBIENTES

---

## 11.1 Objetivo de la Fase

Separar ambientes para evitar errores de despliegue.

---

## 11.2 Definir Ambientes

Ambientes recomendados:

```text
local
development
staging
production
```

---

## 11.3 Crear Variables por Ambiente

Ejemplo:

```env
.env.local
.env.staging
.env.production
```

---

## 11.4 Comprender Separación Ambientes

Permite:

```text
pruebas seguras
rollback
validación progresiva
```

---

# FASE 12. AUTOMATIZACIÓN DE DEPLOY

---

## 12.1 Objetivo de la Fase

El sistema debe desplegar automáticamente después de cada push estable.

---

## 12.2 Configurar Auto Deploy Render

Dentro de Render habilitar:

```text
Auto Deploy
```

---

## 12.3 Configurar Auto Deploy Vercel

Vercel despliega automáticamente al detectar cambios en GitHub.

---

## 12.4 Comprender Automatización

Permite:

```text
entrega continua
integración continua
feedback rápido
```

---

# FASE 13. VALIDACIÓN FINAL

---

## 13.1 Objetivo de la Fase

Verificar funcionamiento completo en ambiente cloud.

---

## 13.2 Verificar Frontend

Abrir URL pública frontend.

Verificar:

```text
chat funcionando
workflows visibles
agentes visibles
```

---

## 13.3 Verificar Backend

Abrir:

```text
https://api.scrumdev-ai.com/health
```

Resultado esperado:

```json
{
  "status": "ok"
}
```

---

## 13.4 Verificar Pipeline

Dentro de GitHub:

```text
Actions
```

Verificar:

```text
tests exitosos
build exitoso
deploy exitoso
```

---

# FASE 14. RESULTADO FINAL DEL PROYECTO

---

## 14.1 Resultado Esperado

Al finalizar todos los talleres el estudiante tendrá:

```text
plataforma multiagente funcional
frontend conversacional
backend distribuido
workflows durables
agentes IA especializados
integración Jira
integración GitHub
memoria semántica
CI/CD automatizado
despliegue cloud
observabilidad
```

---

## 14.2 Capacidades Finales de ScrumDev AI

La plataforma será capaz de:

```text
refinar historias Scrum
proponer arquitecturas
coordinar agentes
generar software
validar calidad
automatizar despliegues
mantener trazabilidad
interactuar con humanos
```

---

## 14.3 Próximos Pasos Recomendados

Posibles evoluciones futuras:

```text
multi-tenant
Kubernetes
RAG avanzado
multi-model LLM
observabilidad distribuida
cost optimization
self-healing workflows
```
