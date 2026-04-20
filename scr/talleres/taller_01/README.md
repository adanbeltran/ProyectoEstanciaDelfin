# Código de apoyo - Taller 01

## Descripción

Este código base presenta una introducción práctica al uso de **agentes individuales con CrewAI** aplicados a tareas básicas del desarrollo de software. Cada script define un agente con un rol específico, ejecuta un prompt puntual y produce una salida concreta. No se trabaja todavía con orquestación multiagente. :contentReference[oaicite:0]{index=0}

## Estructura del código base

El taller incluye los siguientes scripts:

- `agente_profesor.py`: agente introductorio para explicar de forma general qué requiere una app web de reservas. :contentReference[oaicite:1]{index=1}
- `agente_analista_requerimientos.py`: genera historia de usuario, descripción funcional, campos, reglas de negocio, criterios BDD, mensajes, restricciones y supuestos. :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}
- `agente_Desarollador_html.py`: genera el contenido base de un `index.html` para la interfaz del caso de ejemplo. :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}
- `agente_diseñador_css.py`: genera el contenido base de `styles.css` para la interfaz. :contentReference[oaicite:6]{index=6} :contentReference[oaicite:7]{index=7}
- `agente_experto_uml.py`: genera un diagrama de casos de uso en PlantUML, limpia la salida, realiza una validación básica y guarda un archivo `.puml`. :contentReference[oaicite:8]{index=8} :contentReference[oaicite:9]{index=9}

## Requisitos mínimos

- Python
- CrewAI
- `python-dotenv`
- variable `OPENAI_API_KEY` configurada
- variable `OPENAI_MODEL_NAME` configurada

Los scripts cargan variables de entorno con `load_dotenv()` antes de crear y ejecutar los agentes. :contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}

## Ejecución

Desde la carpeta del taller, ejecute:

```bash
python agente_profesor.py
python agente_analista_requerimientos.py
python agente_Desarollador_html.py
python agente_diseñador_css.py
python agente_experto_uml.py
