# -*- coding: utf-8 -*-
# app/modelos/proyecto.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.db import Base
from .usuario import Usuario  

class MovimientoFinanciero(Base):
    """
    Modelo que representa un movimiento financiero.
    Mapea a la tabla 'financial_movements' en la base de datos.
    """
    __tablename__ = 'financial_movements'

    id = Column(Integer, primary_key=True, index=True)
    type = Column('type', String(50), nullable=False)  # Ej: 'ingreso', 'egreso'
    amount = Column('amount', Numeric(10, 2), nullable=False)
    fecha_transaccion = Column('transaction_date', Date, nullable=False)
    concept = Column('concept', Text, nullable=False)
    id_usuario = Column('registered_by_user_id', Integer, ForeignKey('users.id'), nullable=True)

    usuario_registrador = relationship("Usuario", back_populates="movimientos", lazy='joined')

    def __repr__(self):
        return f"<financial(id={self.id}, tipo='{self.tipo}', monto={self.monto})>"
