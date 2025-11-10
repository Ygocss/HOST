# backend/app/api/v1/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
import re
from typing import List, Dict, Optional

router = APIRouter(prefix="/chat", tags=["chat"])

def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())

def has_any(text: str, *needles: str) -> bool:
    t = norm(text)
    return any(n in t for n in needles)

FAQ: Dict[str, Dict] = {
    "cambio_aceite": {
        "q": ["cuando cambio aceite", "cambio de aceite", "cada cuantos km aceite", "aceite cada"],
        "a": ("Como regla general: **cada 8–12 mil km o 6–12 meses** (lo que ocurra primero). "
              "Respeta la viscosidad del manual y **cambia el filtro siempre**."),
        "suggest": ["Checklist de cambio de aceite", "Recordar en 6 meses"]
    },
    # ... resto igual ...
}

OBD_DICT = {
    "p0300": "Misfire aleatorio/múltiple. Revisa bujías, bobinas, fugas de vacío.",
    # ...
}

class ChatIn(BaseModel):
    message: str
    vehicle_km: Optional[int] = None
    vehicle_year: Optional[int] = None

class ChatOut(BaseModel):
    reply: str
    suggestions: List[str] = []
    links: List[Dict[str, str]] = []

def intent_reply(data: ChatIn) -> ChatOut:
    # ... igual a tu lógica actual ...
    return ChatOut(reply="¡Hola! Probando chat.", suggestions=["¿Cuándo cambio el aceite?"])

@router.post("", response_model=ChatOut)
def chat(data: ChatIn):
    return intent_reply(data)
