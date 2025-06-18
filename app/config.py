# -*- coding: utf-8 -*-
# app/config.py
# Este archivo contiene las configuraciones de la aplicación.

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
# Asegúrate de tener un archivo .env en la raíz de tu proyecto con:
# DATABASE_URL=postgresql://sgcpf_user:sgcpf_password@sgcpf_db:5432/sgcpf_db
load_dotenv()

class Configuracion:
    """Clase base de configuración para la aplicación SGCPF."""
    # Clave secreta para seguridad (puedes cambiarla por una más compleja o generarla dinámicamente)
    SECRETO_APP = os.environ.get('SECRET_KEY') or 'una-clave-super-secreta-que-debes-cambiar-en-produccion'

    # Configuración de la base de datos
    # Utiliza la variable de entorno DATABASE_URL.
    # Si la variable no está definida, usa un valor por defecto (útil para pruebas locales).
    # IMPORTANTE: Si tu aplicación Python corre dentro de Docker Compose en la misma red
    # que la base de datos, el host debe ser el nombre del servicio de la BD (ej. 'sgcpf_db').
    # Si la aplicación Python corre fuera de Docker, y el puerto está mapeado, usa 'localhost'.
    URI_BASE_DE_DATOS = os.environ.get('DATABASE_URL') or \
                        'postgresql://sgcpf_user:sgcpf_password@localhost:5432/sgcpf_db'

    # Desactiva el seguimiento de modificaciones de SQLAlchemy (consume memoria innecesariamente)
    SQLALCHEM_SEGUIMIENTO_MODIFICACIONES = False
