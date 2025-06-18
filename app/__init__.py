# -*- coding: utf-8 -*-
# Este archivo inicializa la base de datos para toda la aplicación.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Configuracion # Importa tu clase de configuración, ahora con nombre en español

# Base declarativa para tus modelos (donde tus clases de modelo heredarán)
Base = declarative_base()

# Motor de la base de datos, usando la URL de conexión desde la configuración
engine = create_engine(Configuracion.URI_BASE_DE_DATOS) # Usa el nombre de variable en español

# Fábrica de sesiones, para obtener nuevas sesiones de base de datos
Session = sessionmaker(bind=engine)

# Puedes añadir otras inicializaciones o configuraciones globales aquí si es necesario.
