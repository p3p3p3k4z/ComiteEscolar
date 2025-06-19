# app/repositorios/comite_repo.py
from typing import List, Optional
from app.modelos.comite import Comite

class RepositorioComite:
    def __init__(self, sesion_bd):
        self.db = sesion_bd

    def crear_comite(self, comite: Comite) -> Comite:
        self.db.add(comite)
        self.db.commit()
        self.db.refresh(comite)
        return comite

    def obtener_por_id(self, id_comite: int) -> Optional[Comite]:
        return self.db.query(Comite).filter(Comite.id == id_comite).first()

    def obtener_todos(self) -> List[Comite]:
        return self.db.query(Comite).all()

    def actualizar_comite(self, comite: Comite) -> Comite:
        self.db.commit()
        self.db.refresh(comite)
        return comite

    def eliminar_comite(self, comite: Comite):
        self.db.delete(comite)
        self.db.commit()