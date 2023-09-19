from datetime import datetime
from typing import List

from fastapi import HTTPException

from database import SessionLocal
from models import ArticuloORM


# Casos de Uso
class CrearArticulo:
    def ejecutar(self, titulo: str, contenido: str, autor: str = None) -> ArticuloORM:
        with SessionLocal() as db:
            fecha_publicacion = datetime.now()
            articulo_orm = ArticuloORM(
                    titulo=titulo, contenido=contenido,
                    fecha_publicacion=fecha_publicacion, autor=autor
                    )
            db.add(articulo_orm)
            db.commit()
            db.refresh(articulo_orm)
        return articulo_orm


class ObtenerArticuloPorID:
    def ejecutar(self, id: int) -> ArticuloORM:
        with SessionLocal() as db:
            articulo_orm = db.query(ArticuloORM).filter(ArticuloORM.id == id).first()
            if not articulo_orm:
                raise ValueError("Artículo no encontrado")
        return articulo_orm


class ActualizarArticulo:
    def ejecutar(self, id: int, titulo: str, contenido: str, autor: str = None) -> ArticuloORM:
        with SessionLocal() as db:
            articulo_orm = db.query(ArticuloORM).filter(ArticuloORM.id == id).first()
            if not articulo_orm:
                raise HTTPException(status_code=404, detail="Artículo no encontrado")
            articulo_orm.titulo = titulo
            articulo_orm.contenido = contenido
            articulo_orm.autor = autor
            db.commit()
            db.refresh(articulo_orm)
        return articulo_orm


class EliminarArticulo:
    def ejecutar(self, id: int) -> None:
        with SessionLocal() as db:
            articulo_orm = db.query(ArticuloORM).filter(ArticuloORM.id == id).first()
            if not articulo_orm:
                raise HTTPException(status_code=404, detail="Artículo no encontrado")
            db.delete(articulo_orm)
            db.commit()


class ListarArticulos:
    def ejecutar(self) -> List[ArticuloORM]:
        with SessionLocal() as db:
            articulos = db.query(ArticuloORM).all()
        return articulos