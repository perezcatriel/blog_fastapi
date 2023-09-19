from fastapi import FastAPI

from database import init_db
from routes import articulo_router

# Configuración de FastAPI
app = FastAPI()

app.include_router(articulo_router)

init_db()
