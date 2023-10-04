from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, JSON

from database import Base  # Asegúrate de que esta importación es correcta

# Modelo ORM
class ArticuloORM(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(JSON)  # Lista de strings
    resumen = Column(String)
    palabras_claves = Column(JSON)  # Lista de strings
    introduccion = Column(String)
    metodologia = Column(String)
    resultados = Column(String)
    discusion = Column(String)
    conclusion = Column(String)
    agradecimiento = Column(JSON)  # Lista de strings
    referencias = Column(JSON)  # Lista de strings
    apendices = Column(JSON)  # Lista de strings
    imagen = Column(String)
    fecha_publicacion = Column(DateTime)

# Modelos Pydantic
class ArticuloBase(BaseModel):
    titulo: str
    autor: Optional[List[str]] = ["Catriel Pérez"]
    resumen: str
    palabras_claves: List[str]
    introduccion: str
    metodologia: Optional[str] = None
    resultados: Optional[str] = None
    discusion: Optional[str] = None
    conclusion: str
    agradecimiento: Optional[List[str]] = None
    referencias: Optional[List[str]] = None
    apendices: List[str] = ["datacraft.vercel.app"]
    imagen: Optional[str] = None

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloResponse(BaseModel):
    id: int
    titulo: str
    autor: List[str]
    resumen: str
    palabras_claves: List[str]
    introduccion: str
    metodologia: str
    resultados: str
    discusion: str
    conclusion: str
    agradecimiento: List[str]
    referencias: List[str]
    apendices: List[str]
    imagen: str
    fecha_publicacion: datetime

    class Config:
        orm_mode = True
