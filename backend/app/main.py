# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.db.base import Base
from app.db.session import engine

# Routers v1 (no uses prefijos con /api aquí)
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

# Al entrar a la raíz de la app, redirige a la documentación.
# Con root_path=/api en Uvicorn, externamente esto vive en /api/
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url=f"{app.root_path}/docs")

# Healthchecks sin prefijo (el root_path añade /api externamente)
@app.get("/health")
@app.get("/v1/health")
@app.get("/healt")  # compat: typo histórico
def health():
    return {"status": "ok"}

# Crear tablas al iniciar (útil en dev / single-node)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Registrar routers SOLO en "" y en "/v1".
# IMPORTANTE: NO uses "/api" ni "/api/v1" aquí; el root_path=/api ya lo añade externamente.
for prefix in ("", "/v1"):
    app.include_router(auth_router.router,     prefix=prefix, tags=["auth"])
    app.include_router(vehicles.router,        prefix=prefix, tags=["vehicles"])
    app.include_router(service_records.router, prefix=prefix, tags=["services"])
    app.include_router(reminders.router,       prefix=prefix, tags=["reminders"])
    app.include_router(chatbot.router,         prefix=prefix, tags=["chatbot"])
