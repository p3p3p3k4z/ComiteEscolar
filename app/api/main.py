# -*- coding: utf-8 -*-
# app/api/main.py (Actualización para incluir CORS y el router de reuniones)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Session, Base # Importa el motor, la sesión y Base desde app/db.py
from app.config import Configuracion
from contextlib import asynccontextmanager
from app.api import proyectos # Importa el módulo de rutas de proyectos
from app.api import usuarios # Importa el nuevo módulo de rutas de usuarios
from app.api import reuniones # Importa el nuevo módulo de rutas de reuniones

# Define un gestor de contexto de ciclo de vida para manejar la conexión/desconexión de la BD
@asynccontextmanager
async def ciclo_vida_app(app: FastAPI):
    # Crear tablas al inicio de la aplicación (solo para desarrollo)
    # En producción, usa migraciones (Alembic)
    print("Iniciando aplicación FastAPI. Creando tablas de BD...")
    Base.metadata.create_all(bind=engine) # Esto detecta TODOS los modelos importados en app.__init__
    print("Tablas de BD creadas o ya existentes.")
    yield
    # Lógica de limpieza al cerrar la aplicación si es necesaria
    print("Cerrando aplicación FastAPI. Desconectando de la BD...")
    engine.dispose() # Cierra las conexiones de la base de datos
    print("Desconexión de la BD completada.")

app = FastAPI(lifespan=ciclo_vida_app, title="API SGCPF - Gestión de Proyectos, Usuarios y Reuniones")

# Configurar CORS para permitir requests desde Flask (puerto 5000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000"],  # Permite requests desde Flask
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

# Incluye los routers de tus módulos de API
app.include_router(proyectos.router)
app.include_router(usuarios.router) # Incluye el router de usuarios
app.include_router(reuniones.router) # Incluye el router de reuniones

# Puedes añadir más routers aquí (ej. app.api.comites.router)

@app.get("/")
async def raiz():
    return {"mensaje": "API del Sistema de Gestión del Comité de Padres de Familia (SGCPF)"}

@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "API funcionando correctamente"}
