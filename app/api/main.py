# app/api/main.py (Actualización para incluir el router de proyectos)

from fastapi import FastAPI
from app.__init__ import engine, Session, Base # Importa el motor y la sesión
from app.config import Configuracion
from contextlib import asynccontextmanager
from app.api import proyectos # Importa el módulo de rutas de proyectos

# Define un gestor de contexto de ciclo de vida para manejar la conexión/desconexión de la BD
@asynccontextmanager
async def ciclo_vida_app(app: FastAPI):
    # Crear tablas al inicio de la aplicación (solo para desarrollo)
    # En producción, usa migraciones (Alembic)
    print("Iniciando aplicación FastAPI. Creando tablas de BD...")
    Base.metadata.create_all(bind=engine)
    print("Tablas de BD creadas o ya existentes.")
    yield
    # Lógica de limpieza al cerrar la aplicación si es necesaria
    print("Cerrando aplicación FastAPI. Desconectando de la BD...")
    engine.dispose() # Cierra las conexiones de la base de datos
    print("Desconexión de la BD completada.")

app = FastAPI(lifespan=ciclo_vida_app, title="API SGCPF - Gestión de Proyectos")

# Incluye los routers de tus módulos de API
app.include_router(proyectos.router)

# Puedes añadir más routers aquí (ej. app.api.usuarios.router, app.api.comites.router)

@app.get("/")
async def raiz():
    return {"mensaje": "API del Sistema de Gestión del Comité de Padres de Familia (SGCPF)"}
