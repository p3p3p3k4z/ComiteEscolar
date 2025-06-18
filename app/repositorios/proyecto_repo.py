# -*- coding: utf-8 -*-
# app/repositorios/proyecto_repo.py

from sqlalchemy.orm import Session as SesionBD # Renombra para evitar conflicto
from app.modelos.proyecto import Proyecto
from typing import Optional, List

class RepositorioProyecto:
    """
    Clase Repositorio para operaciones CRUD de la entidad Proyecto.
    """
    def __init__(self, sesion_bd: SesionBD):
        self.db = sesion_bd

    def obtener_por_id(self, id_proyecto: int) -> Optional[Proyecto]:
        """Obtiene un proyecto por su ID."""
        return self.db.query(Proyecto).filter(Proyecto.id == id_proyecto).first()

    def obtener_por_nombre(self, nombre: str) -> Optional[Proyecto]:
        """Obtiene un proyecto por su nombre (para verificar duplicados)."""
        return self.db.query(Proyecto).filter(Proyecto.nombre == nombre).first()

    def guardar(self, proyecto: Proyecto) -> Proyecto:
        """Guarda un nuevo proyecto en la base de datos."""
        self.db.add(proyecto)
        self.db.commit()
        self.db.refresh(proyecto) # Asegura que el objeto tenga el ID generado por la BD
        return proyecto

    def actualizar(self, proyecto: Proyecto) -> Proyecto:
        """Actualiza un proyecto existente en la base de datos."""
        self.db.commit() # Si el objeto ya está 'attached' a la sesión, commit guarda los cambios
        self.db.refresh(proyecto)
        return proyecto

    def eliminar(self, proyecto: Proyecto):
        """Elimina un proyecto de la base de datos."""
        self.db.delete(proyecto)
        self.db.commit()

    def obtener_todos(self) -> List[Proyecto]:
        """Obtiene todos los proyectos."""
        return self.db.query(Proyecto).all()
