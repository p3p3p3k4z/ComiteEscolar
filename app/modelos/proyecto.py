# -*- coding: utf-8 -*-
# app/modelos/proyecto.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base # Importa Base desde el nuevo archivo app/db.py
from .usuario import Usuario # Importa el modelo Usuario para la relación

class Proyecto(Base):
    """
    Clase de modelo para representar un Proyecto Escolar.
    Mapea a la tabla 'projects' en la base de datos.
    """
    __tablename__ = 'projects' # El nombre de la tabla en la DB se mantiene en inglés

    id = Column(Integer, primary_key=True, index=True)
    # Mapeo explícito de 'nombre' a la columna 'name' de la DB
    nombre = Column('name', String(255), unique=True, nullable=False)
    # Mapeo explícito de 'id_usuario_responsable' a la columna 'responsible_user_id' de la DB
    id_usuario_responsable = Column('responsible_user_id', Integer, ForeignKey('users.id'), nullable=True)
    # Mapeo explícito de 'fecha_inicio' a la columna 'start_date' de la DB
    fecha_inicio = Column('start_date', Date, nullable=False)
    # Mapeo explícito de 'fecha_fin' a la columna 'end_date' de la DB
    fecha_fin = Column('end_date', Date, nullable=True)
    # Mapeo explícito de 'ruta_documento' a la columna 'document_path' de la DB
    ruta_documento = Column('document_path', String(255), nullable=True)
    # Mapeo explícito de 'estado' a la columna 'status' de la DB
    estado = Column('status', String(50), default='activo', nullable=False) # Ej: 'activo', 'finalizado', 'pendiente', 'aprobado', 'rechazado'

    # Relación con la tabla de usuarios
    # lazy='joined' cargará automáticamente el usuario responsable cuando se cargue un proyecto
    usuario_responsable = relationship("Usuario", back_populates="proyectos", lazy='joined')

    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre='{self.nombre}', estado='{self.estado}')>"

    def establecer_activo(self):
        """Marca el proyecto como activo."""
        self.estado = 'activo'

    def establecer_aprobado(self):
        """Marca el proyecto como aprobado."""
        self.estado = 'aprobado'

    def establecer_rechazado(self):
        """Marca el proyecto como rechazado."""
        self.estado = 'rechazado'

