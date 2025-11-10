# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, PlainTextResponse

from app.db.base import Base
from app.db.session import engine

# Routers (¡sin prefijos /api aquí!)
from app.api.v1 import vehicles
from app.api.v1 import service_records
from app.api.v1 import reminders
from app.api.v1 import chatbot
from app.api.v1 import auth as auth_router  # /auth/register, /auth/login

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

# Al entrar a "/", redirige a /docs respetando root_path (nginx -> /api)
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url=f"{app.root_path}/docs")

# Health (rutas públicas)
@app.get("/health", include_in_schema=False)
@app.get("/v1/health", include_in_schema=False)
@app.get("/healt", include_in_schema=False)  # compat
def health():
    return {"status": "ok"}

# (DEV) Crear tablas al iniciar
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Registrar routers SOLO en "" y "/v1"
for prefix in ("", "/v1"):
    app.include_router(auth_router.router,     prefix=prefix, tags=["auth"])
    app.include_router(vehicles.router,        prefix=prefix, tags=["vehicles"])
    app.include_router(service_records.router, prefix=prefix, tags=["services"])
    app.include_router(reminders.router,       prefix=prefix, tags=["reminders"])
    app.include_router(chatbot.router,         prefix=prefix, tags=["chatbot"])

# Endpoint de diagnóstico para listar rutas cargadas
@app.get("/_routes", include_in_schema=False, response_class=PlainTextResponse)
def _routes():
    paths = sorted({getattr(r, "path", "") for r in app.router.routes if getattr(r, "path", None)})
    return "\n".join(paths)
