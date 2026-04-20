from dotenv import load_dotenv
import os
import re
from pathlib import Path

load_dotenv()

from crewai import Agent

# =========================
# 1. AGENTE
# =========================
agente_plantuml = Agent(
    role="Arquitecto UML experto en PlantUML",
    goal=(
        "Generar diagramas de casos de uso correctos, mínimos, consistentes "
        "y válidos en sintaxis PlantUML a partir de requerimientos funcionales"
    ),
    backstory=(
        "Eres especialista en ingeniería de requisitos, UML, casos de uso y PlantUML. "
        "Identificas actores, límite del sistema, casos de uso principales y relaciones. "
        "No inventas elementos innecesarios. "
        "Usas <<include>> para comportamientos obligatorios reutilizables. "
        "Usas <<extend>> solo si existe un comportamiento alternativo u opcional claramente justificable. "
        "Tu salida debe ser limpia, renderizable y académicamente correcta."
    ),
    verbose=True
)

# =========================
# 2. PROMPT
# =========================
prompt = """
Actúa como experto en diagramas de casos de uso y sintaxis PlantUML.

Tu tarea es transformar la siguiente especificación en un diagrama de casos de uso correcto.

Especificación:
Como estudiante,
quiero registrar una reserva con mi nombre, fecha y hora,
para apartar una asesoría.

Reglas del sistema:
- El sistema debe permitir registrar una reserva.
- El sistema debe permitir consultar reservas registradas.
- No debe permitirse reservar un horario ya ocupado.
- Un estudiante no puede tener más de 2 reservas activas.
- El sistema debe informar éxito o error al registrar una reserva.

Requisitos obligatorios de salida:
- Devuelve exclusivamente código PlantUML.
- Usa @startuml al inicio y @enduml al final.
- El diagrama debe ser de casos de uso.
- Incluye actor o actores.
- Incluye el límite del sistema usando rectangle.
- Incluye casos de uso principales y, si aplica, validaciones como <<include>>.
- Usa <<extend>> solo si realmente está justificado.
- Usa nombres claros en español.
- No incluyas texto explicativo fuera del código.
- No uses markdown.
- No uses triple comilla.
- No uses bloques ```.

Criterios de calidad:
- No inventes actores que no estén justificados por la especificación.
- No conviertas mensajes de error en actores.
- No modeles campos del formulario como casos de uso.
- Mantén el diagrama simple, correcto y legible.
"""

# =========================
# 3. EJECUCIÓN
# =========================
resultado = agente_plantuml.kickoff(prompt)

# =========================
# 4. LIMPIEZA DE SALIDA
# =========================
def limpiar_plantuml(texto: str) -> str:
    """
    Limpia fences markdown y conserva únicamente el bloque entre @startuml y @enduml si existe.
    """
    texto = texto.strip()

    # Elimina fences tipo ```plantuml ... ```
    texto = re.sub(r"```[a-zA-Z]*", "", texto)
    texto = texto.replace("```", "").strip()

    # Extrae solo el bloque PlantUML si existe
    patron = re.search(r"@startuml[\s\S]*?@enduml", texto, re.IGNORECASE)
    if patron:
        return patron.group(0).strip()

    return texto

codigo_puml = limpiar_plantuml(str(resultado))

# =========================
# 5. VALIDACIÓN BÁSICA
# =========================
def validar_plantuml_casos(codigo: str):
    errores = []

    if "@startuml" not in codigo:
        errores.append("Falta @startuml.")
    if "@enduml" not in codigo:
        errores.append("Falta @enduml.")

    # Actor
    if not re.search(r"\bactor\b", codigo):
        errores.append("No se encontró ningún actor.")

    # Límite del sistema
    if "rectangle" not in codigo:
        errores.append("No se encontró el límite del sistema con rectangle.")

    # Casos de uso
    if not re.search(r"\busecase\b", codigo):
        errores.append("No se encontró ningún usecase.")

    # Debe haber alguna relación
    if not re.search(r"(-->|<--|--|\.>)", codigo):
        errores.append("No se encontraron relaciones entre elementos.")

    return errores

errores = validar_plantuml_casos(codigo_puml)

# =========================
# 6. GUARDAR ARCHIVO
# =========================
archivo_salida = Path("casos_reserva.puml")
archivo_salida.write_text(codigo_puml, encoding="utf-8")

# =========================
# 7. REPORTE
# =========================
print("\n===== CÓDIGO PLANTUML GENERADO =====\n")
print(codigo_puml)

print("\n===== VALIDACIÓN =====\n")
if errores:
    print("Se encontraron problemas:")
    for e in errores:
        print(f"- {e}")
else:
    print("Validación básica aprobada.")

print(f"\nArchivo guardado en: {archivo_salida.resolve()}")