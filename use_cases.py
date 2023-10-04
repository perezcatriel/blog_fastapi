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
        palabras_claves: str,
        introduccion: str,
        conclusion: str,
        autor: Optional[str] = "Catriel Pérez",
        metodologia: Optional[str] = None,
        resultados: Optional[str] = None,
        discusion: Optional[str] = None,
        agradecimiento: Optional[str] = None,
        referencias: Optional[str] = None,
        apendices: Optional[str] = "datacraft.vercel.app",
        imagen: Optional[str] = None
    ) -> ArticuloORM:
        with SessionLocal() as db:
            fecha_publicacion = datetime.now()
            articulo_orm = ArticuloORM(
                titulo=titulo,
                autor=autor,
                resumen=resumen,
                palabras_claves=palabras_claves,
                introduccion=introduccion,
                metodologia=metodologia,
                resultados=resultados,
                discusion=discusion,
                conclusion=conclusion,
                agradecimiento=agradecimiento,
                referencias=referencias,
                apendices=apendices,
                imagen=imagen,
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
        conclusion: str,
        palabras_claves: str,
        introduccion: str,
        autor: Optional[str] = "Catriel Pérez",
        metodologia: Optional[str] = None,
        resultados: Optional[str] = None,
        discusion: Optional[str] = None,
        agradecimiento: Optional[str] = None,
        referencias: Optional[str] = None,
        apendices: Optional[str] = "datacraft.vercel.app",
        imagen: Optional[str] = None
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
            articulo_orm.introduccion = introduccion
            articulo_orm.metodologia = metodologia
            articulo_orm.resultados = resultados
            articulo_orm.discusion = discusion
            articulo_orm.conclusion = conclusion
            articulo_orm.agradecimiento = agradecimiento
            articulo_orm.referencias = referencias
            articulo_orm.apendices = apendices
            articulo_orm.imagen = imagen
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
