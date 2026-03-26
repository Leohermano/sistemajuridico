from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario, Cliente, Processo, Prazo
from app.auth import hash_senha, verificar_senha, criar_token
from pydantic import BaseModel
from typing import Optional
from datetime import date

router = APIRouter()

# --- Schemas ---
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    email: Optional[str] = None
    telefone: Optional[str] = None

class ProcessoCreate(BaseModel):
    numero: str
    descricao: Optional[str] = None
    vara: Optional[str] = None
    cliente_id: int

class PrazoCreate(BaseModel):
    descricao: str
    data_limite: date
    processo_id: int

# --- Autenticação ---
@router.post("/cadastro")
def cadastrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    novo = Usuario(nome=usuario.nome, email=usuario.email, senha=hash_senha(usuario.senha))
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"mensagem": "Usuário cadastrado com sucesso!"}

@router.post("/login")
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    token = criar_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}

# --- Clientes ---
@router.post("/clientes")
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    existe = db.query(Cliente).filter(Cliente.cpf == cliente.cpf).first()
    if existe:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    novo = Cliente(**cliente.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@router.get("/clientes/{id}")
def buscar_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.delete("/clientes/{id}")
def deletar_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso!"}

# --- Processos ---
@router.post("/processos")
def criar_processo(processo: ProcessoCreate, db: Session = Depends(get_db)):
    novo = Processo(**processo.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/processos")
def listar_processos(db: Session = Depends(get_db)):
    return db.query(Processo).all()

@router.get("/processos/{id}")
def buscar_processo(id: int, db: Session = Depends(get_db)):
    processo = db.query(Processo).filter(Processo.id == id).first()
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    return processo

# --- Prazos ---
@router.post("/prazos")
def criar_prazo(prazo: PrazoCreate, db: Session = Depends(get_db)):
    novo = Prazo(**prazo.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/prazos")
def listar_prazos(db: Session = Depends(get_db)):
    return db.query(Prazo).all()

@router.get("/prazos/proximos")
def prazos_proximos(db: Session = Depends(get_db)):
    hoje = date.today()
    return db.query(Prazo).filter(Prazo.data_limite >= hoje, Prazo.concluido == 0).order_by(Prazo.data_limite).all()