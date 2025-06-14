# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import get_db
from models import *
from schemas import *
from crud import *

load_dotenv()

app = FastAPI(title="TurismoPista1100API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos para el admin
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== ENDPOINTS API ====================

# Campeonatos
@app.get("/api/campeonatos", response_model=List[CampeonatoResponse])
async def get_campeonatos(db = Depends(get_db)):
    return get_all_campeonatos(db)

@app.get("/api/campeonatos/{campeonato_id}", response_model=CampeonatoResponse)
async def get_campeonato(campeonato_id: str, db = Depends(get_db)):
    campeonato = get_campeonato_by_id(db, campeonato_id)
    if not campeonato:
        raise HTTPException(status_code=404, detail="Campeonato no encontrado")
    return campeonato

# Pilotos
@app.get("/api/pilotos", response_model=List[PilotoResponse])
async def get_pilotos(campeonato_id: Optional[str] = None, db = Depends(get_db)):
    if campeonato_id:
        return get_pilotos_by_campeonato(db, campeonato_id)
    return get_all_pilotos(db)

# Fechas
@app.get("/api/fechas", response_model=List[FechaResponse])
async def get_fechas(campeonato_id: Optional[str] = None, db = Depends(get_db)):
    if campeonato_id:
        return get_fechas_by_campeonato(db, campeonato_id)
    return get_all_fechas(db)

@app.get("/api/fechas/{fecha_id}", response_model=FechaResponse)
async def get_fecha(fecha_id: str, db = Depends(get_db)):
    fecha = get_fecha_by_id(db, fecha_id)
    if not fecha:
        raise HTTPException(status_code=404, detail="Fecha no encontrada")
    return fecha

# Resultados de carrera
@app.get("/api/carrera/{fecha_id}", response_model=List[CarreraFinalResponse])
async def get_resultados_carrera(fecha_id: str, db = Depends(get_db)):
    return get_resultados_carrera_final(db, fecha_id)

# Clasificación
@app.get("/api/clasificacion/{fecha_id}", response_model=List[ClasificacionResponse])
async def get_clasificacion(fecha_id: str, db = Depends(get_db)):
    return get_clasificacion_by_fecha(db, fecha_id)

# Entrenamientos
@app.get("/api/entrenamientos/{fecha_id}", response_model=List[EntrenamientoResponse])
async def get_entrenamientos(fecha_id: str, numero: Optional[int] = None, db = Depends(get_db)):
    return get_entrenamientos_by_fecha(db, fecha_id, numero)

# Posiciones del campeonato
@app.get("/api/campeonato/{campeonato_id}/posiciones", response_model=List[PosicionCampeonatoResponse])
async def get_posiciones_campeonato(campeonato_id: str, db = Depends(get_db)):
    return get_posiciones_by_campeonato(db, campeonato_id)

# Series clasificatorias
@app.get("/api/series/{fecha_id}", response_model=List[SerieClasificatoriaResponse])
async def get_series_clasificatorias(fecha_id: str, numero: Optional[int] = None, db = Depends(get_db)):
    return get_series_by_fecha(db, fecha_id, numero)

# Circuitos
@app.get("/api/circuitos", response_model=List[CircuitoResponse])
async def get_circuitos(db = Depends(get_db)):
    return get_all_circuitos(db)

# Horarios
@app.get("/api/horarios/{fecha_id}", response_model=List[HorarioResponse])
async def get_horarios(fecha_id: str, db = Depends(get_db)):
    return get_horarios_by_fecha(db, fecha_id)

# ==================== PANEL ADMIN ====================

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    with open("static/admin.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# CRUD para admin
@app.post("/admin/campeonatos", response_model=CampeonatoResponse)
async def create_campeonato(campeonato: CampeonatoCreate, db = Depends(get_db)):
    return create_campeonato_db(db, campeonato)

@app.post("/admin/pilotos", response_model=PilotoResponse)
async def create_piloto(piloto: PilotoCreate, db = Depends(get_db)):
    return create_piloto_db(db, piloto)

@app.post("/admin/fechas", response_model=FechaResponse)
async def create_fecha(fecha: FechaCreate, db = Depends(get_db)):
    return create_fecha_db(db, fecha)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)