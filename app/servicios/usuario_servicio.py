# -*- coding: utf-8 -*-
# app/servicios/usuario_servicio.py

from app.modelos.usuario import Usuario
from app.repositorios.usuario_repo import RepositorioUsuario
from typing import Optional, List

class ServicioUsuario:
    """
    Clase de Servicio para la lógica de negocio relacionada con los Usuarios.
    """
    def __init__(self, repositorio_usuario: RepositorioUsuario):
        self.repositorio_usuario = repositorio_usuario

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        password_hash: str, 
        rol: str
    ) -> Usuario:
        """
        Crea un nuevo usuario en el sistema.
        """
        if not all([nombre, apellido, email, password_hash, rol]):
            raise ValueError("Todos los campos de usuario son obligatorios.")

        if self.repositorio_usuario.obtener_por_email(email):
            raise ValueError(f"Ya existe un usuario con el email '{email}'.")

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password_hash=password_hash,
            rol=rol
        )
        try:
            usuario_guardado = self.repositorio_usuario.guardar(nuevo_usuario)
            return usuario_guardado
        except Exception as e:
            raise RuntimeError(f"Error al guardar el usuario en la base de datos: {e}")

    def obtener_usuario(self, id_usuario: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID."""
        return self.repositorio_usuario.obtener_por_id(id_usuario)

    def obtener_todos_los_usuarios(self) -> List[Usuario]:
        """Obtiene todos los usuarios."""
        return self.repositorio_usuario.obtener_todos()

    def actualizar_usuario(
        self,
        id_usuario: int,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None,
        email: Optional[str] = None,
        password_hash: Optional[str] = None,
        rol: Optional[str] = None
    ) -> Usuario:
        """Actualiza los datos de un usuario existente."""
        usuario_a_actualizar = self.repositorio_usuario.obtener_por_id(id_usuario)
        if not usuario_a_actualizar:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado.")

        if email:
            usuario_existente = self.repositorio_usuario.obtener_por_email(email)
            if usuario_existente and usuario_existente.id != id_usuario:
                raise ValueError(f"Ya existe un usuario con el email '{email}'.")
            usuario_a_actualizar.email = email
        if nombre:
            usuario_a_actualizar.nombre = nombre
        if apellido:
            usuario_a_actualizar.apellido = apellido
        if password_hash:
            usuario_a_actualizar.password_hash = password_hash
        if rol:
            usuario_a_actualizar.rol = rol

        return self.repositorio_usuario.actualizar(usuario_a_actualizar)

    def eliminar_usuario(self, id_usuario: int):
        """Elimina un usuario por su ID."""
        usuario_a_eliminar = self.repositorio_usuario.obtener_por_id(id_usuario)
        if not usuario_a_eliminar:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado.")
        self.repositorio_usuario.eliminar(usuario_a_eliminar)

     # --- FUNCIÓN DE VALIDACIÓN ---
    def validar_credenciales(self, email_ingresado: str, password_ingresada: str) -> Optional[Usuario]:
        """
        Valida las credenciales de un usuario (email y contraseña) SIN HASHEO.
        Regresa el objeto Usuario si la validación es exitosa, de lo contrario None.
        """
        usuario = self.repositorio_usuario.obtener_por_email(email_ingresado)

        if usuario:
            if hasattr(usuario, 'password_hash') and usuario.password_hash == password_ingresada:
                return usuario
            else:
                print("Contraseña no coincide.")
                return None
        else:
            print(f"Usuario con email '{email_ingresado}' no encontrado.")
            return None