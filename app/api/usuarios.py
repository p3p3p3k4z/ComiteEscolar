# -*- coding: utf-8 -*-
# app/api/usuarios.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List

from app.servicios.usuario_servicio import ServicioUsuario
from app.api.dependecias import obtener_servicio_usuario # Importa la dependencia del servicio de usuarios

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# Modelos Pydantic para la entrada y salida de datos de la API
class UsuarioCrear(BaseModel):
    """Esquema de datos para crear un nuevo usuario."""
    nombre: str = Field(..., example="Juan")
    apellido: str = Field(..., example="Perez")
    email: str = Field(..., example="juan.perez@example.com")
    password_hash: str = Field(..., example="secure_hashed_password") # En producción, esto sería un hash
    rol: str = Field(..., example="Director", description="Rol del usuario (Director, Secretario, PadreDeFamilia, etc.)")

class RespuestaUsuario(BaseModel):
    """Esquema de datos para la respuesta de un usuario."""
    id: int
    nombre: str
    apellido: str
    email: str
    rol: str

    class Config:
        from_attributes = True # Permite que Pydantic mapee directamente desde modelos ORM

class UsuarioActualizar(BaseModel):
    """Esquema de datos para actualizar un usuario."""
    nombre: Optional[str] = Field(None, example="Juan Carlos")
    apellido: Optional[str] = Field(None, example="Perez Gomez")
    email: Optional[str] = Field(None, example="juan.carlos@example.com")
    password_hash: Optional[str] = Field(None, example="new_hashed_password")
    rol: Optional[str] = Field(None, example="Administrador")


@router.post("/", response_model=RespuestaUsuario, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    datos_usuario: UsuarioCrear,
    servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario)
):
    """
    Endpoint para crear un nuevo usuario.
    """
    try:
        nuevo_usuario = servicio_usuario.crear_usuario(
            nombre=datos_usuario.nombre,
            apellido=datos_usuario.apellido,
            email=datos_usuario.email,
            password_hash=datos_usuario.password_hash,
            rol=datos_usuario.rol
        )
        return nuevo_usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear el usuario: {e}"
        )

@router.get("/{id_usuario}", response_model=RespuestaUsuario)
async def obtener_usuario(
    id_usuario: int,
    servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario)
):
    """
    Endpoint para obtener los detalles de un usuario por su ID.
    """
    usuario = servicio_usuario.obtener_usuario(id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {id_usuario} no encontrado."
        )
    return usuario

@router.get("/", response_model=List[RespuestaUsuario])
async def obtener_todos_los_usuarios(
    servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario)
):
    """
    Endpoint para obtener todos los usuarios.
    """
    usuarios = servicio_usuario.obtener_todos_los_usuarios()
    return usuarios

@router.put("/{id_usuario}", response_model=RespuestaUsuario)
async def actualizar_usuario(
    id_usuario: int,
    datos_usuario: UsuarioActualizar,
    servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario)
):
    """
    Endpoint para actualizar los datos de un usuario existente.
    """
    try:
        usuario_actualizado = servicio_usuario.actualizar_usuario(
            id_usuario=id_usuario,
            nombre=datos_usuario.nombre,
            apellido=datos_usuario.apellido,
            email=datos_usuario.email,
            password_hash=datos_usuario.password_hash,
            rol=datos_usuario.rol
        )
        return usuario_actualizado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException: # Re-lanza HTTPExceptions desde la capa de servicio
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar el usuario: {e}"
        )

@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    id_usuario: int,
    servicio_usuario: ServicioUsuario = Depends(obtener_servicio_usuario)
):
    """
    Endpoint para eliminar un usuario por su ID.
    """
    try:
        servicio_usuario.eliminar_usuario(id_usuario)
        return {"mensaje": "Usuario eliminado exitosamente."}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar el usuario: {e}"
        )
