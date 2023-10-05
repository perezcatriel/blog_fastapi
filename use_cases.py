from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from database import SessionLocal
from models import ArticuloORM


# Casos de Uso
class CrearArticulo:
    def ejecutar(
        self,
        titulo: str,
        resumen: str,
        palabras_claves: List[str],
        imagen: str,
        documento: dict,
        autor: Optional[List[str]] = ["Catriel Pérez"],
        avatar: Optional[str] = None,
        seguir: Optional[bool] = False,
        formulario: Optional[dict] = None,
        interacciones: Optional[dict] = None,

    ) -> ArticuloORM:
        with SessionLocal() as db:
            fecha_publicacion = datetime.now()
            articulo_orm = ArticuloORM(
                titulo=titulo,
                autor=autor,
                resumen=resumen,
                palabras_claves=palabras_claves,
                imagen=imagen,
                avatar=avatar,
                seguir=seguir,
                formulario=formulario,
                interacciones=interacciones,
                documento=documento,
                fecha_publicacion=fecha_publicacion
            )
            db.add(articulo_orm)
            db.commit()
            db.refresh(articulo_orm)

        return articulo_orm



class ObtenerArticuloPorID:
    def ejecutar(self, id: int) -> ArticuloORM:
        with SessionLocal() as db:
            articulo_orm = db.query(ArticuloORM).filter(
                ArticuloORM.id == id
            ).first()
            if not articulo_orm:
                raise ValueError("Artículo no encontrado")
        return articulo_orm


class ActualizarArticulo:
    def ejecutar(
        self,
        id: int,
        titulo: str,
        resumen: str,
        palabras_claves: List[str],
        imagen: str,
        documento: dict,
        autor: Optional[List[str]] = ["Catriel Pérez"],
        avatar: Optional[str] = None,
        seguir: Optional[bool] = False,
        formulario: Optional[dict] = None,
        interacciones: Optional[dict] = None,
    ) -> ArticuloORM:
        with SessionLocal() as db:
            articulo_orm = db.query(ArticuloORM).filter(
                ArticuloORM.id == id
            ).first()
            if not articulo_orm:
                raise HTTPException(
                    status_code=404, detail="Artículo no encontrado"
                )
            articulo_orm.titulo = titulo
            articulo_orm.autor = autor
            articulo_orm.resumen = resumen
            articulo_orm.palabras_claves = palabras_claves
            articulo_orm.imagen = imagen
            articulo_orm.avatar = avatar
            articulo_orm.seguir = seguir
            articulo_orm.formulario = formulario
            articulo_orm.interacciones = interacciones
            articulo_orm.documento = documento
            db.commit()
            db.refresh(articulo_orm)
        return articulo_orm

class EliminarArticulo:
    def ejecutar(self, id: int) -> None:
        with SessionLocal() as db:
            articulo_orm = db.query(ArticuloORM).filter(
                ArticuloORM.id == id
            ).first()
            if not articulo_orm:
                raise HTTPException(
                    status_code=404, detail="Artículo no encontrado"
                )
            db.delete(articulo_orm)
            db.commit()


class ListarArticulos:
    def ejecutar(self) -> List[ArticuloORM]:
        with SessionLocal() as db:
            articulos = db.query(ArticuloORM).all()
        return articulos
