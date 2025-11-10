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
from app.api.v1 import auth as auth_router  # auth: /auth/register, /auth/login

app = FastAPI(title="CarSense API")  # docs_url default = "/docs"

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health (compat)
@app.get("/health")
@app.get("/api/health")
@app.get("/api/v1/health")
@app.get("/healt")
def health():
    return {"status": "ok"}

# Redirigir raíz del backend a la documentación
@app.get("/")
def root():
    return RedirectResponse(url=f"{app.root_path}{app.docs_url}")

# Crear tablas al iniciar (dev)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Registrar routers con prefijos "", "/api", "/api/v1"
for prefix in ("", "/api", "/api/v1"):
    app.include_router(auth_router.router,     prefix=prefix, tags=["auth"])
    app.include_router(vehicles.router,        prefix=prefix, tags=["vehicles"])
    app.include_router(service_records.router, prefix=prefix, tags=["services"])
    app.include_router(reminders.router,       prefix=prefix, tags=["reminders"])
    app.include_router(chatbot.router,         prefix=prefix, tags=["chatbot"])
