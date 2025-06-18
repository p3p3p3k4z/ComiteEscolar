# app/api/dependecias.py

from sqlalchemy.orm import Session as SesionBD # Renombra para evitar conflicto
from app.__init__ import Session # Importa tu factoría de sesiones
from app.repositorios.proyecto_repo import RepositorioProyecto
from app.servicios.proyecto_servicio import ServicioProyecto
from fastapi import Depends # <--- Se agregó 'Depends' aquí
# Importa otros repositorios y servicios si los necesitas en las dependencias
# from app.repositorios.usuario_repo import RepositorioUsuario
# from app.servicios.usuario_servicio import ServicioUsuario


def obtener_bd():
    """
    Provee una sesión de base de datos para las rutas de la API.
    Asegura que la sesión se cierre después de la solicitud.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

def obtener_repositorio_proyecto(db: SesionBD = Depends(obtener_bd)) -> RepositorioProyecto:
    """
    Provee una instancia de RepositorioProyecto.
    """
    return RepositorioProyecto(db)

def obtener_servicio_proyecto(repositorio_proyecto: RepositorioProyecto = Depends(obtener_repositorio_proyecto)) -> ServicioProyecto:
    """
    Provee una instancia de ServicioProyecto.
    """
    return ServicioProyecto(repositorio_proyecto)

# Puedes añadir más dependencias para otros servicios aquí
# def obtener_repositorio_usuario(db: SesionBD = Depends(obtener_bd)) -> RepositorioUsuario:
#     return RepositorioUsuario(db)

# def obtener_servicio_usuario(repositorio_usuario: RepositorioUsuario = Depends(obtener_repositorio_usuario)) -> ServicioUsuario:
#     return ServicioUsuario(repositorio_usuario)
