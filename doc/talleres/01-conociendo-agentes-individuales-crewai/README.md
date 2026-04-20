# Taller 1 - Conociendo agentes individuales con CrewAI

## Índice

1. [Propósito](#1-propósito)
2. [Requisitos previos para replicar el taller](#2-requisitos-previos-para-replicar-el-taller)
3. [Instrucciones para replicar localmente el taller](#3-instrucciones-para-replicar-localmente-el-taller)
4. [Retos que debe realizar](#4-retos-que-debe-realizar)
5. [Evidencias a mostrar](#5-evidencias-a-mostrar)

---

## 1. Propósito

Este taller tiene como propósito que el estudiante:

1. Comprenda cómo crear y ejecutar agentes individuales con CrewAI usando scripts separados.
2. Replique y analice el código base del taller.
3. Cree agentes especializados para distintos roles del proceso de desarrollo.
4. Mejore los agentes y prompts para que sean reutilizables, evitando dejar información fija dentro del código cuando esta deba venir desde un archivo de contexto.

En este taller no se trabaja con orquestación multiagente. Cada script define un agente, construye un prompt, ejecuta `kickoff()` y genera una salida específica.

El código base del taller se encuentra en la ruta:

```text
scr/talleres/taller_01/
```

La documentación general del proyecto de investigación se encuentra en:

[Repositorio documental del proyecto de investigación](https://uniempresarial-my.sharepoint.com/my?id=%2Fpersonal%2Fabeltran%5Funiempresarial%5Fedu%5Fco%2FDocuments%2FEstancia%2DInvestigacion%2DDelfin&viewid=19cfd5e2%2D40a2%2D4a7b%2Db345%2Df916eae88c57)

---

## 2. Requisitos previos para replicar el taller

Debe contar con lo siguiente:

- Python instalado.
- VS Code o editor equivalente.
- conexión a internet.
- una clave válida de OpenAI.
- entorno virtual disponible.
- CrewAI instalado en el entorno activo.
- `python-dotenv` instalado.
- acceso al repositorio que contiene el taller.

También debe tener disponible el código fuente en la ruta:

```text
scr/talleres/taller_01/
```

---

## 3. Instrucciones para replicar localmente el taller

### Paso 1. Obtener el código fuente
Descargue o clone el repositorio del proyecto en su equipo local.

### Paso 2. Abrir el proyecto
Abra la carpeta raíz del repositorio en VS Code.

### Paso 3. Ubicarse en la raíz del proyecto
Abra una terminal en la carpeta raíz del repositorio.

### Paso 4. Crear el entorno virtual
Ejecute:

```bash
python -m venv .venv
```

### Paso 5. Activar el entorno virtual
En Windows ejecute:

```bash
.venv\Scripts\activate
```

### Paso 6. Instalar dependencias
Ejecute:

```bash
pip install crewai python-dotenv
```

Si el repositorio ya incluye archivo de dependencias, ejecute:

```bash
pip install -r requirements.txt
```

### Paso 7. Configurar variables de entorno
Cree un archivo `.env` en la raíz del proyecto con este contenido:

```env
OPENAI_API_KEY=tu_api_key
OPENAI_MODEL_NAME=gpt-4o-mini
```

### Paso 8. Entrar a la carpeta del taller
Ubique la carpeta:

```text
scr/talleres/taller_01/
```

### Paso 9. Revisar el código base
Antes de ejecutar, revise los scripts base y confirme en cada uno:

- el rol del agente;
- el objetivo del agente;
- el prompt utilizado;
- la salida esperada;
- si la salida se imprime en consola o se guarda en archivo.

### Paso 10. Ejecutar el código base
Ejecute uno por uno los scripts del taller. Ejemplo:

```bash
python agente_analista_requerimientos.py
python agente_Desarollador_html.py
python agente_diseñador_css.py
python agente_experto_uml.py
```

### Paso 11. Guardar las salidas generadas
Cree una subcarpeta para resultados:

```text
scr/talleres/taller_01/salidas/
```

Guarde allí las respuestas generadas por cada agente.

---

## 4. Retos que debe realizar

### Reto 1. Crear un único archivo HTML de contexto
Construya el archivo:

```text
scr/retos/taller1/entradas/contexto_mvp.html
```

Ese archivo debe contener todo el contexto del proyecto necesario para que los agentes trabajen sin depender de información quemada dentro del prompt.

Debe incluir como mínimo estas secciones:

- contexto del negocio;
- problema a resolver;
- objetivo del MVP;
- actores o usuarios;
- alcance;
- requerimientos funcionales;
- requerimientos no funcionales;
- reglas de negocio;
- restricciones;
- supuestos;
- criterios de aceptación;
- entradas esperadas;
- salidas esperadas.

Ejemplo base:

```html
<html>
  <body>
    <section id="contexto-negocio">
      <h2>Contexto del negocio</h2>
      <p>...</p>
    </section>

    <section id="problema">
      <h2>Problema a resolver</h2>
      <p>...</p>
    </section>

    <section id="objetivo-mvp">
      <h2>Objetivo del MVP</h2>
      <p>...</p>
    </section>

    <section id="actores">
      <h2>Actores</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>

    <section id="alcance">
      <h2>Alcance</h2>
      <p>...</p>
    </section>

    <section id="requerimientos-funcionales">
      <h2>Requerimientos funcionales</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>

    <section id="requerimientos-no-funcionales">
      <h2>Requerimientos no funcionales</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>

    <section id="reglas-negocio">
      <h2>Reglas de negocio</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>

    <section id="restricciones">
      <h2>Restricciones</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>

    <section id="supuestos">
      <h2>Supuestos</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>

    <section id="criterios-aceptacion">
      <h2>Criterios de aceptación</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>

    <section id="entradas-esperadas">
      <h2>Entradas esperadas</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>

    <section id="salidas-esperadas">
      <h2>Salidas esperadas</h2>
      <ul>
        <li>...</li>
      </ul>
    </section>
  </body>
</html>
```

### Reto 2. Desacoplar los prompts
Refactorice los agentes originales para que lean el contexto desde `contexto_mvp.html` y no desde texto fijo dentro del script.

### Reto 3. Crear agentes especializados
Implemente los siguientes agentes:

- `agente_scrum.py`
- `agente_scrum_master.py`
- `agente_developer.py`
- `agente_product_owner.py`

Todos deben usar el mismo archivo HTML como entrada de contexto.

### Reto 4. Comparar resultados
Compare la versión original y la versión refactorizada de los agentes e identifique mejoras, limitaciones y posibilidades de reutilización.

### Instrucción final de publicación
Todo el código correspondiente a los retos realizados debe publicarse en la siguiente ruta del repositorio:

```text
scr/retos/taller1/
```

Se recomienda organizarlo así:

```text
scr/retos/taller1/
├── entradas/
│   └── contexto_mvp.html
├── salidas/
├── agente_scrum.py
├── agente_scrum_master.py
├── agente_developer.py
├── agente_product_owner.py
└── analisis_resultados.md
```

---

## 5. Evidencias a mostrar

Debe presentar las siguientes evidencias:

### 1. Ejecución del código base
Capturas o salidas de consola donde se vea la ejecución de los scripts originales.

### 2. Archivo de contexto del proyecto
Debe entregar el archivo:

```text
scr/retos/taller1/entradas/contexto_mvp.html
```

### 3. Código refactorizado
Debe entregar los agentes modificados para trabajar con lectura del archivo HTML de contexto.

### 4. Nuevos agentes creados
Debe entregar los agentes:

- `agente_scrum.py`
- `agente_scrum_master.py`
- `agente_developer.py`
- `agente_product_owner.py`

ubicados en:

```text
scr/retos/taller1/
```

### 5. Resultados generados
Debe mostrar las salidas producidas por cada agente, por ejemplo:

- `.txt`
- `.md`
- `.html`
- `.css`
- `.puml`

preferiblemente organizadas en:

```text
scr/retos/taller1/salidas/
```

### 6. Análisis técnico
Debe incluir un archivo breve de análisis donde explique:

- qué cambios realizó;
- qué información dejó de estar fija en los prompts;
- cómo reutilizó el archivo HTML de contexto;
- qué agente produjo mejores resultados;
- qué limitaciones encontró.

El análisis debe publicarse en:

```text
scr/retos/taller1/analisis_resultados.md
```
