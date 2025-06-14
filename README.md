# Turismo Pista 1100 - Backend API 🚗🏁

Este proyecto es una **API REST** desarrollada con **FastAPI** y **SQLAlchemy**, diseñada para gestionar información de la categoría de automovilismo **Turismo Pista 1100**, incluyendo campeonatos, pilotos, fechas, resultados y más.

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/turismo-pista-backend.git
cd turismo-pista-backend
```

### 2. Configurar el Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Copia el archivo `.env-example` y renómbralo a `.env`. Configura las variables de entorno según tu entorno (por ejemplo, conexión a la base de datos).

```bash
cp .env-example .env
```

### 4. Ejecutar la Aplicación

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`. Puedes acceder a la documentación interactiva en `http://localhost:8000/docs`.

## 📋 Características

- Gestión de **campeonatos**, **pilotos**, **fechas** y **circuitos**.
- Compatible con despliegue en **Supabase** o cualquier motor **PostgreSQL**.

## 🛠 Tecnologías

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-003087?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📦 Estructura del Proyecto

```
turismo-pista-backend/
├── main.py              # Punto de entrada principal de la API
├── models.py            # Definición de modelos ORM con SQLAlchemy
├── schemas.py           # Esquemas Pydantic para validación de datos
├── crud.py              # Funciones de acceso y manipulación de la base de datos
├── database.py          # Configuración de la conexión a la base de datos
├── static/              # Archivos estáticos (panel de administración, imágenes, etc.)
├── .env                 # Variables de entorno (no versionar)
└── requirements.txt     # Dependencias del proyecto
```

## 📝 Notas Adicionales

- Asegúrate de tener **PostgreSQL** instalado y configurado, o utiliza un servicio como **Supabase** para la base de datos.
- El archivo `.env` debe contener las credenciales y configuraciones necesarias para la conexión a la base de datos.

## 📚 Documentación

La API incluye documentación automática generada por FastAPI, accesible en:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
