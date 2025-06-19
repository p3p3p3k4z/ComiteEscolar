# -*- coding: utf-8 -*-
# app/api/reuniones.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional, List

from app.servicios.reunion_servicio import ServicioReunion
from app.api.dependecias import obtener_servicio_reunion

router = APIRouter(
    prefix="/reuniones",
    tags=["Reuniones"]
)

# Modelos Pydantic
class ReunionCrear(BaseModel):
    """Esquema para crear una nueva reunión."""
    fecha: date = Field(..., example="2025-08-15")
    hora: time = Field(..., example="09:00:00")
    lugar: str = Field(..., example="Sala de Juntas")
    agenda: Optional[str] = Field(None, example="Discusión de proyectos escolares")
    miembros_solicitados: List[int] = Field(..., example=[1, 2, 3])

class RespuestaReunion(BaseModel):
    """Esquema para la respuesta de una reunión."""
    id: int
    fecha: date
    hora: time
    lugar: str
    agenda: Optional[str]
    estado: str

    class Config:
        from_attributes = True

class ReunionActualizar(BaseModel):
    """Esquema para actualizar una reunión."""
    fecha: Optional[date] = Field(None, example="2025-08-16")
    hora: Optional[time] = Field(None, example="10:00:00")
    lugar: Optional[str] = Field(None, example="Auditorio")
    agenda: Optional[str] = Field(None, example="Agenda actualizada")
    estado: Optional[str] = Field(None, example="Confirmada")
    miembros_solicitados: Optional[List[int]] = Field(None, example=[1, 2, 4])

class NotificacionEnviar(BaseModel):
    """Esquema para enviar notificaciones."""
    tipo: str = Field(..., example="recordatorio")
    mensaje_personalizado: Optional[str] = Field(None, example="Recordatorio personalizado")

class ActaRegistrar(BaseModel):
    """Esquema para registrar un acta."""
    contenido: str = Field(..., example="Contenido del acta de la reunión...")
    generar_pdf: bool = Field(True, example=True)

@router.post("/", response_model=RespuestaReunion, status_code=status.HTTP_201_CREATED)
async def programar_reunion(
    datos_reunion: ReunionCrear,
    servicio_reunion: ServicioReunion = Depends(obtener_servicio_reunion)
):
    """Programa una nueva reunión del Comité Escolar."""
    try:
        nueva_reunion = servicio_reunion.programar_reunion(
            fecha=datos_reunion.fecha,
            hora=datos_reunion.hora,
            lugar=datos_reunion.lugar,
            agenda=datos_reunion.agenda,
            miembros_solicitados=datos_reunion.miembros_solicitados
        )
        return nueva_reunion
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al programar la reunión: {e}"
        )

@router.get("/{id_reunion}", response_model=RespuestaReunion)
async def obtener_reunion(
    id_reunion: int,
    servicio_reunion: ServicioReunion = Depends(obtener_servicio_reunion)
):
    """Obtiene los detalles de una reunión por su ID."""
    reunion = servicio_reunion.obtener_reunion(id_reunion)
    if not reunion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reunión con ID {id_reunion} no encontrada."
        )
    return reunion

@router.get("/", response_model=List[RespuestaReunion])
async def obtener_todas_reuniones(
    servicio_reunion: ServicioReunion = Depends(obtener_servicio_reunion)
):
    """Obtiene todas las reuniones."""
    reuniones = servicio_reunion.obtener_todas_reuniones()
    return reuniones

@router.put("/{id_reunion}", response_model=RespuestaReunion)
async def actualizar_reunion(
    id_reunion: int,
    datos_reunion: ReunionActualizar,
    servicio_reunion: ServicioReunion = Depends(obtener_servicio_reunion)
):
    """Actualiza una reunión existente."""
    try:
        reunion_actualizada = servicio_reunion.actualizar_reunion(
            id_reunion=id_reunion,
            fecha=datos_reunion.fecha,
            hora=datos_reunion.hora,
            lugar=datos_reunion.lugar,
            agenda=datos_reunion.agenda,
            estado=datos_reunion.estado,
            miembros_solicitados=datos_reunion.miembros_solicitados
        )
        return reunion_actualizada
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar la reunión: {e}"
        )

@router.post("/{id_reunion}/notificar")
async def enviar_notificacion(
    id_reunion: int,
    datos_notificacion: NotificacionEnviar,
    servicio_reunion: ServicioReunion = Depends(obtener_servicio_reunion)
):
    """Envía notificaciones sobre una reunión."""
    try:
        exito = servicio_reunion.enviar_notificacion(
            id_reunion=id_reunion,
            tipo=datos_notificacion.tipo,
            mensaje_personalizado=datos_notificacion.mensaje_personalizado
        )
        if exito:
            return {"mensaje": "Notificaciones enviadas exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al enviar las notificaciones"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{id_reunion}/acta")
async def registrar_acta(
    id_reunion: int,
    datos_acta: ActaRegistrar,
    servicio_reunion: ServicioReunion = Depends(obtener_servicio_reunion)
):
    """Registra el acta de una reunión."""
    try:
        acta = servicio_reunion.registrar_acta(
            id_reunion=id_reunion,
            contenido=datos_acta.contenido,
            generar_pdf=datos_acta.generar_pdf
        )
        return {
            "mensaje": "Acta registrada exitosamente",
            "id_acta": acta.id,
            "archivo_pdf": acta.archivo_pdf
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al registrar el acta: {e}"
        )

@router.get("/{id_reunion}/exportar-pdf")
async def exportar_pdf(
    id_reunion: int,
    servicio_reunion: ServicioReunion = Depends(obtener_servicio_reunion)
):
    """Exporta el acta de una reunión en formato PDF."""
    try:
        archivo_pdf = servicio_reunion.exportar_pdf(id_reunion)
        return {
            "mensaje": "PDF exportado exitosamente",
            "archivo_pdf": archivo_pdf
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al exportar el PDF: {e}"
        )

@router.put("/{id_reunion}/cancelar", response_model=RespuestaReunion)
async def cancelar_reunion(
    id_reunion: int,
    servicio_reunion: ServicioReunion = Depends(obtener_servicio_reunion)
):
    """Cancela una reunión."""
    try:
        reunion_cancelada = servicio_reunion.cancelar_reunion(id_reunion)
        return reunion_cancelada
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al cancelar la reunión: {e}"
        )
