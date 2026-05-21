# Taller 1- Configuración Inicial e Integraciones

---
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/c437f067-82f6-47cc-a1ef-8051f76b6382" />


# FASE 1. PREPARACIÓN DEL ENTORNO BASE

---

## 1.1 Objetivo de la Fase

En esta fase se instalarán las herramientas mínimas necesarias para ejecutar ScrumDev AI localmente. El objetivo es construir un entorno homogéneo y reproducible que permita desarrollar posteriormente el backend, frontend y workflows distribuidos de la plataforma.

---

## 1.2 Instalar Git

Git será utilizado para administrar versiones del proyecto, ramas, commits y sincronización con GitHub. ScrumDev AI utilizará GitHub como repositorio central y posteriormente como parte de los procesos CI/CD.

Ingresar:

```text
https://git-scm.com/downloads
```

Descargar la versión correspondiente al sistema operativo e instalar utilizando la configuración por defecto.

Verificar instalación:

```bash
git --version
```

Resultado esperado:

```text
git version 2.x.x
```

---

## 1.3 Instalar Docker Desktop

Docker permitirá ejecutar servicios de infraestructura localmente sin instalar manualmente PostgreSQL, Redis, RabbitMQ o Temporal.

Ingresar:

```text
https://www.docker.com/products/docker-desktop
```

Descargar Docker Desktop e instalarlo.

Reiniciar el equipo si es solicitado.

Verificar instalación:

```bash
docker --version
docker compose version
```

Resultado esperado:

```text
Docker version xx.x.x
Docker Compose version v2.x.x
```

---

## 1.4 Instalar Python

Python será el lenguaje principal utilizado para desarrollar el backend distribuido y los agentes IA de ScrumDev AI.

Ingresar:

```text
https://www.python.org/downloads/
```

Descargar Python 3.11 o superior.

Durante la instalación activar:

```text
Add Python to PATH
```

Verificar instalación:

```bash
python --version
```

Resultado esperado:

```text
Python 3.11.x
```

---

## 1.5 Instalar Poetry

Poetry administrará dependencias, ambientes virtuales y configuración del proyecto.

Instalar Poetry:

```bash
pip install poetry
```

Verificar instalación:

```bash
poetry --version
```

Resultado esperado:

```text
Poetry version x.x.x
```

---

# FASE 2. CONFIGURACIÓN DE JIRA

---

## 2.1 Objetivo de la Fase

Jira será utilizado como plataforma Scrum para administrar historias, backlog, sprints y estados del proyecto. ScrumDev AI interactuará automáticamente con Jira utilizando APIs REST.

---

## 2.2 Crear Cuenta Jira Cloud

Ingresar:

```text
https://www.atlassian.com/software/jira
```

Seleccionar:

```text
Get it free
```

Crear una cuenta Atlassian utilizando correo institucional o personal.

Crear un workspace nuevo.

Nombre recomendado:

```text
scrumdev-ai
```

---

## 2.3 Crear Proyecto Scrum

Dentro de Jira seleccionar:

```text
Projects
→ Create Project
```

Seleccionar:

```text
Software Development
→ Scrum
```

Configurar:

```text
Project Name: ScrumDev AI
Project Key: SDAI
```

Crear el proyecto.

---

## 2.4 Obtener URL Jira

La URL del proyecto tendrá una estructura similar:

```text
https://misitio.atlassian.net
```

Guardar esta URL porque será utilizada posteriormente en el archivo `.env`.

---

## 2.5 Crear API Token Jira

Ingresar:

```text
https://id.atlassian.com/manage-profile/security/api-tokens
```

Seleccionar:

```text
Create API token
```

Asignar nombre:

```text
ScrumDevAI
```

Generar el token y copiarlo temporalmente.

---

## 2.6 Verificar Información Jira

Al finalizar esta fase se debe tener:

```text
JIRA_BASE_URL
JIRA_EMAIL
JIRA_API_TOKEN
JIRA_PROJECT_KEY
```

---

# FASE 3. CONFIGURACIÓN DE GITHUB

---

## 3.1 Objetivo de la Fase

GitHub será utilizado para almacenar código fuente, administrar ramas, pull requests y automatizar pipelines de integración y despliegue.

---

## 3.2 Crear Cuenta GitHub

Ingresar:

```text
https://github.com
```

Seleccionar:

```text
Sign up
```

Crear una cuenta nueva.

---

## 3.3 Crear Repositorio Principal

Dentro de GitHub seleccionar:

```text
New Repository
```

Configurar:

```text
Repository Name: scrumdev-ai
Visibility: Private
Add README: Yes
```

Crear el repositorio.

---

## 3.4 Crear Personal Access Token

Ingresar:

```text
https://github.com/settings/tokens
```

Seleccionar:

```text
Fine-grained tokens
→ Generate new token
```

Habilitar permisos:

```text
Contents → Read/Write
Pull Requests → Read/Write
Actions → Read/Write
Metadata → Read
```

Generar el token y copiarlo temporalmente.

---

## 3.5 Verificar Información GitHub

Al finalizar esta fase se debe tener:

```text
GIT_PROVIDER
GIT_TOKEN
GIT_OWNER
GIT_REPO
```

---

# FASE 4. CONFIGURACIÓN DE OPENAI

---

## 4.1 Objetivo de la Fase

OpenAI proporcionará los modelos de lenguaje utilizados por los agentes IA de ScrumDev AI.

---

## 4.2 Crear Cuenta OpenAI

Ingresar:

```text
https://platform.openai.com
```

Seleccionar:

```text
Sign up
```

Crear cuenta.

---

## 4.3 Crear API Key OpenAI

Ingresar:

```text
https://platform.openai.com/api-keys
```

Seleccionar:

```text
Create new secret key
```

Generar la API Key y copiarla temporalmente.

---

## 4.4 Verificar Información OpenAI

Al finalizar esta fase se debe tener:

```text
AI_PROVIDER
AI_API_KEY
AI_MODEL
```

Modelo recomendado:

```text
gpt-5.5
```

---

# FASE 5. CONFIGURACIÓN DE BASE DE DATOS

---

## 5.1 Objetivo de la Fase

ScrumDev AI utilizará PostgreSQL para persistencia de conversaciones, workflows, auditoría y memoria semántica.

---

## 5.2 Crear Cuenta Supabase

Ingresar:

```text
https://supabase.com
```

Seleccionar:

```text
Start your project
```

Crear cuenta.

---

## 5.3 Crear Proyecto PostgreSQL

Dentro de Supabase seleccionar:

```text
New Project
```

Configurar:

```text
Project Name: scrumdev-ai-db
```

Definir contraseña segura y esperar despliegue automático.

---

## 5.4 Obtener Connection String

Dentro del proyecto seleccionar:

```text
Project Settings
→ Database
```

Buscar:

```text
Connection String
```

Copiar URI completa.

---

## 5.5 Verificar Información PostgreSQL

Al finalizar esta fase se debe tener:

```text
DATABASE_URL
```

---

# FASE 6. CONFIGURACIÓN DE DESPLIEGUE

---

## 6.1 Objetivo de la Fase

ScrumDev AI automatizará despliegues de aplicaciones utilizando plataformas cloud.

---

## 6.2 Crear Cuenta Render

Ingresar:

```text
https://render.com
```

Seleccionar:

```text
Get Started
```

Crear cuenta.

---

## 6.3 Crear API Key Render

Dentro de Render seleccionar:

```text
Account Settings
→ API Keys
```

Seleccionar:

```text
Create API Key
```

Generar y copiar token.

---

## 6.4 Verificar Información Deploy

Al finalizar esta fase se debe tener:

```text
DEPLOY_PROVIDER
DEPLOY_API_TOKEN
```

---

# FASE 7. CONSTRUCCIÓN DEL ARCHIVO .ENV

---

## 7.1 Objetivo de la Fase

Centralizar configuración externa del sistema siguiendo principios 12-factor app.

---

## 7.2 Crear Archivo `.env`

Crear archivo:

```text
.env
```

en la raíz del proyecto.

---

## 7.3 Agregar Variables de Entorno

Agregar:

```env
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

SCRUMDEV_DATABASE_URL=

SCRUMDEV_DEPLOY_PROVIDER=render
SCRUMDEV_DEPLOY_API_TOKEN=
```

---

## 7.4 Crear Archivo `.gitignore`

Crear archivo:

```text
.gitignore
```

Agregar:

```text
.env
.venv
__pycache__
```

---

## 7.5 Validar Variables de Entorno

Verificar:

```text
variables completas
sin espacios
sin comillas innecesarias
tokens válidos
```

---

# FASE 8. VALIDACIÓN FINAL

---

## 8.1 Objetivo de la Fase

Validar que todas las integraciones fueron configuradas correctamente.

---

## 8.2 Verificar Configuración General

Verificar:

```text
Git instalado
Docker instalado
Python instalado
Poetry instalado
Jira configurado
GitHub configurado
OpenAI configurado
Supabase configurado
Render configurado
.env creado
```

---

## 8.3 Resultado Esperado

Al finalizar este taller el estudiante tendrá:

```text
entorno preparado
credenciales configuradas
integraciones listas
variables entorno centralizadas
infraestructura externa preparada
```

El sistema estará listo para iniciar la construcción del backend distribuido en el siguiente taller.
