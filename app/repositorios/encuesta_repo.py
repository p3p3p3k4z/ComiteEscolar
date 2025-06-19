# -*- coding: utf-8 -*-
# app/repositorios/encuesta_repo.py

from sqlalchemy.orm import Session as SesionBD
from app.modelos.encuesta import Encuesta
from typing import Optional, List

class RepositorioEncuesta:
    """
    Repositorio para operaciones CRUD de la entidad Encuesta.
    """

    def __init__(self, sesion_bd: SesionBD):
        self.db = sesion_bd

    def obtener_por_id(self, id_encuesta: int) -> Optional[Encuesta]:
        """Obtiene una encuesta por su ID."""
        return self.db.query(Encuesta).filter(Encuesta.id == id_encuesta).first()

    def obtener_todas(self) -> List[Encuesta]:
        """Obtiene todas las encuestas."""
        return self.db.query(Encuesta).all()

    def guardar(self, encuesta: Encuesta) -> Encuesta:
        """Guarda una nueva encuesta en la base de datos."""
        self.db.add(encuesta)
        self.db.commit()
        self.db.refresh(encuesta)
        return encuesta

    def actualizar(self, encuesta: Encuesta) -> Encuesta:
        """Actualiza una encuesta existente en la base de datos."""
        self.db.commit()
        self.db.refresh(encuesta)
        return encuesta

    def eliminar(self, encuesta: Encuesta):
        """Elimina una encuesta de la base de datos."""
        self.db.delete(encuesta)
        self.db.commit()

    def obtener_por_usuario(self, id_usuario: int) -> List[Encuesta]:
        """Obtiene todas las encuestas creadas por un usuario."""
        return self.db.query(Encuesta).filter(Encuesta.creator_id == id_usuario).all()
