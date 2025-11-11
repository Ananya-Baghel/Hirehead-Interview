from dataclasses import dataclass
from typing import Dict

@dataclass
class Persona:
    name: str
    style: str         # e.g., "supportive", "probing", "aggressive", "metrics"

PERSONAS: Dict[str, Persona] = {
    "hr": Persona("HR", "supportive"),
    "tech": Persona("Tech", "probing"),
    "manager": Persona("Manager", "metrics"),
    "behavioral": Persona("Behavioral", "probing")
}

def persona_prompt_prefix(p: Persona) -> str:
    if p.style == "supportive": return "Be friendly, ask clarifying follow-ups."
    if p.style == "probing": return "Ask why and how; dig into decisions."
    if p.style == "metrics": return "Request measurable impact and KPIs."
    return "Be neutral."
