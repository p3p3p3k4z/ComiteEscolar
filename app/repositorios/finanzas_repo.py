# -*- coding: utf-8 -*-
# app/repositorios/finanzas_repo.py

from sqlalchemy.orm import Session
from app.modelos.movimientofinanciero import MovimientoFinanciero

class RepositorioFinanzas:
    """
    Repositorio para manejar operaciones CRUD sobre la tabla financial_movements.
    """

    def __init__(self, db: Session):
        self.db = db

    def crear(self, movimiento: MovimientoFinanciero) -> MovimientoFinanciero:
        self.db.add(movimiento)
        self.db.commit()
        self.db.refresh(movimiento)
        return movimiento

    def obtener_por_id(self, id_movimiento: int) -> MovimientoFinanciero | None:
        return self.db.query(MovimientoFinanciero).filter(MovimientoFinanciero.id == id_movimiento).first()

    def obtener_todos(self) -> list[MovimientoFinanciero]:
        return self.db.query(MovimientoFinanciero).order_by(MovimientoFinanciero.fecha_transaccion.desc()).all()

    def actualizar(self, movimiento: MovimientoFinanciero) -> MovimientoFinanciero:
        self.db.commit()
        self.db.refresh(movimiento)
        return movimiento

    def eliminar(self, movimiento: MovimientoFinanciero):
        self.db.delete(movimiento)
        self.db.commit()
