# -*- coding: utf-8 -*-
# app/api/finanzas.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List
from app.servicios.finanzas_servicios import ServicioFinanciero
from app.api.dependecias import obtener_servicio_financiero

router = APIRouter(
    prefix="/finanzas",
    tags=["Movimientos Financieros"]
)

# 📦 Modelos Pydantic
class MovimientoFinancieroCrear(BaseModel):
    tipo: str = Field(..., example="ingreso")
    monto: float = Field(..., example=2500.00)
    fecha_transaccion: Optional[date] = Field(None, example="2025-06-18")
    concepto: str = Field(..., example="Donación de padres")
    id_usuario_registrador: Optional[int] = Field(None, example=1)

class MovimientoFinancieroActualizar(BaseModel):
    tipo: Optional[str] = Field(None, example="egreso")
    monto: Optional[float] = Field(None, example=1250.00)
    fecha_transaccion: Optional[date] = Field(None, example="2025-06-19")
    concepto: Optional[str] = Field(None, example="Compra de útiles")
    id_usuario_registrador: Optional[int] = Field(None, example=2)

class RespuestaMovimientoFinanciero(BaseModel):
    id: int
    tipo: str
    monto: float
    fecha_transaccion: date
    concepto: str
    id_usuario_registrador: Optional[int]

    class Config:
        from_attributes = True

# 📌 Endpoints

@router.post("/", response_model=RespuestaMovimientoFinanciero, status_code=status.HTTP_201_CREATED)
async def crear_movimiento(
    datos: MovimientoFinancieroCrear,
    servicio: ServicioFinanciero = Depends(obtener_servicio_financiero)
):
    try:
        return servicio.crear_movimiento(datos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@router.get("/{id_movimiento}", response_model=RespuestaMovimientoFinanciero)
async def obtener_movimiento(
    id_movimiento: int,
    servicio: ServicioFinanciero = Depends(obtener_servicio_financiero)
):
    movimiento = servicio.obtener_movimiento(id_movimiento)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")
    return movimiento

@router.get("/", response_model=List[RespuestaMovimientoFinanciero])
async def listar_movimientos(servicio: ServicioFinanciero = Depends(obtener_servicio_financiero)):
    return servicio.obtener_todos_los_movimientos()

@router.put("/{id_movimiento}", response_model=RespuestaMovimientoFinanciero)
async def actualizar_movimiento(
    id_movimiento: int,
    datos: MovimientoFinancieroActualizar,
    servicio: ServicioFinanciero = Depends(obtener_servicio_financiero)
):
    try:
        return servicio.actualizar_movimiento(id_movimiento, datos)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")

@router.delete("/{id_movimiento}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_movimiento(
    id_movimiento: int,
    servicio: ServicioFinanciero = Depends(obtener_servicio_financiero)
):
    try:
        servicio.eliminar_movimiento(id_movimiento)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
