from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String

from database import Base


# Modelo ORM
class ArticuloORM(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    contenido = Column(String)
    fecha_publicacion = Column(DateTime)
    autor = Column(String, index=True)


# Modelos Pydantic
class ArticuloBase(BaseModel):
    titulo: str
    contenido: str
    autor: Optional[str] = None


class ArticuloCreate(ArticuloBase):
    pass


class ArticuloResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    fecha_publicacion: datetime
    autor: Optional[str]

    class Config:
        orm_mode = True


