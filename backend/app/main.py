# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Routers v1
from app.api.v1 import vehicles
from app.api.v1 import service_records
from app.api.v1 import reminders
from app.api.v1 import chatbot
from app.api.v1 import auth as auth_router  # /v1/auth/...

app = FastAPI(title="CarSense API", version="1.0.0")

# --- CORS (producción + local dev) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://carsense.online",
        "https://www.carsense.online",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health (quedémonos con una ruta clara) ---
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

# --- Redirigir raíz a /docs respetando root_path (/api) ---
@app.get("/", include_in_schema=False)
def root(request: Request):
    rp = request.scope.get("root_path", "")  # e.g. "/api" detrás del proxy
    return RedirectResponse(url=f"{rp}/docs")

# --- Registrar API v1 SOLO una vez ---
# Importante: Uvicorn ya corre con --root-path /api
# Por eso aquí usamos solo "/v1" para evitar duplicados.
API_PREFIX = "/v1"
app.include_router(auth_router.router,     prefix=API_PREFIX, tags=["auth"])
app.include_router(vehicles.router,        prefix=API_PREFIX, tags=["vehicles"])
app.include_router(service_records.router, prefix=API_PREFIX, tags=["services"])
app.include_router(reminders.router,       prefix=API_PREFIX, tags=["reminders"])
app.include_router(chatbot.router,         prefix=API_PREFIX, tags=["chatbot"])
