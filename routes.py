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
            articulo.titulo, articulo.contenido, articulo.imagen,
            articulo.autor
            )


@articulo_router.get("/articulos/", response_model=List[ArticuloResponse])
def listar_articulos():
    caso_uso = ListarArticulos()
    return caso_uso.ejecutar()


@articulo_router.get("/articulos/{id}/", response_model=ArticuloResponse)
def obtener_articulo(id: int):
    caso_uso = ObtenerArticuloPorID()  # Crear instancia del caso de uso
    try:
        articulo = caso_uso.ejecutar(id)
        if articulo.imagen is None:
            articulo.imagen = "Sin imagen"
        if articulo.autor is None:
            articulo.autor = "Desconocido"  # o cualquier valor predeterminado que desees

        # Convertir la entidad Articulo a un modelo Pydantic
        return ArticuloResponse(
                id=articulo.id,
                titulo=articulo.titulo,
                contenido=articulo.contenido,
                imagen=articulo.imagen,
                fecha_publicacion=articulo.fecha_publicacion,
                autor=articulo.autor
                )

    except ValueError as e:  # Capturar el error específico de "Artículo no encontrado"
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:  # Capturar otros errores
        raise HTTPException(status_code=500, detail=str(e))


@articulo_router.put("/articulos/{id}/", response_model=ArticuloResponse)
def actualizar_articulo(id: int, articulo: ArticuloCreate):
    caso_uso = ActualizarArticulo()
    return caso_uso.ejecutar(
            id, articulo.titulo, articulo.contenido, articulo.imagen,
            articulo.autor
            )


@articulo_router.delete("/articulos/{id}/")
def eliminar_articulo(id: int):
    caso_uso = EliminarArticulo()
    caso_uso.ejecutar(id)
    return {"message": f"Artículo con ID {id} eliminado con éxito"}
