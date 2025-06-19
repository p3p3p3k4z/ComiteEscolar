# -*- coding: utf-8 -*-
# app/repositorios/usuario_repo.py

from sqlalchemy.orm import Session as SesionBD
from app.modelos.usuario import Usuario
from typing import Optional, List

class RepositorioUsuario:
    """
    Clase Repositorio para operaciones CRUD de la entidad Usuario.
    """
    def __init__(self, sesion_bd: SesionBD):
        self.db = sesion_bd

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID."""
        return self.db.query(Usuario).filter(Usuario.id == id_usuario).first()

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su email."""
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def obtener_por_name(self, name: str) -> Optional[Usuario]:
        """Obtiene un usuario por su name."""
        return self.db.query(Usuario).filter(Usuario.email == name).first()

    def guardar(self, usuario: Usuario) -> Usuario:
        """Guarda un nuevo usuario en la base de datos."""
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def actualizar(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente en la base de datos."""
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar(self, usuario: Usuario):
        """Elimina un usuario de la base de datos."""
        self.db.delete(usuario)
        self.db.commit()

    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios."""
        return self.db.query(Usuario).all()
