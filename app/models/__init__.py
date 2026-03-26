from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    clientes = relationship("Cliente", back_populates="usuario")

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="clientes")
    processos = relationship("Processo", back_populates="cliente")

class Processo(Base):
    __tablename__ = "processos"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    vara = Column(String, nullable=True)
    status = Column(String, default="ativo")
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="processos")
    prazos = relationship("Prazo", back_populates="processo")

class Prazo(Base):
    __tablename__ = "prazos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    data_limite = Column(Date, nullable=False)
    concluido = Column(Integer, default=0)
    processo_id = Column(Integer, ForeignKey("processos.id"))
    processo = relationship("Processo", back_populates="prazos")