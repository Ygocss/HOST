# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.db.base import Base
from app.db.session import engine

# Routers v1
from app.api.v1 import vehicles, service_records, reminders, chatbot
from app.api.v1 import auth as auth_router

app = FastAPI(title="CarSense API")

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

# Health (deja todas las que ya tienes)
@app.get("/health")
@app.get("/api/health")
@app.get("/api/v1/health")
@app.get("/healt")
def health():
    return {"status": "ok"}

# <<< NUEVO: cuando lleguen a /api/ (root de la app), mándalos a /docs
@app.get("/", include_in_schema=False)
def root_to_docs():
    return RedirectResponse(url="/docs", status_code=307)
# >>>

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

for prefix in ("", "/api", "/api/v1"):
    app.include_router(auth_router.router,     prefix=prefix, tags=["auth"])
    app.include_router(vehicles.router,        prefix=prefix, tags=["vehicles"])
    app.include_router(service_records.router, prefix=prefix, tags=["services"])
    app.include_router(reminders.router,       prefix=prefix, tags=["reminders"])
    app.include_router(chatbot.router,         prefix=prefix, tags=["chatbot"])
