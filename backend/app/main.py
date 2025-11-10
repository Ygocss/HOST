# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.db.base import Base
from app.db.session import engine

# Routers v1
from app.api.v1 import vehicles
from app.api.v1 import service_records
from app.api.v1 import reminders
from app.api.v1 import chatbot
from app.api.v1 import auth as auth_router  # /v1/auth/register, /v1/auth/login

app = FastAPI(title="CarSense API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1",
        "https://carsense.online",
        "https://www.carsense.online",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Raíz de la app -> docs (externamente será /api/docs por root_path)
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url=f"{app.root_path}/docs")

# Health (interno /health y /v1/health; externo /api/health y /api/v1/health)
@app.get("/health")
@app.get("/v1/health")
def health():
    return {"status": "ok"}

# Crear tablas al iniciar (útil en dev)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Registrar routers SOLO en "/v1"
app.include_router(auth_router.router,     prefix="/v1", tags=["auth"])
app.include_router(vehicles.router,        prefix="/v1", tags=["vehicles"])
app.include_router(service_records.router, prefix="/v1", tags=["services"])
app.include_router(reminders.router,       prefix="/v1", tags=["reminders"])
app.include_router(chatbot.router,         prefix="/v1", tags=["chatbot"])
