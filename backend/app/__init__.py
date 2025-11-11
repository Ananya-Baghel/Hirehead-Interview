
"""
Interview Bot Backend Package

This package contains:
- ML model loaders and trainers (models_core.py)
- Adaptive questioning engine (logic_adaptive.py)
- Multi-agent interview personas (logic_group.py)
- Culture-fit scorer (logic_culture.py)
- Audio analysis utilities (logic_audio.py)
- Image analysis utilities (logic_vision.py)
- Salary negotiation simulator (negotiation.py)
- API schemas (schemas.py)
- Main FastAPI app (main.py)
"""

__all__ = [
    "models_core",
    "logic_adaptive",
    "logic_group",
    "logic_culture",
    "logic_audio",
    "logic_vision",
    "negotiation",
    "schemas",
    "main"
]
