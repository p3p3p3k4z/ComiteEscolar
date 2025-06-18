# -*- coding: utf-8 -*-
# app/api/dependecias.py

from sqlalchemy.orm import Session as SesionBD # Renombra para evitar conflicto
from app.db import Session # Importa tu factoría de sesiones desde app/db.py
from app.repositorios.proyecto_repo import RepositorioProyecto
from app.servicios.proyecto_servicio import ServicioProyecto
from app.repositorios.usuario_repo import RepositorioUsuario # Importa el RepositorioUsuario
from app.servicios.usuario_servicio import ServicioUsuario # Importa el ServicioUsuario
from fastapi import Depends


def obtener_bd():
    """
    Provee una sesión de base de datos para las rutas de la API.
    Asegura que la sesión se cierre después de la solicitud.
    """
    db = Session() # Usar la Session importada directamente desde app.db
    try:
        yield db
    finally:
        db.close()

def obtener_repositorio_proyecto(db: SesionBD = Depends(obtener_bd)) -> RepositorioProyecto:
    """
    Provee una instancia de RepositorioProyecto.
    """
    return RepositorioProyecto(db)

def obtener_repositorio_usuario(db: SesionBD = Depends(obtener_bd)) -> RepositorioUsuario:
    """
    Provee una instancia de RepositorioUsuario.
    """
    return RepositorioUsuario(db)

def obtener_servicio_proyecto(
    repositorio_proyecto: RepositorioProyecto = Depends(obtener_repositorio_proyecto),
    repositorio_usuario: RepositorioUsuario = Depends(obtener_repositorio_usuario) # Inyecta también el repositorio de usuario
) -> ServicioProyecto:
    """
    Provee una instancia de ServicioProyecto.
    """
    return ServicioProyecto(repositorio_proyecto, repositorio_usuario) # Pasa el repositorio de usuario

def obtener_servicio_usuario(
    repositorio_usuario: RepositorioUsuario = Depends(obtener_repositorio_usuario)
) -> ServicioUsuario:
    """
    Provee una instancia de ServicioUsuario.
    """
    return ServicioUsuario(repositorio_usuario)
