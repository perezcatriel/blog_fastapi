from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes import articulo_router

app = FastAPI()

# Configuración de CORS
app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://datacraft.vercel.app"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )

# Inclusión de rutas y inicialización de la base de datos
app.include_router(articulo_router)
init_db()
