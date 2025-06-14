# models.py - Fixed version
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Date, Numeric, BigInteger, Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Campeonato(Base):
    __tablename__ = "campeonatos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    anio = Column(Integer, nullable=False)
    
    fechas = relationship("Fecha", back_populates="campeonato")
    pilotos_campeonato = relationship("PilotoCampeonato", back_populates="campeonato")
    posiciones_campeonato = relationship("PosicionCampeonato", back_populates="campeonato")

class Piloto(Base):
    __tablename__ = "pilotos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False, unique=True)
    pais = Column(String)
    
    pilotos_campeonato = relationship("PilotoCampeonato", back_populates="piloto")
    posiciones_campeonato = relationship("PosicionCampeonato", back_populates="piloto")
    carrera_final = relationship("CarreraFinal", back_populates="piloto")
    clasificacion = relationship("Clasificacion", back_populates="piloto")
    entrenamientos = relationship("Entrenamiento", back_populates="piloto")
    series_clasificatorias = relationship("SerieClasificatoria", back_populates="piloto")

class Circuito(Base):
    __tablename__ = "circuitos"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=text('now()'))
    nombre = Column(String)
    distancia = Column(Float)
    
    # FIXED: Changed back_populates to match the relationship name in Fecha model
    fechas = relationship("Fecha", back_populates="circuito_rel")

class Fecha(Base):
    __tablename__ = "fechas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campeonato_id = Column(UUID(as_uuid=True), ForeignKey("campeonatos.id"))
    nombre = Column(String, nullable=False)
    fecha_desde = Column(Date, nullable=False)
    fecha_hasta = Column(Date)
    circuito = Column(BigInteger, ForeignKey("circuitos.id"))  # This is the foreign key column
    
    campeonato = relationship("Campeonato", back_populates="fechas")
    # FIXED: This relationship name must match what Circuito.fechas back_populates references
    circuito_rel = relationship("Circuito", back_populates="fechas")
    carrera_final = relationship("CarreraFinal", back_populates="fecha")
    clasificacion = relationship("Clasificacion", back_populates="fecha")
    entrenamientos = relationship("Entrenamiento", back_populates="fecha")
    series_clasificatorias = relationship("SerieClasificatoria", back_populates="fecha")
    horarios = relationship("Horario", back_populates="fecha")
    imagenes = relationship("Imagen", back_populates="fecha")

class PilotoCampeonato(Base):
    __tablename__ = "pilotos_campeonato"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    piloto_id = Column(UUID(as_uuid=True), ForeignKey("pilotos.id"))
    campeonato_id = Column(UUID(as_uuid=True), ForeignKey("campeonatos.id"))
    numero_auto = Column(Integer)
    
    piloto = relationship("Piloto", back_populates="pilotos_campeonato")
    campeonato = relationship("Campeonato", back_populates="pilotos_campeonato")

class PosicionCampeonato(Base):
    __tablename__ = "posiciones_campeonato"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campeonato_id = Column(UUID(as_uuid=True), ForeignKey("campeonatos.id"))
    piloto_id = Column(UUID(as_uuid=True), ForeignKey("pilotos.id"))
    puntos_totales = Column(Integer, default=0)
    
    campeonato = relationship("Campeonato", back_populates="posiciones_campeonato")
    piloto = relationship("Piloto", back_populates="posiciones_campeonato")

class CarreraFinal(Base):
    __tablename__ = "carrera_final"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_id = Column(UUID(as_uuid=True), ForeignKey("fechas.id"))
    piloto_id = Column(UUID(as_uuid=True), ForeignKey("pilotos.id"))
    posicion = Column(Integer)
    puntos = Column(Integer, default=0)
    presente = Column(Boolean, default=True)
    vueltas = Column(BigInteger)
    tiempo = Column(Numeric)
    excluido = Column(Boolean, default=False)
    diferencia_primero = Column(Float)
    
    fecha = relationship("Fecha", back_populates="carrera_final")
    piloto = relationship("Piloto", back_populates="carrera_final")

class Clasificacion(Base):
    __tablename__ = "clasificacion"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_id = Column(UUID(as_uuid=True), ForeignKey("fechas.id"), nullable=False)
    piloto_id = Column(UUID(as_uuid=True), ForeignKey("pilotos.id"), nullable=False)
    tiempo = Column(Numeric)
    posicion = Column(Integer)
    vueltas = Column(BigInteger)
    sector_1 = Column(Float)
    sector_2 = Column(Float)
    sector_3 = Column(Float)
    diferencia_primero = Column(Float)
    
    fecha = relationship("Fecha", back_populates="clasificacion")
    piloto = relationship("Piloto", back_populates="clasificacion")

class Entrenamiento(Base):
    __tablename__ = "entrenamientos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_id = Column(UUID(as_uuid=True), ForeignKey("fechas.id"), nullable=False)
    numero = Column(Integer, nullable=False)
    piloto_id = Column(UUID(as_uuid=True), ForeignKey("pilotos.id"), nullable=False)
    tiempo = Column(Numeric)
    posicion = Column(Integer)
    vueltas = Column(BigInteger)
    sector_1 = Column(Float)
    sector_2 = Column(Float)
    sector_3 = Column(Float)
    diferencia_primero = Column(Float)
    
    fecha = relationship("Fecha", back_populates="entrenamientos")
    piloto = relationship("Piloto", back_populates="entrenamientos")

class SerieClasificatoria(Base):
    __tablename__ = "series_clasificatorias"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_id = Column(UUID(as_uuid=True), ForeignKey("fechas.id"))
    numero = Column(Integer, nullable=False)
    piloto_id = Column(UUID(as_uuid=True), ForeignKey("pilotos.id"))
    posicion = Column(Integer)
    puntos = Column(Integer, default=0)
    vueltas = Column(BigInteger)
    tiempo = Column(Numeric)
    mejor_tiempo = Column(Numeric)
    fecha_date = Column(Date)  # FIXED: Renamed to avoid conflict with relationship
    excluido = Column(Boolean, default=False)
    diferencia_primero = Column(Float)
    
    # FIXED: Now this can be named 'fecha' to match back_populates
    fecha = relationship("Fecha", back_populates="series_clasificatorias")
    piloto = relationship("Piloto", back_populates="series_clasificatorias")

class Horario(Base):
    __tablename__ = "horarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_id = Column(UUID(as_uuid=True), ForeignKey("fechas.id"), nullable=False)
    tipo_sesion = Column(String, nullable=False)
    horario = Column(DateTime(timezone=True), nullable=False)
    duracion = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=text('now()'))
    
    fecha = relationship("Fecha", back_populates="horarios")

class Imagen(Base):
    __tablename__ = "imagenes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_id = Column(UUID(as_uuid=True), ForeignKey("fechas.id"))
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    url_cloudinary = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('now()'))
    
    fecha = relationship("Fecha", back_populates="imagenes")

class PuntajePosicion(Base):
    __tablename__ = "puntaje_posicion"
    
    tipo = Column(String, primary_key=True)
    posicion = Column(Integer, primary_key=True)
    puntos = Column(Integer, nullable=False)