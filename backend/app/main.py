from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.db.base import Base
from app.db.session import engine

from app.api.v1 import vehicles, service_records, reminders, chatbot
from app.api.v1 import auth as auth_router

app = FastAPI(title="CarSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://carsense.online",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root(request: Request):
    prefix = request.scope.get("root_path") or ""
    return RedirectResponse(url=f"{prefix}/docs")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router,     prefix="/v1", tags=["auth"])
app.include_router(vehicles.router,        prefix="/v1", tags=["vehicles"])
app.include_router(service_records.router, prefix="/v1", tags=["services"])
app.include_router(reminders.router,       prefix="/v1", tags=["reminders"])
app.include_router(chatbot.router,         prefix="/v1", tags=["chatbot"])
