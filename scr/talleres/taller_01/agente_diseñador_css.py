from crewai import Agent

from dotenv import load_dotenv
import os

load_dotenv()

agente = Agent(
    role="Diseñador CSS",
    goal="Generar estilos CSS simples, limpios y fáciles de entender",
    backstory="Especialista en estilos web básicos para estudiantes que están empezando.",
    verbose=True
)

prompt = """
Genera solo el contenido de styles.css para una app sencilla de reservas.

Requisitos:
- diseño centrado
- formulario legible
- botón visible
- estilos para mensaje exitoso y mensaje de error
- lista de reservas ordenada

No expliques nada. Entrega solo CSS.
"""

resultado = agente.kickoff(prompt)

print("\n===== CSS =====\n")
print(resultado)