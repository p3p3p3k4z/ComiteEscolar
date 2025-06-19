# -*- coding: utf-8 -*-
# app/repositorios/reunion_repo.py

from sqlalchemy.orm import Session as SesionBD
from app.modelos.reunion import Reunion, MiembroReunion, Notificacion, Acta
from typing import Optional, List
from datetime import date

class RepositorioReunion:
    """
    Repositorio para operaciones CRUD de Reuniones.
    """
    def __init__(self, sesion_bd: SesionBD):
        self.db = sesion_bd

    def obtener_por_id(self, id_reunion: int) -> Optional[Reunion]:
        """Obtiene una reunión por su ID."""
        return self.db.query(Reunion).filter(Reunion.id == id_reunion).first()

    def obtener_todas(self) -> List[Reunion]:
        """Obtiene todas las reuniones."""
        return self.db.query(Reunion).all()

    def obtener_por_fecha(self, fecha: date) -> List[Reunion]:
        """Obtiene reuniones por fecha."""
        return self.db.query(Reunion).filter(Reunion.fecha == fecha).all()

    def guardar(self, reunion: Reunion) -> Reunion:
        """Guarda una nueva reunión."""
        self.db.add(reunion)
        self.db.commit()
        self.db.refresh(reunion)
        return reunion

    def actualizar(self, reunion: Reunion) -> Reunion:
        """Actualiza una reunión existente."""
        self.db.commit()
        self.db.refresh(reunion)
        return reunion

    def eliminar(self, reunion: Reunion):
        """Elimina una reunión."""
        self.db.delete(reunion)
        self.db.commit()

class RepositorioMiembroReunion:
    """
    Repositorio para operaciones CRUD de MiembroReunion.
    """
    def __init__(self, sesion_bd: SesionBD):
        self.db = sesion_bd

    def obtener_miembros_por_reunion(self, id_reunion: int) -> List[MiembroReunion]:
        """Obtiene todos los miembros de una reunión."""
        return self.db.query(MiembroReunion).filter(MiembroReunion.id_reunion == id_reunion).all()

    def agregar_miembro(self, miembro_reunion: MiembroReunion) -> MiembroReunion:
        """Agrega un miembro a una reunión."""
        self.db.add(miembro_reunion)
        self.db.commit()
        self.db.refresh(miembro_reunion)
        return miembro_reunion

    def eliminar_miembros_reunion(self, id_reunion: int):
        """Elimina todos los miembros de una reunión."""
        self.db.query(MiembroReunion).filter(MiembroReunion.id_reunion == id_reunion).delete()
        self.db.commit()

class RepositorioNotificacion:
    """
    Repositorio para operaciones CRUD de Notificaciones.
    """
    def __init__(self, sesion_bd: SesionBD):
        self.db = sesion_bd

    def obtener_por_reunion(self, id_reunion: int) -> List[Notificacion]:
        """Obtiene todas las notificaciones de una reunión."""
        return self.db.query(Notificacion).filter(Notificacion.id_reunion == id_reunion).all()

    def guardar(self, notificacion: Notificacion) -> Notificacion:
        """Guarda una nueva notificación."""
        self.db.add(notificacion)
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion

class RepositorioActa:
    """
    Repositorio para operaciones CRUD de Actas.
    """
    def __init__(self, sesion_bd: SesionBD):
        self.db = sesion_bd

    def obtener_por_reunion(self, id_reunion: int) -> Optional[Acta]:
        """Obtiene el acta de una reunión."""
        return self.db.query(Acta).filter(Acta.id_reunion == id_reunion).first()

    def guardar(self, acta: Acta) -> Acta:
        """Guarda una nueva acta."""
        self.db.add(acta)
        self.db.commit()
        self.db.refresh(acta)
        return acta

    def actualizar(self, acta: Acta) -> Acta:
        """Actualiza un acta existente."""
        self.db.commit()
        self.db.refresh(acta)
        return acta
