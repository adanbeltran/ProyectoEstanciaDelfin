from crewai import Agent

from dotenv import load_dotenv
import os

load_dotenv()
print("API KEY cargada:", os.getenv("OPENAI_API_KEY")[:5], "...")

CREWAI_DISABLE_TELEMETRY=True

agente = Agent(
    role="Analista de requerimientos",
    goal="Convertir historias de usuario en requerimientos funcionales claros",
    backstory="Especialista en análisis de software y redacción de requerimientos.",
    verbose=True

)

prompt = """
Actúa como analista de requerimientos experto en historias de usuario y BDD.

Analiza la siguiente necesidad y conviértela en una especificación clara y completa.

Necesidad:
Como estudiante,
quiero registrar una reserva con mi nombre, fecha y hora,
para apartar una asesoría.

Tu respuesta debe estar en español y seguir EXACTAMENTE esta estructura:

1. HISTORIA DE USUARIO COMPLETA
- Redacta la historia de usuario completa y bien formulada.
- Identifica:
  - Rol
  - Necesidad
  - Beneficio

2. DESCRIPCIÓN FUNCIONAL
- Explica brevemente qué debe hacer el sistema.

3. CAMPOS DEL FORMULARIO
- Lista todos los campos necesarios.
- Para cada campo indica:
  - nombre
  - tipo de dato
  - si es obligatorio
  - ejemplo de valor

4. REGLAS DE NEGOCIO
- Enumera todas las reglas mínimas y también las implícitas necesarias.
- Incluye como mínimo validaciones sobre:
  - campos obligatorios
  - fecha
  - hora
  - duplicidad de reserva
  - cantidad máxima de reservas por estudiante
  - duración de la reserva

5. CRITERIOS DE ACEPTACIÓN EN BDD
Genera TODOS los criterios de aceptación necesarios usando formato BDD:
Dado
Cuando
Entonces

Debes incluir escenarios positivos, alternos y de error.

Como mínimo incluye escenarios para:
- crear una reserva válida
- campo nombre vacío
- fecha vacía
- hora vacía
- horario duplicado
- estudiante con máximo de reservas alcanzado
- visualización de la reserva en la lista
- mensaje de confirmación
- mensaje de error

6. MENSAJES ESPERADOS DEL SISTEMA
- Lista los mensajes de éxito, advertencia y error.

7. RESTRICCIONES DEL SISTEMA
- Enumera restricciones funcionales y de uso.

8. SUPUESTOS
- Indica supuestos razonables si hace falta completar la especificación.

Reglas importantes:
- No resumas.
- No omitas criterios.
- No inventes tecnología.
- Redacta criterios de aceptación completos y verificables.
- Cada criterio BDD debe escribirse de forma independiente y numerada.
- Usa lenguaje claro .
"""

resultado = agente.kickoff(prompt)

print("\n===== ANÁLISIS =====\n")
print(resultado)