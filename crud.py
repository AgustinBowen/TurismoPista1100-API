# crud.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc
from models import *
from schemas import *
from typing import List, Optional

# ==================== CAMPEONATOS ====================
def get_all_campeonatos(db: Session) -> List[Campeonato]:
    return db.query(Campeonato).order_by(desc(Campeonato.anio)).all()

def get_campeonato_by_id(db: Session, campeonato_id: str) -> Optional[Campeonato]:
    return db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()

def create_campeonato_db(db: Session, campeonato: CampeonatoCreate) -> Campeonato:
    db_campeonato = Campeonato(**campeonato.dict())
    db.add(db_campeonato)
    db.commit()
    db.refresh(db_campeonato)
    return db_campeonato

# ==================== PILOTOS ====================
def get_all_pilotos(db: Session) -> List[PilotoResponse]:
    pilotos = db.query(Piloto).order_by(Piloto.nombre).all()
    return [PilotoResponse(id=str(p.id), nombre=p.nombre, pais=p.pais) for p in pilotos]

def get_pilotos_by_campeonato(db: Session, campeonato_id: str) -> List[PilotoResponse]:
    pilotos = db.query(Piloto)\
        .join(PilotoCampeonato)\
        .filter(PilotoCampeonato.campeonato_id == campeonato_id)\
        .order_by(Piloto.nombre).all()
    
    result = []
    for p in pilotos:
        pc = db.query(PilotoCampeonato)\
            .filter(PilotoCampeonato.piloto_id == p.id, 
                   PilotoCampeonato.campeonato_id == campeonato_id).first()
        result.append(PilotoResponse(
            id=str(p.id), 
            nombre=p.nombre, 
            pais=p.pais, 
            numero_auto=pc.numero_auto if pc else None
        ))
    return result

def create_piloto_db(db: Session, piloto: PilotoCreate) -> Piloto:
    db_piloto = Piloto(**piloto.dict())
    db.add(db_piloto)
    db.commit()
    db.refresh(db_piloto)
    return db_piloto

# ==================== FECHAS ====================
def get_all_fechas(db: Session) -> List[FechaResponse]:
    fechas = db.query(Fecha).options(joinedload(Fecha.circuito_rel)).order_by(Fecha.fecha_desde).all()
    return [FechaResponse(
        id=str(f.id),
        nombre=f.nombre,
        fecha_desde=f.fecha_desde,
        fecha_hasta=f.fecha_hasta,
        campeonato_id=str(f.campeonato_id) if f.campeonato_id else None,
        circuito=f.circuito,
        circuito_nombre=f.circuito_rel.nombre if f.circuito_rel else None
    ) for f in fechas]

def get_fechas_by_campeonato(db: Session, campeonato_id: str) -> List[FechaResponse]:
    fechas = db.query(Fecha)\
        .options(joinedload(Fecha.circuito_rel))\
        .filter(Fecha.campeonato_id == campeonato_id)\
        .order_by(Fecha.fecha_desde).all()
    
    return [FechaResponse(
        id=str(f.id),
        nombre=f.nombre,
        fecha_desde=f.fecha_desde,
        fecha_hasta=f.fecha_hasta,
        campeonato_id=str(f.campeonato_id) if f.campeonato_id else None,
        circuito=f.circuito,
        circuito_nombre=f.circuito_rel.nombre if f.circuito_rel else None
    ) for f in fechas]

def get_fecha_by_id(db: Session, fecha_id: str) -> Optional[FechaResponse]:
    fecha = db.query(Fecha)\
        .options(joinedload(Fecha.circuito_rel))\
        .filter(Fecha.id == fecha_id).first()
    
    if not fecha:
        return None
        
    return FechaResponse(
        id=str(fecha.id),
        nombre=fecha.nombre,
        fecha_desde=fecha.fecha_desde,
        fecha_hasta=fecha.fecha_hasta,
        campeonato_id=str(fecha.campeonato_id) if fecha.campeonato_id else None,
        circuito=fecha.circuito,
        circuito_nombre=fecha.circuito_rel.nombre if fecha.circuito_rel else None
    )

def create_fecha_db(db: Session, fecha: FechaCreate) -> Fecha:
    db_fecha = Fecha(**fecha.dict())
    db.add(db_fecha)
    db.commit()
    db.refresh(db_fecha)
    return db_fecha

# ==================== CARRERA FINAL ====================
def get_resultados_carrera_final(db: Session, fecha_id: str) -> List[CarreraFinalResponse]:
    resultados = db.query(CarreraFinal)\
        .join(Piloto)\
        .filter(CarreraFinal.fecha_id == fecha_id)\
        .order_by(asc(CarreraFinal.posicion)).all()
    
    return [CarreraFinalResponse(
        id=str(r.id),
        posicion=r.posicion,
        puntos=r.puntos,
        presente=r.presente,
        vueltas=r.vueltas,
        tiempo=r.tiempo,
        excluido=r.excluido,
        diferencia_primero=r.diferencia_primero,
        piloto_nombre=r.piloto.nombre,
        piloto_pais=r.piloto.pais
    ) for r in resultados]

# ==================== CLASIFICACION ====================
def get_clasificacion_by_fecha(db: Session, fecha_id: str) -> List[ClasificacionResponse]:
    clasificacion = db.query(Clasificacion)\
        .join(Piloto)\
        .filter(Clasificacion.fecha_id == fecha_id)\
        .order_by(asc(Clasificacion.posicion)).all()
    
    return [ClasificacionResponse(
        id=str(c.id),
        tiempo=c.tiempo,
        posicion=c.posicion,
        vueltas=c.vueltas,
        sector_1=c.sector_1,
        sector_2=c.sector_2,
        sector_3=c.sector_3,
        diferencia_primero=c.diferencia_primero,
        piloto_nombre=c.piloto.nombre,
        piloto_pais=c.piloto.pais
    ) for c in clasificacion]

# ==================== ENTRENAMIENTOS ====================
def get_entrenamientos_by_fecha(db: Session, fecha_id: str, numero: Optional[int] = None) -> List[EntrenamientoResponse]:
    query = db.query(Entrenamiento)\
        .join(Piloto)\
        .filter(Entrenamiento.fecha_id == fecha_id)
    
    if numero:
        query = query.filter(Entrenamiento.numero == numero)
    
    entrenamientos = query.order_by(asc(Entrenamiento.posicion)).all()
    
    return [EntrenamientoResponse(
        id=str(e.id),
        numero=e.numero,
        tiempo=e.tiempo,
        posicion=e.posicion,
        vueltas=e.vueltas,
        sector_1=e.sector_1,
        sector_2=e.sector_2,
        sector_3=e.sector_3,
        diferencia_primero=e.diferencia_primero,
        piloto_nombre=e.piloto.nombre,
        piloto_pais=e.piloto.pais
    ) for e in entrenamientos]

# ==================== SERIES CLASIFICATORIAS ====================
def get_series_by_fecha(db: Session, fecha_id: str, numero: Optional[int] = None) -> List[SerieClasificatoriaResponse]:
    query = db.query(SerieClasificatoria)