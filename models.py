from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, JSON, Boolean

from database import Base  # Asegúrate de que esta importación es correcta

# Modelo ORM
class ArticuloORM(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(JSON)  # Lista de strings
    resumen = Column(String)
    palabras_claves = Column(JSON)  # Lista de strings
    imagen = Column(String)
    avatar = Column(String)  # Nueva columna para el avatar
    seguir = Column(Boolean, default=False)  # Nueva columna para seguir
    formulario = Column(JSON)  # Objeto con pregunta y respuesta
    interacciones = Column(JSON)  # Objeto con me gustas, comentarios y compartidos
    fecha_publicacion = Column(DateTime)
    documento = Column(JSON)  # Objeto que agrupa las secciones del documento

# Modelos Pydantic
class ArticuloBase(BaseModel):
    titulo: str
    autor: Optional[List[str]] = ["Catriel Pérez"]
    resumen: str
    palabras_claves: List[str]
    imagen: Optional[str] = None
    avatar: Optional[str] = None
    seguir: Optional[bool] = False
    formulario: Optional[dict] = {"pregunta": "", "respuesta": 3}
    interacciones: Optional[dict] = {"me_gustas": 0, "comentarios": 0, "compartidos": 0}
    documento: dict = {
        "introduccion": "",
        "metodologia": "",
        "resultados": "",
        "discusion": "",
        "conclusion": "",
        "agradecimiento": [],
        "referencias": [],
        "apendices": ["datacraft.vercel.app"]
    }

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloResponse(BaseModel):
    id: int
    titulo: str
    autor: List[str]
    resumen: str
    palabras_claves: List[str]
    imagen: str
    avatar: str
    seguir: bool
    formulario: dict
    interacciones: dict
    fecha_publicacion: datetime
    documento: dict

    class Config:
        orm_mode = True
