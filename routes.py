from fastapi import APIRouter, HTTPException
from typing import List

from models import ArticuloCreate, ArticuloResponse
from use_cases import (
    CrearArticulo,
    ObtenerArticuloPorID,
    ListarArticulos,
    ActualizarArticulo,
    EliminarArticulo,
)

articulo_router = APIRouter()

# Rutas
@articulo_router.post("/articulo/", response_model=ArticuloResponse)
def crear_articulo(articulo: ArticuloCreate):
    caso_uso = CrearArticulo()
    return caso_uso.ejecutar(
        titulo=articulo.titulo,
        autor=articulo.autor,
        resumen=articulo.resumen,
        palabras_claves=articulo.palabras_claves,
        introduccion=articulo.introduccion,
        metodologia=articulo.metodologia,
        resultados=articulo.resultados,
        discusion=articulo.discusion,
        conclusion=articulo.conclusion,
        agradecimiento=articulo.agradecimiento,
        referencias=articulo.referencias,
        apendices=articulo.apendices,
        imagen=articulo.imagen
    )

@articulo_router.get("/articulos/", response_model=List[ArticuloResponse])
def listar_articulos():
    caso_uso = ListarArticulos()
    return caso_uso.ejecutar()

@articulo_router.get("/articulos/{id}/", response_model=ArticuloResponse)
def obtener_articulo(id: int):
    caso_uso = ObtenerArticuloPorID()
    try:
        articulo = caso_uso.ejecutar(id)
        if articulo.imagen is None:
            articulo.imagen = "Sin imagen"
        if not articulo.autor:
            articulo.autor = ["Desconocido"]

        return ArticuloResponse(
            id=articulo.id,
            titulo=articulo.titulo,
            autor=articulo.autor,
            resumen=articulo.resumen,
            palabras_claves=articulo.palabras_claves,
            introduccion=articulo.introduccion,
            metodologia=articulo.metodologia,
            resultados=articulo.resultados,
            discusion=articulo.discusion,
            conclusion=articulo.conclusion,
            agradecimiento=articulo.agradecimiento,
            referencias=articulo.referencias,
            apendices=articulo.apendices,
            imagen=articulo.imagen,
            fecha_publicacion=articulo.fecha_publicacion
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@articulo_router.put("/articulos/{id}/", response_model=ArticuloResponse)
def actualizar_articulo(id: int, articulo: ArticuloCreate):
    caso_uso = ActualizarArticulo()
    return caso_uso.ejecutar(
        id=id,
        titulo=articulo.titulo,
        autor=articulo.autor,
        resumen=articulo.resumen,
        palabras_claves=articulo.palabras_claves,
        introduccion=articulo.introduccion,
        metodologia=articulo.metodologia,
        resultados=articulo.resultados,
        discusion=articulo.discusion,
        conclusion=articulo.conclusion,
        agradecimiento=articulo.agradecimiento,
        referencias=articulo.referencias,
        apendices=articulo.apendices,
        imagen=articulo.imagen
    )

@articulo_router.delete("/articulos/{id}/")
def eliminar_articulo(id: int):
    caso_uso = EliminarArticulo()
    caso_uso.ejecutar(id)
    return {"message": f"Artículo con ID {id} eliminado con éxito"}
