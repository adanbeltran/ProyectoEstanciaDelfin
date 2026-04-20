from dotenv import load_dotenv
import os

load_dotenv()
print("API KEY cargada:", os.getenv("OPENAI_API_KEY")[:5], "...")

from crewai import Agent

agente = Agent(
    role="Profesor asistente",
    goal="Explicar una app de reservas",
    backstory="Docente claro y práctico",
    verbose=True
)

resultado = agente.kickoff(
    "Explica qué necesita una app web sencilla de reservas"
)

print(resultado)