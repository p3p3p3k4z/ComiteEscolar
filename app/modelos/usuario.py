# -*- coding: utf-8 -*-
# app/modelos/usuario.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base # Importa Base desde el nuevo archivo app/db.py

class Usuario(Base):
    """
    Clase de modelo para representar un Usuario del sistema.
    Mapea a la tabla 'users' en la base de datos.
    """
    __tablename__ = 'users' # El nombre de la tabla en la DB se mantiene en inglés

    id = Column(Integer, primary_key=True, index=True)
    # Mapeo explícito de 'nombre' a la columna 'name' de la DB
    nombre = Column('name', String(100), nullable=False)
    # Mapeo explícito de 'apellido' a la columna 'last_name' de la DB
    apellido = Column('last_name', String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    # password_hash se mantiene con el nombre de columna de la DB
    password_hash = Column(String(255), nullable=False)
    # Mapeo explícito de 'rol' a la columna 'role' de la DB
    rol = Column('role', String(50), nullable=False) # Ej: 'Director', 'PadreDeFamilia'

    # Relación inversa con la tabla de proyectos, para acceder a los proyectos de un usuario
    proyectos = relationship("Proyecto", back_populates="usuario_responsable")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre} {self.apellido}', rol='{self.rol}')>"

    # Métodos de ejemplo, podrías añadir más lógica de usuario aquí
    def es_director(self) -> bool:
        return self.rol == 'Director'

    def es_padre_de_familia(self) -> bool:
        return self.rol == 'PadreDeFamilia'
