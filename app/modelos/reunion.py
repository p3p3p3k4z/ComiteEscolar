# -*- coding: utf-8 -*-
# app/modelos/reunion.py

from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Reunion(Base):
    """
    Modelo para representar una Reunión del Comité Escolar.
    """
    __tablename__ = 'reuniones'

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    lugar = Column(String(255), nullable=False)
    agenda = Column(Text, nullable=True)
    estado = Column(String(50), default='Programada', nullable=False)

    # Relaciones
    miembros = relationship("MiembroReunion", back_populates="reunion", cascade="all, delete-orphan")
    notificaciones = relationship("Notificacion", back_populates="reunion", cascade="all, delete-orphan")
    actas = relationship("Acta", back_populates="reunion", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Reunion(id={self.id}, fecha='{self.fecha}', lugar='{self.lugar}', estado='{self.estado}')>"

class MiembroReunion(Base):
    """
    Modelo para representar la relación entre Reuniones y Miembros.
    """
    __tablename__ = 'miembros_reunion'

    id = Column(Integer, primary_key=True, index=True)
    id_reunion = Column(Integer, ForeignKey('reuniones.id'), nullable=False)
    id_miembro = Column(Integer, nullable=False)

    # Relaciones
    reunion = relationship("Reunion", back_populates="miembros")

    def __repr__(self):
        return f"<MiembroReunion(id_reunion={self.id_reunion}, id_miembro={self.id_miembro})>"

class Notificacion(Base):
    """
    Modelo para representar las Notificaciones de Reuniones.
    """
    __tablename__ = 'notificaciones'

    id = Column(Integer, primary_key=True, index=True)
    id_reunion = Column(Integer, ForeignKey('reuniones.id'), nullable=False)
    tipo = Column(String(50), nullable=False)  # 'confirmacion', 'recordatorio', 'modificacion', 'cancelacion'
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    reunion = relationship("Reunion", back_populates="notificaciones")

    def __repr__(self):
        return f"<Notificacion(id={self.id}, tipo='{self.tipo}', id_reunion={self.id_reunion})>"

class Acta(Base):
    """
    Modelo para representar las Actas de Reuniones.
    """
    __tablename__ = 'actas'

    id = Column(Integer, primary_key=True, index=True)
    id_reunion = Column(Integer, ForeignKey('reuniones.id'), nullable=False)
    contenido = Column(Text, nullable=False)
    archivo_pdf = Column(String(255), nullable=True)

    # Relaciones
    reunion = relationship("Reunion", back_populates="actas")

    def __repr__(self):
        return f"<Acta(id={self.id}, id_reunion={self.id_reunion})>"
