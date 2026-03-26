from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Jurídico")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend/index.html", encoding="utf-8") as f:
        return f.read()

@app.get("/login", response_class=HTMLResponse)
def login():
    with open("frontend/login.html", encoding="utf-8") as f:
        return f.read()

@app.get("/cadastro", response_class=HTMLResponse)
def cadastro():
    with open("frontend/cadastro.html", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("frontend/dashboard.html", encoding="utf-8") as f:
        return f.read()

@app.get("/processos-page", response_class=HTMLResponse)
def processos_page():
    with open("frontend/processos.html", encoding="utf-8") as f:
        return f.read()

@app.get("/prazos-page", response_class=HTMLResponse)
def prazos_page():
    with open("frontend/prazos.html", encoding="utf-8") as f:
        return f.read()