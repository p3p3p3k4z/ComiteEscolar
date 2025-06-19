# app/servicios/comite_servicio.py
from app.modelos.comite import Comite
from typing import Optional

class ServicioComite:
    def __init__(self, repositorio_comite):
        self.repo = repositorio_comite

    def crear_comite(self, nombre: str, periodo: str) -> Comite:
        if not nombre or not periodo:
            raise ValueError("Nombre y periodo son obligatorios")
        
        nuevo_comite = Comite(name=nombre, period=periodo)
        return self.repo.crear_comite(nuevo_comite)

    def actualizar_comite(self, id_comite: int, nombre: Optional[str] = None, status: Optional[str] = None) -> Comite:
        comite = self.repo.obtener_por_id(id_comite)
        if not comite:
            raise ValueError("Comité no encontrado")

        if nombre:
            comite.name = nombre
        if status:
            comite.status = status

        return self.repo.actualizar_comite(comite)