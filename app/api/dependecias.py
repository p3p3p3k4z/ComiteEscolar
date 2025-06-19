# -*- coding: utf-8 -*-
# app/api/dependecias.py

from sqlalchemy.orm import Session as SesionBD # Renombra para evitar conflicto
from app.db import Session # Importa tu factoría de sesiones desde app/db.py
from app.repositorios.proyecto_repo import RepositorioProyecto
from app.servicios.proyecto_servicio import ServicioProyecto
from app.repositorios.usuario_repo import RepositorioUsuario # Importa el RepositorioUsuario
from app.servicios.usuario_servicio import ServicioUsuario # Importa el ServicioUsuario
from app.repositorios.reunion_repo import (
    RepositorioReunion, RepositorioMiembroReunion, 
    RepositorioNotificacion, RepositorioActa
)
from app.servicios.reunion_servicio import ServicioReunion
from fastapi import Depends
from app.repositorios.finanzas_repo import RepositorioFinanzas
from app.servicios.finanzas_servicios import ServicioFinanciero



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

def obtener_repositorio_reunion(db: SesionBD = Depends(obtener_bd)) -> RepositorioReunion:
    """
    Provee una instancia de RepositorioReunion.
    """
    return RepositorioReunion(db)

def obtener_repositorio_miembro_reunion(db: SesionBD = Depends(obtener_bd)) -> RepositorioMiembroReunion:
    """
    Provee una instancia de RepositorioMiembroReunion.
    """
    return RepositorioMiembroReunion(db)

def obtener_repositorio_notificacion(db: SesionBD = Depends(obtener_bd)) -> RepositorioNotificacion:
    """
    Provee una instancia de RepositorioNotificacion.
    """
    return RepositorioNotificacion(db)

def obtener_repositorio_acta(db: SesionBD = Depends(obtener_bd)) -> RepositorioActa:
    """
    Provee una instancia de RepositorioActa.
    """
    return RepositorioActa(db)

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

def obtener_servicio_reunion(
    repo_reunion: RepositorioReunion = Depends(obtener_repositorio_reunion),
    repo_miembro_reunion: RepositorioMiembroReunion = Depends(obtener_repositorio_miembro_reunion),
    repo_notificacion: RepositorioNotificacion = Depends(obtener_repositorio_notificacion),
    repo_acta: RepositorioActa = Depends(obtener_repositorio_acta),
    repo_usuario: RepositorioUsuario = Depends(obtener_repositorio_usuario)
) -> ServicioReunion:
    """
    Provee una instancia de ServicioReunion.
    """
    return ServicioReunion(repo_reunion, repo_miembro_reunion, repo_notificacion, repo_acta, repo_usuario)

def obtener_repositorio_finanzas(db: SesionBD = Depends(obtener_bd)) -> RepositorioFinanzas:
    """
    Provee una instancia de RepositorioFinanzas.
    """
    return RepositorioFinanzas(db)

def obtener_servicio_financiero(
    repositorio_finanzas: RepositorioFinanzas = Depends(obtener_repositorio_finanzas)
) -> ServicioFinanciero:
    """
    Provee una instancia del servicio financiero.
    """
    return ServicioFinanciero(repositorio_finanzas)
