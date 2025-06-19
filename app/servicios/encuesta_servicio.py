# -*- coding: utf-8 -*-
# app/servicios/encuesta_servicio.py

from typing import List, Optional
from app.modelos.encuesta import Encuesta
from app.repositorios.encuesta_repo import RepositorioEncuesta

class ServicioEncuesta:
    """
    Servicio que contiene la lógica de negocio para las encuestas.
    """

    def __init__(self, repo_encuesta: RepositorioEncuesta):
        self.repo = repo_encuesta

    def crear_encuesta(self, datos: dict) -> Encuesta:
        """
        Crea una nueva encuesta a partir de un diccionario de datos.
        """
        nueva_encuesta = Encuesta(
            creator_id=datos.get("creator_id"),
            questions=datos.get("questions"),
            deadline_date=datos.get("deadline_date"),
        )
        return self.repo.guardar(nueva_encuesta)

    def obtener_encuesta(self, id_encuesta: int) -> Optional[Encuesta]:
        """Obtiene una encuesta por su ID."""
        return self.repo.obtener_por_id(id_encuesta)

    def obtener_todas(self) -> List[Encuesta]:
        """Obtiene todas las encuestas disponibles."""
        return self.repo.obtener_todas()

    def obtener_por_usuario(self, id_usuario: int) -> List[Encuesta]:
        """Devuelve encuestas creadas por un usuario específico."""
        return self.repo.obtener_por_usuario(id_usuario)

    def actualizar_encuesta(self, encuesta: Encuesta) -> Encuesta:
        """Actualiza los datos de una encuesta ya existente."""
        return self.repo.actualizar(encuesta)

    def eliminar_encuesta(self, encuesta: Encuesta):
        """Elimina una encuesta existente."""
        self.repo.eliminar(encuesta)
