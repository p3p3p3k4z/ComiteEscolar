# -*- coding: utf-8 -*-
# app/db.py
# Este archivo contiene la inicialización de la base de datos y la Base declarativa.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Configuracion

# Base declarativa para tus modelos (todos tus modelos heredarán de esta)
Base = declarative_base()

# Motor de la base de datos, usando la URL de conexión desde la configuración
engine = create_engine(Configuracion.URI_BASE_DE_DATOS)

# Fábrica de sesiones, para obtener nuevas sesiones de base de datos
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

