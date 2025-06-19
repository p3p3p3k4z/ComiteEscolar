# -*- coding: utf-8 -*-
# app/servicios/finanzas_servicio.py

from sqlalchemy.orm import Session
from app.modelos.movimientofinanciero import MovimientoFinanciero
from datetime import date
from typing import Optional, List
from pydantic import BaseModel
from app.repositorios.finanzas_repo import RepositorioFinanzas
from app.repositorios.usuario_repo import RepositorioUsuario

class MovimientoFinancieroCrear(BaseModel):
    tipo: str
    monto: float
    fecha_transaccion: Optional[date]
    concepto: str
    id_usuario_registrador: Optional[int]

class MovimientoFinancieroActualizar(BaseModel):
    tipo: Optional[str]
    monto: Optional[float]
    fecha_transaccion: Optional[date]
    concepto: Optional[str]
    id_usuario_registrador: Optional[int]


class ServicioFinanciero:
    def __init__(self, repo_finanzas: RepositorioFinanzas, repo_usuarios: RepositorioUsuario):
        self.repo_finanzas = repo_finanzas
        self.repo_usuarios = repo_usuarios

    def crear_movimiento(self, datos: MovimientoFinancieroCrear) -> MovimientoFinanciero:
        movimiento = MovimientoFinanciero(
            tipo=datos.tipo,
            monto=datos.monto,
            fecha_transaccion=datos.fecha_transaccion or date.today(),
            concepto=datos.concepto,
            id_usuario_registrador=datos.id_usuario_registrador
        )
        return self.repo_finanzas.crear(movimiento)

    def obtener_movimiento(self, id_movimiento: int) -> Optional[MovimientoFinanciero]:
        return self.repo_finanzas.obtener_por_id(id_movimiento)

    def obtener_todos_los_movimientos(self) -> List[MovimientoFinanciero]:
        return self.repo_finanzas.obtener_todos()

    def actualizar_movimiento(self, id_movimiento: int, datos: MovimientoFinancieroActualizar) -> MovimientoFinanciero:
        movimiento = self.repo_finanzas.obtener_por_id(id_movimiento)
        if not movimiento:
            raise ValueError("Movimiento no encontrado")

        for campo, valor in datos.dict(exclude_unset=True).items():
            setattr(movimiento, campo, valor)

        return self.repo_finanzas.crear(movimiento)  # reutiliza crear para hacer commit y refresh

    def eliminar_movimiento(self, id_movimiento: int):
        movimiento = self.repo_finanzas.obtener_por_id(id_movimiento)
        if not movimiento:
            raise ValueError("Movimiento no encontrado")

        self.repo_finanzas.eliminar(movimiento)