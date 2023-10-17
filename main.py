from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes import articulo_router

app = FastAPI()

origins = [
    "http://localhost:8080",  # Asume que tu aplicación Vue se ejecuta en localhost:8080
    "https://datacraft.vercel.app",  # Reemplaza con el dominio de tu aplicación Vue si está en producción
]

# Configuración de CORS
app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )

# Inclusión de rutas y inicialización de la base de datos
app.include_router(articulo_router)
init_db()
