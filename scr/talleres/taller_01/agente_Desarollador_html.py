from crewai import Agent

from dotenv import load_dotenv
import os

load_dotenv()


agente = Agent(
    role="Desarrollador HTML",
    goal="Generar una interfaz HTML simple y clara para una app de reservas",
    backstory="Eres un desarrollador frontend que crea interfaces básicas para principiantes.",
    verbose=True
)

prompt = """
Genera solo el contenido de un archivo index.html para una app de reservas.

Debe incluir:
- un título
- un formulario con campos: estudiante, fecha, hora
- un botón Reservar
- un área para mensajes
- una lista para mostrar reservas

Usa ids claros:
estudiante, fecha, hora, btn-reservar, mensaje, lista-reservas
No expliques nada. Entrega solo código HTML, no incluir css 
"""

resultado = agente.kickoff(prompt)

print("\n===== HTML =====\n")
print(resultado)