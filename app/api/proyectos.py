# app/api/proyectos.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

from app.servicios.proyecto_servicio import ServicioProyecto
from app.api.dependecias import obtener_servicio_proyecto # Importa la dependencia del servicio de proyectos

router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"]
)

# Modelos Pydantic para la entrada y salida de datos de la API
class ProyectoCrear(BaseModel):
    """Esquema de datos para crear un nuevo proyecto."""
    nombre: str = Field(..., example="Campaña de reciclaje escolar")
    id_usuario_responsable: Optional[int] = Field(None, example=1, description="ID del usuario encargado del proyecto")
    fecha_inicio: date = Field(..., example="2025-09-01")
    fecha_fin: Optional[date] = Field(None, example="2025-12-31")
    ruta_documento: Optional[str] = Field(None, example="/docs/proyecto_reciclaje.pdf")

class RespuestaProyecto(BaseModel):
    """Esquema de datos para la respuesta de un proyecto."""
    id: int
    nombre: str
    id_usuario_responsable: Optional[int]
    fecha_inicio: date
    fecha_fin: Optional[date]
    ruta_documento: Optional[str]
    estado: str

    class Config:
        from_attributes = True # Permite que Pydantic mapee directamente desde modelos ORM

class ProyectoActualizar(BaseModel):
    """Esquema de datos para actualizar un proyecto."""
    nombre: Optional[str] = Field(None, example="Campaña de reciclaje ampliada")
    id_usuario_responsable: Optional[int] = Field(None, example=2, description="Nuevo ID del usuario encargado")
    fecha_inicio: Optional[date] = Field(None, example="2025-09-15")
    fecha_fin: Optional[date] = Field(None, example="2026-01-31")
    ruta_documento: Optional[str] = Field(None, example="/docs/proyecto_reciclaje_v2.pdf")
    estado: Optional[str] = Field(None, example="finalizado", description="Nuevo estado del proyecto")

@router.post("/", response_model=RespuestaProyecto, status_code=status.HTTP_201_CREATED)
async def crear_proyecto(
    datos_proyecto: ProyectoCrear,
    servicio_proyecto: ServicioProyecto = Depends(obtener_servicio_proyecto)
):
    """
    Endpoint para agregar un nuevo proyecto escolar.
    """
    try:
        # Aquí se simularía la autenticación del Director si fuera necesaria
        # (ej. verificar rol del usuario actual si tuvieras un sistema de auth)

        nuevo_proyecto = servicio_proyecto.agregar_proyecto(
            nombre=datos_proyecto.nombre,
            id_usuario_responsable=datos_proyecto.id_usuario_responsable,
            fecha_inicio=datos_proyecto.fecha_inicio,
            fecha_fin=datos_proyecto.fecha_fin,
            ruta_documento=datos_proyecto.ruta_documento
        )
        return nuevo_proyecto
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except RuntimeError as e: # Para errores de base de datos o internos
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al crear el proyecto: {e}"
        )

@router.get("/{id_proyecto}", response_model=RespuestaProyecto)
async def obtener_proyecto(
    id_proyecto: int,
    servicio_proyecto: ServicioProyecto = Depends(obtener_servicio_proyecto)
):
    """
    Endpoint para obtener los detalles de un proyecto por su ID.
    """
    proyecto = servicio_proyecto.obtener_proyecto(id_proyecto)
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con ID {id_proyecto} no encontrado."
        )
    return proyecto

@router.get("/", response_model=List[RespuestaProyecto])
async def obtener_todos_los_proyectos(
    servicio_proyecto: ServicioProyecto = Depends(obtener_servicio_proyecto)
):
    """
    Endpoint para obtener todos los proyectos.
    """
    proyectos = servicio_proyecto.obtener_todos_los_proyectos()
    return proyectos

@router.put("/{id_proyecto}", response_model=RespuestaProyecto)
async def actualizar_proyecto(
    id_proyecto: int,
    datos_proyecto: ProyectoActualizar,
    servicio_proyecto: ServicioProyecto = Depends(obtener_servicio_proyecto)
):
    """
    Endpoint para actualizar los datos de un proyecto existente.
    """
    try:
        proyecto_actualizado = servicio_proyecto.actualizar_proyecto(
            id_proyecto=id_proyecto,
            nombre=datos_proyecto.nombre,
            id_usuario_responsable=datos_proyecto.id_usuario_responsable,
            fecha_inicio=datos_proyecto.fecha_inicio,
            fecha_fin=datos_proyecto.fecha_fin,
            ruta_documento=datos_proyecto.ruta_documento,
            estado=datos_proyecto.estado
        )
        return proyecto_actualizado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException: # Vuelve a lanzar HTTPExceptions desde la capa de servicio
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar el proyecto: {e}"
        )

@router.delete("/{id_proyecto}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_proyecto(
    id_proyecto: int,
    servicio_proyecto: ServicioProyecto = Depends(obtener_servicio_proyecto)
):
    """
    Endpoint para eliminar un proyecto por su ID.
    """
    try:
        servicio_proyecto.eliminar_proyecto(id_proyecto)
        return {"mensaje": "Proyecto eliminado exitosamente."}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar el proyecto: {e}"
        )
