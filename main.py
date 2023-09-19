from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, root_validator
from sqlalchemy import Column, create_engine, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de FastAPI
app = FastAPI()

# Configuración de la Base de Datos
DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# Modelo ORM
class ArticuloORM(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    contenido = Column(String)
    fecha_publicacion = Column(DateTime)
    autor = Column(String, index=True)


# Entidad Articulo
class Articulo:
    def __init__(
        self, id: int, titulo: str, contenido: str, fecha_publicacion: datetime,
        autor: str = None
        ):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.fecha_publicacion = fecha_publicacion
        self.autor = autor


# Repositorio (Interfaz no implementada aquí por simplicidad)

# Casos de Uso
class CrearArticulo:
    def ejecutar(
        self, titulo: str, contenido: str, autor: str = None
        ) -> Articulo:
        db = SessionLocal()
        fecha_publicacion = datetime.now()
        articulo_orm = ArticuloORM(
                titulo=titulo, contenido=contenido,
                fecha_publicacion=fecha_publicacion, autor=autor
                )
        db.add(articulo_orm)
        db.commit()
        db.refresh(articulo_orm)
        db.close()
        return Articulo(
                articulo_orm.id, articulo_orm.titulo, articulo_orm.contenido,
                articulo_orm.fecha_publicacion, articulo_orm.autor
                )


class ObtenerArticuloPorID:
    def ejecutar(self, id: int) -> Articulo:
        db = SessionLocal()
        articulo_orm = db.query(ArticuloORM).filter(
                ArticuloORM.id == id
                ).first()
        db.close()
        if not articulo_orm:
            raise ValueError("Artículo no encontrado")
        return Articulo(
                articulo_orm.id, articulo_orm.titulo, articulo_orm.contenido,
                articulo_orm.fecha_publicacion, articulo_orm.autor
                )


class ActualizarArticulo:
    def ejecutar(
        self, id: int, titulo: str, contenido: str, autor: str = None
        ) -> Articulo:
        db = SessionLocal()
        articulo_orm = db.query(ArticuloORM).filter(
                ArticuloORM.id == id
                ).first()
        if not articulo_orm:
            db.close()
            raise HTTPException(
                    status_code=404, detail="Artículo no encontrado"
                    )
        articulo_orm.titulo = titulo
        articulo_orm.contenido = contenido
        articulo_orm.autor = autor
        db.commit()
        db.refresh(articulo_orm)
        db.close()
        return Articulo(
                articulo_orm.id, articulo_orm.titulo, articulo_orm.contenido,
                articulo_orm.fecha_publicacion, articulo_orm.autor
                )


class EliminarArticulo:
    def ejecutar(self, id: int) -> None:
        db = SessionLocal()
        articulo_orm = db.query(ArticuloORM).filter(
                ArticuloORM.id == id
                ).first()
        if not articulo_orm:
            db.close()
            raise HTTPException(
                    status_code=404, detail="Artículo no encontrado"
                    )
        db.delete(articulo_orm)
        db.commit()
        db.close()


class ListarArticulos:
    def ejecutar(self) -> List[Articulo]:
        db = SessionLocal()
        articulos = db.query(ArticuloORM).all()
        db.close()
        return [
            Articulo(a.id, a.titulo, a.contenido, a.fecha_publicacion, a.autor)
            for a in articulos]


# Modelos Pydantic
class ArticuloBase(BaseModel):
    titulo: str
    contenido: str
    autor: str = None


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


# Rutas
@app.post(path="/articulo/", response_model=ArticuloResponse)
def crear_articulo(articulo: ArticuloCreate):
    caso_uso = CrearArticulo()
    return caso_uso.ejecutar(
            articulo.titulo, articulo.contenido,
            articulo.autor
            )


@app.get(path="/articulos/", response_model=List[ArticuloResponse])
def listar_articulos():
    caso_uso = ListarArticulos()
    return caso_uso.ejecutar()


@app.get(path="/articulos/{id}/", response_model=ArticuloResponse)
def obtener_articulo(id: int):
    caso_uso = ObtenerArticuloPorID()  # Crear instancia del caso de uso
    try:
        articulo = caso_uso.ejecutar(id)

        if articulo.autor is None:
            articulo.autor = "Desconocido"  # o cualquier valor predeterminado que desees

        # Convertir la entidad Articulo a un modelo Pydantic
        return ArticuloResponse(
                id=articulo.id,
                titulo=articulo.titulo,
                contenido=articulo.contenido,
                fecha_publicacion=articulo.fecha_publicacion,
                autor=articulo.autor
                )

    except ValueError as e:  # Capturar el error específico de "Artículo no encontrado"
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:  # Capturar otros errores
        raise HTTPException(status_code=500, detail=str(e))

@app.put(path="/articulos/{id}/", response_model=ArticuloResponse)
def actualizar_articulo(id: int, articulo: ArticuloCreate):
    caso_uso = ActualizarArticulo()
    return caso_uso.ejecutar(
            id, articulo.titulo, articulo.contenido,
            articulo.autor
            )


@app.delete(path="/articulos/{id}/")
def eliminar_articulo(id: int):
    caso_uso = EliminarArticulo()
    caso_uso.ejecutar(id)
    return {"message": f"Artículo con ID {id} eliminado con éxito"}


# Inicialización de la Base de Datos
def init_db():
    Base.metadata.create_all(bind=engine)


init_db()
