# schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

# Base schemas
class CampeonatoBase(BaseModel):
    nombre: str
    anio: int

class CampeonatoCreate(CampeonatoBase):
    pass

class CampeonatoResponse(CampeonatoBase):
    id: UUID
    
    class Config:
        from_attributes = True

class PilotoBase(BaseModel):
    nombre: str
    pais: Optional[str] = None

class PilotoCreate(PilotoBase):
    pass

class PilotoResponse(PilotoBase):
    id: UUID
    numero_auto: Optional[int] = None
    
    class Config:
        from_attributes = True

class CircuitoBase(BaseModel):
    nombre: Optional[str] = None
    distancia: Optional[float] = None

class CircuitoResponse(CircuitoBase):
    id: int
    
    class Config:
        from_attributes = True

class FechaBase(BaseModel):
    nombre: str
    fecha_desde: date
    fecha_hasta: Optional[date] = None

class FechaCreate(FechaBase):
    campeonato_id: UUID
    circuito: Optional[int] = None

class FechaResponse(FechaBase):
    id: UUID
    campeonato_id: Optional[UUID]
    circuito: Optional[int]
    circuito_nombre: Optional[str] = None
    
    class Config:
        from_attributes = True

class CarreraFinalResponse(BaseModel):
    id: UUID
    posicion: Optional[int]
    puntos: Optional[int]
    presente: Optional[bool]
    vueltas: Optional[int]
    tiempo: Optional[Decimal]
    excluido: Optional[bool]
    diferencia_primero: Optional[float]
    piloto_nombre: str
    piloto_pais: Optional[str]
    
    class Config:
        from_attributes = True

class ClasificacionResponse(BaseModel):
    id: UUID
    tiempo: Optional[Decimal]
    posicion: Optional[int]
    vueltas: Optional[int]
    sector_1: Optional[float]
    sector_2: Optional[float]
    sector_3: Optional[float]
    diferencia_primero: Optional[float]
    piloto_nombre: str
    piloto_pais: Optional[str]
    
    class Config:
        from_attributes = True

class EntrenamientoResponse(BaseModel):
    id: UUID
    numero: int
    tiempo: Optional[Decimal]
    posicion: Optional[int]
    vueltas: Optional[int]
    sector_1: Optional[float]
    sector_2: Optional[float]
    sector_3: Optional[float]
    diferencia_primero: Optional[float]
    piloto_nombre: str
    piloto_pais: Optional[str]
    
    class Config:
        from_attributes = True

class SerieClasificatoriaResponse(BaseModel):
    id: UUID
    numero: int
    posicion: Optional[int]
    puntos: Optional[int]
    vueltas: Optional[int]
    tiempo: Optional[Decimal]
    mejor_tiempo: Optional[Decimal]
    fecha: Optional[date]
    excluido: Optional[bool]
    diferencia_primero: Optional[float]
    piloto_nombre: str
    piloto_pais: Optional[str]
    
    class Config:
        from_attributes = True

class PosicionCampeonatoResponse(BaseModel):
    piloto_nombre: str
    piloto_pais: Optional[str]
    puntos_totales: int
    numero_auto: Optional[int]
    posicion: int
    
    class Config:
        from_attributes = True

class HorarioResponse(BaseModel):
    id: UUID
    tipo_sesion: str
    horario: datetime
    duracion: Optional[str]
    
    class Config:
        from_attributes = True