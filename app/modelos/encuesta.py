# -*- coding: utf-8 -*-
# app/modelos/encuesta.py

from sqlalchemy import Column, Integer, Text, Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
from app.db import Base
from .usuario import Usuario

class Encuesta(Base):
    """
    Modelo que representa una encuesta creada por un usuario.
    Mapea a la tabla 'surveys' en la base de datos.
    """
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)  # Corregido: String importado de sqlalchemy
    creator_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    questions = Column(Text, nullable=False)  # Se espera JSON serializado
    deadline_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con el modelo Usuario
    creador = relationship("Usuario", back_populates="encuestas", lazy='joined')

    def __repr__(self):
        return f"<Encuesta(id={self.id}, creador_id={self.creator_id}, deadline={self.deadline_date})>"
