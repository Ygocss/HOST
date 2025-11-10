# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.db.base import Base
from app.db.session import engine

# Routers v1
from app.api.v1 import vehicles, service_records, reminders, chatbot
from app.api.v1 import auth as auth_router  # /auth/register, /auth/login

app = FastAPI(
    title="CarSense API",
    version="0.1.0",
    servers=[{"url": "/api"}],  # Docs con base /api
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://carsense.online",
        "https://www.carsense.online",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirección a /docs respetando root_path
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url=f"{app.root_path}/docs")

# Health SIN /api aquí
@app.get("/health")
@app.get("/v1/health")
@app.get("/healt")  # compat
def health():
    return {"status": "ok"}

# Crear tablas al iniciar (dev)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Debug: listar rutas efectivas
@app.get("/_routes", include_in_schema=False)
def _routes():
    return sorted({
        getattr(r, "path", None)
        for r in app.router.routes
        if getattr(r, "path", None)
    })

# Registrar routers SOLO en "" y "/v1" (NUNCA "/api")
for prefix in ("", "/v1"):
    app.include_router(auth_router.router,     prefix=prefix, tags=["auth"])
    app.include_router(vehicles.router,        prefix=prefix, tags=["vehicles"])
    app.include_router(service_records.router, prefix=prefix, tags=["services"])
    app.include_router(reminders.router,       prefix=prefix, tags=["reminders"])
    app.include_router(chatbot.router,         prefix=prefix, tags=["chatbot"])
